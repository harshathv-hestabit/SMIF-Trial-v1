#!/usr/bin/env bash
set -euo pipefail

CERT_URL="${COSMOS_EMULATOR_CERT_URL:-https://cosmos-emulator.DOMAIN:8081/_explorer/emulator.pem}"
CERT_PATH="/usr/local/share/ca-certificates/cosmos-emulator.crt"

echo "Waiting for Cosmos emulator certificate at ${CERT_URL}..."
for _ in $(seq 1 60); do
  if curl --silent --show-error --fail --insecure "${CERT_URL}" -o "${CERT_PATH}"; then
    echo "Cosmos emulator certificate downloaded."
    update-ca-certificates
    exec /opt/startup/start_nonappservice.sh
  fi
  sleep 2
done

echo "Failed to download Cosmos emulator certificate from ${CERT_URL}" >&2
exit 1
