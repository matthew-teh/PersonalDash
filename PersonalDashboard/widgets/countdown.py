import reflex as rx
from ..components.state import DashboardState


def countdown_card(card) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.color_mode_cond(
                light = rx.image(src="lucideicons/clock-fading-light.svg", height="42px", width="42px"),
                dark  = rx.image(src="lucideicons/clock-fading-dark.svg", height="42px", width="42px")
        ),
        rx.vstack(
            rx.heading(card["name"], size="3"),
            rx.text("This week of terra ends in: "),
            spacing="0",
        ),
        rx.spacer(),
        rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card["id"])),
        width="100%",
        height="53.8px",
        ),
        rx.vstack(
            rx.center(
                rx.text(card["data"][0]["time"], font_size="110px", weight="bold"),
                height="100%",
                width="100%",
            ),
            rx.center(
                rx.hstack(
                    rx.text("Hours"),
                    rx.text("Minutes"),
                    rx.text("Seconds"),
                    width="80%",
                    justify="between",
                ),
                height="100%",
                width="100%"
            ),
            width="100%",
            height="215.2px",
            spacing="0",
        ),
        padding="8px",
        width="100%",
        height="285px",
    )