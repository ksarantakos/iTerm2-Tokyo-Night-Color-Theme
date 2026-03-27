"""Generate a Tokyo Night abstract terminal background image."""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import math, os, random

random.seed(42)
np.random.seed(42)

W, H = 3840, 2160  # 4K

# Tokyo Night palette
BG       = (0x1a, 0x1b, 0x2e)   # deep background
BG2      = (0x16, 0x17, 0x27)   # darker bg
BLUE     = (0x52, 0x34, 0xb2)
BLUE_BR  = (0x7c, 0x65, 0xc3)
CYAN     = (0x29, 0xb7, 0xe6)
CYAN_BR  = (0x24, 0xd5, 0xf7)
PURPLE   = (0x9a, 0x84, 0xee)
RED      = (0xe2, 0x51, 0x4f)
ORANGE   = (0xe5, 0x9e, 0x50)
GREEN    = (0x00, 0xbc, 0xdb)


def hex_to_f(h):
    r = int(h[1:3], 16) / 255
    g = int(h[3:5], 16) / 255
    b = int(h[5:7], 16) / 255
    return (r, g, b)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def make_gradient(w, h):
    """Create a dark radial gradient base."""
    img = np.zeros((h, w, 3), dtype=np.float32)
    cx, cy = w * 0.35, h * 0.55
    for name, (px, py, radius, color, strength) in {
        'main':  (cx,       cy,       max(w,h)*0.9, BLUE,    0.25),
        'cyan':  (w*0.75,   h*0.25,   max(w,h)*0.55, CYAN,   0.18),
        'purp':  (w*0.15,   h*0.8,    max(w,h)*0.45, PURPLE, 0.12),
        'red':   (w*0.85,   h*0.75,   max(w,h)*0.35, RED,    0.07),
    }.items():
        y_idx = np.arange(h)[:, None]
        x_idx = np.arange(w)[None, :]
        dist = np.sqrt((x_idx - px)**2 + (y_idx - py)**2)
        falloff = np.exp(-(dist / radius)**1.5) * strength
        for c in range(3):
            img[:, :, c] += falloff * color[c]

    # Base dark color
    base = np.array(BG, dtype=np.float32)
    img = img + base[None, None, :]
    img = np.clip(img, 0, 255).astype(np.uint8)
    return Image.fromarray(img)


def draw_grid_lines(draw, w, h):
    """Subtle perspective grid on the bottom third."""
    horizon_y = int(h * 0.72)
    vp_x = w // 2
    grid_color_h = (0x52, 0x34, 0xb2, 18)   # blue, very transparent
    grid_color_v = (0x29, 0xb7, 0xe6, 14)   # cyan

    # Horizontal lines (get denser near horizon)
    n_h = 22
    for i in range(n_h):
        t = (i / (n_h - 1)) ** 1.8
        y = int(horizon_y + (h - horizon_y) * t)
        alpha = int(8 + 20 * (1 - t))
        draw.line([(0, y), (w, y)], fill=(*BLUE[:3], alpha), width=1)

    # Radiating vertical lines from vanishing point
    n_v = 30
    for i in range(n_v + 1):
        t = i / n_v
        end_x = int(t * w)
        alpha = int(6 + 14 * abs(t - 0.5) * 2)
        draw.line([(vp_x, horizon_y), (end_x, h)], fill=(*CYAN[:3], alpha), width=1)


def draw_circles(draw, w, h):
    """Large faint concentric arcs."""
    cx, cy = int(w * 0.72), int(h * 0.28)
    for r in range(60, 800, 55):
        alpha = max(4, 22 - r // 40)
        bb = [cx - r, cy - r, cx + r, cy + r]
        draw.ellipse(bb, outline=(*PURPLE[:3], alpha), width=1)

    # Second cluster
    cx2, cy2 = int(w * 0.12), int(h * 0.35)
    for r in range(40, 500, 48):
        alpha = max(3, 18 - r // 40)
        bb = [cx2 - r, cy2 - r, cx2 + r, cy2 + r]
        draw.ellipse(bb, outline=(*CYAN[:3], alpha), width=1)


def draw_diagonal_lines(draw, w, h):
    """Faint diagonal speed-lines from upper left."""
    for i in range(0, w + h, 80):
        x0 = i if i < w else 0
        y0 = 0 if i < w else i - w
        length = random.randint(200, 600)
        angle = math.radians(35)
        x1 = int(x0 + math.cos(angle) * length)
        y1 = int(y0 + math.sin(angle) * length)
        alpha = random.randint(4, 14)
        color = random.choice([BLUE_BR, CYAN, PURPLE])
        draw.line([(x0, y0), (x1, y1)], fill=(*color, alpha), width=1)


def draw_dots(draw, w, h):
    """Sparse glowing dot grid."""
    spacing = 90
    for gx in range(0, w, spacing):
        for gy in range(0, h, spacing):
            jx = gx + random.randint(-15, 15)
            jy = gy + random.randint(-15, 15)
            if random.random() < 0.35:
                r = random.randint(1, 3)
                color = random.choice([CYAN_BR, PURPLE, BLUE_BR, GREEN])
                alpha = random.randint(18, 55)
                draw.ellipse([jx-r, jy-r, jx+r, jy+r], fill=(*color, alpha))


def add_noise(img_np, strength=4):
    noise = np.random.randint(-strength, strength+1, img_np.shape, dtype=np.int16)
    out = np.clip(img_np.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return out


print("Generating base gradient...")
base = make_gradient(W, H)

print("Drawing detail layers...")
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
draw_grid_lines(draw, W, H)
draw_circles(draw, W, H)
draw_diagonal_lines(draw, W, H)
draw_dots(draw, W, H)

print("Compositing...")
base_rgba = base.convert("RGBA")
result = Image.alpha_composite(base_rgba, overlay).convert("RGB")

# Subtle blur for glow
blurred = result.filter(ImageFilter.GaussianBlur(radius=1.2))
result_np = np.array(result).astype(np.float32)
blurred_np = np.array(blurred).astype(np.float32)
# Blend: 85% sharp + 15% blurred for soft glow
final_np = (result_np * 0.85 + blurred_np * 0.15).astype(np.uint8)

# Film grain
final_np = add_noise(final_np, strength=5)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tokyo-night-bg.png")
print(f"Saving to {out_path}...")
Image.fromarray(final_np).save(out_path, optimize=False, compress_level=6)
print("Done.")
