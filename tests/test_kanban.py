from src.services.order_service import OrderService
from src.services.kanban_service import KanbanService

def test_kanban_valid_state_transitions(app):
    with app.app_context():
        # Order 5 in seeds is 'placed'
        # 1. Transition placed -> preparing
        order, err = OrderService.update_order_status(5, 'preparing')
        assert err is None
        assert order.status == 'preparing'
        assert order.preparing_at is not None

        # 2. Transition preparing -> ready
        order, err = OrderService.update_order_status(5, 'ready')
        assert err is None
        assert order.status == 'ready'
        assert order.ready_at is not None

        # 3. Transition ready -> in_transit
        order, err = OrderService.update_order_status(5, 'in_transit')
        assert err is None
        assert order.status == 'in_transit'
        assert order.dispatched_at is not None

        # 4. Transition in_transit -> delivered
        order, err = OrderService.update_order_status(5, 'delivered')
        assert err is None
        assert order.status == 'delivered'
        assert order.delivered_at is not None
        assert order.payment_status == 'completed'

def test_kanban_invalid_state_transition(app):
    with app.app_context():
        order, err = OrderService.update_order_status(4, 'delivered')
        assert err is not None
        assert "Invalid status transition" in err

def test_kanban_wip_limits_and_columns(app):
    with app.app_context():
        board = KanbanService.get_order_kanban_board()
        assert 'placed' in board
        assert 'preparing' in board
        assert 'ready' in board
        assert 'in_transit' in board
        assert 'delivered' in board
        assert isinstance(board['placed']['orders'], list)
        
        # Test updating WIP limits
        KanbanService.update_wip_limit('preparing', 2)
        limits = KanbanService.get_wip_limits()
        assert limits['preparing'] == 2

def test_kanban_dev_tasks(app):
    with app.app_context():
        dev_board = KanbanService.get_dev_kanban_board()
        assert len(dev_board['done']['tasks']) > 0
        
        # Move dev task
        task = dev_board['in_progress']['tasks'][0]
        success, err = KanbanService.move_kanban_task(task.id, 'review')
        assert success is True
        
        updated_dev_board = KanbanService.get_dev_kanban_board()
        review_task_ids = [t.id for t in updated_dev_board['review']['tasks']]
        assert task.id in review_task_ids
