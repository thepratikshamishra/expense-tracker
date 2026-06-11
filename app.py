from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "expense_secret"


def get_db():   
    conn = sqlite3.connect("test.db")
    return conn


def create_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Expense(
        serial_number INTEGER PRIMARY KEY AUTOINCREMENT,
        spend_on TEXT,
        amount REAL,
        category TEXT,
        date TEXT DEFAULT CURRENT_DATE
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Expense ORDER BY serial_number DESC")
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM Expense")
    total = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM Expense
        GROUP BY category
    """)
    category_summary = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_summary=category_summary
    )


@app.route("/add", methods=["POST"])
def add():
    spend_on = request.form["spend_on"]
    amount = request.form["amount"]
    category = request.form["category"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Expense(spend_on, amount, category) VALUES (?, ?, ?)",
        (spend_on, amount, category)
    )

    conn.commit()

    flash("✅ Expense Added Successfully!")

    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Expense WHERE serial_number = ?",
        (id,)
    )

    conn.commit()

    flash("🗑️ Expense Deleted Successfully!")

    conn.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
