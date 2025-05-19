#!/bin/bash

TARGET_IP="37.59.174.235"
SOURCE_PORT="1972"
DEST_PORT="1337"

# Sequência de Port Knocking
KNOCK_PORTS="13 37 30000 3000"

echo "Iniciando a sequência de Port Knocking para $TARGET_IP..."

for PORT in $KNOCK_PORTS; do
  echo "Enviando SYN para porta $PORT..."
  sudo hping3 -S -p $PORT -c 1 $TARGET_IP > /dev/null 2>&1
  sleep 0.5
done

echo "Sequência de Port Knocking concluída."

echo "Enviando SYN da porta $SOURCE_PORT para $TARGET_IP:$DEST_PORT..."
sudo hping3 -S -s $SOURCE_PORT -p $DEST_PORT -c 1 $TARGET_IP

echo "Aguardando resposta SYN-ACK por 5 segundos..."
if timeout 5 tcpdump -i eth0 -n -c 1 "tcp and src host $TARGET_IP and src port $DEST_PORT and dst port $SOURCE_PORT and tcp[tcpflags] & (tcp-syn|tcp-ack) != 0" | grep -q "SA"; then
  echo "Recebido SYN-ACK de $TARGET_IP:$DEST_PORT para nossa porta $SOURCE_PORT. Malware possivelmente ativo."
else
  echo "Nenhuma resposta SYN-ACK de $TARGET_IP:$DEST_PORT para nossa porta $SOURCE_PORT recebida dentro do tempo limite."
fi
