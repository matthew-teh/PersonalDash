import reflex as rx
from ..components.state import DashboardState
def dropdown() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(rx.icon("plus", color="#E8E9ED", size=20), variant="ghost"),
        ),
        rx.menu.content(
            rx.menu.item("Crypto Card", on_select = DashboardState.MakeCards({"type":"Crypto"})),
            rx.menu.item("Live Crypto Card", on_select = DashboardState.MakeCards({"type":"AggCrypto"})),
            rx.menu.item("Weather Card", on_select = rx.toast("Coming Soon", description="This feature under development",style={"background_color":"#403D39"})),
            background_color = "#1E221D"
        ),
    )