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

class themeSetting(TypedDict):
    name: str
    text: str
    buttons: str
    widget: str
    page: str
    website: str

def load_json(json_path):
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return []
        
class Dashboard(rx.State):
    # ---- THEME START
    appearance = "dark"
    colors = {
        "name": "gray",
        "text": "var(--gray-12)",
        "buttons": "var(--gray-7)",
        "widget": "var(--gray-3)",
        "page": "var(--gray-2)",
        "website": "var(--gray-1)"
    }

    theme: list[themeSetting] = load_json("FlexDashV4/FDcolors.json")

    @rx.event
    def edit_appearance(self, value):
        self.appearance = value

    @rx.event
    def edit_theme(self, value):
        print(value)
        for t in self.theme:
            
            if t["name"] == value:
                self.colors = t

    smoothness = "8px"
    @rx.event
    def edit_smoothness(self, value):
        self.smoothness = value

    widget_per_row: str = "4"
    @rx.event
    def edit_wpr(self, value):
        self.widget_per_row = value
    
    #---- CLOUD STATUS ( REDIS SERVER )
    sync_status = "Last sync 23:52:21"


    # ---- SIDEBAR START
    page: str = "home"
    parking: bool = False
    @rx.event
    def sidebar_parking(self, active: bool):
        self.parking = active
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
    widgets_store: list[widgetStore]= load_json("FlexDashV4/FDwidgets.json")
    
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

    # FDWIDGET V2 SPECIFICALLY DESIGNED, MUST APPLY AFTER ANY EDIT / ON BLUR 
    temp_name: str = ""
    temp_data00: list[dict[str, str]] = []
    temp_data01: str = ""
    temp_data02: str = ""
    temp_data03: int = 0

    @rx.event
    def edit_any(self, value, types):
        if types == "name": self.temp_name = value
        if types == "00": self.temp_data00 = value
        if types == "01": self.temp_data01 = value
        if types == "02": self.temp_data02 = value
        if types == "03": self.temp_data03 = value
        
    @rx.event
    def apply_any(self, widget_id):
        for widget in self.widgets:
            if widget["id"] == widget_id:
                if self.temp_name: 
                    widget["name"] = self.temp_name
                if self.temp_data00: 
                    widget["data00"] = self.temp_data00
                if self.temp_data01: 
                    widget["data01"] = self.temp_data01
                if self.temp_data02: 
                    widget["data02"] = self.temp_data02
                if self.temp_data03: 
                    widget["data03"] = self.temp_data03
                yield type(self).clear_any
                yield type(self).update_widget(widget_id)

    @rx.event
    def clear_any(self):
        self.temp_name, self.temp_data00, self.temp_data01, self.temp_data02, self.temp_data03 = "", [], "", "", 0

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

    