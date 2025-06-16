#!/usr/bin/env bash
set -euo pipefail


echo "Fetching updates..."
git fetch origin

# Checkout and pull the requested branch
echo "Checking out branch '$BRANCH'..."
git checkout "$BRANCH"
git pull origin "$BRANCH"

# Finally, hand off to whatever was passed in (e.g. bash or jupyter)
exec "$@"

