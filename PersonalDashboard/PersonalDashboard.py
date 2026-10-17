import reflex as rx 
import random
from .api.crypto import *
from .api.basic import *
def navbar_icons(icon, url) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20, color="#ffffff")
        ),
        href=url,
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.heading("FlexDash", as_="h2", size="4", weight="bold"),
                align_items="center",
            ),
            rx.hstack(
                rx.button(rx.icon("refresh_cw", size=20, color="#ffffff"), on_click=[CryptoState.update_prices, BasicState.reload], variant="ghost",), #type:ignore
                navbar_icons("plus", "/#"),
                navbar_icons("settings", "/#"),
                justify="end",
                spacing="5",
            ),
            justify="between",
            align_items="center",
        ),
        
        bg=rx.color("gray", 3),
        color="#ffffff",
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
  
        margin_x="auto",
        border_radius="5px",
    )

def footer() -> rx.Component:
    return rx.vstack(
        rx.box(
            
            rx.hstack(
                rx.hstack(
                    rx.text("FlexDash, 2026", size="1", weight="bold")
                ),
                rx.spacer(),

                rx.hstack(
                    rx.link("FB", size="1", href="https://google.com", weight="bold", underline="none"),
                    rx.link("IG", size="1", href="https://google.com", weight="bold", underline="none"),
                ),
                
            ),  
            width="100%",
        ),
        bg=rx.color("gray", 3),
        color="#ffffff",
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
    
        margin_x="auto",
        border_radius="5px",
    )


def widgets() -> rx.Component:
    return rx.vstack(
        rx.grid(basic_widgets(), columns="2", gap="0.5rem", width="calc(100vw - 1vh)", margin_x="auto",),
        rx.grid(crypto_widgets(), columns="3", gap="0.5rem", width="calc(100vw - 1vh)", margin_x="auto",),
        
    )
def index():
    CryptoState.update_prices
    return rx.vstack(
        navbar(),
        widgets(),
        rx.spacer(),
        footer(),
        justify="between",      # Pushes navbar to top, content in middle, footer to bottom
        min_height="100vh",      # Forces the stack to span the full window height
        width="100%",
        spacing="0",
    ), 


app = rx.App()
app.add_page(index)