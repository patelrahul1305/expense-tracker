import sqlite3
import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry

# Connect to SQLite database
conn = sqlite3.connect("expense.db")
curs = conn.cursor()

# Create expense table if it doesn't exist
curs.execute(
    """CREATE TABLE IF NOT EXISTS expense (id INTEGER PRIMARY KEY, date TEXT, category TEXT, amount REAL)"""
)
conn.commit()


# Function to add an expense
def add_expense():
    # Get input values from entry fields
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    # Clear entry fields
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    # Insert expense into the database
    curs.execute(
        """INSERT INTO expense (date, category, amount) VALUES (?, ?, ?)""",
        (date, category, amount),
    )
    conn.commit()

    # Update the expense tree view and total expense label
    view()
    update_total_expense()


# Function to view expenses
def view():
    # Clear existing data in the expense tree view
    expense_tree.delete(*expense_tree.get_children())

    # Fetch all expenses from the database
    curs.execute("""SELECT * FROM expense""")
    all_expenses = curs.fetchall()

    # Insert expenses into the expense tree view
    for expense in all_expenses:
        expense_tree.insert(
            "", "end", values=(expense[0], expense[1], expense[2], expense[3])
        )


# Function to update total expense label
def update_total_expense():
    # Fetch total expense from the database
    curs.execute("""SELECT SUM(amount) FROM expense""")
    total_expense = curs.fetchone()[0]
    if not total_expense:
        total_expense = 0

    # Update total expense label
    total_expense_label.config(text="Total Expense: ₹ {:.2f}".format(total_expense))


# Function to delete selected expense
def delete_expense():
    # Get selected expense from the expense tree view
    selected_item = expense_tree.focus()
    if selected_item:
        item_values = expense_tree.item(selected_item)["values"]
        expense_id = item_values[0]

        # Delete expense from the database
        curs.execute("""DELETE FROM expense WHERE id=?""", (expense_id,))
        conn.commit()

        # Update the expense tree view and total expense label
        view()
        update_total_expense()


# Create main window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entry fields for date, category, and amount
date_label = tk.Label(root, text="Date")
date_label.grid(row=0, column=0, sticky="w")

date_entry = DateEntry(root)
date_entry.grid(row=0, column=1, sticky="w")

category_label = tk.Label(root, text="Category")
category_label.grid(row=1, column=0, sticky="w")

category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, sticky="w")

amount_label = tk.Label(root, text="Amount")
amount_label.grid(row=2, column=0, sticky="w")

amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, sticky="w")

# Create "Add Expense" button
add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=3, column=1, sticky="w")

# Create expense tree view
expenses = ["Id", "Date", "Category", "Amount"]
expense_tree = ttk.Treeview(root, column=expenses, show="headings")
for i in expenses:
    expense_tree.heading(i, text=i.upper())
view()
expense_tree.grid(row=4, column=0, sticky="w", columnspan=3)

# Create total expense label
total_expense_label = tk.Label(root, text="Total Expense: ₹ 0.00")
total_expense_label.grid(row=5, column=0, columnspan=3)

# Update total expense label
update_total_expense()

# Delete button
delete_button = ttk.Button(root, text="Delete", command=delete_expense)
delete_button.grid(row=5, column=0, padx=5, pady=5)

# Close the SQLite database connection when main window is closed
root.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), root.destroy()))

# Start main event loop
root.mainloop()

# Close the SQLite database connection when main loop exits
conn.close()
