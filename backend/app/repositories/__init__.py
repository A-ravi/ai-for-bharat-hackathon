"""
Repository layer for database operations

This module provides the repository pattern implementation for all models,
with CRUD operations, transaction management, and error handling.
"""

from app.repositories.base import BaseRepository
from app.repositories.farmer import FarmerRepository
from app.repositories.field import FieldRepository
from app.repositories.recommendation import RecommendationRepository
from app.repositories.irrigation_activity import IrrigationActivityRepository
from app.repositories.savings_record import SavingsRecordRepository

__all__ = [
    "BaseRepository",
    "FarmerRepository",
    "FieldRepository",
    "RecommendationRepository",
    "IrrigationActivityRepository",
    "SavingsRecordRepository",
]
