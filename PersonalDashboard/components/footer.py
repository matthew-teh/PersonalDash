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
                    rx.link(rx.text("FB", color="#E8E9ED"), size="1", href="https://www.facebook.com/share/1BTB3PN2CK/", weight="bold", underline="none", is_external=True),
                    rx.link(rx.text("IG", color="#E8E9ED"), size="1", href="https://www.instagram.com/matthew._.teh?exln=amUyZ2Y0ejR0MjZ5", weight="bold", underline="none", is_external=True),
                ),
                
            ),  
            width="100%",
        ),
        background_color="#090C08",
        margin="1vh",
        width="calc(100vw - 1vh)",
        padding="1em",
        border="1px solid var(--gray-7)",
        margin_x="auto",
        border_radius="5px",
    )