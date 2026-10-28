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
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(rx.text("Appearance: ", size="3"),),
                            rx.vstack(                        
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
                                    width="18em"
                                ),
                            ),
                            width="100%",
                            justify="between",
                        ),
                        rx.hstack(
                            rx.vstack(rx.text("Cards Per Row: ", size="3"),),
                            rx.vstack(
                                rx.segmented_control.root(
                                    rx.segmented_control.item(
                                        rx.text("1"),
                                        value="1",
                                    ),
                                    rx.segmented_control.item(
                                        rx.text("2"),
                                        value="2",
                                    ),
                                    rx.segmented_control.item(
                                        rx.text("3"),
                                        value="3",
                                    ),
                                    rx.segmented_control.item(
                                        rx.text("4"),
                                        value="4",
                                    ),
                                    rx.segmented_control.item(
                                        rx.text("5"),
                                        value="5",
                                    ),
                                    rx.segmented_control.item(
                                        rx.text("6"),
                                        value="6",
                                    ),
                                    on_change=DashboardState.set_column, #type:ignore
                                    variant="classic",
                                    radius="large",
                                    value=DashboardState.edit_column,
                                    width="18em"
                                ),
                            ),
                            width="100%",
                            justify="between",
                        ),
                        width="95%",
                    ),
                    
                spacing="2",
                width="100%"
                ),
                height= "50vh",
                width = "50vw",
            ),
        ),
  
    )