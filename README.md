**Crypto Coin Tracker App - README**

This is a multilingual (Turkish and English) cryptocurrency tracking application built using the CoinGecko API and a Tkinter-based GUI. Users can view real-time coin data, inspect previously searched records, and analyze price trends through interactive graphs.

---

**1. Technologies Used**

* Python 3
* Tkinter (GUI)
* SQLite (local database)
* matplotlib (chart rendering)
* CoinGecko API (data source)
* JSON (language support)

---

**2. Application Features**

* Fetch real-time cryptocurrency data from CoinGecko
* Save selected coins to a local SQLite database
* Display and access details from search history
* Visualize price changes over time (7 days to 1 year)
* Dynamic multilingual interface (via `lang.json`)

---

**3. File Structure**

* `app.py`: Main application entry point
* `gui.py`: Displays selected coin details and price graph
* `database.py`: Manages the `history` table in SQLite
* `database_language.py`: Stores the selected language in the `settings` table
* `api_handler.py`: Manages all API communications
* `history.py`: Shows list of stored coin history
* `show_history.py`: Displays detailed data of a previously viewed coin
* `lang.json`: Holds language strings (TR/EN)

---

**4. Installation & Usage**

1. Install required dependencies:

   ```
   pip install matplotlib requests
   ```
2. Place all files in the same folder.
3. Run `app.py` to launch the application.

---