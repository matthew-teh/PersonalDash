import reflex as rx
from ..components.state import DashboardState

def tic_tac_toe_card(card) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.color_mode_cond(
                light=rx.image(src="tictactoeimages/tic-tac-toe-light.svg", height="42px", width="42px"),
                dark=rx.image(src="tictactoeimages/tic-tac-toe-dark.svg", height="42px", width="42px")
            ),
            rx.vstack(
                rx.heading(card["name"], size="3"),
                rx.text("Terra theme week 2 edition"),
                spacing="0",
            ),
            rx.spacer(),
            rx.button(rx.icon("trash_2", size=16), variant="ghost", on_click=DashboardState.delete_card(card["id"])),
            width="100%",
            height="53.8px",
        ),
        rx.hstack(
            rx.flex(
                rx.card(
                    rx.box(
                        rx.vstack(
                            rx.text("You"),
                            rx.hstack(
                                rx.icon("circle", size=48),
                                rx.spacer(),
                                rx.text(card["data3"][0], font_size="48px"),
                                height="100%", width="100%", align_items="center",
                            ),
                            spacing="0",
                            height="100%",
                            width="100%",
                        ),
                        width="100%", height="50%", border_radius="4px", padding="2px",),
                    rx.box(
                        rx.vstack(
                            rx.text("Computer"),
                            rx.hstack(
                                rx.icon("x", size=50), 
                                rx.spacer(),
                                rx.text(card["data3"][1], font_size="48px"),
                                height="100%", width="100%", align_items="center"
                            ),
                            
                            spacing="0",
                            height="100%",
                            width="100%",
                        ),
                        width="100%", height="50%", border_radius="4px", padding="2px"),
                    width="100%",
                    height="196px",
                    padding="8px",
                ),
                justify = "center",
                align_items = "center",
                width="60%",
                paddin= "0px",
                padding_right="8px",
            ),
            rx.flex(
                rx.grid(
                    rx.foreach(
                        card["data"],
                        lambda item:rx.card(
                            rx.center(
                                rx.match(
                                    item["data"],
                                    ("0", rx.text("")),
                                    ("X", rx.icon("x", size=40)),
                                    ("O", rx.icon("circle", size=45)),
                                ),
                                height="100%",
                                width="100%",
                            ), width="60px", height="60px", border_radius="8px", padding="0px",
                            _hover=rx.cond(
                                card["data2"] == 0, 
                                {"backgroundColor" : "#454143"},
                                {}
                            ),
                            on_click=DashboardState.register_click(card["id"], item["id"])
                            ),
                    ),
                    gap="8px",
                    columns="3",
                    width="fit-content",
                    height="fit-content",
                    padding="0px",
                ),
                justify="end",
                align = "center",
                padding="0px",
            ),
            width="100%",
            height="215.2px",
            align_items="end",
            spacing="0",
            padding="0px",
        ),
        padding="8px",
        width="100%",
        height="285px"
    )