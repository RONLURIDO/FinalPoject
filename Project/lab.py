import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import sqlite3

app = customtkinter.CTk()
app.title('Disaster Relief Aid Management System')
app.geometry('1300x420')
app.config(bg='#161C25')
app.resizable(FALSE, FALSE)

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 12, 'bold')

# Connect to the database
conn = sqlite3.connect('relief_aid.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS aid_records
             (beneficiary_id TEXT PRIMARY KEY, item TEXT, location TEXT, beneficiary TEXT, quantity INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS beneficiaries
             (beneficiary_id TEXT PRIMARY KEY, name TEXT, location TEXT, contact TEXT)''')

def add_to_treeview():
    aid_records = fetch_aid_records()
    tree.delete(*tree.get_children())
    for record in aid_records:
        print(record)
        tree.insert('', END, values=record)

def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    beneficiary_id_entry.delete(0, END)
    item_entry.delete(0, END)
    location_entry.delete(0, END)
    beneficiary_entry.delete(0, END)
    quantity_entry.delete(0, END)

def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        beneficiary_id_entry.insert(0, row[0])
        item_entry.insert(0, row[1])
        location_entry.insert(0, row[2])
        beneficiary_entry.insert(0, row[3])
        quantity_entry.insert(0, row[4])
    else:
        pass

def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('ERROR', 'Choose a record to delete.')
    else:
        record_id = tree.item(selected_item)['values'][0]
        delete_record(record_id)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Record has been deleted')

def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Select a record to update')
    else:
        record_id = tree.item(selected_item)['values'][0]
        beneficiary_id = beneficiary_id_entry.get()
        item = item_entry.get()
        location = location_entry.get()
        beneficiary = beneficiary_entry.get()
        quantity = quantity_entry.get()
        update_record(record_id, beneficiary_id, item, location, beneficiary, quantity)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Record has been updated')

def insert():
    beneficiary_id = beneficiary_id_entry.get()
    item = item_entry.get()
    location = location_entry.get()
    beneficiary = beneficiary_entry.get()
    quantity = quantity_entry.get()
    if not (beneficiary_id and item and location and beneficiary and quantity):
        messagebox.showerror('Error', 'Please enter all required fields.')
    else:
        insert_record(beneficiary_id, item, location, beneficiary, quantity)
        add_to_treeview()
        messagebox.showinfo('Success', 'Record has been inserted.')

def fetch_aid_records():
    c.execute("SELECT * FROM aid_records")
    return c.fetchall()

def delete_record(record_id):
    c.execute("DELETE FROM aid_records WHERE beneficiary_id=?", (record_id,))
    conn.commit()

def update_record(record_id, beneficiary_id, item, location, beneficiary, quantity):
    c.execute("UPDATE aid_records SET beneficiary_id=?, item=?, location=?, beneficiary=?, quantity=? WHERE beneficiary_id=?",
              (beneficiary_id, item, location, beneficiary, quantity, record_id))
    conn.commit()

def insert_record(beneficiary_id, item, location, beneficiary, quantity):
    c.execute("INSERT INTO aid_records (beneficiary_id, item, location, beneficiary, quantity) VALUES (?, ?, ?, ?, ?)",
              (beneficiary_id, item, location, beneficiary, quantity))
    conn.commit()

# Create UI elements for input fields, buttons, and treeview
beneficiary_id_label = customtkinter.CTkLabel(app, font=font1, text='Beneficiary ID:', text_color='#fff', bg_color='#161C25')
beneficiary_id_label.place(x=20, y=30)

beneficiary_id_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
beneficiary_id_entry.place(x=200, y=20)

item_label = customtkinter.CTkLabel(app, font=font1, text='Item:', text_color='#fff', bg_color='#161C25')
item_label.place(x=20, y=80)

item_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
item_entry.place(x=200, y=80)

location_label = customtkinter.CTkLabel(app, font=font1, text='Location:', text_color='#fff', bg_color='#161C25')
location_label.place(x=20, y=130)

location_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
location_entry.place(x=200, y=130)

beneficiary_label = customtkinter.CTkLabel(app, font=font1, text='Beneficiary:', text_color='#fff', bg_color='#161C25')
beneficiary_label.place(x=20, y=180)

beneficiary_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
beneficiary_entry.place(x=200, y=180)

quantity_label = customtkinter.CTkLabel(app, font=font1, text='Quantity:', text_color='#fff', bg_color='#161C25')
quantity_label.place(x=20, y=230)

quantity_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
quantity_entry.place(x=200, y=230)

add_button = customtkinter.CTkButton(app, command=insert, font=font1, text_color='#fff', text='Add Record', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=15, width=260)
add_button.place(x=20, y=310)

clear_button = customtkinter.CTkButton(app, command=lambda: clear(True), font=font1, text_color='#fff', text='Clear', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=15, width=260)
clear_button.place(x=20, y=360)

update_button = customtkinter.CTkButton(app, command=update, font=font1, text_color='#fff', text='Update Record', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=15, width=260)
update_button.place(x=300, y=360)
delete_button = customtkinter.CTkButton(app, command=delete, font=font1, text_color='#fff', text='Delete Record', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=15, width=260)
delete_button.place(x=580, y=360)
style = ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
style.map('Treeview', background=[('selected', '#1A8F2D')])
tree = ttk.Treeview(app, height=15)
tree['columns'] = ('Beneficiary ID', 'Item', 'Location', 'Beneficiary', 'Quantity')
tree.column('#0', width=0, stretch=tk.NO)  # Hide the default first column
tree.column('Beneficiary ID', anchor=tk.CENTER, width=120)
tree.column('Item', anchor=tk.CENTER, width=200)
tree.column('Location', anchor=tk.CENTER, width=150)
tree.column('Beneficiary', anchor=tk.CENTER, width=150)
tree.column('Quantity', anchor=tk.CENTER, width=100)
tree.heading('Beneficiary ID', text='Beneficiary ID')
tree.heading('Item', text='Item')
tree.heading('Location', text='Location')
tree.heading('Beneficiary', text='Beneficiary')
tree.heading('Quantity', text='Quantity')
tree.place(x=400, y=20)
tree.bind('<ButtonRelease>', display_data)
add_to_treeview()
app.mainloop()
conn.close()