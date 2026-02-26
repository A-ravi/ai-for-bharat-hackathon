#!/bin/bash

echo "Verifying Jal Sathi Project Setup..."
echo "===================================="
echo ""

# Check Docker
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed"
else
    echo "✗ Docker is not installed"
    exit 1
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "✓ Docker Compose is installed"
else
    echo "✗ Docker Compose is not installed"
    exit 1
fi

# Check project structure
echo ""
echo "Checking project structure..."

directories=(
    "backend/app/core"
    "backend/app/models"
    "backend/app/schemas"
    "backend/app/services"
    "backend/app/api"
    "backend/alembic"
    "backend/tests"
    "frontend/src/components"
    "frontend/src/pages"
    "frontend/src/services"
    "frontend/src/hooks"
    "frontend/src/store"
    "frontend/src/i18n"
)

for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "✓ $dir exists"
    else
        echo "✗ $dir is missing"
        exit 1
    fi
done

# Check key files
echo ""
echo "Checking key configuration files..."

files=(
    "docker-compose.yml"
    "backend/Dockerfile"
    "backend/requirements.txt"
    "backend/.env.example"
    "backend/alembic.ini"
    "frontend/Dockerfile"
    "frontend/package.json"
    "frontend/.env.example"
    "frontend/vite.config.ts"
    "README.md"
    "Makefile"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file is missing"
        exit 1
    fi
done

echo ""
echo "===================================="
echo "✓ Project setup verification complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example files and configure API keys"
echo "2. Run 'docker-compose up -d' to start services"
echo "3. Run 'docker-compose exec backend alembic upgrade head' for migrations"
echo "4. Access frontend at http://localhost:3000"
echo "5. Access backend at http://localhost:8000"
