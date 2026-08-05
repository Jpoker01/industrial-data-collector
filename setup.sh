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

rm -f "$CONFIG_DIR/passwd"

docker run --rm --user "$(id -u):$(id -g)" \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -c -b /mosquitto/config/passwd publisher "$PUB_PW"

docker run --rm --user "$(id -u):$(id -g)" \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -b /mosquitto/config/passwd ingest "$ING_PW"

docker run --rm --user "$(id -u):$(id -g)" \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -b /mosquitto/config/passwd django "$DJ_PW"

echo "Done. Password file: $CONFIG_DIR/passwd"

echo "Generating TLS certificates..."
bash certs/generate_certs.sh

echo "Securing Mosquitto password file and certificate permissions..."
chmod 0644 "$CONFIG_DIR/passwd" certs/server.key
docker run --rm -v "$(pwd)/mosquitto/config:/mosquitto/config" alpine sh -c "chown 1883:1883 /mosquitto/config/passwd && chmod 0700 /mosquitto/config/passwd"

echo "Setup complete!"