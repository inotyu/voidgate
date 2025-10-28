# Start.ps1 - Script para iniciar o VoidGate

# Configuração de ambiente
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "production"

# Carrega as variáveis do .env
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=')
    if ($name -and $value) {
        [System.Environment]::SetEnvironmentVariable($name, $value.Trim())
    }
}

# Verifica se o Python está instalado
try {
    $pythonVersion = python --version
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Erro: Python não encontrado. Por favor, instale o Python 3.8 ou superior." -ForegroundColor Red
    exit 1
}

# Instala dependências
Write-Host "Instalando/Atualizando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# Inicia o servidor
Write-Host "Iniciando o VoidGate..." -ForegroundColor Green
Write-Host "Acesse: http://localhost:80" -ForegroundColor Cyan
python run.py
