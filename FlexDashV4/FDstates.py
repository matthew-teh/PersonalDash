import reflex as rx

class Dashboard(rx.State):
    # THEME START
    colors = {
        "text": "#ffffff", 
        "text_alt": "#000000",
        "page_background": "#191919",
        "background": "#0f0f0f",
    }
    # THEME ENDS

    # ---- SIDEBAR START
    page: str = "home"

    @rx.event
    def set_page(self, value, redirect):
        self.page = value.lower()
        if redirect:
            yield rx.redirect(self.page)

    @rx.event
    def init_page(self):
        self.page = self.router.url.path.lower()
    # ---- SIDEBAR ENDS

    # ---- ADD WIDGETS START
    widgets = [
        {"name" : "Crypto", "desc" : "Shows specific crypto coins info."},
        {"name" : "Weather", "desc" : "Shows weather info for specific city."},
        {"name" : "World Clock", "desc" : "Display a clock for specific city time."},
        {"name" : "Tic Tac Toe", "desc" : "A mini game, play with computer."},
        {"name" : "Quick Notes", "desc" : "A blank text box to write anything."},
        {"name" : "Countdown Terra", "desc" : "A countdown for Terra shipment"},
        {"name" : "Quick Links", "desc" : "Coming Soon, at Terra Week 5"},
        {"name" : "To-do List", "desc" : "Coming Soon, at Terra Week 5"},
        {"name" : "Hackatime Info", "desc" : "Coming Soon, at Terra Week 6"},
        {"name" : "Server Info", "desc" : "Coming Soon, at Terra Week 6"},
    ]

    # ---- ADD WIDGETS ENDS
    widget_name = ""

    @rx.event
    def set_widget_name(self, value=""):
        self.widget_name = value