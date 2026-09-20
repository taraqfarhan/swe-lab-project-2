import sys
import os

# Ensure the root directory is on the python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.app import create_app
from src.database.db import init_db
from src.database.seeder import seed_database
from src.config import Config

app = create_app()

if __name__ == '__main__':
    # Initialize DB if not present
    if not os.path.exists(Config.DATABASE_PATH):
        print("Initializing and seeding database...")
        init_db(Config.DATABASE_PATH)
        seed_database(Config.DATABASE_PATH)
        print("Database ready!")

    port = Config.PORT
    print("==================================================================")
    print(" FoodFlow Delivery Application (Group 11 - Kanban MVP) ")
    print(" CSE 3206 - Software Engineering Sessional | RUET CSE")
    print("==================================================================")
    print(f" Server running on: http://127.0.0.1:{port}")
    print(f" Live Kanban Board: http://127.0.0.1:{port}/kanban")
    print(" Demo Accounts: (Password for all: password123)")
    print("   • Customer:         john_doe")
    print("   • Restaurant Owner: chef_mario")
    print("   • Delivery Rider:   rider_alex")
    print("   • Administrator:    admin")
    print("==================================================================")

    app.run(host='0.0.0.0', port=port, debug=True)
