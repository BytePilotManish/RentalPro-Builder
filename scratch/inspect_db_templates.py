import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", cursor.fetchall())

cursor.execute("SELECT * FROM templates")
print("Templates in DB:")
for r in cursor.fetchall():
    print(r)
conn.close()
