import reflex as rx
import uuid 
import json
from typing import TypedDict

from .FDapi import get_price

class widgetData(TypedDict):
    id: str 
    name: str
    type: str
    data00: list[dict[str, str]]
    data01: str
    data02: str
    data03: float

class widgetStore(TypedDict):
    name: str
    desc: str
    available: bool
    designed_name: str
    designed_type: str
    designed_data00: list[dict[str, str]]
    designed_data01: str
    designed_data02: str
    designed_data03: float



def load_widget_store():
    try:
        with open("FlexDashV4/FDwidgets.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return []
        
class Dashboard(rx.State):
    # ---- THEME START
    colors = {
        "text": "#ffffff", 
        "text_alt": "#000000",
        "widget_background": "#1b1b1b",
        "page_background": "#151515",
        "background": "#0f0f0f",
    }
    
    #---- CLOUD STATUS ( REDIS SERVER )
    sync_status = "Last sync 23:52:20"


    # ---- SIDEBAR START
    page: str = "home"

    @rx.event
    def set_page(self, value: str, redirect: bool):
        if redirect:
            self.page = value.lower()
            yield rx.redirect(self.page)

    @rx.event
    def init_page(self):
        self.page = self.router.url.path.lower()
    # ---- SIDEBAR ENDS

    # ---- WIDGETS MANAGEMENT START 
    widgets: list[widgetData]= []
    widget_store_name = ""
    widgets_store: list[widgetStore]= load_widget_store()
    
    @rx.event
    def set_widget_store_name(self, value=""):
        self.widget_store_name = value

    @rx.event
    def add_widget(self, name):
        for widget in self.widgets_store:
            if name == widget["name"]:
                if widget["available"]:
                    widget_id = str(uuid.uuid4())
                    self.widgets.append({
                        "id": widget_id,
                        "name": widget["designed_name"],
                        "type": widget["designed_type"],
                        "data00": widget["designed_data00"],
                        "data01": widget["designed_data01"],
                        "data02": widget["designed_data02"],
                        "data03": widget["designed_data03"],
                    })
                    print(self.widgets)
                    yield type(self).update_widget(widget_id)
                    yield rx.toast.success(f"New widget added: {name}")
                else:
                    yield rx.toast.warning(f"This card is coming soon.")

    # ---- All widget management.
    @rx.event
    def update_widget(self, widget_id):
        for widget in self.widgets:
            if widget["id"] == widget_id:

                if widget["type"].lower() == "crypto_v1":
                    widget["data00"] = get_price(
                        symbol=widget["name"],
                        window=widget["data01"]
                    )
                    yield type(self).crypto_percentage(widget_id)
                if widget["type"].lower() == "crypto_v2":
                    widget["data00"] = get_price(
                        symbol=widget["data01"],
                        window=widget["data02"]
                    )
                    yield type(self).crypto_percentage(widget_id)
    @rx.event
    def update_all_widget(self):
        for widget in self.widgets:
            yield type(self).update_widget(widget["id"])
        print(self.widgets)

    @rx.event
    def delete_widget(self, widget_id):
        for widget in self.widgets:
            if widget["id"] == widget_id:
                self.widgets.remove(widget)

    @rx.event
    def delete_all_widget(self):
        self.widgets = []

    # ---- CRYPTO WIDGET V1 and V2
    widget_name: str = ""
    @rx.event
    def edit_widget_name(self, value: str):
        self.widget_name = value
    
    @rx.event
    def save_edit_crypto(self, widget_id: str, val={}):
        for widget in self.widgets:
            if widget["id"] == widget_id:
                if not isinstance(val, dict):
                    widget["data01"] = val
                    print("Updated")
                elif self.widget_name:
                    widget["name"] = self.widget_name
                    
                else:
                    yield rx.toast("Nothing updated.")

    @rx.event
    def crypto_percentage(self, widget_id):
        for widget in self.widgets:
            if widget["id"] == widget_id:
                value = -round(((float(widget["data00"][0]["price"]) - float(widget["data00"][-1]["price"])) / float(widget["data00"][0]["price"])) * 100, 2)
                widget["data03"] = value