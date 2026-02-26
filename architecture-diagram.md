# Jal Sathi - Comprehensive Architecture Diagram

## High-Level System Architecture

```mermaid
graph TB
    subgraph "User Layer"
        F[👨‍🌾 Farmer]
        M[📱 Mobile Browser]
        D[💻 Desktop Browser]
        SMS_P[📞 SMS Phone]
    end
    
    subgraph "Frontend Layer"
        WA[🌐 React Web App<br/>PWA + Offline Support]
        SMS_IF[📨 SMS Interface<br/>Bidirectional]
    end
    
    subgraph "API Gateway & Load Balancer"
        LB[⚖️ Load Balancer<br/>NGINX]
        API_GW[🚪 API Gateway<br/>Rate Limiting & Auth]
    end
    
    subgraph "Backend Services"
        API[🚀 FastAPI Backend<br/>Python 3.11+]
        AUTH[🔐 Auth Service<br/>JWT + Phone OTP]
        LANG[🌍 Language Service<br/>8 Indian Languages]
    end
    
    subgraph "AI & Intelligence Layer"
        AI_ORCH[🧠 AI Orchestrator<br/>Claude Integration]
        REC_ENGINE[⚡ Recommendation Engine<br/>ML + Physics Models]
        CROP_AI[🌾 Crop Intelligence<br/>Growth Stage Detection]
        WEATHER_AI[🌤️ Weather Analysis<br/>Pattern Recognition]
    end
    
    subgraph "Core Business Services"
        SCHED[📅 Scheduler Service<br/>Cron Jobs + Queue]
        TRACK[📊 Savings Tracker<br/>Analytics Engine]
        NOTIFY[🔔 Notification Service<br/>Multi-channel]
        FIELD_MGR[🏞️ Field Manager<br/>Spatial Data]
    end
    
    subgraph "Data Layer"
        DB[(🗄️ PostgreSQL<br/>Primary Database)]
        CACHE[(⚡ Redis Cache<br/>Session + Weather)]
        TS_DB[(📈 TimeSeries DB<br/>InfluxDB - Metrics)]
        FILE_STORE[📁 File Storage<br/>S3 Compatible]
    end
    
    subgraph "External APIs & Services"
        CLAUDE[🤖 Claude AI API<br/>Anthropic]
        IMD[🌡️ IMD Weather API<br/>Indian Met Dept]
        OWM[🌍 OpenWeatherMap<br/>Backup Weather]
        SAT_API[🛰️ Satellite APIs<br/>Soil Moisture]
        SMS_GW[📱 SMS Gateway<br/>Indian Providers]
        MAPS[🗺️ Maps API<br/>Location Services]
    end
    
    subgraph "Infrastructure & Monitoring"
        MONITOR[📊 Monitoring<br/>Prometheus + Grafana]
        LOGS[📝 Logging<br/>ELK Stack]
        BACKUP[💾 Backup Service<br/>Automated]
    end
    
    %% User Interactions
    F --> M
    F --> D
    F --> SMS_P
    
    %% Frontend Connections
    M --> WA
    D --> WA
    SMS_P --> SMS_IF
    
    %% API Layer
    WA --> LB
    SMS_IF --> LB
    LB --> API_GW
    API_GW --> API
    
    %% Backend Services
    API --> AUTH
    API --> LANG
    API --> AI_ORCH
    API --> SCHED
    API --> TRACK
    API --> NOTIFY
    API --> FIELD_MGR
    
    %% AI Layer Connections
    AI_ORCH --> REC_ENGINE
    AI_ORCH --> CROP_AI
    AI_ORCH --> WEATHER_AI
    AI_ORCH --> CLAUDE
    
    REC_ENGINE --> DB
    REC_ENGINE --> CACHE
    REC_ENGINE --> TS_DB
    
    %% Core Services to Data
    SCHED --> DB
    TRACK --> DB
    TRACK --> TS_DB
    NOTIFY --> SMS_GW
    FIELD_MGR --> DB
    FIELD_MGR --> FILE_STORE
    
    %% External API Connections
    WEATHER_AI --> IMD
    WEATHER_AI --> OWM
    CROP_AI --> SAT_API
    FIELD_MGR --> MAPS
    
    %% Caching Strategy
    LANG --> CACHE
    WEATHER_AI --> CACHE
    
    %% Monitoring
    API --> MONITOR
    REC_ENGINE --> MONITOR
    DB --> BACKUP
    
    %% Styling
    classDef userLayer fill:#e1f5fe
    classDef frontendLayer fill:#f3e5f5
    classDef apiLayer fill:#fff3e0
    classDef aiLayer fill:#e8f5e8
    classDef serviceLayer fill:#fce4ec
    classDef dataLayer fill:#f1f8e9
    classDef externalLayer fill:#fff8e1
    classDef infraLayer fill:#f5f5f5
    
    class F,M,D,SMS_P userLayer
    class WA,SMS_IF frontendLayer
    class LB,API_GW apiLayer
    class AI_ORCH,REC_ENGINE,CROP_AI,WEATHER_AI aiLayer
    class API,AUTH,LANG,SCHED,TRACK,NOTIFY,FIELD_MGR serviceLayer
    class DB,CACHE,TS_DB,FILE_STORE dataLayer
    class CLAUDE,IMD,OWM,SAT_API,SMS_GW,MAPS externalLayer
    class MONITOR,LOGS,BACKUP infraLayer
```

## AI-Powered Recommendation Flow

```mermaid
sequenceDiagram
    participant F as 👨‍🌾 Farmer
    participant WA as 🌐 Web App
    participant API as 🚀 FastAPI
    participant AI as 🧠 AI Orchestrator
    participant REC as ⚡ Recommendation Engine
    participant CLAUDE as 🤖 Claude AI
    participant WEATHER as 🌤️ Weather Service
    participant DB as 🗄️ Database
    participant SMS as 📱 SMS Service
    
    Note over F,SMS: Daily Recommendation Generation (6 AM)
    
    API->>WEATHER: Fetch latest weather data
    WEATHER->>API: Weather forecast + conditions
    
    API->>DB: Get farmer fields + history
    DB->>API: Field data + irrigation history
    
    API->>AI: Generate recommendations request
    AI->>REC: Calculate base recommendation
    
    Note over REC: Physics-based calculation:<br/>- Evapotranspiration (Penman-Monteith)<br/>- Soil water balance<br/>- Crop coefficients
    
    REC->>AI: Base recommendation data
    AI->>CLAUDE: Enhance with AI reasoning
    
    Note over CLAUDE: AI Enhancement:<br/>- Contextual explanations<br/>- Local language adaptation<br/>- Confidence scoring
    
    CLAUDE->>AI: Enhanced recommendation
    AI->>API: Final recommendation
    
    API->>DB: Store recommendation
    API->>SMS: Send SMS alert
    SMS->>F: "Kal shaam 25mm paani dein"
    
    F->>WA: Check web app
    WA->>API: Get today's recommendation
    API->>WA: Recommendation + reasoning
    WA->>F: Display visual recommendation
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph "Input Data Sources"
        WD[🌡️ Weather Data<br/>IMD + OpenWeather]
        SD[🛰️ Satellite Data<br/>Soil Moisture]
        FD[🏞️ Field Data<br/>Farmer Input]
        HD[📊 Historical Data<br/>Irrigation Logs]
    end
    
    subgraph "AI Processing Pipeline"
        DP[🔄 Data Preprocessing<br/>Validation + Cleaning]
        FE[⚙️ Feature Engineering<br/>Crop Coefficients]
        ML[🤖 ML Models<br/>Pattern Recognition]
        PE[🧮 Physics Engine<br/>Evapotranspiration]
        AI_ENH[✨ AI Enhancement<br/>Claude Integration]
    end
    
    subgraph "Output Generation"
        RG[📋 Recommendation<br/>Generation]
        LT[🌍 Language<br/>Translation]
        FMT[📱 Format for<br/>Channels]
    end
    
    subgraph "Delivery Channels"
        WEB[🌐 Web Dashboard]
        SMS_OUT[📨 SMS Alerts]
        API_OUT[🔌 API Response]
    end
    
    WD --> DP
    SD --> DP
    FD --> DP
    HD --> DP
    
    DP --> FE
    FE --> ML
    FE --> PE
    ML --> AI_ENH
    PE --> AI_ENH
    
    AI_ENH --> RG
    RG --> LT
    LT --> FMT
    
    FMT --> WEB
    FMT --> SMS_OUT
    FMT --> API_OUT
    
    %% Feedback Loop
    API_OUT -.-> HD
    SMS_OUT -.-> HD
    WEB -.-> HD
```

## Technology Stack Details

### Frontend Technologies
- **React 18+** with TypeScript
- **Tailwind CSS** for responsive design
- **PWA** with service workers for offline support
- **React Query** for data fetching and caching
- **i18next** for internationalization

### Backend Technologies
- **Python 3.11+** with FastAPI
- **Pydantic** for data validation
- **SQLAlchemy** with async support
- **Alembic** for database migrations
- **Celery** for background tasks
- **Redis** for caching and task queue

### AI & ML Stack
- **Claude API** (Anthropic) for intelligent reasoning
- **NumPy/SciPy** for scientific calculations
- **Pandas** for data manipulation
- **Scikit-learn** for ML models
- **Custom physics models** for evapotranspiration

### Infrastructure
- **PostgreSQL 15+** for primary database
- **Redis 7+** for caching and sessions
- **InfluxDB** for time-series metrics
- **NGINX** for load balancing
- **Docker** for containerization
- **Kubernetes** for orchestration

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        WAF[🛡️ Web Application Firewall<br/>DDoS Protection]
        TLS[🔒 TLS 1.3 Encryption<br/>End-to-End]
        AUTH_LAYER[🔐 Authentication Layer<br/>JWT + OTP]
        RBAC[👥 Role-Based Access<br/>Farmer/Admin]
        DATA_ENC[🔐 Data Encryption<br/>At Rest + Transit]
        AUDIT[📋 Audit Logging<br/>All Actions]
    end
    
    subgraph "Compliance & Privacy"
        GDPR[📜 GDPR Compliance<br/>Data Rights]
        PII[🔒 PII Protection<br/>Anonymization]
        BACKUP_SEC[💾 Secure Backups<br/>Encrypted]
    end
    
    WAF --> TLS
    TLS --> AUTH_LAYER
    AUTH_LAYER --> RBAC
    RBAC --> DATA_ENC
    DATA_ENC --> AUDIT
    
    AUDIT --> GDPR
    DATA_ENC --> PII
    DATA_ENC --> BACKUP_SEC
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Load Balancer Tier"
            LB1[NGINX LB 1]
            LB2[NGINX LB 2]
        end
        
        subgraph "Application Tier"
            APP1[FastAPI Instance 1]
            APP2[FastAPI Instance 2]
            APP3[FastAPI Instance 3]
        end
        
        subgraph "Database Tier"
            DB_MASTER[(PostgreSQL Master)]
            DB_REPLICA[(PostgreSQL Replica)]
            REDIS_CLUSTER[(Redis Cluster)]
        end
        
        subgraph "Background Services"
            CELERY1[Celery Worker 1]
            CELERY2[Celery Worker 2]
            SCHEDULER[Celery Beat Scheduler]
        end
    end
    
    subgraph "Monitoring & Logging"
        PROMETHEUS[Prometheus]
        GRAFANA[Grafana]
        ELK[ELK Stack]
    end
    
    LB1 --> APP1
    LB1 --> APP2
    LB2 --> APP2
    LB2 --> APP3
    
    APP1 --> DB_MASTER
    APP2 --> DB_MASTER
    APP3 --> DB_MASTER
    
    DB_MASTER --> DB_REPLICA
    
    APP1 --> REDIS_CLUSTER
    APP2 --> REDIS_CLUSTER
    APP3 --> REDIS_CLUSTER
    
    SCHEDULER --> CELERY1
    SCHEDULER --> CELERY2
    
    APP1 --> PROMETHEUS
    APP2 --> PROMETHEUS
    APP3 --> PROMETHEUS
    
    PROMETHEUS --> GRAFANA
    APP1 --> ELK
    APP2 --> ELK
    APP3 --> ELK
```

## Key Architectural Decisions

### 1. AI-First Approach
- **Claude API Integration**: Provides contextual reasoning and natural language explanations
- **Hybrid Model**: Combines physics-based calculations with AI enhancement
- **Confidence Scoring**: AI provides confidence levels for recommendations

### 2. Multi-Language Support
- **Template-based Translation**: Efficient localization for 8 Indian languages
- **AI-Powered Adaptation**: Claude helps adapt agricultural terminology
- **SMS Optimization**: Language-specific character limits and formatting

### 3. Offline-First Design
- **Progressive Web App**: Works offline with cached recommendations
- **Data Synchronization**: Automatic sync when connectivity returns
- **SMS Fallback**: Critical alerts via SMS when internet is unavailable

### 4. Scalable Architecture
- **Microservices**: Loosely coupled services for independent scaling
- **Caching Strategy**: Multi-layer caching for performance
- **Background Processing**: Async tasks for recommendation generation

### 5. Rural-Optimized
- **Low Bandwidth**: Optimized for 2G/3G connections
- **Progressive Loading**: Critical content loads first
- **Compression**: Efficient data transfer protocols