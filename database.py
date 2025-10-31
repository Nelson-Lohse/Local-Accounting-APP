import sqlite3
import os
from tabulate import tabulate
from datetime import datetime

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
    #Catagories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS catagories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
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
    
    print(tabulate(rows, headers=headers, tablefmt="grid") + "\n")
    conn.close()
def print_catagories_pretty():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM catagories")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]  # get column names
    
    print(tabulate(rows, headers=headers, tablefmt="grid") + "\n")
    conn.close()
def add_transaction(description, category, amount, transaction_type, date=None):
    print("Enter Transaction Info")
    if date is None:
        date  = datetime.today().strftime('%Y-%m-%d')
    
    if transaction_type not in ['income', 'expense']:
        raise ValueError("Transaction type must be 'income' or 'expense'")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, description, category, amount, type)
        VALUES (?, ?, ?, ?, ?) 
    """, (date, description, category, amount, transaction_type))

    conn.commit()
    conn.close()

    print(f"Transaction added: {description}, {category}, {amount}, {transaction_type}, {date}")
def delete_transaction(transaction_id):
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Delete query The ? is a placeholder this syntax is neccesary to prevent SQL injection and is a good practice the ? will be substituded wiht teh transaction_id
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    
    # Commit and close
    conn.commit()
    conn.close()
    print(f"Transaction {transaction_id} deleted successfully.")





# TODO complete these functions

def get_transactions():
    print("List Transactions")

def get_transaction_catagory(catagory):
    print( catagory + "transactions")

def update_transaction(transaction):
    print( transaction + "updated")

def get_income():
    print("all income")

def get_expenses():
    print("all expenses")

