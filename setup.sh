#!/usr/bin/env bash
# Generates the Mosquitto password file from the credentials in .env.
set -e

CONFIG_DIR="mosquitto/config"

# Load MQTT passwords from .env
if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi


echo "Generating Mosquitto password file..."

# Drop any existing file first so a stale, unreadable one (e.g. left over
# from an older version of this script) can't block the rewrite below.
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
# Keep these files owned by you (not a container-internal uid) so this repo
# stays writable without sudo; just open read access to "other" so the
# broker's own in-container user can still read them.
chmod 0644 "$CONFIG_DIR/passwd" certs/server.key

echo "Setup complete!"