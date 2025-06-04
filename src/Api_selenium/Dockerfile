FROM python:3.11-slim

# Instala dependências do Chrome e Chromium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends

# Instala o Google Chrome estável
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update && apt-get install -y google-chrome-stable

RUN google-chrome --version
RUN chromedriver --version

# Verifica o caminho do chrome instalado (opcional)
RUN ls -l /usr/bin/google-chrome



# Copia requirements e instala python libs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia app
COPY . /app
WORKDIR /app

EXPOSE 10000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "10000"]
