import reflex as rx
from ..components.state import DashboardState
def dropdown() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(rx.icon("plus", color="#E8E9ED", size=20), variant="ghost"),
        ),
        rx.menu.content(
            rx.menu.item("Crypto Card", on_select = DashboardState.create_card({"type":"crypto"})),
            rx.menu.item("Weather Card", on_select = DashboardState.create_card({"type": "weather"})),
            background_color = "#1E221D"
        ),
    )