#!/bin/bash

# ============================================================
# GNews API - Project Setup Script
# ============================================================

set -e  # Exit on any error

echo "==> Setting up GNews API project..."

# ------------------------------------------------------------
# 1. Create virtual environment
# ------------------------------------------------------------
if [ ! -d "venv" ]; then
    echo "==> Creating virtual environment..."
    python -m venv venv
else
    echo "==> Virtual environment already exists, skipping..."
fi

# ------------------------------------------------------------
# 2. Activate virtual environment
# ------------------------------------------------------------
echo "==> Activating virtual environment..."
source venv/Scripts/activate  # Windows (Git Bash / WSL)
# For Linux/macOS use: source venv/bin/activate

# ------------------------------------------------------------
# 3. Upgrade pip
# ------------------------------------------------------------
echo "==> Upgrading pip..."
pip install --upgrade pip

# ------------------------------------------------------------
# 4. Install Django
# ------------------------------------------------------------
echo "==> Installing Django..."
pip install django

# ------------------------------------------------------------
# 5. Install all dependencies
# ------------------------------------------------------------
echo "==> Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# ------------------------------------------------------------
# 6. Environment variables check
# ------------------------------------------------------------
if [ ! -f ".env" ]; then
    echo ""
    echo "  [WARNING] No .env file found."
    echo "  Copy .env.example to .env and fill in your values:"
    echo "    cp .env.example .env"
    echo ""
fi

# ------------------------------------------------------------
# 7. Run database migrations
# ------------------------------------------------------------
echo "==> Running database migrations..."
python manage.py migrate

# ------------------------------------------------------------
# 8. Create superuser (optional)
# ------------------------------------------------------------
echo ""
read -p "==> Do you want to create a superuser? (y/n): " create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

# ------------------------------------------------------------
# 9. Load sample data (optional)
# ------------------------------------------------------------
if [ -f "fake_data.sql" ]; then
    echo ""
    read -p "==> Do you want to load sample data from fake_data.sql? (y/n): " load_data
    if [ "$load_data" = "y" ] || [ "$load_data" = "Y" ]; then
        echo "==> Loading sample data..."
        echo "  Run manually: mysql -u <user> -p gnews_api < fake_data.sql"
    fi
fi

# ------------------------------------------------------------
# Done
# ------------------------------------------------------------
echo ""
echo "==> Setup complete!"
echo ""
echo "  To start the development server:"
echo "    source venv/Scripts/activate"
echo "    python manage.py runserver"
echo ""
