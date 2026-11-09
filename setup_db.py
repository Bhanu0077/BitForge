import sqlite3
import os

db_path = 'database/bitforge.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Users Table (Goal 1 & 2)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    secret_question TEXT NOT NULL,
    secret_answer TEXT NOT NULL,
    balance REAL DEFAULT 100.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Transactions Table (Goal 2 & 3)
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_email TEXT NOT NULL,
    receiver_email TEXT NOT NULL,
    amount REAL NOT NULL,
    timestamp TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
)
''')

# Blockchain Ledger Table (Goal 2)
cursor.execute('''
CREATE TABLE IF NOT EXISTS blockchain (
    block_index INTEGER PRIMARY KEY,
    previous_hash TEXT NOT NULL,
    current_hash TEXT NOT NULL,
    nonce INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    transactions_data TEXT NOT NULL
)
''')

# Seed Genesis Block if empty
cursor.execute('SELECT COUNT(*) FROM blockchain')
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO blockchain (block_index, previous_hash, current_hash, nonce, timestamp, transactions_data)
    VALUES (1, '0000000000000000000000000000000000000000000000000000000000000000', 
            '0000a1b2c3d4e5f6789012345678901234567890123456789012345678901234', 
            0, DATETIME('now'), 'Genesis Block')
    ''')

# Seed default test users if empty
cursor.execute('SELECT COUNT(*) FROM users')
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO users (email, password_hash, secret_question, secret_answer, balance)
    VALUES ('bhanu@bitforge.org', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'What is your favorite pet?', 'dog', 500.0)
    ''')
    cursor.execute('''
    INSERT INTO users (email, password_hash, secret_question, secret_answer, balance)
    VALUES ('satoshi@bitforge.org', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'What is your favorite pet?', 'dog', 1000.0)
    ''')

conn.commit()
conn.close()
print("Database schema created and seeded successfully at database/bitforge.db")
