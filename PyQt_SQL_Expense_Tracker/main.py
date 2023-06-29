from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QDateEdit, QHBoxLayout
from PyQt5.QtCore import QDate
from database import *

class ExpenseTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Expense Tracker')
        self.resize(525,424)

        self.main_window = QWidget()
        self.master_layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        self.date_edit = QDateEdit()
        self.category_combo = QComboBox()
        self.amount_edit = QLineEdit()
        self.description_edit = QLineEdit()
        self.date_edit.setDate(QDate.currentDate())

        # 
        self.add_button = QPushButton('Add Expense')
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button = QPushButton('Delete Expense')
        self.delete_button.clicked.connect(self.delete_expense)
        # 
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(5)
        self.expense_table.setHorizontalHeaderLabels(['ID', 'Date', 'Category', 'Amount', 'Description'])
        categories = ['Food', 'Transportation', 'Shopping', 'Entertainment', 'Bills', 'Others']
        self.category_combo.addItems(categories)

        row1.addWidget(QLabel('Date:'))
        row1.addWidget(self.date_edit)
        row1.addWidget(QLabel('Category:'))
        row1.addWidget(self.category_combo)
        row2.addWidget(QLabel('Amount:'))
        row2.addWidget(self.amount_edit)
        row2.addWidget(QLabel('Description:'))
        row2.addWidget(self.description_edit)
        row3.addWidget(self.add_button)
        row3.addWidget(self.delete_button)
        # 
        self.master_layout.addLayout(row1)
        self.master_layout.addLayout(row2)
        self.master_layout.addLayout(row3)

        self.master_layout.addWidget(self.expense_table)
        self.main_window.setLayout(self.master_layout)
        self.setCentralWidget(self.main_window)
        self.show()

        self.load_expenses()


    def add_expense(self):
        date = self.date_edit.date().toString('yyyy-MM-dd')
        category = self.category_combo.currentText()
        amount = self.amount_edit.text()
        description = self.description_edit.text()

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        """)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        self.date_edit.setDate(QDate.currentDate())
        self.category_combo.setCurrentIndex(0)
        self.amount_edit.clear()
        self.description_edit.clear()

        self.load_expenses()
        
    def delete_expense(self):
        selected_row = self.expense_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'No Expense Selected', 'Please select an expense to delete.')
            return

        expense_id = int(self.expense_table.item(selected_row, 0).text())

        confirmation = QMessageBox.question(self, 'Confirm Deletion','Are you sure you want to delete this expense?', QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.No:
            return
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        query.exec_()

        self.load_expenses()

    def load_expenses(self):
        self.expense_table.setRowCount(0)

        query = QSqlQuery('SELECT * FROM expenses')
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)
            # 
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(self.delete_expense)

            self.expense_table.insertRow(row)
            self.expense_table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.expense_table.setItem(row, 1, QTableWidgetItem(date))
            self.expense_table.setItem(row, 2, QTableWidgetItem(category))
            self.expense_table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.expense_table.setItem(row, 4, QTableWidgetItem(description))
            self.expense_table.setCellWidget(row, 5, delete_button)

            row += 1


app = QApplication([])
window = ExpenseTrackerApp()
app.exec_()
