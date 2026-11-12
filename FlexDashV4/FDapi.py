import requests, time, openmeteo_requests, sqlite3, csv, ntplib
from zoneinfo import ZoneInfo
from contextlib import closing
from pathlib import Path
from datetime import datetime, timezone, timedelta

ENV = "DEV" # DOCKER

session = requests.Session()

def crypto_get_price(symbol="BTCUSDT", window="1m"):
    URL = "https://api.binance.com/api/v3/klines"
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


weather_db = "assets/databases/worldcities.sqlite3"
mapping_db = Path("assets/databases/weathercodes.csv")

weather_conn = sqlite3.connect(weather_db)


def _safe_client_del(self):
    try:
        self.close()
    except Exception:
        pass

openmeteo_requests.Client.__del__ = _safe_client_del

def _load_weather_mapping():
    weather_mapping = {}
    if mapping_db.exists():
        with open(mapping_db, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                code = int(row["wetcode"])
                weather_mapping[code] = {
                    "description": row["description"],
                    "image": f"weather_icons/{row['image']}",
                }
    return weather_mapping



def weather_get_name(name: str):
    
    cursor = weather_conn.cursor()
    query = """
        SELECT city, country, lat, lng 
        FROM cities 
        WHERE city LIKE ? 
        ORDER BY 
            CASE WHEN city = ? THEN 0 ELSE 1 END,
            CASE WHEN city LIKE ? THEN 0 ELSE 1 END,
            LENGTH(city) ASC
        LIMIT 1
    """
    cursor.execute(query, (f"%{name}%", name, f"{name}%"))
    item = cursor.fetchone()

    if item is None:
        return ""

    city_name, country_name, lat, lng = item
    return str(city_name)

def weather_get_data(name: str):
    start = time.perf_counter()

    cursor = weather_conn.cursor()
    query = """
        SELECT city, country, lat, lng 
        FROM cities 
        WHERE city LIKE ? 
        ORDER BY 
            CASE WHEN city = ? THEN 0 ELSE 1 END,
            CASE WHEN city LIKE ? THEN 0 ELSE 1 END,
            LENGTH(city) ASC
        LIMIT 1
    """
    cursor.execute(query, (f"%{name}%", name, f"{name}%"))
    item = cursor.fetchone()

    if item is None:
        return "", [{}]

    city_name, country_name, lat, lng = item
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current": [
            "relative_humidity_2m",
            "precipitation",
            "weather_code",
            "temperature_2m",
            "wind_speed_10m",
            "apparent_temperature",
            "cloud_cover",
        ],
        "timezone": "auto",
    }
    openmeteo = openmeteo_requests.Client()
    response = openmeteo.weather_api(url, params=params)[0]
    current = response.Current()
    assert current is not None
    assert current.Variables is not None

    wetcode = current.Variables(2).Value() #type:ignore

    mappings = _load_weather_mapping()
    default = {
        "description": "Unknown",
        "image": "weather_icons/default.svg",
    }
    weather_info = mappings.get(int(wetcode), default)

    print(f"{datetime.now().strftime("%H:%M:%S")} API: Weather done {(time.perf_counter() - start) * 1000:.2f}")
    result = [{
        "lat": response.Latitude(),
        "lng": response.Longitude(),
        "relative_humid": round(current.Variables(0).Value()), #type:ignore
        "precip": current.Variables(1).Value(), #type:ignore
        "wetcode": weather_info["description"], 
        "temp": round(current.Variables(3).Value()), #type:ignore
        "windspd": round(current.Variables(4).Value()), #type:ignore
        "feeltemp": round(current.Variables(5).Value()), #type:ignore
        "useimg": weather_info["image"],
        "cloudcvr" : round(current.Variables(6).Value()), #type:ignore
    }]
    
    return name, result


def worldclock_get_timezone(term: str = ""):
    term = term.strip().replace(' ', '_') # Remove spaces " "
    if term == "":
        return ""
    query = """
    SELECT id
    FROM timezones
    WHERE id LIKE ?
    ORDER BY
        CASE WHEN id = ?    THEN 0 ELSE 1 END,
        CASE WHEN id LIKE ? THEN 0 ELSE 1 END,
        CASE WHEN id LIKE ? THEN 0 ELSE 1 END,
        LENGTH(id) ASC
    LIMIT 1
    """
    params = (f'%{term}%', term, f'{term}%', f'%/{term}')
    DB_PATH = 'assets/databases/timezones.sqlite3'
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchone()
        #print(result[0].replace('_', ' ')) # DEBUGGING USE

        if result:
            return str(result[0])
        else:
            return ""
        
def worldclock_get_time(term: str = ""):
    timezone_id = worldclock_get_timezone(term)
    if timezone_id == "":
        return [{}]
    

    client = ntplib.NTPClient()

    if ENV == "DEV":
        response = client.request('172.20.192.1', port="3002", version=3, timeout=1) # DEV USE 
    else: 
        response = client.request('ntp', port="123", version=3, timeout=1) # DOCKER USE 

    dt_utc = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
    zoneinfo = ZoneInfo(timezone_id)
    dt_local = dt_utc.astimezone(zoneinfo)
    dst = dt_local.dst() != timedelta(0)

    date, timex, dst =f"{dt_local.strftime('%Y-%m-%d %H:%M:%S')} {dst}".split(' ')
    return [{"timezone": timezone_id.replace("/", ", ").replace("_", " "), "tz": dt_local.strftime('%z'), "date": date, "time": timex, "dst": str(dst)}]
