from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from ..db.base import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    image = Column(String)
    supplier_price = Column(Float)
    amazon_price = Column(Float)
    asin = Column(String, index=True)
    is_active = Column(Boolean, default=True)
