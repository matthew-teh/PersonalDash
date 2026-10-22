import reflex as rx
from ..components.dropdown import dropdown
from ..components.state import DashboardState
def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.heading("FlexDash", as_="h2", size="4", weight="bold"),
                align="center",
            ),
            rx.hstack(
                dropdown(),
                rx.button(rx.icon("refresh_cw", size=20, color="#E8E9ED"), on_click=DashboardState.update_all, variant="ghost"), 
                rx.button(rx.icon("trash", size=20, color="#E8E9ED"), on_click=DashboardState.delete_all, variant="ghost"),
                rx.button(rx.icon("settings", size=20, color="#E8E9ED"), on_click=rx.toast("Coming Soon", description="This feature under development",style={"background_color":"#1E221D"}),variant="ghost"),
                justify="end",
                spacing="5",
            ),
            justify="between",
            align_items="center",
        ),
        border="1px solid var(--gray-7)",
        background_color="#090C08",
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
        margin_x="auto",
        border_radius="5px",
        height="6vh"
    )