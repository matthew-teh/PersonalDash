import reflex as rx
import json
import uuid
import asyncio
from typing import TypedDict
from ..api.crypto import get_price
from ..api.worldclock import get_time, get_timezone
from ..api import weather

class CardData(TypedDict):
    id: str
    type: str
    name: str
    data: list[dict[str, str]]
    data1: str
    data2: float

class DashboardState(rx.State):
    cards_json: str = rx.LocalStorage("[]", name="dashboard_cards", sync=True)
    cooldown: bool = False
    is_updating = False
    # ---- RX VAR HERE ----
    @rx.var
    def cards(self) -> list[CardData]:
        try:
            data = json.loads(self.cards_json)
            if not isinstance(data, list):
                return []
            valid_cards = []
            for item in data:
                if isinstance(item, dict) and "id" in item:
                    valid_cards.append(item)
            return valid_cards
        except (json.JSONDecodeError, TypeError):
            return []
        
    # ---- RX EVENT BACKGROUND HERE ----
    @rx.event(background=True)
    async def delay_reset(self):
        await asyncio.sleep(2.5)
        async with self:
            self.cooldown = False

    # ---- RX WORLD CLOCK SPECIFIC EVENT HERE ----
    edit_world_clock_name = ""

    @rx.event
    def update_world_clock(self):
        for card in self.cards:
            if card["type"] == "world_clock":
                name = card["data"][0]["timezone"].replace(", ", "/").replace(" ", "_")
                card["data"] = get_time(name)
        self.dump_json(self.cards)
        
    @rx.event
    def set_name_world_clock(self, value, card_id):
        self.edit_world_clock_name = value
        for card in self.cards:
            if card["id"] == card_id:
                card["data1"] = get_timezone(self.edit_world_clock_name).replace("_", " ")
        self.dump_json(self.cards)

    @rx.event
    def save_edit_world_clock(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                card["name"] = card["data1"].split("/")[1]
                card["data"] = get_time(card["data1"].replace(" ", "_"))
                card["data1"] = ""
                self.edit_world_clock_name = ""
                
        self.dump_json(self.cards)

    # ---- RX WEATHER SPECIFIC EVENT HERE ----
    edit_name_weather: str = ""
    @rx.event
    def save_edit_weather(self, card_id):
        for card in self.cards:
            if card_id == card["id"]:
                card["name"] = card["data1"]
                card["data1"] = ""
                self.edit_name_weather = ""
                self.dump_json(self.cards)
                return type(self).update_weather(card_id)
            
    @rx.event
    def update_weather(self, card_id):
        for card in self.cards:
            if card_id == card["id"]:
                name, datas = weather.get_data(card["name"])
                if name == "NaN":
                    return rx.toast("Cannot Update Data, invalid location", style={"background-color" :"#403D39"})
                else:
                    card["data"] = datas
                    self.dump_json(self.cards)
        
    @rx.event
    def set_name_weather(self, value: str, card_id):
        self.edit_name_weather = value
        for card in self.cards:
            if card["id"] == card_id:
                card["data1"] = weather.get_name(value)
                self.dump_json(self.cards)
                
    # ---- RX CRYPTO SPECIFIC EVENT HERE ----
    edit_name_crypto: str = ""
    edit_window_crypto: str = ""

    @rx.event
    def save_edit_crypto(self, card_id: str, value={}):
        for card in self.cards:
            if card["id"] == card_id and card["type"] == "crypto":
                if not isinstance(value, dict) and not card["name"] == "NaN":
                    card["data1"] = value
                    return type(self).update_crypto(card_id, False)
                elif self.edit_name_crypto:
                    card["name"] = self.edit_name_crypto
                    self.edit_name_crypto = ""
                    self.dump_json(self.cards)
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
    def update_crypto(self, card_id: str, passthrough=False):
        if passthrough:
            self.cooldown = False 
        if self.cooldown: return rx.toast("Cooling Down", style={"background-color" :"#403D39"})
        self.cooldown = True
        found = False
        for card in self.cards:
            if card["id"] == card_id:
                found = True
                if card["name"] != "NaN":
                    try:
                        result = get_price(symbol=card["name"],window=card["data1"])
                        card["data"] = result 
                        card["data2"] = -round(((float(result[0]["price"]) - float(result[-1]["price"])) / float(result[0]["price"])) * 100, 2)
                        self.dump_json(self.cards)
                    except Exception as e: 
                        print(f"ERR : {e}")
                        return rx.toast("Wrong Symbol, try ETHUSDT or BTCUSDT, aim something that ending with USDT", style={"background-color" :"#403D39"})
                else:
                    return rx.toast("Cannot Update Data, no symbol set.", style={"background-color" :"#403D39"})
                break
        if not found:
            self.cooldown = False
        return DashboardState.delay_reset
    
    
    def price_diff(self, card: CardData) -> str:
        first = float(card["data"][0]["price"])
        last = float(card["data"][-1]["price"])
        change = -round(((first - last) / first) * 100, 2)
        return str(change)

    # ---- RX SETTING SPECIFIC EVENT HERE ----
    edit_column = "4"

    @rx.event
    def set_column(self, value):
        self.edit_column = value

    # ---- RX ALL EVENT HERE ----
    @rx.event 
    def create_card(self, card):
        card_id =  str(uuid.uuid4())
        if card == "crypto":
            self.cards.append({
                "id": card_id,    
                "type": "crypto",
                "name": "BTCUSDT",
                "data": [{}],
                "data1": "15m",
                "data2": 0
            })
            self.dump_json(self.cards)
            yield
            self.update_crypto(card_id, True)

        if card == "weather":
            # Format [{"lat": lat, "lng": lng, "relative_humid": rlthumid, "precip", precip, "wetcode", wetcode, "temp", temp, "windspd", windspd, "feeltemp", feeltemp}]
            self.cards.append({
                "id": card_id,
                "type": "weather",
                "name": "London",
                "data": [{}],
                "data1": "",
                "data2": 0
            })
            self.dump_json(self.cards)
            yield
            self.update_weather(card_id)

        if card == "world_clock":
            result = get_time('Asia/Singapore')
            self.cards.append({
                "id": card_id,
                "type": "world_clock",
                "name": f"{result[0]["timezone"].split(", ")[1]} Time",
                "data": result, 
                "data1": "",
                "data2": 0
            })
            self.dump_json(self.cards)

    @rx.event
    def update_all(self):
        if self.cooldown: return rx.toast("Reload All: Cooling Down", style={"background-color" :"#403D39"})
        self.is_updating = True
        self.cooldown = True
        yield
        for card in self.cards:
            if card["type"] == "crypto":
                self.update_crypto(card["id"], True)
            if card["type"] == "weather":
                self.update_weather(card["id"])
        rx.toast("Done Refresh.", style={"background-color" :"#403D39"})
        self.is_updating= False
        yield
        return DashboardState.delay_reset()

    @rx.event
    def delete_card(self, card_id):
        for card in self.cards:
            if card_id == card["id"]:
                self.cards.remove(card)
        self.dump_json(self.cards)

    @rx.event
    def delete_all(self):
        self.cards.clear()
        self.dump_json(self.cards)

    @rx.event
    def dump_json(self, cards):
        self.cards_json = json.dumps(cards)

