import tkinter as tk
import sqlite3
import json
from database_language import load_language
from database import DB_NAME

def show_coin_details_from_db(coin_id):
    # Dil dosyasını yükle
    with open("lang.json", "r", encoding="utf-8") as f:
        LANG_DATA = json.load(f)

    LANG = load_language()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT coin_name, symbol, price, change_24h, market_cap, timestamp
        FROM history
        WHERE coin_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (coin_id,))
    result = c.fetchone()
    conn.close()

    def go_back():
        window.destroy()
        import app
        app.launch()

    if not result:
        return

    coin_name, symbol, price, change, cap, timestamp = result

    window = tk.Tk()
    window.title("Coin Details")
    window.geometry("400x350")

    tk.Label(window, text=LANG_DATA[LANG].get("db_title", "Veritabanından Coin Bilgisi"), font=("Arial", 14, "bold")).pack(pady=10)

    info_text = (
        f"Coin: {coin_name} ({symbol.upper()})\n"
        f"{LANG_DATA[LANG].get('price_label', 'Fiyat')}: ${price:.2f}\n"
        f"{LANG_DATA[LANG].get('change_label', '24s Değişim')}: %{change:.2f}\n"
        f"{LANG_DATA[LANG].get('cap_label', 'Market Cap')}: ${cap:,.0f}\n"
        f"{LANG_DATA[LANG].get('time_label', 'Zaman')}: {timestamp}"
    )

    tk.Label(window, text=info_text, font=("Arial", 11), justify="left").pack(pady=10, padx=20)

    # Geri butonu
    tk.Button(window, text=LANG_DATA[LANG].get("back_button", "◀ Geri"), font=("Arial", 10), command=go_back).pack(pady=10)

    window.mainloop()