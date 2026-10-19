import reflex as rx

def navbar_icons(icon, url) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20, color="#FFFCF2")
        ),
        href=url,
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.heading("FlexDash", as_="h2", size="4", weight="bold"),
                align_items="center",
            ),
            rx.hstack(
                rx.button(rx.icon("refresh_cw", size=20, color="#FFFCF2"), on_click=[], variant="ghost",), #type:ignore
                navbar_icons("settings", "/#"),
                justify="end",
                spacing="5",
            ),
            justify="between",
            align_items="center",
        ),
        
        background_color="#403D39",
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
        margin_x="auto",
        border_radius="5px",
    )