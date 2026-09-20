from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.services.restaurant_service import RestaurantService
from src.services.order_service import OrderService
from src.routes.auth_routes import role_required

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@restaurant_bp.route('/dashboard')
@role_required('restaurant_owner')
def dashboard():
    restaurant = RestaurantService.get_restaurant_by_owner_id(session['user_id'])
    if not restaurant:
        flash('No restaurant profile associated with this account.', 'warning')
        return render_template('restaurant/dashboard.html', restaurant=None, orders=[])

    orders = OrderService.get_orders_by_restaurant(restaurant.id)
    return render_template('restaurant/dashboard.html', restaurant=restaurant, orders=orders)

@restaurant_bp.route('/menu')
@role_required('restaurant_owner')
def menu_manage():
    restaurant = RestaurantService.get_restaurant_by_owner_id(session['user_id'])
    if not restaurant:
        flash('No restaurant profile found.', 'warning')
        return redirect(url_for('restaurant.dashboard'))

    items = RestaurantService.get_menu_items(restaurant.id)
    return render_template('restaurant/menu_manage.html', restaurant=restaurant, items=items)

@restaurant_bp.route('/menu/add', methods=['POST'])
@role_required('restaurant_owner')
def add_item():
    restaurant = RestaurantService.get_restaurant_by_owner_id(session['user_id'])
    if not restaurant:
        flash('Restaurant not found.', 'danger')
        return redirect(url_for('restaurant.dashboard'))

    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', 'Main Dish').strip()
    price = float(request.form.get('price', 0.0))
    image_url = request.form.get('image_url', '').strip() or 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&auto=format&fit=crop'

    RestaurantService.add_menu_item(restaurant.id, name, description, category, price, image_url)
    flash(f'Menu item "{name}" created successfully.', 'success')
    return redirect(url_for('restaurant.menu_manage'))

@restaurant_bp.route('/menu/<int:item_id>/edit', methods=['POST'])
@role_required('restaurant_owner')
def edit_item(item_id):
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', '').strip()
    price = float(request.form.get('price', 0.0))
    image_url = request.form.get('image_url', '').strip()
    is_available = bool(request.form.get('is_available'))

    RestaurantService.update_menu_item(item_id, name, description, category, price, image_url, is_available)
    flash('Menu item updated successfully.', 'success')
    return redirect(url_for('restaurant.menu_manage'))

@restaurant_bp.route('/menu/<int:item_id>/toggle', methods=['POST'])
@role_required('restaurant_owner')
def toggle_item(item_id):
    updated = RestaurantService.toggle_item_availability(item_id)
    status_str = "Available" if updated.is_available else "Sold Out"
    flash(f'Item "{updated.name}" is now {status_str}.', 'info')
    return redirect(url_for('restaurant.menu_manage'))

@restaurant_bp.route('/menu/<int:item_id>/delete', methods=['POST'])
@role_required('restaurant_owner')
def delete_item(item_id):
    RestaurantService.delete_menu_item(item_id)
    flash('Menu item removed.', 'info')
    return redirect(url_for('restaurant.menu_manage'))

@restaurant_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@role_required('restaurant_owner')
def update_order_status(order_id):
    target_status = request.form.get('target_status')
    order, err = OrderService.update_order_status(order_id, target_status, actor_role='restaurant_owner')
    if err:
        flash(err, 'danger')
    else:
        flash(f'Order #{order.order_number} moved to status "{order.status_label}".', 'success')
    return redirect(url_for('restaurant.dashboard'))
