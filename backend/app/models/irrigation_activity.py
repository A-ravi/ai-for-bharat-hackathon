from sqlalchemy import Column, String, Float, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class IrrigationActivity(Base):
    __tablename__ = "irrigation_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    amount_mm = Column(Float, nullable=False)
    method = Column(String(20), nullable=False)
    farmer_reported = Column(Boolean, nullable=False, default=False)
    cost_rupees = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    field = relationship("Field", back_populates="irrigation_activities")

    def __repr__(self):
        return f"<IrrigationActivity(id={self.id}, date={self.date}, amount={self.amount_mm}mm, cost=₹{self.cost_rupees})>"
