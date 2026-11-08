from datetime import datetime, timedelta
from pytz import timezone
import ntplib

def get_countdown():
    client = ntplib.NTPClient()
    #unix = client.request('localhost', port="65500").tx_time #DEV USE
    unix = client.request('ntp', port="123").tx_time # DOCKER USE

    ny_tz = timezone("America/New_York")

    ny_now = datetime.fromtimestamp(unix, ny_tz)

    d_sunday = (0 - ny_now.weekday()) % 7
    if d_sunday == 0: d_sunday = 7

    t_date = ny_now.date() + timedelta(days=d_sunday)

    t_ny = ny_tz.localize(datetime(
        t_date.year, t_date.month, t_date.day, 0, 0, 0
    ))

    t_unix = t_ny.timestamp()

    diff = int(t_unix - unix)


    hours = diff // 3600
    minutes = (diff % 3600) // 60
    seconds = diff % 60

    if len(str(hours)) == 1:
        hours = f"0{hours}"
    
    if len(str(minutes)) == 1:
        minutes = f"0{minutes}"

    if len(str(seconds)) == 1:
        seconds = f"0{seconds}"
        
    countdown = f"{hours}:{minutes}:{seconds}"

    return countdown