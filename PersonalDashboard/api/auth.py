import hashlib
import secrets
import json
import redis
from argon2 import PasswordHasher
from typing import cast
from ..api.worldclock import get_time


ph = PasswordHasher()
# hash, pass, user, cards
# DEV USE
#r = redis.Redis(host='127.0.0.1', port=65499, decode_responses=True)


# DOCKER USE 
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def check_exist(username: str):
    return r.exists(f"user:{username}") == 1

def check_cookie(token: str, username: str):
    if not token or not username:
        return False
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    try:
        hashes = json.loads(cast(str, r.hget(f"user:{username}", "hash")))
        for h in hashes:
            if h["hash"] == token_hash:
                return True
        return False
    except Exception as e:
        print(e)
        return False

def register(username, password):
    if not check_exist(username):
        hashed =  ph.hash(password)
        # AUTH 
        token = secrets.token_urlsafe(16) # PARSE user with raw token 
        token_hash = hashlib.sha256(token.encode()).hexdigest() # ENCRYPT
        r.hset(f"user:{username}", mapping={
            "pass" : hashed,
            "hash" : "[]",
            "recovery" : token_hash
        })
        # DATABASE
        r.set(f"cards:{username}", "[]")
        print("success")
        return True, token
    return False, ""

def login(username: str, password: str, UA: str):
    print(username, password)
    print(check_exist(username))
    if check_exist(username):
        user_data = cast(dict, r.hgetall(f"user:{username}"))
        try:
            ph.verify(user_data["pass"], password)
            token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(token.encode()).hexdigest()

            time = get_time("America/New_York")[0]
            hashes = json.loads(user_data.get("hash", "[{}]"))
            hashes.append({
                "hash": token_hash,
                "device" : f"{UA} at {time["date"]} {time["time"]} EST",
            })

            r.hset(f"user:{username}", "hash", json.dumps(hashes))
            return True, token
        except Exception as e:
            print(f"LOGIN : {e}")
            return False, ""
    return False, ""


def logout(username: str, cookie: str):
    if check_exist(username):
        user_data = cast(dict, r.hgetall(f"user:{username}"))
        try:
            token_hash = hashlib.sha256(cookie.encode()).hexdigest()
            hashes = json.loads(user_data.get("hash", "[{}]"))

            processed = []
            for h in hashes:
                if h.get("hash") != token_hash:
                    processed.append(h)


            r.hset(f"user:{username}", "hash", json.dumps(processed))
            return True
        except:
            return True
            
    return True

def delete_acc(username: str, password: str):
    if check_exist(username):
        user_data = cast(dict, r.hgetall(f"user:{username}"))
        try:
            ph.verify(user_data["pass"], password)

            r.delete(f"user:{username}")
            r.delete(f"cards:{username}")
            return "Success"
        except:
            return "Incorrect password"
    else:
        return "404"

def forgot_password(username: str, recoverycode: str, newpassword: str):
    if check_exist(username):
        user_data = cast(dict, r.hgetall(f"user:{username}"))
        hashed = hashlib.sha256(recoverycode.encode()).hexdigest()
        stored_hash = user_data.get("recovery", "")
        if secrets.compare_digest(stored_hash, hashed):
            hashed_pass = ph.hash(newpassword)
            r.hset(f"user:{username}", "pass", hashed_pass)
            token = secrets.token_urlsafe(16) # PARSE user with raw token 
            token_hash = hashlib.sha256(token.encode()).hexdigest() # ENCRYPT
            r.hset(f"user:{username}", "recovery", token_hash) # GIVE USER A NEW TOKEN for next time

            return True, token
        else:
            return False, ""
    else:
        return False, "NOUSERNAME"
def get_UAS(username: str) -> str:
    hashes = json.loads(cast(str, r.hget(f"user:{username}", "hash")))
    
    device_names = [h["device"].strip() for h in hashes if h.get("device")]
    return "\n".join(f"{i}. {d}" for i, d in enumerate(device_names, start=1))