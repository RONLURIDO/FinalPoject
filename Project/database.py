import sqlite3

def create_tables():
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS aid_records
                      (beneficiary_id TEXT PRIMARY KEY, item TEXT, location TEXT, beneficiary TEXT, quantity INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS beneficiaries
                      (beneficiary_id TEXT PRIMARY KEY, name TEXT, location TEXT, contact TEXT)''')
    conn.commit()
    conn.close()

def fetch_aid_records():
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM aid_records')
    aid_records = cursor.fetchall()
    conn.close()
    return aid_records

def fetch_beneficiaries():
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM beneficiaries')
    beneficiaries = cursor.fetchall()
    conn.close()
    return beneficiaries

def insert_aid_record(beneficiary_id, item, location, beneficiary, quantity):
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO aid_records (beneficiary_id, item, location, beneficiary, quantity) VALUES (?, ?, ?, ?, ?)',
                   (beneficiary_id, item, location, beneficiary, quantity))
    conn.commit()
    conn.close()

def insert_beneficiary(beneficiary_id, name, location, contact):
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO beneficiaries (beneficiary_id, name, location, contact) VALUES (?, ?, ?, ?)',
                   (beneficiary_id, name, location, contact))
    conn.commit()
    conn.close()

def delete_aid_record(id):
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM aid_records WHERE beneficiary_id=?', (id,))
    conn.commit()
    conn.close()

def delete_beneficiary(beneficiary_id):
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM beneficiaries WHERE beneficiary_id=?', (beneficiary_id,))
    conn.commit()
    conn.close()

def update_aid_record(id, new_beneficiary_id, new_item, new_location, new_beneficiary, new_quantity):
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE aid_records SET beneficiary_id=?, item=?, location=?, beneficiary=?, quantity=? WHERE beneficiary_id=?",
                   (new_beneficiary_id, new_item, new_location, new_beneficiary, new_quantity, id))
    conn.commit()
    conn.close()

def update_beneficiary(beneficiary_id, new_name, new_location, new_contact):
    conn = sqlite3.connect('relief_aid.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE beneficiaries SET name=?, location=?, contact=? WHERE beneficiary_id=?",
                   (new_name, new_location, new_contact, beneficiary_id))
    conn.commit()
    conn.close()

create_tables()