import sqlite3
import os
from tabulate import tabulate

DB_PATH = "data/accounting.db"

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT,
            category TEXT,
            amount REAL NOT NULL,
            type TEXT CHECK(type IN ('income','expense')) NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    
def print_transactions_pretty():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]  # get column names
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    conn.close()


def add_transaction():
    print("Enter Transaction Info")

def get_transactions():
    print("List Transactions")

def get_transaction_catagory(catagory):
    print( catagory + "transactions")

def update_transaction(transaction):
    print( transaction + "updated")

def delete_transaction(transaction):
    print("deleted" + transaction)

def get_income():
    print("all income")

def get_expenses():
    print("all expenses")

