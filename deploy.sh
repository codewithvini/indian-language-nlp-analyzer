#!/bin/bash

echo "🚀 Indian Language NLP Analyzer - Deployment Helper"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Check if remote exists
if ! git remote | grep -q 'origin'; then
    echo ""
    echo "⚠️  No GitHub remote found!"
    echo ""
    echo "Please create a new repository on GitHub, then run:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/indian-language-nlp-analyzer.git"
    echo ""
else
    echo "✅ GitHub remote configured"
fi

# Stage all files
echo ""
echo "📝 Staging files..."
git add .

# Show status
echo ""
echo "📊 Git Status:"
git status --short

echo ""
echo "📋 Next Steps:"
echo "1. Review the changes above"
echo "2. Run: git commit -m 'Ready for deployment'"
echo "3. Run: git push origin main"
echo "4. Go to Render.com and connect your GitHub repo"
echo "5. Follow steps in DEPLOYMENT_GUIDE.md"
echo ""
echo "📖 Full guide: cat DEPLOYMENT_GUIDE.md"
