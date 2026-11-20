#!/usr/bin/env python3
"""Draw THE WORLD TODAY - a 1024x1024 newspaper front page summing up
Friday 20 November 2026, and write it to entry.png next to this script.

Every story below was reported on 19-20 November 2026 and carried as
the morning's news on Friday 20 November 2026. Sources are listed in
README.md and in the footer of the page itself. All artwork is drawn
with Pillow shapes - no photographs, no network, no randomness.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (253, 252, 247)
INK = (18, 18, 18)
RED = (163, 18, 31)
BLUE = (28, 61, 110)
GOLD = (176, 132, 40)
GREY = (90, 90, 86)
RULE = (18, 18, 18)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, f, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, max_w, leading, fill=INK):
    """Draw wrapped paragraph; return y just below the last line."""
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def rule(d, x0, y, x1, w=2):
    d.line([(x0, y), (x1, y)], fill=RULE, width=w)


# ---------------------------------------------------------------- illustrations
def ill_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    cx, cy = x + w // 2, y + h // 2 + 6
    d.line([(cx, cy - 26), (cx, cy + 22)], fill=INK, width=4)
    d.line([(cx - 30, cy - 26), (cx + 30, cy - 26)], fill=INK, width=4)
    for s in (-1, 1):
        px = cx + s * 30
        d.line([(px, cy - 26), (px, cy - 8)], fill=INK, width=2)
        d.polygon([(px - 14, cy - 8), (px + 14, cy - 8), (px, cy + 8)], fill=GOLD)
    d.rectangle([cx - 16, cy + 22, cx + 16, cy + 26], fill=INK)
    d.text((x + 6, y + 4), "ICJ", font=SANS_B(11), fill=BLUE)


def ill_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 224, 238))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(64, 110, 150))
    d.line([(x + 4, y + h - 22), (x + w - 4, y + h - 22)], fill=INK, width=5)
    for bx in (x + 10, x + w // 2 - 3, x + w - 16):
        d.rectangle([bx, y + h - 44, bx + 6, y + h - 22], fill=INK)
    d.arc([x + 8, y + 8, x + w - 8, y + h - 8], 180, 360, fill=RED, width=4)
    cx, cy = x + w - 22, y + 18
    for dx, dy in [(0, -12), (9, -4), (12, 6), (5, 12), (-5, 12), (-12, 6), (-9, -4)]:
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=(255, 170, 0), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 42, 58))
    for bx, bw, bh in [(x + 6, 16, 34), (x + 26, 12, 48), (x + 42, 18, 30), (x + 64, 12, 42)]:
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(120, 126, 150))
    d.ellipse([x + w - 26, y + 8, x + w - 10, y + 24], fill=(255, 190, 60))
    d.line([(x + 14, y + 14), (x + 30, y + 30)], fill=(255, 120, 40), width=3)
    d.line([(x + 34, y + 10), (x + 22, y + 28)], fill=(255, 120, 40), width=3)
    d.text((x + 6, y + h - 16), "KYIV", font=SANS_B(10), fill=(255, 255, 255))


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.line([(x + 6, y + h - 30), (x + w - 6, y + 14)], fill=(214, 178, 40), width=5)
    for tx in (x + 12, x + 38):
        d.polygon([(tx, y + h - 34), (tx + 22, y + h - 34), (tx + 11, y + h - 52)],
                  fill=(150, 110, 60))
    d.rectangle([x + w - 30, y + 10, x + w - 24, y + h - 30], fill=INK)
    d.rectangle([x + w - 38, y + 16, x + w - 16, y + 22], fill=(90, 90, 90))
    d.text((x + 6, y + 4), "GAZA", font=SANS_B(10), fill=INK)


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 26, 44))
    d.polygon([(x + w // 2 - 12, y + h - 8), (x + w // 2 - 4, y + 12),
               (x + w // 2 + 10, y + 12), (x + w // 2 + 16, y + h - 8)],
              fill=(150, 170, 210))
    for i in range(5):
        yy = y + 18 + i * 10
        d.line([(x + w // 2 - 6 + i, yy), (x + w // 2 + 8 - i, yy)],
               fill=(255, 220, 120), width=2)
    d.line([(x + 6, y + 12), (x + w - 20, y + 30)], fill=(255, 120, 40), width=3)
    d.ellipse([x + w - 24, y + 26, x + w - 14, y + 36], fill=(255, 170, 0))


def ill_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(208, 228, 240))
    cx, cy = x + w // 2, y + h // 2
    for r in (26, 19, 12, 6):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=BLUE, width=4)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(64, 110, 150))
    d.text((x + 6, y + 4), "110 km/h", font=SANS_B(11), fill=BLUE)


def ill_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 232))
    base = y + h - 12
    for i, bh in enumerate((14, 22, 18, 32, 44)):
        bx = x + 8 + i * 14
        d.rectangle([bx, base - bh, bx + 10, base], fill=BLUE if i < 4 else RED)
    d.line([(x + 8, base - 46), (x + w - 8, base - 56)], fill=RED, width=3)
    d.polygon([(x + w - 14, base - 62), (x + w - 4, base - 56), (x + w - 14, base - 50)],
              fill=RED)
    d.text((x + 6, y + 4), "$97.17", font=SANS_B(11), fill=INK)


def ill_fiji(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(244, 232, 200))
    d.ellipse([x + w - 30, y + 6, x + w - 8, y + 28], fill=(255, 170, 0))
    for i in range(6):
        d.line([(x + 8 + i * 12, y + h - 12), (x + 14 + i * 12, y + h - 34)],
               fill=(120, 82, 40), width=2)
    d.line([(x + 6, y + h - 12), (x + w - 6, y + h - 12)], fill=(120, 82, 40), width=3)
    d.text((x + 6, y + 4), "DROUGHT", font=SANS_B(10), fill=(140, 60, 20))


def ill_seoul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    d.polygon([(x + 8, y + 30), (x + w // 2, y + 14), (x + w - 8, y + 30)], fill=INK)
    for i in range(4):
        bx = x + 12 + i * 18
        d.rectangle([bx, y + 32, bx + 8, y + h - 12], fill=INK)
    d.rectangle([x + 8, y + h - 12, x + w - 8, y + h - 8], fill=INK)
    d.text((x + 6, y + 4), "SEOUL", font=SANS_B(10), fill=BLUE)


def ill_missiles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 42, 58))
    for i in range(3):
        bx = x + 10 + i * 26
        d.polygon([(bx + 6, y + 12), (bx + 12, y + 24), (bx, y + 24)], fill=(200, 200, 210))
        d.rectangle([bx, y + 24, bx + 12, y + h - 22], fill=(200, 200, 210))
        d.polygon([(bx, y + h - 22), (bx + 4, y + h - 12), (bx + 8, y + h - 22)],
                  fill=(255, 170, 0))
        d.polygon([(bx + 4, y + h - 22), (bx + 8, y + h - 12), (bx + 12, y + h - 22)],
                  fill=(255, 170, 0))
    d.text((x + 6, y + h - 14), "1,500+", font=SANS_B(11), fill=(255, 255, 255))


def ill_atom(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 226))
    cx, cy = x + w // 2, y + h // 2
    for ang in (0, 60, 120):
        d.arc([cx - 26, cy - 14, cx + 26, cy + 14], ang, ang + 180, fill=BLUE, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    d.text((x + 6, y + 4), "YONGBYON", font=SANS_B(9), fill=INK)


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 214))
    d.rectangle([x + 14, y + 12, x + 20, y + h - 16], fill=(150, 110, 60))
    d.rectangle([x + 12, y + 8, x + 22, y + 16], fill=(150, 110, 60))
    d.ellipse([x + w - 30, y + 12, x + w - 14, y + 28], fill=RED)
    for i in range(3):
        sx = x + w - 44 + i * 8
        d.rectangle([sx, y + h - 30, sx + 4, y + h - 10], fill=(220, 200, 120))
    d.text((x + 30, y + h - 20), "146*", font=SANS_B(16), fill=INK)


# ---------------------------------------------------------------- lead picture
def ill_lead(d, x, y, w, h):
    """Shenzhen summit: skyline, three flags, three leaders at a table."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 34, 56))
    # skyline
    for bx, bw, bh in [(0, 34, 90), (40, 26, 130), (72, 30, 100), (108, 24, 150),
                       (300, 30, 120), (336, 26, 90), (366, 34, 140), (404, 16, 80)]:
        d.rectangle([x + bx, y + h - 96 - bh + 40, x + bx + bw, y + h - 56],
                    fill=(52, 66, 96))
    # lit windows, kept below the caption line
    for wx in range(0, w, 18):
        for wy in range(y + 40, y + 70, 16):
            if (wx * 7 + wy * 3) % 23 < 6:
                d.rectangle([x + wx, wy, x + wx + 5, wy + 7], fill=(255, 220, 120))
    d.text((x + 10, y + 10), "SHENZHEN  -  APEC SUMMIT", font=SANS_B(13),
           fill=(255, 220, 120))
    # flags
    flags = [("US", (178, 34, 52), (255, 255, 255)),
             ("CN", (222, 41, 16), (255, 220, 0)),
             ("RU", (255, 255, 255), (0, 57, 166))]
    for i, (code, c1, c2) in enumerate(flags):
        fx = x + 60 + i * 140
        d.line([(fx, y + 78), (fx, y + 158)], fill=(200, 200, 200), width=3)
        d.rectangle([fx, y + 78, fx + 74, y + 110], fill=c1)
        if code == "US":
            for s in range(4):
                d.rectangle([fx, y + 80 + s * 8, fx + 74, y + 83 + s * 8], fill=c2)
            d.rectangle([fx, y + 78, fx + 30, y + 96], fill=(30, 40, 90))
        elif code == "CN":
            d.ellipse([fx + 8, y + 84, fx + 20, y + 96], fill=c2)
        else:
            d.rectangle([fx, y + 78, fx + 74, y + 89], fill=c2)
            d.rectangle([fx, y + 100, fx + 74, y + 110], fill=(213, 0, 50))
    # leaders at table
    ty = y + h - 56
    d.rectangle([x, y + h - 62, x + w, y + h], fill=(120, 80, 40))
    for i, (name, suit) in enumerate([("TRUMP", (30, 40, 70)),
                                      ("XI", (60, 30, 30)),
                                      ("PUTIN", (30, 50, 40))]):
        cx = x + 95 + i * 140
        d.ellipse([cx - 22, ty - 78, cx + 22, ty - 34], fill=(232, 205, 170))
        d.polygon([(cx - 34, ty - 6), (cx - 26, ty - 40), (cx + 26, ty - 40),
                   (cx + 34, ty - 6)], fill=suit)
        d.polygon([(cx - 7, ty - 40), (cx, ty - 26), (cx + 7, ty - 40)], fill=(255, 255, 255))
        d.text((cx - 26, ty - 22), name, font=SANS_B(12), fill=(255, 255, 255))


# ---------------------------------------------------------------- stories
# (kicker, headline, standfirst, illustration)
STORIES = [
    ("WORLD COURT  •  THE HAGUE",
     "Myanmar guilty of Rohingya genocide",
     "World Court finds the state liable for the first time in its 80-year history; 9–6 verdict, cheered by Rohingya refugees.",
     ill_scales),
    ("UKRAINE  •  CRIMEA",
     "Crimean Bridge hit a third time",
     "Neptune missiles strike the rail span and halt trains; the road arch fell into the strait on Tuesday.",
     ill_bridge),
    ("UKRAINE  •  KYIV",
     "Drone raid hits Kyiv embassies",
     "One killed, five hurt as a Russian drone attack damages the Dutch and Austrian embassies and St Volodymyr's Cathedral.",
     ill_kyiv),
    ("GAZA  •  CEASEFIRE",
     "Israeli tanks cross Gaza line",
     "First ground raid beyond the ceasefire line since the October 2025 truce ends after a day; 1,600+ killed since the truce began.",
     ill_gaza),
    ("YEMEN  •  SAUDI ARABIA",
     "Houthi missile hits Riyadh tower",
     "Windows blown out across seven floors of the PIF Tower, the kingdom's tallest; no injuries, and the Houthis say nothing.",
     ill_riyadh),
    ("WEATHER  •  INDIA",
     "Cyclone Akvan makes landfall",
     "More than 300,000 evacuated as the storm crosses the Andhra Pradesh–Odisha coast near Gopalpur, gusts of 110 km/h.",
     ill_cyclone),
    ("TECH  •  MARKETS",
     "Anthropic's record IPO closes",
     "ANT ends its first day at $97.17, up 17% on the $83 price; the $81.3bn listing is the largest ever.",
     ill_ipo),
    ("PACIFIC  •  CLIMATE",
     "Fiji declares drought disaster",
     "A national state of disaster as El Niño drought drains water supplies; F$20m set aside for relief.",
     ill_fiji),
    ("SOUTH KOREA  •  SEOUL",
     "Top court overturns Han's term",
     "Supreme Court sends ex-PM Han Duck-soo's martial-law case back for retrial; other guilty findings stand.",
     ill_seoul),
    ("MIDDLE EAST  •  IRAN",
     "Iran may still hold 2,500 missiles",
     "US intelligence puts Tehran's arsenal at 1,500–2,500 — a low-confidence estimate — after nine months of war.",
     ill_missiles),
    ("NORTH KOREA  •  NUCLEAR",
     "Pyongyang expands enrichment",
     "UN watchdog reports North Korea is enlarging its uranium enrichment plant at Yongbyon.",
     ill_atom),
    ("SPORT  •  CRICKET",
     "Nicholls 146* as NZ pass 300",
     "Phillips falls for 118 as New Zealand reach 317 for 6 at lunch on day two in Wellington.",
     ill_cricket),
]


def draw_card(d, x, y, w, h, kicker, headline, standfirst, ill):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=(200, 200, 192), width=1)
    d.rectangle([x, y, x + w, y + 3], fill=RED)
    iw, ih = 82, 82
    ix, iy = x + w - iw - 9, y + 10
    ill(d, ix, iy, iw, ih)
    tx = x + 10
    tw = w - iw - 28
    d.text((tx, y + 9), kicker, font=SANS_B(10), fill=RED)
    yy = para(d, tx, y + 25, headline, SERIF_B(16), tw, 19)
    para(d, tx, yy + 2, standfirst, SANS(11), tw, 14, fill=(60, 60, 56))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.text((W // 2, 14), "THE WORLD TODAY", font=SERIF_B(58), fill=INK, anchor="ma")
    rule(d, 28, 88, 996, 3)
    d.text((28, 96), "FRIDAY, 20 NOVEMBER 2026", font=SANS_B(15), fill=INK)
    d.text((996, 96), "ONE DAY  •  ONE PAGE  •  ALL THE NEWS",
           font=SANS_B(13), fill=GREY, anchor="ra")
    rule(d, 28, 120, 996, 1)

    # lead story
    lx, ly = 28, 132
    lw = 528
    d.text((lx, ly), "SUMMIT IN SHENZHEN  •  APEC", font=SANS_B(13), fill=RED)
    yy = para(d, lx, ly + 22,
              "Trump, Xi and Putin meet face to face",
              SERIF_B(37), lw, 42)
    yy = para(d, lx, yy + 6,
              "The three leaders hold their first-ever three-way talks in China, "
              "on nuclear arms control, energy and the wars in Ukraine and the "
              "Middle East — and issue a four-point peace declaration.",
              SANS(16), lw, 21, fill=(40, 40, 36))
    yy += 8
    for b in ("Four-point peace declaration issued — but the details are thin.",
              "Putin: no agreements after the bridge strikes.",
              "European allies meet in Berlin, say they are ready for talks with Russia."):
        d.text((lx + 12, yy), "•", font=SANS_B(15), fill=RED)
        yy = para(d, lx + 26, yy, b, SANS(14), lw - 26, 18)
        yy += 2
    ill_lead(d, 576, 132, 420, 296)
    rule(d, 28, 444, 996, 2)

    # grid of further stories
    gx, gy = 28, 458
    cw, ch, gap = 314, 122, 13
    for i, (kicker, headline, standfirst, ill) in enumerate(STORIES):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + 10)
        draw_card(d, cx, cy, cw, ch, kicker, headline, standfirst, ill)

    # footer strip
    fy = 972
    rule(d, 28, fy, 996, 2)
    para(d, 28, fy + 8,
         "ALSO IN THE NEWS:  S&P 500 falls 2% for a fifth straight day  •  "
         "California opens a probe into Nvidia's China AI-chip sales  •  "
         "Trump pardons baseball's Pete Rose  •  COP31 closes in Antalya",
         SANS_B(11), 968, 14, fill=INK)
    d.text((28, 1004),
           "Sources: Reuters, AP, AFP, The Wall Street Journal, IAEA, India Meteorological Dept, "
           "SEC filings — all stories reported 19–20 November 2026.",
           font=SANS(9), fill=GREY)
    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    print(out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
