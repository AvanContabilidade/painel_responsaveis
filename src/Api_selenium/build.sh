#!/usr/bin/env bash
set -o errexit

STORAGE_DIR="/opt/render/project/.render"
CHROME_DIR="$STORAGE_DIR/chrome"
CHROME_DEB="google-chrome-stable_current_amd64.deb"

if [[ ! -d "$CHROME_DIR" ]]; then
  echo "... Baixando o Chrome"
  mkdir -p "$CHROME_DIR"
  cd "$CHROME_DIR"
  wget -q "https://dl.google.com/linux/direct/$CHROME_DEB"
  dpkg -x "$CHROME_DEB" "$CHROME_DIR"
  rm "$CHROME_DEB"
else
  echo "... Usando o Chrome a partir do cache"
fi

# Retorna ao diretório do projeto
cd "$HOME/project/src"

# Dependências do sistema necessárias para o Chrome rodar
apt-get update && apt-get install -y \
    libgbm-dev \
    libxss1 \
    libasound2 \
    libnspr4 \
    libnss3 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    ca-certificates \
    curl \
    unzip

# Instala Poetry e dependências do projeto
pip install poetry
poetry install
