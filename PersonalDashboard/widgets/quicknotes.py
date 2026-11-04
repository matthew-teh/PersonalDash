import reflex as rx
from ..components.state import DashboardState

def quick_notes(card) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.color_mode_cond(
                light = rx.image(src="quicknotesimages/quick_notes_light.svg", height="42px", width="42px"),
                dark  = rx.image(src="quicknotesimages/quick_notes_dark.svg", height="42px", width="42px")
            ),
            rx.vstack(
                rx.heading(card["name"], size="3"),
                rx.text("A text area to note, auto saved.   "),
                spacing="0",
            ),
            rx.spacer(),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card["id"])),
            width="100%",
            height="53.8px",
        ),
        rx.hstack(
            rx.text_area(
                placeholder="Start typing here...",
                value = card["data"][0]["text"],
                on_focus=DashboardState.start_editing(card["id"], card["data"][0]["text"]),
                on_change=DashboardState.live_update,
                width="100%",
                height="100%",
            ),
            width="100%",
            height="215.2px",
            spacing="0",
        ),
        padding="8px",
        width="100%",
        height="285px",
    )