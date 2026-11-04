import reflex as rx
from ..components.state import DashboardState

def sidebar() -> rx.Component:
    return rx.box(
        rx.drawer.root(
            rx.drawer.trigger(rx.button(rx.icon("plus", size=20), variant='ghost')),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.scroll_area(
                        rx.hstack(rx.text("Add Cards", weight="bold", size="4"), rx.spacer(), rx.drawer.close(rx.icon("x", size=30)), width="100%",align='center'),
                        rx.vstack(
                            rx.card(
                                rx.vstack(
                                    rx.text("Tic Tac Toe - Terra Special"),
                                    rx.image(
                                        src=rx.color_mode_cond(light="sidebarimages/light_tic_tac_toe.png", dark="sidebarimages/dark_tic_tac_toe.png"),
                                        alt="tictactoeimage",
                                        border_radius="5px"),
                                    spacing="1",
                                    align="center",
                                ),
                                on_click=DashboardState.create_card("tic_tac_toe"), 
                            ),
                            rx.card(
                                rx.vstack(
                                    rx.text("Crypto Card"),
                                    rx.image(src=rx.color_mode_cond(light="sidebarimages/light_crypto.png", dark="sidebarimages/dark_crypto.png"),
                                            alt="cryptoimage",
                                            border_radius="5px"),
                                    spacing="1",
                                    align="center",
                                ),
                                on_click=DashboardState.create_card("crypto"),
                            ),
                            rx.card(
                                rx.vstack(
                                    rx.text("Weather Card"),
                                    rx.image(src=rx.color_mode_cond(light="sidebarimages/light_weather.png", dark="sidebarimages/dark_weather.png"),
                                            alt="weatherimage",
                                            border_radius="5px"),
                                    spacing="1",
                                    align="center",
                                ),
                                on_click=DashboardState.create_card("weather"),
                            ),
                            rx.card(
                                rx.vstack(
                                    rx.text("World Clock Card"),
                                    rx.image(
                                        src=rx.color_mode_cond(light="sidebarimages/light_world_clock.png", dark="sidebarimages/dark_world_clock.png"),
                                        alt="worldclockimage",
                                        border_radius="5px"),
                                    spacing="1",
                                    align="center",
                                ),
                                on_click=DashboardState.create_card("world_clock"), 
                            ),
                            rx.card(
                                rx.vstack(
                                    rx.text("Pomodoro Timer Card"),
                                    rx.image(
                                        src=rx.color_mode_cond(light="sidebarimages/light_pomodoro.png", dark="sidebarimages/dark_pomodoro.png"),
                                        alt="pomodoroimage",
                                        border_radius="5px"),
                                    spacing="1",
                                    align="center",
                                ),
                                on_click=DashboardState.create_card("pomodoro"), 
                            ),
                            rx.card(
                                rx.vstack(
                                    rx.text("Quick Notes"),
                                    rx.image(
                                        src=rx.color_mode_cond(light="sidebarimages/light_quick_notes.png", dark="sidebarimages/dark_quick_notes.png"),
                                        alt="pomodoroimage",
                                        border_radius="5px"),
                                    spacing="1",        
                                    align="center",
                                ),
                                on_click=DashboardState.create_card("quick_notes"), 
                            ),
                            width="100%",
                            height="100%",       
                            spacing="2",
                        ),
                    ),
                        left="auto",   
                        position="fixed",
                        height="100vh",  
                        width="20em",
                        padding="0.5em",
                        align="start",
                        
                        background_color = rx.color_mode_cond(light=rx.color('gray', 4), dark=rx.color('gray', 4)),
                )
            ),
            direction="right",
        ),
        
    )