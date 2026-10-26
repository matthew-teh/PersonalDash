import sqlite3
import csv
import time
from pathlib import Path
from functools import lru_cache
import openmeteo_requests
from datetime import datetime
DB_PATH = "assets/databases/worldcities.sqlite3"
CSV_PATH = Path("assets/databases/weathercodes.csv")

_conn = sqlite3.connect(DB_PATH)

def _safe_client_del(self):
    try:
        self.close()
    except Exception:
        pass

openmeteo_requests.Client.__del__ = _safe_client_del

@lru_cache(maxsize=1)
def _load_weather_mapping():
    weather_mapping = {}
    if CSV_PATH.exists():
        with open(CSV_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                code = int(row["wetcode"])
                weather_mapping[code] = {
                    "description": row["description"],
                    "image": f"weatherimages/{row['image']}",
                }
    return weather_mapping

def get_weather(wetcode):
    weather_mapping = _load_weather_mapping()
    default = {
        "description": "Unknown",
        "image": "weatherimages/default.svg",
    }
    return weather_mapping.get(int(wetcode), default)

def get_name(name: str):
    start = time.perf_counter()
    
    cursor = _conn.cursor()
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

def get_data(name: str):
    start = time.perf_counter()

    cursor = _conn.cursor()
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
        return "NaN", [{}]

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

    wetcode = current.Variables(2).Value()
    weather_info = get_weather(wetcode)

    print(f"{datetime.now().strftime("%H:%M:%S")} API: Weather done {(time.perf_counter() - start) * 1000:.2f}")
    result = [{
        "lat": response.Latitude(),
        "lng": response.Longitude(),
        "relative_humid": current.Variables(0).Value(),
        "precip": current.Variables(1).Value(),
        "wetcode": weather_info["description"],
        "temp": current.Variables(3).Value(),
        "windspd": current.Variables(4).Value(),
        "feeltemp": current.Variables(5).Value(),
        "useimg": weather_info["image"],
        "cloudcvr" : current.Variables(6).Value(),
    }]
    
    return name, result
# Setup the Open-Meteo API clients

'''import pandas as pd
import sqlite3

df = pd.read_csv("assets/databases/worldcities.csv")

cols_to_drop = ['city_ascii', 'iso2', 'iso3', 'admin_name', 'capital', 'population', 'id']
df_filtered = df.drop(columns=cols_to_drop)
conn = sqlite3.connect("assets/databases/worldcities.sqlite3")

df_filtered.to_sql('cities', conn, if_exists="replace", index=False)
conn.close()
print("Done")'''