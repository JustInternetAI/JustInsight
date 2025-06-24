#!/usr/bin/env bash
set -euo pipefail

#use this code for deployment on EC2
#######################################################################################
# # Default branch (override via env if you want)
# BRANCH="${BRANCH:-master}"

# # Tell Git that /workspace is safe to operate on
# git config --global --add safe.directory /workspace

# # Bail early if we don’t see a .git folder
# if [ ! -d .git ]; then
#   echo "❌  Error: /workspace is not a git repo. Please 'git clone' on the host first."
#   exit 1
# fi

# # Update & switch branches
# echo "⏳  Fetching updates..."
# git fetch origin --prune

# echo "⏳  Checking out branch '$BRANCH'..."
# # if branch already exists locally, switch; otherwise track remote
# if git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
#   git checkout "$BRANCH"
# else
#   git checkout --track "origin/$BRANCH"
# fi

# echo "⏳  Pulling latest changes..."
# git pull --ff-only origin "$BRANCH"
#######################################################################################


#use this code for local development
#######################################################################################
# Skip Git checkout for local dev — just use the mounted code as-is
echo "Skipping Git checkout — using mounted code in /workspace"

# Set the Python path and working dir
#cd /workspace/src
#export PYTHONPATH=/workspace/src
#######################################################################################


# Hand off to whatever was passed in (e.g. bash)
exec "${@:-bash}"

