import reflex as rx

from .FDstates import Dashboard
from .FDcomponents import sidebar, widget

@rx.page("/", title="FlexDash | Dashboard", on_load=Dashboard.init_page)
def home() -> rx.Component:
    return rx.box(
        rx.hstack(
            sidebar(),
            rx.box(width="85%", height="100%", background_color = Dashboard.colors["page_background"], border_radius="8px"),
            width="100%",
            height="100%",
        ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["background"],
    )

@rx.page("/widgets", title="FlexDash | Widgets", on_load=Dashboard.init_page)
def widgets() -> rx.Component:
    return rx.box(
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.text("FlexDash Widgets", weight="bold", font_size="64px", opacity=0.95),
                    rx.scroll_area(
                        rx.grid(
                            rx.foreach(
                                Dashboard.widgets,
                                lambda item : widget(item.name, item.image, item.desc),
                            ),
                            gap="8px",
                            columns="4",
                            width="100%",
                        ),
                        height="84vh",
                        width="100%",
                    ),
                    width="100%",
                    spacing="1",
                ),
                padding="8px",
                width="85%", 
                height="100%", 
                background_color = Dashboard.colors["page_background"], 
                border_radius="8px"),
            width="100%",
            height="100%",
        ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["background"],
    )