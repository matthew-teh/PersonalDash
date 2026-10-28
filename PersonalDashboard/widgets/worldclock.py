
import reflex as rx
from ..components.state import DashboardState  

def world_clock_card(card) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.box(
                rx.image(
                    src= "worldclockimages/worldclock.png",
                    alt= "worldclockimages",
                    width= "42px",
                ),
                height="60px",
            ),
            rx.vstack(
                rx.heading("Penang Time", size="3"),
                rx.text("Asia/Kuala Lumpur"),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16), variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Edit Card", size="3", weight="bold"),
                            rx.button(rx.icon("check"), variant="ghost"),
                            width="100%",
                            justify="between"
                        ),
                        rx.text("City", size="2"),
                        rx.input(
                            #value,
                            #on_change
                            placeholder = "Paris"
                        ),  
                        rx.text(f"Recommended: "),
                    ),
                    side="left",
                ),
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost"),
            rx.button(rx.icon("trash_2", size=16), variant="ghost"),
        
            justify='start',
            width="100%",
            height="20%"
        ),
        rx.separator(), # Delet ewhen prod
        rx.vstack(
            rx.text("24:00:05", font_size="48px", weight="bold"),
            rx.spacer(),
            rx.hstack(rx.card("Test", width="50%"), 
                      rx.card("Test", width="50%"),
                      width="100%", spacing="1"),    
            rx.hstack(rx.card("Test", width="50%"), 
                      rx.card("Test", width="50%"), 
                      width="100%", spacing="1"),    
            align="center",
            spacing="1",
            width="100%",
            height="80%"
        ),
        padding="0.8rem",
        width="100%",
        height="30vh",
    )



