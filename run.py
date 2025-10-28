from dotenv import load_dotenv
import os
from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from datetime import datetime, timedelta, timezone
import re

load_dotenv()
app = create_app()

# Função para limpar vídeos expirados
def cleanup_expired_videos():
    from supabase import create_client

    supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

    try:
        # Corrigir timestamps antigos
        problematic_videos = supabase.table('videos').select('id, expiration_date').execute()
        for vid in problematic_videos.data:
            if vid.get('expiration_date') and isinstance(vid['expiration_date'], str):
                if vid['expiration_date'].endswith('Z'):
                    corrected_date = vid['expiration_date'][:-1]
                    supabase.table('videos').update({'expiration_date': corrected_date}).eq('id', vid['id']).execute()
                    print(f"Timestamp corrigido para vídeo {vid['id']}")
        print("Dados de timestamp antigos corrigidos no banco")
    except Exception as e:
        print(f"Erro ao corrigir dados antigos: {e}")

    # Deletar vídeos expirados
    expired_videos = supabase.table('videos').select('*').lt('expiration_date', datetime.now(timezone.utc).isoformat()).execute()
    for vid in expired_videos.data:
        file_url = vid['file_url']
        match = re.search(r'/storage/v1/object/public/voidgate/(.+)', file_url)
        if match:
            file_path = match.group(1)
            try:
                supabase.storage.from_('voidgate').remove([file_path])
                print(f"Deleted from storage: {file_path}")
            except Exception as e:
                print(f"Error deleting from storage: {e}")
        supabase.table('videos').delete().eq('id', vid['id']).execute()
        print(f"Deleted from DB: {vid['id']}")

    # Set expiration for videos without it
    supabase.table('videos').update({
        'expiration_date': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }).is_('expiration_date', 'null').execute()
    print("Set expiration for videos without it")

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=cleanup_expired_videos,
    trigger=IntervalTrigger(minutes=5),
    id='cleanup_expired_videos',
    name='Cleanup Expired Videos',
    replace_existing=True
)
scheduler.start()  # ❌ Removido daemon=True
atexit.register(scheduler.shutdown)  # ✅ fecha o scheduler ao sair

if __name__ == "__main__":
    print("🚀 Iniciando o VoidGate na ShardCloud (porta 80)...")
    app.run(host="0.0.0.0", port=80, debug=False)
