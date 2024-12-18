#!/bin/bash
#!/bin/bash


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

#!/bin/bash
set -e
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
mkdir -p staticfiles_build/static
python3 manage.py collectstatic --noinput

