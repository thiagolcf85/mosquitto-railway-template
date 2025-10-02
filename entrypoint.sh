#!/bin/sh

# Shutdown on error
set -e

# Check if MOSQUITTO_USERNAME and MOSQUITTO_PASSWORD environment variables are defined
if [ -z "$MOSQUITTO_USERNAME" ] || [ -z "$MOSQUITTO_PASSWORD" ]; then
  echo "ERRO: As variáveis de ambiente MOSQUITTO_USERNAME e MOSQUITTO_PASSWORD precisam ser definidas."
  exit 1
fi

# Create password file as root
mosquitto_passwd -b -c /mosquitto/config/password_file "$MOSQUITTO_USERNAME" "$MOSQUITTO_PASSWORD"

# Set proper ownership and permissions for Mosquitto 2.0.22
chown mosquitto:mosquitto /mosquitto/config/password_file
chmod 600 /mosquitto/config/password_file

# Now switch to mosquitto user and execute mosquitto
# Use su-exec if available (alpine), otherwise use su
if command -v su-exec > /dev/null 2>&1; then
    exec su-exec mosquitto "$@"
else
    exec su mosquitto -s /bin/sh -c "$*"
fi