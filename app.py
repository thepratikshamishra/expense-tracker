from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("test.db")
    return conn

@app.route("/")
@app.route("/")
def home():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Expense")
    expenses = cursor.fetchall()
    
    cursor.execute("SELECT SUM(Amount) FROM Expense")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT Category, SUM(Amount) FROM Expense GROUP BY Category")
    category_summary = cursor.fetchall()
    
    conn.close()
    
    return render_template("index.html", expenses=expenses, total=total, category_summary=category_summary)
@app.route("/add", methods=["POST"])
def add():
    spend_on = request.form["spend_on"]
    amount = request.form["amount"]
    category = request.form["category"]
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Expense(Spend_On, Amount, Category) VALUES(?, ?, ?)",
                   (spend_on, amount, category))
    conn.commit()
    conn.close()
    
    return redirect("/")
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Expense WHERE Serial_number = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)