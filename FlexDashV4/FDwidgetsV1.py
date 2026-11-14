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
                            rx.heading("Edit widget", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=Dashboard.save_edit_widget(widget["id"])),
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
                                    on_change=lambda val: Dashboard.save_edit_widget(widget["id"], val),
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
        style={"background_color": Dashboard.colors["widget"]},
        border_radius=Dashboard.smoothness,
    )

def weather_widget(widget) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(
                src=f"/{widget["data00"][0]["useimg"]}",
                alt=widget["data00"][0]["useimg"],
                height= "42px",
            ),
            rx.vstack(
                rx.heading(widget["name"], size="3"),
                rx.text(widget["data00"][0]["wetcode"]),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16), variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Edit widget", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=Dashboard.save_edit_widget(widget["id"])),
                            width="100%",
                            justify="between",
                        ),
                        rx.text(f"City: {widget["data01"]}", size="2"),
                        rx.input(
                            value=Dashboard.widget_name,
                            on_change=lambda val, cid=widget["id"]: Dashboard.edit_widget_name(val, cid),
                            placeholder="New York",
                        ),
                    ),
                    side="left",
                    width="250px",
                ),
                
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost", on_click=Dashboard.update_widget(widget["id"])),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=Dashboard.delete_widget(widget["id"])),
            width="100%",
            height="20%",
        ),
        rx.hstack(
            rx.hstack(
                rx.text(f"{widget["data00"][0]["temp"]}", font_size="120px", weight="bold"),
                rx.text("℃"),
                width="50%",
                height='100%',
                align="center",
                justify="center",
            ),
            rx.grid(
                rx.card(
                    rx.flex(rx.text("Feels Like", font_size="14px"), align_items="center", justify_content="center", width="100%", height="15%"),
                    rx.flex(
                        rx.text(f"{widget["data00"][0]["feeltemp"]}", font_size="42px", weight="bold"), 
                        rx.text("℃", font_size="14px"),
                        align_items="center", justify_content="center", width="100%", height="85%"),
                    height="100%"
                ),
                rx.card(
                    rx.flex(rx.text("Humidity", font_size="14px"), align_items="center", justify_content="center", width="100%", height="15%"),
                    rx.flex(rx.text(f"{widget["data00"][0]["relative_humid"]}", font_size="42px", weight="bold"), 
                            rx.text("%", font_size="14"), 
                            align_items="center", justify_content="center", width="100%", height="85%"),
                    height="100%"
                ),
                rx.card(
                    rx.flex(rx.text("Wind speed", font_size="14px"), align_items="center", justify_content="center", width="100%", height="15%"),
                    rx.flex(rx.text(f"{widget["data00"][0]["windspd"]}", font_size="42px", weight="bold"), 
                            rx.text("km/h", font_size="14px"), 
                            align_items="center", justify_content="center", width="100%", height="85%"),
                    height="100%"
                ),
                rx.card(
                    rx.flex(rx.text("Cloud Cover", font_size="14px"), align_items="center", justify_content="center", width="100%", height="15%"),
                    rx.flex(rx.text(f"{widget["data00"][0]["cloudcvr"]}", font_size="42px", weight="bold"), 
                            rx.text("%", font_size="14px"), 
                            align_items="center", justify_content="center", width="100%", height="85%"),
                    height="100%"
                ),
                columns="2",
                width="50%",
                height="100%",
                gap="0.25rem",
            ),
            width="100%",
            height="80%",
            spacing="0",
        ),
        padding="8px",
        overflow="hidden",
        width="100%",
        aspect_ratio=" 1/1",
        style={"background_color": Dashboard.colors["widget"]},
        border_radius=Dashboard.smoothness,
    )

def worldclock_widget(widget) -> rx.Component:
    return rx.box(
        rx.hstack(            
            rx.image(
                src= "/matthew_icons/earth.png",
                alt= "worldclockimages",
                width= "42px",
            ),
            rx.vstack(
                rx.heading(widget["name"], size="3"),
                rx.text(widget["data00"][0]["timezone"]),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16), variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Edit Card", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=Dashboard.save_edit_widget(widget["id"])),
                            width="100%",
                            justify="between"
                        ),
                        rx.text(f"City: {widget["data01"]}", size="2"),
                        rx.input(
                            value=Dashboard.widget_name,
                            on_change=lambda value, cid=widget["id"]: Dashboard.edit_widget_name(value, cid),
                            placeholder = "Paris"
                        ), 
                    ),
                    side="left",
                ),
            ),
            rx.button(rx.icon("refresh_cw", size=16), variant="ghost", hidden=True),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=Dashboard.delete_widget(widget['id'])),
            
            width="100%",
            height="20%"
        ),
        rx.vstack(
            rx.box(rx.text(widget["data00"][0]["time"], font_size="68px", weight="bold"),
                   display="flex",
                   align_items="center",
                   justify_content="center",
                   height="50%",
                   width="100%"),
            rx.vstack(
                rx.card(rx.center(f"Universal Time Coordinates: {widget["data00"][0]["tz"]}", width="100%", height="100%"), width="100%", height="50%"),
                rx.hstack(
                    rx.card(rx.center(f"{widget["data00"][0]["date"]} {widget["data00"][0]["time"]}", width="100%", height="100%"), width="50%", display="flex", height="100%", padding="0", padding_left="12px"),
                    rx.card(rx.center(f"DST: {widget["data00"][0]["dst"]}", width="100%", height="100%"), width="50%", height="100%", display="flex", padding="0", padding_left="12px"),
                    height='50%',
                    width='100%',
                    spacing="1", 
                ),
                spacing="1",   
                width="100%",
                height="50%",
                flex="1",
            ),
            spacing="1",
            width="100%",
            height="80%"
        ),
        padding="8px",
        overflow="hidden",
        width="100%",
        aspect_ratio=" 1/1",
        style={"background_color": Dashboard.colors["widget"]},
        border_radius=Dashboard.smoothness,
    )

def pomodoro_widget(widget) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("apple", height="42px", width="42px", color='red'),
            rx.vstack(
                rx.heading(widget["name"], size="3"),
                rx.match(
                    widget["data00"][0]["mode"],
                    ("pomodoro", rx.text("Pomodoro - Focus Mode")),
                    ("short", rx.text("Short Break - Take a sip of coffee")),
                    ("long", rx.text("Long Break - Get a snack")),
                ),
                spacing="0",
            ),
            rx.spacer(),
            rx.hover_card.root(
                rx.hover_card.trigger(rx.button(rx.icon("settings", size=16), variant="ghost")),
                rx.hover_card.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Edit Card", size="3"),
                            rx.button(rx.icon("check"), variant="ghost", on_click=Dashboard.save_edit_pomodoro(widget["id"])),
                            width="100%",   
                            justify="between",
                        ),
                        
                        rx.text("Pomodoro Time (minutes)"),
                        rx.input(
                            value=Dashboard.pomodoro,
                            on_change=Dashboard.edit_pomodoro,
                            placeholder="25",
                            width="100%",
                        ),
                        rx.text("Short and long breaks"),
                        rx.hstack(
                            rx.input(
                                value=Dashboard.short,
                                on_change=Dashboard.edit_short,
                                width="50%",
                                placeholder="5",
                            ),
                            rx.input(
                                value=Dashboard.long,
                                on_change=Dashboard.edit_long,
                                width="50%",
                                placeholder="15"
                            ),
                            width="100%", 
                        ),
                    ),
                    side="left",
                    width="250px",
                )
            ),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=Dashboard.delete_widget(widget["id"])),
            width="100%",
            height="20%",
        ),
        rx.vstack(
            rx.text(widget["data00"][0]["timing"], font_size="132px", weight="bold"),
            rx.hstack(
                rx.button(rx.icon("play"), variant="ghost", on_click=Dashboard.command_pomodoro(widget["id"], "start")),
                rx.button(rx.icon("pause"), variant="ghost", on_click=Dashboard.command_pomodoro(widget["id"], "stop")),
                rx.button(rx.icon("timer-reset"), variant="ghost", on_click=Dashboard.command_pomodoro(widget["id"], "reset")),
                spacing="5",
            ),
            align_items="center",
            justify="center",
            width="100%",
            height="80%",
            spacing="0",
        ),
        padding="8px",
        overflow="hidden",
        width="100%",
        aspect_ratio=" 1/1",
        style={"background_color": Dashboard.colors["widget"]},
        border_radius=Dashboard.smoothness,
    )

def quicknotes_widget(widget) -> rx.Component:
    return rx.box(
        rx.hstack(
            
            rx.cond(
                Dashboard.appearance == "dark",
                rx.image(src="/lucide_icons/book_dark.svg", height="42px", width="42px"),
                rx.image(src="/lucide_icons/book_light.svg", height="42px", width="42px")
            ),
            rx.vstack(
                rx.heading(widget["name"], size="3"),
                rx.text("A text area to note, auto saved.   "),
                spacing="0",
            ),
            rx.spacer(),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=Dashboard.delete_widget(widget["id"])),
            width="100%",
            height="20%",
        ),
        rx.hstack(
            rx.text_area(
                placeholder="Start typing here...",
                value=widget["data00"][0]["text"],
                on_change=lambda val: Dashboard.save_notes(widget["id"], val),
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
        width="100%",
        aspect_ratio=" 1/1",
        style={"background_color": Dashboard.colors["widget"]},
        border_radius=Dashboard.smoothness,
    )

def terracd_widget(widget) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.cond(
                Dashboard.appearance == "dark",
                rx.image(src="/lucide_icons/clock_fading_dark.svg", height="42px", width="42px"),
                rx.image(src="/lucide_icons/clock_fading_light.svg", height="42px", width="42px")
        ),
        rx.vstack(
            rx.heading(widget["name"], size="3"),
            rx.text("This week of terra ends in: "),
            spacing="0",
        ),
        rx.spacer(),
        rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=Dashboard.delete_widget(widget["id"])),
        width="100%",
        height="20%",
        ),
        rx.vstack(
            rx.center(
                rx.text(widget["data00"][0]["time"], font_size="100px", weight="bold"),
                height="100%",
                width="100%",
            ),
            rx.center(
                rx.hstack(
                    rx.text("Hours"),
                    rx.text("Minutes"),
                    rx.text("Seconds"),
                    width="80%",
                    justify="between",
                ),
                height="100%",
                width="100%"
            ),
            width="100%",
            height="80%",
            spacing="0",
        ),
        padding="8px",
        overflow="hidden",
        width="100%",
        aspect_ratio=" 1/1",
        style={"background_color": Dashboard.colors["widget"]},
        border_radius=Dashboard.smoothness,
    )