import reflex as rx
from ..components.state import DashboardState

def pomodoro_card(card) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.icon("apple", height="42px", width="42px", color='red'),
            rx.vstack(
                rx.heading(card["name"], size="3"),
                rx.match(
                    card["data"][0]["mode"],
                    ("pomodoro", rx.text("Pomodoro - Focus Mode")),
                    ("short", rx.text("Short Break - Take a sip of coffee")),
                    ("long", rx.text("Long Break - Get a snack")),
                ),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16), variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Edit Card", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=DashboardState.save_edit_pomodoro(card["id"])),
                            width="100%",   
                            justify="between",
                        ),
                        
                        rx.text("Pomodoro Time (minutes)"),
                        rx.input(
                            value=DashboardState.pomodoro,
                            on_change=DashboardState.edit_pomodoro_pomodoro,
                            placeholder="25",
                            width="100%",
                        ),
                        rx.text("Short and long breaks"),
                        rx.hstack(
                            rx.input(
                                value=DashboardState.short,
                                on_change=DashboardState.edit_short_pomodoro,
                                width="50%",
                                placeholder="5",
                            ),
                            rx.input(
                                value=DashboardState.long,
                                on_change=DashboardState.edit_long_pomodoro,
                                width="50%",
                                placeholder="15"
                            ),
                            width="100%", 
                        ),
                    ),
                    side="left",
                    width="250px",
                )
            ),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card["id"])),
            width="100%",
            height="53.8px",
        ),
        rx.vstack(
            # 164 without buttons
            # rxcond here
            rx.text(card["data"][0]["timing"], font_size="132px", weight="bold"),
            rx.hstack(
                rx.button(rx.icon("play"), variant="ghost", on_click=DashboardState.command_pomodoro(card["id"], "start")),
                rx.button(rx.icon("pause"), variant="ghost", on_click=DashboardState.command_pomodoro(card["id"], "stop")),
                rx.button(rx.icon("timer-reset"), variant="ghost", on_click=DashboardState.command_pomodoro(card["id"], "reset")),
                spacing="5",
            ),
            align_items="center",
            justify="center",
            width="100%",
            height="215.2px",
            spacing="0",
        ),

        padding="8px",
        width="100%",
        height="285px"
    )
# Expected config : Pomodoro, Short Break, Long Break
# Needed : pomodoro, short, long, times ( short break ) , initial time, started?
