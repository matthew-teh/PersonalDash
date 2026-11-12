import reflex as rx

from .FDstates import Dashboard
from .FDcomponents import sidebar, widget, render_widget

@rx.page("/", title="FlexDash | Dashboard", on_load=Dashboard.init_page)
def home() -> rx.Component:
    empty = Dashboard.widgets.length() == 0 #type:ignore
    return rx.box(
        rx.hstack(
            sidebar(),
            rx.cond(
                empty,
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.text("Nothing yet. Maybe add some widgets?"),
                            rx.button(
                                rx.text("Explore widgets", color=Dashboard.colors["text_alt"]),
                                background_color=Dashboard.colors["text"],
                                size="4",
                                on_click=rx.redirect('/widgets')
                            ),
                            align="center",
                        ),
                        width="100%",
                        height="100%"
                    ),
                    width="87%", 
                    height="100%", 
                    background_color = Dashboard.colors["page_background"], 
                    border_radius="8px"
                ),
                rx.box(
                    rx.grid(
                        rx.foreach(
                            Dashboard.widgets,
                            lambda item: render_widget(item)
                        ),
                        padding="8px",
                        columns="4",
                        gap="8px",
                    ),
                    rx.moment(
                        interval=1000,
                        on_change=[
                            Dashboard.update_widget("",widget_type="pomodoro_v1"), 
                            Dashboard.update_widget("", widget_type="worldclock_v1"),
                            Dashboard.update_widget("", widget_type="terracd_v1")
                        ],
                        display="None",
                    ),
                    width="87%", 
                    height="100%", 
                    background_color = Dashboard.colors["page_background"], 
                    border_radius="8px"
                ),
            ),
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
                                Dashboard.widgets_store,
                                lambda item : widget(item.name, item.image, item.desc, item.available),
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
                width="87%", 
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