import sqlite3
import hashlib
import secrets
import json
import time
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from contextlib import closing

ph = PasswordHasher()
DB = "assets/databases/users.sqlite3"

def create_table():
    with closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
        user    TEXT,
        pass    TEXT,
        data    TEXT,
        hash    TEXT)
        """
        )
        conn.commit()

def check_exist(username: str):
    with closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        row = cur.execute(("SELECT 1 FROM users WHERE user = ? LIMIT 1"), (username, )).fetchone()
        return row is not None   

def check_cookie(token: str, username: str):
    with closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        row = cur.execute(("SELECT hash FROM users WHERE user = ? LIMIT 1"), (username, )).fetchone()
        try:
            hashes = json.loads(row[0])
            if not isinstance(hashes, list):
                    return False
            return token_hash in hashes
        except Exception as e:
            print(e)
            return False
        
def register(username, password):
    if not check_exist(username) == None:
        with closing(sqlite3.connect(DB)) as conn:

            hash = ph.hash(password)
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO users (user, pass, data, hash)
                VALUES (?, ?, ?, ?)
                """,
                (username, hash, "", "")
            )
            conn.commit()
            return True
    else:
        return False

def login(username, password):

    if check_exist(username):
        with closing(sqlite3.connect(DB)) as conn:
            cur = conn.cursor()
            hashed = cur.execute((
                "SELECT pass FROM users WHERE user = ? LIMIT 1"), (username, )).fetchone()
            try:

                ph.verify(hashed[0], password)

                token = secrets.token_urlsafe(32)
                token_hash = hashlib.sha256(token.encode()).hexdigest()

                row = cur.execute("SELECT hash FROM users WHERE user = ?", (username, )).fetchone()

                if row[0] == "":
                    hashes = []
                else:
                    hashes = json.loads(row[0])

                hashes.append(token_hash)
                print(hashes)
                cur.execute("UPDATE users SET hash = ? WHERE user = ?", (json.dumps(hashes), username))

                conn.commit()

                return True, token
            except VerifyMismatchError, VerificationError, InvalidHashError:
                return False, ""
    else:
        return False, ""

def get_cards(username: str):
    with closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        try:
            row = cur.execute("SELECT data FROM users WHERE user = ?", (username, )).fetchone()
            if row[0] == "":
                return ""
            else:
                return json.loads(row[0]) # Return a [{}]
        except Exception as e:
            print(e)
            return ""

def update_cards(username: str, cards: list):

    with closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE users SET data = ? WHERE user = ?",
                (json.dumps(cards), username)
                )
            conn.commit()
        except Exception as e:
            print(e)