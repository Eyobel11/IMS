#!/bin/bash
#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Debugging: Check Python and pip versions



python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip list --format=freeze


echo "Python version:"
python3 --version
echo "Pip version:"
python3 -m pip --version

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
python3 -m pip install -r requirements.txt

# Create static files
python3 manage.py collectstatic --noinput

mkdir static
