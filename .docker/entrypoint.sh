#!/usr/bin/env bash
set -euo pipefail

# Hand off to whatever was passed in (e.g. bash)
exec "${@:-bash}"

