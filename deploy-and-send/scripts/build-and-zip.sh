#!/usr/bin/env bash
# Build the devops-claw project and zip the dist output
set -euo pipefail

PROJECT_DIR="${1:-.}"
ZIP_NAME="${2:-dist.zip}"

cd "$PROJECT_DIR"

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building project..."
npm run build

echo "🗜️  Zipping dist/ to ${ZIP_NAME}..."
rm -f "$ZIP_NAME"
zip -r "$ZIP_NAME" dist/ -x "dist/.DS_Store" -x "dist/__MACOSX/*"

SIZE=$(du -h "$ZIP_NAME" | cut -f1)
echo "✅ Done: ${ZIP_NAME} (${SIZE})"
