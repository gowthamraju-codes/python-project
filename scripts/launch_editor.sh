#!/bin/bash

# Launch Monaco Editor with Streamlit
# Get the project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "==================================================="
echo "  Python Script Editor with Monaco"
echo "==================================================="
echo ""
echo "Starting Streamlit application..."
echo ""

source .venv/bin/activate
streamlit run src/monaco-editor.py

echo ""
echo "Application stopped."

