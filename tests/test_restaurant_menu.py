from src.services.restaurant_service import RestaurantService

def test_get_all_restaurants(app):
    with app.app_context():
        restaurants = RestaurantService.get_all_restaurants()
        assert len(restaurants) >= 3
        names = [r.name for r in restaurants]
        assert 'Bella Italia' in names
        assert 'Tokyo Express Sushi & Ramen' in names

def test_restaurant_search_and_filter(app):
    with app.app_context():
        italian_rests = RestaurantService.get_all_restaurants(cuisine_filter='Italian')
        assert len(italian_rests) == 1
        assert italian_rests[0].name == 'Bella Italia'

        searched = RestaurantService.get_all_restaurants(search_query='burger')
        assert len(searched) == 1
        assert 'Burger' in searched[0].name

def test_menu_item_crud_and_availability(app):
    with app.app_context():
        # Add item
        item = RestaurantService.add_menu_item(
            restaurant_id=1,
            name='Test Garlic Bread',
            description='Crispy toasted bread with garlic butter',
            category='Appetizer',
            price=4.50,
            image_url='https://example.com/bread.jpg',
            is_available=True
        )
        assert item.id is not None
        assert item.name == 'Test Garlic Bread'

        # Toggle availability
        toggled = RestaurantService.toggle_item_availability(item.id)
        assert toggled.is_available is False

        # Update item
        updated = RestaurantService.update_menu_item(
            item_id=item.id,
            name='Test Cheesy Garlic Bread',
            description='With melted mozzarella',
            category='Appetizer',
            price=5.50,
            image_url=None,
            is_available=True
        )
        assert updated.name == 'Test Cheesy Garlic Bread'
        assert updated.price == 5.50

        # Delete item
        deleted = RestaurantService.delete_menu_item(item.id)
        assert deleted is True
        assert RestaurantService.get_menu_item_by_id(item.id) is None
