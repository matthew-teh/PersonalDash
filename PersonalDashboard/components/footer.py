import reflex as rx
from ..components.state import DashboardState, ServerState

def footer() -> rx.Component:
    return rx.card(
            rx.hstack(
                rx.vstack(
                    rx.text("FlexDash, 2026, crafted by Matthew, a hobbyist", size="1", weight="bold"),
                    rx.hstack(
                    rx.link(rx.text("GitHub", size="1"), href="https://github.com/matthew-teh/PersonalDash", weight="bold", underline="none", is_external=True),
                    rx.link(rx.text("FB", size="1"), href="https://www.facebook.com/share/1BTB3PN2CK/", weight="bold", underline="none", is_external=True),
                    rx.link(rx.text("IG",  size="1"), href="https://www.instagram.com/matthew._.teh?exln=amUyZ2Y0ejR0MjZ5", weight="bold", underline="none", is_external=True),
                    spacing="1"
                    ),
                    height="100%",
                    spacing="0",
                ),
                rx.separator(
                    orientation="vertical",
                    height="100%",          # Makes it stretch to the height of the hstack
                    min_height="30px",
                ),
                rx.vstack(
                    rx.text("Server uptime:", size="1"),
                    rx.text(f"{ServerState.uptime}", size="1"),
                    spacing="1",
                ),
                
                height="100%",
                width="100%",
            ),  
            margin_bottom="4px",
            width="calc(100% - 8px - 8px)",
            padding="1em",
            margin_x="auto",
        )