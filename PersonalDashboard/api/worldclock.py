import ntplib
import sqlite3
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from contextlib import closing

DB_PATH = 'assets/databases/timezones.sqlite3'
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
            return str(result[0])
        else:
            return ""
# Tried to use pytz, failed because iana formating isnt good enough.
def get_time(term: str = ""):
    timezone_id = get_timezone(term)
    if timezone_id == "":
        return [{}]
    

    client = ntplib.NTPClient()
    #response = client.request('localhost', port="65500", version=3, timeout=1) # DEV USE 
    response = client.request('ntp', port="123", version=3, timeout=1) # DOCKER USE 
    dt_utc = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
    zoneinfo = ZoneInfo(timezone_id)
    dt_local = dt_utc.astimezone(zoneinfo)
    dst = dt_local.dst() != timedelta(0)

    date, timex, dst =f"{dt_local.strftime('%Y-%m-%d %H:%M:%S')} {dst}".split(' ')
    return [{"timezone": timezone_id.replace("/", ", ").replace("_", " "), "tz": dt_local.strftime('%z'), "date": date, "time": timex, "dst": str(dst)}]
