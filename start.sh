#!/bin/bash

# IYC Conference Registration - Production Server Startup Script
# This script starts the FastAPI backend in production mode
# The backend also serves the frontend static files

cd "$(dirname "$0")"

echo "🚀 Starting IYC Conference Registration (Production Mode)..."
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "backend/.venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create a virtual environment first:"
    echo "  cd backend"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source backend/.venv/bin/activate

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "❌ .env file not found!"
    echo "Please create backend/.env with your configuration"
    echo "You can copy .env.example as a starting point"
    exit 1
fi

# Navigate to backend directory
cd backend

# Start the server in production mode
echo "✅ Starting server in production mode..."
echo ""
echo "📍 Application will be available at:"
echo "   Frontend: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Health:   http://localhost:8000/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="
echo ""

# Use more workers in production for better performance
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
