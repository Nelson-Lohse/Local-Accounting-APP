import sqlite3
from database import init_db
from database import print_transactions_pretty

def main():
    print("Start Accounting APP")
    init_db()
    print_transactions_pretty()

if __name__=="__main__":
    main()

# Functionallity: