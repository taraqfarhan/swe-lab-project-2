from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.services.auth_service import AuthService
from src.services.restaurant_service import RestaurantService
from src.services.order_service import OrderService
from src.services.kanban_service import KanbanService
from src.routes.auth_routes import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@role_required('admin')
def dashboard():
    users = AuthService.get_all_users()
    restaurants = RestaurantService.get_all_restaurants()
    orders = OrderService.get_all_orders()
    metrics = KanbanService.get_analytics_summary()
    
    return render_template('admin/dashboard.html', 
                           users=users, 
                           restaurants=restaurants, 
                           orders=orders, 
                           metrics=metrics)
