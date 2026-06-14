#!/bin/bash

# Simple build script for Angular app
echo "Building Angular application..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

# Build the application
echo "Building..."
npx ng build --configuration production

echo "Build complete! Output in dist/document-rag-app"
