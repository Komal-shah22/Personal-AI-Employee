#!/bin/bash
# Initialize vault as Git repository

VAULT_PATH="${VAULT_PATH:-$HOME/AI_Employee_Vault}"

cd "$VAULT_PATH" || exit 1

echo "Initializing Git repository in vault..."

# Initialize git
git init

# Copy .gitignore
cp ../sync/.gitignore .gitignore

# Initial commit
git add .
git commit -m "Initial vault setup - $(date)"

echo "✓ Git initialized in vault"
echo "Next: Add remote with: git remote add origin <URL>"
