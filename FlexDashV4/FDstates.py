import reflex as rx
import uuid 
import json
import copy
import psutil
from typing import TypedDict

from .FDapi import *

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
    image: str
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
        "mode": "dark",
        "text": "#ffffff", 
        "text_alt": "#000000",
        "widget_background": "#1b1b1b",
        "page_background": "#151515",
        "background": "#0f0f0f",
    }

    @rx.event
    def edit_theme(self, value):
        if value == "dark":
            self.colors = {
                "mode": "dark",
                "text": "#ffffff", 
                "text_alt": "#000000",
                "widget_background": "#1b1b1b",
                "page_background": "#151515",
                "background": "#0f0f0f",
            }
        elif value == "light":
            self.colors = {
                "mode": "light",
                "text": "#000000", 
                "text_alt": "#ffffff",
                "widget_background": "#e4e4e4",
                "page_background": "#eaeaea",
                "background": "#f0f0f0",
            }
        print(self.colors)

    smoothness = "8px"
    @rx.event
    def edit_smoothness(self, value):
        self.smoothness = value
    #---- CLOUD STATUS ( REDIS SERVER )
    sync_status = "Last sync 23:52:21"


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
    widget_store_name: str = ""
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
                    new_widget = copy.deepcopy(widget)
                    self.widgets.append({
                        "id":  widget_id,
                        "name": new_widget["designed_name"],
                        "type": new_widget["designed_type"],
                        "data00": new_widget["designed_data00"],
                        "data01": new_widget["designed_data01"],
                        "data02": new_widget["designed_data02"],
                        "data03": new_widget["designed_data03"],
                    })
                    yield type(self).update_widget(widget_id)
                    yield rx.toast.success(f"New widget added: {name}")

                else:
                    yield rx.toast.warning(f"This widget is currently disabled.")

                print(self.widgets)


    # ---- All widget management.
    @rx.event
    def update_widget(self, widget_id, widget_type=""):
            
        for widget in self.widgets:

            if widget_type:
                if widget["type"].lower() != widget_type.lower():
                    continue
            if not widget_type and widget["id"] != widget_id:
                    continue

            if widget["type"].lower() == "crypto_v1":
                widget["data00"] = crypto_get_price(
                    symbol=widget["name"],
                    window=widget["data01"]
                )
                yield type(self).crypto_percentage(widget_id)
            if widget["type"].lower() == "crypto_v2":
                widget["data00"] = crypto_get_price(
                    symbol=widget["data01"],
                    window=widget["data02"]
                )
                yield type(self).crypto_percentage(widget_id)

            if widget["type"].lower() == "weather_v1":
                name, data = weather_get_data(widget["name"])
                if name:
                    widget["data00"] = data
                else:
                    yield rx.toast("Failed to update, city not found.")

            if widget["type"].lower() == "worldclock_v1":
                name = widget["data00"][0]["timezone"].replace(", ", "/").replace(" ", "_")
                widget["data00"] = worldclock_get_time(name)

            if widget["type"].lower() == "pomodoro_v1":
                if widget["data00"][0]["started"].lower() == "true":
                    sec = round(float(widget["data00"][0]["sec_left"])) - 1
                    widget["data00"][0]["sec_left"] = str(float(widget["data00"][0]["sec_left"]) - 1)
                    if sec == 0: 
                        widget["data00"][0]["timing"] ="00:00"
                        intervals = int(widget["data00"][0]["intervals"])
                        mode = widget["data00"][0]["mode"]
                        if mode == "pomodoro":
                            if intervals >= 4:
                                widget["data00"][0]["sec_left"] = str(float(widget["data00"][0]["long"])*60)
                                widget["data00"][0]["mode"] = "long"
                            else:
                                widget["data00"][0]["sec_left"] = str(float(widget["data00"][0]["short"])*60)
                                widget["data00"][0]["intervals"] = str(intervals +1)
                                widget["data00"][0]["mode"] = "short"
                        elif mode == "short":
                            widget["data00"][0]["sec_left"] = str(float(widget["data00"][0]["pomodoro"])*60)
                            widget["data00"][0]["mode"] = "pomodoro"

                        elif mode == "long":
                            widget["data00"][0]["sec_left"] = str(float(widget["data00"][0]["pomodoro"])*60)
                            widget["data00"][0]["intervals"] = "1"
                            widget["data00"][0]["mode"] = "pomodoro"
                    else:
                        minutes = round((sec % 3600) // 60)
                        seconds = round(sec % 60)
                        if len(str(minutes)) == 1:
                            minutes = f"0{minutes}"
                        if len(str(seconds)) == 1:
                            seconds = f"0{seconds}"
                        widget["data00"][0]["timing"] = f"{minutes}:{seconds}"

            if widget["type"].lower() == "terracd_v1":
                widget["data00"][0]["time"] = terracd_get_countdown()
                

            yield
                    
    @rx.event
    def update_all_widget(self):
        for widget in self.widgets:
            yield type(self).update_widget(widget["id"])
        

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
    def edit_widget_name(self, value: str, widget_id=""):
        self.widget_name = value

        for widget in self.widgets:
            if widget["id"] == widget_id:
                if widget["type"] == "weather_v1":
                    widget["data01"] = weather_get_name(value)

                if widget["type"] == "worldclock_v1":
                    widget["data01"] = worldclock_get_timezone(value).replace("_", " ")

    
    @rx.event
    def save_edit_widget(self, widget_id: str, val={}):
        for widget in self.widgets:
            if widget["id"] == widget_id:
                if widget["type"] == "crypto_v1":
                    if not isinstance(val, dict):
                        widget["data01"] = val
                        print("Updated")
                    elif self.widget_name:
                        widget["name"] = self.widget_name
                        
                if widget["type"] == "weather_v1":
                    widget["name"] = widget["data01"]

                if widget["type"] == "worldclock_v1":
                    widget["name"] = widget["data01"].split("/")[1]
                    widget["data00"] = worldclock_get_time(widget["data01"].replace(" ", "/")) 

                self.widget_name = ""
                yield type(self).update_widget(widget_id)

    # CRYPTO SPECIFIC 
    @rx.event
    def crypto_percentage(self, widget_id):
        for widget in self.widgets:
            if widget["id"] == widget_id:
                value = -round(((float(widget["data00"][0]["price"]) - float(widget["data00"][-1]["price"])) / float(widget["data00"][0]["price"])) * 100, 2)
                widget["data03"] = value

    # POMODORO SPECIFIC
    pomodoro, short, long = "", "", ""

    @rx.event
    def edit_pomodoro(self, value): self.pomodoro = value
    @rx.event
    def edit_short(self, value): self.short = value
    @rx.event
    def edit_long(self, value): self.long = value
    @rx.event
    def save_edit_pomodoro(self, widget_id):
        print("called_set", widget_id)
        for widget in self.widgets:
            if widget["id"] == widget_id:
                widget["data00"][0]["pomodoro"], widget["data00"][0]["short"], widget["data00"][0]["long"] = self.pomodoro, self.short, self.long
                print(widget)
                self.pomodoro, self.short, self.long = "25", "5", "15"
                yield type(self).command_pomodoro(widget_id, "reset")

    @rx.event
    def command_pomodoro(self, widget_id, command):
        print(f"Before command : {self.widgets}")
        print(f"Command: set {widget_id} to {command}")
        for widget in self.widgets:
            if widget["id"] == widget_id:
                if command == "start":
                    widget["data00"][0]["started"] = "true"
                    if not float(widget["data00"][0]["sec_left"]) < float(widget["data00"][0]["pomodoro"])*60: # If below than settings, means it is going
                        widget["data00"][0]["sec_left"] = str(float(widget["data00"][0]["pomodoro"])*60)
                        widget["data00"][0]["mode"] = "pomodoro"
                        widget["data00"][0]["intervals"] = "1"
                elif command == "stop":
                    widget["data00"][0]["started"] = "false"
                elif command == "reset":
                    widget["data00"][0]["sec_left"] = str(float(widget["data00"][0]["pomodoro"])*60)
                    widget["data00"][0]["started"] = "false"
                    widget["data00"][0]["mode"] = "pomodoro"
                    widget["data00"][0]["intervals"] = "1"
                    sec = float(widget["data00"][0]["sec_left"])
                    minutes = round(( sec % 3600) // 60)
                    seconds = round(sec % 60)
                    if len(str(minutes)) == 1:
                        minutes = f"0{minutes}"
                    if len(str(seconds)) == 1:
                        seconds = f"0{seconds}"
                    widget["data00"][0]["timing"] = f"{minutes}:{seconds}"
        print(f"After command : {self.widgets}")

    # QUICKNOTES SPECIFIC
    notes: str = ""

    @rx.event
    def save_notes(self, widget_id: str, new_text: str):
        for widget in self.widgets:
            if widget["id"] == widget_id:
                widget["data00"][0]["text"] = new_text

starttime = time.time()
class System(rx.State):
    cpu: float = 0
    ram: float = 0
    uptime: float = 0
    formatted_uptime: str = ""

    @rx.event
    def update_server_status(self):
        self.uptime = time.time() - starttime
        self.cpu = psutil.cpu_percent(interval=1)
        self.ram = psutil.virtual_memory().percent

        days, remainder = divmod(self.uptime, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        seconds = round(seconds,1)
        self.formatted_uptime = f"{days}d, {hours}h, {minutes}m, {seconds}s"
