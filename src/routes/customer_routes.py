from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from src.services.restaurant_service import RestaurantService
from src.services.order_service import OrderService
from src.services.auth_service import AuthService
from src.routes.auth_routes import login_required

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/')
def index():
    cuisine = request.args.get('cuisine', 'all')
    search = request.args.get('q', '').strip()
    restaurants = RestaurantService.get_all_restaurants(cuisine_filter=cuisine, search_query=search)
    return render_template('customer/restaurants.html', restaurants=restaurants, selected_cuisine=cuisine, search_query=search)

@customer_bp.route('/restaurants/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurant = RestaurantService.get_restaurant_by_id(restaurant_id)
    if not restaurant:
        flash('Restaurant not found.', 'danger')
        return redirect(url_for('customer.index'))
    
    # Group menu items by category
    categories = {}
    for item in restaurant.menu_items:
        categories.setdefault(item.category, []).append(item)
        
    return render_template('customer/menu.html', restaurant=restaurant, categories=categories)

@customer_bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    subtotal = 0.0
    restaurant_id = session.get('cart_restaurant_id')
    restaurant = RestaurantService.get_restaurant_by_id(restaurant_id) if restaurant_id else None

    for item_id_str, qty in cart.items():
        item = RestaurantService.get_menu_item_by_id(int(item_id_str))
        if item:
            item_subtotal = round(item.price * qty, 2)
            subtotal += item_subtotal
            cart_items.append({
                'item': item,
                'quantity': qty,
                'subtotal': item_subtotal
            })

    delivery_fee = 2.99 if cart_items else 0.0
    total = round(subtotal + delivery_fee, 2)
    user = AuthService.get_user_by_id(session['user_id']) if 'user_id' in session else None

    return render_template('customer/cart.html', cart_items=cart_items, subtotal=subtotal, 
                           delivery_fee=delivery_fee, total=total, restaurant=restaurant, user=user)

@customer_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    item_id = int(request.form.get('item_id'))
    restaurant_id = int(request.form.get('restaurant_id'))
    quantity = int(request.form.get('quantity', 1))

    item = RestaurantService.get_menu_item_by_id(item_id)
    if not item or not item.is_available:
        flash('This item is currently unavailable.', 'danger')
        return redirect(request.referrer or url_for('customer.index'))

    # Check if cart already has items from another restaurant
    current_cart_rest = session.get('cart_restaurant_id')
    if current_cart_rest and current_cart_rest != restaurant_id:
        # Reset cart for new restaurant
        session['cart'] = {}
        session['cart_restaurant_id'] = restaurant_id
        flash('Cart was reset to add items from the new restaurant.', 'info')
    else:
        session['cart_restaurant_id'] = restaurant_id

    cart = session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + quantity
    session['cart'] = cart
    session.modified = True

    flash(f'Added {item.name} ({quantity}x) to your cart.', 'success')
    return redirect(request.referrer or url_for('customer.restaurant_menu', restaurant_id=restaurant_id))

@customer_bp.route('/cart/update', methods=['POST'])
def update_cart():
    item_id = str(request.form.get('item_id'))
    action = request.form.get('action') # 'increase', 'decrease', 'remove'

    cart = session.get('cart', {})
    if item_id in cart:
        if action == 'increase':
            cart[item_id] += 1
        elif action == 'decrease':
            cart[item_id] -= 1
            if cart[item_id] <= 0:
                del cart[item_id]
        elif action == 'remove':
            del cart[item_id]

    if not cart:
        session.pop('cart_restaurant_id', None)

    session['cart'] = cart
    session.modified = True
    return redirect(url_for('customer.view_cart'))

@customer_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session.pop('cart_restaurant_id', None)
    flash('Cart has been emptied.', 'info')
    return redirect(url_for('customer.view_cart'))

@customer_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    restaurant_id = session.get('cart_restaurant_id')
    if not cart or not restaurant_id:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('customer.view_cart'))

    delivery_address = request.form.get('delivery_address', '').strip()
    customer_phone = request.form.get('customer_phone', '').strip()
    payment_method = request.form.get('payment_method', 'cash_on_delivery')
    notes = request.form.get('notes', '').strip()
    promo_code = request.form.get('promo_code', '').strip()

    if not delivery_address or not customer_phone:
        flash('Please provide delivery address and contact phone number.', 'danger')
        return redirect(url_for('customer.view_cart'))

    items_list = [{'menu_item_id': int(k), 'quantity': v} for k, v in cart.items()]
    order, err = OrderService.create_order(
        customer_id=session['user_id'],
        restaurant_id=restaurant_id,
        items=items_list,
        delivery_address=delivery_address,
        customer_phone=customer_phone,
        payment_method=payment_method,
        notes=notes,
        promo_code=promo_code
    )

    if err:
        flash(f'Error placing order: {err}', 'danger')
        return redirect(url_for('customer.view_cart'))

    # Empty cart on successful order
    session.pop('cart', None)
    session.pop('cart_restaurant_id', None)
    flash(f'Order #{order.order_number} placed successfully! Track your delivery status below.', 'success')
    return redirect(url_for('customer.order_detail', order_id=order.id))

@customer_bp.route('/orders')
@login_required
def my_orders():
    orders = OrderService.get_orders_by_customer(session['user_id'])
    return render_template('customer/orders.html', orders=orders)

@customer_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = OrderService.get_order_by_id(order_id)
    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('customer.my_orders'))
    
    # Check permissions
    if order.customer_id != session['user_id'] and session.get('user_role') not in ('admin', 'rider'):
        flash('You cannot view this order.', 'danger')
        return redirect(url_for('customer.my_orders'))

    return render_template('customer/order_detail.html', order=order)

@customer_bp.route('/orders/<int:order_id>/review', methods=['POST'])
@login_required
def submit_review(order_id):
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '').strip()

    review_id, err = OrderService.add_review(order_id, session['user_id'], rating, comment)
    if err:
        flash(err, 'danger')
    else:
        flash('Thank you for your review!', 'success')
    return redirect(url_for('customer.order_detail', order_id=order_id))
