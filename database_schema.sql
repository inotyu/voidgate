-- SQL para criar tabelas no Supabase (PostgreSQL)

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    avatar TEXT, -- URL ou inicial
    plan VARCHAR(20) DEFAULT 'free', -- free, premium, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de vídeos
CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL, -- Link do Backblaze
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expiration_date TIMESTAMP WITH TIME ZONE, -- Pode ser NULL se não expirar
    size BIGINT, -- Tamanho em bytes
    status VARCHAR(20) DEFAULT 'active' -- active, expired, deleted
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_videos_user_id ON videos(user_id);
CREATE INDEX IF NOT EXISTS idx_videos_expiration ON videos(expiration_date);

-- Inserir usuário de exemplo (remova após desenvolvimento)
-- INSERT INTO users (username, email, password_hash, avatar, plan)
-- VALUES ('joao_silva', 'joao@example.com', 'hashed_password', 'JS', 'free');
