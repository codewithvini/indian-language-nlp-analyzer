#!/bin/bash
# Startup script for Indian Language NLP Analyzer

echo "🇮🇳 Indian Language NLP Analyzer"
echo "================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Start the application
echo ""
echo "🚀 Starting the application..."
echo "✨ Features: Word Frequency, Sentiment Analysis, Entity Recognition"
echo "📊 Supported languages: Hindi, Gujarati, Marathi"
echo ""
echo "🌐 Open your browser and navigate to:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python analyzer.py
