#!/usr/bin/env bash
# Generates the Mosquitto password file from the credentials in .env.
set -e

CONFIG_DIR="mosquitto/config"

if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi

PUB_PW="${MQTT_PUBLISHER_PASSWORD:-password}"
ING_PW="${MQTT_INGEST_PASSWORD:-password}"
DJ_PW="${MQTT_DJANGO_PASSWORD:-password}"

echo "Generating Mosquitto password file..."

docker run --rm --user "$(id -u):$(id -g)" \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -c -b /mosquitto/config/passwd publisher "$PUB_PW"

docker run --rm --user "$(id -u):$(id -g)" \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -b /mosquitto/config/passwd ingest "$ING_PW"

docker run --rm --user "$(id -u):$(id -g)" \
    -v "$(pwd)/$CONFIG_DIR:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -b /mosquitto/config/passwd django "$DJ_PW"

chmod 644 "$CONFIG_DIR/passwd" "$CONFIG_DIR/aclfile"
echo "Done. Password file: $CONFIG_DIR/passwd"

echo "Generating TLS certificates..."
bash certs/generate_certs.sh