#!/bin/bash
# 1. Mata processos do backdoor
pkill -f "37.59.174.235:1337"

# 2. Remove arquivos persistentes
declare -a suspect_files=(
    "/lib/systemd/system/ace-service.service"
    "/etc/cron.hourly/backdoor"
    "/tmp/.ace"
)

for file in "${suspect_files[@]}"; do
    if [ -f "$file" ]; then
        echo "[+] Removendo arquivo malicioso: $file"
        sudo rm -f "$file"
    fi
done

# 3. Limpa crontabs
sudo sed -i '/37.59.174.235/d' /etc/crontab
sudo sed -i '/1337/d' /var/spool/cron/*

# 4. Reinicia serviços críticos
sudo systemctl daemon-reload
sudo systemctl restart sshd

echo "[+] Limpeza completa. Verifique com: sudo netstat -tulnp | grep 1337"
