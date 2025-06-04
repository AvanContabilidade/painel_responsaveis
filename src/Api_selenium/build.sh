#!/bin/bash
set -e

# Instala dependências do sistema
apt-get update && apt-get install -y \
    wget \
    unzip \
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
    gnupg \
    curl \
    xvfb  # Adicionado X virtual framebuffer

# Instala Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update && apt-get install -y google-chrome-stable

# Verifica a instalação
echo "Chrome instalado em: $(which google-chrome)"
echo "Versão do Chrome: $(google-chrome --version)"

# Instala Poetry e dependências do Python
pip install poetry
poetry install