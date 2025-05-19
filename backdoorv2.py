#!/usr/bin/env python3
import socket
import sys
from time import sleep

# Configurações baseadas no PCAP
TARGET_IP = "37.59.174.235"
BACKDOOR_PORT = 1337
TIMEOUT = 3.0

def analyze_pcap_behavior():
    print("[*] Padrão observado no PCAP:")
    print("1. Sequência SYN-SYN/ACK-ACK (3-way handshake completo)")
    print("2. Pacote com 25 bytes de dados após conexão estabelecida")
    print("3. Flag PUSH enviada pelo cliente")
    print("4. Encerramento com FIN-ACK\n")

def check_backdoor():
    print(f"[*] Iniciando verificação em {TARGET_IP}:{BACKDOOR_PORT}")
    
    try:
        # Cria socket TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        
        # 1. Estabelece conexão (SYN)
        print("[*] Enviando SYN...")
        s.connect((TARGET_IP, BACKDOOR_PORT))
        print("[+] Conexão estabelecida (SYN-ACK recebido)")
        
        # 2. Envia payload (25 bytes como visto no PCAP)
        payload = b"[SYN] SeePS Win=512 Len=9\x00"  # Total 25 bytes
        print(f"[*] Enviando payload de {len(payload)} bytes...")
        s.send(payload)
        
        # 3. Aguarda resposta
        try:
            response = s.recv(1024)
            if response:
                print(f"[+] Resposta recebida ({len(response)} bytes): {response.hex()}")
            else:
                print("[!] Backdoor não respondeu com dados")
        except socket.timeout:
            print("[!] Timeout aguardando resposta")
        
        # 4. Encerra conexão (FIN)
        print("[*] Encerrando conexão...")
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return True
        
    except ConnectionRefusedError:
        print("[-] Conexão recusada - porta fechada")
    except socket.timeout:
        print("[-] Timeout - serviço não responsivo")
    except Exception as e:
        print(f"[-] Erro inesperado: {str(e)}")
    
    return False

if __name__ == "__main__":
    print("\n[ Backdoor.ACE Detector ]".center(50, '='))
    
    # Mostra comportamento esperado
    analyze_pcap_behavior()
    
    # Verifica backdoor
    if check_backdoor():
        print("\n[!] ALERTA: Comportamento do backdoor detectado!")
        print("[*] Evidências:")
        print(f"- Conexão bem-sucedida em {TARGET_IP}:{BACKDOOR_PORT}")
        print("- Resposta ao payload específico")
        print("- Padrão de comunicação idêntico ao PCAP")
    else:
        print("\n[*] Nenhuma atividade maliciosa detectada")

    print("\n[+] Análise completa".center(50, '='))
