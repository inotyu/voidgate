# Sync Music Player 🎵

### Selecione seu Idioma
[![Português](https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/45px-Flag_of_Brazil.svg.png)](#-português)  
[![English](https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg/50px-Flag_of_the_United_Kingdom_%283-5%29.svg.png)](#-english)

## 🇧🇷 Português

### 🚀 Visão Geral
O Sync Music Player é uma aplicação web que permite que múltiplos usuários criem e compartilhem playlists do YouTube sincronizadas em tempo real. Desenvolvido com Python (Flask) e JavaScript, oferece uma experiência fluida para escuta colaborativa de músicas.

### ✨ Recursos
- Sincronização de playlist em tempo real
- Salas para múltiplos usuários
- Controles intuitivos de reprodução
- Design responsivo
- Integração com vídeos do YouTube
- Autenticação de usuários
- Banco de dados PostgreSQL
- Armazenamento em nuvem com Supabase

### 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/inotyu/sync_msc.git
   cd sync_msc
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
2. Crie uma conta ou faça login
3. Crie uma nova sala ou entre em uma existente
4. Adicione vídeos do YouTube à playlist
5. Controle a reprodução para todos os usuários da sala

## 🇬🇧 English

### 🚀 Overview
Sync Music Player is a web application that allows multiple users to create and share synchronized YouTube playlists in real-time. Built with Python (Flask) and JavaScript, it provides a seamless experience for collaborative music listening.

### ✨ Features
- Real-time playlist synchronization
- Multiple user rooms for collaborative listening
- Intuitive playback controls
- Responsive design
- YouTube video integration
- User authentication
- PostgreSQL database
- Cloud storage with Supabase

### 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/inotyu/sync_msc.git
   cd sync_msc
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
2. Create an account or log in
3. Create a new room or join an existing one
4. Add YouTube video URLs to the playlist
5. Control playback for all users in the room

### 📝 Licença / License
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👥 Contribuição / Contributing
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
Contributions are welcome! Feel free to open issues and submit pull requests.
