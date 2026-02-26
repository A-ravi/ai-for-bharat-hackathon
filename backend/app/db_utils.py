"""
Database utility functions for Jal Sathi

This module provides utilities for database management, migrations,
and health checks.
"""

import sys
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import engine, check_db_connection, init_db
from app.models import Farmer, Field, Recommendation, IrrigationActivity, SavingsRecord
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_schema():
    """
    Verify that all database tables exist and have correct structure
    
    Returns:
        bool: True if schema is valid, False otherwise
    """
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        expected_tables = [
            'farmers',
            'fields',
            'recommendations',
            'irrigation_activities',
            'savings_records'
        ]
        
        existing_tables = inspector.get_table_names()
        
        for table in expected_tables:
            if table not in existing_tables:
                logger.error(f"Missing table: {table}")
                return False
            else:
                logger.info(f"✓ Table exists: {table}")
        
        logger.info("All required tables exist")
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"Schema verification failed: {str(e)}")
        return False


def verify_indexes():
    """
    Verify that all required indexes exist for performance optimization
    
    Returns:
        bool: True if all indexes exist, False otherwise
    """
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        # Check critical indexes
        critical_indexes = {
            'farmers': ['ix_farmers_phone_number'],
            'fields': ['ix_fields_farmer_id'],
            'recommendations': ['ix_recommendations_field_id', 'ix_recommendations_date', 'ix_recommendations_field_date'],
            'irrigation_activities': ['ix_irrigation_activities_field_id', 'ix_irrigation_activities_date', 'ix_irrigation_activities_field_date'],
            'savings_records': ['ix_savings_records_field_id', 'ix_savings_records_period_start', 'ix_savings_records_period_end', 'ix_savings_records_field_period']
        }
        
        all_indexes_exist = True
        
        for table, expected_indexes in critical_indexes.items():
            existing_indexes = [idx['name'] for idx in inspector.get_indexes(table)]
            
            for idx_name in expected_indexes:
                if idx_name in existing_indexes:
                    logger.info(f"✓ Index exists: {table}.{idx_name}")
                else:
                    logger.warning(f"✗ Missing index: {table}.{idx_name}")
                    all_indexes_exist = False
        
        return all_indexes_exist
        
    except SQLAlchemyError as e:
        logger.error(f"Index verification failed: {str(e)}")
        return False


def get_db_stats():
    """
    Get database statistics including table row counts
    
    Returns:
        dict: Dictionary with table names and row counts
    """
    try:
        from sqlalchemy import text
        
        stats = {}
        tables = ['farmers', 'fields', 'recommendations', 'irrigation_activities', 'savings_records']
        
        with engine.connect() as conn:
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                stats[table] = count
                logger.info(f"{table}: {count} rows")
        
        return stats
        
    except SQLAlchemyError as e:
        logger.error(f"Failed to get database stats: {str(e)}")
        return {}


def main():
    """Main function for CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python -m app.db_utils [check|verify|stats|init]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        logger.info("Checking database connection...")
        if check_db_connection():
            logger.info("✓ Database connection successful")
            sys.exit(0)
        else:
            logger.error("✗ Database connection failed")
            sys.exit(1)
    
    elif command == "verify":
        logger.info("Verifying database schema...")
        schema_ok = verify_schema()
        indexes_ok = verify_indexes()
        
        if schema_ok and indexes_ok:
            logger.info("✓ Database schema and indexes verified")
            sys.exit(0)
        else:
            logger.error("✗ Database verification failed")
            sys.exit(1)
    
    elif command == "stats":
        logger.info("Getting database statistics...")
        stats = get_db_stats()
        if stats:
            logger.info("✓ Database statistics retrieved")
            sys.exit(0)
        else:
            logger.error("✗ Failed to get database statistics")
            sys.exit(1)
    
    elif command == "init":
        logger.warning("Initializing database (development only)...")
        try:
            init_db()
            logger.info("✓ Database initialized")
            sys.exit(0)
        except Exception as e:
            logger.error(f"✗ Database initialization failed: {str(e)}")
            sys.exit(1)
    
    else:
        logger.error(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
