# Note : This file is designed specfically to generate FDcolors.json to prevent developer hand die because typing 1by1

import json
from typing import TypedDict

class themeSetting(TypedDict):
    name: str
    text: str
    buttons: str
    widget: str
    page: str
    website: str

theme_presets = []
radix_colors = ["gray", "mauve", "sage", "olive", "sand", "tomato", "red", "ruby", "crimson", "pink", "plum", "purple", "violet",
                "iris", "indigo", "blue", "cyan", "teal", "jade", "green", "grass", "bronze", "gold", "brown", "orange", "amber", "yellow", "lime",
                "mint","sky"]

for color in radix_colors:
    theme_presets.append({
        "name": f"dark-{color.lower()}",
        "text": f"var(--{color}-12)",
        "buttons": f"var(--{color}-7)",
        "widget": f"var(--{color}-3)",
        "page": f"var(--{color}-2)",
        "website": f"var(--{color}-1)"
    })

with open("FDcolors.json", "w") as f:
    json.dump(theme_presets, f, indent=4)

print(f"Done, at colors {len(radix_colors)} of types ")