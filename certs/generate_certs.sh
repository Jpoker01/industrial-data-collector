#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

openssl req -new -x509 -days 3650 -nodes -keyout ca.key -out ca.crt -subj "/CN=idc-ca"
openssl req -new -nodes -keyout server.key -out server.csr -subj "/CN=mosquitto"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 3650 \
  -out server.crt -extfile <(printf "subjectAltName=DNS:mosquitto,DNS:localhost,IP:127.0.0.1")
  
rm -f server.csr ca.srl
echo "Certificates generated in $(pwd)"