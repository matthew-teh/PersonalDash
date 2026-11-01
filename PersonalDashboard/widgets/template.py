import reflex as rx
from ..components.state import DashboardState
# REFINED FROM WEATHER CARD
def weather_card(card) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.image(
                src=card["data"][0]["useimg"],
                height= "42px",
            ),
            rx.vstack(
                rx.heading(card["name"], size="3"),
                rx.text(card["data"][0]["wetcode"]),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16), variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Edit Card", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=DashboardState.save_edit_weather(card["id"])),
                            width="100%",
                            justify="between",
                        ),
                        rx.text(f"City: {card["data1"]}", size="2"),
                        rx.input(
                            value=DashboardState.edit_name_weather,
                            on_change=lambda val, cid=card["id"]: DashboardState.set_name_weather(val, cid),
                            placeholder="New York",
                        ),
                    ),
                    side="left",
                ),
                width="100px",
                
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost", on_click=DashboardState.update_weather(card["id"])),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card["id"])),
            width="100%",
            height="53.8px",
        ),
        rx.hstack(
            width="100%",
            height="215.2px",
            spacing="0",
        ),
        padding="8px",
        width="100%",
        height="285px",
    )