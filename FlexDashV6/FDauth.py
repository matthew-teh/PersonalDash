import reflex as rx
import redis
import json 
import hashlib
import secrets
import time
import humanize
from user_agents import parse
from typing import cast
from argon2 import PasswordHasher 
from datetime import datetime, timezone
from .FDapi import worldclock_get_time

ph = PasswordHasher()
ENV = 'DEV' 
# TODO REWRITE ENV SETUP 

if ENV == 'DEV':
    r = redis.Redis(
        host= 'localhost',
        port= 65501,
        decode_responses= True
    )

else:
    r = redis.Redis(
        host= 'dragonfly_db',
        port= 6379,
        decode_responses= True
    )

class Auth(rx.State):
    logged_username: str = rx.Cookie(secure=True, same_site="lax")
    logged_cookie: str = rx.Cookie(secure=True, same_site="lax")
    logged_devices: list[list[str]] =  []

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
            if self.username_field == "" or self.password_2_field == "":
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
    def auto_signin(self):
        result = False
        if self.logged_cookie and self.logged_username:
            try:
                token_hash = hashlib.sha256(self.logged_cookie.encode()).hexdigest()
                
                hashes_raw = r.hget(f"user:{self.logged_username}", "hash")

                
                if hashes_raw:
                    hashes = json.loads(cast(str, hashes_raw))
                    for h in hashes:
                        if h.get("hash") == token_hash:
                            result = True
                            h["last_act"] = str(round(time.time()))
                            break
                    r.hset(f"user:{self.logged_username}", "hash", json.dumps(hashes))
            except Exception as e:
                print(e)
                result = False
                
        self.exist_acc = result
        if result:
            yield rx.toast.success(f"Welcome, {self.logged_username}")
            yield rx.redirect("/home")

    
    @rx.event
    def sign_in(self):
        self.recovery_token = ""
        username = self.username_field
        password = self.password_2_field
        
        headers = self.router.headers or {}
        ua_raw = self.router.headers.user_agent
        ua = parse(ua_raw) if ua_raw else None
        ua_formatted = f"{ua.browser.family} on {ua.os.family}" if ua else "Unknown Device"
        
        ip = getattr(self.router.session, "client_ip", "Unknown IP")
        timex = worldclock_get_time("America/New_York")[0] # CONFLICT with TIME.TIME()
        time_formatted = f"{timex["time"]} {timex["date"]}"

        if r.exists(f"user:{username}") == 1:
            user_data = cast(dict, r.hgetall(f"user:{username}"))
            try:
                ph.verify(user_data["pass"], password)

                token = secrets.token_urlsafe(32)
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                hashes = json.loads(user_data.get("hash", "[]"))
                
                hashes.append({
                    "hash": token_hash,
                    "device": f"{ua_formatted}|{ip}|{time_formatted}",
                    "last_act" : time.time(),
                })

                r.hset(f"user:{username}", "hash", json.dumps(hashes))
                yield type(self).clear()

                self.logged_username = username
                self.logged_cookie = token
                self.exist_acc = True

                yield rx.toast.success(f"Welcome, {username}")
                return rx.redirect("/home")
            except Exception as e:
                print(e)
                yield rx.toast.warning("Incorrect username / password", position="top-center")
        else:
            yield rx.toast.warning("Incorrect username / password", position="top-center")

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


    @rx.event
    def upload_widgets(self, widgets):
        if self.logged_username:
            try:
                r.set(f"widgets:{self.logged_username}", json.dumps(widgets))
            except Exception as e:
                print(e)

    @rx.event
    def download_widgets(self):
        if self.logged_username:
            data = cast(str | None, r.get(f"widgets:{self.logged_username}"))

            if not data:
                return []
            try:
                return json.loads(data)
            except Exception as e:
                print(e)
                return []
        else: return []


    @rx.event
    def sign_out(self):
        if self.logged_username and self.logged_cookie:
            token_hash = hashlib.sha256(self.logged_cookie.encode()).hexdigest()
            user_key = f"user:{self.logged_username}"
            
            if r.exists(user_key):
                user_data = cast(dict, r.hgetall(user_key))
                hashes = json.loads(user_data.get("hash", "[]"))
                
                updated_hashes = [h for h in hashes if h.get("hash") != token_hash]
                r.hset(user_key, "hash", json.dumps(updated_hashes))

        self.logged_username = ""
        self.logged_cookie = ""
        self.exist_acc = False
        
        yield type(self).clear()
        yield rx.toast.info("Signed out successfully", position="top-center")
        return rx.redirect("/")


    @rx.event
    def delete_account(self):
        username = self.logged_username
        if not self.password_2_field == "" : 
            if r.exists(f"user:{username}") == 1:
                result = ""
                user_data = cast(dict, r.hgetall(f"user:{username}"))
                try:
                    ph.verify(user_data["pass"], self.password_2_field)

                    r.delete(f"user:{username}")
                    r.delete(f"widgets:{username}")
                    result = "Success"
                except:
                    result = "Incorrect password"
                
                print(result)
                if result == "Success":
                    yield rx.redirect("/signin")
                    yield rx.toast.success("Account deleted, goodbye.", position="top-center")
                elif result == "Incorrect password":
                    yield rx.toast.warning("Wrong password.", position="top-center")
                elif result == "404":
                    yield rx.toast.error("404 Delete Account, contact admin", position="top-center")
                else:
                    yield rx.toast.error(f"Unknown error: {result}", position="top-center")
        else:
            print("No pswd")

    @rx.event
    def prepare_devices(self):
        user_data = cast(dict, r.hgetall(f"user:{self.logged_username}"))
        self.logged_devices = []
        try:
            data = json.loads(user_data["hash"])
            for h in data:
                x = h["device"].split("|")
                if h["hash"] == hashlib.sha256(self.logged_cookie.encode()).hexdigest():
                    x[0] = f"{x[0]}|This Device"
                last_active = int(h["last_act"]) if h.get("last_act") else 0
                formatted = humanize.naturaltime(datetime.now(timezone.utc) - datetime.fromtimestamp(last_active, tz=timezone.utc))
                x.append(formatted)        
                x.append(h["hash"])
                self.logged_devices.append(x)
        except Exception as e:
            print(e)
            return []

    @rx.event
    def change_password(self):
        if self.password_field != self.password_2_field:
            return rx.toast.warning("Confirm password not same as password.", position="top-center")
        user_data = cast(dict, r.hgetall(f"user:{self.logged_username}"))
        try:    
            ph.verify(user_data["pass"], self.username_field)

            hashed = ph.hash(self.password_2_field)
            r.hset(f"user:{self.logged_username}", "pass", hashed)

            yield rx.toast.success("Password changed, login again.", position="top-center")
            yield type(self).sign_out
        except Exception as e:
            yield rx.toast.warning("Incorrect password.", position="top-center")

    @rx.event()
    def handle_logout_device(self, hash):
        user_data = cast(dict, r.hgetall(f"user:{self.logged_username}"))
        try:
            ph.verify(user_data["pass"], self.password_field)

            devices = json.loads(user_data["hash"])

            processed = [device for device in devices if device["hash"] != hash]

            r.hset(f"user:{self.logged_username}", "hash", json.dumps(processed))
            yield type(self).prepare_devices
            if hash == hashlib.sha256(self.logged_cookie.encode()).hexdigest():
                yield type(self).sign_out

        except Exception as e:
            print(e)
            yield rx.toast.warning("Incorrect password.", position="top-center")