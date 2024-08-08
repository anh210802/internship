import sqlite3
import hashlib

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("data_sql.sqlite")
cur = conn.cursor()

# Create the users table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(64) NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature FLOAT,
    humidity FLOAT,
    pm1 FLOAT,
    pm25 FLOAT,
    pm10 FLOAT,
    co_value FLOAT,
    max_value FLOAT,
    level INT,
    date TIMESTAMP
);
""")

# User data
username1, password1 = "admin", hashlib.sha256("admin".encode()).hexdigest()
username2, password2 = "user", hashlib.sha256("user".encode()).hexdigest()
username3, password3 = "guest", hashlib.sha256("guest".encode()).hexdigest()

# Insert user data into the table
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username1, password1))
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username2, password2))
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username3, password3))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
