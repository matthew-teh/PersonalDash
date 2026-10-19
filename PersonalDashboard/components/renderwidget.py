import reflex as rx

from ..widgets.crypto import CryptoCard
from ..components.state import DashboardState

def render_single_card(card) -> rx.Component:
    return rx.cond(
        card["type"] == "Crypto",
        CryptoCard(card),
        rx.box(),
    )


def render_all_widgets() -> rx.Component:
    return rx.vstack(
        rx.button(
            "Add Crypto Card",
            on_click=DashboardState.CreateCrypto,
        ),
        rx.grid(
            rx.foreach(
                DashboardState.cards,
                render_single_card,
            ),
            columns="3",
            width="100%",
            spacing="1",
        ),
        width="calc(100vw - 1vh)",
        margin_x="auto",
        align="stretch",
    )