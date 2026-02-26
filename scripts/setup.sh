#!/bin/bash

echo "Setting up Jal Sathi Development Environment..."
echo "================================================"
echo ""

# Create .env files if they don't exist
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env from example..."
    cp backend/.env.example backend/.env
    echo "✓ Created backend/.env"
else
    echo "✓ backend/.env already exists"
fi

if [ ! -f frontend/.env ]; then
    echo "Creating frontend/.env from example..."
    cp frontend/.env.example frontend/.env
    echo "✓ Created frontend/.env"
else
    echo "✓ frontend/.env already exists"
fi

echo ""
echo "Building Docker containers..."
docker-compose build

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for database to be ready..."
sleep 5

echo ""
echo "Running database migrations..."
docker-compose exec -T backend alembic upgrade head

echo ""
echo "================================================"
echo "✓ Setup complete!"
echo ""
echo "Services are running:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo ""
echo "Don't forget to add your API keys to backend/.env:"
echo "  - WEATHER_API_KEY"
echo "  - IMD_API_KEY"
echo "  - SMS_GATEWAY_API_KEY"
echo "  - CLAUDE_API_KEY"
