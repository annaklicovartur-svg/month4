import sqlite3
from datetime import datetime

class ShoppingListDB:
    def __init__(self, db_name="shopping_list.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                purchased INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_purchase(self, name, quantity=1):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO purchases (name, quantity) VALUES (?, ?)",
            (name, quantity)
        )
        conn.commit()
        purchase_id = cursor.lastrowid
        conn.close()
        return purchase_id
    
    def get_all_purchases(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity, purchased FROM purchases ORDER BY purchased, created_at DESC")
        purchases = cursor.fetchall()
        conn.close()
        return purchases
    
    def get_purchases_by_filter(self, filter_type="all"):
        """filter_type: 'all', 'purchased', 'not_purchased'"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if filter_type == "purchased":
            cursor.execute("SELECT id, name, quantity, purchased FROM purchases WHERE purchased = 1 ORDER BY created_at DESC")
        elif filter_type == "not_purchased":
            cursor.execute("SELECT id, name, quantity, purchased FROM purchases WHERE purchased = 0 ORDER BY created_at DESC")
        else:
            cursor.execute("SELECT id, name, quantity, purchased FROM purchases ORDER BY purchased, created_at DESC")
        
        purchases = cursor.fetchall()
        conn.close()
        return purchases
    
    def toggle_purchase(self, purchase_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT purchased FROM purchases WHERE id = ?", (purchase_id,))
        result = cursor.fetchone()
        if result:
            new_state = 0 if result[0] else 1
            cursor.execute("UPDATE purchases SET purchased = ? WHERE id = ?", (new_state, purchase_id))
            conn.commit()
        conn.close()
    
    def delete_purchase(self, purchase_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM purchases WHERE id = ?", (purchase_id,))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM purchases")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM purchases WHERE purchased = 1")
        purchased = cursor.fetchone()[0]
        conn.close()
        return total, purchased

db = ShoppingListDB()