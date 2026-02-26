# Jal Sathi Setup Script for Windows

Write-Host "Setting up Jal Sathi Development Environment..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Create .env files if they don't exist
if (-not (Test-Path "backend\.env")) {
    Write-Host "Creating backend\.env from example..."
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✓ Created backend\.env" -ForegroundColor Green
} else {
    Write-Host "✓ backend\.env already exists" -ForegroundColor Green
}

if (-not (Test-Path "frontend\.env")) {
    Write-Host "Creating frontend\.env from example..."
    Copy-Item "frontend\.env.example" "frontend\.env"
    Write-Host "✓ Created frontend\.env" -ForegroundColor Green
} else {
    Write-Host "✓ frontend\.env already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Building Docker containers..."
docker-compose build

Write-Host ""
Write-Host "Starting services..."
docker-compose up -d

Write-Host ""
Write-Host "Waiting for database to be ready..."
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Running database migrations..."
docker-compose exec -T backend alembic upgrade head

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "✓ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Services are running:"
Write-Host "  - Frontend: http://localhost:3000"
Write-Host "  - Backend API: http://localhost:8000"
Write-Host "  - API Docs: http://localhost:8000/docs"
Write-Host "  - PostgreSQL: localhost:5432"
Write-Host "  - Redis: localhost:6379"
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  - View logs: docker-compose logs -f"
Write-Host "  - Stop services: docker-compose down"
Write-Host "  - Restart services: docker-compose restart"
Write-Host ""
Write-Host "Don't forget to add your API keys to backend\.env:" -ForegroundColor Yellow
Write-Host "  - WEATHER_API_KEY"
Write-Host "  - IMD_API_KEY"
Write-Host "  - SMS_GATEWAY_API_KEY"
Write-Host "  - CLAUDE_API_KEY"
