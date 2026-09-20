from src.services.order_service import OrderService

def test_create_order_success(app):
    with app.app_context():
        items = [
            {'menu_item_id': 1, 'quantity': 2}, # Margherita Classica (9.99 * 2 = 19.98)
            {'menu_item_id': 4, 'quantity': 1}  # Tiramisu (5.99)
        ]
        # Total subtotal: 25.97, Delivery: 2.99 -> Total: 28.96
        order, err = OrderService.create_order(
            customer_id=2,
            restaurant_id=1,
            items=items,
            delivery_address='Talaimari, Rajshahi',
            customer_phone='+8801711111111',
            payment_method='cash_on_delivery',
            notes='Please bring extra napkins'
        )
        assert err is None
        assert order is not None
        assert order.status == 'placed'
        assert order.total_amount == 28.96
        assert len(order.items) == 2

def test_create_order_with_promo_discount(app):
    with app.app_context():
        items = [{'menu_item_id': 1, 'quantity': 2}] # 19.98 subtotal
        # RUET10 promo gives 10% off (1.998 -> 2.00 discount) -> 19.98 - 2.00 + 2.99 = 20.97
        order, err = OrderService.create_order(
            customer_id=2,
            restaurant_id=1,
            items=items,
            delivery_address='RUET Campus',
            customer_phone='+8801711111111',
            promo_code='RUET10'
        )
        assert err is None
        assert order.discount_amount == 2.00
        assert order.total_amount == 20.97

def test_order_reviews(app):
    with app.app_context():
        # Order 1 in seed data is delivered to customer 2
        # Adding duplicate review should fail
        rev_id, err = OrderService.add_review(1, customer_id=2, rating=5, comment="Amazing!")
        assert err == "You have already reviewed this order."

        # Non-delivered order review should fail
        rev_id2, err2 = OrderService.add_review(5, customer_id=2, rating=5, comment="Too early!")
        assert err2 == "Only delivered orders can be reviewed."
