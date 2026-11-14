import reflex as rx
import redis
import json 
import hashlib
import secrets

from typing import cast
from argon2 import PasswordHasher 
from .FDapi import worldclock_get_time

ph = PasswordHasher()
ENV = 'DEV' 
if ENV == 'DEV':
    r = redis.Redis(
        host= 'localhost',
        port= 3001,
        decode_responses= True
    )

else:
    r = redis.Redis(
        host= 'FlexDashV4Dragonfly',
        port= 6379,
        decode_responses= True
    )

class Auth(rx.State):
    logged_username: str = ""
    logged_token: str = ""

    username_field: str = ""
    password_field: str = ""
    password_2_field: str = ""

    exist_acc: bool = False
    disabled: bool = True
    mode: str = "in"

    recovery_token: str = "" # MUST CLEAR AFTER USE.

    @rx.event
    def security_rp(self): # SECURITY PAGE ROUTE PROTECT
        if self.recovery_token == "":
            yield rx.redirect("/signin")

    @rx.event
    def set_mode(self, value):
        self.mode = value
        yield type(self).clear

    @rx.event
    def clear(self):
        self.username_field = ""
        self.password_field = ""
        self.password_2_field = ""

    @rx.event
    def set_username(self, value):
        self.username_field = value
        yield type(self).check_disable

    @rx.event
    def set_password(self, value):
        self.password_field = value
        yield type(self).check_disable

    @rx.event
    def set_2_password(self, value):
        self.password_2_field = value
        yield type(self).check_disable

    @rx.event
    def check_disable(self):
        if self.mode == "in":
            if self.username_field == "" or self.password_field == "":
                self.disabled = True
            else: 
                self.disabled = False
        elif self.mode == "up":
            if self.username_field == "" or self.password_field == "" or self.password_2_field == "":
                self.disabled = True
            else: 
                self.disabled = False

    # CHECK EXIST: r.exists(f"user:{username}") == 1

    @rx.event
    def sign_in(self):
        self.recovery_token = ""
        username = self.username_field
        password = self.password_2_field
        ua = self.router.headers.user_agent
        ip = self.router.session.client_ip
        time = worldclock_get_time("America/New_York")[0]

        if r.exists(f"user:{username}") == 1:
            user_data = cast(dict, r.hgetall(f"user:{username}"))
            try:
                ph.verify(user_data["pass"], password)
                token = secrets.token_urlsafe(32)
                token_hash = hashlib.sha256(token.encode()).hexdigest()

                
                hashes = json.loads(user_data.get("hash", "[{}]"))
                hashes.append({
                    "hash": token_hash,
                    "device" : f"{ua}|{ip}|{time}",
                })

                r.hset(f"user:{username}", "hash", json.dumps(hashes))
                yield type(self).clear
                self.logged_username = username
                yield rx.toast.success(f"Welcome, {username}")
                yield rx.redirect("/home")
            except Exception as e:
                yield rx.toast.warning("Incorrect username / password", position="top-center")
                print(e)
        else: yield rx.toast.warning("Incorrect username / password", position="top-center") # Instead saying username not exist ( increase security )

        yield type(self).clear()

    @rx.event
    def sign_up(self):
        username = self.username_field
        password = self.password_2_field # take confirmed one.
        if password != self.password_field:
            return rx.toast.warning("Password doesn't same with confirmed.", position="top-center")
        if not r.exists(f"user:{username}") == 1:

            hashed =  ph.hash(password)
            token = secrets.token_urlsafe(16) # 2 USER
            
            token_hash = hashlib.sha256(token.encode()).hexdigest()

            r.hset(f"user:{username}", mapping={
                "pass" : hashed,
                "hash" : "[]",
                "recovery" : token_hash
            })

            r.set(f"widgets:{username}", "[]")
            self.recovery_token = token
            return rx.redirect("/security")
        
        else: yield rx.toast.warning("Username already taken, try another.", position="top-center")

    @rx.event
    def recovery(self):
        username = self.username_field
        recovery = self.password_field
        new_password = self.password_2_field
        if r.exists(f"user:{username}") == 1:
            user_data = cast(dict, r.hgetall(f"user:{username}"))
            hashed = hashlib.sha256(recovery.encode()).hexdigest()
            stored_hash = user_data.get("recovery", "")
            if secrets.compare_digest(stored_hash, hashed):
                hashed_pass = ph.hash(new_password)
                r.hset(f"user:{username}", "pass", hashed_pass)
                token = secrets.token_urlsafe(16) # PARSE user with raw token 
                token_hash = hashlib.sha256(token.encode()).hexdigest() # ENCRYPT

                r.hset(f"user:{username}", "recovery", token_hash) # GIVE USER A NEW TOKEN for next time
                self.recovery_token = token
                return rx.redirect("/security")
            else:
                yield rx.toast.warning("Incorrect recovery code", position="top-center")
        else:
            yield rx.toast.warning("Username doesn't exist", position="top-center")