#!/usr/bin/env python3
"""Render the news-image-20261125 poster: a one-page newspaper front page
summarising the world news of Wednesday 25 November 2026.

Flat vector style, drawn entirely with PIL shapes. No external images,
no network, fully deterministic: the same input always produces the
same PNG bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (245, 240, 230)
INK = (20, 20, 20)
RULE = (20, 20, 20)
PANEL_BG = (255, 255, 255)
PANEL_BORDER = (30, 30, 30)
MUTED = (70, 70, 70)
ACCENT = (178, 34, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_TITLE = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_BODY = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


# ---------------------------------------------------------------- pictograms
def pic_ships(d, x0, y0, x1, y1, fg):
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    # sea waves
    for i, wy in enumerate((cy + 18, cy + 28, cy + 38)):
        d.arc([x0 + 14, wy - 8, x0 + 60, wy + 8], 0, 180, fill=fg, width=3)
        d.arc([x1 - 60, wy - 8, x1 - 14, wy + 8], 0, 180, fill=fg, width=3)
    # hull
    d.polygon([(cx - 52, cy - 2), (cx + 52, cy - 2), (cx + 38, cy + 16),
               (cx - 38, cy + 16)], fill=fg)
    # mast + flag
    d.line([(cx, cy - 2), (cx, cy - 34)], fill=fg, width=4)
    d.polygon([(cx, cy - 34), (cx + 20, cy - 28), (cx, cy - 22)], fill=(255, 200, 60))
    # drone above
    dx, dy = cx + 66, cy - 26
    d.rectangle([dx - 8, dy - 4, dx + 8, dy + 4], fill=fg)
    d.ellipse([dx - 18, dy - 10, dx - 8, dy - 2], outline=fg, width=2)
    d.ellipse([dx + 8, dy - 10, dx + 18, dy - 2], outline=fg, width=2)


def pic_globe(d, x0, y0, x1, y1, fg):
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    r = 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fg, width=4)
    d.arc([cx - 14, cy - r, cx + 14, cy + r], 0, 360, fill=fg, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=fg, width=3)
    # crack
    d.line([(cx - 6, cy - 26), (cx + 4, cy - 10), (cx - 4, cy + 4),
            (cx + 8, cy + 18), (cx + 2, cy + 28)], fill=(255, 90, 60), width=4)
    # small sun
    sx, sy = x1 - 40, y0 + 18
    d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(255, 200, 60))
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([(sx + 12 * math.cos(a), sy + 12 * math.sin(a)),
                (sx + 18 * math.cos(a), sy + 18 * math.sin(a))],
               fill=(255, 200, 60), width=2)


def pic_tower(d, x0, y0, x1, y1, fg):
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    # tower
    d.rectangle([cx - 16, cy - 26, cx + 16, cy + 40], fill=fg)
    d.line([(cx, cy - 26), (cx, cy - 42)], fill=fg, width=3)
    d.ellipse([cx - 3, cy - 46, cx + 3, cy - 40], fill=(255, 60, 40))
    for wy in range(cy - 18, cy + 36, 12):
        for wx in (cx - 10, cx + 2):
            d.rectangle([wx, wy, wx + 6, wy + 6], fill=(255, 220, 120))
    # explosion starburst at the top
    ex, ey = cx + 52, cy - 22
    pts = []
    import math
    for i in range(12):
        a = math.radians(i * 30)
        rr = 20 if i % 2 == 0 else 8
        pts.append((ex + rr * math.cos(a), ey + rr * math.sin(a)))
    d.polygon(pts, fill=(255, 200, 40))
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 90, 40))


def pic_gavel(d, x0, y0, x1, y1, fg):
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    # handle
    d.rectangle([cx - 48, cy - 2, cx + 30, cy + 6], fill=fg)
    # head
    d.rectangle([cx + 30, cy - 16, cx + 56, cy + 20], fill=fg)
    d.rectangle([cx + 22, cy - 12, cx + 30, cy + 16], fill=fg)
    # sound block
    d.rectangle([cx - 48, cy + 26, cx - 8, cy + 34], fill=fg)
    # document
    d.rectangle([cx - 62, cy - 34, cx - 30, cy - 6], outline=fg, width=3)
    d.line([(cx - 56, cy - 26), (cx - 36, cy - 26)], fill=fg, width=2)
    d.line([(cx - 56, cy - 18), (cx - 36, cy - 18)], fill=fg, width=2)


def pic_monitor(d, x0, y0, x1, y1, fg):
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    d.rectangle([cx - 44, cy - 30, cx + 44, cy + 22], outline=fg, width=4)
    d.rectangle([cx - 38, cy - 24, cx + 38, cy + 16], fill=(200, 30, 30))
    fnt = font(F_BOLD, 40)
    d.text((cx - 9, cy - 24), "!", font=fnt, fill=(255, 255, 255))
    d.line([(cx, cy + 22), (cx, cy + 34)], fill=fg, width=5)
    d.line([(cx - 22, cy + 36), (cx + 22, cy + 36)], fill=fg, width=5)


def pic_rocket(d, x0, y0, x1, y1, fg):
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    # flame
    d.polygon([(cx - 10, cy + 26), (cx + 10, cy + 26), (cx, cy + 46)],
              fill=(255, 140, 0))
    d.polygon([(cx - 5, cy + 26), (cx + 5, cy + 26), (cx, cy + 38)],
              fill=(255, 220, 60))
    # body
    d.rectangle([cx - 12, cy - 26, cx + 12, cy + 26], fill=fg)
    d.polygon([(cx - 12, cy - 26), (cx + 12, cy - 26), (cx, cy - 44)],
              fill=(255, 60, 40))
    # fins
    d.polygon([(cx - 12, cy + 10), (cx - 26, cy + 30), (cx - 12, cy + 26)],
              fill=(255, 60, 40))
    d.polygon([(cx + 12, cy + 10), (cx + 26, cy + 30), (cx + 12, cy + 26)],
              fill=(255, 60, 40))
    # window
    d.ellipse([cx - 6, cy - 12, cx + 6, cy + 0], fill=(160, 220, 255))
    # stars
    for sx, sy in ((x0 + 24, y0 + 16), (x1 - 26, y0 + 26), (x0 + 30, y1 - 18)):
        d.polygon([(sx, sy - 6), (sx + 2, sy - 2), (sx + 6, sy),
                   (sx + 2, sy + 2), (sx, sy + 6), (sx - 2, sy + 2),
                   (sx - 6, sy), (sx - 2, sy - 2)], fill=(255, 220, 120))


# ---------------------------------------------------------------- stories
STORIES = [
    ("UKRAINE HITS RUSSIAN SHIPS",
     "Kyiv's drones struck a Russian cargo ship in the Gulf of Finland and a "
     "warship off Libya; Zelenskiy confirmed Ukraine did it, Norway urged "
     "caution, Moscow calls the attacks \u201cterrorism\u201d.",
     (31, 58, 95), pic_ships),
    ("COP31 COLLAPSES",
     "The UN climate summit in Antalya ends with no final deal after oil and "
     "gas producers block fossil-fuel phase-out language.",
     (14, 107, 92), pic_globe),
    ("HOUTHI STRIKE ON RIYADH",
     "Attack hits Riyadh's tallest tower; 11 wounded, including two Indians; "
     "second strike on the Saudi capital in days.",
     (185, 119, 14), pic_tower),
    ("HUAWEI CONVICTED",
     "A US federal jury convicts China's Huawei in a sprawling criminal trial "
     "over its Iran business and trade-secret theft.",
     (55, 71, 79), pic_gavel),
    ("MICROSOFT \u201cCODE RED\u201d",
     "Microsoft declares an internal \u201cCode Red\u201d after a major "
     "historic outage.",
     (192, 57, 43), pic_monitor),
    ("SHENZHOU-24 LAUNCHES",
     "China launches Shenzhou-24 to the Tiangong station carrying the first "
     "Pakistani astronaut.",
     (26, 82, 118), pic_rocket),
]


def draw_panel(d, x0, y0, x1, y1, headline, summary, band, pic):
    d.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    band_h = 84
    d.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + band_h], fill=band)
    pic(d, x0, y0 + 2, x1, y0 + band_h, (255, 255, 255))
    tx = x0 + 16
    tw = x1 - x0 - 32
    y = y0 + band_h + 12
    f_head = font(F_BOLD, 25)
    for line in wrap(d, headline, f_head, tw):
        d.text((tx, y), line, font=f_head, fill=INK)
        y += 30
    y += 2
    f_sum = font(F_BODY, 16)
    for line in wrap(d, summary, f_sum, tw):
        d.text((tx, y), line, font=f_sum, fill=MUTED)
        y += 21


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    cx = W // 2
    f_title = font(F_TITLE, 76)
    draw_centered(d, cx, 22, "THE WORLD TODAY", f_title)
    f_date = font(F_BOLD, 30)
    draw_centered(d, cx, 112, "WEDNESDAY 25 NOVEMBER 2026", f_date, fill=ACCENT)
    d.line([(32, 158), (W - 32, 158)], fill=RULE, width=3)
    d.line([(32, 164), (W - 32, 164)], fill=RULE, width=1)

    # ---- grid: 2 columns x 3 rows ----
    gx, gy = 32, 180
    gw = W - 2 * gx
    gh = 992 - gy
    cols, rows = 2, 3
    gutter = 16
    pw = (gw - gutter) // cols
    ph = (gh - gutter * (rows - 1)) // rows
    for i, (headline, summary, band, pic) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x0 = gx + c * (pw + gutter)
        y0 = gy + r * (ph + gutter)
        draw_panel(d, x0, y0, x0 + pw, y0 + ph, headline, summary, band, pic)

    # ---- footer ----
    f_foot = font(F_BODY, 14)
    draw_centered(d, cx, 1002, "Drawn entirely in code  \u00b7  No photographs  \u00b7  Six stories, one image",
                  f_foot, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
