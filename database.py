import sqlite3
from datetime import datetime

DB_NAME = "coin_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin_id TEXT NOT NULL,
            coin_name TEXT,
            symbol TEXT,
            price REAL,
            change_24h REAL,
            market_cap REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_coin_to_history(coin_id, name, symbol, price, change_24h, market_cap):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO history (coin_id, coin_name, symbol, price, change_24h, market_cap, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (coin_id, name, symbol, price, change_24h, market_cap, timestamp))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT coin_name, symbol, price, timestamp, coin_id, change_24h, market_cap
        FROM history
        ORDER BY id DESC
        LIMIT 50
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def delete_history_by_coin_id(coin_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE coin_id = ?", (coin_id,))
    conn.commit()
    conn.close()