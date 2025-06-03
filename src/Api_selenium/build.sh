#!/bin/bash

# Instala dependências do sistema
apt-get update && apt-get install -y \
    wget \
    unzip \
    libgbm-dev \
    libxss1 \
    libasound2 \
    libnspr4 \
    libnss3 \
    fonts-liberation

# Instala Chrome
mkdir -p /opt/chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
apt-get install -y ./chrome.deb
rm chrome.deb
ln -s /usr/bin/google-chrome /opt/chrome/chrome

# Instala Chromium e chromedriver
apt-get update
apt-get install -y chromium-browser chromium-chromedriver

# Instala Poetry e dependências do projeto
pip install poetry
poetry install