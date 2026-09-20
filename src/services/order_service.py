import datetime
import random
import string
from src.database.db import query_db, execute_db
from src.models.order import Order, OrderItem, ORDER_STATUS_FLOW

class OrderService:
    @staticmethod
    def generate_order_number():
        chars = ''.join(random.choices(string.digits, k=4))
        return f"ORD-{datetime.datetime.now().strftime('%Y')}-{chars}"

    @staticmethod
    def create_order(customer_id: int, restaurant_id: int, items: list, delivery_address: str, 
                     customer_phone: str, payment_method: str = 'cash_on_delivery', 
                     notes: str = '', promo_code: str = None):
        """Create a new order with items, calculate totals, and record initial 'placed' state."""
        if not items:
            return None, "Order must contain at least one item."

        # Calculate subtotal
        subtotal = 0.0
        validated_items = []
        for it in items:
            item_id = it.get('menu_item_id')
            qty = int(it.get('quantity', 1))
            if qty <= 0:
                continue
            item_row = query_db("SELECT * FROM menu_items WHERE id = ? AND restaurant_id = ?", (item_id, restaurant_id), one=True)
            if not item_row:
                return None, f"Item ID {item_id} is not available at this restaurant."
            if not item_row['is_available']:
                return None, f"Item '{item_row['name']}' is currently sold out."
            
            item_price = float(item_row['price'])
            item_total = round(item_price * qty, 2)
            subtotal += item_total
            validated_items.append({
                'menu_item_id': item_id,
                'name': item_row['name'],
                'price': item_price,
                'quantity': qty,
                'subtotal': item_total
            })

        if not validated_items:
            return None, "No valid items selected for order."

        delivery_fee = 2.99
        discount_amount = 0.0
        
        # Simple promo discount support (e.g. RUET10 gives 10% discount, KANBAN5 gives $5 off)
        if promo_code:
            code = promo_code.strip().upper()
            if code == 'RUET10':
                discount_amount = round(subtotal * 0.10, 2)
            elif code == 'KANBAN5':
                discount_amount = min(5.00, subtotal)

        total_amount = round(max(0.0, subtotal - discount_amount + delivery_fee), 2)
        order_number = OrderService.generate_order_number()
        payment_status = 'completed' if payment_method in ('card', 'digital_wallet') else 'pending'

        order_id = execute_db(
            """INSERT INTO orders (order_number, customer_id, restaurant_id, status, total_amount, 
                                  discount_amount, delivery_fee, delivery_address, customer_phone, 
                                  payment_method, payment_status, notes, placed_at)
               VALUES (?, ?, ?, 'placed', ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (order_number, customer_id, restaurant_id, total_amount, discount_amount, delivery_fee, 
             delivery_address.strip(), customer_phone.strip(), payment_method, payment_status, notes.strip())
        )

        for vit in validated_items:
            execute_db(
                """INSERT INTO order_items (order_id, menu_item_id, item_name, unit_price, quantity, subtotal)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (order_id, vit['menu_item_id'], vit['name'], vit['price'], vit['quantity'], vit['subtotal'])
            )

        return OrderService.get_order_by_id(order_id), None

    @staticmethod
    def get_order_by_id(order_id: int):
        sql = """
            SELECT o.*, 
                   r.name as restaurant_name,
                   c.full_name as customer_name,
                   rd.full_name as rider_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            JOIN users c ON o.customer_id = c.id
            LEFT JOIN users rd ON o.rider_id = rd.id
            WHERE o.id = ?
        """
        row = query_db(sql, (order_id,), one=True)
        if not row:
            return None
        
        order = Order.from_dict(row)
        item_rows = query_db("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
        order.items = [OrderItem.from_dict(it) for it in item_rows]
        return order

    @staticmethod
    def get_order_by_number(order_number: str):
        sql = """
            SELECT o.*, 
                   r.name as restaurant_name,
                   c.full_name as customer_name,
                   rd.full_name as rider_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            JOIN users c ON o.customer_id = c.id
            LEFT JOIN users rd ON o.rider_id = rd.id
            WHERE o.order_number = ?
        """
        row = query_db(sql, (order_number.strip(),), one=True)
        if not row:
            return None
        
        order = Order.from_dict(row)
        item_rows = query_db("SELECT * FROM order_items WHERE order_id = ?", (order.id,))
        order.items = [OrderItem.from_dict(it) for it in item_rows]
        return order

    @staticmethod
    def get_orders_by_customer(customer_id: int):
        sql = """
            SELECT o.*, r.name as restaurant_name, rd.full_name as rider_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            LEFT JOIN users rd ON o.rider_id = rd.id
            WHERE o.customer_id = ?
            ORDER BY o.id DESC
        """
        rows = query_db(sql, (customer_id,))
        orders = []
        for r in rows:
            ord_obj = Order.from_dict(r)
            item_rows = query_db("SELECT * FROM order_items WHERE order_id = ?", (ord_obj.id,))
            ord_obj.items = [OrderItem.from_dict(it) for it in item_rows]
            orders.append(ord_obj)
        return orders

    @staticmethod
    def get_orders_by_restaurant(restaurant_id: int):
        sql = """
            SELECT o.*, r.name as restaurant_name, c.full_name as customer_name, rd.full_name as rider_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            JOIN users c ON o.customer_id = c.id
            LEFT JOIN users rd ON o.rider_id = rd.id
            WHERE o.restaurant_id = ?
            ORDER BY o.id DESC
        """
        rows = query_db(sql, (restaurant_id,))
        orders = []
        for r in rows:
            ord_obj = Order.from_dict(r)
            item_rows = query_db("SELECT * FROM order_items WHERE order_id = ?", (ord_obj.id,))
            ord_obj.items = [OrderItem.from_dict(it) for it in item_rows]
            orders.append(ord_obj)
        return orders

    @staticmethod
    def get_available_delivery_orders():
        """Orders ready for pickup that have not been assigned to a rider, or are ready."""
        sql = """
            SELECT o.*, r.name as restaurant_name, r.address as restaurant_address, c.full_name as customer_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            JOIN users c ON o.customer_id = c.id
            WHERE o.status = 'ready' AND o.rider_id IS NULL
            ORDER BY o.id ASC
        """
        rows = query_db(sql)
        orders = []
        for r in rows:
            ord_obj = Order.from_dict(r)
            item_rows = query_db("SELECT * FROM order_items WHERE order_id = ?", (ord_obj.id,))
            ord_obj.items = [OrderItem.from_dict(it) for it in item_rows]
            orders.append(ord_obj)
        return orders

    @staticmethod
    def get_orders_by_rider(rider_id: int):
        sql = """
            SELECT o.*, r.name as restaurant_name, r.address as restaurant_address, c.full_name as customer_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            JOIN users c ON o.customer_id = c.id
            WHERE o.rider_id = ?
            ORDER BY o.id DESC
        """
        rows = query_db(sql, (rider_id,))
        orders = []
        for r in rows:
            ord_obj = Order.from_dict(r)
            item_rows = query_db("SELECT * FROM order_items WHERE order_id = ?", (ord_obj.id,))
            ord_obj.items = [OrderItem.from_dict(it) for it in item_rows]
            orders.append(ord_obj)
        return orders

    @staticmethod
    def get_all_orders():
        sql = """
            SELECT o.*, r.name as restaurant_name, c.full_name as customer_name, rd.full_name as rider_name
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.id
            JOIN users c ON o.customer_id = c.id
            LEFT JOIN users rd ON o.rider_id = rd.id
            ORDER BY o.id DESC
        """
        rows = query_db(sql)
        orders = []
        for r in rows:
            ord_obj = Order.from_dict(r)
            item_rows = query_db("SELECT * FROM order_items WHERE order_id = ?", (ord_obj.id,))
            ord_obj.items = [OrderItem.from_dict(it) for it in item_rows]
            orders.append(ord_obj)
        return orders

    @staticmethod
    def update_order_status(order_id: int, target_status: str, actor_role: str = 'admin'):
        """Transition order status through the Kanban workflow pipeline."""
        order = OrderService.get_order_by_id(order_id)
        if not order:
            return None, "Order not found."

        if target_status == order.status:
            return order, None

        if not order.can_transition_to(target_status):
            return None, f"Invalid status transition from '{order.status}' to '{target_status}'."

        timestamp_column = None
        if target_status == 'preparing':
            timestamp_column = "preparing_at = CURRENT_TIMESTAMP"
        elif target_status == 'ready':
            timestamp_column = "ready_at = CURRENT_TIMESTAMP"
        elif target_status == 'in_transit':
            timestamp_column = "dispatched_at = CURRENT_TIMESTAMP"
        elif target_status == 'delivered':
            timestamp_column = "delivered_at = CURRENT_TIMESTAMP, payment_status = 'completed'"
        
        sql = f"UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP"
        if timestamp_column:
            sql += f", {timestamp_column}"
        sql += " WHERE id = ?"

        execute_db(sql, (target_status, order_id))
        return OrderService.get_order_by_id(order_id), None

    @staticmethod
    def assign_rider(order_id: int, rider_id: int):
        order = OrderService.get_order_by_id(order_id)
        if not order:
            return None, "Order not found."
        
        execute_db("UPDATE orders SET rider_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (rider_id, order_id))
        return OrderService.get_order_by_id(order_id), None

    @staticmethod
    def add_review(order_id: int, customer_id: int, rating: int, comment: str):
        order = OrderService.get_order_by_id(order_id)
        if not order:
            return None, "Order not found."
        if order.customer_id != customer_id:
            return None, "You can only review your own orders."
        if order.status != 'delivered':
            return None, "Only delivered orders can be reviewed."

        existing = query_db("SELECT id FROM reviews WHERE order_id = ?", (order_id,), one=True)
        if existing:
            return None, "You have already reviewed this order."

        rating = max(1, min(5, int(rating)))
        review_id = execute_db(
            "INSERT INTO reviews (order_id, customer_id, restaurant_id, rating, comment) VALUES (?, ?, ?, ?, ?)",
            (order_id, customer_id, order.restaurant_id, rating, comment.strip())
        )
        
        # Update restaurant average rating
        avg_row = query_db("SELECT AVG(rating) as avg_rating FROM reviews WHERE restaurant_id = ?", (order.restaurant_id,), one=True)
        if avg_row and avg_row['avg_rating']:
            execute_db("UPDATE restaurants SET rating = ? WHERE id = ?", (round(avg_row['avg_rating'], 1), order.restaurant_id))

        return review_id, None
