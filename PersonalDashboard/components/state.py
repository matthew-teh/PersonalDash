import reflex as rx
import random
from typing import TypedDict


class CardData(TypedDict):
    id: str
    type: str
    name: str
    crypto: str
    data: list[dict[str, float]]

class DashboardState(rx.State):
    cards: list[CardData] = []
    EditName: str = ""
    EditCrypto: str = ""
    editing_card_id: str = ""

    @rx.event
    def CreateCrypto(self):
        self.cards.append({
            "id": str(len(self.cards) + 1),
            "type": "Crypto",
            "name": "NaN",
            "crypto" : "",
            "data": [{"price": random.randint(0, 100)} for _ in range(25)]
        })

    @rx.event
    def UpdateCrypto(self, card_id: str):
        for card in self.cards:
            if card["id"] == card_id:
                card["data"] =  [{"price": random.randint(0, 100)} for _ in range(25)]
                break
    
    @rx.event
    def DeleteCrypto(self, card_id: str):
        for card in self.cards:
            if card["id"] == card_id:
                self.cards.remove(card)

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
                self.editing_card_id = card_id
                self.EditName = card["name"]
                self.EditCrypto = card["crypto"]
                break

    @rx.event
    def SaveEdit(self, card_id):

        for card in self.cards:
            if card["id"] == card_id:
                card["name"] = self.EditName
                card["crypto"] = self.EditCrypto
                self.EditName, self.EditCrypto = "","" # Clear after set 
                break
        
        