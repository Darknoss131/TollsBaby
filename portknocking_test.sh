#!/bin/bash

# IP de destino
TARGET="37.59.174.235"

# Sequência de portas de knocking
PORT_SEQUENCE=(13 37 30000 3000)

# Tempo entre os knocks (em segundos)
DELAY=1

echo "Iniciando sequência de Port Knocking para $TARGET..."
for PORT in "${PORT_SEQUENCE[@]}"; do
    echo "Enviando pacote SYN para a porta $PORT..."
    hping3 -S -p $PORT -c 1 $TARGET > /dev/null 2>&1
    sleep $DELAY
done

echo "Sequência finalizada."
echo "Tente agora verificar se a porta 1972 está aberta com:"
echo "    nc -zv $TARGET 1972"
