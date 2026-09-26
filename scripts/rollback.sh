#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${DEPLOY_ROOT:-deployments/test}"
ACTIVE_FILE="$ROOT/active"

if [[ ! -s "$ACTIVE_FILE" ]]; then
  echo "ROLLBACK_SKIPPED no existe un despliegue activo en $ROOT"
  exit 0
fi

active_slot="$(cat "$ACTIVE_FILE")"
if [[ "$active_slot" == "blue" ]]; then
  previous_slot="green"
else
  previous_slot="blue"
fi

if [[ ! -s "$ROOT/$previous_slot/version" ]]; then
  echo "ROLLBACK_FAILED no hay una versión previa disponible"
  exit 1
fi

printf '%s\n' "$previous_slot" > "$ACTIVE_FILE"
previous_version="$(cat "$ROOT/$previous_slot/version")"
printf '%s\n' "$previous_version" > "$ROOT/last-successful"
printf 'ROLLBACK_OK active_slot=%s version=%s\n' "$previous_slot" "$previous_version"
