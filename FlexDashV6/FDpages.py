import reflex as rx
from reflex.style import set_color_mode, color_mode
from .FDstates import Dashboard, System, Landing
from .FDcomponents import *
from .FDauth import Auth
from .FDapi import terracd_get_countdown

@rx.page("/home", title="FlexDash | Dashboard", on_load=[Dashboard.init_page, Dashboard.sync_down_cloud, Dashboard.update_all_widget(True)])
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
                    width=rx.cond(Dashboard.expanded, "87%", "100%"), 
                    height="100%", 
                    background_color = Dashboard.colors["page"], 
                    border_radius=Dashboard.smoothness
                ),
                rx.box(
                    rx.scroll_area(
                        rx.grid(
                            rx.foreach(
                                Dashboard.widgets,
                                lambda item: render_widget(item)
                            ),
                            padding="8px",
                            columns=Dashboard.widget_per_row,
                            gap="8px",
                        ),
                    ),
                    rx.moment(
                        interval=1000,
                        on_change=[
                            Dashboard.update_widget("",widget_type="pomodoro_v1"),  # type: ignore
                            Dashboard.update_widget("", widget_type="worldclock_v1"), # type: ignore
                            Dashboard.update_widget("", widget_type="terracd_v1"), # type: ignore
                            Dashboard.update_widget("", widget_type="terracd_v2") # type: ignore
                        ],
                        display="None",
                    ),
                    rx.moment(
                        interval= Dashboard.interval.to(int), # type: ignore
                        on_change=Dashboard.sync_up_cloud,
                        display="None"
                    ),
                    width=rx.cond(Dashboard.expanded, "87%", "100%"), 
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
                        rx.vstack(
                            rx.hstack(
                                rx.separator(flex_grow="1"),
                                rx.text("FlexDash V1 Widgets", white_space="nowrap", opacity=0.5),
                                rx.separator(flex_grow="1"),
                                width="100%",
                                align="center",
                                spacing="4",
                            ),
                            rx.grid(
                                rx.foreach(
                                    Dashboard.widgets_store,
                                    lambda item : widget(item.name, item.designed_type, item.image, item.desc, item.available),
                                ),
                                gap="8px",
                                columns="4",
                                width="100%",
                            ),
                            rx.hstack(
                                rx.separator(flex_grow="1"),
                                rx.text("FlexDash V2 Widgets", white_space="nowrap", opacity=0.5),
                                rx.separator(flex_grow="1"),
                                width="100%",
                                align="center",
                                spacing="4"
                            ),
                            rx.grid(
                                rx.foreach(
                                    Dashboard.widgets_storev2,
                                    lambda item : widget(item.name, item.designed_type, item.image, item.desc, item.available),
                                ),
                                gap="8px",
                                columns="4",
                                width="100%",
                            ),
                            width="100%",
                            height="100%",
                        ),
                        height="84vh",
                        width="100%",
                    ),
                    width="100%",
                    spacing="1",
                ),
                padding="8px",
                width=rx.cond(Dashboard.expanded, "87%", "100%"), 
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
                                            value= color_mode,
                                            on_change=[set_color_mode, Dashboard.edit_appearance], #type:ignore #PYLINT ERROR
                                            
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
                                    rx.text("Cloud Preferences", font_size="32px"),
                                    rx.spacer(),
                                    rx.text("Only triggers at Dashboard page.", font_size="14px", opacity=0.5),
                                    width="100%",
                                    align="end",
                                    ),
                                    rx.separator(),
                                    rx.vstack(
                                        rx.text("SYNC INTERVAL", font_size="16px", weight="bold"),
                                        rx.segmented_control.root(
                                            rx.segmented_control.item("30s", value="30000"),
                                            rx.segmented_control.item("60s", value="60000"),
                                            rx.segmented_control.item("90s", value="90000"),
                                            rx.segmented_control.item("120s", value="120000"),
                                            value= Dashboard.interval,
                                            on_change=Dashboard.edit_interval,
                                        ),
                                        spacing="1"
                                    ),
                                ),
                                height="100%",
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
                        rx.vstack(
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
                                width="100%",
                                border_radius=Dashboard.smoothness,
                                
                                background_color = Dashboard.colors["widget"],
                            
                            ),
                            width="50%",
                            height="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),
                padding="8px",
                width=rx.cond(Dashboard.expanded, "87%", "100%"), 
                height="100%", 
                background_color = Dashboard.colors["page"], 
                border_radius=Dashboard.smoothness
                ),
            width="100%",
            height="100%",
        ),
        width="100%",
        height="100vh",
        padding="8px",
        background_color = Dashboard.colors["page"],
        color=Dashboard.colors["text"]
    )

@rx.page("/signin", title="FlexDash | Sign in", on_load=[Dashboard.init_page(False), Auth.auto_signin, Auth.set_mode('in')])
def signin() -> rx.Component:
    return rx.box(
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.vstack(
                            rx.image(src="/logo_light.svg", width="60px", border_radius="5px"),
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
                                    rx.input(placeholder="MochiMunchies", width="100%", size="3", type="password", value=Auth.password_2_field, on_change=Auth.set_2_password),
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
                        rx.image(src="/logo_light.svg", width="60px", border_radius="5px"),
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
                        rx.image(src="/logo_light.svg", width="60px", border_radius="5px"),
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
                        rx.image(src="/logo_light.svg", width="60px", border_radius="5px"),
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

@rx.page("/", title="FlexDash | Landing", on_load=Landing.init)
def landing() -> rx.Component:
    def tech_stack(image, name, desc, link) -> rx.Component:
        return rx.hstack(
            rx.image(
                src=f"/landing_icons/{image}",
                height="32px",
                width="auto",
            ),
            rx.vstack(
                rx.text(name),
                rx.text(desc),
                spacing="1"
            ),
            rx.spacer(),
            rx.link(rx.icon("arrow_up_right", size=36, opacity=1, _hover={"opacity": 0.8}, href=link, is_external=True)),
            align="center",
            padding="12px",
            border_radius="8px",
            border="1px solid rgba(255, 255, 255, 0.15)",
            width="320px"
        )
    return rx.vstack(
        landing_header(),
        rx.scroll_area(
            rx.vstack(
                rx.box(
                    
                    rx.hstack(
                        rx.box(width="15%"),
                        rx.vstack(
                            rx.vstack(
                                rx.text("Your Dashboard, Your Way.", font_size="32px", weight="bold"),
                                rx.text("Design your own dashboard, your choice, your creativity. Everything customizable.", opacity=0.8),
                                spacing='2'
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.button(rx.text("Try Now", color="#FFFFFF"), variant="outline", width="128px", cursor="pointer", on_click=rx.redirect("#try")),
                                    rx.button(rx.text("Create Account", color="#FFFFFF"), variant="outline", width="128px", cursor="pointer", on_click=rx.redirect("/signup")),
                                ),
                                rx.button(rx.text("Enter Dashboard",  color="var(--gray-1)"), width="100%", background_color="var(--gray-12)", opacity=1, _hover={"opacity": 0.8}, cursor="pointer", on_click=rx.redirect("/home")),
                            ),
                            rx.vstack(
                                rx.text("Hosted with Cloudflare Tunnel.", opacity=0.8),
                                rx.hstack(
                                    rx.text("Completely Free & Open Sourced on ", opacity=0.8),
                                    rx.image(
                                        src="lockup-github-16.svg",
                                        filter="invert(100%)"
                                    ),
                                    align="center",
                                    opacity=0.8,
                                    _hover={"opacity": 1},
                                    on_click=rx.redirect("https://github.com/matthew-teh/PersonalDash", is_external=True),
                                    cursor="pointer",
                                ),
                                spacing='1'
                            ),
                            justify="between",
                            width="23%",
                            height="45%",
                        ),
                        rx.vstack(
                            rx.image(
                                src="/images/introduction.svg", 
                                border_radius="32px", 
                                width="100%", 
                                height="auto",
                                
                            ),
                            width="47%",
                            height="45%",
                            justify="center",
                            align="center",
                        ),
                        rx.box(width="15%"),
                        align="center",
                        height="100%",
                        spacing="2"
                    ),    
                    min_height="95vh", 
                    width="100%", 
                    background_color="var(--gray-2)",
                    id="home",
                ),
                rx.box(
                    rx.hstack(
                        rx.box(width="15%"),
                        rx.vstack(
                            rx.hstack(
                                rx.text("Explore Widgets", font_size="48px", weight="bold"),
                                rx.box(
                                    width="5%",
                                ),
                                rx.vstack(
                                    rx.text("Horizontal Scrolling", opacity=0.8),
                                    rx.hstack(
                                        rx.text("Shift", font_size="24px", padding="8px", border="1px solid rgba(255, 255, 255, 0.2)", border_radius="8px"),
                                        rx.text("+"),
                                        rx.text("Mouse Scroll", font_size="24px", padding="8px", border="1px solid rgba(255, 255, 255, 0.2)", border_radius="8px"),
                                        align="center",
                                    ),
                                    spacing="1",
                                ),

                               align="center",
                               width="100%",
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.dialog.root(
                                        rx.dialog.trigger(rx.text("Widgets V1", font_size="16px", opacity=0.8, _hover={"opacity": 1}, cursor="pointer")),
                                        rx.dialog.content(
                                            rx.box(
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Widgets Info", font_size="16px"),
                                                        rx.dialog.close(rx.icon('x', size=16, opacity=0.8, _hover={"opacity": 1})),
                                                        justify="between",
                                                        align="center",
                                                        width="100%",
                                                    ),
                                                    rx.vstack(
                                                        rx.text("Widgets Version 1", weight="bold"),
                                                        rx.text("These widgets are invented when the first project. They aren't that bad.", white_space="pre"),
                                                        spacing="2",
                                                    ),
                                                    rx.spacer(),
                                                    rx.vstack(
                                                        rx.hstack(
                                                            rx.text("Widgets exist since: PersonalDashboard V0, V1, V2", opacity=0.8),
                                                            rx.separator(orientation="vertical", min_height="24px"),
                                                            rx.text("FlexDash V3", opacity=0.8),
                                                        ),
                                                        rx.text("Crafted by Matthew :D", opacity=0.8),
                                                        spacing="1"
                                                    ),
                                                    height="100%",
                                                    spacing="4"
                                                    
                                                ),
                                                width="100%",
                                                height="100%",
                                            ),
                                            height="250px",
                                            aspect_ratio="2/1",
                                        ),

                                    ),
                                    rx.separator(orientation="vertical", min_height="16px"),
                                    rx.text("Click images below for more details", font_size="16px", opacity=0.8)
                                ),
                                rx.scroll_area(
                                    rx.hstack(
                                        rx.foreach(
                                            Dashboard.widgets_store, 
                                            lambda item : rx.box(
                                                rx.dialog.root(
                                                    rx.dialog.trigger(
                                                        rx.box(
                                                            rx.image(
                                                                src=f"{item.image}_dark.svg",
                                                                width="320px",
                                                                height="auto",
                                                                opacity=1,
                                                                _hover={"opacity": 0.8},
                                                                border_radius="8px",
                                                            ),
                                                            opacity=1,
                                                            _hover={"opacity": 0.8},
                                                            padding="0px",
                                                        ),
                                                    ),
                                                    rx.dialog.content(
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("Widget Info", font_size="24px"),
                                                                rx.dialog.close(rx.icon('x', opacity=0.8, _hover={"opacity": 1})),
                                                                width="100%",
                                                                justify="between",
                                                            ),
                                                            rx.vstack(
                                                                rx.image(
                                                                    src=f"{item.image}_dark.svg",
                                                                    width="360px",
                                                                    height="auto",
                                                                    border_radius="8px"
                                                                ),
                                                                rx.text(item.desc),
                                                                rx.button(
                                                                    rx.text("Add to my dashboard", color="#000000"),
                                                                    background_color="#FFFFFF",
                                                                    width="100%",
                                                                    opacity=1,
                                                                    _hover={"opacity": 0.8},
                                                                    on_click=rx.toast("This Feature Is Coming Soon"), # TODO : Make 
                                                                ),
                                                                height="100%",
                                                                justify="between",
                                                            ),
                                                            padding="8px",
                                                            height="100%",
                                                            width="100%"
                                                        ),
                                                        background_color="var(--gray-2)",
                                                        width="380px",
                                                    ),
                                                ),
                                                width="320px",
                                                background_color="var(--gray-2)",
                                                padding="1px",
                                            ),
                                        )
                                    ),
                                    scroll_bars="horizontal",
                                    max_height="100%",
                                    max_width="100%",
                                ),
                                width="100%",
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.dialog.root(
                                        rx.dialog.trigger(rx.text("Widgets V2", font_size="16px", opacity=0.8, _hover={"opacity": 1}, cursor="pointer")),
                                        rx.dialog.content(
                                            rx.box(
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Widgets Info", font_size="16px"),
                                                        rx.dialog.close(rx.icon('x', size=16, opacity=0.8, _hover={"opacity": 1})),
                                                        justify="between",
                                                        align="center",
                                                        width="100%",
                                                    ),
                                                    rx.vstack(
                                                        rx.text("Widgets Version 2", weight="bold"),
                                                        rx.text("These widgets are either refined from Widgets Version 1 or newly created.\nTheir designs are completely different from Version 1.", white_space="pre"),
                                                        spacing="2"
                                                    ),
                                                    rx.spacer(),
                                                    rx.vstack(
                                                        rx.text("Widgets exist since: FlexDash V4, V5, V6", opacity=0.8),
                                                        rx.text("Also Crafted by Matthew :D", opacity=0.8),
                                                        spacing="1"
                                                    ),
                                                    height="100%",
                                                    spacing="4",
                                                ),
                                                height="100%",
                                                width="100%",
                                            ),
                                            height="250px",
                                            aspect_ratio="2/1"
                                        ),
                                    ),
                                    rx.separator(orientation="vertical", min_height="16px"),
                                    rx.text("Click images below for more details", font_size="16px", opacity=0.8),
                                    align="center"
                                ),
                                rx.scroll_area(
                                    rx.hstack(
                                        rx.foreach(
                                            Dashboard.widgets_storev2, 
                                            lambda item : rx.box(
                                                rx.dialog.root(
                                                    rx.dialog.trigger(
                                                        rx.box(
                                                            rx.image(
                                                                src=f"{item.image}_dark.svg",
                                                                width="320px",
                                                                height="auto",
                                                                opacity=1,
                                                                _hover={"opacity": 0.8},
                                                                border_radius="8px",
                                                            ),
                                                            opacity=1,
                                                            _hover={"opacity": 0.8},
                                                            padding="0px",
                                                        ),
                                                    ),
                                                    rx.dialog.content(
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("Widget Info", font_size="24px"),
                                                                rx.dialog.close(rx.icon('x', opacity=0.8, _hover={"opacity": 1})),
                                                                width="100%",
                                                                justify="between",
                                                            ),
                                                            rx.vstack(
                                                                rx.image(
                                                                    src=f"{item.image}_dark.svg",
                                                                    width="360px",
                                                                    height="auto",
                                                                    border_radius="8px"
                                                                ),
                                                                rx.text(item.desc),
                                                                rx.button(
                                                                    rx.text("Add to my dashboard", color="#000000"),
                                                                    background_color="#FFFFFF",
                                                                    width="100%",
                                                                    opacity=1,
                                                                    _hover={"opacity": 0.8},
                                                                    on_click=rx.toast("This Feature Is Coming Soon"), # TODO : Make 
                                                                ),
                                                                height="100%",
                                                                justify="between",
                                                            ),
                                                            padding="8px",
                                                            height="100%",
                                                            width="100%"
                                                        ),
                                                        background_color="var(--gray-2)",
                                                        width="380px",
                                                    ),
                                                ),
                                                width="320px",
                                                background_color="var(--gray-2)",
                                                padding="1px",
                                            ),
                                        )
                                    ),
                                    scroll_bars="horizontal",
                                    max_height="100%",
                                    max_width="100%",
                                ),
                                width="100%",
                            ),
                            width="70%",
                            justify="center",
                            height="100%",
                        ),
                        rx.box(width="15%"),
                        height="100%",
                        id="explore_widgets",
                    ),
                    min_height="95vh",
                    width="100%",
                    background_color="var(--gray-2)",
                ),
                rx.box(
                    rx.hstack(
                        rx.box(width="15%"),
                        rx.box(
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Try Now", weight="bold", font_size="48px"),
                                    rx.vstack(
                                        rx.text("Our widgets are live updates, interactive."),
                                        rx.text("It's at right side, try it."),
                                        rx.text("Still under testing, more widgets coming soon", opacity=0.8),
                                    ),
                                    spacing="1",
                                ),
                                rx.spacer(),
                                rx.hstack(
                                    rx.box(
                                        rx.hstack(
                                            rx.image(src="/lucide_icons/book_dark.svg", height="42px", width="auto"),
                                            rx.vstack(
                                                rx.heading("Quick Notes", size="3"),
                                                rx.text("A text area to make note."),
                                                spacing="0",
                                            ),
                                            height="20%",
                                        ),
                                        rx.hstack(
                                            rx.text_area(
                                                placeholder="Start typing here...",  
                                                width="100%",
                                                height="100%"
                                            ),
                                            width="100%",
                                            height="80%",
                                            spacing="0"
                                        ),
                                        padding="8px",
                                        width="50%",
                                        aspect_ratio="1/1",
                                        border_radius="8px",
                                        border="1px dashed rgba(255, 255, 255, 0.1)"
                                    ),
                                    rx.box(
                                        rx.hstack(
                                            rx.image(src=f"/lucide_icons/clock_fading_dark.svg", width="30px"),
                                            rx.text("TERRA COUNTDOWN", weight="bold", font_size="20px"),
                                            rx.spacer(),
                                            spacing="2",
                                            align="center",
                                            width="100%",
                                            height="32px",
                                        ),
                                        rx.center(
                                            rx.vstack(
                                                rx.hstack(
                                                    rx.vstack(circle_progress(Landing.time[0].to(float)/6, 125, Landing.time[0]), rx.text("Days"), align="center", spacing="0"), #type:ignore
                                                    rx.vstack(circle_progress(Landing.time[0].to(float)/24, 125, Landing.time[1]), rx.text("Hours"), align="center", spacing="0"), #type:ignore
                                                    width="100%",
                                                ),
                                                rx.hstack(
                                                    rx.vstack(circle_progress(Landing.time[2].to(float)/60, 125, Landing.time[2]), rx.text("Minutes"), align="center", spacing="0"), #type:ignore
                                                    rx.vstack(circle_progress(Landing.time[3].to(float)/60, 125, Landing.time[3]), rx.text("Seconds"), align="center", spacing="0"), #type:ignore
                                                ),
                                            ),
                                            flex="1",
                                            min_height = 0,
                                        ),
                                        rx.moment(
                                          interval=1000,
                                          on_change=Landing.update_time,
                                          display="none",
                                        ),
                                        display="flex",
                                        flex_direction="column",
                                        padding="8px",
                                        width="50%",
                                        aspect_ratio="1/1",
                                        border_radius="8px",
                                        border="1px dashed rgba(255, 255, 255, 0.1)"
                                    ),
                                    width="60%",
                                    align="center",
                                    justify="center",
                                ),
                                width="100%",
                                height="100%",
                                align="center",
                                id="try",
                            ),
                            height="100%",
                            width="70%",
                        ),
                        rx.box(width="15%"),
                        width="100%",
                        height="100%",
                    ),
                    min_height="95vh",
                    width="100%",
                    background_color="var(--gray-2)",
                ),
                rx.box(
                    rx.hstack(
                        rx.box(width="15%"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Tech Stack", weight="bold", font_size="48px"),
                                rx.text("We uses these tools below to achieve this website.", opacity=0.8),
                                tech_stack("python_logo.svg", "Main Language", "Python 3.14", "https://www.python.org/downloads/release/python-3140/"),
                                tech_stack("reflex.svg", "Frontend and Backend", "Reflex Python", "https://reflex.dev"),
                                tech_stack("dragonfly.svg", "Database", "DragonflyDB", "https://www.dragonflydb.io/"),
                                tech_stack("cloudflared.svg", "Hosting", "Cloudflare Tunnel", "https://developers.cloudflare.com/tunnel/"),
                                width="50%",
                            ),
                            rx.vstack(
                                rx.text("How it Works", weight="bold", font_size="48px"),
                                rx.text("Below is a simple working on FlexDash.", opacity=0.8),
                                rx.box(
                                    rx.vstack(
                                        rx.text("Client / Website", padding="12px", border_radius="8px", border="1px solid rgba(255, 255, 255, 0.15)", width="100%", align="center"),
                                        rx.hstack(
                                            rx.box(width="5%"),
                                            rx.hstack(
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto"),
                                                rx.text("HTTPS TLS", width="45%", align="center"),
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto", transform="rotate(180deg)"),
                                                width="40%",
                                                align="center",
                                                justify="center"
                                            ),
                                            rx.box(width="10%"),
                                            rx.hstack(
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto"),
                                                rx.text("WEBSOCKET", width="45%", align="center"),
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto", transform="rotate(180deg)"),
                                                width="40%",
                                                align="center", 
                                                justify="center"
                                            ),
                                            rx.box(width="5%"),
                                            align="center",
                                            width="100%"
                                        ),
                                        rx.text("Cloudflare Tunnel", padding="12px", border_radius="8px", border="1px solid rgba(255, 255, 255, 0.15)", width="100%", align="center"),
                                        rx.hstack(
                                            rx.box(width="5%"),
                                            rx.hstack(
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto"),
                                                rx.text("FRONTEND", width="45%", align="center"),
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto", transform="rotate(180deg)"),
                                                width="40%",
                                                align="center",
                                                justify="center"
                                            ),
                                            rx.box(width="10%"),
                                            rx.hstack(
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto"),
                                                rx.text("BACKEND", width="45%", align="center"),
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto", transform="rotate(180deg)"),
                                                width="40%",
                                                align="center",
                                                justify="center"
                                            ),
                                            rx.box(width="5%"),
                                            align="center",
                                            width="100%"
                                        ),     
                                        rx.hstack(
                                            rx.text("Reflex React / Node.js", padding="12px", border_radius="8px", border="1px solid rgba(255, 255, 255, 0.15)", width="100%", align="center"),
                                            rx.text("Reflex State", padding="12px", border_radius="8px", border="1px solid rgba(255, 255, 255, 0.15)", width="100%", align="center"),
                                            width="100%",
                                        ),                                
                                        rx.hstack(
                                            rx.box(width="40%"),
                                            rx.box(width="10%"),
                                            rx.box(width="5%"), # TO MATCH HSTACK SPACING, used 3 rx.Box.
                                            rx.hstack(
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto"),
                                                rx.box(width="45%", padding="0px"),
                                                rx.image(src="matthew_icons/arrow.svg", height="32px", width="auto", transform="rotate(180deg)"),
                                                align="center",
                                                justify="center",
                                                width="40%",
                                            ),
                                            rx.box(width="5%"),
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.box(width="50%"),
                                            rx.box(
                                                rx.text("Dragonfly DB", padding="12px", border_radius="8px", border="1px solid rgba(255, 255, 255, 0.15)", width="100%", align="center"),
                                                width="50%",
                                            ),
                                            width="100%",
                                        ),
                                    ),
                                    width="100%",
                                    padding="12px",
                                    border_radius="8px",
                                ),
                                width="50%",
                            ),
                            width="70%",
                        ),
                        rx.box(width="15%"),
                        width="100%",
                    ),
                    min_height="95vh",
                    width="100%",
                    background_color="var(--gray-2)",
                    padding="32px",
                    id="how_it_works"
                ),
                landing_footer(),
                margin="0px",
                padding_left="4px",
                padding_right="4px",
                justify="start",
                align="center",
                width="100vw",
                height="100vh",
                background_color="var(--gray-2)",
                spacing="0"
            ),
            height="100vh",
            width="100vw",
            type="scroll",
        ),
        spacing="0",
        height="100vh",
        width="100vw",
    )

@rx.page("/account", title="FlexDash | Account", on_load=[Dashboard.init_page, Auth.prepare_devices])
def account() -> rx.Component:
    return rx.box(
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.text("Account Settings", weight="bold", font_size="64px", opacity=0.95, margin_bottom="16px",),               
                ),
                rx.hstack(

                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.text("Account Info", font_size="32px"),
                                rx.separator(),
                                rx.text(f"Username: {Auth.logged_username}")
                            ),
                            padding="32px",
                            border_radius=Dashboard.smoothness,
                            background_color=Dashboard.colors["widget"],
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Devices Logged In", font_size="32px"),
                                rx.separator(),
                                rx.scroll_area(
                                    rx.table.root(
                                        rx.table.header(
                                            rx.table.row(
                                                rx.table.column_header_cell("Device Name"),
                                                rx.table.column_header_cell("IP Address"),
                                                rx.table.column_header_cell("Time EST"),
                                                rx.table.column_header_cell("Last Active"),
                                                rx.table.column_header_cell("Action"),
                                            ),
                                        ),
                                        rx.table.body(
                                            rx.foreach(Auth.logged_devices, show_devices),
                                        ),
                                    ),
                                height="255px",
                                width="100%",
                                ),
                            ),
                            padding="32px",
                            border_radius=Dashboard.smoothness,
                            background_color=Dashboard.colors["widget"],
                            width="100%",
                        ),
                        width="50%",
                    ),
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.text("Account Actions", font_size="32px"),
                                rx.separator(),
                                rx.hstack(
                                    rx.dialog.root(
                                        rx.dialog.trigger(rx.button("Sign out", color_scheme=Dashboard.colors["name"])), # type: ignore
                                            rx.dialog.content(
                                                rx.vstack(
                                                    rx.heading("Are you sure?", size="4"),
                                                    rx.hstack(
                                                        rx.button("Yes", color_scheme="tomato", variant="outline", size="3", on_click=Auth.sign_out),
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
                                    rx.dialog.root(
                                        rx.dialog.trigger(rx.button("Change password", color_scheme=Dashboard.colors["name"])), # type: ignore
                                            rx.dialog.content(
                                                rx.vstack(
                                                    rx.heading("Change password", size="4"),
                                                    rx.form(
                                                        rx.vstack(
                                                            rx.text("Current password"),
                                                            rx.input(placeholder="Blushies", width="100%", type="password", value=Auth.username_field, on_change=Auth.set_username),
                                                            rx.text("New Password"),
                                                            rx.input(placeholder="NotBlushies", width="100%", type="password", value=Auth.password_field, on_change=Auth.set_password),
                                                            rx.text("Confirm New password",),
                                                            rx.input(placeholder="NotBlushies", width="100%", type="password", value=Auth.password_2_field, on_change=Auth.set_2_password),
                                                            rx.center(
                                                                rx.button("Change password", background_color=Dashboard.colors["buttons"]),
                                                                width="100%",
                                                            ),
                                                        ),
                                                        on_submit=Auth.change_password,
                                                    ),
                                                    width="100%",
                                                    align="center",
                                                    spacing="5"
                                                ),
                                                width="300px",
                                            ),
                                        on_blur=Auth.clear,
                                    ),

                                    spacing="2",
                                    width="100%"
                                ),
                                width="100%",
                            ),
                            height="100%",
                            padding="32px",
                            width="100%",
                            border_radius=Dashboard.smoothness,
                            background_color = Dashboard.colors["widget"],
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Dangerous Area", font_size="32px"),
                                rx.separator(),
                                rx.dialog.root(
                                    rx.dialog.trigger(rx.button("Delete Account", color_scheme="tomato", variant="outline", width="70px", height="70px")),
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
                                                        value=Auth.password_2_field, 
                                                        on_change=Auth.set_2_password,
                                                        width="100%",
                                                        size="3",
                                                        required=True
                                                    ),
                                                    rx.button("Submit", color_scheme="tomato", variant="outline", width="100%"),
                                                    width="100%",
                                                ),  
                                                on_submit=Auth.delete_account,
                                                width="100%",
                                            ),
                                            width="100%",
                                        ),
                                        width="100%",
                                    ),

                                ),
                                width="100%",
                            ),
                            height="100%",
                            padding="32px",
                            width="100%",
                            border_radius=Dashboard.smoothness,
                            background_color = 'var(--ruby-3)',
                        ),
                        width="50%",
                    ),
                ),
                width=rx.cond(Dashboard.expanded, "87%", "100%"), 
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

