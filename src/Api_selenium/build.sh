#!/bin/bash
set -e

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
    curl

# Install Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update && sudo apt-get install -y google-chrome-stable
which google-chrome 

# Instala Poetry e dependências
pip install poetry
poetry install


