import tkinter as tk
from tkinter import messagebox, ttk, END
import mysql.connector

# Database connection function
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sneha25",
        database="library_management"
    )

# Main application class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Library Management System")
        self.root.geometry("600x500")

        # Setting up tab navigation
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=1, fill="both")

        # Create Tabs
        self.create_books_tab()
        self.create_members_tab()
        self.create_transactions_tab()

    def create_books_tab(self):
        books_tab = ttk.Frame(self.tabs)
        self.tabs.add(books_tab, text="Books")

        # Book Form
        ttk.Label(books_tab, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_entry = ttk.Entry(books_tab)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(books_tab, text="Author:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.author_entry = ttk.Entry(books_tab)
        self.author_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(books_tab, text="Year:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.year_entry = ttk.Entry(books_tab)
        self.year_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(books_tab, text="Copies:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.copies_entry = ttk.Entry(books_tab)
        self.copies_entry.grid(row=3, column=1, padx=10, pady=10)

        # Add Book Button
        ttk.Button(books_tab, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Search bar
        ttk.Label(books_tab, text="Search by Title or Author:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.search_entry = ttk.Entry(books_tab)
        self.search_entry.grid(row=5, column=1, padx=10, pady=10)
        ttk.Button(books_tab, text="Search", command=self.search_books).grid(row=5, column=2, padx=10, pady=10)

        # Display Area
        self.books_display = tk.Text(books_tab, height=10, width=70)
        self.books_display.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def create_members_tab(self):
        members_tab = ttk.Frame(self.tabs)
        self.tabs.add(members_tab, text="Members")

        ttk.Label(members_tab, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.member_name_entry = ttk.Entry(members_tab)
        self.member_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(members_tab, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.member_email_entry = ttk.Entry(members_tab)
        self.member_email_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add Member Button
        ttk.Button(members_tab, text="Add Member", command=self.add_member).grid(row=2, column=0, columnspan=2, pady=10)

        # Remove Member Button
        ttk.Button(members_tab, text="Remove Member", command=self.remove_member).grid(row=3, column=0, columnspan=2, pady=10)

        # Member List Display
        self.members_display = tk.Text(members_tab, height=10, width=70)
        self.members_display.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Refresh member list on startup
        self.refresh_members_display()

    def create_transactions_tab(self):
        transactions_tab = ttk.Frame(self.tabs)
        self.tabs.add(transactions_tab, text="Transactions")

        ttk.Label(transactions_tab, text="Member ID:").grid(row=0, column=0, padx=10, pady=10)
        self.transaction_member_id_entry = ttk.Entry(transactions_tab)
        self.transaction_member_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(transactions_tab, text="Book ID:").grid(row=1, column=0, padx=10, pady=10)
        self.transaction_book_id_entry = ttk.Entry(transactions_tab)
        self.transaction_book_id_entry.grid(row=1, column=1, padx=10, pady=10)

        # Issue and Return Buttons
        ttk.Button(transactions_tab, text="Issue Book", command=self.issue_book).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(transactions_tab, text="Return Book", command=self.return_book).grid(row=2, column=1, padx=10, pady=10)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        copies = self.copies_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Books (title, author, year_published, copies_available) VALUES (%s, %s, %s, %s)",
                           (title, author, year, copies))
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully!")
            self.title_entry.delete(0, END)
            self.author_entry.delete(0, END)
            self.year_entry.delete(0, END)
            self.copies_entry.delete(0, END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error adding book: {err}")
        finally:
            cursor.close()
            conn.close()
            self.refresh_books_display()

    def search_books(self):
        search_term = self.search_entry.get()
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Books WHERE title LIKE %s OR author LIKE %s", (f'%{search_term}%', f'%{search_term}%'))
            books = cursor.fetchall()
            self.books_display.delete(1.0, END)
            for book in books:
                self.books_display.insert(END, f"{book}\n")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching books: {err}")
        finally:
            cursor.close()
            conn.close()

    def add_member(self):
        name = self.member_name_entry.get()
        email = self.member_email_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Members (name, email, join_date) VALUES (%s, %s, CURDATE())", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "Member added successfully!")
            self.member_name_entry.delete(0, END)
            self.member_email_entry.delete(0, END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error adding member: {err}")
        finally:
            cursor.close()
            conn.close()
            self.refresh_members_display()

    def remove_member(self):
        email = self.member_email_entry.get()  # Assuming we are using email to remove the member

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Members WHERE email = %s", (email,))
            conn.commit()
            messagebox.showinfo("Success", "Member removed successfully!")
            self.member_email_entry.delete(0, END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error removing member: {err}")
        finally:
            cursor.close()
            conn.close()
            self.refresh_members_display()

    def refresh_members_display(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Members")
            members = cursor.fetchall()
            self.members_display.delete(1.0, END)
            for member in members:
                self.members_display.insert(END, f"{member}\n")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching members: {err}")
        finally:
            cursor.close()
            conn.close()

    def issue_book(self):
        member_id = self.transaction_member_id_entry.get()
        book_id = self.transaction_book_id_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Transactions (member_id, book_id, issue_date) VALUES (%s, %s, CURDATE())", (member_id, book_id))
            conn.commit()
            messagebox.showinfo("Success", "Book issued successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error issuing book: {err}")
        finally:
            cursor.close()
            conn.close()

    def return_book(self):
        member_id = self.transaction_member_id_entry.get()
        book_id = self.transaction_book_id_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Transactions SET return_date = CURDATE() WHERE member_id = %s AND book_id = %s AND return_date IS NULL", (member_id, book_id))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error returning book: {err}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

