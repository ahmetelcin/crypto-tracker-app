import tkinter as tk
from tkinter import ttk, messagebox
import json
from database import get_history, delete_history_by_coin_id
from show_history import show_coin_details_from_db
from database_language import load_language

with open("lang.json", "r", encoding="utf-8") as f:
    LANG_DATA = json.load(f)

LANG = load_language()

def show_history():
    def load_history():
        tree.delete(*tree.get_children())
        history = get_history()
        for coin_name, symbol, price, timestamp, coin_id, change, cap in history:
            coin_display = f"{coin_name} ({symbol.upper()})"
            tree.insert("", tk.END, values=(coin_display, timestamp, coin_id))

    def open_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", LANG_DATA[LANG].get("select_warning", "Lütfen açmak için bir coin seçin."))
            return
        item = tree.item(selected[0])
        coin_id = item["values"][2]
        window.destroy()
        show_coin_details_from_db(coin_id)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Uyarı", LANG_DATA[LANG].get("delete_warning", "Lütfen silmek için bir coin seçin."))
            return
        item = tree.item(selected[0])
        coin_id = item["values"][2]

        if messagebox.askyesno("Onay", LANG_DATA[LANG].get("confirm_delete", "Bu kaydı silmek istediğinizden emin misiniz?")):
            delete_history_by_coin_id(coin_id)
            load_history()

    def go_back():
        window.destroy()
        import app
        app.launch()

    window = tk.Tk()
    window.title(LANG_DATA[LANG].get("history_title", "Geçmiş"))
    window.geometry("600x500")

    tk.Label(window, text=LANG_DATA[LANG].get("history_label", "Geçmişte Seçilen Coin'ler"), font=("Arial", 14, "bold")).pack(pady=10)

    columns = ("Coin", "Zaman", "ID")

    tree = ttk.Treeview(window, columns=columns, show="headings", selectmode="browse")
    tree.heading("Coin", text="Coin")
    tree.heading("Zaman", text="Zaman")
    tree.heading("ID", text="ID")
    tree.column("Coin", width=250)
    tree.column("Zaman", width=200)
    tree.column("ID", width=0, stretch=False)  # ID gizli

    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Butonlar
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text=LANG_DATA[LANG].get("back_button", "◀ Geri"), width=12, command=go_back).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text=LANG_DATA[LANG].get("delete_button", "🗑 Sil"), width=12, command=delete_selected).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text=LANG_DATA[LANG].get("open_button", "📂 Aç"), width=12, command=open_selected).pack(side=tk.LEFT, padx=10)

    load_history()
    window.mainloop()
