import tkinter as tk
from tkinter import ttk
from api_handler import get_coin_details
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
import requests
import datetime
import json
from database_language import load_language

with open("lang.json", "r", encoding="utf-8") as f:
    LANG_DATA = json.load(f)

LANG = load_language()

def get_market_chart(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return data["prices"]
    except Exception as e:
        print("Grafik verisi alınamadı:", e)
    return []

def show_gui(coin_id):
    def fetch_coin_data():
        data = get_coin_details(coin_id)
        if not data:
            return

        name = data["name"]
        symbol = data["symbol"].upper()
        market_data = data["market_data"]

        info = {
            LANG_DATA[LANG].get("coin", "Coin"): f"{name} ({symbol})",
            LANG_DATA[LANG].get("price_label", "Fiyat"): f"${market_data['current_price']['usd']:.2f}",
            LANG_DATA[LANG].get("change_label", "24s Değişim"): f"%{market_data['price_change_percentage_24h']:.2f}",
            LANG_DATA[LANG].get("cap_label", "Market Cap"): f"${market_data['market_cap']['usd']:,.0f}",
            LANG_DATA[LANG].get("volume", "Hacim"): f"${market_data['total_volume']['usd']:,.0f}",
            LANG_DATA[LANG].get("rank", "Piyasa Sıralaması"): f"#{data.get('market_cap_rank', 'N/A')}",
            LANG_DATA[LANG].get("ath", "ATH"): f"${market_data['ath']['usd']:.2f} ({market_data['ath_date']['usd'][:10]})",
            LANG_DATA[LANG].get("total_supply", "Toplam Arz"): f"{market_data.get('total_supply', 'Bilinmiyor')}",
            LANG_DATA[LANG].get("circulating_supply", "Dolaşımdaki Arz"): f"{market_data.get('circulating_supply', 'Bilinmiyor')}"
        }

        for label, value in info.items():
            row = tk.Frame(left_frame)
            row.pack(anchor="w", pady=2, padx=5, fill=tk.X)
            tk.Label(row, text=f"{label}:", font=("Arial", 11, "bold"), width=18, anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("Arial", 11), anchor="w").pack(side=tk.LEFT)

    def plot_chart(days):
        for widget in chart_frame.winfo_children():
            widget.destroy()
        prices = get_market_chart(coin_id, days)
        if not prices:
            return
        dates = [datetime.datetime.fromtimestamp(p[0]/1000).strftime('%d/%m') for p in prices]
        values = [p[1] for p in prices]

        fig, ax = plt.subplots(figsize=(5.5, 3), dpi=100)
        ax.plot(dates, values, linewidth=2)
        ax.set_title(LANG_DATA[LANG].get("price_chart_title", f"Son {days} Günlük Fiyat Değişimi"), fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=8))
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_period_change(event):
        selected = period_var.get()
        days = period_options[selected]
        plot_chart(days)

    def go_back():
        window.destroy()
        import app
        app.launch()

    window = tk.Tk()
    window.title(LANG_DATA[LANG].get("coin_details_title", "Coin Detayları"))
    window.geometry("920x520")
    window.resizable(False, False)

    left_frame = tk.Frame(window, width=320, bg="#f5f5f5", relief=tk.GROOVE, bd=2)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(left_frame, text=LANG_DATA[LANG].get("coin_info", "Coin Bilgileri"), font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

    right_frame = tk.Frame(window)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    top_controls = tk.Frame(right_frame)
    top_controls.pack(anchor="ne", fill=tk.X)

    period_options = {
        LANG_DATA[LANG].get("7_days", "7 Gün"): 7,
        LANG_DATA[LANG].get("1_month", "1 Ay"): 30,
        LANG_DATA[LANG].get("3_months", "3 Ay"): 90,
        LANG_DATA[LANG].get("6_months", "6 Ay"): 180,
        LANG_DATA[LANG].get("1_year", "1 Yıl"): 365
    }

    period_var = tk.StringVar(value=list(period_options.keys())[0])
    tk.Label(top_controls, text=LANG_DATA[LANG].get("time_range", "Zaman Aralığı:"), font=("Arial", 10)).pack(side=tk.LEFT)
    period_menu = ttk.Combobox(top_controls, textvariable=period_var, values=list(period_options.keys()), state="readonly", width=10)
    period_menu.pack(side=tk.LEFT, padx=5)
    period_menu.bind("<<ComboboxSelected>>", on_period_change)

    chart_frame = tk.Frame(right_frame)
    chart_frame.pack(fill=tk.BOTH, expand=True)

    back_button = tk.Button(right_frame, text=LANG_DATA[LANG].get("back_button", "◀ Geri"), font=("Arial", 10), command=go_back)
    back_button.pack(anchor="se", pady=10)

    threading.Thread(target=fetch_coin_data).start()
    plot_chart(7)

    window.mainloop()