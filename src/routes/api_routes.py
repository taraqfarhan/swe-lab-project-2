from flask import Blueprint, jsonify, request
from src.services.restaurant_service import RestaurantService
from src.services.order_service import OrderService
from src.services.kanban_service import KanbanService

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'project': 'Food Delivery Application (Group 11)', 'process_model': 'Kanban'})

@api_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    cuisine = request.args.get('cuisine')
    search = request.args.get('search')
    restaurants = RestaurantService.get_all_restaurants(cuisine_filter=cuisine, search_query=search)
    return jsonify({
        'success': True,
        'count': len(restaurants),
        'data': [r.__dict__ for r in restaurants]
    })

@api_bp.route('/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    restaurant = RestaurantService.get_restaurant_by_id(restaurant_id)
    if not restaurant:
        return jsonify({'success': False, 'message': 'Restaurant not found'}), 404

    items = RestaurantService.get_menu_items(restaurant_id, available_only=True)
    return jsonify({
        'success': True,
        'restaurant': restaurant.name,
        'count': len(items),
        'items': [i.__dict__ for i in items]
    })

@api_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order_status(order_id):
    order = OrderService.get_order_by_id(order_id)
    if not order:
        return jsonify({'success': False, 'message': 'Order not found'}), 404

    return jsonify({
        'success': True,
        'order_number': order.order_number,
        'status': order.status,
        'status_label': order.status_label,
        'total_amount': order.total_amount,
        'placed_at': order.placed_at,
        'dispatched_at': order.dispatched_at,
        'delivered_at': order.delivered_at
    })

@api_bp.route('/kanban/metrics', methods=['GET'])
def get_metrics():
    metrics = KanbanService.get_analytics_summary()
    return jsonify({'success': True, 'metrics': metrics})
