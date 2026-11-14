#!/usr/bin/env bash
set -e

echo "Starting Backend..."
cd "$(dirname "$0")/backend"
export PYTHONPATH="$(pwd)"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

echo "Starting Frontend..."
cd "../frontend"
npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait

