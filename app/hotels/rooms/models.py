from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Rooms(Base):
    """Модель комнат"""
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(ForeignKey('hotels.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    hotel = relationship('Hotels', back_populates='rooms')
    booking = relationship('Bookings', back_populates='room')

    def __str__(self):
        return f'Номер {self.name}'
