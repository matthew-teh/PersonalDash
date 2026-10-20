import reflex as rx 
import random
from . import components

def index():
    return rx.vstack(
        components.header.navbar(),
        components.renderwidget.render_all_widgets(),
        rx.spacer(),
        components.footer.footer(),
        justify="between", 
        min_height="100vh", 
        width="100%",
        spacing="0",
        color="#FFFCF2",      
        background_color="#090C08", 
    ), 

app = rx.App(
    head_components=[
        rx.el.link(rel="stylesheet", href="/styles.css"),
    ]
)
app.add_page(
    index, 
)