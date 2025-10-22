#!/bin/bash

echo "🚀 Starting SmartDocQ deployment process..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm run install:all

# Build the project
echo "🔨 Building project..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo "🚀 Ready for deployment to Render!"
    echo ""
    echo "Next steps:"
    echo "1. Push your code to GitHub"
    echo "2. Connect your GitHub repo to Render"
    echo "3. Use the render.yaml configuration"
    echo "4. Set up your environment variables in Render dashboard"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi
