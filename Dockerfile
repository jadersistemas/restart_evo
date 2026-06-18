# Usar uma imagem oficial e leve do Python
FROM python:3.11-slim

# Instalar o Docker CLI e o pacote de fuso horário (tzdata)
RUN apt-get update && \
    apt-get install -y docker.io tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configura o fuso horário para o Brasil (fundamental para o agendador funcionar na hora certa)
ENV TZ="America/Sao_Paulo"

# Definir a pasta de trabalho
WORKDIR /app

# Copiar nosso script Python para a imagem
COPY restart_evolution.py .

# Rodar o Python em modo 'unbuffered' (-u) para vermos os logs no Easypanel em tempo real
CMD ["python", "-u", "restart_evolution.py"]
