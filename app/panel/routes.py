from flask import render_template, session, redirect, url_for, request, flash, jsonify
from supabase import create_client, Client
from . import panel_bp
import os
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializar Supabase
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

@panel_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    username = session['username']

    # Buscar dados do usuário
    user = supabase.table('users').select('*').eq('id', user_id).execute()
    if user.data:
        user_data = user.data[0]
        email = user_data['email']
        created_at = datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00')) if user_data['created_at'] else None
    else:
        email = 'Email não encontrado'
        created_at = None

    # Buscar vídeos do usuário (apenas não expirados)
    videos = supabase.table('videos').select('*').eq('user_id', user_id).gte('expiration_date', datetime.now(timezone.utc).isoformat()).execute()

    # Converter datas ISO para datetime e calcular minutos restantes
    if videos.data:
        for vid in videos.data:
            if vid.get('upload_date'):
                try:
                    vid['upload_date'] = datetime.fromisoformat(vid['upload_date'].replace('Z', '+00:00'))
                except Exception:
                    pass
            if vid.get('expiration_date') and isinstance(vid['expiration_date'], str):
                try:
                    vid['expiration_date'] = datetime.fromisoformat(vid['expiration_date'].replace('Z', '+00:00'))
                    # Calcular minutos restantes
                    now = datetime.now(timezone.utc)
                    remaining_seconds = (vid['expiration_date'] - now).total_seconds()
                    vid['remaining_minutes'] = max(0, int(remaining_seconds / 60))
                except Exception:
                    vid['remaining_minutes'] = 0

    # Calcular totais
    total_videos = len(videos.data) if videos.data else 0
    total_size_bytes = sum(vid.get('size', 0) for vid in videos.data) if videos.data else 0
    total_size_mb = total_size_bytes / (1024 * 1024)

    # Estatísticas dinâmicas
    total_storage_mb = 10 * 1024  # 10 GB
    used_mb = total_size_mb
    percentage = (used_mb / total_storage_mb) * 100 if total_storage_mb > 0 else 0
    free_mb = total_storage_mb - used_mb

    avatar_url = user_data.get('avatar') if user.data else None

    return render_template('painel.html', videos=videos.data, total_videos=total_videos, total_size_mb=total_size_mb, username=username, email=email, created_at=created_at, avatar_url=avatar_url, used_percentage=percentage, free_space_mb=free_mb)

@panel_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Verificar se há arquivo
        if 'video' not in request.files:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Nenhum arquivo enviado.'}), 400
            flash('Nenhum arquivo enviado.', 'error')
            return redirect(url_for('panel.upload'))

        file = request.files['video']
        if file.filename == '':
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Nenhum arquivo selecionado.'}), 400
            flash('Nenhum arquivo selecionado.', 'error')
            return redirect(url_for('panel.upload'))

        # Get custom name from form
        custom_name = request.form.get('videoName', '').strip()
        video_name = custom_name if custom_name else file.filename

        # Ler arquivo em bytes e verificar tamanho (máx 100MB)
        file_bytes = file.read()
        size = len(file_bytes)
        if size > 100 * 1024 * 1024:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Arquivo muito grande (máx 100MB).'}), 400
            flash('Arquivo muito grande (máx 100MB).', 'error')
            return redirect(url_for('panel.upload'))

        # Upload para Supabase Storage
        bucket_name = 'voidgate'
        import time
        file_path = f"{session['user_id']}/{int(time.time())}_{file.filename}"
        try:
            upload_result = supabase.storage.from_(bucket_name).upload(file_path, file_bytes, {'content-type': file.content_type})
            if upload_result:
                # Gerar URL público
                public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)

                # Calcular expiração (1 hora)
                expiration_date = datetime.now(timezone.utc) + timedelta(hours=1)

                # Salvar no banco
                new_video = {
                    'user_id': session['user_id'],
                    'name': video_name,  # Use custom name or file.filename
                    'file_url': public_url,
                    'size': size,
                    'expiration_date': expiration_date.isoformat()
                }

                result = supabase.table('videos').insert(new_video).execute()
                if result.data:
                    # Buscar username do usuário
                    user_resp = supabase.table('users').select('username').eq('id', session['user_id']).single().execute()
                    username = user_resp.data.get('username', 'user') if user_resp.data else 'user'
                    
                    # Criar URL amigável (sem ID para ficar mais curta)
                    video_name_slug = ''.join(c if c.isalnum() or c in '-_' else '-' for c in video_name.lower().replace(' ', '-'))
                    video_url = url_for('api.serve_video', path=f"{username}/{video_name_slug}", _external=True)
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({
                            'success': True, 
                            'message': 'Vídeo enviado com sucesso!', 
                            'expires_in': 3600,
                            'video_url': video_url
                        })
                    flash('Vídeo enviado com sucesso! Expira em 1 hora.', 'success')
                    return redirect(url_for('panel.dashboard'))
                else:
                    error_msg = 'Erro ao salvar vídeo no banco.'
            else:
                error_msg = 'Erro no upload para o storage.'
        except Exception as e:
            error_msg = f'Erro no upload: {str(e)}'

        # Se chegou aqui é porque houve erro
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': error_msg}), 500
        flash(error_msg, 'error')
        return redirect(url_for('panel.upload'))

    return render_template('upload.html')

@panel_bp.route('/update_username', methods=['POST'])
def update_username():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({'error': 'Username required'}), 400

    new_username = data['username'].strip()
    if not new_username:
        return jsonify({'error': 'Username inválido'}), 400

    # Atualizar no Supabase
    try:
        result = supabase.table('users').update({'username': new_username}).eq('id', session['user_id']).execute()
        if result.data:
            session['username'] = new_username
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Falha ao atualizar'}), 500


@panel_bp.route('/update_avatar', methods=['POST'])
def update_avatar():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    if 'avatar' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'error': 'Arquivo inválido'}), 400

    # Limite de 2MB
    file_bytes = file.read()
    if len(file_bytes) > 2 * 1024 * 1024:
        return jsonify({'error': 'Tamanho máximo 2MB'}), 400

    import base64
    data_uri = f"data:{file.content_type};base64,{base64.b64encode(file_bytes).decode()}"
    try:
        supabase.table('users').update({'avatar': data_uri}).eq('id', session['user_id']).execute()
        return jsonify({'success': True, 'avatar_url': data_uri})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@panel_bp.route('/update_password', methods=['POST'])
def update_password():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    required = {'current', 'new'}
    if not data or not required.issubset(data):
        return jsonify({'error': 'Campos obrigatórios'}), 400

    current = data['current']
    new = data['new']

    # Buscar usuário
    user_resp = supabase.table('users').select('password_hash').eq('id', session['user_id']).single().execute()
    if not user_resp.data:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    if not check_password_hash(user_resp.data['password_hash'], current):
        return jsonify({'error': 'Senha atual incorreta'}), 400

    new_hash = generate_password_hash(new)
    try:
        upd = supabase.table('users').update({'password_hash': new_hash}).eq('id', session['user_id']).execute()
        if upd.data:
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Falha ao atualizar'}), 500


@panel_bp.route('/delete_video/<video_id>', methods=['POST'])
def delete_video(video_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Get video details to delete from storage
    video = supabase.table('videos').select('file_url').eq('id', video_id).eq('user_id', session['user_id']).execute()
    if video.data:
        file_url = video.data[0]['file_url']
        # Extract file path from URL (assuming URL format)
        # Example: https://bucket.supabase.co/storage/v1/object/public/voidgate/user_id/filename
        # Need to parse the path
        import re
        match = re.search(r'/storage/v1/object/public/voidgate/(.+)', file_url)
        if match:
            file_path = match.group(1)
            try:
                supabase.storage.from_('voidgate').remove([file_path])
            except Exception as e:
                print(f"Error deleting from storage: {e}")

    # Delete from database
    supabase.table('videos').delete().eq('id', video_id).eq('user_id', session['user_id']).execute()
    return redirect(url_for('panel.dashboard'))
