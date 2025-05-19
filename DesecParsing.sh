#!/bin/bash

# Verificação de argumento
if [ -z "$1" ]; then
    echo "Uso: $0 dominio.com"
    exit 1
fi

dominio=$1

echo "##############################################"
echo "<--|         Buscando Hosts...            |-->"
echo "##############################################"

# Busca subdomínios no crt.sh e limpa com grep/sed
curl -s "https://crt.sh/?q=%25.${dominio}&output=json" | \
    jq -r '.[].name_value' 2>/dev/null | \
    sed 's/\*\.//g' | \
    sort -u | \
    tee hosts_temp.txt

echo "##############################################"
echo "<--|         Resolvendo Hosts...          |-->"
echo "##############################################"

# Resolvendo IPs dos subdomínios
while read host; do
    # Ignorar linhas vazias ou mal formadas
    if [[ -n "$host" ]]; then
        ip=$(dig +short "$host" | head -n1)
        if [[ -n "$ip" ]]; then
            echo "$host has address $ip"
        else
            echo "$host -> [NÃO RESOLVEU]"
        fi
    fi
done < hosts_temp.txt

# Limpeza
rm -f hosts_temp.txt

