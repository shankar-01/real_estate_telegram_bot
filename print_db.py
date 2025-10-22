import sqlite3

DB_NAME = "websites_data.db"

def print_db_values(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"\n📋 Table: {table_name}")
        cursor.execute(f"SELECT * FROM '{table_name}'")
        rows = cursor.fetchall()
        if not rows:
            print("  ⚠️ No data found")
        else:
            # Fetch column names
            cursor.execute(f'PRAGMA table_info("{table_name}")')
            columns = [col[1] for col in cursor.fetchall()]
            for row in rows:
                row_dict = dict(zip(columns, row))
                for k, v in row_dict.items():
                    print(f"  {k}: {v}")
                print("-" * 30)

    conn.close()

if __name__ == "__main__":
    print_db_values()
