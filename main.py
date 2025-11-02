import sqlite3
from database import init_db
from database import print_transactions_pretty, print_catagories_pretty, add_transaction, delete_transaction, get_transactions, get_transaction_catagory, update_transaction, income, expenses, get_revenue, get_income_transactions, get_expenses_transactions

def main():
    print("Start Accounting APP\n")
    init_db()

    add_transaction("CSGO Cases", "Entertainment", 200.0, "expense")
    add_transaction("Salary", "Job", 3000.0, "income")
    get_transactions()

    update_transaction(1, "CSGO Skins", "Entertainment", 300.0, "expense")

    get_expenses_transactions()

    expenses()

    get_income_transactions()

    income()

    get_revenue()


    print("Transactions table")
    print_transactions_pretty()
    print("catagories table")
    print_catagories_pretty()

if __name__=="__main__":
    main()

# Functionallity: