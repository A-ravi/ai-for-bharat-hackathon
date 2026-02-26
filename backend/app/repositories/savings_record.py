"""
Savings Record repository with specialized queries

This module provides CRUD operations and custom queries for SavingsRecord entities.
"""

from typing import Optional, List
from sqlalchemy import select, and_, desc, func
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from datetime import date
import logging

from app.models.savings_record import SavingsRecord
from app.repositories.base import BaseRepository, RepositoryError

logger = logging.getLogger(__name__)


class SavingsRecordRepository(BaseRepository[SavingsRecord]):
    """Repository for SavingsRecord entity operations"""

    def __init__(self, db):
        super().__init__(SavingsRecord, db)

    def get_by_field_id(
        self,
        field_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[SavingsRecord]:
        """
        Get all savings records for a specific field
        
        Args:
            field_id: Field UUID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of savings records for the field, ordered by period_start descending
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(SavingsRecord)
                .where(SavingsRecord.field_id == field_id)
                .order_by(desc(SavingsRecord.period_start))
                .offset(skip)
                .limit(limit)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get savings records for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve savings records: {str(e)}")

    def get_by_period(
        self,
        field_id: UUID,
        period_start: date,
        period_end: date
    ) -> Optional[SavingsRecord]:
        """
        Get savings record for a specific field and period
        
        Args:
            field_id: Field UUID
            period_start: Start date of period
            period_end: End date of period
            
        Returns:
            SavingsRecord instance or None if not found
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = select(SavingsRecord).where(
                and_(
                    SavingsRecord.field_id == field_id,
                    SavingsRecord.period_start == period_start,
                    SavingsRecord.period_end == period_end
                )
            )
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get savings record for field_id={field_id}, "
                f"period {period_start} to {period_end}: {str(e)}"
            )
            raise RepositoryError(f"Failed to retrieve savings record: {str(e)}")

    def get_overlapping_periods(
        self,
        field_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[SavingsRecord]:
        """
        Get savings records that overlap with a given date range
        
        Args:
            field_id: Field UUID
            start_date: Start date to check
            end_date: End date to check
            
        Returns:
            List of savings records with overlapping periods
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(SavingsRecord)
                .where(
                    and_(
                        SavingsRecord.field_id == field_id,
                        SavingsRecord.period_start <= end_date,
                        SavingsRecord.period_end >= start_date
                    )
                )
                .order_by(SavingsRecord.period_start)
            )
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to get overlapping savings records for field_id={field_id}: {str(e)}"
            )
            raise RepositoryError(f"Failed to retrieve savings records: {str(e)}")

    def get_latest_by_field(self, field_id: UUID) -> Optional[SavingsRecord]:
        """
        Get the most recent savings record for a field
        
        Args:
            field_id: Field UUID
            
        Returns:
            Latest savings record or None if no records exist
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(SavingsRecord)
                .where(SavingsRecord.field_id == field_id)
                .order_by(desc(SavingsRecord.period_start))
                .limit(1)
            )
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get latest savings record for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve savings record: {str(e)}")

    def calculate_total_water_saved(
        self,
        field_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> float:
        """
        Calculate total water saved for a field
        
        Args:
            field_id: Field UUID
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            Total water saved in liters
            
        Raises:
            RepositoryError: If calculation fails
        """
        try:
            conditions = [SavingsRecord.field_id == field_id]
            
            if start_date:
                conditions.append(SavingsRecord.period_end >= start_date)
            if end_date:
                conditions.append(SavingsRecord.period_start <= end_date)
            
            stmt = (
                select(func.sum(SavingsRecord.water_saved_liters))
                .where(and_(*conditions))
            )
            result = self.db.execute(stmt)
            total = result.scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            logger.error(f"Failed to calculate total water saved for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to calculate water savings: {str(e)}")

    def calculate_total_cost_saved(
        self,
        field_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> float:
        """
        Calculate total cost saved for a field
        
        Args:
            field_id: Field UUID
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            Total cost saved in rupees
            
        Raises:
            RepositoryError: If calculation fails
        """
        try:
            conditions = [SavingsRecord.field_id == field_id]
            
            if start_date:
                conditions.append(SavingsRecord.period_end >= start_date)
            if end_date:
                conditions.append(SavingsRecord.period_start <= end_date)
            
            stmt = (
                select(func.sum(SavingsRecord.cost_saved_rupees))
                .where(and_(*conditions))
            )
            result = self.db.execute(stmt)
            total = result.scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            logger.error(f"Failed to calculate total cost saved for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to calculate cost savings: {str(e)}")

    def get_savings_summary(self, field_id: UUID) -> dict:
        """
        Get comprehensive savings summary for a field
        
        Args:
            field_id: Field UUID
            
        Returns:
            Dictionary with total water saved, cost saved, and record count
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = (
                select(
                    func.sum(SavingsRecord.water_saved_liters).label('total_water_saved'),
                    func.sum(SavingsRecord.cost_saved_rupees).label('total_cost_saved'),
                    func.count().label('record_count')
                )
                .where(SavingsRecord.field_id == field_id)
            )
            result = self.db.execute(stmt)
            row = result.one()
            
            return {
                'total_water_saved_liters': row.total_water_saved if row.total_water_saved else 0.0,
                'total_cost_saved_rupees': row.total_cost_saved if row.total_cost_saved else 0.0,
                'record_count': row.record_count if row.record_count else 0
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to get savings summary for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve savings summary: {str(e)}")

    def count_by_field(self, field_id: UUID) -> int:
        """
        Count savings records for a specific field
        
        Args:
            field_id: Field UUID
            
        Returns:
            Number of savings records for the field
            
        Raises:
            RepositoryError: If count fails
        """
        try:
            stmt = (
                select(func.count())
                .select_from(SavingsRecord)
                .where(SavingsRecord.field_id == field_id)
            )
            result = self.db.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Failed to count savings records for field_id={field_id}: {str(e)}")
            raise RepositoryError(f"Failed to count savings records: {str(e)}")
