# Dockerfile para API FastAPI + Selenium + Chrome
FROM python:3.11-slim

# Evita prompts do apt
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema e Chrome
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libxrandr2 \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 \
    fonts-liberation libgbm-dev libxss1 \
    && rm -rf /var/lib/apt/lists/*

# Instala o Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -fy \
    && rm google-chrome-stable_current_amd64.deb

# Define o caminho binário do Chrome
ENV CHROME_BIN=/usr/bin/google-chrome

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto
COPY pyproject.toml poetry.lock.

# Instala o Poetry e dependências do projeto
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Copia código-fonte restante
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
