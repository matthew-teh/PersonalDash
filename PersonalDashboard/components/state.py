import reflex as rx
from typing import TypedDict
class CardData(TypedDict):
    id: str
    type: str
    name: str
    data: list[dict[str, float]]

class DashboardState(rx.State):
    cards: list[CardData] = []

    @rx.event
    def CreateCrypto(self):
        self.cards.append({
            "id": str(len(self.cards) + 1),
            "type": "Crypto",
            "name": "NaN",
            "data": [
                {"price": 250},
                {"price": 680},
                {"price": 440},
                {"price": 280},
                {"price": 210},
            ],
        })

    @rx.event
    def UpdateCrypto(self, card_id: str):
        for card in self.cards:
            if card["id"] == card_id:
                card["data"] =  [{"price": 200},{"price": 690},{"price": 400},{"price": 250},{"price": 280},]
                break
    
    @rx.event
    def DeleteCrypto(self, card_id: str):
        for card in self.cards:
            if card["id"] == card_id:
                self.cards.remove(card)