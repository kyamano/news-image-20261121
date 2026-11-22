#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page as a 1024x1024 PNG.

Deterministic: no clock, no randomness, no network. Running it twice writes
byte-identical output. Run: python3 generate.py [output-path]
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (24, 28, 36)
NAVY = (20, 38, 63)
NAVY_LIGHT = (31, 58, 95)
RED = (178, 34, 34)
GREY = (96, 100, 108)
CARD = (255, 255, 255)
CARD_EDGE = (205, 200, 188)
BRIEF_BG = (238, 233, 220)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_TITLE = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_TEXT = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- stories
# (tag, headline, summary, icon, accent colour)
STORIES = [
    ("CLIMATE", "COP31 talks run into overtime",
     "Nearly 200 nations are deadlocked in Antalya as the draft deal drops "
     "every mention of fossil fuels.",
     "leaf", (46, 125, 50)),
    ("UKRAINE", "Missile hits Zelensky's hometown",
     "A Russian strike on Kryvyi Rih kills two, including a 7-year-old boy, "
     "and wounds about 60.",
     "missile", (176, 58, 46)),
    ("BALTIC SEA", "Drones hit Russian cargo ship",
     "The sanctioned freighter Sparta II catches fire in the Gulf of Finland; "
     "Finland says Ukraine was likely behind it.",
     "ship", (26, 82, 118)),
    ("GAZA", "Strike hits food-aid van in Gaza City",
     "Three Palestinians are killed as an Israeli strike hits a van "
     "delivering food in Tel al-Hawa.",
     "cross", (125, 60, 152)),
    ("PERU", "M6.7 quake shakes central Peru",
     "The tremor rattles Lima from its Junin epicentre; no deaths or major "
     "damage are reported.",
     "crack", (147, 81, 22)),
    ("GULF", "Hormuz tanker attacks hit wartime high",
     "Two more tankers are struck and oil shipments through the strait fall "
     "15% as the US-Iran standoff deepens.",
     "tanker", (14, 102, 85)),
    ("SAUDI ARABIA", "Riyadh downs three Houthi missiles",
     "Saudi defences intercept missiles aimed at the capital as Houthi "
     "attacks from Yemen continue.",
     "shield", (30, 132, 73)),
    ("DENMARK", "Denmark expels Russian attache",
     "Copenhagen acts over a foiled plot to assassinate US-Ukrainian rapper "
     "Kyivstoner.",
     "flag", (44, 62, 80)),
    ("NEPAL - INDIA", "Nepal's PM begins India visit",
     "Balendra Shah arrives for a two-day state visit and talks with Prime "
     "Minister Modi.",
     "flags", (169, 50, 38)),
    ("UKRAINE", "Zelensky: Putin is a 'killer'",
     "Kyiv's leader hits back after Trump calls the Russian president a "
     "friend.",
     "speech", (36, 113, 163)),
]

BRIEFS = [
    "Wall Street rout: S&P 500 -3.7% and Dow enter correction; Nasdaq -5.3%",
    "UK-EU seal post-Brexit reset: food trade, carbon link, youth mobility",
    "Russian missiles land in Poland; NATO calls it a 'grave violation'",
    "US-Iran talks stall over uranium; mediators warn of renewed conflict",
    "Japan core inflation 2.2% in October; BOJ rate-hike bets rise",
    "Anthropic slides on day two: shares close at $88.91 after $83 IPO",
    "Cancer pill hope: daraxonrasib leaves tumours undetectable in 1 in 12",
    "FBI probes apparent hack of its NCIC crime database",
    "Mamdani unveils plan to close Rikers Island jail by 2032",
    "Man convicted of starting LA's deadly 2025 Palisades fire",
    "Sudan army clears 10 RSF positions in West Kordofan",
    "Iraqi troops storm Iran-aligned Kataeb Hezbollah stronghold",
    "EU proposes 3% Big Tech tax to fund its 2028-34 budget",
    "Manipur spurious liquor: 13 dead, 300+ in hospital",
    "Cricket: India 486/4, lead New Zealand by 118 on Day 3",
    "Gen Z Youth Day of Action: walkouts in 25 European countries",
    "US offers first deep-sea mining leases near American Samoa",
    "Iran FM: open to a 'just' US deal - but uranium stays put",
    "Eisenkot tasked with forming Israel's next government",
    "Nvidia halts H200 AI chip exports to China",
]

FOOTER = ("Reported 21 November 2026  |  Reuters  -  AP  -  AFP  -  Al Jazeera  -  "
          "Le Monde  -  The Hindu  -  Times of Israel  -  USGS")


# ---------------------------------------------------------------- icons
def draw_icon(d, kind, box, colour):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "leaf":
        # A leaf: two curved sides meeting at a point, with a centre vein.
        d.polygon([(cx - 24, cy + 18), (cx - 20, cy - 18), (cx + 4, cy - 26),
                   (cx + 24, cy - 6), (cx + 18, cy + 20), (cx - 6, cy + 24)],
                  outline=colour, width=4)
        d.line([cx - 20, cy + 14, cx + 16, cy - 14], fill=colour, width=3)
        d.line([cx - 8, cy + 4, cx - 2, cy - 8], fill=colour, width=3)
        d.line([cx + 4, cy - 4, cx + 10, cy - 14], fill=colour, width=3)
        d.arc([cx - 30, cy - 32, cx - 2, cy - 4], 270, 360, fill=(255, 193, 7),
              width=4)
    elif kind == "missile":
        d.polygon([(cx + 22, cy - 26), (cx + 30, cy - 6), (cx + 14, cy - 2)],
                  fill=colour)
        d.polygon([(cx - 22, cy + 26), (cx - 6, cy + 18), (cx - 14, cy + 30)],
                  fill=(230, 126, 34))
        d.line([cx - 22, cy + 22, cx + 22, cy - 22], fill=colour, width=7)
        d.line([cx - 30, cy + 6, cx - 18, cy + 26], fill=colour, width=4)
        d.line([cx - 6, cy + 30, cx + 14, cy + 18], fill=colour, width=4)
    elif kind == "ship":
        d.polygon([(cx - 28, cy + 4), (cx + 28, cy + 4), (cx + 20, cy + 22),
                   (cx - 20, cy + 22)], fill=colour)
        d.line([cx, cy + 4, cx, cy - 24], fill=colour, width=4)
        d.polygon([(cx, cy - 24), (cx, cy - 6), (cx + 18, cy - 6)],
                  fill=colour)
        for wy in (30, 36):
            d.arc([cx - 30, cy + wy - 6, cx + 30, cy + wy + 6], 0, 180,
                  fill=(52, 152, 219), width=3)
    elif kind == "cross":
        d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], outline=colour,
                    width=4)
        d.rectangle([cx - 6, cy - 18, cx + 6, cy + 18], fill=RED)
        d.rectangle([cx - 18, cy - 6, cx + 18, cy + 6], fill=RED)
    elif kind == "crack":
        d.rectangle([cx - 26, cy + 10, cx - 10, cy + 26], outline=colour,
                    width=3)
        d.rectangle([cx + 10, cy + 10, cx + 26, cy + 26], outline=colour,
                    width=3)
        d.line([(cx - 26, cy - 24), (cx - 12, cy - 10), (cx - 20, cy + 2),
                (cx - 4, cy - 6), (cx + 6, cy + 8), (cx + 22, cy - 14)],
               fill=colour, width=5)
    elif kind == "tanker":
        d.polygon([(cx - 28, cy + 2), (cx + 28, cy + 2), (cx + 20, cy + 20),
                   (cx - 20, cy + 20)], fill=colour)
        d.rectangle([cx - 18, cy - 14, cx - 4, cy + 2], fill=colour)
        d.rectangle([cx + 6, cy - 8, cx + 18, cy + 2], fill=colour)
        d.polygon([(cx + 2, cy - 30), (cx + 12, cy - 14), (cx - 8, cy - 14)],
                  fill=(230, 126, 34))
    elif kind == "shield":
        d.polygon([(cx, cy - 26), (cx + 24, cy - 16), (cx + 24, cy + 4),
                   (cx, cy + 26), (cx - 24, cy + 4), (cx - 24, cy - 16)],
                  outline=colour, width=4)
        d.line([(cx - 12, cy), (cx - 3, cy + 10), (cx + 14, cy - 10)],
               fill=colour, width=4)
    elif kind == "flag":
        d.line([cx - 18, cy - 26, cx - 18, cy + 26], fill=colour, width=4)
        d.polygon([(cx - 18, cy - 26), (cx + 22, cy - 18), (cx - 18, cy - 8)],
                  fill=colour)
        d.line([(cx - 26, cy + 26), (cx + 26, cy + 26)], fill=colour, width=3)
    elif kind == "flags":
        d.polygon([(cx - 24, cy - 24), (cx - 2, cy - 14), (cx - 24, cy - 4)],
                  fill=(220, 60, 50))
        d.polygon([(cx - 24, cy - 2), (cx - 2, cy + 8), (cx - 24, cy + 18)],
                  fill=(40, 90, 180))
        d.polygon([(cx + 2, cy - 24), (cx + 24, cy - 14), (cx + 2, cy - 4)],
                  fill=(255, 153, 51))
        d.polygon([(cx + 2, cy - 2), (cx + 24, cy + 8), (cx + 2, cy + 18)],
                  fill=(19, 136, 8))
    elif kind == "speech":
        d.rounded_rectangle([cx - 26, cy - 24, cx + 26, cy + 12], radius=8,
                            outline=colour, width=4)
        d.polygon([(cx - 12, cy + 12), (cx - 18, cy + 26), (cx + 2, cy + 12)],
                  fill=colour)
        d.text((cx - 14, cy - 18), "''", font=font(F_BOLD, 26), fill=colour)


# ---------------------------------------------------------------- page
def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- title bar
    d.rectangle([0, 0, W, 64], fill=NAVY)
    d.rectangle([0, 64, W, 68], fill=RED)
    d.text((18, 8), "WORLD NEWS", font=font(F_TITLE, 34), fill=(255, 255, 255))
    d.text((18, 44), "SATURDAY 21 NOVEMBER 2026",
           font=font(F_BOLD, 15), fill=(255, 214, 90))
    right = "ONE DAY  -  ONE IMAGE"
    d.text((W - 18 - d.textlength(right, font=font(F_BOLD, 15)), 44),
           right, font=font(F_BOLD, 15), fill=(200, 210, 225))

    # --- main panels: 2 columns x 5 rows
    px, py = 16, 76
    pw, ph = 488, 116
    gx, gy = 16, 8
    f_tag = font(F_BOLD, 11)
    f_head = font(F_BOLD, 17)
    f_sum = font(F_TEXT, 12)
    for i, (tag, head, summ, icon, colour) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = px + col * (pw + gx)
        y = py + row * (ph + gy)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=6, fill=CARD,
                            outline=CARD_EDGE, width=1)
        d.rectangle([x, y + 6, x + 5, y + ph - 6], fill=colour)
        # icon tile
        ix0, iy0 = x + 14, y + 14
        d.rounded_rectangle([ix0, iy0, ix0 + 76, iy0 + 76], radius=8,
                            fill=(240, 244, 248), outline=CARD_EDGE, width=1)
        draw_icon(d, icon, (ix0 + 8, iy0 + 8, ix0 + 68, iy0 + 68), colour)
        tx = x + 102
        d.text((tx, y + 10), tag, font=f_tag, fill=colour)
        lines = wrap(d, head, f_head, pw - 118)
        ly = y + 28
        for ln in lines[:2]:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 21
        slines = wrap(d, summ, f_sum, pw - 118)
        sy = y + 28 + 21 * min(len(lines), 2) + 2
        for ln in slines[:2]:
            d.text((tx, sy), ln, font=f_sum, fill=(58, 62, 70))
            sy += 16

    # --- briefs header
    by = 692
    d.rectangle([0, by, W, by + 26], fill=NAVY_LIGHT)
    d.text((18, by + 4), "ALSO ON SATURDAY  -  20 MORE STORIES",
           font=font(F_BOLD, 14), fill=(255, 255, 255))

    # --- briefs: 2 columns x 10 rows
    f_brief = font(F_TEXT, 12)
    f_bullet = font(F_BOLD, 12)
    bx, byy = 16, 728
    bw = 488
    for i, item in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        x = bx + col * (bw + 16)
        y = byy + row * 26
        d.text((x, y), "\u2022", font=f_bullet, fill=RED)
        lines = wrap(d, item, f_brief, bw - 18)
        d.text((x + 16, y), lines[0], font=f_brief, fill=INK)
        if len(lines) > 1:
            d.text((x + 16, y + 13), lines[1], font=f_brief, fill=INK)

    # --- footer
    d.text(((W - d.textlength(FOOTER, font=font(F_TEXT, 10))) // 2, 1000),
           FOOTER, font=font(F_TEXT, 10), fill=GREY)

    img.save(path, format="PNG")
    return path


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
    print(out)


if __name__ == "__main__":
    main()
