import reflex as rx
from ..components.state import DashboardState
from ..components.sidebar import sidebar
from ..components.settings import settings
def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.heading("FlexDash", as_="h2", size="4", weight="bold"),
                align="center",
            ),
            rx.hstack(
                sidebar(),  
                rx.button(rx.icon("refresh_cw", size=20, class_name=rx.cond(DashboardState.is_updating, "spinning", "")), on_click=DashboardState.update_all, variant="ghost", disabled=DashboardState.is_updating), 
                rx.button(rx.icon("trash", size=20), on_click=DashboardState.delete_all, variant="ghost"),
                settings(),
                justify="end",
                spacing="5",
            ),
            
            justify="between",
            align_items="center",
        ),
        border="1px solid",
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
        margin_x="auto",
        border_radius="5px",
        height="6vh"
    )