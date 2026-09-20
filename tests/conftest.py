import pytest
import os
import tempfile
from src.app import create_app
from src.database.db import init_db
from src.database.seeder import seed_database

@pytest.fixture
def app():
    # Create a temporary file to isolate the database for tests
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    app = create_app({
        'TESTING': True,
        'DATABASE_PATH': db_path,
        'SECRET_KEY': 'test-secret-key-cse3206'
    })

    with app.app_context():
        init_db(db_path)
        seed_database(db_path)

    yield app

    # Cleanup after test
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
