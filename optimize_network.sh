#!/bin/bash
# Script para otimizar configurações de rede para baixa latência MQTT
# Use este script em ambientes onde você tem controle sobre o kernel

echo "=== Otimizações de Rede para Baixa Latência MQTT ==="
echo ""
echo "NOTA: Estas otimizações requerem privilégios de administrador."
echo "No Railway, as otimizações de socket já estão configuradas no mosquitto.conf"
echo ""
echo "Para ambientes locais ou VPS, execute com sudo:"
echo ""

cat << 'EOF'
# TCP optimizations
sudo sysctl -w net.ipv4.tcp_nodelay=1
sudo sysctl -w net.ipv4.tcp_low_latency=1
sudo sysctl -w net.ipv4.tcp_sack=1
sudo sysctl -w net.ipv4.tcp_timestamps=0

# Buffer sizes
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.wmem_max=134217728
sudo sysctl -w net.ipv4.tcp_rmem="4096 87380 134217728"
sudo sysctl -w net.ipv4.tcp_wmem="4096 65536 134217728"

# Connection handling
sudo sysctl -w net.ipv4.tcp_fin_timeout=10
sudo sysctl -w net.ipv4.tcp_tw_reuse=1
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096
sudo sysctl -w net.core.somaxconn=4096

# Congestion control
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
sudo sysctl -w net.ipv4.tcp_notsent_lowat=16384

# Queue management
sudo sysctl -w net.core.netdev_max_backlog=5000
sudo sysctl -w net.ipv4.tcp_max_orphans=60000

# Make persistent
sudo sysctl -p
EOF

echo ""
echo "Para tornar permanente, adicione as linhas acima em /etc/sysctl.conf"