#!/bin/bash

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

# Instala Google Chrome
mkdir -p /opt/chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
dpkg -i chrome.deb || apt-get install -fy
rm chrome.deb
ln -s /usr/bin/google-chrome /opt/chrome/chrome

# Instala Poetry e dependências
pip install poetry
poetry install
