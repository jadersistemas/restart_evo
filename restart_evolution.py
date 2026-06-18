import time
import datetime
import subprocess
import os

# Pega os horários via variável de ambiente ou usa o padrão
horarios_env = os.environ.get("HORARIOS_REINICIO", "07:00,13:00")
HORARIOS_REINICIO = [h.strip() for h in horarios_env.split(",")]

# Nome do container da Evolution no Easypanel
# Importante: No Easypanel o nome do container geralmente é "nome-do-projeto_nome-do-serviço" (ex: myproject_evolution)
NOME_CONTAINER = os.environ.get("NOME_CONTAINER", "nome-do-projeto_evolution")

def reiniciar_servico():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Tentando reiniciar o container: {NOME_CONTAINER}")
    try:
        # Comando para reiniciar o container Docker
        subprocess.run(["docker", "restart", NOME_CONTAINER], check=True)
        print("Container reiniciado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao reiniciar o container. Verifique o nome do container e se o docker.sock está mapeado. Detalhes: {e}")
    except FileNotFoundError:
        print("Erro: O comando 'docker' não foi encontrado dentro deste container.")

def main():
    print("Script de agendamento (Easypanel/Docker) iniciado.")
    print(f"O container '{NOME_CONTAINER}' será reiniciado todos os dias nos seguintes horários: {', '.join(HORARIOS_REINICIO)}")
    
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
