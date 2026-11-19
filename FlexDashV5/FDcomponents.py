import reflex as rx

from .FDstates import Dashboard
from .FDauth import Auth
from . import FDwidgetsV1
from . import FDwidgetsV2

# ---- SIDEBAR START
def sidebar_items(name: str, image: str, link: str, redirect: bool) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.image(src=f"{image}_{Dashboard.appearance}.svg"),
            rx.text(name, font_size="16px", color=Dashboard.colors["text"]),
            width="100%",
            height="100%",
            align="center",
        ),
        opacity = rx.cond(Dashboard.page == link.lower(), 1 , 0.5),
        _hover={"opacity": 1.0},
        transition="all 0.2s ease-in-out",
        width="100%",
        variant="ghost",
        border_radius=Dashboard.smoothness,
        height="32px",
        on_click= Dashboard.set_page(link, redirect),
        border = rx.cond(Dashboard.page == link.lower(), "1px solid rgba(255, 255, 255, 0.2)", "1px solid transparent"),
        
    )

def sidebar_items_functional(name: str, image: str, function) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.image(src=f"{image}_{Dashboard.appearance}.svg"),
            rx.text(name, font_size="16px", color=Dashboard.colors["text"]),
            width="100%",
            height="100%",
            align="center",
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

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.image(src="/logo.svg", border_radius="4px", width="19%", height="auto"),
                rx.vstack(
                    rx.text("FlexDash V4", weight="bold", font_size="24px"),
                    rx.text(Auth.logged_username, font_size="16px", opacity=0.5),
                    spacing="0",    
                    width="100%",
                ),
                align_items="center",
            ),  
            rx.vstack(
                rx.hstack(rx.separator(max_width="25%"), rx.text("Widgets home", font_size="12px", opacity=0.8), rx.separator(max_width="25%"), width="100%", justify="between", align="center"),
                sidebar_items("Dashboard", "/lucide_icons/house", "/home", True),
                sidebar_items("Add widgets", "/lucide_icons/shopping_bag", "/widgets", True),
                rx.hstack(rx.separator(max_width="25%"), rx.text("Widgets control", font_size="12px", opacity=0.8), rx.separator(max_width="25%"), width="100%", justify="between", align="center"),
                sidebar_items_functional("Refresh all", "/lucide_icons/refresh_cw", Dashboard.update_all_widget),
                sidebar_items_functional("Delete all", "/lucide_icons/trash", Dashboard.delete_all_widget),
                rx.hstack(rx.separator(max_width="25%"), rx.text("Cloud status", font_size="12px", opacity=0.8), rx.separator(max_width="25%"), width="100%", justify="between", align="center"),
                sidebar_items_functional("Sync now", "/lucide_icons/cloud_sync", Dashboard.sync_up_cloud),
                rx.hstack(
                    rx.image(src=f"/lucide_icons/cloud_check_{Dashboard.appearance}.svg"),
                    rx.text(Dashboard.sync_status),
                    opacity = 0.5,
                    _hover={"opacity": 1.0},
                    transition="opacity 0.2s ease-in-out",
                    width="100%",
                    variant="ghost",
                    border_radius=Dashboard.smoothness,
                    height="32px",
                ),
                rx.flex(
                    rx.vstack(
                        rx.image(src=rx.cond(Dashboard.appearance=="dark","lucide_icons/square_dashed_mouse_pointer_dark.svg", "lucide_icons/square_dashed_mouse_pointer_light.svg"), opacity=rx.cond(Dashboard.parking, 1.0, 0.5)),
                        rx.cond(
                            Dashboard.parking,
                            rx.text("CURSOR PARKED HERE", opacity=1.0, white_space="pre-wrap"),
                            rx.text("CURSOR PARKING AREA", opacity=0.5, white_space="pre-wrap"),
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


                rx.hstack(rx.separator(max_width="25%"), rx.text("Preferences", font_size="12px", opacity=0.8), rx.separator(max_width="25%"), width="100%", justify="between", align="center"),
                sidebar_items("Account", "/lucide_icons/user_round", "/account", True),
                sidebar_items("Settings", "/lucide_icons/settings", "/settings", True),
                width="100%",
                height="100%",
            ),
            height="100%",
            align="center"
        ),
        width="13%",
        height="100%",
        padding="8px",
        border_radius=Dashboard.smoothness,
        color=Dashboard.colors["text"]
    )


# ---- SIDEBAR ENDS

# ---- WIDGETS STARTS
def widget(name: str, image:str="", desc: str="", available: bool=False):
    is_active = Dashboard.widget_store_name == name
    return rx.card(
        rx.vstack(
            rx.text(name, weight="bold"),
            rx.cond(
                image,
                rx.image(
                    src=f"{image}_{Dashboard.appearance}.png",
                    width="260px",
                    height="260px",
                    border_radius=Dashboard.smoothness,
                ),

                rx.text("Widget placeholder")
            ),
            rx.box(
                rx.text(desc),
                rx.flex(
                    rx.button(rx.text("Add to dashboard", color=Dashboard.colors["text"]), border_radius=Dashboard.smoothness, width="100%", background_color=Dashboard.colors["buttons"], on_click=Dashboard.add_widget(name)),
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
        on_mouse_enter=Dashboard.set_widget_store_name(name),
        on_mouse_leave=Dashboard.set_widget_store_name(value=""),
        border_radius=Dashboard.smoothness,
        color=Dashboard.colors["text"]
    )

def render_widget(item: dict):
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
        )
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