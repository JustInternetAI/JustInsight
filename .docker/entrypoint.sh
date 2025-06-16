#!/usr/bin/env bash
set -euo pipefail

# Change these defaults if you rename the repo or directory
REPO_URL="${REPO_URL:-https://github.com/JustInternetAI/JustInsight.git}"
REPO_DIR="${REPO_DIR:-justinsight}"

# Which branch to check out (default to main)
BRANCH="${BRANCH:-master}"

# Clone if first run
if [ ! -d "$REPO_DIR" ]; then
  echo "Cloning $REPO_URL into $REPO_DIR..."
  git clone "$REPO_URL" "$REPO_DIR"
fi

cd "$REPO_DIR"

echo "Fetching updates..."
git fetch origin

# Checkout and pull the requested branch
echo "Checking out branch '$BRANCH'..."
git checkout "$BRANCH"
git pull origin "$BRANCH"

# Finally, hand off to whatever was passed in (e.g. bash or jupyter)
exec "$@"

