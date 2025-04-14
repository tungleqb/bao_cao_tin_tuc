#!/bin/bash
echo "Running FastAPI server at http://127.0.0.1:8000"
uvicorn backend.app.main:app --reload
