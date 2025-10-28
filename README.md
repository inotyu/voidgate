# VoidGate 🚪🔒

### Selecione seu Idioma
[![Português](https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/45px-Flag_of_Brazil.svg.png)](#-português)  
[![English](https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg/50px-Flag_of_the_United_Kingdom_%283-5%29.svg.png)](#-english)

## 🇧🇷 Português

### 🚀 Visão Geral
O VoidGate é um sistema de gerenciamento de acesso e conteúdo baseado na web, desenvolvido com Python (Flask) e tecnologias modernas. Oferece um painel de controle robusto para gerenciamento de usuários, autenticação segura e armazenamento em nuvem com Supabase.

### ✨ Recursos
- Autenticação de usuários segura
- Painel administrativo
- Armazenamento em nuvem com Supabase
- Banco de dados PostgreSQL
- Interface responsiva
- Gerenciamento de sessões
- Limpeza automática de conteúdo expirado
- API RESTful

### 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/inotyu/voidgate.git
   cd voidgate
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=sua_chave_secreta_aqui
   DATABASE_URL=postgresql://usuario:senha@localhost/nome_do_banco
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_KEY=sua_chave_do_supabase
   ```

5. **Inicialize o banco de dados:**
   ```bash
   flask db upgrade
   ```

6. **Execute a aplicação:**
   ```bash
   python run.py
   ```
   A aplicação estará disponível em `http://localhost:5000`

### 🎮 Como Usar
1. Acesse a aplicação no navegador
2. Faça login com suas credenciais
3. Acesse o painel administrativo
4. Gerencie usuários e permissões
5. Acompanhe as atividades do sistema

## 🇬🇧 English

### 🚀 Overview
VoidGate is a web-based access and content management system, built with Python (Flask) and modern technologies. It provides a robust control panel for user management, secure authentication, and cloud storage with Supabase.

### ✨ Features
- Secure user authentication
- Admin dashboard
- Cloud storage with Supabase
- PostgreSQL database
- Responsive interface
- Session management
- Automatic cleanup of expired content
- RESTful API

### 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/inotyu/voidgate.git
   cd voidgate
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory with the following variables:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

5. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

6. **Run the application:**
   ```bash
   python run.py
   ```
   The application will be available at `http://localhost:5000`

### 🎮 Usage
1. Open the application in your web browser
2. Log in with your credentials
3. Access the admin dashboard
4. Manage users and permissions
5. Monitor system activities

### 📝 Licença / License
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👥 Contribuição / Contributing
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
Contributions are welcome! Feel free to open issues and submit pull requests.
