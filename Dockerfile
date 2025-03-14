# Use uma imagem base do Python
FROM python:3.9-slim

# Instalar dependências do sistema para build
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    libpython3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para dentro do contêiner
COPY . .

# Atualizar o pip
RUN pip install --upgrade pip

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/openai/whisper.git
# Expor a porta do app, se necessário
EXPOSE 5000

# Comando para rodar o app
CMD ["python3", "main.py"]
