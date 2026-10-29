from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from contextlib import closing
import ntplib
import sqlite3

DB_PATH = '/home/matthew/Desktop/PersonalDashboardVersions/PersonalDashboard/assets/databases/timezones.sqlite3' # PYTHON USE
#DB_PATH = 'assets/databases/timezones.sqlite3'# PROD USE
def get_timezone(term: str = ""):
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

    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchone()
        #print(result[0].replace('_', ' ')) # DEBUGGING USE
        if result:
            return result[0]
        else:
            return ""

def get_time(term: str = ""):
    timezone_id = get_timezone(term)
    if timezone_id == "":
        return {}

    client = ntplib.NTPClient()
    response = client.request('127.0.0.1', port="65500", version=3) # Self hosted backend on docker

    dt_utc = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
    zoneinfo = ZoneInfo(timezone_id)
    dt_local = dt_utc.astimezone(zoneinfo)
    dst = dt_local.dst() != timedelta(0)

    date, time, dst =f"{dt_local.strftime('%Y-%m-%d %H:%M:%S')} {dst}".split(' ')
   
    return {"timezone": timezone_id, "tz": dt_local.strftime('%z'), "date": date, "time": time, "dst": str(dst)}
