#!/usr/bin/env bash
# Generates the Mosquitto password files from the credentials in .env & implement tls for mosquitto
set -e

CONFIG_DIR="mosquitto/config"

if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi

echo "Generating Mosquitto password file..."
# (You might need to prefix this rm with sudo just in case it was created by root previously)
sudo rm -f "$CONFIG_DIR/passwd"

# Run as 1883 so it has permission to write in the mosquitto/config directory
docker run --rm --user 1883:1883 \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -c -b /mosquitto/config/passwd publisher "$MQTT_PUBLISHER_PASSWORD"

docker run --rm --user 1883:1883 \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -b /mosquitto/config/passwd ingest "$MQTT_INGEST_PASSWORD"

docker run --rm --user 1883:1883 \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -b /mosquitto/config/passwd django "$MQTT_DJANGO_PASSWORD"

echo "Done. Password file: $CONFIG_DIR/passwd"

echo "Generating TLS certificates..."
bash certs/generate_certs.sh

echo "Securing Mosquitto password file and certificate permissions..."

docker run --rm \
    -v "$(pwd)/mosquitto/config:/mosquitto/config" \
    -v "$(pwd)/certs:/certs" \
    alpine sh -c "chown -R 1883:1883 /mosquitto/config /certs && \
                  chmod 0700 /mosquitto/config/passwd && \
                  chmod 0700 /mosquitto/config/aclfile && \
                  chmod 0600 /certs/server.key"


echo "Setup complete!"
