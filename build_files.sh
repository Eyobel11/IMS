#!/bin/bash
python3 -m pip install --upgrade pip  # Use the default Python runtime to upgrade pip
python3 -m pip install -r requirements.txt  # Install dependencies
python3 manage.py collectstatic --noinput  # Collect static files

# Debugging: Check Python version and pip availability
python3 --version
python3 -m pip --version
