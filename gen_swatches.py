"""Generate 20×20 PNG colour swatches for the Tokyo Night v2 palette.

Reads colour values directly from tokyo-night-v2.itermcolors so the
swatches are always in sync with the shipped theme file.

Output: colors-v2/{black,red,green,yellow,blue,magenta,cyan,white}.png
        colors-v2/bright_{black,red,green,yellow,blue,magenta,cyan,white}.png
"""
import os, plistlib
from PIL import Image

HERE    = os.path.dirname(os.path.abspath(__file__))
SRC     = os.path.join(HERE, "tokyo-night-v2.itermcolors")
OUT_DIR = os.path.join(HERE, "colors-v2")
os.makedirs(OUT_DIR, exist_ok=True)

with open(SRC, "rb") as f:
    palette = plistlib.load(f)

def ansi_rgb(index):
    d = palette[f"Ansi {index} Color"]
    return (
        round(d["Red Component"]   * 255),
        round(d["Green Component"] * 255),
        round(d["Blue Component"]  * 255),
    )

NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

for i, name in enumerate(NAMES):
    for prefix, ansi_index in [("", i), ("bright_", i + 8)]:
        rgb      = ansi_rgb(ansi_index)
        filename = os.path.join(OUT_DIR, f"{prefix}{name}.png")
        Image.new("RGB", (20, 20), rgb).save(filename)
        print(f"  {prefix}{name}.png  →  #{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}")

print("Done.")
