import json
import redis
from .auth import check_exist, check_cookie
from argon2 import PasswordHasher
from typing import cast

ph = PasswordHasher()

r = redis.Redis(host='localhost', port=65499, decode_responses=True)

def get_cards(username: str):
    if not username:
        return []

    data = cast(str | None, r.get(f"cards:{username}"))

    if not data:
        return []

    try:
        return json.loads(data)
    except Exception as e:
        return []

def update_cards(username: str, cards: list):
    if not username: return 
    try:
        r.set(f"cards:{username}", json.dumps(cards))
    except Exception as e:
        print(f"ERR update cards {e}")

def get_redis_uptime():
    seconds = cast(dict, r.info(section="server")).get("uptime_in_seconds", 0)
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    return f"{days}d {hours}h {minutes}m"

