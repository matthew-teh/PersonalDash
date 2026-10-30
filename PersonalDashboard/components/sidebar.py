import reflex as rx
from ..components.state import DashboardState

def sidebar() -> rx.Component:
    return rx.box(
        rx.drawer.root(
            rx.drawer.trigger(rx.button(rx.icon("plus", size=20), variant='ghost')),
            rx.drawer.overlay(),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.vstack(
                        rx.hstack(rx.text("Add Cards", weight="bold", size="4"), rx.spacer(), rx.drawer.close(rx.icon("x", size=30)), width="100%",align='center'),
                        rx.inset(
                            rx.vstack(
                                rx.text("Crypto Card"),
                                rx.image(src="sidebarimages/crypto.png",
                                        alt="cryptoimage",
                                        border_radius="5px"),
                                spacing="1",
                                align="center",
                            ),
                            on_click=DashboardState.create_card("crypto"),
                            border = "1px solid var(--gray-5)",
                            border_radius = "5px"
                        ),
                        rx.inset(
                            rx.vstack(
                                rx.text("Weather Card"),
                                rx.image(src="sidebarimages/weather.png",
                                        alt="cryptoimage",
                                        border_radius="5px"),
                                spacing="1",
                                align="center",
                            ),
                            on_click=DashboardState.create_card("weather"),
                            border = "1px solid var(--gray-5)",
                            border_radius = "5px"
                        ),
                        rx.inset(
                            rx.vstack(
                                rx.text("World Clock Card"),
                                rx.image(
                                    src="sidebarimages/world_clock.png",
                                    alt="weatherimage",
                                    border_radius="5px"),
                                spacing="1",
                                align="center",
                            ),
                            on_click=DashboardState.create_card("world_clock"),
                            border = "1px solid var(--gray-5)",
                            border_radius = "5px",
                        ),
                        width="100%",
                        spacing="2",

                    ),
                    left="auto",         
                    bottom="0px", 
                    position="fixed",
                    height="100%",
                    width="20em",
                    padding="0.5em",
                    align="start",
                )
            ),
            direction="right",
        ),
    )