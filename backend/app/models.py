from sqlalchemy import Column, BigInteger, Text, Numeric, Boolean, TIMESTAMP, func, String, Integer, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sku = Column(Text, nullable=False)
    sku_lower = Column(Text, nullable=False)
    name = Column(Text)
    description = Column(Text)
    price = Column(Numeric(12,2))
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint('sku_lower', name='uq_products_sku_lower'),)

class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False)
    event_type = Column(Text, nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class ImportJob(Base):
    __tablename__ = "import_jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(Text)
    total_rows = Column(BigInteger, default=0)
    processed_rows = Column(BigInteger, default=0)
    status = Column(Text, default='PENDING')
    errors = Column(JSON, default=[])
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
