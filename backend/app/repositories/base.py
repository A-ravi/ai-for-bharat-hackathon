"""
Base repository class with common CRUD operations

This module provides a generic base repository with transaction management
and error handling for all database operations.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select, update, delete
from uuid import UUID
import logging

from app.core.database import Base

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)


class RepositoryError(Exception):
    """Base exception for repository errors"""
    pass


class NotFoundError(RepositoryError):
    """Raised when a requested entity is not found"""
    pass


class DuplicateError(RepositoryError):
    """Raised when attempting to create a duplicate entity"""
    pass


class BaseRepository(Generic[ModelType]):
    """
    Base repository class providing common CRUD operations
    
    This class implements the repository pattern with:
    - Transaction management
    - Error handling and logging
    - Common CRUD operations
    - Type safety with generics
    """

    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db

    def create(self, obj: ModelType) -> ModelType:
        """
        Create a new entity
        
        Args:
            obj: Model instance to create
            
        Returns:
            Created model instance with ID
            
        Raises:
            DuplicateError: If entity violates unique constraints
            RepositoryError: If creation fails
        """
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            logger.info(f"Created {self.model.__name__} with id={obj.id}")
            return obj
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Duplicate {self.model.__name__}: {str(e)}")
            raise DuplicateError(f"Entity already exists: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Failed to create {self.model.__name__}: {str(e)}")
            raise RepositoryError(f"Failed to create entity: {str(e)}")

    def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """
        Get entity by ID
        
        Args:
            id: Entity UUID
            
        Returns:
            Model instance or None if not found
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = self.db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get {self.model.__name__} by id={id}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve entity: {str(e)}")

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all entities with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
            
        Raises:
            RepositoryError: If query fails
        """
        try:
            stmt = select(self.model).offset(skip).limit(limit)
            result = self.db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Failed to get all {self.model.__name__}: {str(e)}")
            raise RepositoryError(f"Failed to retrieve entities: {str(e)}")

    def update(self, id: UUID, data: Dict[str, Any]) -> Optional[ModelType]:
        """
        Update entity by ID
        
        Args:
            id: Entity UUID
            data: Dictionary of fields to update
            
        Returns:
            Updated model instance or None if not found
            
        Raises:
            RepositoryError: If update fails
        """
        try:
            # First check if entity exists
            obj = self.get_by_id(id)
            if not obj:
                return None
            
            # Update fields
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            
            self.db.commit()
            self.db.refresh(obj)
            logger.info(f"Updated {self.model.__name__} with id={id}")
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Failed to update {self.model.__name__} with id={id}: {str(e)}")
            raise RepositoryError(f"Failed to update entity: {str(e)}")

    def delete(self, id: UUID) -> bool:
        """
        Delete entity by ID
        
        Args:
            id: Entity UUID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            RepositoryError: If deletion fails
        """
        try:
            obj = self.get_by_id(id)
            if not obj:
                return False
            
            self.db.delete(obj)
            self.db.commit()
            logger.info(f"Deleted {self.model.__name__} with id={id}")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Failed to delete {self.model.__name__} with id={id}: {str(e)}")
            raise RepositoryError(f"Failed to delete entity: {str(e)}")

    def exists(self, id: UUID) -> bool:
        """
        Check if entity exists
        
        Args:
            id: Entity UUID
            
        Returns:
            True if exists, False otherwise
        """
        try:
            return self.get_by_id(id) is not None
        except RepositoryError:
            return False

    def count(self) -> int:
        """
        Count total entities
        
        Returns:
            Total count of entities
            
        Raises:
            RepositoryError: If count fails
        """
        try:
            from sqlalchemy import func
            stmt = select(func.count()).select_from(self.model)
            result = self.db.execute(stmt)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Failed to count {self.model.__name__}: {str(e)}")
            raise RepositoryError(f"Failed to count entities: {str(e)}")
