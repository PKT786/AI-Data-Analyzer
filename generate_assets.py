"""
generate_assets.py
-------------------
One-time helper that creates the premium branding assets used on the
homepage:

    assets/logo/logo.png     - "PTH" gradient monogram badge
    assets/images/hero_banner.png - premium hero illustration: a floating
                                     analytics-dashboard mockup (KPI cards +
                                     bar/line/donut charts) on a soft
                                     gradient / glow backdrop

Run once (or whenever you want to regenerate the art):
    python3 generate_assets.py

Replace either file at any time with your own artwork - same
filenames, any reasonable size - and the app will pick it up.
"""

import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

random.seed(11)

# ---------------------------------------------------------------- palette --
NAVY_DARK = (9, 14, 32)
NAVY = (13, 27, 42)
INDIGO = (28, 45, 96)
VIOLET = (72, 58, 150)
TEAL = (20, 130, 130)
GOLD = (201, 168, 119)
GOLD_BRIGHT = (231, 196, 138)
GREEN = (46, 176, 122)
BLUE = (61, 133, 224)
WHITE = (255, 255, 255)
MIST = (214, 220, 232)


def _font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


POPPINS_BOLD = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
POPPINS_SEMI = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
POPPINS_MED = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
POPPINS_REG = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _vertical_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size, top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=_lerp(top, bottom, y / max(h - 1, 1)))
    return img


def _diagonal_gradient(size, top_left, bottom_right):
    w, h = size
    base = Image.new("RGB", size)
    px = base.load()
    for y in range(h):
        for x in range(0, w, 2):
            t = (x / w + y / h) / 2
            c = _lerp(top_left, bottom_right, t)
            px[x, y] = c
            if x + 1 < w:
                px[x + 1, y] = c
    return base


def _soft_glow(size, center, radius, color, alpha):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.5))


# ------------------------------------------------------------------- logo --
def make_logo(path="assets/logo/logo.png", size=320):
    """Premium gradient 'PTH' monogram badge with a soft ring + shadow."""

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    m = int(size * 0.06)
    sd.ellipse([m, m + size * 0.05, size - m, size - m + size * 0.05], fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.035))
    canvas.alpha_composite(shadow)

    badge = _diagonal_gradient((size, size), INDIGO, VIOLET).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([m, m, size - m, size - m], fill=255)
    canvas.paste(badge, (0, 0), mask)

    d = ImageDraw.Draw(canvas)

    sheen = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shd = ImageDraw.Draw(sheen)
    shd.ellipse([size * 0.10, size * 0.06, size * 0.75, size * 0.55], fill=(255, 255, 255, 28))
    sheen = sheen.filter(ImageFilter.GaussianBlur(size * 0.06))
    canvas.alpha_composite(sheen)

    ring_w = max(2, int(size * 0.012))
    d.ellipse([m + ring_w, m + ring_w, size - m - ring_w, size - m - ring_w],
              outline=GOLD + (230,), width=ring_w)

    font = _font(POPPINS_BOLD, int(size * 0.36))
    text = "PTH"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx, ty = (size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1] - size * 0.01
    d.text((tx, ty), text, font=font, fill=WHITE + (255,))

    line_w = size * 0.30
    ly = ty + th + size * 0.045
    d.rounded_rectangle(
        [size / 2 - line_w / 2, ly, size / 2 + line_w / 2, ly + max(2, size * 0.012)],
        radius=4, fill=GOLD_BRIGHT + (255,),
    )

    os.makedirs(os.path.dirname(path), exist_ok=True)
    canvas.save(path)
    print(f"wrote {path}")


# ------------------------------------------------------------------- hero --
def make_hero(path="assets/images/hero_banner.png", w=1800, h=760):
    """Premium SaaS-style hero: gradient backdrop with glow orbs and a
    floating analytics-dashboard mockup (KPI cards + bar/line/donut
    charts), suited to a wide homepage banner."""

    base = _vertical_gradient((w, h), NAVY_DARK, INDIGO).convert("RGBA")

    base.alpha_composite(_soft_glow((w, h), (w * 0.85, h * 0.15), int(h * 0.85), VIOLET, 130))
    base.alpha_composite(_soft_glow((w, h), (w * 0.08, h * 0.90), int(h * 0.75), TEAL, 70))
    base.alpha_composite(_soft_glow((w, h), (w * 0.45, h * -0.05), int(h * 0.60), GOLD, 55))

    # faint dot grid
    dots = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    step = 42
    for gy in range(0, h, step):
        for gx in range(0, w, step):
            dd.ellipse([gx, gy, gx + 2, gy + 2], fill=(255, 255, 255, 16))
    base.alpha_composite(dots)

    # decorative rings
    ring_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring_layer)
    for i, radius in enumerate([620, 470, 340]):
        alpha = 45 - i * 10
        cx, cy = w * 0.06, h * 0.05
        rd.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                   outline=GOLD + (alpha,), width=3)
    base.alpha_composite(ring_layer)

    # --------- headline text on the left third ---------
    td = ImageDraw.Draw(base)
    title_font = _font(POPPINS_BOLD, int(h * 0.135))
    sub_font = _font(POPPINS_REG, int(h * 0.052))
    tag_font = _font(POPPINS_SEMI, int(h * 0.040))

    tx = int(w * 0.045)
    ty = int(h * 0.24)
    td.text((tx, ty), "Turn Raw Data", font=title_font, fill=WHITE + (255,))
    td.text((tx, ty + int(h * 0.145)), "Into Decisions", font=title_font, fill=GOLD_BRIGHT + (255,))
    td.text((tx, ty + int(h * 0.145) * 2 + int(h * 0.01)),
             "AI cleaning \u2022 dashboards \u2022 insights \u2022 reports",
             font=sub_font, fill=MIST + (255,))

    # small feature chips under the tagline
    chips = ["\u2713 AI Insights", "\u2713 Premium Dashboards", "\u2713 One-Click Reports"]
    cx = tx
    cy = ty + int(h * 0.145) * 2 + int(h * 0.09)
    for label in chips:
        bb = td.textbbox((0, 0), label, font=tag_font)
        lw = bb[2] - bb[0] + int(w * 0.02)
        lh = int(h * 0.075)
        td.rounded_rectangle([cx, cy, cx + lw, cy + lh], radius=lh // 2,
                              outline=GOLD + (255,), width=2)
        td.text((cx + (lw - (bb[2] - bb[0])) / 2 - bb[0], cy + (lh - (bb[3] - bb[1])) / 2 - bb[1]),
                 label, font=tag_font, fill=GOLD_BRIGHT + (255,))
        cx += lw + int(w * 0.014)

    # ---------------- floating dashboard mockup (right two-thirds) --------
    card_w, card_h = int(w * 0.46), int(h * 0.86)
    pad = 36
    card_layer = Image.new("RGBA", (card_w + pad * 2, card_h + pad * 2), (0, 0, 0, 0))

    shadow = Image.new("RGBA", card_layer.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([pad + 12, pad + 22, pad + card_w + 12, pad + card_h + 22],
                          radius=26, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    card_layer.alpha_composite(shadow)

    cd = ImageDraw.Draw(card_layer)
    card_box = [pad, pad, pad + card_w, pad + card_h]
    cd.rounded_rectangle(card_box, radius=24, fill=(250, 251, 253, 255))

    # header bar
    header_h = int(card_h * 0.13)
    header_grad = _diagonal_gradient((card_w, header_h), NAVY, INDIGO).convert("RGBA")
    header_mask = Image.new("L", (card_w, header_h), 0)
    hmd = ImageDraw.Draw(header_mask)
    hmd.rounded_rectangle([0, 0, card_w, header_h + 26], radius=24, fill=255)
    hmd.rectangle([0, header_h - 26, card_w, header_h], fill=255)
    card_layer.paste(header_grad, (pad, pad), header_mask)

    dot_colors = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]
    for i, c in enumerate(dot_colors):
        r = header_h * 0.09
        cx_ = pad + int(card_w * 0.045) + i * int(r * 3)
        cy_ = pad + header_h // 2
        cd.ellipse([cx_ - r, cy_ - r, cx_ + r, cy_ + r], fill=c + (255,))

    header_title_font = _font(POPPINS_SEMI, int(header_h * 0.30))
    cd.text((pad + int(card_w * 0.045), pad + header_h * 0.58),
             "Executive Dashboard", font=header_title_font, fill=WHITE + (255,))

    live_w, live_h = int(card_w * 0.14), int(header_h * 0.42)
    lx1 = pad + card_w - int(card_w * 0.05) - live_w
    ly1 = pad + (header_h - live_h) // 2
    cd.rounded_rectangle([lx1, ly1, lx1 + live_w, ly1 + live_h], radius=live_h // 2,
                          fill=GREEN + (255,))
    live_font = _font(POPPINS_SEMI, int(live_h * 0.5))
    lb = cd.textbbox((0, 0), "LIVE", font=live_font)
    cd.text((lx1 + (live_w - (lb[2] - lb[0])) / 2 - lb[0],
              ly1 + (live_h - (lb[3] - lb[1])) / 2 - lb[1]),
             "LIVE", font=live_font, fill=WHITE + (255,))

    body_x = pad + int(card_w * 0.045)
    body_w = card_w - int(card_w * 0.09)
    body_y = pad + header_h + int(card_h * 0.035)

    # KPI mini-cards row
    kpi_h = int(card_h * 0.13)
    kpi_gap = int(card_w * 0.025)
    kpi_w = (body_w - kpi_gap * 2) / 3
    kpi_data = [
        ("Revenue", "$482K", GREEN),
        ("Growth", "+18.4%", BLUE),
        ("Churn", "2.1%", GOLD),
    ]
    kpi_label_font = _font(POPPINS_REG, int(kpi_h * 0.24))
    kpi_value_font = _font(POPPINS_BOLD, int(kpi_h * 0.36))
    for i, (label, value, color) in enumerate(kpi_data):
        kx = body_x + i * (kpi_w + kpi_gap)
        cd.rounded_rectangle([kx, body_y, kx + kpi_w, body_y + kpi_h], radius=12,
                              fill=(244, 246, 250, 255))
        cd.rectangle([kx, body_y, kx + int(kpi_w * 0.045), body_y + kpi_h], fill=color + (255,))
        cd.text((kx + kpi_w * 0.12, body_y + kpi_h * 0.16), label, font=kpi_label_font,
                 fill=(110, 118, 138, 255))
        cd.text((kx + kpi_w * 0.12, body_y + kpi_h * 0.48), value, font=kpi_value_font,
                 fill=(30, 38, 60, 255))

    chart_y = body_y + kpi_h + int(card_h * 0.035)
    chart_h = card_h - (chart_y - pad) - int(card_h * 0.04)
    bar_w = body_w * 0.56
    donut_w = body_w - bar_w - kpi_gap

    # bar chart panel
    cd.rounded_rectangle([body_x, chart_y, body_x + bar_w, chart_y + chart_h], radius=12,
                          fill=(244, 246, 250, 255))
    bars = [0.35, 0.55, 0.42, 0.72, 0.60, 0.88, 0.68]
    n = len(bars)
    inner_pad = bar_w * 0.06
    slot = (bar_w - inner_pad * 2) / n
    bar_colors = [BLUE, GREEN, GOLD, VIOLET]
    base_y = chart_y + chart_h - inner_pad
    max_bar_h = chart_h - inner_pad * 2.2
    for i, frac in enumerate(bars):
        bx0 = body_x + inner_pad + i * slot + slot * 0.18
        bx1 = body_x + inner_pad + i * slot + slot * 0.82
        by1 = base_y
        by0 = base_y - max_bar_h * frac
        cd.rounded_rectangle([bx0, by0, bx1, by1], radius=6,
                              fill=bar_colors[i % len(bar_colors)] + (255,))

    # donut chart panel
    donut_x = body_x + bar_w + kpi_gap
    cd.rounded_rectangle([donut_x, chart_y, donut_x + donut_w, chart_y + chart_h], radius=12,
                          fill=(244, 246, 250, 255))
    donut_cx = donut_x + donut_w / 2
    donut_cy = chart_y + chart_h / 2 - chart_h * 0.05
    donut_r = min(donut_w, chart_h) * 0.32
    segments = [(0, 130, BLUE), (130, 230, GREEN), (230, 300, GOLD), (300, 360, VIOLET)]
    for start, end, color in segments:
        cd.pieslice([donut_cx - donut_r, donut_cy - donut_r, donut_cx + donut_r, donut_cy + donut_r],
                     start - 90, end - 90, fill=color + (255,))
    hole_r = donut_r * 0.55
    cd.ellipse([donut_cx - hole_r, donut_cy - hole_r, donut_cx + hole_r, donut_cy + hole_r],
                fill=(250, 251, 253, 255))

    legend_font = _font(POPPINS_REG, int(chart_h * 0.075))
    legend_y = donut_cy + donut_r + chart_h * 0.06
    legend_items = [("Sales", BLUE), ("Mktg", GREEN), ("Ops", GOLD), ("R&D", VIOLET)]
    lx = donut_x + donut_w * 0.08
    for label, color in legend_items:
        r = chart_h * 0.02
        cd.ellipse([lx, legend_y - r, lx + r * 2, legend_y + r], fill=color + (255,))
        cd.text((lx + r * 2.6, legend_y - r * 1.4), label, font=legend_font, fill=(90, 98, 118, 255))
        bb = cd.textbbox((0, 0), label, font=legend_font)
        lx += r * 2.6 + (bb[2] - bb[0]) + donut_w * 0.05

    rotated = card_layer.rotate(-3.2, resample=Image.BICUBIC, expand=True)
    rx = int(w * 0.50)
    ry = int(h * 0.06)
    base.alpha_composite(rotated, (rx, ry))

    # floating particles
    particles = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(particles)
    for _ in range(26):
        px_ = random.uniform(w * 0.02, w * 0.46)
        py_ = random.uniform(h * 0.05, h * 0.95)
        s = random.uniform(4, 12)
        alpha = random.randint(50, 160)
        if random.random() < 0.5:
            pd.rectangle([px_, py_, px_ + s, py_ + s], fill=GOLD_BRIGHT + (alpha,))
        else:
            pd.ellipse([px_, py_, px_ + s, py_ + s], fill=(255, 255, 255, int(alpha * 0.55)))
    base.alpha_composite(particles)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    base.convert("RGB").save(path, quality=95)
    print(f"wrote {path}")


if __name__ == "__main__":
    os.makedirs("assets/logo", exist_ok=True)
    os.makedirs("assets/images", exist_ok=True)
    make_logo()
    make_hero()
