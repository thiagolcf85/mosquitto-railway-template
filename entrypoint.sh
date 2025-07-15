#!/bin/sh

# Encerra o script se qualquer comando falhar
set -e

# Verifica se as variáveis de ambiente foram definidas
if [ -z "$MOSQUITTO_USERNAME" ] || [ -z "$MOSQUITTO_PASSWORD" ]; then
  echo "ERRO: As variáveis de ambiente MOSQUITTO_USERNAME e MOSQUITTO_PASSWORD precisam ser definidas."
  exit 1
fi

# Cria o arquivo de senha a partir das variáveis de ambiente
mosquitto_passwd -b -c /mosquitto/config/password_file "$MOSQUITTO_USERNAME" "$MOSQUITTO_PASSWORD"

# Passa a execução para o comando original do contêiner (inicia o mosquitto)
# "$@" representa todos os argumentos passados para o script, que no nosso caso
# será o comando para iniciar o broker definido no Dockerfile.
exec "$@"