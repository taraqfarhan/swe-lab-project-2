from dataclasses import dataclass
from typing import Optional, List

@dataclass
class MenuItem:
    id: Optional[int]
    restaurant_id: int
    name: str
    description: str
    category: str
    price: float
    image_url: Optional[str] = None
    is_available: bool = True
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get('id'),
            restaurant_id=data.get('restaurant_id'),
            name=data.get('name'),
            description=data.get('description', ''),
            category=data.get('category', 'General'),
            price=float(data.get('price', 0.0)),
            image_url=data.get('image_url'),
            is_available=bool(data.get('is_available', 1)),
            created_at=data.get('created_at')
        )

@dataclass
class Restaurant:
    id: Optional[int]
    owner_id: int
    name: str
    description: str
    cuisine_type: str
    address: str
    phone: str
    image_url: Optional[str] = None
    rating: float = 4.5
    is_active: bool = True
    created_at: Optional[str] = None
    menu_items: Optional[List[MenuItem]] = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get('id'),
            owner_id=data.get('owner_id'),
            name=data.get('name'),
            description=data.get('description', ''),
            cuisine_type=data.get('cuisine_type', 'General'),
            address=data.get('address', ''),
            phone=data.get('phone', ''),
            image_url=data.get('image_url'),
            rating=float(data.get('rating', 4.5)),
            is_active=bool(data.get('is_active', 1)),
            created_at=data.get('created_at')
        )
