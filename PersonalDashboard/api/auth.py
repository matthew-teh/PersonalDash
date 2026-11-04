import sqlite3
import hashlib
import secrets
import json
import time
import redis
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from contextlib import closing
from typing import cast

ph = PasswordHasher()
DB = "assets/databases/users.sqlite3"


r = redis.Redis(host='localhost', port=65499, decode_responses=True)

def check_exist(username: str):
    return r.exists(f"user:{username}") == 1

def check_cookie(token: str, username: str):
    if not token or not username:
        return False
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    try:
        hashes = json.loads(cast(str, r.hget(f"user:{username}", "hash")))
        if not isinstance(hashes, list): return False
        return token_hash in hashes
    except:
        return False


def register(username, password):
    if not check_exist(username):
        hashed =  ph.hash(password)

        r.hset(f"user:{username}", mapping={
            "pass" : hashed,
            "hash" : "[]"
        })

        r.set(f"cards:{username}", "[]")
        return True
    return False

def login(username: str, password: str):
    if check_exist(username):
        user_data = cast(dict, r.hgetall(f"user:{username}"))
        try:
            ph.verify(user_data["pass"], password)
            token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            hashes = json.loads(user_data.get("hash", "[]"))
            hashes.append(token_hash)

            r.hset(f"user:{username}", "hash", json.dumps(hashes))
            return True, token
        except:
            return False, ""
    return False, ""
            
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