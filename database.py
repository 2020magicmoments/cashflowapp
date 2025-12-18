import sqlite3
import os
from kivy.utils import platform

class Database:
    def __init__(self):
        # Determine storage path based on OS
        if platform == "android":
            from android.storage import app_storage_path
            storage_path = app_storage_path()
            self.db_path = os.path.join(storage_path, "cashflow.db")
        else:
            self.db_path = "cashflow.db"
            
        self.con = sqlite3.connect(self.db_path)
        self.cursor = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                amount REAL,
                category TEXT,
                date TEXT
            )
        """)
        self.con.commit()

    def add_transaction(self, t_type, amount, category, date):
        self.cursor.execute("INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)",
                            (t_type, amount, category, date))
        self.con.commit()

    def get_balance(self):
        self.cursor.execute("SELECT type, amount FROM transactions")
        data = self.cursor.fetchall()
        balance = 0
        for row in data:
            if row[0] == "Income":
                balance += row[1]
            else:
                balance -= row[1]
        return balance

    def get_report(self, start_date, end_date):
        self.cursor.execute("SELECT * FROM transactions WHERE date BETWEEN ? AND ? ORDER BY date DESC", 
                            (start_date, end_date))
        return self.cursor.fetchall()

# Create a single instance to be imported by other files
db = Database()