
import reflex as rx
from ..components.state import DashboardState  

def template(card) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.hstack( # HEADING 
                    rx.vstack(
                        rx.heading("", size="3"),
                        spacing="0",
                    ),
                    rx.spacer(),
                    rx.hover_card.root(
                        rx.vstack(
                            rx.hstack(
                                rx.text("Symbol", size="3", weight="bold"),
                                rx.spacer(),
                                rx.button(
                                    rx.icon("check"),
                                    variant="ghost",
                                    on_click=DashboardState.save_edit_crypto(card["id"]),
                                ),
                                justify="between",
                                width="100%"
                            ),
                        )
                    ),
                    rx.button(
                        rx.icon("refresh_cw", size=16),
                        variant="ghost",
                        on_click=lambda x:x,
                    ),
                    rx.button(
                        rx.icon("trash_2", size=16),
                        variant="ghost",
                        on_click=lambda x:x,
                    )
                ),
                # Contents here
            )
        ),
        size="1",
        width="100%",
        height="30vh",
    )



