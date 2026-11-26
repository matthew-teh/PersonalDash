import reflex as rx

from .FDstates import Dashboard, Landing
from .FDauth import Auth
from . import FDwidgetsV1
from . import FDwidgetsV2

# ---- SIDEBAR START
def sidebar_items(name: str, image: str, link: str, redirect: bool) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.image(src=f"{image}_{Dashboard.appearance}.svg"),
            rx.cond(Dashboard.expanded, rx.text(name, font_size="16px", color=Dashboard.colors["text"], white_space="nowrap"), rx.fragment()),
            width="100%",
            height="100%",
            align="center",
            justify=rx.cond(Dashboard.expanded, "start", "center"),
        ),
        opacity = rx.cond(Dashboard.page == link.lower(), 1 , 0.5),
        _hover={"opacity": 1.0},
        transition="all 0.2s ease-in-out",
        width="100%",
        variant="ghost",
        border_radius=Dashboard.smoothness,
        height="32px",
        on_click= Dashboard.set_page(link, redirect),
        border = rx.cond(
            Dashboard.page == link.lower(), 
            rx.cond(
                Dashboard.appearance=="dark",
                "1px solid rgba(255, 255, 255, 0.2)",
                "1px solid rgba(0, 0, 0, 0.2)"
            ),
            "1px solid transparent"
            )
    )
def sidebar_items_functional(name: str, image: str, function) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.image(src=f"{image}_{Dashboard.appearance}.svg"),
            rx.cond(Dashboard.expanded, rx.text(name, font_size="16px", color=Dashboard.colors["text"], white_space="nowrap"), ""),
            width="100%",
            height="100%",
            align_items="center",
            justify=rx.cond(Dashboard.expanded, "start", "center"),
        ),
        opacity = 0.5,
        _hover={"opacity": 1.0},
        transition="opacity 0.2s ease-in-out",
        width="100%",
        variant="ghost",
        border_radius=Dashboard.smoothness,
        height="32px",
        on_click=function,
    )

def sidebar_separator(text) -> rx.Component:
    return rx.cond(
        Dashboard.expanded,
        rx.hstack(
            rx.separator(flex_grow="1"),
            rx.text(text, font_size="12px", opacity=0.8, white_space="nowrap"),
            rx.separator(flex_grow="1"),
            spacing="4",
            align="center",
            width="100%",
            height="40px"
        ),
        rx.hstack(rx.separator(flex_grow="1"), width="100%", spacing="4", align="center", height="40px"),
    )
def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.image(
                    src=f"/logo_{Dashboard.appearance}.svg", 
                    border_radius="4px", 
                    width=rx.cond(Dashboard.expanded, "19%", "48px"),
                    height="auto",
                    on_click=Dashboard.flip_expanded,
                ),
                rx.cond(
                    Dashboard.expanded,                
                    rx.vstack(
                        rx.text("FlexDash V4", weight="bold", font_size="24px", white_space="nowrap"),
                        rx.text(Auth.logged_username, font_size="16px", opacity=0.5),
                        spacing="0",    
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                align_items="center",
                min_height="58px",
            ),  
            rx.vstack(
                sidebar_separator("Widgets Home"),
                sidebar_items("Dashboard", "/lucide_icons/house", "/home", True),
                sidebar_items("Add widgets", "/lucide_icons/shopping_bag", "/widgets", True),
                sidebar_separator("Widgets control"),
                sidebar_items_functional("Refresh all", "/lucide_icons/refresh_cw", Dashboard.update_all_widget),
                sidebar_items_functional("Delete all", "/lucide_icons/trash", Dashboard.delete_all_widget),
                sidebar_separator("Cloud Status"),
                sidebar_items_functional("Sync now", "/lucide_icons/cloud_sync", Dashboard.sync_up_cloud),
                rx.hstack(
                    rx.image(src=f"/lucide_icons/cloud_check_{Dashboard.appearance}.svg"),
                    rx.cond(Dashboard.expanded,rx.text(Dashboard.sync_status, white_space="nowrap"), rx.fragment()),
                    opacity = 0.5,
                    _hover={"opacity": 1.0},
                    transition="opacity 0.2s ease-in-out",
                    width="100%",
                    variant="ghost",
                    border_radius=Dashboard.smoothness,
                    height="32px",
                    justify=rx.cond(Dashboard.expanded, "start", "center"),
                ),
                rx.flex(
                    rx.vstack(
                        rx.image(src=f"lucide_icons/square_dashed_mouse_pointer_{Dashboard.appearance}.svg", opacity=rx.cond(Dashboard.parking, 1.0, 0.5)),
                        rx.cond(
                            Dashboard.expanded,
                            rx.cond(
                                Dashboard.parking,
                                rx.text("CURSOR PARKED HERE", opacity=1.0, white_space="nowrap"),
                                rx.text("CURSOR PARKING AREA", opacity=0.5, white_space="nowrap"),
                            ),
                            rx.fragment(),
                        ),
                        align="center",
                        justify="center",
                        height="100%",
                        width="100%",
                        
                    ),
                    height="100%",
                    width="100%",
                    border_radius= Dashboard.smoothness,
                    background_color = Dashboard.colors["widget"],
                    cursor="none",
                    on_mouse_enter=Dashboard.sidebar_parking(True),
                    on_mouse_leave=Dashboard.sidebar_parking(False),
                ),


                sidebar_separator("Preferences"),
                sidebar_items("Account", "/lucide_icons/user_round", "/account", True),
                sidebar_items("Settings", "/lucide_icons/settings", "/settings", True),
                width="96%",
                height="100%",
                justify="center",
                align="center",
            ),
            height="100%",
            align="center"
        ),
        width=rx.cond(Dashboard.expanded, "13%", "2.5%"),
        height="100%",
        padding="8px",
        border_radius=Dashboard.smoothness,
        color=Dashboard.colors["text"],
        overflow="hidden",
        style={
            "transition" : "width 0.2s ease-in-out",
        },
    )
        


# ---- SIDEBAR ENDS

# ---- WIDGETS STARTS
def widget(name: str, type:str, image:str="", desc: str="", available: bool=False):
    is_active = Dashboard.widget_store_name == type
    return rx.card(
        rx.vstack(
            rx.text(name, weight="bold"),
            rx.cond(
                image,
                rx.image(
                    src=f"{image}_{Dashboard.appearance}.svg",
                    width="260px",
                    height="260px",
                    border_radius=Dashboard.smoothness,
                ),

                rx.text("Widget placeholder")
            ),
            rx.box(
                rx.text(desc),
                rx.flex(
                    rx.button(rx.text("Add to dashboard", color=Dashboard.colors["text"]), border_radius=Dashboard.smoothness, width="100%", background_color=Dashboard.colors["buttons"], on_click=Dashboard.add_widget(type)),
                    width="100%",
                    opacity=rx.cond(is_active, 1, 0),   
                    transition="all 0.3s ease-in-out",
                    overflow="hidden",
                    max_height=rx.cond(is_active, "60px", "0px",),
                ),
                padding="0px",
                width="100%",
            ),
            overflow="hidden",
            width="100%",
            aspect_ratio="1 / 1",
            align = "center",
            justify="between",
        ),
        on_mouse_enter=Dashboard.set_widget_store_name(type),
        on_mouse_leave=Dashboard.set_widget_store_name(value=""),
        border_radius=Dashboard.smoothness,
        color=Dashboard.colors["text"]
    )

def render_widget(item: dict) -> rx.Component:
    return rx.box(
        rx.match(
            item["type"].lower(),
            ("crypto_v1", FDwidgetsV1.crypto_widget(item)),
            ("weather_v1", FDwidgetsV1.weather_widget(item)),
            ("worldclock_v1", FDwidgetsV1.worldclock_widget(item)),
            ("pomodoro_v1", FDwidgetsV1.pomodoro_widget(item)),
            ("quicknotes_v1", FDwidgetsV1.quicknotes_widget(item)),
            ("terracd_v1", FDwidgetsV1.terracd_widget(item)),
            ("crypto_v2", FDwidgetsV2.crypto_widget(item)),
            ("checklist_v2", FDwidgetsV2.checklist_widget(item)),
            ("terracd_v2", FDwidgetsV2.terracd_widget(item)),
            rx.box(),   
        ),
    )
# ---- WIDGETS ENDS

def show_devices(device: list):
    return rx.table.row(
        rx.table.cell(
            rx.cond(
                device[0].contains("|"),
                rx.vstack(
                    rx.text(f"* {device[0].split("|")[1]}"),
                    rx.text(device[0].split("|")[0]),
                    spacing="0"
                ),
                rx.text(device[0])
            ),
        ),
        rx.table.cell(device[1]),
        rx.table.cell(device[2]),
        rx.table.cell(device[3]),
        rx.table.cell(
            rx.dialog.root(
                rx.dialog.trigger(rx.button("Logout", variant='ghost', border_radius=Dashboard.smoothness, border=f"1px solid {Dashboard.colors["buttons"]}", on_click=Auth.clear)),
                rx.dialog.content(
                    rx.vstack(
                        rx.hstack(
                            rx.text(f"Enter password to continue"),
                            rx.dialog.close(rx.icon('x'), opacity=0.5, _hover={"opacity": 1}),
                            justify="between",
                            width="100%",
                        ),
                        
                        rx.input(
                            placeholder="OvercookChicken", 
                            width="100%", 
                            value=Auth.password_field, 
                            on_change=Auth.set_password,
                            on_key_down=lambda key: rx.cond(
                                key == "Enter",
                                Auth.handle_logout_device(device[4]),
                                None,
                            ),
                            type="password"
                        ),
                        rx.button(rx.text("Continue"), width="100%", on_click=Auth.handle_logout_device(device[4])),
                        width="100%",
                    )
                )
            )
        )
    )

def circle_progress(progress, size, label) -> rx.Component:
    circumference = 251.2
    progress_val = progress
    stroke_dashoffset = circumference - (progress_val * circumference)
    swid = max(2, size * 0.03)
    return rx.el.svg(
        rx.el.circle(
            cx="50",
            cy="50",
            r="40",
            fill="none",
            stroke=Dashboard.colors["page"],
            stroke_width=swid,
        ),
        rx.el.circle(
            cx="50",
            cy="50",
            r="40",
            fill="none",
            stroke=Dashboard.colors["text"],
            stroke_width=swid,
            stroke_dasharray=str(circumference),
            stroke_dashoffset=stroke_dashoffset,
            stroke_linecap="round",
            style={
                "transform": "rotate(-90deg)",
                "transform-origin": "50px 50px",
                "transition": "stroke-dashoffset 0.5s ease-in-out",
            },
        ),
        rx.el.text(
            label,
            x="50",
            y="50",
            text_anchor="middle",
            dominant_baseline="central",
            fill=Dashboard.colors["text"], # Adjusted for your dark background
            font_size="32px",
            font_weight="500",
            opacity=0.8
        ),
        view_box="0 0 100 100",
        width=f"{size}px",
        height=f"{size}px",
    )



def create_link(text, link, external=False, paddin=False) -> rx.Component:
    return rx.text(
        text,
        font_size="16px",
        padding= rx.cond(
            paddin,
            "0px 12px 0px 12px",
            "0px"
        ),
        border_radius="4px",
        _hover={"opacity": 2},
        cursor="pointer",
        opacity= rx.cond(Landing.on_page.lower() == link.lower(), 1, 0.8),
        on_click=rx.redirect(link, is_external=external),
    )
    
def landing_header() -> rx.Component:
    return rx.hstack(
        rx.box(width="15%"),
        rx.image(src="/logo_light.svg", height="100%", width="auto", border_radius="8px",  border="1px solid rgba(255, 255, 255, 0.25)"),
        rx.text("FlexDash", weight="bold", font_size="20px"),
        rx.spacer(),
        rx.hstack(
            create_link("Home", "#home", False, True),
            create_link("Explore widgets", "#explore_widgets", False, True),
            create_link("Try it out", "#try", False, True),
            create_link("How it works", "#how_it_works", False, True),
            align="center",
            height="100%"
        ),
        rx.spacer(),
        rx.button(rx.text("Sign In", color="#FFFFFF"), variant="outline", color_scheme="mint", on_click=rx.redirect("/signin"), cursor="pointer"),
        rx.button(rx.text("Sign Up", color="#000000"), background_color="var(--gray-12)", opacity=1, _hover={"opacity": 0.8}, on_click=rx.redirect("/signup"), cursor="pointer"),
        rx.box(width="15%"),
        background_color="var(--gray-2)",
        height="5vh",
        width="100%",
        padding="8px",
        align="center",
        border_bottom="1px solid rgba(255, 255, 255, 0.15)"
    )

def landing_footer() -> rx.Component:
    return rx.hstack(
        rx.box(width="15%"),
        rx.hstack(
            rx.image(src="/logo_light.svg", height="40px", width="auto", border_radius="8px", border="1px solid rgba(255, 255, 255, 0.25)"),
            rx.vstack(
                rx.text("FlexDash", weight="bold", font_size="20px"),
                rx.text("2026", opacity=0.6),
                spacing="0",
                height="100%"
            ),
            align="center",
        ),
        rx.spacer(),
        rx.vstack(
            rx.text("Links", weight="bold"),
            create_link("Home", "#home"),
            create_link("Explore widgets", "#explore_widgets"),
            create_link("Try", "#try"),
            create_link("How it works", "#how_it_works"),
            spacing="2"
        ),
        rx.spacer(),
        rx.vstack(
            rx.text("Social", weight="bold"),
            create_link("Slack", "https://hackclub.enterprise.slack.com/team/U0A9CFG6519", True),
            create_link("GitHub", "https://github.com/matthew-teh", True),
            create_link("Hackatime", "https://hackatime.hackclub.com/@Matthew-Teh", True),
            create_link("Instagram", "https://www.instagram.com/matthew._.teh?avpt=amUyZ2Y0ejR0MjZ5", True),
            spacing="2"
        ),
        rx.spacer(),
        rx.vstack(
            rx.text("Tech Stack", weight="bold"),
            create_link("Python", "https://www.python.org/", True),
            create_link("Reflex", "https://reflex.dev/", True),
            create_link("DragonflyDB", "https://www.dragonflydb.io/", True),
            create_link("Cloudflare Tunnel", "https://developers.cloudflare.com/tunnel/", True),
        ),
        rx.spacer(),
        rx.vstack(
            rx.vstack(
                rx.text("Open Source", weight="bold"),
                rx.hstack(
                    rx.box(
                        rx.hstack(
                            rx.text("Available on"),
                            rx.image(src="/lockup-github-16.svg", filter="invert(100%)"), 
                            align="center"
                        ),
                        on_click= rx.redirect("https://github.com/matthew-teh/PersonalDash", is_external=True),
                        hover="none",
                        cursor="pointer",
                    ),# todo: make attribution
                    align="center",
                    opacity=0.8,
                    _hover={"opacity": 1}
                ),
            ),
            rx.vstack(
                rx.text("Status", weight="bold"),
                create_link("All System Normal", "https://status.flexdasboard.xyz", True),
                spacing="1"
            ),
            spacing="3"
        ),
        rx.box(width="15%"),
        background_color="var(--gray-2)",
        height="22%",
        width="100%",
        padding="32px 8px 8px 8px",
        border_top="1px solid rgba(255, 255, 255, 0.15)"
    )