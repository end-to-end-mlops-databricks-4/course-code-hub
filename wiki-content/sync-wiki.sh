#!/bin/bash

# Sync local wiki markdown files to GitHub Wiki
# Usage: ./wiki-content/sync-wiki.sh

set -e

# Set these variables
REPO_URL="https://github.com/end-to-end-mlops-databricks-4/course-code-hub.wiki.git"
WIKI_TMP_DIR="/tmp/course-code-hub-wiki-tmp"
WIKI_SRC_DIR="$(dirname "$0")"  # wiki-content

# 1. Clone the wiki repo (fresh each time for safety)
echo "Cloning Wiki repo..."
rm -rf "$WIKI_TMP_DIR"
git clone "$REPO_URL" "$WIKI_TMP_DIR"

# 2. Copy all markdown files from wiki-content/ to wiki repo
echo "Copying markdown files..."
cp "$WIKI_SRC_DIR"/*.md "$WIKI_TMP_DIR"/

# 3. Commit and push
echo "Committing and pushing to Wiki repo..."
cd "$WIKI_TMP_DIR"
git add .
git commit -m "Update wiki docs from main repo" || echo "No changes to commit."
git push

echo "✅ Wiki sync complete!"
