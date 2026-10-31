
import reflex as rx
from ..components.state import DashboardState  

def world_clock_card(card) -> rx.Component:
    return rx.card(
        rx.hstack(            
            rx.image(
                src= "worldclockimages/worldclock.png",
                alt= "worldclockimages",
                width= "42px",
            ),
            rx.vstack(
                rx.heading(card["name"], size="3"),
                rx.text(card["data"][0]["timezone"]),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16), variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Edit Card", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=DashboardState.save_edit_world_clock(card["id"])),
                            width="100%",
                            justify="between"
                        ),
                        rx.text(f"City: {card["data1"]}", size="2"),
                        rx.input(
                            value=DashboardState.edit_world_clock_name,
                            on_change=lambda value, cid=card["id"]: DashboardState.set_name_world_clock(value, cid),
                            placeholder = "Paris"
                        ), 
                    ),
                    side="left",
                ),
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost", hidden=True),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card['id'])),
            
            width="100%",
            height="53.8px"
        ),
        rx.vstack(
            rx.box(rx.text(card["data"][0]["time"], font_size="68px", weight="bold"),
                   display="flex",
                   align_items="center",
                   justify_content="center",
                   height="50%",
                   width="100%"),
            rx.vstack(
                rx.card(f"Universal Time Coordinates: {card["data"][0]["tz"]}", width="100%"),
                rx.hstack(
                    rx.card(f"{card["data"][0]["date"]} {card["data"][0]["time"]}", width="50%", display="flex", height="100%", align_items="center", padding="0", padding_left="12px"),
                    rx.card(f"DST: {card["data"][0]["dst"]}", width="50%", height="100%", display="flex", align_items="center", padding="0", padding_left="12px"),
                    height='50%',
                    width='100%',
                    spacing="1", 
                ),
                spacing="1",   
                width="100%",
                height="50%",
                flex="1",
            ),
            spacing="1",
            width="100%",
            height="215.2px"
        ),
        padding="8px",
        width="100%",
        height="285px",
    )



