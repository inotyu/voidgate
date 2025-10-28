from flask import jsonify, request, redirect, abort
from supabase import create_client, Client
from . import api_bp
import os
import requests
import json

# Inicializar Supabase (se necessário para outros endpoints)
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# Credenciais do B2 do .env
B2_KEY_ID = os.getenv('B2_APPLICATION_KEY_ID')
B2_APP_KEY = os.getenv('B2_APPLICATION_KEY')
B2_BUCKET_NAME = os.getenv('BUCKET_NAME')  # Adicione BUCKET_NAME no .env se não estiver

# URLs da API do B2
B2_AUTH_URL = "https://api.backblazeb2.com/b2api/v2/b2_authorize_account"
B2_DOWNLOAD_AUTH_URL = "https://api.backblazeb2.com/b2api/v2/b2_get_download_authorization"

def get_b2_auth_token():
    """Obtém o token de autorização do B2."""
    response = requests.get(
        B2_AUTH_URL,
        auth=(B2_KEY_ID, B2_APP_KEY),
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        return data['authorizationToken'], data['apiUrl'], data['downloadUrl']
    else:
        raise Exception(f"Erro na autenticação B2: {response.status_code} - {response.text}")

def get_bucket_id():
    """Obtém o bucketId real do B2 com base no nome do bucket."""
    auth_token, api_url, _ = get_b2_auth_token()
    headers = {"Authorization": auth_token}
    response = requests.post(
        f"{api_url}/b2api/v2/b2_list_buckets",
        headers=headers,
        timeout=10
    )
    if response.status_code == 200:
        buckets = response.json()['buckets']
        for bucket in buckets:
            if bucket['bucketName'] == B2_BUCKET_NAME:
                return bucket['bucketId']
    raise Exception("Bucket não encontrado ou credenciais inválidas.")

def generate_download_link(file_name):
    """Gera link temporário de download para o arquivo."""
    try:
        auth_token, api_url, download_url = get_b2_auth_token()
        bucket_id = get_bucket_id()  # Obter bucketId dinamicamente
        
        # Preparar payload para autorização de download
        payload = {
            "bucketId": bucket_id,
            "fileNamePrefix": file_name,
            "validDurationInSeconds": 3600,  # 1 hora
            "b2ContentDisposition": "attachment"  # Opcional: forçar download
        }
        
        headers = {
            "Authorization": auth_token,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{api_url}/b2api/v2/b2_get_download_authorization",
            data=json.dumps(payload),
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            # Construir o link completo
            temp_url = f"{download_url}/file/{B2_BUCKET_NAME}/{file_name}?Authorization={data['authorizationToken']}"
            return temp_url
        else:
            raise Exception(f"Erro ao gerar link: {response.status_code} - {response.text}")
    except Exception as e:
        raise Exception(f"Erro geral: {str(e)}")

@api_bp.route('/v/<path:path>.mp4')
def serve_video(path):
    """Rota para streaming de vídeo com URL amigável.
    
    Formatos suportados:
    - /v/<username>/<video_name>.mp4 (curto, busca por nome)
    - /v/<username>/<video_name>_<video_id>.mp4 (com ID como fallback)
    """
    parts = path.split('/')
    if len(parts) != 2:
        return abort(404)
    
    username, video_part = parts
    
    # Buscar usuário pelo username
    user_resp = supabase.table('users').select('id').eq('username', username.lower()).single().execute()
    if not user_resp.data:
        return abort(404)
    
    user_id = user_resp.data['id']
    
    # Primeiro tentar buscar pelo nome do vídeo (URL curta)
    if '_' not in video_part:
        video_resp = supabase.table('videos').select('file_url, name, user_id, id') \
            .eq('user_id', user_id) \
            .ilike('name', video_part) \
            .single().execute()
        
        if video_resp.data:
            # Verificar se encontrou exatamente o nome (case insensitive)
            if video_resp.data['name'].lower() == video_part.lower():
                file_url = video_resp.data['file_url']
                # Fazer proxy do arquivo
                return proxy_video(file_url)
        
        return abort(404)
    
    # Fallback: tentar pelo ID (formato antigo)
    video_id = video_part.split('_')[-1]
    video_resp = supabase.table('videos').select('file_url, name, user_id').eq('id', video_id).single().execute()
        
    if not video_resp.data:
        return abort(404)
    
    # Verificar se o username corresponde
    if video_resp.data['user_id'] != user_id:
        return abort(404)
    
    file_url = video_resp.data['file_url']
    return proxy_video(file_url)

def proxy_video(file_url):
    """Faz proxy do arquivo para não expor a URL real"""
    from flask import Response, stream_with_context
    import requests

    def generate():
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

    return Response(stream_with_context(generate()), mimetype='video/mp4')


@api_bp.route('/get_link/<path:file_name>', methods=['GET'])
def get_temporary_link(file_name):
    """Endpoint para gerar link temporário de download."""
    try:
        temp_url = generate_download_link(file_name)
        return jsonify({"url_temporaria": temp_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
