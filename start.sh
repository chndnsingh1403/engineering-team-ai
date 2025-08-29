#!/bin/bash

# Engineering Team AI - Startup Script

echo "🚀 Starting Engineering Team AI..."

# Check if we're in the correct directory
if [ ! -f "backend/main.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to start backend
start_backend() {
    echo "🐍 Starting Backend (FastAPI)..."
    cd backend
    if [ ! -d "venv" ]; then
        echo "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    source venv/bin/activate
    
    # Install dependencies if needed
    pip install -r requirements.txt > /dev/null 2>&1
    
    echo "Backend starting on http://localhost:8000"
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
}

# Function to start frontend
start_frontend() {
    echo "⚛️  Starting Frontend (React + Vite)..."
    cd frontend
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing Node.js dependencies..."
        npm install
    fi
    
    echo "Frontend starting on http://localhost:3000 (or next available port)"
    npm run dev &
    FRONTEND_PID=$!
    cd ..
}

# Start both services
start_backend
sleep 2
start_frontend

echo ""
echo "✅ Both services are starting up..."
echo ""
echo "🌐 Frontend: http://localhost:3000 (or check terminal for actual port)"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for Ctrl+C
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
