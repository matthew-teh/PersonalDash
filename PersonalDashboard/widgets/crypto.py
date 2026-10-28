
import reflex as rx
from ..components.state import DashboardState   
def crypto_card(card) -> rx.Component:
    return rx.card(
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.image(
                                src=f"/cryptoimages/{(card["name"].lower()).replace('usdt', '')}.png",
                                width="45px",
                            ),
                            height="60px",
                        ),
                        rx.vstack(
                            rx.heading(card["name"], size="3"),
                            rx.text(f'{card["data"][-1]["price"]} USD   {-round(((card["data"][0]["price"] - card["data"][-1]["price"]) / card["data"][0]["price"]) * 100, 2)}%'),
                            spacing="0",
                        ),
                        rx.spacer(),
                        rx.hover_card.root(
                            rx.hover_card.trigger(
                                rx.button(
                                    rx.icon("settings", size=16),
                                    variant="ghost",
                                    pointer_events="auto",
                                ),
                            ),
                            rx.hover_card.content(
                                rx.vstack(
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text("Edit Card", size="3", weight="bold"),
                                            spacing="0",
                                        ),
                                        rx.spacer(),
                                        rx.button(
                                            rx.icon("check"),
                                            variant="ghost",
                                            on_click=DashboardState.save_edit_crypto(card["id"]),
                                            pointer_events="auto",
                                        ),
                                        justify="between",
                                        width="100%",
                                    ),
                                    rx.text("Symbol", size="2"),
                                    rx.input(
                                        value=DashboardState.edit_name_crypto,
                                        on_change=DashboardState.set_name_crypto,
                                        placeholder="eg: BTCUSDT",
                                        width="100%",
                                    ),
                                    rx.cond(
                                        card["name"] != "NaN", 
                                        rx.box(
                                        rx.text("Window", size="2"),
                                            rx.segmented_control.root(
                                            rx.segmented_control.item(rx.text("1m"), value="1m"),
                                            rx.segmented_control.item(rx.text("15m"), value="15m"),
                                            rx.segmented_control.item(rx.text("1H"), value="1h"),
                                            rx.segmented_control.item(rx.text("4H"), value="4h"),
                                            rx.segmented_control.item(rx.text("1D"), value="1d"),
                                            default_value=card["data1"],
                                            on_change=lambda val: DashboardState.save_edit_crypto(card["id"], val)),),
                                        rx.box(),
                                    ),
                                ),
                                side="left",
                                pointer_events="auto",
                            ),
                        ),
                        rx.button(
                            rx.icon("refresh_cw", size=16),
                            variant="ghost",
                            on_click=DashboardState.update_crypto(card["id"]),
                            pointer_events="auto",
                        ),
                        rx.button(
                            rx.icon("trash_2", size=16),
                            variant="ghost",
                            on_click=DashboardState.delete_card(card["id"]),
                            pointer_events="auto",
                        ),
                        width="100%",
                        height="9%",
                    ),
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
                            domain=["auto", "auto"],
                            hide=True,
                        ),
                        rx.recharts.graphing_tooltip(),
                        data=card["data"],
                        width="100%",
                        height="100%",
                        is_animation_active=True,
                        wrapper_style={"backgroundColor": rx.cond(card["data"][-1]["price"] >= card["data"][0]["price"],"#40F698","#F64740",)},
                    ),
                    spacing="0",
                    height="100%",
                    width="100%",
                ),
                width="100%",
                height="100%",
            ),
            width="100%",
            height="100%",
        ),
        size="1",
        width="100%",
        height="30vh",
    )