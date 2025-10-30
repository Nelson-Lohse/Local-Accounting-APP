import sqlite3
from database import init_db
from database import print_transactions_pretty, print_catagories_pretty

def main():
    print("Start Accounting APP\n")
    init_db()
    print("Transactions table")
    print_transactions_pretty()
    print("catagories table")
    print_catagories_pretty()

if __name__=="__main__":
    main()

# Functionallity: