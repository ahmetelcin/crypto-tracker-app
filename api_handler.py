import requests

def search_coins(query):
    """Kullanıcının yazdığı query'e göre ilk 5 coin sonucunu döner."""
    if not query:
        return []

    url = f"https://api.coingecko.com/api/v3/search?query={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['coins'][:5]
    except Exception as e:
        print(f"API Hatası: {e}")
    return []

def get_coin_details(coin_id):
    """CoinGecko üzerinden coin detaylarını getir."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Detay API hatası: {e}")
    return None
