# Jal Sathi - Quick Start Guide

## Prerequisites

Before you begin, ensure you have the following installed:
- **Docker Desktop** (includes Docker and Docker Compose)
- **Git** (for version control)

## Setup Instructions

### 1. Environment Configuration

The project includes `.env` files with default values for development. To customize:

**Backend Configuration** (`backend/.env`):
```bash
# Add your API keys here
WEATHER_API_KEY=your_openweathermap_api_key
IMD_API_KEY=your_imd_api_key
SMS_GATEWAY_API_KEY=your_sms_gateway_key
CLAUDE_API_KEY=your_claude_api_key
```

**Frontend Configuration** (`frontend/.env`):
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Jal Sathi
```

### 2. Start the Application

#### Option A: Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Wait for services to be ready (about 30 seconds)
# Then run database migrations
docker-compose exec backend alembic upgrade head

# View logs
docker-compose logs -f
```

#### Option B: Using Makefile (Linux/Mac)

```bash
# Build containers
make build

# Start services
make up

# Run migrations
make migrate

# View logs
make logs
```

### 3. Access the Application

Once all services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **PostgreSQL**: localhost:5432 (user: jalsathi, password: jalsathi, db: jalsathi)
- **Redis**: localhost:6379

### 4. Verify Installation

Check that all services are running:

```bash
docker-compose ps
```

You should see:
- `jalsathi-frontend` (running on port 3000)
- `jalsathi-backend` (running on port 8000)
- `jalsathi-db` (PostgreSQL on port 5432)
- `jalsathi-redis` (Redis on port 6379)

### 5. Test the API

Visit http://localhost:8000/docs to explore the API endpoints using Swagger UI.

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

## Development Workflow

### Backend Development

The backend uses hot-reload, so changes to Python files will automatically restart the server.

```bash
# View backend logs
docker-compose logs -f backend

# Run backend tests
docker-compose exec backend pytest

# Create a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head
```

### Frontend Development

The frontend also uses hot-reload via Vite.

```bash
# View frontend logs
docker-compose logs -f frontend

# Install new packages
docker-compose exec frontend npm install <package-name>

# Run frontend tests
docker-compose exec frontend npm test
```

### Database Management

```bash
# Access PostgreSQL shell
docker-compose exec db psql -U jalsathi -d jalsathi

# Backup database
docker-compose exec db pg_dump -U jalsathi jalsathi > backup.sql

# Restore database
docker-compose exec -T db psql -U jalsathi jalsathi < backup.sql
```

### Redis Management

```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# View all keys
docker-compose exec redis redis-cli KEYS '*'

# Clear cache
docker-compose exec redis redis-cli FLUSHALL
```

## Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This deletes all data)
docker-compose down -v
```

## Troubleshooting

### Port Already in Use

If you get port conflict errors:

```bash
# Check what's using the port
netstat -ano | findstr :3000  # Windows
lsof -i :3000                 # Linux/Mac

# Change ports in docker-compose.yml if needed
```

### Database Connection Issues

```bash
# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db

# Verify database is healthy
docker-compose exec db pg_isready -U jalsathi
```

### Frontend Not Loading

```bash
# Rebuild frontend container
docker-compose build frontend
docker-compose up -d frontend

# Check frontend logs
docker-compose logs frontend
```

### Backend API Errors

```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Verify environment variables
docker-compose exec backend env | grep DATABASE_URL
```

## Next Steps

1. **Configure API Keys**: Add your actual API keys to `backend/.env`
2. **Explore the API**: Visit http://localhost:8000/docs
3. **Start Development**: Begin implementing features from the task list
4. **Run Tests**: Ensure all tests pass before committing changes

## Useful Commands Reference

```bash
# Docker Compose
docker-compose up -d              # Start services in background
docker-compose down               # Stop services
docker-compose restart            # Restart all services
docker-compose logs -f            # Follow logs
docker-compose ps                 # List running services
docker-compose exec <service> sh  # Access service shell

# Database Migrations
docker-compose exec backend alembic upgrade head      # Apply migrations
docker-compose exec backend alembic downgrade -1     # Rollback one migration
docker-compose exec backend alembic current          # Show current migration
docker-compose exec backend alembic history          # Show migration history

# Testing
docker-compose exec backend pytest                   # Run backend tests
docker-compose exec backend pytest -v                # Verbose output
docker-compose exec backend pytest tests/test_file.py # Run specific test
docker-compose exec frontend npm test                # Run frontend tests
```

## Support

For issues or questions:
1. Check the main [README.md](README.md) for detailed documentation
2. Review the [design document](.kiro/specs/jal-sathi/design.md)
3. Open an issue on GitHub

Happy coding! 🌾💧
