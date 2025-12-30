import sqlite3
import json
from config import WEBSITE_CONFIGS  # your config file

# 1️⃣ Connect to SQLite (or create it)
conn = sqlite3.connect("website_configs.db")
cursor = conn.cursor()

# 2️⃣ Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT UNIQUE,
    config_json TEXT
)
""")