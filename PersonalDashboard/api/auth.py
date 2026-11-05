import hashlib
import secrets
import json
import redis
from argon2 import PasswordHasher
from typing import cast

ph = PasswordHasher()
# hash, pass, user, cards

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
        return True, token
    return False, ""

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


def logout(username: str, cookie: str):
    if check_exist(username):
        user_data = cast(dict, r.hgetall(f"user:{username}"))
        try:
            token_hash = hashlib.sha256(cookie.encode()).hexdigest()
            hashes = json.loads(user_data.get("hash", "[]"))
            processed = [h for h in hashes if h != token_hash]

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
