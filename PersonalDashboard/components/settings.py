import reflex as rx
from ..components.state import DashboardState
from reflex.style import set_color_mode, color_mode
def settings() -> rx.Component:
    return rx.box(
        rx.dialog.root(
            rx.dialog.trigger(rx.button(rx.icon("settings", size=20), variant="ghost")),
            rx.dialog.content(
                rx.vstack(
                    rx.hstack(
                        rx.text("Settings",size="4", weight="bold"),
                        rx.dialog.close(rx.button(rx.icon('x',  size=25), variant='ghost')),
                        justify='between',
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text("Appearance: ", size="3"),
                        rx.segmented_control.root(
                                rx.segmented_control.item(
                                    rx.icon(tag="monitor", size=20),
                                    value="system",
                                ),
                                rx.segmented_control.item(
                                    rx.icon(tag="sun", size=20),
                                    value="light",
                                ),
                                rx.segmented_control.item(
                                    rx.icon(tag="moon", size=20),
                                    value="dark",
                                ),
                                on_change=set_color_mode, #type:ignore
                                variant="classic",
                                radius="large",
                                value=color_mode,
                            ),
                        align="center"
                    ),
                spacing="2"
                ),
                height= "50vh",
                width = "50vw",
            ),
        ),
  
    )