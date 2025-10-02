#!/bin/sh

# Shutdown on error
set -e

echo "=== Iniciando Mosquitto MQTT Broker ==="
echo "Timestamp: $(date)"

# Check if MOSQUITTO_USERNAME and MOSQUITTO_PASSWORD environment variables are defined
if [ -z "$MOSQUITTO_USERNAME" ] || [ -z "$MOSQUITTO_PASSWORD" ]; then
  echo "ERRO: As variáveis de ambiente MOSQUITTO_USERNAME e MOSQUITTO_PASSWORD precisam ser definidas."
  exit 1
fi

echo "Usuário configurado: $MOSQUITTO_USERNAME"

# Create password file as root
echo "Criando arquivo de senha..."
mosquitto_passwd -b -c /mosquitto/config/password_file "$MOSQUITTO_USERNAME" "$MOSQUITTO_PASSWORD"

# Verify file was created
if [ -f /mosquitto/config/password_file ]; then
    echo "Arquivo de senha criado com sucesso"
    ls -la /mosquitto/config/password_file
else
    echo "ERRO: Falha ao criar arquivo de senha"
    exit 1
fi

# Set proper ownership and permissions for Mosquitto 2.0.22
echo "Ajustando permissões..."
chown mosquitto:mosquitto /mosquitto/config/password_file
chmod 600 /mosquitto/config/password_file

# Show final permissions
echo "Permissões finais:"
ls -la /mosquitto/config/password_file

# Show configuration file
echo "Verificando arquivo de configuração:"
ls -la /mosquitto/config/mosquitto.conf

# Now switch to mosquitto user and execute mosquitto
echo "Iniciando Mosquitto como usuário 'mosquitto'..."
echo "Comando: $@"

# Use su-exec if available (alpine), otherwise use su
if command -v su-exec > /dev/null 2>&1; then
    echo "Usando su-exec..."
    exec su-exec mosquitto "$@"
else
    echo "Usando su..."
    exec su mosquitto -s /bin/sh -c "$*"
fi