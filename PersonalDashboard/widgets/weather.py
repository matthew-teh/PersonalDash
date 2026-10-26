import reflex as rx
from ..components.state import DashboardState

def weather_card(card) -> rx.Component:
    return rx.card(
         rx.box(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.image(src=f"{card["data"][0]["useimg"]}", 
                                width="60px", 
                                height="auto",
                                object_fit="contain",
                                object_position="center",
                                ),
                            rx.vstack(
                                rx.heading(card["name"], size="3"),
                                rx.text(card["data"][0]["wetcode"]),
                                spacing="0",
                            ),
                        rx.spacer(),
                        rx.hover_card.root(
                            rx.hover_card.trigger(
                                rx.button(
                                    rx.icon("settings", size=16),
                                    variant="ghost",
                                    pointer_events="auto",
                                ),
                            ),
                            rx.hover_card.content(
                                rx.vstack(
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text("Edit Card", size="3", weight="bold"),
                                            spacing="0",
                                        ),
                                        rx.spacer(),
                                        rx.button(
                                            rx.icon("check"),
                                            variant="ghost",
                                            on_click=DashboardState.save_edit_weather(card["id"]),
                                            pointer_events="auto",
                                        ),
                                        justify="between",
                                        width="100%",
                                    ),
                                    rx.text("Location", size="2"),
                                    rx.input(
                                        value=DashboardState.edit_name_weather,
                                        on_change=lambda value, cid=card["id"]: DashboardState.set_name_weather(value, cid),
                                        placeholder="Los Angeles",
                                        width="100%",
                                    ),
                                    rx.text(f"Recommended: {card["data1"]}", size="2"),
                                ),
                                pointer_events="auto",
                            ),
                        ),
                        rx.button(
                            rx.icon("refresh_cw", size=16),
                            variant="ghost",
                            on_click=DashboardState.update_weather(card["id"]),
                            pointer_events="auto",
                        ),
                        rx.button(
                            rx.icon("trash_2", size=16),
                            variant="ghost",
                            on_click=DashboardState.delete_card(card["id"]),
                            pointer_events="auto",
                        ),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.hstack(
                            rx.text(f"{round(card["data"][0]["temp"])}",font_size="120px",weight="bold"),
                            rx.text("℃"),
                            width="50%",
                            height="100%",
                            align="center",
                            justify="center",
                        ),
                        rx.vstack(
                            rx.card(
                                rx.vstack(
                                    rx.text(f"Feels Like", font_size="14px"),
                                    rx.text(f"{round(card["data"][0]["feeltemp"])}℃",size="7", weight="bold"),
                                    spacing="2",
                                    align="center",
                                    justify="center",   
                                ), width="100%", height="50%"),
                            rx.card(
                                rx.vstack(
                                    rx.text(f"Wind speed", font_size="14px"),
                                    rx.text(f"{round(card["data"][0]["windspd"])}km/h",size="7", weight="bold"),
                                    spacing="2",
                                    align="center",
                                ), width="100%", height="50%"),
                            width="25%",
                            height="100%",
                            spacing="1",
                            align="center"
                        ),
                        rx.vstack(
                            rx.card(
                                rx.vstack(
                                    rx.text(f"Humidity", font_size="14px"),
                                    rx.text(f"{round(card["data"][0]["relative_humid"])}%",size="7", weight="bold"),
                                    spacing="2",
                                    align="center",
                                    justify="center",   
                                ), width="100%", height="50%"),
                            rx.card(
                                rx.vstack(
                                    rx.text(f"Cloud Cover", font_size="14px"),
                                    rx.text(f"{round(card["data"][0]["cloudcvr"])}%",size="7", weight="bold"),
                                    spacing="2",
                                    align="center",
                                ), width="100%", height="50%"),
                            width="25%",
                            height="100%",
                            spacing="1",
                            align="center"
                        ),
                        
                        spacing="1",
                        width="100%",
                        height="100%",
                    ),
                    spacing="1",
                    height="100%",
                    width="100%",

                ),
                width="100%",
                height="100%",
            ),
            width="100%",
            height="100%",
        ),
        size="1",
        width="100%",
        height="30vh",
    )