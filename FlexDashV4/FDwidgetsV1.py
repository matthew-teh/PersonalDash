import reflex as rx

from .FDstates import Dashboard

def crypto_widget(widget) -> rx.Component:
    return rx.box(
        rx.hstack(                        
            rx.image(
                src=f"/crypto_icons/{widget["name"].lower().replace("usdt", "")}.png",
                width="42px",
            ),
            rx.vstack(
                rx.heading(widget["name"], size="3"),
                rx.text(f"{widget["data00"][-1]["price"]} USDT, {widget["data03"]}%"),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16),variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Edit Card", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=Dashboard.save_edit_crypto(widget["id"])),
                            width="100%",
                            justify="between",
                        ),
                        rx.text(f"Symbol", size="2"),
                        rx.input(
                            value=Dashboard.widget_name,
                            on_change=Dashboard.edit_widget_name,
                            placeholder="BTCUSDT",
                            width="100%",
                        ),
                        rx.cond(
                            widget["name"] != "NaN",
                            rx.box(
                                rx.text("Window", size="2"),
                                rx.segmented_control.root(
                                    rx.segmented_control.item("1m", value="1m"),
                                    rx.segmented_control.item("15m", value='15m'),
                                    rx.segmented_control.item("1H", value="1h"),
                                    rx.segmented_control.item("4H", value="4h"),
                                    rx.segmented_control.item("1D", value="1d"),
                                    default_value=widget["data01"],
                                    on_change=lambda val: Dashboard.save_edit_crypto(widget["id"], val),
                                ),
                            ),
                            
                            rx.box(),
                        ),
                    ),
                    side="left",
                    width="335px",
                ),
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost", on_click=Dashboard.update_widget(widget["id"])),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=Dashboard.delete_widget(widget["id"])),
            width="100%",
            height="20%",
        ),
        rx.vstack(
            rx.recharts.area_chart(
                rx.recharts.area(
                    data_key="price",
                    stroke=rx.cond(widget["data00"][-1]["price"] >= widget["data00"][0]["price"],"#40F698","#F64740",),
                    fill=rx.cond(
                        widget["data00"][-1]["price"] >= widget["data00"][0]["price"],
                        "rgba(64, 246, 152, 0.25)",  # Transparent Green
                        "rgba(246, 71, 64, 0.25)",   # Transparent Red
                    ),
                ),
                rx.recharts.y_axis(
                    domain=["auto","auto"],
                    hide=True,
                ),
                rx.recharts.graphing_tooltip(),
                data=widget["data00"],
                wrapper_style={"backgroundColor": rx.cond(widget["data00"][-1]["price"] >= widget["data00"][0]["price"],"#40F698","#F64740",)},
                margin={ "top": 0, "right": 0, "bottom": 0, "left": 0 },
            ),
            height="80%",
            width="100%",
            spacing="0"
        ),
        padding="8px",
        overflow="hidden",
        width="100%",
        aspect_ratio=" 1/1",
        style={"background_color": Dashboard.colors["widget_background"]},
        border_radius="8px",
        border = "1px solid rgba(255, 255, 255, 0.2)",
    )