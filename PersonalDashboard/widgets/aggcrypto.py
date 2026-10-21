
import reflex as rx
from ..components.state import DashboardState


def AggCryptoCard(card) -> rx.Component:
    return rx.card(
        rx.box(
            rx.recharts.area_chart(
                rx.el.svg.defs(
                    rx.el.svg.linear_gradient(
                        rx.el.svg.stop(
                            offset="0%", stop_color="#F64740", stop_opacity=0.9
                        ),
                        rx.el.svg.stop(
                            offset="100%", stop_color="#F64740", stop_opacity=0.2
                        ),
                        id="area_gradient", x1=0, x2=0, y1=0, y2=1,
                    ),
                ),
                rx.recharts.area(
                    data_key="price",
                    stroke="#F64740",
                    fill="url(#area_gradient)",
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
                wrapper_style={"backgroundColor": "#F64740"},
            ),

            rx.hstack(
                rx.vstack(
                    rx.heading(card["name"], size="3"),
                    rx.text(f'{card["data"][-1]["price"]} USD   {round(((card["data"][-1]["price"]-card["data"][0]["price"])/card["data"][-1]["price"])*100, 2)}%'),
                    rx.spacer(),
                    rx.text(f"Live market data", size="1",pointer_events="none",),
                    rx.text("Crypto data provided by Binance WebSocket", size="1",pointer_events="none",),
                    spacing="0",
                    height="100%",
                    width="100%",
                    align="start",
                    pointer_events="none",
                ),
                rx.spacer(),
                rx.hover_card.root(
                    rx.hover_card.trigger(
                        rx.button(
                            rx.icon("settings", color="#E8E9ED", size=16),
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
                                    rx.icon("check", color="#E8E9ED"),
                                    variant="ghost",
                                    on_click=DashboardState.SaveEdit(card["id"]),
                                    pointer_events="auto",
                                ),
                                justify="between",
                                width="100%",
                            ),
                            rx.text("Symbol", size="2"),
                            rx.input(
                                value=DashboardState.EditName,
                                on_change=DashboardState.SetEditName,
                                placeholder="eg: BTCUSDT",
                                width="100%",
                            ),
                        ),
                        background_color="#1E221D",
                        pointer_events="auto",
                    ),
                ),
                rx.button(
                    rx.icon("trash_2", color="#E8E9ED", size=16),
                    variant="ghost",
                    on_click=DashboardState.DeleteCrypto(card["id"]),
                    pointer_events="auto",
                ),
                width="100%",
                height="100%",
                position="absolute",
                top="0",
                left="0",
                z_index="10",
                pointer_events="none",
            ),

            position="relative",
            width="100%",
            height="100%",
        ),
        size="1",
        width="100%",
        height="30vh",
        background_color="#1E221D",
    )
