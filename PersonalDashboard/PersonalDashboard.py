import reflex as rx
import random
from . import components
from .components.state import DashboardState
from typing import Any

@rx.page()
def index() -> rx.Component:
    return rx.vstack(
        components.header.navbar(),
        components.renderwidget.render_all_widgets(),
        rx.spacer(),
        components.footer.footer(),

        rx.moment(
            interval=1000,
            on_change=DashboardState.update_world_clock,
            display="None",
        ),

        justify="between",
        min_height="100vh",
        width="100%",
        spacing="0",
        overflow_x = "hidden",
        overflow_y = "auto",
    )

app = rx.App(
    stylesheets=["/styles.css"], # type:ignore
)
