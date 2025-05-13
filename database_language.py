import sqlite3

DB_NAME = "coin_history.db"

def init_settings():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_language(lang):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""REPLACE INTO settings (key, value) VALUES (?, ?)""", ('language', lang))
    conn.commit()
    conn.close()

def load_language():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT value FROM settings WHERE key = 'language'""")
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'Türkçe'
