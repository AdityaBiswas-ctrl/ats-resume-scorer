#!/bin/bash

# Start FastAPI backend in the background
echo "Starting FastAPI backend..."
uvicorn app.main:app --host 127.0.0.1 --port 8000 &

# Wait for the backend to be ready
sleep 3

# Start Streamlit frontend on the port provided by Render
echo "Starting Streamlit frontend..."
export API_URL="http://127.0.0.1:8000"
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
