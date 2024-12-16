import tkinter as tk
from tkinter import messagebox
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin123",
    database="bank_mangement"
)
print(connection)

cursor = connection.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    balance FLOAT DEFAULT 0.0
)
''')
connection.commit()

# Functions
def create_account_window():
    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            messagebox.showinfo("Success", "Account created successfully.")
            create_account_win.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"{err}")

    create_account_win = tk.Toplevel(root)
    create_account_win.title("Create Account")
    create_account_win.configure(bg="#F7DC6F")

    tk.Label(create_account_win, text="Username:", bg="#F7DC6F").pack(pady=5)
    username_entry = tk.Entry(create_account_win)
    username_entry.pack(pady=5)
    tk.Label(create_account_win, text="Password:", bg="#F7DC6F").pack(pady=5)
    password_entry = tk.Entry(create_account_win, show="*")
    password_entry.pack(pady=5)
    tk.Button(create_account_win, text="Create Account", bg="#2ECC71", fg="white", command=create_account).pack(pady=10)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "All fields are required.")
        return
    cursor.execute("SELECT id, balance FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        user_id, balance = user
        dashboard(user_id, username, balance)
    else:
        messagebox.showerror("Error", "Invalid credentials.")

def dashboard(user_id, username, balance):
    def deposit():
        amount = float(amount_entry.get())
        cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
        connection.commit()
        update_balance()
        messagebox.showinfo("Success", "Amount deposited successfully.")

    def withdraw():
        amount = float(amount_entry.get())
        cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
        current_balance = cursor.fetchone()[0]
        if amount > current_balance:
            messagebox.showerror("Error", "Insufficient balance.")
        else:
            cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, user_id))
            connection.commit()
            update_balance()
            messagebox.showinfo("Success", "Amount withdrawn successfully.")

    def update_balance():
        cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
        new_balance = cursor.fetchone()[0]
        balance_label.config(text=f"Balance: ${new_balance:.2f}")

    def delete_account():
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your account?")
        if confirmation:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            dashboard_win.destroy()
            messagebox.showinfo("Account Deleted", "Your account has been deleted successfully.")

    dashboard_win = tk.Toplevel(root)
    dashboard_win.title(f"Welcome {username}")
    dashboard_win.configure(bg="#AED6F1")

    balance_label = tk.Label(dashboard_win, text=f"Balance: ${balance:.2f}", bg="#AED6F1", font=("Arial", 12, "bold"))
    balance_label.pack(pady=10)

    tk.Label(dashboard_win, text="Amount:", bg="#AED6F1").pack(pady=5)
    amount_entry = tk.Entry(dashboard_win)
    amount_entry.pack(pady=5)

    tk.Button(dashboard_win, text="Deposit", bg="#2ECC71", fg="white", command=deposit).pack(pady=5)
    tk.Button(dashboard_win, text="Withdraw", bg="#F39C12", fg="white", command=withdraw).pack(pady=5)
    tk.Button(dashboard_win, text="Delete Account", bg="#E74C3C", fg="white", command=delete_account).pack(pady=5)

# GUI setup
root = tk.Tk()
root.title("Bank Management System")
root.configure(bg="#D5DBDB")

tk.Label(root, text="Bank Management System", font=("Arial", 16, "bold"), bg="#D5DBDB").pack(pady=10)
tk.Label(root, text="Username:", bg="#D5DBDB").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

tk.Label(root, text="Password:", bg="#D5DBDB").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

tk.Button(root, text="Login", bg="#3498DB", fg="white", command=login).pack(pady=10)
tk.Button(root, text="Create Account", bg="#1ABC9C", fg="white", command=create_account_window).pack(pady=5)

root.mainloop()

# Close the database connection
connection.close()
