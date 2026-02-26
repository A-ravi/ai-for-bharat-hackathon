from sqlalchemy import Column, Float, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class SavingsRecord(Base):
    __tablename__ = "savings_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    period_start = Column(Date, nullable=False, index=True)
    period_end = Column(Date, nullable=False, index=True)
    water_saved_liters = Column(Float, nullable=False)
    cost_saved_rupees = Column(Float, nullable=False)
    traditional_usage_liters = Column(Float, nullable=False)
    actual_usage_liters = Column(Float, nullable=False)
    calculated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    field = relationship("Field", back_populates="savings_records")

    def __repr__(self):
        return f"<SavingsRecord(id={self.id}, water_saved={self.water_saved_liters}L, cost_saved=₹{self.cost_saved_rupees})>"
