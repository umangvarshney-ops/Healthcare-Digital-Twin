import sqlite3

conn = sqlite3.connect("database/healthcare.db")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# Patient History Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patient_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    age INTEGER,
    chol REAL,
    trestbps REAL,
    thalach REAL,
    health_score REAL,
    risk_level TEXT,
    disease_probability REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")
