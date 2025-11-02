import sqlite3

import database as db

def main():
    print("Start Accounting APP\n")
    db.init_db()

    print("Transactions table")
    db.print_transactions_pretty()
    print("catagories table")
    db.print_catagories_pretty()

if __name__=="__main__":
    main()

