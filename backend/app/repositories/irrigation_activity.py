"""
Irrigation Activity repository with specialized queries

This module provides CRUD operations and custom queries for IrrigationActivity entities.
"""

from typing import Optional, List
from sqlalchemy import select, and_, desc, func
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from datetime import date
import logging

from app.models.irrigation_activity import IrrigationActivity
from app.repositories.base import BaseRepository, RepositoryError

logger = logging.getLogger(__name__)


class IrrigationActivityRepository(BaseRepository[IrrigationActivity]):
    """Repository for IrrigationActivity entity operations"""

    def __init__(self, db):
        super().__init__(IrrigationActivity, db)

    def get_by_field_id(
        self,
        field_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[IrrigationActivity]:
        """
        Get all irrigation activities for a specific field
        
        Args:
            field_id: Field UUID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of irrigation activities for the field, ordered by date descending
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(IrrigationActivity)
                .where(IrrigationActivity.field_id == field_id)
                .order_by(desc(IrrigationActivity.date))
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get irrigation activities for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve irrigation activities: {str(e)}")

    def get_by_field_and_date(
        self,
        field_id: UUID,
        date_value: date
    ) -> Optional[IrrigationActivity]:
        """
        Get irrigation activity for a specific field and date
        
        Args:
            field_id: Field UUID
            date_value: Date of activity
            
        Returns:
            IrrigationActivity instance or None if not found
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = select(IrrigationActivity).where(
                and_(
                    IrrigationActivity.field_id == field_id,
                    IrrigationActivity.date == date_value
                )
            )
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get irrigation activity for field_id={field_id}, "
                f"date={date_value}: {str(e)}"
            )
            raise RepositoryError(f"Failed to retrieve irrigation activity: {str(e)}")

    def get_by_date_range(
        self,
        field_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[IrrigationActivity]:
        """
        Get irrigation activities for a field within a date range
        
        Args:
            field_id: Field UUID
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of irrigation activities within the date range, ordered by date
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(IrrigationActivity)
                .where(
                    and_(
                        IrrigationActivity.field_id == field_id,
                        IrrigationActivity.date >= start_date,
                        IrrigationActivity.date <= end_date
                    )
                )
                .order_by(IrrigationActivity.date)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get irrigation activities for field_id={field_id}, "
                f"date range {start_date} to {end_date}: {str(e)}"
            )
            raise RepositoryError(f"Failed to retrieve irrigation activities: {str(e)}")

    def get_farmer_reported(
        self,
        field_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[IrrigationActivity]:
        """
        Get farmer-reported irrigation activities
        
        Args:
            field_id: Field UUID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of farmer-reported irrigation activities
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(IrrigationActivity)
                .where(
                    and_(
                        IrrigationActivity.field_id == field_id,
                        IrrigationActivity.farmer_reported == True
                    )
                )
                .order_by(desc(IrrigationActivity.date))
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get farmer-reported activities for field_id={field_id}: {str(e)}"
            )
            raise RepositoryError(f"Failed to retrieve irrigation activities: {str(e)}")

    def calculate_total_water_usage(
        self,
        field_id: UUID,
        start_date: date,
        end_date: date
    ) -> float:
        """
        Calculate total water usage for a field in a date range
        
        Args:
            field_id: Field UUID
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            Total water usage in millimeters
            
        Raises:
            RepositoryError: If calculation fails
        """
        try:
            stmt = (
                select(func.sum(IrrigationActivity.amount_mm))
                .where(
                    and_(
                        IrrigationActivity.field_id == field_id,
                        IrrigationActivity.date >= start_date,
                        IrrigationActivity.date <= end_date
                    )
                )
            )
            result = self.db.execute(stmt)
            total = result.scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to calculate water usage for field_id={field_id}: {str(e)}"
            )
            raise RepositoryError(f"Failed to calculate water usage: {str(e)}")

    def calculate_total_cost(
        self,
        field_id: UUID,
        start_date: date,
        end_date: date
    ) -> float:
        """
        Calculate total irrigation cost for a field in a date range
        
        Args:
            field_id: Field UUID
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            Total cost in rupees
            
        Raises:
            RepositoryError: If calculation fails
        """
        try:
            stmt = (
                select(func.sum(IrrigationActivity.cost_rupees))
                .where(
                    and_(
                        IrrigationActivity.field_id == field_id,
                        IrrigationActivity.date >= start_date,
                        IrrigationActivity.date <= end_date
                    )
                )
            )
            result = self.db.execute(stmt)
            total = result.scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to calculate irrigation cost for field_id={field_id}: {str(e)}"
            )
            raise RepositoryError(f"Failed to calculate cost: {str(e)}")

    def count_by_field(self, field_id: UUID) -> int:
        """
        Count irrigation activities for a specific field
        
        Args:
            field_id: Field UUID
            
        Returns:
            Number of irrigation activities for the field
            
        Raises:
            RepositoryError: If count fails
        """
        try:
            stmt = (
                select(func.count())
                .select_from(IrrigationActivity)
                .where(IrrigationActivity.field_id == field_id)
            )
            result = self.db.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to count irrigation activities for field_id={field_id}: {str(e)}"
            )
            raise RepositoryError(f"Failed to count irrigation activities: {str(e)}")
