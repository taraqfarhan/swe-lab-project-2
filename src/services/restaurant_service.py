from src.database.db import query_db, execute_db
from src.models.restaurant import Restaurant, MenuItem

class RestaurantService:
    @staticmethod
    def get_all_restaurants(cuisine_filter=None, search_query=None):
        """Fetch all active restaurants with optional cuisine filter or search query."""
        sql = "SELECT * FROM restaurants WHERE is_active = 1"
        params = []

        if cuisine_filter and cuisine_filter != 'all':
            sql += " AND LOWER(cuisine_type) LIKE ?"
            params.append(f"%{cuisine_filter.lower()}%")

        if search_query:
            sql += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)"
            params.extend([f"%{search_query.lower()}%", f"%{search_query.lower()}%"])

        sql += " ORDER BY rating DESC, name ASC"
        rows = query_db(sql, params)
        return [Restaurant.from_dict(r) for r in rows]

    @staticmethod
    def get_restaurant_by_id(restaurant_id: int):
        row = query_db("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,), one=True)
        if not row:
            return None
        restaurant = Restaurant.from_dict(row)
        restaurant.menu_items = RestaurantService.get_menu_items(restaurant_id)
        return restaurant

    @staticmethod
    def get_restaurant_by_owner_id(owner_id: int):
        row = query_db("SELECT * FROM restaurants WHERE owner_id = ?", (owner_id,), one=True)
        if not row:
            return None
        restaurant = Restaurant.from_dict(row)
        restaurant.menu_items = RestaurantService.get_menu_items(restaurant.id)
        return restaurant

    @staticmethod
    def create_restaurant(owner_id: int, name: str, description: str, cuisine_type: str, address: str, phone: str, image_url: str = None):
        rest_id = execute_db(
            """INSERT INTO restaurants (owner_id, name, description, cuisine_type, address, phone, image_url)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (owner_id, name.strip(), description.strip(), cuisine_type.strip(), address.strip(), phone.strip(), image_url)
        )
        return RestaurantService.get_restaurant_by_id(rest_id)

    @staticmethod
    def update_restaurant(restaurant_id: int, name: str, description: str, cuisine_type: str, address: str, phone: str, image_url: str = None):
        execute_db(
            """UPDATE restaurants
               SET name = ?, description = ?, cuisine_type = ?, address = ?, phone = ?, image_url = COALESCE(?, image_url)
               WHERE id = ?""",
            (name.strip(), description.strip(), cuisine_type.strip(), address.strip(), phone.strip(), image_url, restaurant_id)
        )
        return RestaurantService.get_restaurant_by_id(restaurant_id)

    @staticmethod
    def get_menu_items(restaurant_id: int, available_only=False):
        sql = "SELECT * FROM menu_items WHERE restaurant_id = ?"
        params = [restaurant_id]
        if available_only:
            sql += " AND is_available = 1"
        sql += " ORDER BY category ASC, price ASC"
        rows = query_db(sql, params)
        return [MenuItem.from_dict(r) for r in rows]

    @staticmethod
    def get_menu_item_by_id(item_id: int):
        row = query_db("SELECT * FROM menu_items WHERE id = ?", (item_id,), one=True)
        return MenuItem.from_dict(row) if row else None

    @staticmethod
    def add_menu_item(restaurant_id: int, name: str, description: str, category: str, price: float, image_url: str = None, is_available: bool = True):
        item_id = execute_db(
            """INSERT INTO menu_items (restaurant_id, name, description, category, price, image_url, is_available)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (restaurant_id, name.strip(), description.strip(), category.strip(), float(price), image_url, 1 if is_available else 0)
        )
        return RestaurantService.get_menu_item_by_id(item_id)

    @staticmethod
    def update_menu_item(item_id: int, name: str, description: str, category: str, price: float, image_url: str = None, is_available: bool = True):
        execute_db(
            """UPDATE menu_items
               SET name = ?, description = ?, category = ?, price = ?, image_url = COALESCE(?, image_url), is_available = ?
               WHERE id = ?""",
            (name.strip(), description.strip(), category.strip(), float(price), image_url, 1 if is_available else 0, item_id)
        )
        return RestaurantService.get_menu_item_by_id(item_id)

    @staticmethod
    def delete_menu_item(item_id: int):
        execute_db("DELETE FROM menu_items WHERE id = ?", (item_id,))
        return True

    @staticmethod
    def toggle_item_availability(item_id: int):
        item = RestaurantService.get_menu_item_by_id(item_id)
        if not item:
            return None
        new_status = 0 if item.is_available else 1
        execute_db("UPDATE menu_items SET is_available = ? WHERE id = ?", (new_status, item_id))
        return RestaurantService.get_menu_item_by_id(item_id)
