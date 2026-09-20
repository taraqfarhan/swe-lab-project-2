import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'food-delivery-kanban-secret-key-cse3206-group11')
    DATABASE_PATH = os.path.join(PROJECT_ROOT, 'food_delivery.db')
    TEST_DATABASE_PATH = os.path.join(PROJECT_ROOT, 'test_food_delivery.db')
    DEBUG = True
    PORT = int(os.environ.get('PORT', 9000))
    
    # Kanban Flow Configuration (WIP Limits)
    ORDER_WIP_LIMITS = {
        'placed': 15,
        'preparing': 5,
        'ready': 4,
        'in_transit': 6,
        'delivered': 100
    }
    
    DEV_TASK_WIP_LIMITS = {
        'backlog': 10,
        'in_progress': 3,
        'review': 2,
        'done': 50
    }
