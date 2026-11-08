import reflex as rx
import random
from .components.footer import footer
from .components.header import header
from .components.renderwidget import render_all_widgets
from .components.authenticate import signin, signup, provide_recovery_token, forgot_password
from .components.state import DashboardState, ServerState, AuthState

@rx.page("/home", title="FlexDash | Home", on_load=[DashboardState.load_cards, AuthState.route_protect])
def home() -> rx.Component:
    return rx.theme(
        rx.vstack(
            header(landing=False),
            render_all_widgets(),
            rx.spacer(),
            footer(),

            rx.moment(
                interval=1000,
                on_change=[DashboardState.update_world_clock, DashboardState.update_pomodoro, DashboardState.update_countdown],
                display="None",
            ),
            rx.moment(
                interval=60000,
                on_change=ServerState.updateSystem,
                display="None"
            ),


            radius=DashboardState.edit_radius,
            justify="between",
            min_height="100vh",
            width="100%",
            spacing="0",
            overflow_x = "hidden",
            overflow_y = "auto",
        ),
        radius=DashboardState.edit_radius,
    )

@rx.page("/", title="FlexDash | Sign In", on_load=[ServerState.updateSystem, 
                                                   AuthState.check_signedin, 
                                                   AuthState.reset_field, 
                                                   rx.call_script("navigator.userAgent", callback=AuthState.receiveUA)])
def landing() -> rx.Component:
    return rx.theme(
        rx.vstack(
            header(landing=True),
            rx.flex(signin(), height="100%", width="100%", justify="center", align_items="center"),
            footer(),
            
            radius=DashboardState.edit_radius,
            justify="between",
            min_height="100vh",
            width="100%",   
            spacing="0",
            overflow_x = "hidden",
            overflow_y = "auto",
        ),  
        radius=DashboardState.edit_radius,
    )

@rx.page("/signup", title="FlexDash | Sign Up", on_load=[ServerState.updateSystem, AuthState.check_signedin])
def signingup() -> rx.Component:
    return rx.theme(
        rx.vstack(
            header(landing=True),
            rx.flex(signup(), height="100%", width="100%", justify="center", align_items="center"),
            footer(),
            radius=DashboardState.edit_radius,
            justify="between",
            min_height="100vh",
            width="100%",
            spacing="0",
            overflow_x = "hidden",
            overflow_y = "auto",
        ),

        radius=DashboardState.edit_radius,
    )

@rx.page("/security", title="FlexDash | Action Needed", on_load=[AuthState.route_protect_recovery])
def signin_token() -> rx.Component:
    return rx.theme(
        rx.vstack(
            header(landing=True),
            rx.flex(provide_recovery_token(), height="100%", width="100%", justify="center", align_items="center"),
            footer(),
            radius=DashboardState.edit_radius,
            justify="between",
            min_height="100vh",
            width="100%",
            spacing="0",
            overflow_x = "hidden",
            overflow_y = "auto",
        ),
        radius=DashboardState.edit_radius,
    )

@rx.page("/forgot_password", title="FlexDash | Forgot Password?")
def reset_password() -> rx.Component:
    return rx.theme(
        rx.vstack(
            header(landing=True),
            rx.flex(forgot_password(), height="100%", width="100%", justify="center", align_items="center"),
            footer(),
            radius=DashboardState.edit_radius,
            justify="between",
            min_height="100vh",
            width="100%",
            spacing="0",
            overflow_x = "hidden",
            overflow_y = "auto",
        ),
        radius=DashboardState.edit_radius,
    )


app = rx.App(
    stylesheets=["/styles.css"], # type:ignore
)


