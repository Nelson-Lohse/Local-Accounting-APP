import sqlite3
from database import init_db
from database import print_transactions_pretty, print_catagories_pretty, add_transaction, delete_transaction

def main():
    print("Start Accounting APP\n")
    init_db()

    #add_transaction("CSGO Cases", "Entertainment", 200.0, "expense")
    #delete_transaction(2)


    print("Transactions table")
    print_transactions_pretty()
    print("catagories table")
    print_catagories_pretty()

if __name__=="__main__":
    main()

# Functionallity: