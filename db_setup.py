import sqlite3

conn = sqlite3.connect("bookings.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    email TEXT,
    phone TEXT,
    car TEXT,
    pickup TEXT,
    drop_location TEXT,
    start_date TEXT,
    end_date TEXT,
    comments TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()
conn.close()

print("✅ bookings table created successfully")
