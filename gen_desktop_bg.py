"""
Generate a Tokyo Night v2 macOS desktop background.

Composition:
  - Deep navy sky with radial colour blooms
  - Aurora borealis bands (more vivid than the terminal version)
  - Star field
  - Stylised city silhouette with lit windows at the bottom

Output: tokyo-night-desktop-bg.png  (3840 × 2160, 4K)
"""
import math, os, random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

random.seed(13)
np.random.seed(13)

W, H = 3440, 1440

HERE     = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "tokyo-night-desktop-bg.png")

# ── Palette (Tokyo Night v2) ──────────────────────────────────────────────────
BG        = (0x1a, 0x1b, 0x27)
BG_DARK   = (0x0d, 0x0e, 0x1a)
BLUE      = (0x7a, 0xa2, 0xf7)
BLUE_BR   = (0xa9, 0xb8, 0xff)
CYAN      = (0x2a, 0xb7, 0xe7)
CYAN_BR   = (0x24, 0xd5, 0xf8)
GREEN     = (0x00, 0xbc, 0xdb)
GREEN_BR  = (0x4e, 0xf4, 0xdf)
PURPLE    = (0x9b, 0x84, 0xee)
PURPLE_BR = (0xb0, 0x9a, 0xff)
RED       = (0xf7, 0x76, 0x8e)
ORANGE    = (0xe6, 0x9f, 0x51)
YELLOW    = (0xe1, 0xc3, 0x81)
FG        = (0xbb, 0xc6, 0xf6)

HORIZON   = int(H * 0.68)   # y-coordinate of the rooftop horizon


# ── 1. Sky base gradient ──────────────────────────────────────────────────────

def make_sky(w, h, horizon):
    img = np.zeros((h, w, 3), dtype=np.float32)

    # Radial blooms
    y_f = np.arange(h)[:, None] / h
    x_f = np.arange(w)[None, :] / w
    blooms = [
        (0.18, 0.55, 0.70, 0.70, BLUE,   0.35),
        (0.82, 0.20, 0.55, 0.55, CYAN,   0.25),
        (0.50, 0.42, 0.85, 0.85, PURPLE, 0.12),
        (0.05, 0.18, 0.38, 0.38, GREEN,  0.14),
        (0.88, 0.78, 0.28, 0.28, RED,    0.07),
        (0.40, 0.72, 0.30, 0.30, PURPLE, 0.10),
    ]
    for cx, cy, rx, ry, color, strength in blooms:
        dx = (x_f - cx) / rx
        dy = (y_f - cy) / ry
        dist = np.sqrt(dx**2 + dy**2)
        falloff = np.exp(-(dist)**1.7) * strength
        for c in range(3):
            img[:, :, c] += falloff * color[c]

    base = np.array(BG, dtype=np.float32)
    img = img + base[None, None, :]

    # Darken toward the very top corners
    corner_vignette = np.ones((h, w), dtype=np.float32)
    for cx_f, cy_f in [(0.0, 0.0), (1.0, 0.0)]:
        dx = (x_f - cx_f) * 1.2
        dy = (y_f - cy_f) * 0.8
        dist = np.sqrt(dx**2 + dy**2)
        corner_vignette *= (1 - 0.35 * np.exp(-(dist)**2 / (2 * 0.25**2)))
    for c in range(3):
        img[:, :, c] *= corner_vignette

    return np.clip(img, 0, 255).astype(np.uint8)


# ── 2. Aurora bands ───────────────────────────────────────────────────────────

def make_aurora(w, h, horizon):
    glow = np.zeros((h, w, 3), dtype=np.float32)
    x = np.linspace(0, 1, w)
    y_coords = np.arange(h)
    sky_frac = horizon / h   # aurora lives only in the sky portion

    bands = [
        # (base_y as fraction of sky, amp, freq, phase, thick_frac of sky, color, strength)
        (0.08, 0.035, 2.8, 0.00, 0.11, CYAN_BR,  80),
        (0.20, 0.048, 2.3, 1.20, 0.10, GREEN_BR, 65),
        (0.32, 0.042, 1.9, 0.60, 0.12, BLUE,     75),
        (0.44, 0.038, 3.1, 2.10, 0.10, PURPLE,   85),
        (0.55, 0.052, 1.7, 0.90, 0.11, CYAN,     60),
        (0.65, 0.030, 3.8, 3.00, 0.08, GREEN,    45),
    ]

    for base_y_sky, amp, freq, phase, thick, color, strength in bands:
        base_y = base_y_sky * sky_frac  # convert to full-image fraction
        cy = (base_y + amp * np.sin(freq * math.pi * x + phase)) * h
        cy += (amp * 0.40 * np.sin(freq * 1.7 * math.pi * x + phase + 1.1)) * h

        thick_px = thick * horizon
        sigma = thick_px * 0.45
        dist = np.abs(y_coords[:, None].astype(np.float32) - cy[None, :])
        falloff = np.exp(-(dist**2) / (2 * sigma**2))

        # Fade above image top and below horizon
        sky_mask = np.where(y_coords < horizon, 1.0, 0.0)
        falloff *= sky_mask[:, None]

        edge_fade = np.sin(np.pi * x) ** 0.3
        falloff *= edge_fade[None, :]

        col = np.array(color, dtype=np.float32)
        glow += falloff[:, :, None] * (col / 255.0) * strength

    return glow


# ── 3. Stars ──────────────────────────────────────────────────────────────────

def make_stars(w, h, horizon):
    layer = np.zeros((h, w, 4), dtype=np.uint8)
    rng = np.random.default_rng(42)
    n = 2200
    xs = rng.integers(0, w, n)
    ys = rng.integers(0, int(horizon * 0.92), n)
    alphas = rng.integers(30, 120, n)
    palette = [CYAN_BR, BLUE_BR, GREEN_BR, PURPLE_BR, FG, (255, 255, 255)]
    for i in range(n):
        col = palette[i % len(palette)]
        a = int(alphas[i])
        layer[ys[i], xs[i]] = (*col, a)
        if rng.random() < 0.09:   # larger star with a soft cross
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = ys[i]+dy, xs[i]+dx
                if 0 <= ny < h and 0 <= nx < w:
                    layer[ny, nx] = (*col, a // 3)
    return layer


# ── 4. City silhouette ────────────────────────────────────────────────────────

def make_city(w, h, horizon):
    """
    Procedurally generated skyline silhouette.
    Returns an RGBA image: buildings are near-black with lit windows.
    """
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw  = ImageDraw.Draw(layer)

    rng = random.Random(7)

    BUILDING_DARK = (0x0a, 0x0b, 0x14, 255)
    BUILDING_MID  = (0x10, 0x11, 0x1c, 255)

    # Window colours: accent palette colours, dim
    WINDOW_COLORS = [
        (0x7a, 0xa2, 0xf7, 200),   # blue
        (0x2a, 0xb7, 0xe7, 180),   # cyan
        (0x9b, 0x84, 0xee, 190),   # purple
        (0xe1, 0xc3, 0x81, 170),   # yellow/warm
        (0xe6, 0x9f, 0x51, 160),   # orange
        (0xbb, 0xc6, 0xf6, 150),   # fg/cool white
    ]

    x = 0
    buildings = []
    while x < w:
        bw = rng.randint(55, 260)
        # Cluster buildings: vary height based on local density
        bh = rng.randint(int(h * 0.08), int(h * 0.42))
        buildings.append((x, bw, bh))
        x += bw + rng.randint(-10, 8)   # slight overlap for depth

    # Sort so taller buildings draw last (appear in front)
    buildings.sort(key=lambda b: b[2])

    for bx, bw, bh in buildings:
        top = horizon - bh
        color = BUILDING_DARK if bh > h * 0.22 else BUILDING_MID
        draw.rectangle([bx, top, bx + bw, h], fill=color)

        # Windows
        ww, wh = rng.randint(6, 14), rng.randint(8, 18)
        pad_x, pad_y = 10, 12
        cols = max(1, (bw - 2 * pad_x) // (ww + 8))
        rows = max(1, (bh - 2 * pad_y) // (wh + 10))
        for row in range(rows):
            for col in range(cols):
                if rng.random() < 0.45:   # ~45% of windows lit
                    wx = bx + pad_x + col * (ww + 8)
                    wy = top + pad_y + row * (wh + 10)
                    wcol = rng.choice(WINDOW_COLORS)
                    draw.rectangle([wx, wy, wx + ww, wy + wh], fill=wcol)

    return np.array(layer)


# ── 5. Ground / reflection strip ─────────────────────────────────────────────

def make_ground(w, h, horizon):
    """Very dark ground below the city — subtle colour-tinted floor."""
    layer = np.zeros((h, w, 4), dtype=np.uint8)
    ground = np.array(BG_DARK, dtype=np.float32)
    # Slight blue-purple tint from reflected city lights
    tint = np.array(PURPLE, dtype=np.float32) * 0.06
    fill = np.clip(ground + tint, 0, 255).astype(np.uint8)
    layer[horizon:, :, :3] = fill
    layer[horizon:, :, 3]  = 255
    return layer


# ── Composite helpers ─────────────────────────────────────────────────────────

def composite_add(base, glow):
    return np.clip(base.astype(np.float32) + glow, 0, 255).astype(np.uint8)


def composite_alpha(base_rgb, layer_rgba):
    base = base_rgb.astype(np.float32)
    src  = layer_rgba[:, :, :3].astype(np.float32)
    a    = layer_rgba[:, :, 3:4].astype(np.float32) / 255.0
    return np.clip(base * (1 - a) + src * a, 0, 255).astype(np.uint8)


def add_noise(img, strength=3):
    noise = np.random.randint(-strength, strength + 1, img.shape, dtype=np.int16)
    return np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)


# ── Main ──────────────────────────────────────────────────────────────────────

print(f"Canvas: {W}×{H}, horizon at y={HORIZON}")

print("Sky base...")
result = make_sky(W, H, HORIZON)

print("Aurora...")
aurora = make_aurora(W, H, HORIZON)
aurora_pil = Image.fromarray(np.clip(aurora, 0, 255).astype(np.uint8))
aurora_pil = aurora_pil.filter(ImageFilter.GaussianBlur(radius=16))
result = composite_add(result, np.array(aurora_pil).astype(np.float32))

print("Stars...")
stars = make_stars(W, H, HORIZON)
result = composite_alpha(result, stars)

print("Ground...")
ground = make_ground(W, H, HORIZON)
result = composite_alpha(result, ground)

print("City silhouette...")
city = make_city(W, H, HORIZON)
result = composite_alpha(result, city)

print("Glow blend + grain...")
pil_res = Image.fromarray(result)
blurred = pil_res.filter(ImageFilter.GaussianBlur(radius=1.2))
result = (np.array(pil_res) * 0.88 + np.array(blurred) * 0.12).astype(np.uint8)
result = add_noise(result, strength=4)

print(f"Saving to {OUT_PATH} ...")
Image.fromarray(result).save(OUT_PATH, optimize=False, compress_level=6)
print("Done.")
