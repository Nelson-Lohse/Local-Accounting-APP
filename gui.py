import sys
import os
import sqlite3
from datetime import datetime
from PyQt6.QtGui import QAction

from PyQt6 import QtWidgets as QtW, QtCore as QtC
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from database import (
    init_db, get_transactions, add_transaction, delete_transaction, update_transaction,
    get_income_transactions, get_expenses_transactions, income, expenses, get_revenue
)

DB_PATH = "data/accounting.db"

class AccountingApp(QtW.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Accounting App")
        self.setGeometry(200, 200, 900, 600)

        init_db()

        self.tabs = QtW.QTabWidget()
        self.setCentralWidget(self.tabs)

        self.transactions_tab = QtW.QWidget()
        self.categories_tab = QtW.QWidget()
        self.revenue_tab = QtW.QWidget()

        self.tabs.addTab(self.transactions_tab, "Transactions")
        self.tabs.addTab(self.categories_tab, "Categories")
        self.tabs.addTab(self.revenue_tab, "Revenue & Charts")

        self.setup_transactions_tab()
        self.setup_categories_tab()
        self.setup_revenue_tab()
        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        add_tx_action = QAction("Add Transaction", self)
        add_tx_action.triggered.connect(self.show_add_transaction_form)
        file_menu.addAction(add_tx_action)

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.load_transactions)
        file_menu.addAction(refresh_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def setup_transactions_tab(self):
        layout = QtW.QVBoxLayout()
        self.transactions_tab.setLayout(layout)

        self.tx_table = QtW.QTableWidget()
        layout.addWidget(self.tx_table)

        btn_layout = QtW.QHBoxLayout()
        layout.addLayout(btn_layout)

        refresh_btn = QtW.QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_transactions)
        btn_layout.addWidget(refresh_btn)

        add_btn = QtW.QPushButton("Add Transaction")
        add_btn.clicked.connect(self.show_add_transaction_form)
        btn_layout.addWidget(add_btn)

        update_btn = QtW.QPushButton("Update Transaction")
        update_btn.clicked.connect(self.show_update_transaction_form)
        btn_layout.addWidget(update_btn)

        delete_btn = QtW.QPushButton("Delete Transaction")
        delete_btn.clicked.connect(self.delete_selected_transaction)
        btn_layout.addWidget(delete_btn)

        self.load_transactions()

    def load_transactions(self):
        transactions = get_transactions()
        self.tx_table.setRowCount(len(transactions))
        self.tx_table.setColumnCount(6)
        self.tx_table.setHorizontalHeaderLabels(["ID", "Date", "Description", "Category", "Amount", "Type"])

        for row_index, row_data in enumerate(transactions):
            for col_index, value in enumerate(row_data):
                self.tx_table.setItem(row_index, col_index, QtW.QTableWidgetItem(str(value)))

        self.tx_table.resizeColumnsToContents()

    def show_add_transaction_form(self):
        self.show_transaction_form(mode="add")

    def show_update_transaction_form(self):
        selected = self.tx_table.currentRow()
        if selected < 0:
            QtW.QMessageBox.warning(self, "No Selection", "Please select a transaction to update.")
            return
        tx_id = int(self.tx_table.item(selected, 0).text())
        current_data = [
            self.tx_table.item(selected, i).text() for i in range(6)
        ]
        self.show_transaction_form(mode="update", tx_id=tx_id, current_data=current_data)

    def show_transaction_form(self, mode="add", tx_id=None, current_data=None):
        dialog = QtW.QDialog(self)
        dialog.setWindowTitle("Transaction Form")
        layout = QtW.QFormLayout(dialog)

        desc_input = QtW.QLineEdit()
        cat_input = QtW.QComboBox()
        amount_input = QtW.QDoubleSpinBox()
        amount_input.setMaximum(1e9)
        type_input = QtW.QComboBox()
        type_input.addItems(["income", "expense"])
        date_input = QtW.QDateEdit(QtC.QDate.currentDate())
        date_input.setCalendarPopup(True)

        # Populate categories dropdown
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM catagories")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        cat_input.addItems(categories)

        if mode == "update" and current_data:
            desc_input.setText(current_data[2])
            cat_input.setCurrentText(current_data[3])
            amount_input.setValue(float(current_data[4]))
            type_input.setCurrentText(current_data[5])
            date_input.setDate(QtC.QDate.fromString(current_data[1], "yyyy-MM-dd"))

        layout.addRow("Description:", desc_input)
        layout.addRow("Category:", cat_input)
        layout.addRow("Amount:", amount_input)
        layout.addRow("Type:", type_input)
        layout.addRow("Date:", date_input)

        btn = QtW.QPushButton("Save")
        layout.addWidget(btn)

        def save_transaction():
            if mode == "add":
                add_transaction(
                    desc_input.text(),
                    cat_input.currentText(),
                    amount_input.value(),
                    type_input.currentText(),
                    date_input.date().toString("yyyy-MM-dd")
                )
            else:
                update_transaction(
                    tx_id,
                    description=desc_input.text(),
                    category=cat_input.currentText(),
                    amount=amount_input.value(),
                    transaction_type=type_input.currentText(),
                    date=date_input.date().toString("yyyy-MM-dd")
                )
            dialog.accept()
            self.load_transactions()
            self.load_categories()
            self.update_revenue_chart()

        btn.clicked.connect(save_transaction)
        dialog.exec()

    def delete_selected_transaction(self):
        selected = self.tx_table.currentRow()
        if selected >= 0:
            tx_id = int(self.tx_table.item(selected, 0).text())
            delete_transaction(tx_id)
            self.load_transactions()
            self.update_revenue_chart()

    def setup_categories_tab(self):
        layout = QtW.QVBoxLayout()
        self.categories_tab.setLayout(layout)

        self.cat_table = QtW.QTableWidget()
        layout.addWidget(self.cat_table)

        btn_layout = QtW.QHBoxLayout()
        layout.addLayout(btn_layout)

        refresh_btn = QtW.QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_categories)
        btn_layout.addWidget(refresh_btn)

        add_btn = QtW.QPushButton("Add Category")
        add_btn.clicked.connect(self.show_add_category_form)
        btn_layout.addWidget(add_btn)

        del_btn = QtW.QPushButton("Delete Category")
        del_btn.clicked.connect(self.delete_selected_category)
        btn_layout.addWidget(del_btn)

        self.load_categories()

    def load_categories(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
    
        # Query to get category totals
        cursor.execute("""
            SELECT c.id, c.name,
                IFNULL(SUM(CASE WHEN t.type='income' THEN t.amount END), 0) AS total_income,
               IFNULL(SUM(CASE WHEN t.type='expense' THEN t.amount END), 0) AS total_expense
            FROM catagories c
            LEFT JOIN transactions t ON c.name = t.category
            GROUP BY c.id, c.name
        """)
    
        rows = cursor.fetchall()
        conn.close()

        self.cat_table.setRowCount(len(rows))
        self.cat_table.setColumnCount(4)
        self.cat_table.setHorizontalHeaderLabels(["ID", "Name", "Total Income", "Total Expenses"])

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                if col_index in [2, 3]:  # Format totals as currency
                    self.cat_table.setItem(row_index, col_index, QtW.QTableWidgetItem(f"${value:.2f}"))
                else:
                    self.cat_table.setItem(row_index, col_index, QtW.QTableWidgetItem(str(value)))

        self.cat_table.resizeColumnsToContents()

    def show_add_category_form(self):
        text, ok = QtW.QInputDialog.getText(self, "Add Category", "Category name:")
        if ok and text:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO catagories (name) VALUES (?)", (text,))
                conn.commit()
            except sqlite3.IntegrityError:
                QtW.QMessageBox.warning(self, "Error", "Category already exists.")
            conn.close()
            self.load_categories()

    def delete_selected_category(self):
        selected = self.cat_table.currentRow()
        if selected >= 0:
            cat_id = int(self.cat_table.item(selected, 0).text())
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM catagories WHERE id = ?", (cat_id,))
            conn.commit()
            conn.close()
            self.load_categories()

    def setup_revenue_tab(self):
        layout = QtW.QVBoxLayout()
        self.revenue_tab.setLayout(layout)

        self.income_label = QtW.QLabel()
        self.expense_label = QtW.QLabel()
        self.revenue_label = QtW.QLabel()
        layout.addWidget(self.income_label)
        layout.addWidget(self.expense_label)
        layout.addWidget(self.revenue_label)

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.update_revenue_chart()

    def update_revenue_chart(self):
        total_income = income()
        total_expenses = expenses()
        total_revenue = get_revenue()

        self.income_label.setText(f"Total Income: ${total_income:.2f}")
        self.expense_label.setText(f"Total Expenses: ${total_expenses:.2f}")
        self.revenue_label.setText(f"Total Revenue: ${total_revenue:.2f}")

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(["Income", "Expenses"], [total_income, total_expenses], color=["green", "red"])
        ax.set_title("Income vs Expenses")
        self.canvas.draw()


if __name__ == "__main__":
    app = QtW.QApplication(sys.argv)
    window = AccountingApp()
    window.show()
    sys.exit(app.exec())
