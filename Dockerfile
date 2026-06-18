# Usar uma imagem oficial e leve do Python
FROM python:3.11-slim

# Instalar o Docker CLI para permitir que este container execute comandos no Docker host
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Definir a pasta de trabalho
WORKDIR /app

# Copiar nosso script Python para a imagem
COPY restart_evolution.py .

# Rodar o Python em modo 'unbuffered' (-u) para vermos os logs no Easypanel em tempo real
CMD ["python", "-u", "restart_evolution.py"]
