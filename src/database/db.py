import sqlite3
import os
from flask import g, current_app
from src.config import Config

def get_db(db_path=None):
    """Obtain a database connection stored in Flask's application context 'g'."""
    if 'db' not in g:
        path = db_path or current_app.config.get('DATABASE_PATH', Config.DATABASE_PATH)
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    """Close the database connection if it exists."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(db_path=None):
    """Initialize database tables using schema.sql."""
    path = db_path or Config.DATABASE_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()

def query_db(query, args=(), one=False, db_path=None):
    """Helper to query database and return dictionary or list of dictionaries."""
    db = get_db(db_path)
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (dict(rv[0])) if rv and one else ([dict(r) for r in rv] if not one else None)

def execute_db(query, args=(), db_path=None):
    """Helper to execute write operations (INSERT, UPDATE, DELETE) and return lastrowid."""
    db = get_db(db_path)
    cur = db.execute(query, args)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id
