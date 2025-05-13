import tkinter as tk
from tkinter import ttk
import threading
import json
import sqlite3
from api_handler import search_coins, get_coin_details
from gui import show_gui
from database import init_db, save_coin_to_history
from database_language import init_settings, save_language, load_language
from history import show_history

with open("lang.json", "r", encoding="utf-8") as f:
    LANG_DATA = json.load(f)

def launch():
    init_db()
    init_settings()
    LANG = load_language()

    def change_language(value):
        nonlocal LANG
        LANG = value
        save_language(LANG)
        update_labels()

    def update_labels():
        search_label.config(text=LANG_DATA[LANG]["search_label"])
        lang_label.config(text=LANG_DATA[LANG]["language_label"])
        history_button.config(text=LANG_DATA[LANG]["history_button"])
        exit_button.config(text=LANG_DATA[LANG]["exit_button"])

    def on_keyrelease(event):
        query = search_var.get()
        if len(query) < 2:
            listbox.delete(0, tk.END)
            return

        def search():
            results = search_coins(query)
            coin_list.clear()
            listbox.delete(0, tk.END)
            for coin in results:
                coin_list.append(coin["id"])
                listbox.insert(tk.END, f"{coin['name']} ({coin['symbol'].upper()})")

        threading.Thread(target=search).start()

    def on_select(event):
        index = listbox.curselection()
        if index:
            selected_id = coin_list[index[0]]
            data = get_coin_details(selected_id)
            if data:
                name = data["name"]
                symbol = data["symbol"]
                price = data["market_data"]["current_price"]["usd"]
                change = data["market_data"]["price_change_percentage_24h"]
                cap = data["market_data"]["market_cap"]["usd"]
                save_coin_to_history(selected_id, name, symbol, price, change, cap)
            root.destroy()
            show_gui(selected_id)

    def show_history_ui():
        root.destroy()
        show_history()

    def quit_app():
        root.destroy()

    root = tk.Tk()
    root.title("Kripto Coin Uygulaması")
    root.geometry("600x400")

    top_frame = tk.Frame(root)
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    lang_label = tk.Label(top_frame, text="")
    lang_label.pack(side=tk.RIGHT)
    lang_var = tk.StringVar(value=LANG)
    lang_menu = ttk.OptionMenu(top_frame, lang_var, LANG, *LANG_DATA.keys(), command=change_language)
    lang_menu.pack(side=tk.RIGHT, padx=5)

    search_label = tk.Label(top_frame, text="", font=("Arial", 12))
    search_label.pack(side=tk.LEFT)
    search_var = tk.StringVar()
    search_entry = tk.Entry(top_frame, textvariable=search_var, font=("Arial", 12))
    search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    search_entry.bind("<KeyRelease>", on_keyrelease)

    middle_frame = tk.Frame(root)
    middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    listbox = tk.Listbox(middle_frame, height=5, font=("Arial", 11))
    listbox.pack(fill=tk.X)
    listbox.bind("<<ListboxSelect>>", on_select)

    coin_list = []

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(pady=10)

    history_button = tk.Button(bottom_frame, text="", width=12, command=show_history_ui)
    history_button.pack(side=tk.LEFT, padx=10)

    exit_button = tk.Button(bottom_frame, text="", width=12, command=quit_app)
    exit_button.pack(side=tk.LEFT, padx=10)

    update_labels()
    root.mainloop()

if __name__ == "__main__":
    launch()
