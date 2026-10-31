import reflex as rx
from ..components.state import DashboardState

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
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost", on_click=DashboardState.update_weather(card["id"])),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card["id"])),
            width="100%",
            height="53.8px",
        ),
        rx.hstack(
            rx.hstack(
                rx.text(f"{card["data"][0]["temp"]}", font_size="120px", weight="bold"),
                rx.text("℃"),
                width="50%",
                height='100%',
                align="center",
                justify="center",
            ),
            rx.grid(
                rx.card(
                    rx.flex(rx.text("Feels Like", font_size="14px"), align_items="center", justify_content="center", width="100%", height="15%"),
                    rx.flex(
                        rx.text(f"{card["data"][0]["feeltemp"]}", font_size="42px", weight="bold"), 
                        rx.text("℃", font_size="14px"),
                        align_items="center", justify_content="center", width="100%", height="85%"),
                    height="100%"
                ),
                rx.card(
                    rx.flex(rx.text("Humidity", font_size="14px"), align_items="center", justify_content="center", width="100%", height="15%"),
                    rx.flex(rx.text(f"{card["data"][0]["relative_humid"]}", font_size="42px", weight="bold"), 
                            rx.text("%", font_size="14"), 
                            align_items="center", justify_content="center", width="100%", height="85%"),
                    height="100%"
                ),
                rx.card(
                    rx.flex(rx.text("Wind speed", font_size="14px"), align_items="center", justify_content="center", width="100%", height="15%"),
                    rx.flex(rx.text(f"{card["data"][0]["windspd"]}", font_size="42px", weight="bold"), 
                            rx.text("km/h", font_size="14px"), 
                            align_items="center", justify_content="center", width="100%", height="85%"),
                    height="100%"
                ),
                rx.card(
                    rx.flex(rx.text("Cloud Cover", font_size="14px"), align_items="center", justify_content="center", width="100%", height="15%"),
                    rx.flex(rx.text(f"{card["data"][0]["cloudcvr"]}", font_size="42px", weight="bold"), 
                            rx.text("%", font_size="14px"), 
                            align_items="center", justify_content="center", width="100%", height="85%"),
                    height="100%"
                ),
                columns="2",
                width="50%",
                height="100%",
                gap="0.25rem",
            ),
            width="100%",
            height="215.2px",
            spacing="0",
        ),
        padding="8px",
        width="100%",
        height="285px",
    )