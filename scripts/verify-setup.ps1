# Jal Sathi Setup Verification Script for Windows

Write-Host "Verifying Jal Sathi Project Setup..." -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# Check Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✓ Docker is installed" -ForegroundColor Green
} else {
    Write-Host "✗ Docker is not installed" -ForegroundColor Red
    exit 1
}

# Check Docker Compose
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    Write-Host "✓ Docker Compose is installed" -ForegroundColor Green
} else {
    Write-Host "✗ Docker Compose is not installed" -ForegroundColor Red
    exit 1
}

# Check project structure
Write-Host ""
Write-Host "Checking project structure..."

$directories = @(
    "backend\app\core",
    "backend\app\models",
    "backend\app\schemas",
    "backend\app\services",
    "backend\app\api",
    "backend\alembic",
    "backend\tests",
    "frontend\src\components",
    "frontend\src\pages",
    "frontend\src\services",
    "frontend\src\hooks",
    "frontend\src\store",
    "frontend\src\i18n"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "✓ $dir exists" -ForegroundColor Green
    } else {
        Write-Host "✗ $dir is missing" -ForegroundColor Red
        exit 1
    }
}

# Check key files
Write-Host ""
Write-Host "Checking key configuration files..."

$files = @(
    "docker-compose.yml",
    "backend\Dockerfile",
    "backend\requirements.txt",
    "backend\.env.example",
    "backend\alembic.ini",
    "frontend\Dockerfile",
    "frontend\package.json",
    "frontend\.env.example",
    "frontend\vite.config.ts",
    "README.md",
    "Makefile"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "✗ $file is missing" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "✓ Project setup verification complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Copy .env.example files and configure API keys"
Write-Host "2. Run 'docker-compose up -d' to start services"
Write-Host "3. Run 'docker-compose exec backend alembic upgrade head' for migrations"
Write-Host "4. Access frontend at http://localhost:3000"
Write-Host "5. Access backend at http://localhost:8000"
