import reflex as rx

from .FDstates import Dashboard
from . import FDcomponents

def crypto_widget(widget) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src=f"/crypto_icons/{widget["data01"].replace("USDT", "").lower()}.png",
                        alt="",
                        width="28px"
                    ),
                    rx.heading(f"{widget["name"].split(" ")[0]}", font_size="20px"),
                    rx.text(f"{widget["name"].split(" ")[1]}", font_size="12px", opacity=0.6),
                    rx.spacer(),
                    rx.hover_card.root(
                        rx.hover_card.trigger(
                            rx.icon("pencil-line", size=16, color=Dashboard.colors["text"],opacity=0.5,
                            background_color="transparent",
                            padding="0",
                            cursor="pointer",
                            _hover={"opacity": 1}),
                        ),
                        rx.hover_card.content(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("EDIT WIDGET", weight="bold", font_size="16px"),
                                    rx.button(rx.text("SAVE", color=Dashboard.colors["text"]), background_color=Dashboard.colors["buttons"], opacity=0.6, _hover={"opacity": 1.0}, on_click=Dashboard.apply_any(widget["id"])),
                                    justify="between",
                                    align="center",
                                    width="100%"
                                ),
                                rx.vstack(
                                    rx.text("Widget Name: "),
                                    rx.input(
                                        value=Dashboard.temp_name,
                                        placeholder=widget["name"],
                                        on_change= lambda val : Dashboard.edit_any(val, "name")
                                    ),
                                    rx.text("Cryptocurrency: "),
                                    rx.input(
                                        value=Dashboard.temp_data01,
                                        placeholder=widget["data01"],
                                        on_change= lambda val : Dashboard.edit_any(val, "01")
                                    ),
                                    
                                ),
                                
                                width="100%",
                            ),
                            
                            on_mouse_leave=Dashboard.clear_any
                        ),

                        direction="right",
                    ),
                    rx.icon("rotate-cw", size=16, color=Dashboard.colors["text"], opacity=0.5, _hover={"opacity": 1.0}, on_click=lambda: Dashboard.update_widget(widget["id"])),
                    rx.icon("trash", size=16, color=Dashboard.colors["text"], opacity=0.5, _hover={"opacity": 1.0}, on_click=lambda: Dashboard.delete_widget(widget["id"])),
                    height="32px",
                    spacing="2",
                    align="center",
                    padding_bottom="2px",
                    width="100%",
                ),
                rx.text(f"Current price, interval {widget["data02"]}", font_size="12px", opacity=0.6),
                rx.hstack(
                    rx.heading(
                        f"${widget["data00"][-1]["price"]}", 
                        font_size="36px", 
                        color=rx.cond(widget["data00"][-1]["price"] >= widget["data00"][0]["price"],"#40F698","#F64740",),
                    ),
                    rx.image(src=rx.cond(widget["data03"] > 0, "/matthew_icons/arrow_up.svg", "/matthew_icons/arrow_down.svg"), height="42px", width="42px  "),
                    rx.heading(f"{widget["data03"]}%", font_size="18px", color=rx.cond(widget["data00"][-1]["price"] >= widget["data00"][0]["price"],"#40F698","#F64740",)),
                    spacing="1",
                    align="center",
                ),
                padding="8px",
                spacing="0",
                width="100%",
            ),
            rx.recharts.area_chart(
                rx.el.svg.defs(
                    rx.el.svg.linear_gradient(
                        rx.el.svg.stop(
                            offset="5%", stop_color=rx.cond(widget["data00"][-1]["price"] >= widget["data00"][0]["price"],"#40F698","#F64740",), stop_opacity=0.8,
                        ),
                        rx.el.svg.stop(
                            offset="95%", stop_color=rx.cond(widget["data00"][-1]["price"] >= widget["data00"][0]["price"],"#40F698","#F64740",), stop_opacity=0.2,
                        ),
                    id="area_gradient",
                    x1=0,
                    x2=0,
                    y1=0,
                    y2=1,
                    ),
                ),
                rx.recharts.area(
                    data_key="price",
                    stroke=rx.cond(widget["data00"][-1]["price"] >= widget["data00"][0]["price"],"#40F698","#F64740",),
                    fill="url(#area_gradient)",
                    type_="natural",
                ),
                rx.recharts.y_axis(domain=["auto","auto"], hide=True),
                rx.recharts.graphing_tooltip(),
                data=widget["data00"],
                wrapper_style={"backgroundColor": rx.cond(widget["data00"][-1]["price"] >= widget["data00"][0]["price"],"#40F698","#F64740",)},
                margin={ "top": 10, "right": 0, "bottom": 0, "left": 0 },
                height="100%"
            ),
            spacing="0",
            width="100%",
            height="100%",
        ),  
        overflow="hidden",
        width="100%",
        aspect_ratio=" 1/1",
        style={"background_color": Dashboard.colors["widget"]},
        border_radius=Dashboard.smoothness,
        
    )   

def render_tasks(item):
    return rx.box(
        rx.hstack(
            rx.text(item["tasks"], text_decoration=rx.cond(item["status"] == "completed", "line-through", "")),
            rx.spacer(),
            rx.icon(rx.cond(item["status"]=='completed', 'x', 'check'), size=16, opacity=0.5, _hover={"opacity": 1}, on_click=lambda: Dashboard.mark_tasks(item["uid"], item["wid"])),
            rx.icon('trash', size=16, opacity=0.5, _hover={"opacity": 1}, on_click=lambda :Dashboard.delete_tasks(item["uid"], item["wid"])),
            align="center",
            width="100%",
            opacity=0.5,
            _hover={"opacity": 1},
            transition="all ease-in-out 0.2s"
        ),
        padding = "8px",
        border_radius=Dashboard.smoothness,
        margin="2px",
        width="calc(100%-2px)",
        background_color = Dashboard.colors["buttons"],
    )

def checklist_widget(widget) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.image(src=f"/lucide_icons/list_checks_{Dashboard.appearance}.svg", width="30px"),
                rx.text("CHECKLIST", weight="bold", font_size="20px"),
                rx.spacer(),
                rx.icon('trash', size=16, color=Dashboard.colors["text"], opacity=0.5, _hover={"opacity": 1.0}, on_click=lambda:Dashboard.delete_widget(widget["id"])),
                align="center",
                width="100%",
                height="32px",
            ),
    
            rx.hstack(
                rx.input(
                    placeholder='Add tasks', 
                    width="90%", 
                    value=Dashboard.temp_data01, 
                    on_change=lambda val: Dashboard.edit_any(val, "01"), 
                    on_key_down= lambda key: rx.cond(
                        key == "Enter",
                        Dashboard.add_tasks(widget["id"]),
                        None,
                    ),
                    on_blur=Dashboard.clear_any
                ),
                rx.icon('plus', opacity=0.5, _hover={"opacity": 1}, on_click=Dashboard.add_tasks(widget["id"])),
                align="center",
                width="100%",
            ),
            rx.scroll_area(
                rx.foreach(
                    widget["data00"], 
                    lambda item: render_tasks(item)
                ),
                min_height="0",
                flex="1",
            ),
            height="100%",
        ),
        padding="8px",
        overflow="hidden",
        width="100%",
        aspect_ratio="1/1",
        background_color= Dashboard.colors["widget"],
        border_radius=Dashboard.smoothness
    )


def terracd_widget(widget) -> rx.Component:
    size = 150
    time = widget["data00"][0]["diff"].split("|")
    return rx.box(
        rx.hstack(
            rx.image(src=f"/lucide_icons/clock_fading_{Dashboard.appearance}.svg", width="30px"),
            rx.text("TERRA COUNTDOWN", weight="bold", font_size="20px"),
            rx.spacer(),
            rx.icon("rotate-cw", size=16, color=Dashboard.colors["text"], opacity=0.5, _hover={"opacity": 1}, on_click=Dashboard.update_widget(widget["id"])),
            rx.icon('trash', size=16, color=Dashboard.colors["text"], opacity=0.5, _hover={"opacity": 1}, on_click=Dashboard.delete_widget(widget["id"])),
            spacing="2",
            align="center",
            width="100%",
            height="32px",
        ),
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.vstack(FDcomponents.circle_progress(time[0].to(float)/6, size, time[0]), rx.text("Days"), align="center", spacing="0"),
                    rx.vstack(FDcomponents.circle_progress(time[1].to(float)/24, size, time[1]), rx.text("Hours"), align="center", spacing="0"),
                    width="100%"
                ),
                rx.hstack(
                    rx.vstack(FDcomponents.circle_progress(time[2].to(float)/60, size, time[2]), rx.text("Minutes"), align="center", spacing="0"),
                    rx.vstack(FDcomponents.circle_progress(time[3].to(float)/60, size, time[3]), rx.text("Seconds"), align="center", spacing="0"),
                    width="100%"
                ),
                justify_content="center",
                align_items="center"
            ),
            flex="1",
            min_height = 0,
        ),
        display="flex",
        flex_direction="column",
        padding="8px",
        overflow="hidden",
        width="100%",
        aspect_ratio="1/1",
        background_color=Dashboard.colors["widget"],
        border_radius=Dashboard.smoothness
    )