import reflex as rx
from ..components.state import DashboardState
from ..components.sidebar import sidebar
from ..components.settings import settings
from ..components.user import user
def header(landing) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.heading("FlexDash", size="4", weight="bold"),
            rx.cond(
                landing == False,
                rx.hstack(
                    sidebar(),  
                    rx.button(rx.icon("refresh_cw", size=20, class_name=rx.cond(DashboardState.is_updating, "spinning", "")), on_click=DashboardState.update_all, variant="ghost", disabled=DashboardState.is_updating), 
                    rx.button(rx.icon("trash", size=20), on_click=DashboardState.delete_all, variant="ghost"),
                    settings(),
                    user(),
                    justify="end",
                    spacing="5",
                ),

            ),
            justify="between",
            align_items="center",
            height="100%",
            width="100%"
        ),
        margin_top="4px",
        width="calc(100% - 8px - 8px)",
        padding="1em",
        margin_x="auto",
        height="6vh",
    )