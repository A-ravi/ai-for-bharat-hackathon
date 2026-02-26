from sqlalchemy import Column, String, Float, DateTime, Date, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    irrigate = Column(Boolean, nullable=False)
    amount_mm = Column(Float, nullable=False)
    timing = Column(String(20), nullable=False)  # morning, afternoon, evening
    confidence = Column(Float, nullable=False)
    weather_data = Column(JSON, nullable=False)
    reasoning = Column(String(500), nullable=False)
    localized_message = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    field = relationship("Field", back_populates="recommendations")

    def __repr__(self):
        return f"<Recommendation(id={self.id}, date={self.date}, irrigate={self.irrigate}, amount={self.amount_mm}mm)>"
