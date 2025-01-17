#!/bin/bash

# Navigate to the application directory
cd /workspace

# Utwórz katalog .streamlit, jeśli nie istnieje
mkdir -p .streamli

# Run the generate_secrets.py script
python generate_secrets.py
