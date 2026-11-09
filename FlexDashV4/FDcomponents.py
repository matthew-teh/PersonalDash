import reflex as rx

from .FDstates import Dashboard

# ---- SIDEBAR START
def sidebar_items(name: str, image: str, link: str, redirect: bool) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.image(src=image),
            rx.text(name, font_size="16px", color=Dashboard.colors["text"]),
            width="100%",
            height="100%",
            align="center",
        ),
        opacity = rx.cond(Dashboard.page == link.lower(), 1 , 0.5),
        _hover={"opacity": 1.0},
        transition="opacity 0.2s ease-in-out",
        width="100%",
        variant="ghost",
        border_radius="8px",
        height="32px",
        on_click= Dashboard.set_page(link, redirect),
    )

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.image(src="/logo.svg", border_radius="4px", width="19%", height="auto"),
                rx.vstack(
                    rx.text("FlexDash V4", weight="bold", font_size="24px"),
                    rx.text("Developer", font_size="16px", opacity=0.5),
                    spacing="0",    
                    width="100%",
                ),
                align_items="center",
            ),  
            rx.separator(),
            rx.vstack(
                sidebar_items("Dashboard", "/lucide_icons/house_dark.svg", "/", True),
                sidebar_items("Add widgets", "/lucide_icons/shopping_bag_dark.svg", "/widgets", True),
                rx.separator(),
                sidebar_items("Refresh all", "/lucide_icons/refresh_cw_dark.svg", "", False),
                sidebar_items("Delete all", "/lucide_icons/trash_dark.svg", "", False),
                rx.separator(),
                rx.spacer(),
                rx.separator(),
                sidebar_items("Account", "/lucide_icons/user_round_dark.svg", "/account", True),
                sidebar_items("Settings", "/lucide_icons/settings_dark.svg", "/settings", True),
                width="100%",
                height="100%",
            ),
            height="100%",
            align="center"
        ),
        width="15%",
        height="100%",
        padding="8px",
        border_radius="8px",
    )
# ---- SIDEBAR ENDS

# ---- WIDGETS STARTS
def widget(name: str, image: str, desc: str):
    is_active = Dashboard.widget_name == name
    return rx.card(
        rx.vstack(
            rx.text(name, weight="bold"),
            rx.text("card placeholder"),
            rx.box(
                rx.text(desc),
                rx.flex(
                    rx.button(rx.text("Add to dashboard", color=Dashboard.colors["text_alt"]), border_radius="8px", width="100%", background_color="#EEEEEE"),
                    width="100%",
                    opacity=rx.cond(is_active, 1, 0),
                    transition="all 0.3s ease-in-out",
                    overflow="hidden",
                    max_height=rx.cond(is_active, "60px", "0px",),
                ),
                padding="0px",
                width="100%",
            ),
            width="100%",
            aspect_ratio="1 / 1",
            align = "center",
            justify="between",
        ),
        on_mouse_enter=Dashboard.set_widget_name(name),
        on_mouse_leave=Dashboard.set_widget_name(value=""),
        border_radius="8px",
    )
# ---- WIDGETS ENDS