import reflex as rx
from ..components.dropdown import dropdown

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.heading("FlexDash", as_="h2", size="4", weight="bold"),
                align_items="center",
            ),
            rx.hstack(
                dropdown(),
                rx.button(rx.icon("refresh_cw", size=20, color="#FFFCF2"), on_click=rx.toast("Coming Soon", description="This feature under development",style={"background_color":"#403D39"}), variant="ghost"), 
                rx.button(rx.icon("settings", size=20, color="#FFFCF2"), on_click=rx.toast("Coming Soon", description="This feature under development",style={"background_color":"#403D39"}),variant="ghost"),
                justify="end",
                spacing="5",
            ),
            justify="between",
            align_items="center",
        ),
        
        background_color="#403D39",
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
        margin_x="auto",
        border_radius="5px",
    )