from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from src.services.kanban_service import KanbanService
from src.services.order_service import OrderService
from src.routes.auth_routes import login_required

kanban_bp = Blueprint('kanban', __name__, url_prefix='/kanban')

@kanban_bp.route('', methods=['GET'])
@kanban_bp.route('/', methods=['GET'])
def board():
    view_type = request.args.get('view', 'orders') # 'orders' or 'dev'
    order_columns = KanbanService.get_order_kanban_board()
    dev_columns = KanbanService.get_dev_kanban_board()
    metrics = KanbanService.get_analytics_summary()
    wip_limits = KanbanService.get_wip_limits()

    return render_template('kanban/board.html', 
                           view_type=view_type,
                           order_columns=order_columns,
                           dev_columns=dev_columns,
                           metrics=metrics,
                           wip_limits=wip_limits)

@kanban_bp.route('/orders/move', methods=['POST'])
def move_order():
    order_id = int(request.form.get('order_id'))
    target_status = request.form.get('target_status')
    
    order, err = OrderService.update_order_status(order_id, target_status)
    if err:
        flash(f'Cannot move order: {err}', 'danger')
    else:
        flash(f'Order #{order.order_number} moved to "{order.status_label}".', 'success')
    
    return redirect(url_for('kanban.board', view='orders'))

@kanban_bp.route('/dev/move', methods=['POST'])
def move_dev_task():
    task_id = int(request.form.get('task_id'))
    target_column = request.form.get('target_column')

    success, err = KanbanService.move_kanban_task(task_id, target_column)
    if not success:
        flash(f'Failed to move task: {err}', 'danger')
    else:
        flash('Development task moved successfully.', 'success')

    return redirect(url_for('kanban.board', view='dev'))

@kanban_bp.route('/dev/add', methods=['POST'])
def add_dev_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', 'Engineering').strip()
    priority = request.form.get('priority', 'medium')
    column_name = request.form.get('column_name', 'backlog')
    assignee = request.form.get('assignee', 'Unassigned').strip()

    if not title:
        flash('Task title is required.', 'danger')
        return redirect(url_for('kanban.board', view='dev'))

    KanbanService.create_kanban_task(title, description, category, priority, column_name, assignee)
    flash(f'Task "{title}" added to Kanban Backlog.', 'success')
    return redirect(url_for('kanban.board', view='dev'))

@kanban_bp.route('/wip-limits/update', methods=['POST'])
def update_wip():
    column_name = request.form.get('column_name')
    new_limit = int(request.form.get('wip_limit', 5))

    KanbanService.update_wip_limit(column_name, new_limit)
    flash(f'WIP limit for column "{column_name}" updated to {new_limit}.', 'info')
    return redirect(url_for('kanban.board', view=request.form.get('return_view', 'orders')))
