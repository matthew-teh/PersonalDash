
import reflex as rx

class BasicState(rx.State):
    cards: list[dict] = [
        {"Name": "To-Do", "data": ["WashClothes"]},
        {"Name": "To-Do1", "data": ["WashBathroom"]},
    ]

    def reload(self):
        updated_cards = []
        for card in self.cards:
            if "To-Do" in card["Name"]:
                new_data = [{"task": "Wash Bathroom"}]
                updated_cards.append({"Name": card["Name"], "data": new_data})
            else:
                updated_cards.append(card)
        self.cards = updated_cards

def basic_widgets() -> rx.Component:
    return rx.foreach(
        BasicState.cards,
        lambda item: rx.card(
            rx.box(
                rx.vstack(
                    rx.text(item["Name"], weight="bold"),    
                    rx.text(item["data"]),           
                    width="100%",
                    height="100%",
                ),
            ),
            size="2", 
            width="calc(((100vw-1vh)/2)-0.5rem)",  # Adjusted for 2 columns!
            height="25vh",  
        )
    )
