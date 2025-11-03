import sqlite3
from datetime import datetime
import database as db

def main():
    print("Start Accounting APP\n")
    db.init_db()
    """

    db.add_catagory("Income")
    db.add_catagory("Food")
    db.add_catagory("Utilities")
    db.add_catagory("Entertainment")
    db.add_catagory("Trasnportation")

    ### Add sample transactions
    
    db.add_transaction("Salary June", "Salary", 5000.00, "income", "2024-06-01")
    db.add_transaction("Groceries", "Food", 150.75, "expense", "2024-06-02")
    db.add_transaction("Electricity Bill", "Utilities", 75.50, "expense", "2024-06-03")
    db.add_transaction("Freelance Project", "Salary", 1200.00, "income", "2024-06-04")
    db.add_transaction("Internet Bill", "Utilities", 60.00, "expense", "2024-06-05")
    db.add_transaction("Dinner Out", "Food", 45.25, "expense", "2024-06-06")
    db.add_transaction("Movie Tickets", "Entertainment", 30.00, "expense", "2024-06-07")
    db.add_transaction("Concert Tickets", "Entertainment", 75.00, "expense", "2024-06-08")
    db.add_transaction("Lunch Out", "Food", 20.00, "expense", "2024-06-09")
    db.add_transaction("Bus Pass", "Transportation", 50.00, "expense", "2024-06-10")
    db.add_transaction("Taxi Ride", "Transportation", 35.00, "expense", "2024-06-11")
    db.add_transaction("Bonus", "Salary", 1000.00, "income", "2024-06-12")
    db.add_transaction("Snacks", "Food", 15.50, "expense", "2024-06-13")
    db.add_transaction("Water Bill", "Utilities", 40.00, "expense", "2024-06-14")
    db.add_transaction("Uber", "Transportation", 25.00, "expense", "2024-06-15")
    db.add_transaction("Dinner Party", "Food", 80.00, "expense", "2024-06-16")
    db.add_transaction("Theater Tickets", "Entertainment", 60.00, "expense", "2024-06-17")
    db.add_transaction("Freelance Writing", "Salary", 400.00, "income", "2024-06-18")
    db.add_transaction("Gym Snacks", "Food", 10.00, "expense", "2024-06-19")
    db.add_transaction("Movie Night", "Entertainment", 25.00, "expense", "2024-06-20")
    db.add_transaction("Bus Ticket", "Transportation", 5.00, "expense", "2024-06-21")
    db.add_transaction("Internet Upgrade", "Utilities", 70.00, "expense", "2024-06-22")
    db.add_transaction("Pizza Party", "Food", 55.00, "expense", "2024-06-23")
    db.add_transaction("Freelance Design", "Salary", 800.00, "income", "2024-06-24")
    db.add_transaction("Movie Snacks", "Food", 12.50, "expense", "2024-06-25")
    db.add_transaction("Concert Snacks", "Food", 20.00, "expense", "2024-06-26")
    db.add_transaction("Taxi Fare", "Transportation", 40.00, "expense", "2024-06-27")
    db.add_transaction("Board Game Night", "Entertainment", 35.00, "expense", "2024-06-28")
    db.add_transaction("Salary July", "Salary", 5000.00, "income", "2024-06-29")
    db.add_transaction("Dinner Out", "Food", 60.00, "expense", "2024-06-30")    
    ###
    """


    print("Transactions table")
    db.print_transactions_pretty()
    print("catagories table")
    db.print_catagories_pretty()

if __name__=="__main__":
    main()

