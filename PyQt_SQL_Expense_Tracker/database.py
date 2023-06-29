from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox
import sys


# Create a connection to the database
database = QSqlDatabase.addDatabase('QSQLITE')
database.setDatabaseName('database.db')
if not database.open():
    QMessageBox.critical(None, 'Error', 'Could not open the database.')
    sys.exit(1)

# Create the expense table if it doesn't exist
query = QSqlQuery()
query.exec_("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
""")
