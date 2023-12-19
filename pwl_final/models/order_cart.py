from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class OrderCart(Base):
    __tablename__ = 'order_cart'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    note = Column(String, nullable=True)