import requests
import time
from datetime import datetime
session = requests.Session()
URL = "https://api.binance.com/api/v3/klines"

def get_price(symbol="BTCUSDT", window="1m"):
    params = {
        "symbol": symbol.upper(),
        "interval": window,
        "limit": 24
    }
    
    try:
        start = time.perf_counter()
        response = session.get(URL, params=params, timeout=3)
        response.raise_for_status()
        candles = response.json()
        print(f"{datetime.now().strftime("%H:%M:%S")} API: Crypto done {(time.perf_counter()-start)*1000:.2f}")
        return [{"price": str(round(float(c[4]),2))} for c in candles]
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        raise ValueError