"""
Farmer repository with specialized queries

This module provides CRUD operations and custom queries for Farmer entities.
"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging

from app.models.farmer import Farmer
from app.repositories.base import BaseRepository, RepositoryError

logger = logging.getLogger(__name__)


class FarmerRepository(BaseRepository[Farmer]):
    """Repository for Farmer entity operations"""

    def __init__(self, db):
        super().__init__(Farmer, db)

    def get_by_phone_number(self, phone_number: str) -> Optional[Farmer]:
        """
        Get farmer by phone number
        
        Args:
            phone_number: Farmer's phone number
            
        Returns:
            Farmer instance or None if not found
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = select(Farmer).where(Farmer.phone_number == phone_number)
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get farmer by phone={phone_number}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve farmer: {str(e)}")

    def get_by_language(self, language: str, skip: int = 0, limit: int = 100) -> List[Farmer]:
        """
        Get farmers by preferred language
        
        Args:
            language: Language code (e.g., 'hi', 'en')
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of farmers with specified language preference
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Farmer)
                .where(Farmer.preferred_language == language)
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get farmers by language={language}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve farmers: {str(e)}")

    def get_sms_enabled_farmers(self, skip: int = 0, limit: int = 100) -> List[Farmer]:
        """
        Get farmers with SMS enabled
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of farmers with SMS enabled
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Farmer)
                .where(Farmer.sms_enabled == True)
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get SMS-enabled farmers: {str(e)}")
            raise RepositoryError(f"Failed to retrieve farmers: {str(e)}")

    def update_last_active(self, farmer_id) -> Optional[Farmer]:
        """
        Update farmer's last active timestamp
        
        Args:
            farmer_id: Farmer UUID
            
        Returns:
            Updated farmer instance or None if not found
            
        Raises:
            RepositoryError: If update fails
        """
        try:
            farmer = self.get_by_id(farmer_id)
            if not farmer:
                return None
            
            farmer.last_active = datetime.utcnow()
            self.db.commit()
            self.db.refresh(farmer)
            logger.info(f"Updated last_active for farmer id={farmer_id}")
            return farmer
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Failed to update last_active for farmer id={farmer_id}: {str(e)}")
            raise RepositoryError(f"Failed to update farmer: {str(e)}")

    def get_with_fields(self, farmer_id) -> Optional[Farmer]:
        """
        Get farmer with all related fields (eager loading)
        
        Args:
            farmer_id: Farmer UUID
            
        Returns:
            Farmer instance with fields loaded or None if not found
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            from sqlalchemy.orm import joinedload
            
            stmt = (
                select(Farmer)
                .options(joinedload(Farmer.fields))
                .where(Farmer.id == farmer_id)
            )
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get farmer with fields for id={farmer_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve farmer: {str(e)}")
