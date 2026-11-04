import reflex as rx
from ..components.state import DashboardState
from ..components.state import AuthState
def user() -> rx.Component:
    return rx.box(
        rx.dialog.root(
            rx.dialog.trigger(rx.button(rx.icon("user_round", size=20), variant="ghost")),
            rx.dialog.content(
                rx.vstack(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Account Info", size="4"),   
                            rx.dialog.close(rx.button(rx.icon("x", size=25), variant='ghost')),
                            justify="between",
                            width="100%",
                        ),
                        rx.text(f"Username: {AuthState.user}"),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.button(
                            "Logout", 
                            color_scheme='tomato', 
                            variant="outline", 
                            on_click = AuthState.logout,
                        ),
                    ),
                    justify="between",
                    height="100%",
                    width="100%",
                ),    
                width="960px",
                height="496.5px",
            )
        )
    )