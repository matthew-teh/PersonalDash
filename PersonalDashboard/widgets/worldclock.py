
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
                rx.heading(card["name"], size="3"),
                rx.text(card["data"]["timezone"].replace("/", ", ")),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16), variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Edit Card", size="3", weight="bold"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=DashboardState.save_edit_world_clock(card["id"])),
                            width="100%",
                            justify="between"
                        ),
                        rx.text("City", size="2"),
                        rx.input(
                            value=DashboardState.edit_world_clock_name,
                            on_change=lambda value, cid=card["id"]: DashboardState.set_name_world_clock(value, cid),
                            placeholder = "Paris"
                        ), 
                        rx.text(f"Search: {card["data1"]}"),
                    ),
                    side="left",
                ),
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost", hidden=True),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card['id'])),
            
            justify='start',
            width="100%",
            height="20%"
        ),
        rx.vstack(
            rx.box(rx.text(card["data"]["time"], font_size="68px", weight="bold"),
                   display="flex",
                   align_items="center",
                   justify_content="center",
                   height="50%",
                   width="100%"),
            rx.vstack(
                rx.card(f"Universal Time Coordinates: {card["data"]["tz" ]}", width="100%"),
                rx.hstack(
                    rx.card(f"{card["data"]["date"]} {card["data"]["time"]}", width="50%"),
                    rx.card(f"DST: {card["data"]["dst"]}", width="50%"),
                    height='50%',
                    width='100%',
                    spacing="1", 
                ),
                spacing="1",   
                width="100%",
                height="50%",
            ),
            spacing="1",
            width="100%",
            height="80%"
        ),
        padding="0.8rem",
        width="100%",
        height="30vh",
    )



