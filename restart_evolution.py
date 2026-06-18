import time
import datetime
import subprocess
import os

# Pega os horários via variável de ambiente ou usa o padrão
horarios_env = os.environ.get("HORARIOS_REINICIO", "07:00,13:00")
HORARIOS_REINICIO = [h.strip() for h in horarios_env.split(",")]

# Apenas o nome do serviço no Easypanel (ex: evolution)
NOME_SERVICO = os.environ.get("NOME_SERVICO", "evolution")

def reiniciar_servico():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Buscando o container para o serviço: {NOME_SERVICO}")
    try:
        # Lista todos os nomes de containers rodando no Docker
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, check=True)
        containers = result.stdout.strip().split('\n')
        
        container_alvo = None
        for c in containers:
            # Verifica se o container termina com _nomedoservico (padrão Easypanel) ou é exatamente o nome
            if c == NOME_SERVICO or c.endswith(f"_{NOME_SERVICO}"):
                container_alvo = c
                break
                
        if not container_alvo:
            print(f"Erro: Nenhum container encontrado para o serviço '{NOME_SERVICO}'. O serviço está rodando?")
            return
            
        print(f"Container encontrado: {container_alvo}. Reiniciando...")
        
        # Comando para reiniciar o container Docker encontrado
        subprocess.run(["docker", "restart", container_alvo], check=True)
        print("Serviço reiniciado com sucesso.")
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando do docker. Verifique se o docker.sock está mapeado. Detalhes: {e}")
    except FileNotFoundError:
        print("Erro: O comando 'docker' não foi encontrado dentro deste container.")

def main():
    print("Script de agendamento (Easypanel/Docker) iniciado.")
    print(f"O serviço '{NOME_SERVICO}' será reiniciado todos os dias nos seguintes horários: {', '.join(HORARIOS_REINICIO)}")
    
    while True:
        # Pega a hora e minuto atuais
        agora = datetime.datetime.now().strftime("%H:%M")
        
        if agora in HORARIOS_REINICIO:
            reiniciar_servico()
            # Espera 61 segundos para não repetir o comando no mesmo minuto
            time.sleep(61)
        else:
            time.sleep(30)

if __name__ == "__main__":
    main()
