import sys
import sqlite3
import hashlib

class SQLite:
    def __init__(self, fileName):
        self.conn = None
        self.cursor = None
        self.fileName = fileName

    def connectSQL(self):
        try:
            self.conn = sqlite3.connect(self.fileName)
            self.cursor = self.conn.cursor()
            print("Connected to the database successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None
            self.cursor = None
            sys.exit(1)

    def isLogin(self, username, password):
        if not self.cursor:
            print("Cursor is not initialized. Make sure the database connection was successful.")
            return False
        
        passed = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, passed))
            result = self.cursor.fetchone()
            if result:
                print("Login successful.")
                return True
            else:
                print("Login failed: Invalid username or password.")
                return False
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return False

    def closeSQL(self):
        if self.cursor:
            self.cursor.close()
            print("Cursor closed.")
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def getDataSensor(self):
        if not self.cursor:
            print("Cursor is not initialized. Make sure the database connection was successful.")
            return None
        
        try:
            self.cursor.execute("SELECT * FROM sensor_data")
            result = self.cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        
    def showRealTimeData(self):
        if not self.cursor:
            print("Cursor is not initialized. Make sure the database connection was successful.")
            return None
        
        try:
            self.cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
