# Dockerfile otimizado para baixa latência no Railway
FROM eclipse-mosquitto:2.0.22

# Switch to root to set up permissions
USER root

# Copy custom configuration file
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Create necessary directories and set permissions
RUN mkdir -p /mosquitto/data /mosquitto/log /mosquitto/config && \
    chown -R mosquitto:mosquitto /mosquitto

# Copy entrypoint as root
COPY --chmod=755 entrypoint.sh /usr/bin/entrypoint.sh

# The entrypoint will run as root to create password file
ENTRYPOINT ["/usr/bin/entrypoint.sh"]

# Define the command that the entrypoint will execute after creating the password file.
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]