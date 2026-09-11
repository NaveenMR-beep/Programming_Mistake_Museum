import sqlite3

connection = sqlite3.connect("museum.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mistakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    error_type TEXT NOT NULL,
    error_message TEXT,
    project TEXT,
    code TEXT,
    explanation TEXT,
    solution TEXT,
    created_at TEXT
)
""")

connection.commit()

connection.close()

print("Database created successfully!")
connection = sqlite3.connect("museum.db")
cursor = connection.cursor()

cursor.execute("""
    ALTER TABLE mistakes
    ADD COLUMN category TEXT
""")

connection.commit()
connection.close()

print("Category column added successfully!")
