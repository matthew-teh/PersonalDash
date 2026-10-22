import reflex as rx
from ..components.state import DashboardState

def weather_card(card) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.icon("map-pin", size=16),
                    rx.text("Los Angeles", size="3"),
                    align_items = "center",
                    spacing="1"
                ),
                rx.spacer(),
                rx.text("35°", font_size="120px", weight= "bold"),  
                justify = "between",
                height="100%",
                width="45%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.card(rx.text("Card 1"), width="50%", height="100%"),
                    rx.card(rx.text("Card 2"), width="50%", height="100%"),
                    height="50%",
                    width="100%"
                ),
                rx.hstack(
                    rx.card(rx.text("Card 3"), width="50%", height="100%"),
                    rx.card(rx.text("Card 4"), width="50%", height="100%"),
                    height="50%",
                    width="100%"
                ),
                height="100%",
                width="65%",
            ),
            height="100%",
            width="100%",
        ),
        size="1",
        width="100%",
        height="30vh",
        background_color="#090C08",
    )
 
   