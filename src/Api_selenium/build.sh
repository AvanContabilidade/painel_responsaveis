#!/usr/bin/env bash
pip install poetry
poetry install


#instalação chrome

# Instala o Chrome manualmente
mkdir -p /opt/chrome
curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb
apt-get update && apt-get install -y ./chrome.deb
ln -s /usr/bin/google-chrome /opt/chrome/chrome

# Instala o ChromeDriver compatível
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
curl -sSL "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -o chromedriver.zip
unzip chromedriver.zip
chmod +x chromedriver
mv chromedriver /opt/chrome/chromedriver