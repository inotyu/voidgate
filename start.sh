#!/bin/sh

echo "==========================================="
echo "🚀 Iniciando o VoidGate na ShardCloud..."
echo "==========================================="

# Carrega variáveis do .env de forma segura
echo "Carregando variáveis do .env..."
if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi

# Limpa a pasta de libs antigas
echo "🧹 Limpando libs antigas..."
rm -rf /app/.lib/*

# Instala dependências
echo "🔍 Instalando dependências..."
pip install --no-cache-dir --upgrade -r requirements.txt --target /app/.lib

# Ajusta o PYTHONPATH pra usar libs do target
export PYTHONPATH=/app/.lib:$PYTHONPATH

# Roda a aplicação
echo "✅ Tudo pronto! Rodando aplicação..."
exec python run.py
