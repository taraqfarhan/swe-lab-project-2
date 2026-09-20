from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.services.order_service import OrderService
from src.routes.auth_routes import role_required

delivery_bp = Blueprint('delivery', __name__, url_prefix='/delivery')

@delivery_bp.route('/dashboard')
@role_required('rider')
def dashboard():
    rider_id = session['user_id']
    available_orders = OrderService.get_available_delivery_orders()
    my_orders = OrderService.get_orders_by_rider(rider_id)
    
    active_deliveries = [o for o in my_orders if o.status in ('ready', 'in_transit')]
    completed_deliveries = [o for o in my_orders if o.status == 'delivered']
    
    total_earnings = sum(o.delivery_fee for o in completed_deliveries)

    return render_template('delivery/dashboard.html', 
                           available_orders=available_orders,
                           active_deliveries=active_deliveries,
                           completed_deliveries=completed_deliveries,
                           total_earnings=round(total_earnings, 2))

@delivery_bp.route('/orders/<int:order_id>/accept', methods=['POST'])
@role_required('rider')
def accept_order(order_id):
    rider_id = session['user_id']
    OrderService.assign_rider(order_id, rider_id)
    flash('You have accepted this delivery task.', 'success')
    return redirect(url_for('delivery.dashboard'))

@delivery_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@role_required('rider')
def update_status(order_id):
    target_status = request.form.get('target_status')
    order, err = OrderService.update_order_status(order_id, target_status, actor_role='rider')
    if err:
        flash(err, 'danger')
    else:
        flash(f'Order #{order.order_number} status updated to "{order.status_label}".', 'success')
    return redirect(url_for('delivery.dashboard'))
