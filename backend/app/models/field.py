from sqlalchemy import Column, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Field(Base):
    __tablename__ = "fields"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_type = Column(String(50), nullable=False)
    field_size_acres = Column(Float, nullable=False)
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    pincode = Column(String(10), nullable=False)
    irrigation_method = Column(String(20), nullable=False)  # drip, sprinkler, flood
    planting_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    farmer = relationship("Farmer", back_populates="fields")
    recommendations = relationship("Recommendation", back_populates="field", cascade="all, delete-orphan")
    irrigation_activities = relationship("IrrigationActivity", back_populates="field", cascade="all, delete-orphan")
    savings_records = relationship("SavingsRecord", back_populates="field", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Field(id={self.id}, crop={self.crop_type}, size={self.field_size_acres} acres)>"
