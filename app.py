from flask import Flask, render_template, request, session, redirect, jsonify
from db import DBManager
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.getenv("MY_KEY")
db = DBManager()


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = db.get_user(username)

        if hashed_password is not None:
            is_valid = bcrypt.check_password_hash(hashed_password,password)
            if is_valid:
                result = db.login_user(username)
                session['user_id'] = result[0]
                session['first_name'] = result[4]
                return redirect('/user_home')
            else:
                return render_template("login.html", result = "fail")
        else:
            return render_template("login.html", result="fail")
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        email = request.form['email']
        first_name = request.form['firstName']
        surname = request.form['surname']
        result = db.signup_user(username, hashed_password, email, first_name, surname)
        if result[0] == "Success":
            session['user_id'] = result[1]
            session['first_name'] = result[2]
            return redirect('/user_home')
        else:
            return render_template("signup.html", result = "fail")
    return render_template("signup.html")

@app.route('/user_home')
def user_home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template("user_home.html")

@app.route('/user_home/expenses', methods=['GET', 'POST'])
def expenses():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        description = request.form['description']
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        add = db.add_expense(session['user_id'],description, date, amount, category)
        db.add_expense_category(add[0], add[1])
    result_expenses = db.get_expenses(session['user_id'])
    return render_template("expenses.html", result_expenses = result_expenses)

@app.route("/user_home/statistics")
def statistics():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template("charts.html")

@app.route("/user_home/charts")
def category_chart():
    if 'user_id' not in session:
        return redirect('/login')
    result = db.get_expenses_by_category(session['user_id'])
    return jsonify(result)

@app.route("/user_home/charts_yearly")
def yearly_chart():
    if 'user_id' not in session:
        return redirect('/login')
    result = db.get_yearly_expenses(session['user_id'])
    return jsonify(result)

@app.route("/user_home/charts_monthly")
def monthly_chart():
    if 'user_id' not in session:
        return redirect('/login')
    year = request.args.get('year')
    result = db.get_monthly_expenses(session['user_id'], year)
    return jsonify(result)

@app.route("/user_home/years")
def get_years():
    if 'user_id' not in session:
        return redirect('/login')
    result = db.get_years(session['user_id'])
    return jsonify(result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run()