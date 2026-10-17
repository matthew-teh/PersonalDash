from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.layout import Layout  
from rich import box, print
from api import *
from datetime import datetime

BORDER_COLOR = "#bd43ff"
BG_RGB = "#111111"  
STYLE = f"white on {BG_RGB}" 

layout = Layout()
console = Console()

layout.split_column(
    Layout(name="header", size=3),
    Layout(name="main", ratio=1),
    Layout(name="footer", size=3)
)
# making 2x2 grid
layout["main"].split_row(
    Layout(name="left"),
    Layout(name="right")
)
layout["left"].split_column(
    Layout(name="weather", ratio=1),
    Layout(name="todo", ratio=1)
)

layout["right"].split_column(
    Layout(name="crypto", ratio=1),
    Layout(name="system", ratio=1)
)


# head and foot setting
layout["header"].update(
    Panel("PersonalDash v1.0", style=STYLE, border_style=BORDER_COLOR, box=box.ROUNDED)
)
layout["footer"].update(
    Panel(f"Status: [bold green]Online[/ bold green], Last update: {datetime.now().strftime("%H:%M:%S")}, Press CTRL+C to exit", style=STYLE, border_style=BORDER_COLOR, box=box.ROUNDED)
)
# main
layout["weather"].update(
    Panel(market(), title="Weather", style=STYLE, border_style=BORDER_COLOR, box=box.ROUNDED)
)
layout["todo"].update(
    Panel(todo(), title="To-do", style=STYLE, border_style=BORDER_COLOR, box=box.ROUNDED)
)
layout["crypto"].update(
    Panel(crypto(), title="Crypto", style=STYLE, border_style=BORDER_COLOR, box=box.ROUNDED)
)
layout["system"].update(
    Panel(system(), title="System", style=STYLE, border_style=BORDER_COLOR, box=box.ROUNDED)
)

console.print(layout)