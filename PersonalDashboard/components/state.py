import reflex as rx
import random
import asyncio
import json
from typing import TypedDict
from ..api.crypto import GetPrice
from ..api.aggcrypto import candle
class CardData(TypedDict):
    id: str
    type: str
    name: str
    data: list[dict[str, float]]
    data1: str

class DashboardState(rx.State):
    cardsJson: str = rx.LocalStorage("[]", name="dashboard_cards", sync=True)
    cooldown: bool = False
    streaming: bool = False
    tasks: dict = {}
    EditName: str = ""
    EditWindow: str = ""
    # ---- RX VAR HERE ----
    @rx.var
    def cards(self) -> list[CardData]:
        try:
            data = json.loads(self.cardsJson)
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
    async def DelayReset(self):
        await asyncio.sleep(5)
        async with self:
            self.cooldown = False

    @rx.event(background=True)
    async def LiveUpdates(self):
        if self.streaming: return
        async with self: self.streaming = True

        while self.streaming:
            async with self:
                pairs = set()
                for card in self.cards:
                    if card["name"] and card["type"] == "AggCrypto":
                        pairs.add(card["name"])
            for pair in pairs:
                if pair not in self.tasks:
                    self.tasks[pair] = asyncio.create_task(self.runcandle(pair))

            for pair in set(self.tasks.keys() - pairs):
                self.tasks[pair].cancel()
                del self.tasks[pair]
                print(f"Stop stream {pair}")
            await asyncio.sleep(1)

    async def runcandle(self, pair: str):
        try:
            await candle(pair, self.candleCard)
        except asyncio.CancelledError:
            print(f"Task cancelled {pair}")
    async def candleCard(self, pair: str, data: list):
        async with self:
            for card in self.cards:
                if card["name"] == pair:
                   card["data"] = data
                   break
            self.cardsJson = json.dumps(self.cards) 
    # ---- RX EVENT HERE ----
    @rx.event 
    def MakeCards(self, card):
        if card["type"] == "Crypto":
            self.cards.append({
                "id": str(len(self.cards) + 1),
                "type": "Crypto",
                "name": "NaN",
                "data": [{"price": random.randint(0, 100)} for _ in range(25)],
                "data1" : "15m",
            })
        elif card["type"] == "AggCrypto":
            self.cards.append({
                "id": str(len(self.cards) + 1),
                "type": "AggCrypto",
                "name": "NaN",
                "data": [{"price": random.randint(0, 100)} for _ in range(25)],
                "data1" : "",
            })
        self.cardsJson = json.dumps(self.cards)
    

    @rx.event
    async def UpdateAll(self):
        if self.cooldown: return rx.toast("Reload All: Cooling Down", style={"background-color" :"#403D39"})
        self.cooldown = True
        for card in self.cards:
            if card["type"] == "Crypto":
                await self.UpdateCrypto(card["id"], True)
        return DashboardState.DelayReset

    @rx.event
    async def UpdateCrypto(self, card_id: str, passthrough=False):
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
                        card["data"] = GetPrice(symbol=card["name"],window=card["data1"])
                        self.cardsJson = json.dumps(list(self.cards))
                    except Exception as e: 
                        print(f"ERR : {e}")
                else:
                    return rx.toast("Cannot Update Data, no symbol set.", style={"background-color" :"#403D39"})
                break
        if not found:
            self.cooldown = False
            return
        return DashboardState.DelayReset

    @rx.event
    def DeleteCrypto(self, card_id: str):
        for card in self.cards:
            if card["id"] == card_id:
                self.cards.remove(card)
        self.cardsJson = json.dumps(list(self.cards))



    @rx.event
    async def SaveEdit(self, card_id: str, value={}):
        for card in self.cards:
            if card["id"] == card_id and card["type"] == "AggCrypto":
                if not isinstance(value, dict) and not card["name"] == "NaN":
                    return
                elif self.EditName:
                    card["name"] = self.EditName
                    self.EditName = "" 
                    self.cardsJson = json.dumps(list(self.cards))
                    return type(self).LiveUpdates
            elif card["id"] == card_id and card["type"] == "Crypto":
                if not isinstance(value, dict) and not card["name"] == "NaN":
                    card["data1"] = value
                    return type(self).UpdateCrypto(card_id, False)
                elif self.EditName:
                    card["name"] = self.EditName
                    self.EditName = ""
                    self.cardsJson = json.dumps(list(self.cards))
                    return type(self).UpdateCrypto(card_id, True)
                else:
                    return rx.toast("Cannot Update Data, no symbol set.", style={"background-color" :"#403D39"})

        
        

    @rx.event
    def SetEditName(self, value: str):
        self.EditName = value

    @rx.event
    def SetWindow(self, value: str):
        self.EditWindow = value