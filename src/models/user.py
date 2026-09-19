from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    role: str  # 'customer', 'restaurant_owner', 'rider', 'admin'
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            role=data.get('role'),
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            address=data.get('address'),
            created_at=data.get('created_at')
        )

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def is_restaurant_owner(self) -> bool:
        return self.role == 'restaurant_owner'

    def is_rider(self) -> bool:
        return self.role == 'rider'

    def is_customer(self) -> bool:
        return self.role == 'customer'
