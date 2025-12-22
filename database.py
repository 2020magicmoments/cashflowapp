import sqlite3
import os
from kivy.utils import platform
from kivy.app import App

class Database:
    def __init__(self):
        self.con = None
        self.cursor = None
        
        # We don't connect immediately here anymore to prevent crashes
        # during the import phase. We call connect() manually.
        self.connect()

    def connect(self):
        # Determine storage path based on OS
        if platform == "android":
            # This gets the safe, internal storage directory for your app
            app = App.get_running_app()
            # If this is called before the app starts, app will be None
            if app:
                storage_path = app.user_data_dir
                self.db_path = os.path.join(storage_path, "cashflow.db")
            else:
                # Fallback or error handling if initialized too early
                print("Error: Database initialized before App started")
                return 
        else:
            self.db_path = "cashflow.db"
            
        self.con = sqlite3.connect(self.db_path)
        self.cursor = self.con.cursor()
        self.create_table()
        print(f"Database connected at: {self.db_path}")

    def create_table(self):
        if self.cursor:
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

# DELETE the line below from this file!
# db = Database()