import reflex as rx
from ..components.state import DashboardState

def crypto_card(card) -> rx.Component:
    return rx.card(
        rx.hstack(                        
            rx.image(
                src=f"/cryptoimages/{(card["name"].lower().replace('usdt', ''))}.png",
                width="42px",
            ),
            rx.vstack(
                rx.heading(card["name"], size="3"),
                rx.text(f"{card["data"][-1]["price"]} USDT, {card["data2"]}%"),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16),variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Edit Card", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=DashboardState.save_edit_crypto(card["id"])),
                            width="100%",
                            justify="between",
                        ),
                        rx.text(f"Symbol", size="2"),
                        rx.input(
                            value=DashboardState.edit_name_crypto,
                            on_change=DashboardState.set_name_crypto,
                            placeholder="BTCUSDT",
                        ),
                        rx.cond(
                            card["name"] != "NaN",
                            rx.box(
                                rx.text("Window", size="2"),
                                rx.segmented_control.root(
                                    rx.segmented_control.item("1m", value="1m"),
                                    rx.segmented_control.item("15m", value='15m'),
                                    rx.segmented_control.item("1H", value="1h"),
                                    rx.segmented_control.item("4H", value="4h"),
                                    rx.segmented_control.item("1D", value="1d"),
                                    default_value=card["data1"],
                                    on_change=lambda val: DashboardState.save_edit_crypto(card["id"], val),
                                ),
                                rx.box(),
                            ),
                        ),
                    ),
                    side="left",
                ),
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost", on_click=DashboardState.update_crypto(card["id"])),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card["id"])),
            width="100%",
            height="20%",
        ),
        rx.vstack(
            rx.recharts.area_chart(
                rx.recharts.area(
                    data_key="price",
                    stroke=rx.cond(card["data"][-1]["price"] >= card["data"][0]["price"],"#40F698","#F64740",),
                    fill=rx.cond(
                        card["data"][-1]["price"] >= card["data"][0]["price"],
                        "rgba(64, 246, 152, 0.25)",  # Transparent Green
                        "rgba(246, 71, 64, 0.25)",   # Transparent Red
                    ),
                ),
                rx.recharts.y_axis(
                    domain=["auto","auto"],
                    hide=True,
                ),
                rx.recharts.graphing_tooltip(),
                data=card["data"],
                wrapper_style={"backgroundColor": rx.cond(card["data"][-1]["price"] >= card["data"][0]["price"],"#40F698","#F64740",)},
            ),
            height="80%",
            width="100%",
            spacing="0"
        ),
        padding="0.8rem",
        width="100%",
        height="285px"
    )