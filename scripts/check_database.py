import sqlite3

conn = sqlite3.connect('data/hazardx_live.db')
cursor = conn.cursor()
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
for name, sql in cursor.fetchall():
    print(f"=== TABLE: {name} ===")
    print(sql)
    print()
