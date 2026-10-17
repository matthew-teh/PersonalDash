import reflex as rx
import random 

class CryptoState(rx.State):
    cards: list[dict] = [
        {"title": "BTC   Bitcoin", 
         "value": "$64,000", 
         "data" : []},
        {"title": "ETH   Ethereum", 
         "value": "$64,000", 
         "data" : []},
        {"title": "SOL   Solana", 
         "value": "$64,000", 
         "data" : []},
    ]

    def update_prices(self):
        for card in self.cards:
            if "Bitcoin" in card["title"]:
                new_prices = [{"price": round(random.uniform(60000, 70000), 2)} for _ in range(25)]
                card["data"] = new_prices
            elif "Ethereum" in card["title"]:
                new_prices = [{"price": round(random.uniform(3000, 4000), 2)} for _ in range(25)]
                card["data"] = new_prices
            elif "Solana" in card["title"]:
                new_prices = [{"price": round(random.uniform(3000, 4000), 2)} for _ in range(25)]
                card["data"] = new_prices

                
def crypto_widgets() -> rx.Component:
    return rx.foreach(
        CryptoState.cards, 
        lambda item: rx.card(
            rx.box(
                rx.recharts.area_chart(
                    rx.el.svg.defs(
                        rx.el.svg.linear_gradient(
                            rx.el.svg.stop(
                                offset="0%", stop_color="#AACCD6", stop_opacity=1
                            ),
                            rx.el.svg.stop(
                                offset="100%", stop_color="#4382DF", stop_opacity=0.1
                            ),
                            id="area_gradient",x1=0,x2=0,y1=0,y2=1,
                        ),
                    ),
                    rx.recharts.area(
                        data_key="price",
                        stroke="#8884d8",
                        fill="url(#area_gradient)",
                    ),
                    rx.recharts.y_axis(
                        domain=["auto", "auto"],  
                        hide=True,
                    ),
                    rx.recharts.graphing_tooltip(),
                    data=item["data"],
                    width="100%",
                    height="100%",
                ),
                rx.vstack(
                    rx.heading(item["title"], size="3"), 
                    rx.text(item["value"]),
                    position="absolute",
                    top="1rem",  
                    left="1rem",  
                    z_index="10",
                ),
                
                position="relative",
                width="100%",
                height="100%",
            ),
            size="2", 
            width="calc(((100vw-1vh)/3)-0.5rem)", 
            height="25vh"
        )
    )