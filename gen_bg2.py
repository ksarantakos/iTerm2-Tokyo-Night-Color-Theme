"""Generate a Tokyo Night v2 aurora-wave terminal background image."""
import numpy as np
from PIL import Image, ImageFilter
import math, os, random

random.seed(7)
np.random.seed(7)

W, H = 3840, 2160  # 4K

# Tokyo Night v2 palette
BG       = (0x1a, 0x1b, 0x27)
BG2      = (0x0d, 0x0e, 0x1a)   # extra dark for base
BLUE     = (0x7a, 0xa2, 0xf7)
CYAN     = (0x2a, 0xb7, 0xe7)
CYAN_BR  = (0x24, 0xd5, 0xf8)
GREEN    = (0x00, 0xbc, 0xdb)
GREEN_BR = (0x4e, 0xf4, 0xdf)
PURPLE   = (0x9b, 0x84, 0xee)
PURPLE_BR= (0xb0, 0x9a, 0xff)   # slightly toned down from pure white
RED      = (0xf7, 0x76, 0x8e)
ORANGE   = (0xe6, 0x9f, 0x51)


# ── Base gradient ──────────────────────────────────────────────────────────────

def make_base(w, h):
    img = np.zeros((h, w, 3), dtype=np.float32)
    y_idx = np.arange(h)[:, None] / h
    x_idx = np.arange(w)[None, :] / w

    lights = [
        # (cx, cy, radius_x, radius_y, color, strength)
        (0.20, 0.80, 0.65, 0.65, BLUE,    0.30),
        (0.80, 0.20, 0.55, 0.55, CYAN,    0.22),
        (0.50, 0.50, 0.90, 0.90, PURPLE,  0.10),
        (0.05, 0.20, 0.35, 0.35, GREEN,   0.12),
        (0.90, 0.85, 0.30, 0.30, RED,     0.06),
    ]
    for cx, cy, rx, ry, color, strength in lights:
        dx = (x_idx - cx) / rx
        dy = (y_idx - cy) / ry
        dist = np.sqrt(dx**2 + dy**2)
        falloff = np.exp(-(dist)**1.6) * strength
        for c in range(3):
            img[:, :, c] += falloff * color[c]

    base = np.array(BG, dtype=np.float32)
    img = img + base[None, None, :]
    return np.clip(img, 0, 255).astype(np.uint8)


# ── Aurora bands ──────────────────────────────────────────────────────────────

def make_aurora(w, h):
    """Render flowing sine-wave aurora ribbons as additive RGB glow (0–255 float)."""
    glow = np.zeros((h, w, 3), dtype=np.float32)  # additive contribution

    x = np.linspace(0, 1, w)
    y_coords = np.arange(h)

    aurora_bands = [
        # (base_y_frac, amplitude, freq, phase, thickness_frac, color, strength)
        # strength = peak pixel addition per channel (glow is already in 0-255 units)
        (0.07, 0.032, 2.8, 0.00, 0.09, CYAN_BR,  72),
        (0.20, 0.048, 2.2, 1.20, 0.08, GREEN_BR, 60),
        (0.33, 0.042, 1.9, 0.60, 0.10, BLUE,     65),
        (0.47, 0.038, 3.0, 2.10, 0.09, PURPLE,   70),   # purple band — boosted
        (0.62, 0.052, 1.6, 0.90, 0.10, CYAN,     55),
        (0.77, 0.030, 3.8, 3.00, 0.07, GREEN,    42),
    ]

    for base_y, amp, freq, phase, thick, color, strength in aurora_bands:
        # Wavy center line with two harmonics
        center_y = (base_y + amp * np.sin(freq * math.pi * x + phase)) * h
        center_y += (amp * 0.40 * np.sin(freq * 1.7 * math.pi * x + phase + 1.1)) * h

        thick_px = thick * h          # e.g. 0.10 * 2160 = 216 px wide swath
        sigma = thick_px * 0.45       # sigma ≈ half the swath width

        dist = np.abs(y_coords[:, None].astype(np.float32) - center_y[None, :])
        falloff = np.exp(-(dist**2) / (2 * sigma**2))  # (h, w), peak=1.0

        # Taper near screen edges
        edge_fade = np.sin(np.pi * x) ** 0.35
        falloff *= edge_fade[None, :]

        col = np.array(color, dtype=np.float32)
        # Each band adds at most `strength` pixel values per channel, scaled by
        # the colour's own intensity (col/255) so colours keep their hue.
        glow += falloff[:, :, None] * (col / 255.0) * strength

    return glow  # float, unbounded — caller clips after blur


# ── Horizontal scan-line shimmer ───────────────────────────────────────────────

def make_scanlines(w, h):
    layer = np.zeros((h, w, 4), dtype=np.uint8)
    for y in range(0, h, 3):
        layer[y, :, :] = (0, 0, 0, 6)
    return layer


# ── Sparse star field ──────────────────────────────────────────────────────────

def draw_stars(layer_np, w, h):
    rng = np.random.default_rng(99)
    n = 1200
    xs = rng.integers(0, w, n)
    ys = rng.integers(0, h // 2, n)  # only upper half
    alphas = rng.integers(20, 90, n)
    colors = [CYAN_BR, PURPLE_BR, BLUE, GREEN_BR, (255, 255, 255)]
    for i in range(n):
        col = colors[i % len(colors)]
        a = int(alphas[i])
        layer_np[ys[i], xs[i]] = (*col, a)
        # occasional slightly larger star
        if rng.random() < 0.08:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = ys[i] + dy, xs[i] + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        layer_np[ny, nx] = (*col, a // 2)
    return layer_np


def add_noise(img_np, strength=4):
    noise = np.random.randint(-strength, strength + 1, img_np.shape, dtype=np.int16)
    return np.clip(img_np.astype(np.int16) + noise, 0, 255).astype(np.uint8)


def composite_rgba(base_rgb, layer_rgba):
    """Alpha-composite an RGBA uint8 numpy layer onto an RGB base."""
    base = base_rgb.astype(np.float32)
    src_rgb = layer_rgba[:, :, :3].astype(np.float32)
    src_a   = layer_rgba[:, :, 3:4].astype(np.float32) / 255.0
    out = base * (1 - src_a) + src_rgb * src_a
    return np.clip(out, 0, 255).astype(np.uint8)


# ── Main ───────────────────────────────────────────────────────────────────────

print("Generating base gradient...")
base_np = make_base(W, H)

print("Generating aurora bands...")
aurora_glow = make_aurora(W, H)  # float additive glow, shape (H, W, 3)

# Blur aurora for soft glow spread before adding
aurora_pil = Image.fromarray(np.clip(aurora_glow, 0, 255).astype(np.uint8))
aurora_pil = aurora_pil.filter(ImageFilter.GaussianBlur(radius=14))
aurora_blurred = np.array(aurora_pil).astype(np.float32)

print("Compositing aurora (additive)...")
result_f = base_np.astype(np.float32) + aurora_blurred
result = np.clip(result_f, 0, 255).astype(np.uint8)

print("Adding stars...")
star_layer = np.zeros((H, W, 4), dtype=np.uint8)
star_layer = draw_stars(star_layer, W, H)
result = composite_rgba(result, star_layer)

print("Adding scanlines...")
scan_layer = make_scanlines(W, H)
result = composite_rgba(result, scan_layer)

print("Applying glow blur blend...")
pil_result = Image.fromarray(result)
blurred = pil_result.filter(ImageFilter.GaussianBlur(radius=1.5))
r_np = np.array(pil_result).astype(np.float32)
b_np = np.array(blurred).astype(np.float32)
result = (r_np * 0.82 + b_np * 0.18).astype(np.uint8)

print("Adding film grain...")
result = add_noise(result, strength=4)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tokyo-night-v2-bg.png")
print(f"Saving to {out_path} ...")
Image.fromarray(result).save(out_path, optimize=False, compress_level=6)
print("Done.")
