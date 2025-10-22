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

# 3️⃣ Insert configs
for website, config in WEBSITE_CONFIGS.items():
    json_data = json.dumps(config, ensure_ascii=False)  # preserve unicode for Russian text
    cursor.execute("""
        INSERT OR REPLACE INTO configs (website, config_json)
        VALUES (?, ?)
    """, (website, json_data))

conn.commit()

# 4️⃣ Print stored values
cursor.execute("SELECT id, website, config_json FROM configs")
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}")
    print(f"Website: {row[1]}")
    print(f"Config JSON:\n{row[2]}\n{'-'*50}")

conn.close()
