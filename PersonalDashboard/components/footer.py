import reflex as rx
def footer() -> rx.Component:
    return rx.vstack(
        rx.box(
            
            rx.hstack(
                rx.hstack(
                    rx.text("FlexDash, 2026, crafted by Matthew, a hobbyist", size="1", weight="bold")
                ),
                rx.spacer(),

                rx.hstack(
                    rx.link(rx.text("FB", color="#FFFCF2"), size="1", href="https://www.facebook.com/share/1BTB3PN2CK/", weight="bold", underline="none"),
                    rx.link(rx.text("IG", color="#FFFCF2"), size="1", href="https://www.instagram.com/matthew._.teh?exln=amUyZ2Y0ejR0MjZ5", weight="bold", underline="none"),
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