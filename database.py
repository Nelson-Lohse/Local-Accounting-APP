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
def get_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    print("List Transactions\n")
    print(rows)
    return rows
def get_transaction_catagory(catagory):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE category = ?", (catagory,))
    rows = cursor.fetchall()
    print( catagory + " transactions\n")
    print(rows)
    return rows
def update_transaction(id, description=None, category=None, amount=None, transaction_type=None, date=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE id = ?", (id,))
    transaction = cursor.fetchone()
    if not transaction:
        print("Transaction not found.\n")
        return
    updated_description = description if description is not None else transaction[2]
    updated_category = category if category is not None else transaction[3]
    updated_amount = amount if amount is not None else transaction[4]
    updated_type = transaction_type if transaction_type is not None else transaction[5]
    updated_date = date if date is not None else transaction[1]
    cursor.execute("""
        UPDATE transactions
        SET description = ?, category = ?, amount = ?, type = ?, date = ?
        WHERE id = ?
    """, (updated_description, updated_category, updated_amount, updated_type, updated_date, id))
    conn.commit()
    conn.close()
    print(f"Transaction {id} updated successfully.\n")
def get_income_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE type = 'income'")
    rows = cursor.fetchall()
    
    print("all income\n")
    print(rows)
    return rows
def income():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    income = cursor.fetchone()[0] or 0
    print(f"Total Income: {income}\n")
    return income
def get_expenses_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE type = 'expense'")
    rows = cursor.fetchall()

    print("all expenses\n")
    print(rows)
    return rows
def expenses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    expenses = cursor.fetchone()[0] or 0
    print(f"Total Expenses: {expenses}\n")
    return expenses
def get_revenue():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    expenses = cursor.fetchone()[0] or 0

    revenue = income - expenses
    print(f"Total Revenue: {revenue}\n")
    return revenue
def add_catagory(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO catagories (name) VALUES (?)", (name,))
    
    conn.commit()
    conn.close()
    print(f"Catagory added: {name}\n")