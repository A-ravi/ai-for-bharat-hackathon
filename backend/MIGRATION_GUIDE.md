# Database Migration Guide

This guide explains how to set up and run database migrations for Jal Sathi.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ installed
- PostgreSQL database running (via Docker Compose)

## Quick Start

### 1. Start the Database

```bash
# From the project root
docker compose up -d db
```

Wait a few seconds for PostgreSQL to initialize.

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
# Apply all migrations
alembic upgrade head
```

### 4. Verify Setup

```bash
# Check database connection
python -m app.db_utils check

# Verify schema and indexes
python -m app.db_utils verify

# Get database statistics
python -m app.db_utils stats
```

## Migration Commands

### Check Current Migration Status

```bash
alembic current
```

This shows which migration is currently applied.

### View Migration History

```bash
alembic history --verbose
```

This shows all available migrations.

### Upgrade to Latest

```bash
alembic upgrade head
```

Applies all pending migrations.

### Upgrade by Steps

```bash
# Upgrade one migration
alembic upgrade +1

# Upgrade to specific revision
alembic upgrade 001
```

### Downgrade

```bash
# Downgrade one migration
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade 001

# Downgrade all
alembic downgrade base
```

## Creating New Migrations

### Auto-generate Migration

After modifying models in `app/models/`:

```bash
alembic revision --autogenerate -m "Description of changes"
```

This will:
1. Compare your models with the current database schema
2. Generate a new migration file in `alembic/versions/`
3. Include upgrade and downgrade functions

### Manual Migration

For complex changes:

```bash
alembic revision -m "Description of changes"
```

Then edit the generated file to add your custom migration logic.

## Migration File Structure

```python
"""Description of changes

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add your upgrade logic here
    pass

def downgrade() -> None:
    # Add your downgrade logic here
    pass
```

## Common Migration Operations

### Add a Column

```python
def upgrade():
    op.add_column('table_name', 
        sa.Column('new_column', sa.String(50), nullable=True))

def downgrade():
    op.drop_column('table_name', 'new_column')
```

### Add an Index

```python
def upgrade():
    op.create_index('ix_table_column', 'table_name', ['column_name'])

def downgrade():
    op.drop_index('ix_table_column', table_name='table_name')
```

### Modify a Column

```python
def upgrade():
    op.alter_column('table_name', 'column_name',
        type_=sa.String(100),
        existing_type=sa.String(50))

def downgrade():
    op.alter_column('table_name', 'column_name',
        type_=sa.String(50),
        existing_type=sa.String(100))
```

## Troubleshooting

### Migration Already Applied

If you see "Target database is not up to date":

```bash
# Check current status
alembic current

# If needed, stamp the database
alembic stamp head
```

### Migration Conflicts

If you have multiple migration branches:

```bash
# View branches
alembic branches

# Merge branches
alembic merge -m "Merge branches" <rev1> <rev2>
```

### Database Connection Issues

If migrations fail to connect:

1. Check if database is running:
   ```bash
   docker compose ps db
   ```

2. Verify connection string in `.env`:
   ```
   DATABASE_URL=postgresql://jalsathi:jalsathi@db:5432/jalsathi
   ```

3. Test connection:
   ```bash
   python -m app.db_utils check
   ```

### Reset Database (Development Only)

To completely reset the database:

```bash
# Stop and remove database container
docker compose down -v

# Start fresh database
docker compose up -d db

# Wait a few seconds, then run migrations
alembic upgrade head
```

## Best Practices

1. **Always test migrations** in development before production
2. **Create backups** before running migrations in production
3. **Review auto-generated migrations** - they may need manual adjustments
4. **Keep migrations small** - one logical change per migration
5. **Test both upgrade and downgrade** paths
6. **Never modify existing migrations** that have been applied to production
7. **Use descriptive migration messages** for easy identification

## Production Deployment

For production deployments:

1. **Backup the database** before running migrations
2. **Test migrations** on a staging environment first
3. **Plan for downtime** if needed for complex migrations
4. **Monitor the migration** process for errors
5. **Have a rollback plan** ready

Example production migration workflow:

```bash
# 1. Backup database
pg_dump -h localhost -U jalsathi jalsathi > backup_$(date +%Y%m%d).sql

# 2. Check current status
alembic current

# 3. Review pending migrations
alembic history

# 4. Apply migrations
alembic upgrade head

# 5. Verify
python -m app.db_utils verify

# 6. If issues, rollback
alembic downgrade -1
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
