#!/bin/bash

# LinkedIn Sourcing Agent Startup Script
echo "🚀 Starting LinkedIn Sourcing Agent..."

# Check if virtual environment exists
if [ ! -d "senv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv senv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source senv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "GOOGLE_API_KEY=your_google_api_key"
    echo "GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id"
    echo "GROQ_API_KEY=your_groq_api_key"
    echo ""
fi

# Start the enhanced backend
echo "🌐 Starting enhanced backend server..."
cd backend
python enhanced_main.py 