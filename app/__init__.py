import os
from flask import Flask, redirect, url_for, render_template, session
from .auth import auth_bp
from .panel import panel_bp
from .api import api_bp
from flask import send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

def create_app():
    app = Flask(__name__)
    app.template_folder = '../templates'  # Aponta para templates/ no diretório raiz
    app.static_folder = '../static'  # Aponta para static/ no diretório raiz
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
    app.config['SUPABASE_KEY'] = os.getenv('SUPABASE_KEY')

    # Session configuration for better security
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(panel_bp, url_prefix='/panel')
    app.register_blueprint(api_bp, url_prefix='/api')

        # Rota raiz: exibe index.html
    @app.route('/')
    def index():
        return render_template('index.html')

    # Rota alternativa para index.html (redireciona para a raiz)
    @app.route('/index.html')
    def index_html():
        return redirect(url_for('index'))

    # Rota para /inicio (redireciona para a raiz)
    @app.route('/inicio')
    def inicio():
        return redirect(url_for('index'))

    # Rota para servir uploads locais
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory('../uploads', filename)

    # Handler para erro 404
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # Função para limpar vídeos expirados
    def cleanup_expired_videos():
        from supabase import create_client
        import re
        from datetime import datetime, timedelta

        supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

        # Buscar vídeos expirados (com expiration_date definido)
        expired_videos = supabase.table('videos').select('*').lt('expiration_date', datetime.now()).execute()

        for vid in expired_videos.data:
            # Deletar do storage
            file_url = vid['file_url']
            match = re.search(r'/storage/v1/object/public/voidgate/(.+)', file_url)
            if match:
                file_path = match.group(1)
                try:
                    supabase.storage.from_('voidgate').remove([file_path])
                    print(f"Deleted from storage: {file_path}")
                except Exception as e:
                    print(f"Error deleting from storage: {e}")

            # Deletar do banco
            supabase.table('videos').delete().eq('id', vid['id']).execute()
            print(f"Deleted from DB: {vid['id']}")

        # Nota: Vídeos existentes sem expiration_date não serão deletados automaticamente
        # Você pode deletar manualmente ou definir expiration_date no banco

    return app
