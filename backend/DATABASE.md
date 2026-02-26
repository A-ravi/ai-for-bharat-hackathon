# Jal Sathi Database Setup

This document describes the database schema, migrations, and management for the Jal Sathi application.

## Database Schema

The Jal Sathi application uses PostgreSQL with the following tables:

### Tables

1. **farmers** - Farmer profile information
   - `id` (UUID, PK)
   - `phone_number` (String, unique, indexed)
   - `preferred_language` (String)
   - `created_at` (DateTime)
   - `last_active` (DateTime)
   - `sms_enabled` (Boolean)

2. **fields** - Agricultural field information
   - `id` (UUID, PK)
   - `farmer_id` (UUID, FK to farmers, indexed)
   - `crop_type` (String)
   - `field_size_acres` (Float)
   - `location_lat` (Float)
   - `location_lng` (Float)
   - `pincode` (String)
   - `irrigation_method` (String)
   - `planting_date` (Date)
   - `created_at` (DateTime)

3. **recommendations** - Daily irrigation recommendations
   - `id` (UUID, PK)
   - `field_id` (UUID, FK to fields, indexed)
   - `date` (Date, indexed)
   - `irrigate` (Boolean)
   - `amount_mm` (Float)
   - `timing` (String)
   - `confidence` (Float)
   - `weather_data` (JSON)
   - `reasoning` (String)
   - `localized_message` (String)
   - `created_at` (DateTime)
   - Composite index: (field_id, date)

4. **irrigation_activities** - Actual irrigation activities logged
   - `id` (UUID, PK)
   - `field_id` (UUID, FK to fields, indexed)
   - `date` (Date, indexed)
   - `amount_mm` (Float)
   - `method` (String)
   - `farmer_reported` (Boolean)
   - `cost_rupees` (Float)
   - `created_at` (DateTime)
   - Composite index: (field_id, date)

5. **savings_records** - Water and cost savings calculations
   - `id` (UUID, PK)
   - `field_id` (UUID, FK to fields, indexed)
   - `period_start` (Date, indexed)
   - `period_end` (Date, indexed)
   - `water_saved_liters` (Float)
   - `cost_saved_rupees` (Float)
   - `traditional_usage_liters` (Float)
   - `actual_usage_liters` (Float)
   - `calculated_at` (DateTime)
   - Composite index: (field_id, period_start, period_end)

## Performance Optimizations

### Indexes

The schema includes several indexes for performance optimization:

1. **Single-column indexes**:
   - `farmers.phone_number` (unique) - Fast farmer lookup by phone
   - `fields.farmer_id` - Fast field lookup by farmer
   - `recommendations.field_id` - Fast recommendation lookup by field
   - `recommendations.date` - Fast recommendation lookup by date
   - `irrigation_activities.field_id` - Fast activity lookup by field
   - `irrigation_activities.date` - Fast activity lookup by date
   - `savings_records.field_id` - Fast savings lookup by field
   - `savings_records.period_start` - Fast savings lookup by period
   - `savings_records.period_end` - Fast savings lookup by period

2. **Composite indexes**:
   - `recommendations(field_id, date)` - Optimized for daily recommendation queries
   - `irrigation_activities(field_id, date)` - Optimized for activity history queries
   - `savings_records(field_id, period_start, period_end)` - Optimized for savings period queries

### Connection Pooling

The application uses SQLAlchemy connection pooling with the following configuration:

- **Pool size**: 10 connections (configurable via `DB_POOL_SIZE`)
- **Max overflow**: 20 additional connections (configurable via `DB_MAX_OVERFLOW`)
- **Pool pre-ping**: Enabled - verifies connections before use
- **Pool recycle**: 3600 seconds (1 hour) - prevents stale connections

### Error Handling

The database layer includes comprehensive error handling:

- Automatic connection verification before use
- Transaction rollback on errors
- Connection pool monitoring with event listeners
- Graceful error logging and propagation

## Database Migrations

The application uses Alembic for database migrations.

### Running Migrations

1. **Check current migration status**:
   ```bash
   cd backend
   alembic current
   ```

2. **Apply all pending migrations**:
   ```bash
   alembic upgrade head
   ```

3. **Rollback last migration**:
   ```bash
   alembic downgrade -1
   ```

4. **Create a new migration** (after modifying models):
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

### Initial Migration

The initial migration (`001_initial_schema.py`) creates all tables with proper:
- Foreign key constraints with CASCADE delete
- Indexes for performance
- Proper data types including UUID, JSON, and DateTime

## Database Management Utilities

The `app/db_utils.py` module provides utilities for database management:

### Check Database Connection
```bash
python -m app.db_utils check
```

### Verify Schema and Indexes
```bash
python -m app.db_utils verify
```

### Get Database Statistics
```bash
python -m app.db_utils stats
```

### Initialize Database (Development Only)
```bash
python -m app.db_utils init
```

## Environment Configuration

Database configuration is managed through environment variables:

```env
DATABASE_URL=postgresql://jalsathi:jalsathi@db:5432/jalsathi
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DEBUG=False
```

## Development Setup

1. Start the database container:
   ```bash
   docker compose up -d db
   ```

2. Run migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```

3. Verify setup:
   ```bash
   python -m app.db_utils verify
   ```

## Production Considerations

1. **Backups**: Set up automated daily backups with point-in-time recovery
2. **Monitoring**: Monitor connection pool usage and query performance
3. **Scaling**: Consider read replicas for high-traffic scenarios
4. **Security**: Use strong passwords and restrict database access
5. **Maintenance**: Regular VACUUM and ANALYZE operations for PostgreSQL

## Troubleshooting

### Connection Issues

If you encounter connection issues:

1. Check if PostgreSQL is running:
   ```bash
   docker compose ps db
   ```

2. Verify connection settings in `.env`

3. Test connection:
   ```bash
   python -m app.db_utils check
   ```

### Migration Issues

If migrations fail:

1. Check current migration status:
   ```bash
   alembic current
   ```

2. Review migration history:
   ```bash
   alembic history
   ```

3. If needed, manually fix the database and stamp the migration:
   ```bash
   alembic stamp head
   ```

### Performance Issues

If queries are slow:

1. Check if indexes exist:
   ```bash
   python -m app.db_utils verify
   ```

2. Monitor connection pool:
   - Check logs for connection checkout/checkin events
   - Adjust `DB_POOL_SIZE` and `DB_MAX_OVERFLOW` if needed

3. Analyze query performance:
   - Enable SQL logging with `DEBUG=True`
   - Use PostgreSQL's `EXPLAIN ANALYZE` for slow queries
