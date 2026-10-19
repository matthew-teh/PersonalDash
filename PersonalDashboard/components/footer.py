import reflex as rx
def footer() -> rx.Component:
    return rx.vstack(
        rx.box(
            
            rx.hstack(
                rx.hstack(
                    rx.text("FlexDash, 2026", size="1", weight="bold")
                ),
                rx.spacer(),

                rx.hstack(
                    rx.link(rx.text("FB", color="#FFFCF2"), size="1", href="https://google.com", weight="bold", underline="none"),
                    rx.link(rx.text("IG", color="#FFFCF2"), size="1", href="https://google.com", weight="bold", underline="none"),
                ),
                
            ),  
            width="100%",
        ),
        background_color="#403D39",
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
    
        margin_x="auto",
        border_radius="5px",
    )