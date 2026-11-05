import reflex as rx
from ..components.state import AuthState

def signin() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.image(src="logo.png", width="50px", border_radius="5px"),
                rx.heading("Sign in to your account"),
                width="100%",
                align="center",
            ),    
            rx.form(
                rx.vstack(
                    rx.vstack(
                        rx.text("Username"),
                        rx.input(placeholder="FlavorFocus", width="100%", size="3", value=AuthState.username, on_change=AuthState.set_username),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Password"),
                        rx.input(placeholder="MochiMunchies", width="100%", size="3", type="password", value=AuthState.password, on_change=AuthState.set_password),
                        width='100%',   
                    ),
                    rx.button("Sign in", width="100%", size="3", type="submit", disabled=AuthState.disabled),
                ),
                on_submit=AuthState.signin
            ),
            
            rx.hstack(
                rx.text("New here?"),
                rx.link("Sign Up", href="/signup"),
            ),
            spacing="5",
            width="100%",
            align="center",
        ),
        padding="16px",
        width="400px",
    )

def signup() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.image(src="logo.png", width="50px", border_radius="5px"),
                rx.heading("Create account"),
                width="100%",
                align="center",
            ), 
            rx.form(
                rx.vstack(   
                    rx.vstack(
                        rx.hstack(
                            rx.text("Username"),
                            width="100%",
                            justify="between",
                        ),
                        rx.input(placeholder="SavorySymphony", width="100%", size="3", value=AuthState.username, on_change=AuthState.set_username, required=True),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Password"),
                        rx.input(placeholder="HoneyToastie", width="100%", size="3", type="password", value=AuthState.password, on_change=AuthState.set_password, required=True),
                        width='100%',   
                    ),
                    rx.button("Create account", width="100%", size="3", type="submit", disabled=AuthState.disabled),
                    spacing="5",
                    width="100%",
                    align="center"
                ),
                on_submit = AuthState.signup,
            ), 
            rx.hstack(
                rx.text("Already have a account?"),
                rx.link("Sign In", href="/"),
            ),
            spacing="5",
            width="100%",
            align="center",
            
        ),
        padding="16px",
        width="400px",
    )