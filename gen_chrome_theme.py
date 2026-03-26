"""
Generate a Tokyo Night Chrome theme extension.

Output: chrome-theme/
  manifest.json
  images/
    theme_frame.png          – browser titlebar / window frame
    theme_toolbar.png        – tab strip + address bar area
    theme_ntp_background.png – New Tab Page background (aurora, 1920×1080)
    theme_tab_background.png – inactive tab background strip

Load in Chrome via chrome://extensions → "Load unpacked" → select chrome-theme/
"""
import os, json, math
import numpy as np
from PIL import Image, ImageFilter

# ── Palette (Tokyo Night v2) ──────────────────────────────────────────────────
BG        = (0x1a, 0x1b, 0x27)   # #1A1B27  main background
BG_DARK   = (0x13, 0x14, 0x1e)   # #13141E  darker background
BG_MID    = (0x1e, 0x20, 0x36)   # #1E2036  mid-tone (tab strip)
FG        = (0xbb, 0xc6, 0xf6)   # #BBC6F6  foreground / active tab text
BLUE      = (0x7a, 0xa2, 0xf7)   # #7AA2F7
BLUE_BR   = (0xa9, 0xb8, 0xff)   # #A9B8FF
CYAN      = (0x2a, 0xb7, 0xe7)   # #2AB7E7
CYAN_BR   = (0x24, 0xd5, 0xf8)   # #24D5F8
GREEN     = (0x00, 0xbc, 0xdb)   # #00BCDB
GREEN_BR  = (0x4e, 0xf4, 0xdf)   # #4EF4DF
PURPLE    = (0x9b, 0x84, 0xee)   # #9B84EE
PURPLE_DIM= (0x60, 0x50, 0x90)   # dim purple for inactive tabs
RED       = (0xf7, 0x76, 0x8e)   # #F7768E
ORANGE    = (0xe6, 0x9f, 0x51)   # #E69F51

OUT_DIR    = os.path.join(os.path.dirname(__file__), "chrome-theme")
IMG_DIR    = os.path.join(OUT_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)


# ── Manifest ──────────────────────────────────────────────────────────────────

MANIFEST = {
    "manifest_version": 3,
    "name": "Tokyo Night",
    "version": "1.0",
    "description": "Tokyo Night dark theme — inspired by tokyo-night-vscode and Catppuccin.",
    "theme": {
        "images": {
            "theme_frame":           "images/theme_frame.png",
            "theme_frame_inactive":  "images/theme_frame.png",
            "theme_toolbar":         "images/theme_toolbar.png",
            "theme_tab_background":  "images/theme_tab_background.png",
            "theme_ntp_background":  "images/theme_ntp_background.png",
        },
        "colors": {
            # Browser chrome / frame
            "frame":                list(BG),
            "frame_inactive":       list(BG_DARK),
            "frame_incognito":      [0x16, 0x0d, 0x2a],   # dark purple tint
            # Toolbar (address bar row)
            "toolbar":              list(BG_MID),
            # Tab text
            "tab_text":             list(FG),
            "tab_background_text":  [0x72, 0x62, 0xaa],   # dim purple
            # Bookmarks bar
            "bookmark_text":        list(FG),
            # New Tab Page
            "ntp_background":       list(BG),
            "ntp_text":             list(FG),
            "ntp_link":             list(BLUE),
            "ntp_header":           list(BG_DARK),
            "ntp_section":          list(BG_MID),
            "ntp_section_text":     list(FG),
            "ntp_section_link":     list(CYAN),
            # Omnibox
            "omnibox_background":   list(BG_DARK),
            "omnibox_text":         list(FG),
        },
        "tints": {
            # Toolbar icons: hue=neutral, sat=low, lightness=bright
            "buttons":          [0.5, 0.5, 0.78],
            "background_tab":   [-1, -1, -1],
        },
        "properties": {
            "ntp_background_alignment": "center top",
            "ntp_background_repeat":    "no-repeat",
            "ntp_logo_alternate":       1,
        },
    },
}

manifest_path = os.path.join(OUT_DIR, "manifest.json")
with open(manifest_path, "w") as f:
    json.dump(MANIFEST, f, indent=2)
print(f"Wrote {manifest_path}")


# ── Helper: make a horizontal gradient strip ──────────────────────────────────

def gradient_strip(w, h, left_color, right_color, mid_color=None):
    """
    Create an RGB gradient strip of size (w, h).
    If mid_color is given, it's a two-segment gradient (left→mid, mid→right).
    """
    img = np.zeros((h, w, 3), dtype=np.float32)
    x = np.linspace(0.0, 1.0, w)

    for c in range(3):
        if mid_color is not None:
            # first half: left → mid
            seg1 = np.where(x < 0.5,
                            left_color[c] + (mid_color[c] - left_color[c]) * (x / 0.5),
                            mid_color[c]  + (right_color[c] - mid_color[c]) * ((x - 0.5) / 0.5))
            img[:, :, c] = seg1[None, :]
        else:
            img[:, :, c] = (left_color[c] + (right_color[c] - left_color[c]) * x)[None, :]

    return np.clip(img, 0, 255).astype(np.uint8)


# ── theme_frame.png ───────────────────────────────────────────────────────────
# Subtle left-to-right gradient across the title bar; very dark overall.
print("Generating theme_frame.png ...")
frame = gradient_strip(
    w=3840, h=80,
    left_color=(0x16, 0x17, 0x28),   # slightly blue-dark on left
    right_color=(0x1c, 0x1d, 0x30),  # slightly lighter right
    mid_color=BG,
)
# Add a 1px bottom highlight line (subtle blue rule at bottom of frame)
frame[-1, :] = [0x2a, 0x2c, 0x4a]
Image.fromarray(frame).save(os.path.join(IMG_DIR, "theme_frame.png"))
print("  → chrome-theme/images/theme_frame.png")


# ── theme_toolbar.png ─────────────────────────────────────────────────────────
# Slightly lighter than the frame; very subtle top-to-bottom gradient.
print("Generating theme_toolbar.png ...")
toolbar = np.zeros((80, 3840, 3), dtype=np.uint8)
y = np.linspace(0.0, 1.0, 80)
for c in range(3):
    col = BG_MID[c] + (BG[c] - BG_MID[c]) * y
    toolbar[:, :, c] = np.clip(col, 0, 255).astype(np.uint8)[:, None]
# Bottom separator line
toolbar[-1, :] = [0x30, 0x32, 0x50]
Image.fromarray(toolbar).save(os.path.join(IMG_DIR, "theme_toolbar.png"))
print("  → chrome-theme/images/theme_toolbar.png")


# ── theme_tab_background.png ──────────────────────────────────────────────────
# Inactive tab: a small (200×40) strip, slightly lighter than the toolbar.
print("Generating theme_tab_background.png ...")
tab_bg = gradient_strip(
    w=200, h=40,
    left_color=(0x22, 0x24, 0x3c),
    right_color=(0x1e, 0x20, 0x36),
)
Image.fromarray(tab_bg).save(os.path.join(IMG_DIR, "theme_tab_background.png"))
print("  → chrome-theme/images/theme_tab_background.png")


# ── theme_ntp_background.png — aurora waves at 1920×1080 ─────────────────────

NW, NH = 1920, 1080

def make_ntp_base(w, h):
    img = np.zeros((h, w, 3), dtype=np.float32)
    y_f = np.arange(h)[:, None] / h
    x_f = np.arange(w)[None, :] / w
    lights = [
        (0.20, 0.80, 0.65, 0.65, BLUE,    0.28),
        (0.78, 0.22, 0.55, 0.55, CYAN,    0.20),
        (0.50, 0.50, 0.90, 0.90, PURPLE,  0.09),
        (0.05, 0.20, 0.35, 0.35, GREEN,   0.11),
        (0.90, 0.85, 0.30, 0.30, RED,     0.05),
    ]
    for cx, cy, rx, ry, color, strength in lights:
        dx = (x_f - cx) / rx
        dy = (y_f - cy) / ry
        dist = np.sqrt(dx**2 + dy**2)
        falloff = np.exp(-(dist)**1.6) * strength
        for c in range(3):
            img[:, :, c] += falloff * color[c]
    base = np.array(BG, dtype=np.float32)
    img = img + base[None, None, :]
    return np.clip(img, 0, 255).astype(np.uint8)


def make_ntp_aurora(w, h):
    glow = np.zeros((h, w, 3), dtype=np.float32)
    x = np.linspace(0, 1, w)
    y_coords = np.arange(h)
    bands = [
        (0.07, 0.032, 2.8, 0.00, 0.10, CYAN_BR,  52),
        (0.20, 0.048, 2.2, 1.20, 0.09, GREEN_BR, 44),
        (0.33, 0.042, 1.9, 0.60, 0.10, BLUE,     48),
        (0.47, 0.038, 3.0, 2.10, 0.09, PURPLE,   56),
        (0.62, 0.052, 1.6, 0.90, 0.10, CYAN,     42),
        (0.77, 0.030, 3.8, 3.00, 0.07, GREEN,    34),
    ]
    for base_y, amp, freq, phase, thick, color, strength in bands:
        cy = (base_y + amp * np.sin(freq * math.pi * x + phase)) * h
        cy += (amp * 0.40 * np.sin(freq * 1.7 * math.pi * x + phase + 1.1)) * h
        thick_px = thick * h
        sigma = thick_px * 0.45
        dist = np.abs(y_coords[:, None].astype(np.float32) - cy[None, :])
        falloff = np.exp(-(dist**2) / (2 * sigma**2))
        edge_fade = np.sin(np.pi * x) ** 0.35
        falloff *= edge_fade[None, :]
        col = np.array(color, dtype=np.float32)
        glow += falloff[:, :, None] * (col / 255.0) * strength
    return glow


def draw_ntp_stars(layer, w, h):
    rng = np.random.default_rng(77)
    n = 600
    xs = rng.integers(0, w, n)
    ys = rng.integers(0, h * 2 // 3, n)
    alphas = rng.integers(25, 100, n)
    palette = [CYAN_BR, BLUE_BR, GREEN_BR, PURPLE, (255, 255, 255)]
    for i in range(n):
        col = palette[i % len(palette)]
        a = int(alphas[i])
        layer[ys[i], xs[i]] = (*col, a)
        if rng.random() < 0.07:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = ys[i] + dy, xs[i] + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        layer[ny, nx] = (*col, a // 2)
    return layer


def composite_add(base_rgb, glow_rgb):
    return np.clip(base_rgb.astype(np.float32) + glow_rgb, 0, 255).astype(np.uint8)


def composite_alpha(base_rgb, layer_rgba):
    base = base_rgb.astype(np.float32)
    src  = layer_rgba[:, :, :3].astype(np.float32)
    a    = layer_rgba[:, :, 3:4].astype(np.float32) / 255.0
    return np.clip(base * (1 - a) + src * a, 0, 255).astype(np.uint8)


def add_noise(img, strength=3):
    noise = np.random.randint(-strength, strength + 1, img.shape, dtype=np.int16)
    return np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)


print("Generating theme_ntp_background.png (1920×1080) ...")
np.random.seed(7)

base_np   = make_ntp_base(NW, NH)
aurora    = make_ntp_aurora(NW, NH)
aurora_pil = Image.fromarray(np.clip(aurora, 0, 255).astype(np.uint8))
aurora_pil = aurora_pil.filter(ImageFilter.GaussianBlur(radius=7))
aurora_blurred = np.array(aurora_pil).astype(np.float32)

result = composite_add(base_np, aurora_blurred)

star_layer = np.zeros((NH, NW, 4), dtype=np.uint8)
star_layer = draw_ntp_stars(star_layer, NW, NH)
result = composite_alpha(result, star_layer)

# Scanlines (every 3rd row darkened slightly)
for y in range(0, NH, 3):
    result[y] = np.clip(result[y].astype(np.int16) - 6, 0, 255).astype(np.uint8)

pil_res  = Image.fromarray(result)
blurred  = pil_res.filter(ImageFilter.GaussianBlur(radius=0.8))
result   = (np.array(pil_res) * 0.84 + np.array(blurred) * 0.16).astype(np.uint8)
result   = add_noise(result, strength=4)

Image.fromarray(result).save(os.path.join(IMG_DIR, "theme_ntp_background.png"),
                              optimize=False, compress_level=6)
print("  → chrome-theme/images/theme_ntp_background.png")

print()
print("Done! Load the theme in Chrome:")
print("  chrome://extensions → 'Load unpacked' → select chrome-theme/")
