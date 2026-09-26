#!/usr/bin/env bash
set -Eeuo pipefail

ARTIFACT="${1:?Uso: ./scripts/deploy-test.sh target/automatizacion-pruebas-1.0.0-SNAPSHOT.jar}"
ROOT="${DEPLOY_ROOT:-deployments/test}"
ACTIVE_FILE="$ROOT/active"
mkdir -p "$ROOT/blue" "$ROOT/green"

if [[ ! -f "$ARTIFACT" ]]; then
  echo "DEPLOYMENT_FAILED artifact_not_found=$ARTIFACT"
  exit 1
fi

current_slot=""
if [[ -s "$ACTIVE_FILE" ]]; then
  current_slot="$(cat "$ACTIVE_FILE")"
fi
if [[ "$current_slot" == "blue" ]]; then
  target_slot="green"
else
  target_slot="blue"
fi

version="$(basename "$ARTIFACT" .jar)"
rm -rf "$ROOT/$target_slot"/*
cp "$ARTIFACT" "$ROOT/$target_slot/$version.jar"
printf '%s\n' "$version" > "$ROOT/$target_slot/version"

# Health check determinista: el artefacto y su metadata deben existir antes del switch.
[[ -s "$ROOT/$target_slot/$version.jar" ]]
[[ "$(cat "$ROOT/$target_slot/version")" == "$version" ]]

printf '%s\n' "$target_slot" > "$ACTIVE_FILE"
printf '%s\n' "$version" > "$ROOT/last-successful"
printf 'DEPLOYMENT_OK strategy=blue-green active_slot=%s version=%s environment=test\n' "$target_slot" "$version"
