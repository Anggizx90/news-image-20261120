#!/usr/bin/env python3
"""Draw THE WORLD TODAY, Friday 20 November 2026, as a 1024x1024 front page.

Run with Pillow installed:  python3 draw_poster.py
Writes entry.png next to this file. Every picture on the page is drawn
from simple shapes; no photographs and no network are used anywhere.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (168, 32, 26)
NAVY = (28, 38, 66)
GOLD = (201, 162, 39)
MUTED = (90, 86, 76)
SKY = (214, 228, 238)


def pick_font(bold, serif, size):
    """Return a TrueType font, falling back through the usual system paths."""
    if serif:
        names = ["DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf"] if bold else ["DejaVuSerif.ttf"]
    else:
        names = ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"] if bold else ["DejaVuSans.ttf"]
    for name in names:
        for folder in ("/usr/share/fonts/truetype/dejavu",
                       "/usr/share/fonts/truetype/liberation",
                       "/usr/share/fonts/truetype"):
            path = os.path.join(folder, name)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap_words(draw, text, font, width):
    """Split text into lines that fit inside width pixels."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def put_text(draw, x, y, text, font, width, fill=INK, gap=4, align="left"):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap_words(draw, text, font, width):
        if align == "center":
            lx = x + (width - draw.textlength(line, font=font)) // 2
        else:
            lx = x
        draw.text((lx, y), line, font=font, fill=fill)
        y += font.size + gap
    return y


def rule(draw, x0, y, x1, colour=INK, thick=2):
    draw.line([(x0, y), (x1, y)], fill=colour, width=thick)


# ---- small spot illustrations, one per story box (72 x 72) -----------------

def icon_scales(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=(226, 232, 240))
    d.line([(x + 36, y + 12), (x + 36, y + 58)], fill=INK, width=3)
    d.line([(x + 12, y + 20), (x + 60, y + 20)], fill=INK, width=3)
    d.polygon([(x + 36, y + 8), (x + 30, y + 16), (x + 42, y + 16)], fill=GOLD)
    for cx in (x + 14, x + 58):
        d.polygon([(cx - 9, y + 34), (cx + 9, y + 34), (cx, y + 46)], fill=GOLD)
        d.line([(cx, y + 20), (cx, y + 34)], fill=INK, width=2)
    d.rectangle([x + 24, y + 56, x + 48, y + 62], fill=INK)


def icon_bridge(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=SKY)
    d.rectangle([x, y + 52, x + 72, y + 72], fill=(70, 110, 140))
    d.arc([x + 8, y + 8, x + 64, y + 60], 180, 360, fill=RED, width=5)
    for px in (x + 16, x + 32, x + 48):
        d.line([(px, y + 34), (px, y + 52)], fill=INK, width=3)
    d.rectangle([x + 4, y + 50, x + 68, y + 56], fill=INK)
    d.ellipse([x + 52, y + 12, x + 62, y + 22], fill=(255, 170, 40))
    for dx, dy in ((-6, 0), (6, 0), (0, -6), (0, 6)):
        d.line([(x + 57 + dx, y + 17 + dy), (x + 57 - dx, y + 17 - dy)],
               fill=(255, 170, 40), width=2)


def icon_drone(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=NAVY)
    d.rectangle([x + 10, y + 46, x + 62, y + 72], fill=(52, 66, 96))
    d.rectangle([x + 22, y + 34, x + 50, y + 72], fill=(70, 84, 118))
    d.ellipse([x + 48, y + 8, x + 64, y + 24], fill=GOLD)
    d.line([(x + 18, y + 14), (x + 34, y + 30)], fill=(255, 90, 60), width=4)
    d.line([(x + 34, y + 14), (x + 18, y + 30)], fill=(255, 90, 60), width=4)
    d.ellipse([x + 20, y + 16, x + 32, y + 28], fill=(220, 225, 235))
    d.text((x + 6, y + 56), "KYIV", font=pick_font(True, False, 13), fill=(255, 255, 255))


def icon_tank(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=(238, 226, 196))
    d.polygon([(x + 8, y + 48), (x + 20, y + 48), (x + 16, y + 58), (x + 4, y + 58)],
              fill=(120, 90, 40))
    d.rectangle([x + 14, y + 30, x + 48, y + 50], fill=(74, 92, 58))
    d.rectangle([x + 44, y + 36, x + 68, y + 41], fill=(74, 92, 58))
    d.rectangle([x + 10, y + 50, x + 56, y + 62], fill=(40, 44, 34))
    for wx in (16, 28, 40, 50):
        d.ellipse([x + wx, y + 53, x + wx + 7, y + 60], fill=(200, 200, 190))
    d.text((x + 6, y + 6), "GAZA", font=pick_font(True, False, 13), fill=RED)


def icon_tower(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=NAVY)
    d.polygon([(x + 30, y + 8), (x + 44, y + 8), (x + 50, y + 64), (x + 24, y + 64)],
              fill=(150, 175, 205))
    for wy in (16, 26, 36, 46):
        d.line([(x + 29, y + wy), (x + 45, y + wy)], fill=GOLD, width=2)
    d.line([(x + 8, y + 20), (x + 58, y + 44)], fill=(255, 120, 60), width=3)
    d.ellipse([x + 56, y + 40, x + 66, y + 50], fill=(255, 170, 40))
    d.text((x + 4, y + 58), "RIYADH", font=pick_font(True, False, 11), fill=(255, 255, 255))


def icon_cyclone(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=SKY)
    cx, cy = x + 36, y + 40
    for r in (26, 19, 12):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=NAVY, width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    d.text((x + 6, y + 4), "110 km/h", font=pick_font(True, False, 12), fill=NAVY)
    d.rectangle([x, y + 64, x + 72, y + 72], fill=(70, 110, 140))


def icon_chart(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=(235, 240, 235))
    bars = [14, 22, 18, 30, 38, 48]
    for i, h in enumerate(bars):
        bx = x + 6 + i * 11
        colour = RED if i == len(bars) - 1 else NAVY
        d.rectangle([bx, y + 62 - h, bx + 8, y + 62], fill=colour)
    d.line([(x + 6, y + 14), (x + 66, y + 6)], fill=(200, 60, 40), width=3)
    d.polygon([(x + 66, y + 6), (x + 58, y + 4), (x + 60, y + 12)], fill=(200, 60, 40))
    d.text((x + 4, y + 64), "", font=pick_font(True, False, 10), fill=INK)


def icon_drought(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=(240, 222, 180))
    d.ellipse([x + 46, y + 6, x + 66, y + 26], fill=(255, 170, 40))
    d.text((x + 4, y + 4), "DROUGHT", font=pick_font(True, False, 11), fill=(140, 90, 20))
    for i in range(5):
        lx = x + 10 + i * 12
        d.line([(lx, y + 66), (lx + 5, y + 44)], fill=(150, 110, 50), width=3)
        d.line([(lx + 5, y + 44), (lx + 10, y + 66)], fill=(150, 110, 50), width=3)


def icon_court(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=(226, 232, 240))
    d.polygon([(x + 36, y + 8), (x + 8, y + 26), (x + 64, y + 26)], fill=INK)
    for px in (14, 28, 42, 56):
        d.rectangle([x + px - 3, y + 30, x + px + 3, y + 54], fill=INK)
    d.rectangle([x + 6, y + 54, x + 66, y + 60], fill=INK)
    d.rectangle([x + 10, y + 62, x + 62, y + 66], fill=INK)
    d.text((x + 4, y + 68), "", font=pick_font(True, False, 10), fill=INK)


def icon_missiles(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=NAVY)
    for mx in (14, 32, 50):
        d.polygon([(x + mx, y + 8), (x + mx - 5, y + 20), (x + mx + 5, y + 20)],
                  fill=(220, 225, 235))
        d.rectangle([x + mx - 5, y + 20, x + mx + 5, y + 52], fill=(200, 205, 215))
        d.polygon([(x + mx - 2, y + 52), (x + mx + 2, y + 52), (x + mx, y + 62)],
                  fill=GOLD)
    d.text((x + 8, y + 62), "1,500+", font=pick_font(True, False, 12), fill=(255, 255, 255))


def icon_atom(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=(235, 238, 228))
    cx, cy = x + 36, y + 38
    for tilt in (0.0, 1.05, 2.09):
        pts = []
        for step in range(41):
            ang = step * 2 * math.pi / 40
            ex = 26 * math.cos(ang)
            ey = 11 * math.sin(ang)
            rx = ex * math.cos(tilt) - ey * math.sin(tilt)
            ry = ex * math.sin(tilt) + ey * math.cos(tilt)
            pts.append((cx + rx, cy + ry))
        d.line(pts, fill=NAVY, width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    d.text((x + 4, y + 4), "YONGBYON", font=pick_font(True, False, 10), fill=NAVY)


def icon_cricket(d, x, y):
    d.rectangle([x, y, x + 72, y + 72], fill=(226, 240, 214))
    d.rectangle([x + 12, y + 10, x + 20, y + 58], fill=(190, 150, 90))
    d.rectangle([x + 13, y + 58, x + 19, y + 66], fill=(120, 85, 40))
    d.ellipse([x + 44, y + 12, x + 62, y + 30], fill=RED)
    d.rectangle([x + 48, y + 32, x + 54, y + 38], fill=RED)
    for bx in (40, 48, 56):
        d.rectangle([bx, y + 52, bx + 5, y + 62], fill=GOLD)
    for sx in (26, 32, 38):
        d.rectangle([x + sx, y + 44, x + sx + 3, y + 66], fill=(210, 180, 110))
    d.text((x + 30, y + 62), "146*", font=pick_font(True, False, 13), fill=INK)


ICONS = {
    "scales": icon_scales, "bridge": icon_bridge, "drone": icon_drone,
    "tank": icon_tank, "tower": icon_tower, "cyclone": icon_cyclone,
    "chart": icon_chart, "drought": icon_drought, "court": icon_court,
    "missiles": icon_missiles, "atom": icon_atom, "cricket": icon_cricket,
}


# ---- page sections ---------------------------------------------------------

def draw_masthead(d):
    title = pick_font(True, True, 76)
    d.text((PAGE // 2, 14), "THE WORLD TODAY", font=title, fill=INK, anchor="ma")
    rule(d, 28, 100, 996, INK, 4)
    rule(d, 28, 106, 996, INK, 1)
    date_font = pick_font(True, False, 17)
    tag_font = pick_font(False, False, 15)
    d.text((28, 114), "FRIDAY, 20 NOVEMBER 2026", font=date_font, fill=INK)
    tag = "ONE DAY  •  ONE PAGE  •  ALL THE NEWS"
    d.text((996, 114), tag, font=tag_font, fill=MUTED, anchor="ra")
    rule(d, 28, 140, 996, INK, 2)


def draw_summit_art(d, x, y, w, h):
    """Night skyline in Shenzhen with three flags and three leaders."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sh in ((0, 150), (70, 190), (150, 130), (230, 175), (310, 140), (370, 165)):
        d.rectangle([x + sx, y + h - sh - 70, x + sx + 55, y + h - 70],
                    fill=(52, 66, 96))
    for wx in range(x + 14, x + w - 10, 26):
        for wy in range(y + 16, y + h - 90, 24):
            if (wx + wy) % 52 == 0:
                d.rectangle([wx, wy, wx + 7, wy + 10], fill=(255, 214, 120))
    d.text((x + 10, y + 8), "SHENZHEN  •  APEC SUMMIT", font=pick_font(True, False, 15),
           fill=GOLD)
    # three flags on poles
    poles = [(x + 55, "US"), (x + 195, "CN"), (x + 335, "RU")]
    flag_cols = {"US": [(200, 40, 50), (255, 255, 255), (40, 60, 140)],
                 "CN": [(222, 40, 30)], "RU": [(255, 255, 255), (40, 80, 200), (220, 40, 40)]}
    for px, code in poles:
        d.line([(px, y + 52), (px, y + 190)], fill=(220, 220, 210), width=3)
        if code == "US":
            for i in range(4):
                col = (200, 40, 50) if i % 2 == 0 else (255, 255, 255)
                d.rectangle([px + 3, y + 52 + i * 9, px + 73, y + 61 + i * 9], fill=col)
            d.rectangle([px + 3, y + 52, px + 30, y + 70], fill=(40, 60, 140))
            continue
        cols = flag_cols[code]
        fh = 34 // len(cols)
        for i, col in enumerate(cols):
            d.rectangle([px + 3, y + 52 + i * fh, px + 73, y + 52 + (i + 1) * fh], fill=col)
        if code == "CN":
            d.ellipse([px + 12, y + 58, px + 26, y + 72], fill=GOLD)
    # table first, then the three leaders sit behind it, names on its front
    d.rectangle([x, y + h - 70, x + w, y + h], fill=(122, 82, 32))
    d.rectangle([x, y + h - 70, x + w, y + h - 64], fill=(150, 104, 44))
    names = ["TRUMP", "XI", "PUTIN"]
    suits = [(38, 48, 88), (88, 40, 40), (34, 66, 48)]
    for i, (name, suit) in enumerate(zip(names, suits)):
        cx = x + 90 + i * 140
        d.ellipse([cx - 24, y + 132, cx + 24, y + 180], fill=(232, 200, 160))
        d.pieslice([cx - 34, y + 180, cx + 34, y + 236], 180, 360, fill=suit)
        d.text((cx, y + h - 58), name, font=pick_font(True, False, 15),
               fill=(255, 255, 255), anchor="ma")


def draw_lead(d):
    kick = pick_font(True, False, 15)
    head = pick_font(True, True, 40)
    body = pick_font(False, True, 19)
    small = pick_font(False, False, 15)
    d.text((28, 152), "SUMMIT IN SHENZHEN  •  APEC", font=kick, fill=RED)
    y = put_text(d, 28, 176, "Trump, Xi and Putin\nmeet face to face",
                 head, 520, gap=2)
    y = put_text(d, 28, y + 8,
                 "The three leaders hold their first-ever three-way talks in "
                 "China, on nuclear arms control, energy and the wars in "
                 "Ukraine and the Middle East — and issue a four-point "
                 "peace declaration.", body, 520, gap=5)
    bullets = [
        "Four-point peace declaration issued — but the details are thin.",
        "Putin: no agreements after the bridge strikes.",
        "European allies meet in Berlin, say they are ready for talks with Russia.",
    ]
    y += 6
    for item in bullets:
        d.ellipse([30, y + 6, 38, y + 14], fill=RED)
        y = put_text(d, 46, y, item, small, 500, gap=4) + 2
    draw_summit_art(d, 576, 152, 420, 286)
    rule(d, 28, 452, 996, INK, 3)


STORIES = [
    ("WORLD COURT  •  THE HAGUE", "Myanmar guilty of Rohingya genocide",
     "First state ever found liable by the World Court: 9–6 verdict, "
     "cheered by Rohingya refugees.", "scales"),
    ("UKRAINE  •  CRIMEA", "Crimean Bridge hit a third time",
     "Neptune missiles strike the rail span and halt trains; the road arch "
     "fell into the strait on Tuesday.", "bridge"),
    ("UKRAINE  •  KYIV", "Drone raid hits Kyiv embassies",
     "One killed, five hurt as a Russian drone attack damages two embassies "
     "and a cathedral.", "drone"),
    ("GAZA  •  CEASEFIRE", "Israeli tanks cross Gaza line",
     "First ground raid beyond the ceasefire line since the October 2025 "
     "truce; 1,600+ killed since.", "tank"),
    ("YEMEN  •  SAUDI ARABIA", "Houthi missile hits Riyadh tower",
     "Windows blown out across seven floors of the PIF Tower, the kingdom's "
     "tallest; no injuries.", "tower"),
    ("WEATHER  •  INDIA", "Cyclone Akvan makes landfall",
     "More than 300,000 evacuated as the storm crosses the Andhra "
     "Pradesh–Odisha coast.", "cyclone"),
    ("TECH  •  MARKETS", "Anthropic's record IPO closes",
     "ANT ends its first day at $97.17, up 17% on the $83 price; the $81.3bn "
     "listing is the largest ever.", "chart"),
    ("PACIFIC  •  CLIMATE", "Fiji declares drought disaster",
     "A national state of disaster as El Niño drought drains water supplies; "
     "F$20m set aside.", "drought"),
    ("SOUTH KOREA  •  SEOUL", "Top court overturns Han's term",
     "Supreme Court sends ex-PM Han Duck-soo's martial-law case back for "
     "retrial; other findings stand.", "court"),
    ("MIDDLE EAST  •  IRAN", "Iran may still hold 2,500 missiles",
     "US intelligence puts Tehran's arsenal at 1,500–2,500 — a low-confidence "
     "estimate.", "missiles"),
    ("NORTH KOREA  •  NUCLEAR", "Pyongyang expands enrichment",
     "UN watchdog reports North Korea is enlarging its uranium enrichment "
     "plant at Yongbyon.", "atom"),
    ("SPORT  •  CRICKET", "Nicholls 146* as NZ pass 300",
     "Phillips falls for 118 as New Zealand reach 317 for 6 at lunch on day "
     "two in Wellington.", "cricket"),
]


def draw_grid(d):
    kick = pick_font(True, False, 12)
    head = pick_font(True, True, 17)
    body = pick_font(False, False, 12)
    top, left = 460, 28
    cw, ch, gap = 304, 120, 8
    for i, (kicker, title, text, icon) in enumerate(STORIES):
        row, col = divmod(i, 3)
        x = left + col * (cw + gap)
        y = top + row * (ch + gap)
        rule(d, x, y, x + cw, RED, 3)
        d.text((x, y + 6), kicker, font=kick, fill=RED)
        hy = put_text(d, x, y + 24, title, head, cw - 82, gap=1)
        put_text(d, x, hy + 2, text, body, cw - 82, gap=2)
        ICONS[icon](d, x + cw - 72, y + 24)


def draw_footer(d):
    rule(d, 28, 972, 996, INK, 3)
    strip = ("ALSO IN THE NEWS:  S&P 500 falls 2% for a fifth straight day  •  "
             "California opens a probe into Nvidia's China AI-chip sales  •  "
             "Trump pardons baseball's Pete Rose  •  COP31 closes in Antalya")
    put_text(d, 28, 980, strip, pick_font(True, False, 13), 968, gap=2)
    note = ("Sources: Reuters, AP, AFP, The Wall Street Journal, IAEA, India "
            "Meteorological Dept, SEC filings — all stories reported 19–20 November 2026.")
    d.text((28, 1008), note, font=pick_font(False, False, 11), fill=MUTED)


def build_page():
    canvas = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(canvas)
    draw_masthead(d)
    draw_lead(d)
    draw_grid(d)
    draw_footer(d)
    return canvas


if __name__ == "__main__":
    build_page().save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote entry.png")
