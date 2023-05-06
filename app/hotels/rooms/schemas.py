from typing import List, Optional

from pydantic import BaseModel


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: Optional[List[str]]
    quantity: int
    image_id: Optional[int]

    class Config:
        orm_mode = True


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    class Config:
        orm_mode = True
