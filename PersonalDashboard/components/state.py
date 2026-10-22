import reflex as rx
import random
import json
from typing import TypedDict, Any
from ..api.crypto import get_price
import asyncio


class CardData(TypedDict):
    id: str
    type: str
    name: str
    data: list[dict[str, float]]
    data1: str

class DashboardState(rx.State):
    cards_json: str = rx.LocalStorage("[]", name="dashboard_cards", sync=True)
    cooldown: bool = False

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
        
    # ---- RX WEATHER SPECIFIC EVENT HERE ----

    # ---- RX crypto SPEICFIC EVENT HERE ----
    edit_name_crypto: str = ""
    edit_window_crypto: str = ""

    @rx.event
    def save_edit_crypto(self, card_id: str, value={}):
        for card in self.cards:
            if card["id"] == card_id and card["type"] == "crypto":
                print("got")
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
            print("passthrough")
        if self.cooldown: return rx.toast("Cooling Down", style={"background-color" :"#403D39"})
        self.cooldown = True
        found = False
        for card in self.cards:
            if card["id"] == card_id:
                found = True
                if card["name"] != "NaN":
                    try:
                        card["data"] = get_price(symbol=card["name"],window=card["data1"])
                        self.dump_json(self.cards)
                    except Exception as e: 
                        print(f"ERR : {e}")
                else:
                    return rx.toast("Cannot Update Data, no symbol set.", style={"background-color" :"#403D39"})
                break
        if not found:
            self.cooldown = False
        return DashboardState.delay_reset

    @rx.event
    def delete_crypto(self, card_id: str):
        for card in self.cards:
            print(card)
            if card["id"] == card_id and card["type"] == "crypto":
                self.cards.remove(card)
        self.cards_json = json.dumps(self.cards_json)
    
    # ---- RX ALL EVENT HERE ----
    @rx.event 
    def create_card(self, card):
        if card["type"] == "crypto":
            self.cards.append({
                "id": str(len(self.cards) + 1),
                "type": "crypto",
                "name": "NaN",
                "data": [{"price": random.randint(0, 100)} for _ in range(25)],
                "data1" : "15m",
            })
            self.dump_json(self.cards)
        if card["type"] == "weather":
            self.cards.append({
                "id": str(len(self.cards) + 1),
                "type": "weather",
                "name": "NaN",
                "data": [{}],
                "data1" : "",
            })
            self.dump_json(self.cards)

    @rx.event
    def update_all(self):
        if self.cooldown: return rx.toast("Reload All: Cooling Down", style={"background-color" :"#403D39"})
        self.cooldown = True
        for card in self.cards:
            if card["type"] == "crypto":
                self.update_crypto(card["id"], True)
        return DashboardState.delay_reset()

    @rx.event
    def delete_all(self):
        for card in self.cards:
            self.cards.remove(card)
            print("Removed card")
        self.dump_json(self.cards)

    @rx.event
    def delete_card(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                self.cards.remove(card)
        self.dump_json(self.cards)

    @rx.event
    def dump_json(self, cards):
        self.cards_json = json.dumps(cards)

