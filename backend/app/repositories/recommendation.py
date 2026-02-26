"""
Recommendation repository with specialized queries

This module provides CRUD operations and custom queries for Recommendation entities.
"""

from typing import Optional, List
from sqlalchemy import select, and_, desc
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from datetime import date, datetime
import logging

from app.models.recommendation import Recommendation
from app.repositories.base import BaseRepository, RepositoryError

logger = logging.getLogger(__name__)


class RecommendationRepository(BaseRepository[Recommendation]):
    """Repository for Recommendation entity operations"""

    def __init__(self, db):
        super().__init__(Recommendation, db)

    def get_by_field_id(
        self,
        field_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Recommendation]:
        """
        Get all recommendations for a specific field
        
        Args:
            field_id: Field UUID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of recommendations for the field, ordered by date descending
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Recommendation)
                .where(Recommendation.field_id == field_id)
                .order_by(desc(Recommendation.date))
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get recommendations for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve recommendations: {str(e)}")

    def get_by_field_and_date(self, field_id: UUID, date_value: date) -> Optional[Recommendation]:
        """
        Get recommendation for a specific field and date
        
        Args:
            field_id: Field UUID
            date_value: Date of recommendation
            
        Returns:
            Recommendation instance or None if not found
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = select(Recommendation).where(
                and_(
                    Recommendation.field_id == field_id,
                    Recommendation.date == date_value
                )
            )
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get recommendation for field_id={field_id}, date={date_value}: {str(e)}"
            )
            raise RepositoryError(f"Failed to retrieve recommendation: {str(e)}")

    def get_by_date_range(
        self,
        field_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[Recommendation]:
        """
        Get recommendations for a field within a date range
        
        Args:
            field_id: Field UUID
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of recommendations within the date range, ordered by date
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Recommendation)
                .where(
                    and_(
                        Recommendation.field_id == field_id,
                        Recommendation.date >= start_date,
                        Recommendation.date <= end_date
                    )
                )
                .order_by(Recommendation.date)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get recommendations for field_id={field_id}, "
                f"date range {start_date} to {end_date}: {str(e)}"
            )
            raise RepositoryError(f"Failed to retrieve recommendations: {str(e)}")

    def get_latest_by_field(self, field_id: UUID) -> Optional[Recommendation]:
        """
        Get the most recent recommendation for a field
        
        Args:
            field_id: Field UUID
            
        Returns:
            Latest recommendation or None if no recommendations exist
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Recommendation)
                .where(Recommendation.field_id == field_id)
                .order_by(desc(Recommendation.date))
                .limit(1)
            )
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get latest recommendation for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve recommendation: {str(e)}")

    def get_irrigation_recommendations(
        self,
        field_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[Recommendation]:
        """
        Get recommendations where irrigation is recommended
        
        Args:
            field_id: Field UUID
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of recommendations with irrigate=True
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(Recommendation)
                .where(
                    and_(
                        Recommendation.field_id == field_id,
                        Recommendation.date >= start_date,
                        Recommendation.date <= end_date,
                        Recommendation.irrigate == True
                    )
                )
                .order_by(Recommendation.date)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get irrigation recommendations for field_id={field_id}: {str(e)}"
            )
            raise RepositoryError(f"Failed to retrieve recommendations: {str(e)}")

    def count_by_field(self, field_id: UUID) -> int:
        """
        Count recommendations for a specific field
        
        Args:
            field_id: Field UUID
            
        Returns:
            Number of recommendations for the field
            
        Raises:
            RepositoryError: If count fails
        """
        try:
            from sqlalchemy import func
            stmt = (
                select(func.count())
                .select_from(Recommendation)
                .where(Recommendation.field_id == field_id)
            )
            result = self.db.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Failed to count recommendations for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to count recommendations: {str(e)}")
