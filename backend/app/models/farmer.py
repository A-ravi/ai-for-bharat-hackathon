from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    preferred_language = Column(String(10), nullable=False, default="en")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_active = Column(DateTime, nullable=False, default=datetime.utcnow)
    sms_enabled = Column(Boolean, nullable=False, default=True)

    # Relationships
    fields = relationship("Field", back_populates="farmer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Farmer(id={self.id}, phone={self.phone_number}, language={self.preferred_language})>"
