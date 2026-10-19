import reflex as rx
import random
from ..components.state import DashboardState
# Format : card.cards.append({"id": "1", "type ":"Crypto", "name": "", "data" : [{"price": 100},{"price": 150},{"price": 200},{"price": 250}]})
def CryptoCard(card) -> rx.Component:
    return rx.card(
        rx.box(
            rx.recharts.area_chart(
                rx.el.svg.defs(
                    rx.el.svg.linear_gradient(
                        rx.el.svg.stop(
                            offset="0%", stop_color="#EB5E28", stop_opacity=1
                        ),
                        rx.el.svg.stop(
                            offset="100%", stop_color="#EB5E28", stop_opacity=0.1
                        ),
                        id="area_gradient",x1=0,x2=0,y1=0,y2=1,
                    ),
                ),
                rx.recharts.area(
                    data_key="price",
                    stroke="#EB5E28",
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
            ),
            
            rx.hstack(
                rx.vstack(
                    rx.heading(card["name"], size="3"), 
                    rx.text(card["data"][-1]["price"]),
                    
                    top="0",  
                    left="0",  
                    z_index="0",
                    spacing="1",
                ),
                rx.spacer(),
                rx.button(rx.icon("refresh_cw", color="#FFFCF2", size=16), variant="ghost", on_click=DashboardState.UpdateCrypto(card["id"])),
                rx.button(rx.icon("trash_2", color="#FFFCF2", size=16), variant="ghost", on_click=DashboardState.DeleteCrypto(card["id"])),
                width="100%",
                position="absolute",
                top="0",
                left="0",
                z_index="10",
            ),

            
            position="relative",
            width="100%",
            height="100%",
        ),
        size="1", 
        width="100%", 
        height="25vh"
    )
