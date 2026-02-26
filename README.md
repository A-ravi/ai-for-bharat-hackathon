# Jal Sathi (जल साथी) - Water Companion

AI-powered irrigation advisor platform for Indian farmers to optimize water usage and reduce irrigation costs.

## Features

- 🌾 Personalized irrigation recommendations in 8 Indian languages
- 📱 Responsive web application optimized for rural connectivity
- 💧 30-40% water savings through AI-powered advice
- 📊 Real-time savings tracking and milestone celebrations
- 📅 7-day irrigation schedule with weather integration
- 📲 SMS alerts for critical irrigation updates
- 🌤️ Multi-source weather data integration with fallback mechanisms

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Reliable data persistence with connection pooling
- **Redis** - Caching for weather data and recommendations
- **SQLAlchemy** - ORM with Alembic migrations
- **Claude AI** - Enhanced recommendation generation

### Frontend
- **React 18** - Modern UI library with TypeScript
- **Vite** - Fast build tool and dev server
- **React Query** - Data fetching and caching
- **PWA** - Progressive Web App with offline capabilities
- **Mobile-first** - Responsive design optimized for all devices

### Infrastructure
- **Docker** - Containerized development environment
- **Docker Compose** - Multi-container orchestration

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd jal-sathi
```

2. Create environment files:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Update the `.env` files with your API keys:
   - Weather API keys (OpenWeatherMap, IMD)
   - SMS Gateway credentials
   - Claude AI API key

4. Start all services:
```bash
docker-compose up -d
```

5. Run database migrations:
```bash
docker-compose exec backend alembic upgrade head
```

6. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
jal-sathi/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── core/             # Core configuration
│   │   │   ├── config.py     # Settings management
│   │   │   ├── database.py   # Database connection
│   │   │   └── cache.py      # Redis cache
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── api/              # API routes
│   │   └── main.py           # FastAPI application
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API clients
│   │   ├── hooks/            # Custom React hooks
│   │   ├── store/            # State management
│   │   ├── i18n/             # Translations
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## Supported Languages

- Hindi (हिंदी)
- English
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Punjabi (ਪੰਜਾਬੀ)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

## Database Migrations

Create a new migration:
```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
docker-compose exec backend alembic upgrade head
```

Rollback migration:
```bash
docker-compose exec backend alembic downgrade -1
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.
