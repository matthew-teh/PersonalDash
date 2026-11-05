import reflex as rx
import json
import uuid
import asyncio
import time 
from typing import TypedDict, Literal, cast
from ..api.crypto import get_price
from ..api.worldclock import get_time, get_timezone
from ..api import weather
from ..api.tictactoe import check_win, computer_decide
from ..api.auth import register, check_exist, login, check_cookie, delete_acc, logout, forgot_password
from ..api.database import get_cards, update_cards, get_redis_uptime

start = time.time()

class CardData(TypedDict):
    id: str
    type: str
    name: str
    data: list[dict[str, str]]
    data1: str
    data2: float
    data3: list[int]

class DashboardState(rx.State):
    # DB
    cards_json: str = "[]" 
    # ---- RX VAR HERE ----
    @rx.var
    def cards(self) -> list[CardData]:
        try:
            # Parse from state, not from SQLite
            data = json.loads(self.cards_json)
            if not isinstance(data, list):
                return []
            return [cast(CardData, item) for item in data if isinstance(item, dict) and "id" in item]
        except (json.JSONDecodeError, TypeError):
            return []

    @rx.event
    async def load_cards(self):
        auth = await self.get_state(AuthState)
        data = get_cards(auth.user)
        if isinstance(data, list):
            self.cards_json = json.dumps(data)
        else:
            self.cards_json = "[]"

    @rx.event
    async def dump_json(self, cards: list[CardData]):
        self.cards_json = json.dumps(cards)
        auth = await self.get_state(AuthState)
        update_cards(auth.user, cards)

    is_updating = False
    # ---- RX EVENT BACKGROUND HERE ----

    # ---- RX QUICK NOTES SPECIFIC EVENT HERE ----
    editing_card_id: str = "" # SET EDITING. Not live syncing idk
    editing_text: str = ""

    @rx.event
    def start_editing(self, card_id, text):
        self.editing_card_id = card_id
        self.editing_text = text

    @rx.event
    async def live_update(self, text: str):
        self.editing_text = text

        for card in self.cards:
            if card["id"] == self.editing_card_id:
                card["data"][0]["text"] = self.editing_text
        await self.dump_json(self.cards)

    # ---- RX WORLD CLOCK SPECIFIC EVENT HERE ----
    edit_world_clock_name = ""

    @rx.event
    async def update_world_clock(self):
        for card in self.cards:
            if card["type"] == "world_clock":
                async with self:
                    name = card["data"][0]["timezone"].replace(", ", "/").replace(" ", "_")
                    card["data"] = get_time(name)
        await self.dump_json(self.cards)
        
    @rx.event
    async def set_name_world_clock(self, value, card_id):
        self.edit_world_clock_name = value
        for card in self.cards:
            if card["id"] == card_id:
                card["data1"] = get_timezone(self.edit_world_clock_name).replace("_", " ")
        await self.dump_json(self.cards)

    @rx.event
    async def save_edit_world_clock(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                card["name"] = card["data1"].split("/")[1]
                card["data"] = get_time(card["data1"].replace(" ", "_"))
                card["data1"] = ""
                self.edit_world_clock_name = ""
                
        await self.dump_json(self.cards)

    # ---- RX WEATHER SPECIFIC EVENT HERE ----
    edit_name_weather: str = ""
    @rx.event
    async def save_edit_weather(self, card_id):
        for card in self.cards:
            if card_id == card["id"]:
                card["name"] = card["data1"]
                card["data1"] = ""
                self.edit_name_weather = ""
                await self.dump_json(self.cards)
                return type(self).update_weather(card_id)
            
    @rx.event
    async def update_weather(self, card_id):
        for card in self.cards:
            if card_id == card["id"]:
                name, datas = weather.get_data(card["name"])
                if name == "NaN":
                    return rx.toast("Cannot Update Data, invalid location", style={"background-color" :"#403D39"})
                else:
                    card["data"] = datas
                    await self.dump_json(self.cards)
        
    @rx.event
    async def set_name_weather(self, value: str, card_id):
        self.edit_name_weather = value
        for card in self.cards:
            if card["id"] == card_id:
                card["data1"] = weather.get_name(value)
                await self.dump_json(self.cards)
                
    # ---- RX CRYPTO SPECIFIC EVENT HERE ----
    edit_name_crypto: str = ""
    edit_window_crypto: str = ""

    @rx.event
    async def save_edit_crypto(self, card_id: str, value={}):
        for card in self.cards:
            if card["id"] == card_id and card["type"] == "crypto":
                if not isinstance(value, dict) and not card["name"] == "NaN":
                    card["data1"] = value
                    return type(self).update_crypto(card_id, False)
                elif self.edit_name_crypto:
                    card["name"] = self.edit_name_crypto
                    self.edit_name_crypto = ""
                    await self.dump_json(self.cards)
                    return type(self).update_crypto(card_id, True)
                else:
                    return rx.toast("Cannot Update Data, no symbol set.", style={"background-color" :"#403D39"})

    @rx.event
    def set_name_crypto(self, value: str):
        self.edit_name_crypto = value
    @rx.event
    def set_window_crypto(self, value: str):
        self.edit_window_crypto = value

    @rx.event
    async def update_crypto(self, card_id: str, passthrough=False): # PASSTHROUGH deprecated
        for card in self.cards:
            if card["id"] == card_id:
                found = True
                if card["name"] != "NaN":
                    try:
                        result = get_price(symbol=card["name"],window=card["data1"])
                        card["data"] = result 
                        card["data2"] = -round(((float(result[0]["price"]) - float(result[-1]["price"])) / float(result[0]["price"])) * 100, 2)
                        await self.dump_json(self.cards)
                    except:
                        return rx.toast("Wrong Symbol, try ETHUSDT or BTCUSDT, aim something that ending with USDT", style={"background-color" :"#403D39"})
                else:
                    return rx.toast("Cannot Update Data, no symbol set.", style={"background-color" :"#403D39"})
                break
    
    
    def price_diff(self, card: CardData) -> str:
        first = float(card["data"][0]["price"])
        last = float(card["data"][-1]["price"])
        change = -round(((first - last) / first) * 100, 2)
        return str(change)

    # ---- RX POMODORO SPECIFIC EVENT HERE ----
    pomodoro, short, long = "25", "5", "15"

    @rx.event
    def edit_pomodoro_pomodoro(self, value):
        self.pomodoro = value
    @rx.event
    def edit_short_pomodoro(self, value):
        self.short = value
    @rx.event
    def edit_long_pomodoro(self, value):
        self.long = value

    @rx.event
    async def save_edit_pomodoro(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                card["data"][0]["pomodoro"] = self.pomodoro
                card["data"][0]["short"] = self.short
                card["data"][0]["long"] = self.long

                self.pomodoro, self.short, self.long = "25", "5", "15"
        await self.dump_json(self.cards)
        await self.command_pomodoro(card_id, "reset")

    @rx.event
    async def command_pomodoro(self, card_id, command):
        for card in self.cards:
            if card["id"] == card_id:
                if command == "start":
                    card["data"][0]["started"] = "true"
                    if not float(card["data"][0]["sec_left"]) < float(card["data"][0]["pomodoro"])*60: # If below than settings, means it is going

                        card["data"][0]["sec_left"] = str(float(card["data"][0]["pomodoro"])*60)
                        card["data"][0]["mode"] = "pomodoro"
                        card["data"][0]["intervals"] = "1"
                elif command == "stop":
                    card["data"][0]["started"] = "false"
                elif command == "reset":
                    card["data"][0]["sec_left"] = str(float(card["data"][0]["pomodoro"])*60)
                    card["data"][0]["started"] = "false"
                    card["data"][0]["mode"] = "pomodoro"
                    card["data"][0]["intervals"] = "1"
                    sec = float(card["data"][0]["sec_left"])
                    minutes = round(( sec % 3600) // 60)
                    seconds = round(sec % 60)
                    if len(str(minutes)) == 1:
                        minutes = f"0{minutes}"
                    if len(str(seconds)) == 1:
                        seconds = f"0{seconds}"
                    card["data"][0]["timing"] = f"{minutes}:{seconds}" # Calculate differences.
        await self.dump_json(self.cards)

    @rx.event
    async def update_pomodoro(self):
        for card in self.cards:
            if card["type"] == "pomodoro" and card["data"][0]["started"].lower() == "true": # If is running
                sec = round(float(card["data"][0]["sec_left"])) - 1
                card["data"][0]["sec_left"] = str(float(card["data"][0]["sec_left"]) - 1)
                if sec == 0: 
                    card["data"][0]["timing"] ="00:00"
                    intervals = int(card["data"][0]["intervals"])
                    mode = card["data"][0]["mode"]
                    if mode == "pomodoro":
                        if intervals >= 4:
                            card["data"][0]["sec_left"] = str(float(card["data"][0]["long"])*60)
                            card["data"][0]["mode"] = "long"
                        else:
                            card["data"][0]["sec_left"] = str(float(card["data"][0]["short"])*60)
                            card["data"][0]["intervals"] = str(intervals +1)
                            card["data"][0]["mode"] = "short"
                    elif mode == "short":
                        card["data"][0]["sec_left"] = str(float(card["data"][0]["pomodoro"])*60)
                        card["data"][0]["mode"] = "pomodoro"

                    elif mode == "long":
                        card["data"][0]["sec_left"] = str(float(card["data"][0]["pomodoro"])*60)
                        card["data"][0]["intervals"] = "1"
                        card["data"][0]["mode"] = "pomodoro"

                else:
                    minutes = round((sec % 3600) // 60)
                    seconds = round(sec % 60)
                    if len(str(minutes)) == 1:
                        minutes = f"0{minutes}"
                    if len(str(seconds)) == 1:
                        seconds = f"0{seconds}"
                    card["data"][0]["timing"] = f"{minutes}:{seconds}" # Calculate differences.


        await self.dump_json(self.cards)

    # ---- RX TIC_TAC_TOE SPECIFIC EVENT HERE
    edit_diff_tic_tac_toe = ""
    @rx.event
    def set_diff_tic_tac_toe(self, value):
        self.edit_diff_tic_tac_toe = value

    @rx.event
    async def setup_tic_tac_toe(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                grids = []
                for r in range(3):
                    for c in range(3):
                        grids.append({
                            "id" : str(r*3+c),
                            "data" : "0",
                        })
                card["data"] = grids
        await self.dump_json(self.cards)

    @rx.event
    async def register_click(self, card_id, button_id):
        for card in self.cards:
            if card["id"] == card_id and card["data2"] == 0: # 0 player 1 computer
                for item in card["data"]:
                    if item["id"] == button_id and item["data"] != "X":
                        item["data"] = "O"
                        await self.dump_json(self.cards)
                        yield
                        await self.calculate(card_id)
                        break
    @rx.event
    async def calculate(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                status = check_win(card["data"])
                time.sleep(0.1)
                if status == "none":
                    move = computer_decide(card["data"])
                    if not move == {}:
                        for item in card["data"]:
                            if item["id"] == move["id"]:
                                item["data"] = move["data"]
                status = check_win(card["data"])
                if status == "player":
                    card["data3"][0] += 1
                    await self.setup_tic_tac_toe(card_id)
                if status == "computer":
                    card["data3"][1] += 1
                    await self.setup_tic_tac_toe(card_id)
                if status == "tie":
                    await self.setup_tic_tac_toe(card_id)
                await self.dump_json(self.cards)
        
    # ---- RX SETTING SPECIFIC EVENT HERE ----
    edit_column = "4"
    edit_radius: Literal["none", "small", "medium", "large", "full"] = "medium"
    @rx.event
    def set_column(self, value):
        self.edit_column = value

    @rx.event
    def set_radius(self, value):
        self.edit_radius = value

    # ---- RX ALL EVENT HERE ----
    @rx.event 
    async def create_card(self, card):
        card_id =  str(uuid.uuid4())
        if card == "crypto":
            self.cards.append({
                "id": card_id,    
                "type": "crypto",
                "name": "BTCUSDT",
                "data": [{}],
                "data1": "15m",
                "data2": 0,
                "data3": [],
            })
            await self.dump_json(self.cards)
            yield
            await self.update_crypto(card_id, True)

        if card == "weather":
            # Format [{"lat": lat, "lng": lng, "relative_humid": rlthumid, "precip", precip, "wetcode", wetcode, "temp", temp, "windspd", windspd, "feeltemp", feeltemp}]
            self.cards.append({
                "id": card_id,
                "type": "weather",
                "name": "London",
                "data": [{}],
                "data1": "",
                "data2": 0,
                "data3": [],
            })
            await self.dump_json(self.cards)
            yield
            await self.update_weather(card_id)

        if card == "world_clock":
            result = get_time('Asia/Singapore')
            self.cards.append({
                "id": card_id,
                "type": "world_clock",
                "name": f"{result[0]["timezone"].split(", ")[1]} Time",
                "data": result, 
                "data1": "",
                "data2": 0,
                "data3": [],
            })
            await self.dump_json(self.cards)

        if card == "pomodoro":
            self.cards.append({
                "id": card_id,
                "type": "pomodoro",
                "name": "Pomodoro Timer",
                "data": [{"pomodoro":"25", "short":"5", "long":"15", "intervals": "1", "started": "false", "sec_left":"0", "mode":"pomodoro"}], 
                "data1": "",
                "data2": 0,
                "data3" : [], 
            })
            await self.command_pomodoro(card_id, "reset")
            await self.dump_json(self.cards)

        if card == "tic_tac_toe":
            self.cards.append({
                "id": card_id,
                "type": "tic_tac_toe",
                "name": "Tic Tac Toe",
                "data": [{}], 
                "data1": "easy",
                "data2": 0,
                "data3": [0, 0],
            })
            await self.setup_tic_tac_toe(card_id)
            await self.dump_json(self.cards)

        if card == "quick_notes":
            self.cards.append({
                "id": card_id,
                "type": "quick_notes",
                "name": "Quick Notes",
                "data": [{"text" : ""}], 
                "data1": "",
                "data2": 0,
                "data3": [0, 0],
            })
            await self.dump_json(self.cards)
            

    @rx.event
    async def update_all(self):
        self.is_updating = True
        yield 
        for card in self.cards:
            if card["type"] == "crypto":
                await self.update_crypto(card["id"], True)
            if card["type"] == "weather":
                await self.update_weather(card["id"])
        rx.toast("Done Refresh.", style={"background-color" :"#403D39"})
        self.is_updating = False 
        yield

    @rx.event
    async def delete_card(self, card_id):
        for card in self.cards:
            if card_id == card["id"]:
                self.cards.remove(card)
        await self.dump_json(self.cards)

    @rx.event
    async def delete_all(self):
        self.cards.clear()
        await self.dump_json(self.cards)



# ---- SERVER ONLY STATE ----

class ServerState(rx.State):
    cpu = 0
    mem = 0
    server_uptime = ""
    redis_uptime = ""
    
    @rx.event
    async def updateSystem(self):

        sec = int(time.time() - start)
        days = sec // 86400
        hours = (sec % 86400) // 3600
        minutes = ( sec % 3600) // 60
        async with self:
            self.server_uptime =  f"{days}d {hours}h {minutes}m"
            self.redis_uptime = get_redis_uptime()

class AuthState(rx.State):
    logged_in : bool = False
    user: str = ""
    cookie: str = rx.Cookie("")
    user_cookie: str = rx.Cookie("")

    
    tries: int = 0
    username: str = ""
    password: str = ""
    password2: str = ""
    disabled: bool = True
    recovery_token: str = ""


    # SIGNIN / SIGNUP 
    @rx.event(background=True)
    async def rate_limit(self):
        await asyncio.sleep(5)
        async with self:
            self.tries = 0
            self.disabled = False

    @rx.event
    def set_username(self, value):
        self.username = value
        return type(self).check_registrable
    
    @rx.event
    def set_password(self, value):
        self.password = value
        return type(self).check_registrable

    @rx.event
    def set_password2(self, value):
        self.password2 = value
        return type(self).check_registrable

    @rx.event
    def check_registrable(self):
        if self.username == "" or self.password == "": 
            self.disabled = True
        else:
            self.disabled = False

    @rx.event
    def reset_field(self):
        self.password = ""
        self.password2 = ""
        self.username = ""
        self.disabled = True

    @rx.event
    def check_signedin(self):
        if not self.cookie == "" and not self.user_cookie == "": # User have cookie
            result = check_cookie(self.cookie, self.user_cookie)
            if result:
                self.logged_in = True
                self.user = self.user_cookie
                return rx.redirect("/home")

    @rx.event
    def signin(self):
        if not self.tries > 10:
            result, token = login(self.username, self.password)
            if result:
                self.logged_in = True
                self.user = self.username
                yield rx.toast.success(f"Welcome, {self.username}.", position="top-center")
                self.cookie = token 
                self.user_cookie = self.username
                self.reset_field()
                return rx.redirect('/home')
            else:
                self.tries += 1
                self.reset_field()
                return rx.toast.error("Incorrect username or password.", position="top-center")
        else:
            self.disabled = True

            yield rx.toast.error("Login rate-limited, please try later.", position="top-center") 
            return type(self).rate_limit

    @rx.event
    def signup(self):
        if not self.username == "" or not self.password == "" :
            if check_exist(self.username) == False:
                if self.password == self.password2:
                    result, token = register(self.username, self.password)
                    if result: 
                        self.recovery_token = token
                        return rx.redirect("/security")
                    else:
                        yield rx.toast.error("Register failed, contact admin", position="top-center")
                else:
                    yield rx.toast.error("Password isn't same to confirm password.", position="top-center")
            else:
                return rx.toast.error("Username used, try another one.", position="top-center")
        else:
            return rx.toast.error("Username/Password cannot be blank.", position="top-center")

    # SECURITY 
    @rx.event
    def route_protect(self):
        if not self.cookie == "" and not self.user_cookie == "": # User have cookie
            result = check_cookie(self.cookie, self.user_cookie)
            if not result:
                return rx.redirect("/")
        else:
            return rx.redirect("/")

    @rx.event
    def route_protect_recovery(self):
        if self.recovery_token == "":
            return rx.redirect("/")


    # REDIRECT
    @rx.event
    def token_done(self):
        self.recovery_token = ""
        return self.signin()
    
    # DANGEROUS AREA
    @rx.event
    def signout(self, needed=True):
        status = logout(self.user, self.cookie)
        if status:
            self.logged_in = False
            self.user = ""
            self.cookie = ""
            self.user_cookie = ""
            self.reset_field()
            if needed: 
                yield rx.toast.success("Logged out.", position="top-center")
            else:
                yield rx.toast.success("Account deleted, goodbye.", position="top-center")
            return rx.redirect("/")
        else:
            yield rx.toast.error("404 Logout, contact admin", position="top-center")


    @rx.event
    def delete_account(self):
        if not self.password == "" : 
            if check_exist(self.user):
                result = delete_acc(self.user, self.password)
                if result == "Success":
                    yield type(self).signout(False)
                elif result == "Incorrect password":
                    yield rx.toast.warning("Wrong password.", position="top-center")
                elif result == "404":
                    yield rx.toast.error("404 Delete Account, contact admin", position="top-center")
                else:
                    yield rx.toast.error(f"Unknown error: {result}", position="top-center")

    @rx.event
    def forgot_password(self):
        if not self.password2 == "":
            result, token = forgot_password(self.username, self.password, self.password2)
            if result:
                self.recovery_token = token
                yield rx.toast.success("Password edited.", position="top-center")
                self.password = self.password2 
                return rx.redirect("/security")
            elif not result and token == "NOUSERNAME":
                yield rx.toast.error("Username not found.", position="top-center")
            else:
                yield rx.toast.error("Wrong recovery code.", position="top-center")
        else:
            yield rx.toast.error(f"New password cannot be blank.", position="top-center")