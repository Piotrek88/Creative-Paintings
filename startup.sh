#!/bin/bash

# Navigate to the application directory
cd /workspace

# Run the generate_secrets.py script
python generate_secrets.py

# Start your main application with the correct host and port
streamlit run app.py
