import sqlite3

class DBManager:
    def __init__(self, db_name="expense_tracker.db"):
        self.db_name = db_name
        self.create_db()

    def create_db(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")


       # cursor.execute("DROP TABLE IF EXISTS user")

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                surname TEXT NOT NULL
                );
        """)

        cursor.execute("""
                 CREATE TABLE IF NOT EXISTS category (
                 category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL UNIQUE
                 );
        """)

        cursor.execute("""
                 CREATE TABLE IF NOT EXISTS expense (
                 expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL,
                 description TEXT NOT NULL,
                 date TEXT NOT NULL,
                 amount REAL NOT NULL,  
                 FOREIGN KEY (user_id) REFERENCES user(id) 
                 ON UPDATE CASCADE ON DELETE CASCADE
                 );
        """)

        cursor.execute("""
                 CREATE TABLE IF NOT EXISTS expense_category (
                 expense_id INTEGER NOT NULL,
                 category_id INTEGER NOT NULL,
                 PRIMARY KEY (expense_id, category_id),
                 FOREIGN KEY (expense_id) REFERENCES expense(expense_id) 
                 ON UPDATE CASCADE ON DELETE CASCADE,
                 FOREIGN KEY (category_id) REFERENCES category(category_id) 
                 ON UPDATE CASCADE ON DELETE CASCADE
                );
        """)

        connection.commit()
        connection.close()

    def signup_user(self, username, pass_hash, user_email, user_first_name, user_last_name):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "SELECT * FROM user WHERE username = ?"
        data = (username,)
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result is None:
            query = "INSERT INTO user (username, password_hash, email, first_name, surname) VALUES (?, ?, ?, ?, ?)"
            data = (username, pass_hash, user_email, user_first_name, user_last_name)
            cursor.execute(query, data)
            connection.commit()
            query = "SELECT id FROM user WHERE username = ?"
            data = (username,)
            cursor.execute(query, data)
            result = cursor.fetchone()
            connection.close()
            return "Success", result[0], user_first_name
        else:
            print("username already exists")
            connection.close()
            return "Failed"

    def login_user(self, username):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "SELECT * FROM user WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        connection.close()
        return result

    def get_user(self, username):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "SELECT password_hash FROM user WHERE username = ?"
        data = (username,)
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result:
            connection.close()
            return result[0]
        else:
            connection.close()
            return None

    def get_expenses(self, user_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "SELECT expense.description, expense.date, expense.amount, category.name FROM category JOIN expense_category ON category.category_id = expense_category.category_id JOIN expense ON expense.expense_id = expense_category.expense_id WHERE expense.user_id = ?"
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        connection.close()
        return result


    def add_expense(self, user_id, description, date, amount, category):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "INSERT INTO expense (user_id, description, date, amount) VALUES (?, ?, ?, ?)"
        data = (user_id, description, date, amount)
        cursor.execute(query, data)
        connection.commit()
        expense_id = cursor.lastrowid
        query = "SELECT category_id FROM category WHERE name = ?"
        data = (category,)
        cursor.execute(query, data)
        result = cursor.fetchone()
        if result is None:
            query = "INSERT INTO category (name) VALUES (?)"
            data = (category,)
            cursor.execute(query, data)
            connection.commit()
            category_id = cursor.lastrowid
            connection.close()
            return expense_id, category_id
        else:
            connection.close()
            return expense_id, result[0]

    def add_expense_category(self, expense_id, category_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "INSERT INTO expense_category (expense_id, category_id) VALUES (?, ?)"
        data = (expense_id, category_id)
        cursor.execute(query, data)
        connection.commit()
        connection.close()

    def get_expenses_by_category(self, user_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "SELECT category.name, SUM(expense.amount) FROM category JOIN expense_category ON category.category_id = expense_category.category_id JOIN expense ON expense.expense_id = expense_category.expense_id WHERE expense.user_id = ? GROUP BY category.name"
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        connection.close()
        return result


    def get_yearly_expenses(self, user_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "SELECT strftime('%Y', date), SUM(amount) FROM expense WHERE user_id = ? GROUP BY strftime('%Y', date)"
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        connection.close()
        return result

    def get_monthly_expenses(self, user_id, year):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "SELECT strftime('%m', date), SUM(amount) FROM expense WHERE user_id = ? AND strftime('%Y', date) = ?  GROUP BY strftime('%m', date)"
        data = (user_id, year)
        cursor.execute(query, data)
        result = cursor.fetchall()
        connection.close()
        return result

    def get_years(self, user_id):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        query = "SELECT DISTINCT strftime('%Y', date) FROM expense WHERE user_id = ? ORDER BY strftime('%Y', date)"
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchall()
        connection.close()
        return result