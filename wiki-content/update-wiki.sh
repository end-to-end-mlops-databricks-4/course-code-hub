#!/bin/bash

# Update Wiki Content Pipeline
# This script regenerates wiki content from lectures and syncs to GitHub Wiki

set -e

echo "🔄 Updating wiki content pipeline..."

# Step 1: Generate wiki content from lectures
echo "📚 Step 1: Generating wiki content from lectures..."
python wiki-content/generate-wiki-content.py

# Step 2: Sync to GitHub Wiki
echo "🔄 Step 2: Syncing to GitHub Wiki..."
./wiki-content/sync-wiki.sh

echo "✅ Wiki update complete!"
