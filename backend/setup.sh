#!/bin/bash

# Script para configurar e iniciar o backend PHP
echo "Configurando Backend PHP Musician AI..."

# Verificar se o Composer está instalado
if ! command -v composer &> /dev/null; then
    echo "Composer não encontrado. Instalando..."
    curl -sS https://getcomposer.org/installer | php
    sudo mv composer.phar /usr/local/bin/composer
fi

# Instalar dependências
echo "Instalando dependências do Composer..."
composer install

# Copiar arquivo de configuração se não existir
if [ ! -f ".env" ]; then
    cp env.example .env
    echo "Arquivo .env criado. Configure as variáveis de banco de dados."
fi

# Verificar se MySQL está rodando
if ! pgrep -x "mysqld" > /dev/null; then
    echo "MySQL não está rodando. Inicie o MySQL antes de continuar."
    exit 1
fi

# Executar script SQL para criar banco e tabelas
echo "Configurando banco de dados..."
mysql -u root -p < database/schema.sql

echo "Backend PHP configurado com sucesso!"
echo "Para iniciar o servidor, execute: composer start"
echo "O servidor estará disponível em: http://localhost:8000"
