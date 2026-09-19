from dataclasses import dataclass
from typing import Optional, List, Dict

ORDER_STATUS_FLOW = {
    'placed': ['preparing', 'cancelled'],
    'preparing': ['ready', 'cancelled'],
    'ready': ['in_transit', 'cancelled'],
    'in_transit': ['delivered', 'cancelled'],
    'delivered': [],
    'cancelled': []
}

ORDER_STATUS_LABELS = {
    'placed': 'Order Placed (Backlog)',
    'preparing': 'Kitchen Preparing (WIP)',
    'ready': 'Ready for Pickup',
    'in_transit': 'Out for Delivery (In Transit)',
    'delivered': 'Delivered (Done)',
    'cancelled': 'Cancelled'
}

@dataclass
class OrderItem:
    id: Optional[int]
    order_id: int
    menu_item_id: int
    item_name: str
    unit_price: float
    quantity: int
    subtotal: float

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get('id'),
            order_id=data.get('order_id'),
            menu_item_id=data.get('menu_item_id'),
            item_name=data.get('item_name'),
            unit_price=float(data.get('unit_price', 0.0)),
            quantity=int(data.get('quantity', 1)),
            subtotal=float(data.get('subtotal', 0.0))
        )

@dataclass
class Order:
    id: Optional[int]
    order_number: str
    customer_id: int
    restaurant_id: int
    rider_id: Optional[int]
    status: str
    total_amount: float
    discount_amount: float
    delivery_fee: float
    delivery_address: str
    customer_phone: str
    payment_method: str
    payment_status: str
    notes: Optional[str] = None
    placed_at: Optional[str] = None
    preparing_at: Optional[str] = None
    ready_at: Optional[str] = None
    dispatched_at: Optional[str] = None
    delivered_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    items: Optional[List[OrderItem]] = None
    restaurant_name: Optional[str] = None
    customer_name: Optional[str] = None
    rider_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get('id'),
            order_number=data.get('order_number'),
            customer_id=data.get('customer_id'),
            restaurant_id=data.get('restaurant_id'),
            rider_id=data.get('rider_id'),
            status=data.get('status', 'placed'),
            total_amount=float(data.get('total_amount', 0.0)),
            discount_amount=float(data.get('discount_amount', 0.0)),
            delivery_fee=float(data.get('delivery_fee', 2.99)),
            delivery_address=data.get('delivery_address', ''),
            customer_phone=data.get('customer_phone', ''),
            payment_method=data.get('payment_method', 'cash_on_delivery'),
            payment_status=data.get('payment_status', 'pending'),
            notes=data.get('notes'),
            placed_at=data.get('placed_at'),
            preparing_at=data.get('preparing_at'),
            ready_at=data.get('ready_at'),
            dispatched_at=data.get('dispatched_at'),
            delivered_at=data.get('delivered_at'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            restaurant_name=data.get('restaurant_name'),
            customer_name=data.get('customer_name'),
            rider_name=data.get('rider_name')
        )

    def can_transition_to(self, target_status: str) -> bool:
        return target_status in ORDER_STATUS_FLOW.get(self.status, [])

    @property
    def status_label(self) -> str:
        return ORDER_STATUS_LABELS.get(self.status, self.status.capitalize())
