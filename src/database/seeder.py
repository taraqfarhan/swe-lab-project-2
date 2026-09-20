import sqlite3
import datetime
from werkzeug.security import generate_password_hash
from src.config import Config

def seed_database(db_path=None):
    """Populate database with rich initial sample data for MVP demonstration."""
    path = db_path or Config.DATABASE_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Clear existing data and reset autoincrement sequences
    cursor.executescript("""
        DELETE FROM reviews;
        DELETE FROM order_items;
        DELETE FROM orders;
        DELETE FROM menu_items;
        DELETE FROM restaurants;
        DELETE FROM kanban_tasks;
        DELETE FROM kanban_wip_limits;
        DELETE FROM users;
        DELETE FROM sqlite_sequence WHERE name IN (
            'reviews', 'order_items', 'orders', 'menu_items', 'restaurants', 'kanban_tasks', 'users'
        );
    """)

    # 1. Seed Users (with explicit IDs to ensure exact foreign key mapping)
    default_password = generate_password_hash("password123")
    users = [
        (1, 'admin', 'admin@ruetfood.com', default_password, 'admin', 'System Administrator', '+8801700000001', 'CSE Building, RUET, Rajshahi'),
        (2, 'john_doe', 'john@example.com', default_password, 'customer', 'John Doe', '+8801711111111', 'Talaimari, Kazla, Rajshahi'),
        (3, 'sarah_connor', 'sarah@example.com', default_password, 'customer', 'Sarah Connor', '+8801722222222', 'Padma Residential Area, Rajshahi'),
        (4, 'chef_mario', 'mario@bellaitalia.com', default_password, 'restaurant_owner', 'Chef Mario Rossi', '+8801733333333', 'Shaheb Bazar, Rajshahi'),
        (5, 'chef_kenji', 'kenji@tokyoexpress.com', default_password, 'restaurant_owner', 'Chef Kenji Sato', '+8801744444444', 'New Market, Rajshahi'),
        (6, 'chef_alex', 'alex@burgercraze.com', default_password, 'restaurant_owner', 'Alex Johnson', '+8801755555555', 'Vodra Mor, Rajshahi'),
        (7, 'rider_alex', 'rider.alex@ruetfood.com', default_password, 'rider', 'Alex Delivery Rider', '+8801766666666', 'Station Road, Rajshahi'),
        (8, 'rider_rahim', 'rider.rahim@ruetfood.com', default_password, 'rider', 'Rahim Rider', '+8801777777777', 'Shiroil, Rajshahi')
    ]
    cursor.executemany("""
        INSERT INTO users (id, username, email, password_hash, role, full_name, phone, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, users)

    # 2. Seed Restaurants (with explicit IDs)
    restaurants = [
        (1, 4, 'Bella Italia', 'Authentic stone-oven artisanal Italian pizzas, handmade pastas, and classic tiramisu.', 'Italian', 'Shaheb Bazar, Rajshahi', '+8801733333333', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&auto=format&fit=crop', 4.8, 1),
        (2, 5, 'Tokyo Express Sushi & Ramen', 'Traditional Japanese hand-rolled sushi, nigiri, and rich authentic tonkotsu ramen.', 'Japanese', 'New Market, Rajshahi', '+8801744444444', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800&auto=format&fit=crop', 4.9, 1),
        (3, 6, 'Burger Craze & Grill', 'Juicy gourmet smashed beef burgers, crispy buttermilk fried chicken, and loaded fries.', 'American / Fast Food', 'Vodra Mor, Rajshahi', '+8801755555555', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&auto=format&fit=crop', 4.7, 1)
    ]
    cursor.executemany("""
        INSERT INTO restaurants (id, owner_id, name, description, cuisine_type, address, phone, image_url, rating, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, restaurants)

    # 3. Seed Menu Items (with explicit IDs)
    menu_items = [
        # Bella Italia (rest_id=1)
        (1, 1, 'Margherita Classica', 'Fresh mozzarella, San Marzano tomato sauce, fresh basil, extra virgin olive oil', 'Pizza', 9.99, 'https://images.unsplash.com/photo-1604382355076-af4b0eb60143?w=600&auto=format&fit=crop', 1),
        (2, 1, 'Quattro Formaggi', 'Blend of mozzarella, gorgonzola, parmesan, and creamy fontina cheese', 'Pizza', 12.99, 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&auto=format&fit=crop', 1),
        (3, 1, 'Fettuccine Alfredo', 'Fresh fettuccine tossed in rich parmesan cream sauce with wild herbs', 'Pasta', 11.50, 'https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=600&auto=format&fit=crop', 1),
        (4, 1, 'Tiramisu Tradizionale', 'Espresso-soaked ladyfingers layered with mascarpone cream and cocoa powder', 'Dessert', 5.99, 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600&auto=format&fit=crop', 1),
        
        # Tokyo Express (rest_id=2)
        (5, 2, 'Salmon Nigiri Platter (8 pcs)', 'Fresh Norwegian salmon lightly torched with sweet unagi glaze', 'Sushi', 14.50, 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=600&auto=format&fit=crop', 1),
        (6, 2, 'Dragon Roll (8 pcs)', 'Tempura prawn, sliced avocado, cucumber, unagi eel sauce, spicy mayo', 'Sushi', 15.99, 'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=600&auto=format&fit=crop', 1),
        (7, 2, 'Tonkotsu Ramen Special', '24-hour pork bone broth, tender chashu pork, ajitsuke tamago, nori, scallions', 'Ramen', 13.50, 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600&auto=format&fit=crop', 1),
        (8, 2, 'Matcha Green Tea Gelato', 'Ceremonial grade matcha ice cream topped with sweet red bean paste', 'Dessert', 4.99, 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=600&auto=format&fit=crop', 1),

        # Burger Craze (rest_id=3)
        (9, 3, 'Double Smash Cheeseburger', 'Two 100% Angus beef patties, aged cheddar, caramelized onions, secret sauce, brioche bun', 'Burgers', 10.99, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&auto=format&fit=crop', 1),
        (10, 3, 'Crispy Hot Honey Fried Chicken Burger', 'Crispy buttermilk chicken breast tossed in hot chili honey with tangy coleslaw', 'Burgers', 11.49, 'https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?w=600&auto=format&fit=crop', 1),
        (11, 3, 'Truffle Parmesan Loaded Fries', 'Hand-cut golden fries drizzled with white truffle oil and freshly shaved parmesan', 'Sides', 6.50, 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&auto=format&fit=crop', 1),
        (12, 3, 'Classic Vanilla Bean Milkshake', 'Creamy whole milk blended with Madagascar vanilla ice cream and whipped cream', 'Beverages', 4.50, 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&auto=format&fit=crop', 1)
    ]
    cursor.executemany("""
        INSERT INTO menu_items (id, restaurant_id, name, description, category, price, image_url, is_available)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, menu_items)

    # 4. Seed Kanban WIP Limits
    wip_limits = [
        ('placed', 15),
        ('preparing', 5),
        ('ready', 4),
        ('in_transit', 6),
        ('delivered', 100)
    ]
    cursor.executemany("""
        INSERT INTO kanban_wip_limits (column_name, wip_limit)
        VALUES (?, ?)
    """, wip_limits)

    # 5. Seed Initial Orders (with explicit IDs)
    def fmt(dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else None

    now = datetime.datetime.now()
    orders = [
        (1, 'ORD-2026-1001', 2, 1, 7, 'delivered', 24.48, 2.00, 2.99, 'Talaimari, Kazla, Rajshahi', '+8801711111111', 'card', 'completed', 'Ring doorbell please', 
         fmt(now - datetime.timedelta(hours=2)), fmt(now - datetime.timedelta(minutes=100)), fmt(now - datetime.timedelta(minutes=70)), fmt(now - datetime.timedelta(minutes=60)), fmt(now - datetime.timedelta(minutes=30))),
        (2, 'ORD-2026-1002', 3, 2, 7, 'in_transit', 33.99, 0.00, 2.99, 'Padma Residential Area, Rajshahi', '+8801722222222', 'digital_wallet', 'completed', 'Leave at main reception', 
         fmt(now - datetime.timedelta(minutes=45)), fmt(now - datetime.timedelta(minutes=35)), fmt(now - datetime.timedelta(minutes=20)), fmt(now - datetime.timedelta(minutes=10)), None),
        (3, 'ORD-2026-1003', 2, 3, 8, 'ready', 22.48, 0.00, 2.99, 'Talaimari, Kazla, Rajshahi', '+8801711111111', 'cash_on_delivery', 'pending', 'Extra ketchup please', 
         fmt(now - datetime.timedelta(minutes=30)), fmt(now - datetime.timedelta(minutes=25)), fmt(now - datetime.timedelta(minutes=5)), None, None),
        (4, 'ORD-2026-1004', 3, 1, None, 'preparing', 18.98, 0.00, 2.99, 'Padma Residential Area, Rajshahi', '+8801722222222', 'card', 'completed', 'Hot and spicy', 
         fmt(now - datetime.timedelta(minutes=15)), fmt(now - datetime.timedelta(minutes=10)), None, None, None),
        (5, 'ORD-2026-1005', 2, 2, None, 'placed', 17.99, 0.00, 2.99, 'Talaimari, Kazla, Rajshahi', '+8801711111111', 'cash_on_delivery', 'pending', 'Fast delivery please', 
         fmt(now - datetime.timedelta(minutes=5)), None, None, None, None)
    ]
    cursor.executemany("""
        INSERT INTO orders (id, order_number, customer_id, restaurant_id, rider_id, status, total_amount, discount_amount, delivery_fee, delivery_address, customer_phone, payment_method, payment_status, notes, placed_at, preparing_at, ready_at, dispatched_at, delivered_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, orders)

    # 6. Seed Order Items (with explicit IDs)
    order_items = [
        (1, 1, 1, 'Margherita Classica', 9.99, 1, 9.99),
        (2, 1, 4, 'Tiramisu Tradizionale', 5.99, 2, 11.98),
        (3, 2, 5, 'Salmon Nigiri Platter (8 pcs)', 14.50, 1, 14.50),
        (4, 2, 7, 'Tonkotsu Ramen Special', 13.50, 1, 13.50),
        (5, 3, 9, 'Double Smash Cheeseburger', 10.99, 1, 10.99),
        (6, 3, 11, 'Truffle Parmesan Loaded Fries', 6.50, 1, 6.50),
        (7, 4, 2, 'Quattro Formaggi', 12.99, 1, 12.99),
        (8, 5, 6, 'Dragon Roll (8 pcs)', 15.99, 1, 15.99)
    ]
    cursor.executemany("""
        INSERT INTO order_items (id, order_id, menu_item_id, item_name, unit_price, quantity, subtotal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, order_items)

    # 7. Seed Review
    cursor.execute("""
        INSERT INTO reviews (id, order_id, customer_id, restaurant_id, rating, comment)
        VALUES (1, 1, 2, 1, 5, 'Delicious wood-fired pizza and prompt delivery! Will definitely order again.')
    """)

    # 8. Seed Kanban Software Engineering Development Tasks
    kanban_tasks = [
        (1, 'FR1: User Authentication & Role Based Access Control', 'Implement secure registration, bcrypt password hashing, and role checks for Customer, Owner, Rider, Admin', 'Engineering', 'high', 'done', 'Member 1', 3.5),
        (2, 'FR2 & FR3: Restaurant Catalog & Menu Item Management', 'Implement restaurant listings, categories, and owner menu CRUD operations with instant UI preview', 'Engineering', 'high', 'done', 'Member 2', 4.0),
        (3, 'FR4 & FR5: Shopping Cart & Real-Time Order Lifecycle', 'Cart state management, checkout transaction, and order status transitions', 'Engineering', 'high', 'done', 'Member 3', 5.0),
        (4, 'FR6 & FR9: Interactive Kanban Order Management Board', 'Live visual Kanban pipeline with configurable WIP Limits, status drags, and lead-time tracking', 'Engineering', 'critical', 'done', 'Member 1', 4.5),
        (5, 'FR7: Payment Simulation & Checkout Workflow', 'Implement Cash on Delivery, Credit Card, and Digital Wallet checkout flows', 'Engineering', 'medium', 'done', 'Member 2', 2.0),
        (6, 'FR8 & FR10: Reviews, Ratings & Customer Order History', 'Allow customers to review delivered orders and track historical purchases', 'Engineering', 'medium', 'done', 'Member 3', 2.5),
        (7, 'Phase 1: Comprehensive Requirement Analysis & Use Cases', 'Document 12+ Functional Requirements, 10+ Non-Functional Requirements, and 5 detailed User Stories', 'Documentation', 'high', 'done', 'Member 1', 3.0),
        (8, 'Phase 2: Process Model Selection & Kanban Justification', 'Draft in-depth justification of Kanban with comparative analysis against Waterfall, Scrum, Spiral', 'Documentation', 'high', 'done', 'Member 2', 3.0),
        (9, 'Automated Testing Suite (Unit & Integration Tests)', 'Write automated pytest suites covering Auth, Menu CRUD, Cart, Orders, and Kanban state machine', 'Testing', 'high', 'done', 'Member 3', 3.5),
        (10, 'Continuous Flow Optimization & Lead Time Analytics', 'Monitor order lead times and kitchen queue metrics to dynamically alert WIP limit saturation', 'Feature', 'low', 'in_progress', 'Member 1', 1.5),
        (11, 'Real-Time Geolocation GPS Rider Tracker Simulator', 'Simulate rider delivery coordinates moving along delivery path on interactive map', 'Feature', 'low', 'backlog', 'Unassigned', 0.0)
    ]
    cursor.executemany("""
        INSERT INTO kanban_tasks (id, title, description, category, priority, column_name, assignee, lead_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, kanban_tasks)

    conn.commit()
    conn.close()
    print(f"Database seeded successfully at {path}")

if __name__ == '__main__':
    seed_database()
