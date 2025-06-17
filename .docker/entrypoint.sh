#!/usr/bin/env bash
set -euo pipefail

# Default branch (override via env if you want)
BRANCH="${BRANCH:-master}"

# Tell Git that /workspace is safe to operate on
git config --global --add safe.directory /workspace

# Bail early if we don’t see a .git folder
if [ ! -d .git ]; then
  echo "❌  Error: /workspace is not a git repo. Please 'git clone' on the host first."
  exit 1
fi

# Update & switch branches
echo "⏳  Fetching updates..."
git fetch origin --prune

echo "⏳  Checking out branch '$BRANCH'..."
# if branch already exists locally, switch; otherwise track remote
if git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
  git checkout "$BRANCH"
else
  git checkout --track "origin/$BRANCH"
fi

echo "⏳  Pulling latest changes..."
git pull --ff-only origin "$BRANCH"

# Hand off to whatever was passed in (e.g. bash)
exec "${@:-bash}"

