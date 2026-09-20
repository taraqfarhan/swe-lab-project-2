import os
from flask import Flask, render_template
from src.config import Config
from src.database.db import init_db, close_db
from src.database.seeder import seed_database
from src.routes.auth_routes import auth_bp
from src.routes.customer_routes import customer_bp
from src.routes.restaurant_routes import restaurant_bp
from src.routes.delivery_routes import delivery_bp
from src.routes.admin_routes import admin_bp
from src.routes.kanban_routes import kanban_bp
from src.routes.api_routes import api_bp

def create_app(test_config=None):
    """Application factory for the Food Delivery Application."""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    # Register DB teardown
    app.teardown_appcontext(close_db)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(kanban_bp)
    app.register_blueprint(api_bp)

    # Global template context processor
    @app.context_processor
    def inject_cart_count():
        from flask import session
        cart = session.get('cart', {})
        count = sum(cart.values()) if isinstance(cart, dict) else 0
        return {'cart_item_count': count, 'app_name': 'FoodFlow Kanban'}

    # 404 handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_message="Page not found"), 404

    # Ensure DB file exists and is seeded if not present
    db_file = app.config.get('DATABASE_PATH', Config.DATABASE_PATH)
    if not os.path.exists(db_file) and not app.config.get('TESTING'):
        init_db(db_file)
        seed_database(db_file)

    return app

if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=Config.PORT, debug=True)
