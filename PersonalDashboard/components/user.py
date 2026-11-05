import reflex as rx
from ..components.state import DashboardState
from ..components.state import AuthState
def user() -> rx.Component:
    return rx.box(
        rx.dialog.root(
            rx.dialog.trigger(rx.button(rx.icon("user_round", size=20), variant="ghost")),
            rx.dialog.content(
                rx.vstack(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Account Info", size="4"),   
                            rx.dialog.close(rx.button(rx.icon("x", size=25), variant='ghost')),
                            justify="between",
                            width="100%",
                        ),
                        rx.text(f"Username: {AuthState.user}"),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Dangerous area", color_scheme="tomato"),
                        rx.hstack(
                            rx.vstack(
                                rx.dialog.root(
                                rx.dialog.trigger(rx.button("Sign out", color_scheme="tomato", variant="outline")),
                                    rx.dialog.content(
                                        rx.vstack(
                                            rx.heading("Are you sure?", size="4"),
                                            rx.hstack(
                                                rx.button("Yes", color_scheme="tomato", variant="outline", size="3", on_click=AuthState.signout),
                                                rx.dialog.close(rx.button("No", color_scheme="green", size="3")),
                                                width="100%",
                                                justify="center"
                                            ),  
                                            width="100%",
                                            align="center",
                                            spacing="5"
                                        ),
                                        width="300px",
                                    ),
                            
                                ),
                            ),
                            rx.vstack(
                                rx.dialog.root(
                                    
                                rx.dialog.trigger(rx.button("Delete Account", color_scheme="tomato", variant="outline")),
                                    rx.dialog.content(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.heading("Enter your password to continue.", size="4"),
                                                rx.dialog.close(rx.button(rx.icon("x"), variant="ghost")),
                                                width="100%",
                                                justify="between",
                                            ),
                                            rx.form(
                                                rx.vstack(
                                                    rx.input(
                                                        placeholder="blissful_pepperoni",
                                                        type="password",
                                                        value=AuthState.password, 
                                                        on_change=AuthState.set_password,
                                                        width="100%",
                                                        size="3",
                                                        required=True
                                                    ),
                                                    rx.button("Submit", color_scheme="tomato", variant="outline", width="100%"),
                                                    width="100%",
                                                ),  
                                                on_submit=AuthState.delete_account,
                                                width="100%",
                                            ),
                                            width="100%",
                                        ),
                                        width="100%",
                                    ),
                            
                                ),
                            ),
                        ),
                    ),
                    justify="between",
                    height="100%",
                    width="100%",
                ),    
                width="960px",
                height="496.5px",
            )
        )
    )