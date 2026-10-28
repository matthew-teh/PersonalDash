import reflex as rx
from ..components.state import DashboardState

def footer() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.text("FlexDash, 2026, crafted by Matthew, a hobbyist", size="1", weight="bold")
                ),
                rx.spacer(),

                rx.hstack(
                    rx.link(rx.text("GitHub", size="1"), href="https://github.com/matthew-teh/PersonalDash", weight="bold", underline="none", is_external=True),
                    rx.link(rx.text("FB", size="1"), href="https://www.facebook.com/share/1BTB3PN2CK/", weight="bold", underline="none", is_external=True),
                    rx.link(rx.text("IG",  size="1"), href="https://www.instagram.com/matthew._.teh?exln=amUyZ2Y0ejR0MjZ5", weight="bold", underline="none", is_external=True),
                    rx.link(rx.text("Built with Reflex place"),  size="1", href="https://reflex.dev/", weight="bold", underline="none", is_external=True),
                    height="100%",
                ),
            ),  
            width="100%",
        ),
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
        margin_x="auto",
        border_radius="5px",
    )