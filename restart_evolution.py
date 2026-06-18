import time
import datetime
import subprocess
import os
import urllib.request
import json

# Pega os horários via variável de ambiente (.env) ou usa o padrão
horarios_env = os.environ.get("HORARIOS_REINICIO", "07:00,13:00")
HORARIOS_REINICIO = [h.strip() for h in horarios_env.split(",")]

# O nome do serviço no Easypanel (ex: evolution)
NOME_SERVICO = os.environ.get("NOME_SERVICO", "evolution")

# Dados da API passados via variáveis de ambiente (.env) no Easypanel
# Deixei os seus dados como padrão (fallback), mas se você criar essas variáveis no Easypanel elas vão substituir
URL_EVOLUTION = os.environ.get("URL_EVOLUTION", "https://evolution.zapmais.net")
API_KEY = os.environ.get("API_KEY", "Movel3164973131@@")
NUMERO_AVISO = os.environ.get("NUMERO_AVISO", "5588981843138")
NOME_INSTANCIA = os.environ.get("NOME_INSTANCIA", "NOME_DA_SUA_INSTANCIA_AQUI")

def enviar_mensagem_whatsapp():
    url = f"{URL_EVOLUTION}/message/sendText/{NOME_INSTANCIA}"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Corpo da mensagem
    payload = {
        "number": NUMERO_AVISO,
        "text": "✅ *Aviso de Sistema*\n\nO serviço da Evolution API foi reiniciado automaticamente e já estabilizou!"
    }
    
    try:
        print(f"Tentando enviar mensagem de aviso para {NUMERO_AVISO} usando a instância {NOME_INSTANCIA}...")
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            print("Mensagem enviada com sucesso pelo WhatsApp!")
    except urllib.error.HTTPError as e:
        print(f"Erro na API ao enviar mensagem (Código {e.code}). Verifique se o nome da instância está correto. Detalhes: {e.read().decode()}")
    except Exception as e:
        print(f"Erro ao tentar se conectar com a API: {e}")

def reiniciar_servico():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Buscando o container para o serviço: {NOME_SERVICO}")
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, check=True)
        containers = result.stdout.strip().split('\n')
        
        container_alvo = None
        for c in containers:
            if c == NOME_SERVICO or c.endswith(f"_{NOME_SERVICO}"):
                container_alvo = c
                break
                
        if not container_alvo:
            print(f"Erro: Nenhum container encontrado para o serviço '{NOME_SERVICO}'.")
            return
            
        print(f"Container encontrado: {container_alvo}. Reiniciando...")
        subprocess.run(["docker", "restart", container_alvo], check=True)
        print("Serviço reiniciado com sucesso.")
        
        # Espera 30 segundos para dar tempo do serviço da Evolution ligar completamente e o WhatsApp conectar
        print("Aguardando 30 segundos para o serviço estabilizar antes de enviar a mensagem...")
        time.sleep(30)
        
        # Envia a mensagem
        enviar_mensagem_whatsapp()
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando do docker. Detalhes: {e}")
    except FileNotFoundError:
        print("Erro: O comando 'docker' não foi encontrado.")

def main():
    print("Script de agendamento (Easypanel/Docker) iniciado.")
    print(f"O serviço '{NOME_SERVICO}' será reiniciado todos os dias nos seguintes horários: {', '.join(HORARIOS_REINICIO)}")
    
    while True:
        agora = datetime.datetime.now().strftime("%H:%M")
        
        if agora in HORARIOS_REINICIO:
            reiniciar_servico()
            time.sleep(61)
        else:
            time.sleep(30)

if __name__ == "__main__":
    main()
