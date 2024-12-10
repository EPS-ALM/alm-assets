from sqlalchemy import Column, Integer, String, Float
from database import Base


# Modelo de exemplo
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
