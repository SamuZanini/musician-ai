#!/bin/bash

# Script para iniciar o serviço de IA
echo "Iniciando Serviço de IA Musician..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Copiar arquivo de configuração se não existir
if [ ! -f ".env" ]; then
    cp env.example .env
    echo "Arquivo .env criado. Configure as variáveis conforme necessário."
fi

# Iniciar o serviço
echo "Iniciando servidor de IA na porta 8001..."
python3 main.py
