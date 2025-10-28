from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import create_client, Client
from . import auth_bp
import os

# Inicializar Supabase
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['email']  # Renamed for clarity, it's username or email
        password = request.form['password']

        # Try to find user by email or username
        user = supabase.table('users').select('*').eq('email', login_input).execute()
        if not user.data:
            # If not found by email, try by username
            user = supabase.table('users').select('*').eq('username', login_input).execute()

        if user.data and check_password_hash(user.data[0]['password_hash'], password):
            session['user_id'] = user.data[0]['id']
            session['username'] = user.data[0]['username']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('panel.dashboard'))
        else:
            flash('Usuário/email ou senha incorretos.', 'error')

    return render_template('autenticacao.html', form_type='login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')  # Campo oculto ou ajustar no template

        # Verificar se senhas coincidem
        if password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return redirect(url_for('auth.register'))

        # Verificar se usuário já existe
        existing_user = supabase.table('users').select('id').eq('email', email).execute()
        if existing_user.data:
            flash('Email já cadastrado.', 'error')
            return redirect(url_for('auth.register'))

        # Hash da senha
        hashed_password = generate_password_hash(password)

        # Criar usuário
        new_user = {
            'username': username,
            'email': email,
            'password_hash': hashed_password
        }

        result = supabase.table('users').insert(new_user).execute()
        if result.data:
            # Logar o usuário automaticamente
            user = supabase.table('users').select('*').eq('email', email).execute()
            if user.data:
                session['user_id'] = user.data[0]['id']
                session['username'] = user.data[0]['username']
            flash('Conta criada com sucesso! Bem-vindo!', 'success')
            return redirect(url_for('panel.dashboard'))
        else:
            flash('Erro ao criar conta.', 'error')

    return render_template('autenticacao.html', form_type='register')

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form['email']
    username = request.form['username']
    new_password = request.form['new_password']

    if not email or not username or not new_password:
        flash('Todos os campos são obrigatórios.', 'error')
        return redirect(url_for('auth.login'))

    # Verificar se o usuário existe com email e username
    user = supabase.table('users').select('*').eq('email', email).eq('username', username).execute()

    if not user.data:
        flash('Usuário ou email não encontrado.', 'error')
        return redirect(url_for('auth.login'))

    # Hash da nova senha
    hashed_password = generate_password_hash(new_password)

    # Atualizar senha
    supabase.table('users').update({'password_hash': hashed_password}).eq('id', user.data[0]['id']).execute()

@auth_bp.route('/logout')
def logout():
    session.clear()  # Clear entire session to ensure no remnants
    flash('Logout realizado.', 'info')
    return redirect(url_for('auth.login'))
