import reflex as rx
import random
import asyncio
import json
import time
from typing import TypedDict
from ..api.crypto import GetPrice

class CardData(TypedDict):
    id: str
    type: str
    name: str
    data: list[dict[str, float]]

class DashboardState(rx.State):
    cardsJson: str = rx.LocalStorage("[]", name="dashboard_cards", sync=True)
    cooldown: bool = False
    EditName: str = ""
    EditCrypto: str = ""
    EditingCardId: str = ""

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


    @rx.event
    def save_card(self):
        current_cards = self.cards
        for card in current_cards:
            if card["id"] == self.EditingCardId:
                card["name"] = self.EditName
                break
        self.cards_json = json.dumps(current_cards)

    @rx.event
    def CreateCrypto(self):
        card = list(self.cards)
        card.append({
            "id": str(len(self.cards) + 1),
            "type": "Crypto",
            "name": "NaN",
            "data": [{"price": random.randint(0, 100)} for _ in range(25)]
        })
        self.cardsJson = json.dumps(card)

    @rx.event
    async def UpdateAll(self):
        if self.cooldown: return
        self.cooldown = True
        for card in self.cards:
            if card["type"] == "Crypto":
                await self.UpdateCrypto(card["id"], True)
        return DashboardState.DelayReset
    
    @rx.event(background=True)
    async def DelayReset(self):
        await asyncio.sleep(5)
        async with self:
            self.cooldown = False

    @rx.event
    async def UpdateCrypto(self, card_id: str, passthrough=False):
        if passthrough: self.cooldown = False
        if self.cooldown: return  
        self.cooldown = True
        found = False
        for card in self.cards:
            if card["id"] == card_id:
                found = True
                if card["name"] != "NaN":
                    try:
                        card["data"] = GetPrice(symbol=card["name"])
                        self.cardsJson = json.dumps(list(self.cards))
                    except Exception as e: 
                        print(f"ERR : {e}")
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
    def UpdateEditName(self, value: str):
        self.EditName = value

    @rx.event
    def UpdateEditCrypto(self, value: str):
        self.EditCrypto = value
    
    @rx.event
    def StartEdit(self, card_id: str):
        for card in self.cards:
            if card["id"] == card_id:
                self.EditingCardId = card_id
                self.EditName = card["name"]
                break

    @rx.event
    def SaveEdit(self, card_id):
        for card in self.cards:
            if card["id"] == card_id:
                card["name"] = self.EditName
                self.EditName, self.EditCrypto, self.EditingCardId = "", "", "" # Clear after set 
                break
        self.cardsJson = json.dumps(list(self.cards))