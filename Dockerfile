# Imagem oficial do Eclipse Mosquitto
FROM eclipse-mosquitto:latest

# Copia o arquivo de configuração personalizado
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

RUN mkdir -p /mosquitto/data /mosquitto/log && chown -R mosquitto:mosquitto /mosquitto/data /mosquitto/log

# Copia o nosso script de inicialização para dentro do contêiner
COPY entrypoint.sh /usr/bin/entrypoint.sh

# Garante que o script seja executável
RUN chmod +x /usr/bin/entrypoint.sh

# Define o nosso script como o ponto de entrada do contêiner
ENTRYPOINT ["entrypoint.sh"]

# Define o comando padrão que o entrypoint irá executar depois de criar o arquivo de senha.
# Este é o comando padrão da imagem original para iniciar o mosquitto.
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]