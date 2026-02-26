"""
Field repository with specialized queries

This module provides CRUD operations and custom queries for Field entities.
"""

from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
import logging

from app.models.field import Field
from app.repositories.base import BaseRepository, RepositoryError

logger = logging.getLogger(__name__)


class FieldRepository(BaseRepository[Field]):
    """Repository for Field entity operations"""

    def __init__(self, db):
        super().__init__(Field, db)

    def get_by_farmer_id(self, farmer_id: UUID, skip: int = 0, limit: int = 100) -> List[Field]:
        """
        Get all fields for a specific farmer
        
        Args:
            farmer_id: Farmer UUID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of fields owned by the farmer
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Field)
                .where(Field.farmer_id == farmer_id)
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get fields for farmer_id={farmer_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve fields: {str(e)}")

    def get_by_crop_type(self, crop_type: str, skip: int = 0, limit: int = 100) -> List[Field]:
        """
        Get fields by crop type
        
        Args:
            crop_type: Type of crop
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of fields with specified crop type
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Field)
                .where(Field.crop_type == crop_type)
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get fields by crop_type={crop_type}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve fields: {str(e)}")

    def get_by_pincode(self, pincode: str, skip: int = 0, limit: int = 100) -> List[Field]:
        """
        Get fields by pincode
        
        Args:
            pincode: Postal code
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of fields in specified pincode area
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Field)
                .where(Field.pincode == pincode)
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get fields by pincode={pincode}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve fields: {str(e)}")

    def get_by_location_range(
        self,
        min_lat: float,
        max_lat: float,
        min_lng: float,
        max_lng: float,
        skip: int = 0,
        limit: int = 100
    ) -> List[Field]:
        """
        Get fields within a geographic bounding box
        
        Args:
            min_lat: Minimum latitude
            max_lat: Maximum latitude
            min_lng: Minimum longitude
            max_lng: Maximum longitude
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of fields within the specified area
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Field)
                .where(
                    and_(
                        Field.location_lat >= min_lat,
                        Field.location_lat <= max_lat,
                        Field.location_lng >= min_lng,
                        Field.location_lng <= max_lng
                    )
                )
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get fields by location range: {str(e)}")
            raise RepositoryError(f"Failed to retrieve fields: {str(e)}")

    def get_with_recommendations(self, field_id: UUID) -> Optional[Field]:
        """
        Get field with all related recommendations (eager loading)
        
        Args:
            field_id: Field UUID
            
        Returns:
            Field instance with recommendations loaded or None if not found
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            from sqlalchemy.orm import joinedload
            
            stmt = (
                select(Field)
                .options(joinedload(Field.recommendations))
                .where(Field.id == field_id)
            )
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get field with recommendations for id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve field: {str(e)}")

    def count_by_farmer(self, farmer_id: UUID) -> int:
        """
        Count fields for a specific farmer
        
        Args:
            farmer_id: Farmer UUID
            
        Returns:
            Number of fields owned by the farmer
            
        Raises:
            RepositoryError: If count fails
        """
        try:
            from sqlalchemy import func
            stmt = select(func.count()).select_from(Field).where(Field.farmer_id == farmer_id)
            result = self.db.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Failed to count fields for farmer_id={farmer_id}: {str(e)}")
            raise RepositoryError(f"Failed to count fields: {str(e)}")
