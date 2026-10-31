import reflex as rx
import random
from . import components
from .components.state import DashboardState, ServerState
from typing import Any

@rx.page()
def index() -> rx.Component:
    return rx.theme(
        rx.vstack(
            components.header.navbar(),
            components.renderwidget.render_all_widgets(),
            rx.spacer(),
            components.footer.footer(),

            rx.moment(
                interval=1000,
                on_change=DashboardState.update_world_clock,
                display="None",
            ),

            rx.moment(
                interval=5000,
                on_change=ServerState.updateSystem,
                display="None",
            ),

            radius=DashboardState.edit_radius,
            justify="between",
            min_height="100vh",
            width="100%",
            spacing="0",
            overflow_x = "hidden",
            overflow_y = "auto",
        ),
        radius=DashboardState.edit_radius,
    )

app = rx.App(
    stylesheets=["/styles.css"], # type:ignore
)
