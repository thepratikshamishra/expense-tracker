import sqlite3
conn = sqlite3.connect("test.db") 
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Expense(
    serial_number INTEGER PRIMARY KEY AUTOINCREMENT ,
    spend_on TEXT,
    amount REAL,
    category TEXT,
    date TEXT DEFAULT CURRENT_DATE)
""")

while True:
    print("What do you want to do ?")
    print("1. Add Expense")
    print("2.  View All Expenses")
    print("3.  Exit")
    print("4. Want Summary")
    
    choice = input("Enter choice: ")
    
    if choice == "1":
        spend_on = input("What did you spend on?  ")
        amount = float(input("How Much you spend?  "))
        category = input ("Category??  ") 
        cursor.execute("INSERT INTO Expense(spend_on, amount, category) VALUES(?, ?, ?)",
                (spend_on, amount, category))
        conn.commit()
         
        print("Expense added successfully!") 
        
    elif choice == "2":
      
       cursor.execute("SELECT * FROM Expense")
       row = cursor.fetchall()
       for r in row:
          print(f"| {r[0]:<3} | {r[1]:<10} | {r[2]:<8} | {r[3]:<10} | {r[4]:<12} |")
       

    elif choice == "3":
        break

    elif choice == "4":
        cursor.execute("SELECT SUM(amount) FROM Expense")
        result = cursor.fetchone()
        print(f"Total Spent: {result[0]}")
     
    else:
        print("Invalid choice!")


conn.close()
print("Table is creted")  
 

