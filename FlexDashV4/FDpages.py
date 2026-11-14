import reflex as rx
from reflex.style import set_color_mode, color_mode
from .FDstates import Dashboard, System
from .FDcomponents import sidebar, widget, render_widget
from .FDauth import Auth

@rx.page("/home", title="FlexDash | Dashboard", on_load=[Dashboard.init_page])
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
                                rx.text("Explore widgets", color=Dashboard.colors["text"]),
                                background_color=Dashboard.colors["buttons"],
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
                    background_color = Dashboard.colors["page"], 
                    border_radius=Dashboard.smoothness
                ),
                rx.box(
                    rx.grid(
                        rx.foreach(
                            Dashboard.widgets,
                            lambda item: render_widget(item)
                        ),
                        padding="8px",
                        columns=Dashboard.widget_per_row,
                        gap="8px",
                    ),
                    rx.moment(
                        interval=1000,
                        on_change=[
                            Dashboard.update_widget("",widget_type="pomodoro_v1"),  # type: ignore
                            Dashboard.update_widget("", widget_type="worldclock_v1"), # type: ignore
                            Dashboard.update_widget("", widget_type="terracd_v1") # type: ignore
                        ],
                        display="None",
                    ),
                    width="87%", 
                    height="100%", 
                    background_color = Dashboard.colors["page"], 
                    border_radius=Dashboard.smoothness
                ),
            ),
            width="100%",
            height="100%",
        ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["page"],
        color=Dashboard.colors["text"]
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
                background_color = Dashboard.colors["page"], 
                border_radius=Dashboard.smoothness),
                
            width="100%",
            height="100%",
        ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["page"],
        color=Dashboard.colors["text"]
    )

@rx.page("/settings", title="FlexDash | Settings", on_load=[Dashboard.init_page, System.update_server_status])
def settings() -> rx.Component:
        return rx.box(
        rx.hstack(
            sidebar(),  
            rx.box(
                rx.vstack(
                    rx.text("FlexDash Settings & Preferences", weight="bold", font_size="64px", opacity=0.95, margin_bottom="16px",),                    
                    rx.hstack(
                        rx.vstack(
                            rx.box(
                                rx.vstack(
                                    rx.text("Appearance", font_size="32px"),
                                    rx.separator(),
                                    margin_bottom="32px",
                                ),
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("THEME PRESETS", font_size="16px", weight="bold"),
                                        rx.segmented_control.root(
                                            rx.segmented_control.item("Light", value="light"),
                                            rx.segmented_control.item("Dark", value="dark"),
                                            on_change=[set_color_mode, Dashboard.edit_appearance], #type:ignore #PYLINT ERROR
                                            value= color_mode,
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.grid(
                                                rx.foreach(
                                                    Dashboard.theme,
                                                    lambda item: rx.box( 
                                                        width="20px",
                                                        height="20px", 
                                                        border_radius=rx.cond(
                                                            Dashboard.colors["name"] == item["name"],
                                                            "10px", "4px"
                                                        ),
                                                        background_color=f"var(--{item["name"]}-9)",
                                                        on_click=Dashboard.edit_theme(item["name"]),
                                                        transition="transform 0.2s ease-in-out",
                                                        _hover={
                                                            "transform" : "scale(1.5)",
                                                        },
                                                    ),
                                                ),
                                                columns="10",
                                                gap="8px",
                                            ),
                                        ),
                                        width="40%",    
                                    ),
                                    rx.vstack(
                                        rx.text("BORDER SMOOTHNESS", font_size="16px", weight="bold"),
                                        rx.segmented_control.root(
                                            rx.segmented_control.item(rx.text("Sharp"), value="0px"),
                                            rx.segmented_control.item(rx.text("Soft"), value="4px"),
                                            rx.segmented_control.item(rx.text("Rounded"), value="8px"),
                                            rx.segmented_control.item(rx.text("Curved"), value="16px"),
                                            rx.segmented_control.item(rx.text("Pill"), value="32px"),
                                            width="100%",
                                            value=Dashboard.smoothness,
                                            on_change=Dashboard.edit_smoothness,     # type: ignore
                                        ),
                                        rx.text("WIDGETS PER ROW", font_size="16px", weight="bold", margin_top="16px"),
                                        rx.segmented_control.root(
                                            rx.segmented_control.item(rx.text("1"), value="1"),
                                            rx.segmented_control.item(rx.text("2"), value="2"),
                                            rx.segmented_control.item(rx.text("3"), value="3"),
                                            rx.segmented_control.item(rx.text("4"), value="4"),
                                            rx.segmented_control.item(rx.text("5"), value="5"),
                                            rx.segmented_control.item(rx.text("6"), value="6"),
                                            value=Dashboard.widget_per_row,
                                            on_change=Dashboard.edit_wpr,
                                            width="100%",
                                        ),
                                        width="60%"
                                    ),
                                    spacing="5",
                                ),
                                padding="32px",
                                width="100%",
                                border_radius=Dashboard.smoothness,
                                
                                background_color = Dashboard.colors["widget"],
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Server Status", font_size="32px"),
                                        rx.spacer(),
                                        rx.text("Hover for refresh", font_size="14px", opacity=0.5),
                                        width="100%",
                                        align="end"
                                    ),
                                    rx.separator(),
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text(f"CPU Usage: {System.cpu}%"),
                                            rx.text(f"RAM Usage: {System.ram}%"),
                                            width="20%",
                                        ),
                                        rx.vstack(
                                            rx.progress(value=System.cpu.to(int), width='70%', height="20px",fill_color=Dashboard.colors["buttons"], background_color=Dashboard.colors["website"]), # type: ignore
                                            rx.progress(value=System.ram.to(int), width='70%', height="20px",fill_color=Dashboard.colors["buttons"], background_color=Dashboard.colors["website"]), # type: ignore
                                            height="100%",
                                            width="80%",
                                        ),
                                        align="center",
                                        width="100%",
                                        height="100%",
                                    ),
                                    rx.text(f"Uptime: {System.formatted_uptime}"),
                                    margin_bottom="32px",
                                ),
                                height="100%",
                                padding="32px",
                                width="100%",
                                border_radius=Dashboard.smoothness,
                                
                                on_mouse_enter=System.update_server_status,
                                background_color = Dashboard.colors["widget"],
                            ),
                        width="50%"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Live Preview", font_size="32px"),
                                    rx.spacer(),
                                    rx.text("Ignore the borders", font_size="14px", opacity=0.5),
                                    align="end",
                                    width="100%",
                                    height="100%",
                                ),
                                rx.separator(),
                                margin_bottom="32px",
                            ),
                            rx.center(
                                rx.box(
                                    rx.hstack(
                                        rx.cond(
                                            Dashboard.appearance == "dark",
                                            rx.image(src="/lucide_icons/book_dark.svg", height="42px", width="42px"),
                                            rx.image(src="/lucide_icons/book_light.svg", height="42px", width="42px")
                                        ),
                                        rx.vstack(
                                            rx.heading("Quick Notes", size="3"),
                                            rx.text("A text area to note, auto saved."),
                                            spacing="0",
                                        ),
                                        rx.spacer(),
                                        rx.button(rx.icon("trash_2", size=16), variant="ghost"),
                                        width="100%",
                                        height="20%",
                                    ),
                                    rx.hstack(
                                        rx.text_area(
                                            placeholder="Start typing here...",
                                            width="100%",
                                            height="100%",
                                            color=Dashboard.colors["text"]
                                        ),
                                        width="100%",
                                        height="80%",
                                        spacing="0",
                                    ),
                                    padding="8px",
                                    overflow="hidden",
                                    width="50%",
                                    aspect_ratio=" 1/1",
                                    style={"background_color": Dashboard.colors["widget"]},
                                    border_radius=Dashboard.smoothness,
                                    border_width="1px",
                                    border_color=Dashboard.colors["text"]
                                ),
                            ),
                            padding="32px",
                            width="50%",
                            border_radius=Dashboard.smoothness,
                            
                            background_color = Dashboard.colors["widget"],
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),
                padding="8px",
                width="87%", 
                height="100%", 
                background_color = Dashboard.colors["page"], 
                border_radius=Dashboard.smoothness),
            width="100%",
            height="100%",
        ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["page"],
        color=Dashboard.colors["text"]
    )

@rx.page("/signin", title="FlexDash | Sign in", on_load=[Dashboard.init_page(False), Auth.set_mode('in')])
def signin() -> rx.Component:
    return rx.box(
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.vstack(
                            rx.image(src="/logo.svg", width="60px", border_radius="5px"),
                            rx.heading("Sign in to your account", size="7"),
                            width="100%",
                            align="center",
                        ),    
                        rx.form(
                            rx.vstack(
                                rx.vstack(
                                    rx.text("Username", size="3"),
                                    rx.input(placeholder="FlavorFocus", width="100%", size="3", value=Auth.username_field, on_change=Auth.set_username),
                                    width="100%",
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("Password", size="3"),
                                        rx.link("Forgot Password?", href="/forgot_password", size="3"),
                                        width="100%",
                                        justify="between"
                                    ),
                                    rx.input(placeholder="MochiMunchies", width="100%", size="3", type="password", value=Auth.password_field, on_change=Auth.set_password),
                                    width='100%',   
                                ),
                                rx.button("Sign in", width="100%", size="3", type="submit", disabled=Auth.disabled),
                                spacing="5",
                                width="100%",
                                align="center"
                            ),
                            on_submit = Auth.sign_in,
                        ),
                        rx.hstack(
                            rx.text("New here?"),
                            rx.link("Create account", href="/signup"),
                        ),
                        spacing="5",
                        align="center",
                        padding="32px",
                    ),
                    width="500px",
                    aspect_ratio="1/1",
                    background_color = Dashboard.colors["widget"],
                    border_radius= Dashboard.smoothness
                ),
            width="100%",
            height="100%",
            ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["page"],
        color=Dashboard.colors["text"]
    )

@rx.page("/signup", title="FlexDash | Sign Up", on_load=[Dashboard.init_page(False), Auth.set_mode('up')])
def signup() -> rx.Component:
    return rx.box(
        rx.center(
            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.image(src="/logo.svg", width="60px", border_radius="5px"),
                        rx.heading("Create account", size="7"),
                        width="100%",
                        align="center",
                    ),    
                    rx.form(
                        rx.vstack(
                            rx.vstack(
                                rx.text("Username", size="3"),
                                rx.input(placeholder="ZeroSugar", width="100%", size="3", value=Auth.username_field, on_change=Auth.set_username),
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text("Password", size="3"),
                                rx.input(placeholder="PeachyPudding", width="100%", size="3", type="password", value=Auth.password_field, on_change=Auth.set_password),
                                width='100%',   
                            ),
                            rx.vstack(
                                rx.text("Confirm password", size="3"),
                                rx.input(placeholder="PeachyPudding", width="100%", size="3", type="password", value=Auth.password_2_field, on_change=Auth.set_2_password),
                                width='100%',   
                            ),
                            rx.button("Create account", width="100%", size="3", type="submit", disabled=Auth.disabled),
                            spacing="5",
                            width="100%",
                            align="center"
                        ),
                        on_submit=Auth.sign_up
                    ),
                    rx.hstack(
                        rx.text("Already have account?"),
                        rx.link("Sign In", href="/signin"),
                    ),
                    spacing="5",
                    align="center",
                    padding="32px",
                ),
                width="500px",
                aspect_ratio="1/1",
                background_color = Dashboard.colors["widget"],
                border_radius= Dashboard.smoothness
            ),
            width="100%",
            height="100%",
        ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["page"],
        color=Dashboard.colors["text"]
    )

@rx.page("/security", title="FlexDash | Action needed", on_load=Auth.security_rp)
def security() -> rx.Component:
    return rx.box(
        rx.center(
            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.image(src="/logo.svg", width="60px", border_radius="5px"),
                        rx.heading("Action needed", size="7"),
                        spacing="5",
                        width="100%",
                        align="center",
                    ),
                    rx.vstack(
                        rx.text("Here is a important key, store it somewhere."),
                        rx.code_block(Auth.recovery_token, width="100%"),
                        rx.text("In case you forget your password, use this."),
                        rx.button("I've stored somewhere.", width="100%", size="3", on_click=Auth.sign_in),
                        justify="center",
                        width="100%",
                     ),
                    spacing="5",
                    width="100%",
                    align="center",
                    padding="32px",
                ),
                width="400px",
                aspect_ratio="1/1",
                background_color = Dashboard.colors["widget"],
                border_radius= Dashboard.smoothness,
            ),
            width="100%",
            height="100%",
        ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["page"],
        color=Dashboard.colors["text"]
    )    

@rx.page("/forgot_password", title="FlexDash | Recovery", on_load=[Dashboard.init_page(False), Auth.set_mode('up')])
def recovery() -> rx.Component:
    return rx.box(
        rx.center(
            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.image(src="/logo.svg", width="60px", border_radius="5px"),
                        rx.heading("Forgot Password", size="7"),
                        width="100%",
                        align="center",
                    ),    
                    rx.form(
                        rx.vstack(
                            rx.vstack(
                                rx.text("Username", size="3"),
                                rx.input(placeholder="ZeroSugar", width="100%", size="3", value=Auth.username_field, on_change=Auth.set_username),
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text("Recovery Code", size="3"),
                                rx.input(placeholder="PeachyPudding", width="100%", size="3", type="password", value=Auth.password_field, on_change=Auth.set_password),
                                width='100%',   
                            ),
                            rx.vstack(
                                rx.text("New password", size="3"),
                                rx.input(placeholder="PeachyPudding", width="100%", size="3", type="password", value=Auth.password_2_field, on_change=Auth.set_2_password),
                                width='100%',   
                            ),
                            rx.button("Forgot password", width="100%", size="3", type="submit", disabled=Auth.disabled),
                            spacing="5",
                            width="100%",
                            align="center"
                        ),
                        on_submit=Auth.recovery
                    ),
                    rx.hstack(
                        rx.text("Not here?"),
                        rx.link("Sign In", href="/signin"),
                    ),
                    spacing="5",
                    align="center",
                    padding="32px",
                ),
                width="500px",
                aspect_ratio="1/1",
                background_color = Dashboard.colors["widget"],
                border_radius= Dashboard.smoothness
            ),
            width="100%",
            height="100%",
        ),
        width="100vw",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["page"],
        color=Dashboard.colors["text"]
    )