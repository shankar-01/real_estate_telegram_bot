import sqlite3
import json
from typing import Optional, Dict, Any

DB_PATH = "website_configs.db"  # Path to your existing SQLite database


class ConfigDBDriver:
    def __init__(self, db_path: str = DB_PATH):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Enables dict-like access
        self.cursor = self.conn.cursor()

        # Ensure table exists
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT UNIQUE,
            config_json TEXT
        )
        """)
        self.conn.commit()

    def insert_config(self, website: str, config: Dict[str, Any]):
        """Insert or replace a website config."""
        json_data = json.dumps(config, ensure_ascii=False)
        self.cursor.execute("""
            INSERT OR REPLACE INTO configs (website, config_json)
            VALUES (?, ?)
        """, (website, json_data))
        self.conn.commit()
        print(f"✅ Config saved for: {website}")

    def get_config(self, website: str) -> Optional[Dict[str, Any]]:
        """Fetch configuration by website name."""
        self.cursor.execute("SELECT config_json FROM configs WHERE website = ?", (website,))
        row = self.cursor.fetchone()
        if row:
            return json.loads(row["config_json"])
        print(f"⚠️ No config found for website: {website}")
        return None

    def list_configs(self):
        """List all website configs."""
        self.cursor.execute("SELECT id, website, config_json FROM configs")
        rows = self.cursor.fetchall()
        for row in rows:
            print(f"ID: {row['id']}")
            print(f"Website: {row['website']}")
            print(f"Config JSON: {row['config_json']}")
            print("-" * 60)

    def delete_config(self, website: str):
        """Delete config by website."""
        self.cursor.execute("DELETE FROM configs WHERE website = ?", (website,))
        self.conn.commit()
        print(f"🗑️ Deleted config for: {website}")

    def close(self):
        """Close the database connection."""
        self.conn.close()
        print("🔒 Connection closed.")


# -------------------------------
# Example usage (for testing)
# -------------------------------
if __name__ == "__main__":
    db = ConfigDBDriver()

    # 1️⃣ Insert new config
    example_config = {"xpath": "//div[@class='property']", "transform": "value.strip()"}
    db.insert_config("example.com", example_config)

    # 2️⃣ Fetch specific config
    config = db.get_config("example.com")
    print("Fetched config:", config)

    # 3️⃣ List all configs
    db.list_configs()

    # 4️⃣ Delete example
    # db.delete_config("example.com")

    db.close()
