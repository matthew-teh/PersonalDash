import reflex as rx
from typing import Any
from ..widgets.crypto import crypto_card
from ..widgets.weather import weather_card
from ..components.state import DashboardState

def render_single_card(card, index:int) -> rx.Component | rx.Var:
    return rx.box(
        rx.match(
            card["type"],
            ("crypto", crypto_card(card)),
            ("weather", weather_card(card)),
            rx.box(),
        ),
        class_name="card-pop",
        style={
            "animation-delay": f"{index * 0.1}s",
        },
    )

def render_all_widgets() -> rx.Component:
    return rx.vstack(
        rx.grid(
            rx.foreach(
                DashboardState.cards,
                lambda card, index: render_single_card(card, index),
            ),
            columns="4",
            width="100%",
            spacing="1",
        ),
        width="calc(100vw - 1vh)",
        margin_x="auto",
        align="stretch",
    )