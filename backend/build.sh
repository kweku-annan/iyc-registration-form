#!/usr/bin/env bash
# Render.com build script for IYC Conference Registration Backend

set -o errexit

echo "🔨 Building IYC Conference Registration Backend..."
echo "==================================================="

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build complete!"
