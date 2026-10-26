import reflex as rx
import random
from . import components
from .components.state import DashboardState
from typing import Any

def index() -> rx.Component:
    return rx.vstack(
        components.header.navbar(),
        components.renderwidget.render_all_widgets(),
        rx.spacer(),
        components.footer.footer(),
        justify="between",
        min_height="100vh",
        width="100%",
        spacing="0",
    )


app = rx.App(
    stylesheets=["/styles.css"], # type:ignore
    theme=rx.theme( # type:ignore 
        appearance="light", has_background=True, radius="medium", accent_color="teal"
    )
)
app.add_page(index)