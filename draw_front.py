"""Build script (local only, not the entrypoint): draws entry.png v2.

Run: python3 draw_front.py
Writes entry.png beside this file, 1024x1024, white newspaper front page.
v2: only 5 stories, all text >= 28px, big date, bold summit-table visual.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (15, 42, 68)
GOLD = (197, 146, 44)
RED = (178, 34, 34)
INK = (20, 20, 20)
GREY = (90, 90, 90)
LIGHT = (238, 240, 243)
TEAL = (0, 110, 110)
SKY = (210, 232, 238)
TABLE = (120, 72, 40)
CHAIR = (60, 60, 60)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

# Masthead: title + huge date
d.rectangle([0, 0, W, 176], fill=NAVY)
d.text((36, 16), "THE WORLD IN ONE DAY", font=font(SERIF, 56), fill=(255, 255, 255))
d.text((36, 96), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 44), fill=(255, 210, 110))
d.rectangle([0, 176, W, 182], fill=GOLD)

# Lead story: COP31. Text left, summit-table visual right.
d.text((36, 200), "CLIMATE  •  COP31  •  ANTALYA, TURKEY", font=font(SANS_B, 28), fill=RED)
d.text((36, 238), "COP31", font=font(SERIF, 88), fill=NAVY)
d.text((36, 326), "COLLAPSES", font=font(SERIF, 88), fill=NAVY)
text_block(d, 36, 428, "Nearly 200 countries fail to agree a climate declaration.", font(SANS, 32), 540, leading=41)

# Summit visual panel: an empty conference table, three empty chairs,
# microphones with no one speaking, and a red crack across the table.
px, py, pw, ph = 620, 198, 368, 300
d.rounded_rectangle([px, py, px + pw, py + ph], radius=12, fill=SKY, outline=NAVY, width=3)
# chairs (backs) behind the table
for cx in (px + 48, px + 152, px + 256):
    d.rounded_rectangle([cx, py + 52, cx + 64, py + 128], radius=10, fill=CHAIR)
    d.rectangle([cx + 8, py + 128, cx + 56, py + 142], fill=CHAIR)
# table
d.polygon([(px + 18, py + 150), (px + pw - 18, py + 150),
           (px + pw - 34, py + 236), (px + 34, py + 236)], fill=TABLE, outline=NAVY, width=2)
# blank name plates on the table front: seats taken by no one
for nx in (px + 66, px + 170, px + 274):
    d.rectangle([nx, py + 186, nx + 56, py + 214], fill=(255, 255, 255), outline=NAVY, width=2)
# red crack across the table and floor
d.line([(px + 150, py + 150), (px + 190, py + 190), (px + 168, py + 220),
        (px + 210, py + 252)], fill=RED, width=7)
d.text((px + 22, py + 258), "NO DEAL IN ANTALYA", font=font(SANS_B, 28), fill=RED)

# Second story: US House, full-width band
d.rectangle([36, 544, 988, 712], fill=LIGHT, outline=NAVY, width=2)
d.text((56, 560), "UNITED STATES  •  HOUSE", font=font(SANS_B, 28), fill=NAVY)
d.text((56, 596), "Democrats win House majority", font=font(SERIF, 52), fill=INK)
d.text((56, 660), "At least 258 seats — the largest since 1992.", font=font(SANS, 30), fill=INK)
d.text((812, 558), "258", font=font(SERIF, 108), fill=RED)
d.text((828, 668), "SEATS", font=font(SANS_B, 28), fill=RED)

# Three large cards, one row
cards = [
    ("SUMMIT", "Xi, Trump and Putin meet in first trilateral talks",
     "First three-way talks"),
    ("UKRAINE", "Sea drones strike a Russian warship in Libya",
     "Ship hit in the Baltic"),
    ("MEXICO", "Mexico captures a drug kingpin on the FBI most-wanted list",
     "Deadly firefight"),
]
cw, ch = 304, 252
x0, y0 = 36, 740
for i, (kicker, headline, sub) in enumerate(cards):
    cx = x0 + i * (cw + 20)
    d.rectangle([cx, y0, cx + cw, y0 + ch], outline=(180, 180, 180), width=2)
    d.rectangle([cx, y0, cx + cw, y0 + 44], fill=NAVY)
    d.text((cx + 14, y0 + 8), kicker, font=font(SANS_B, 28), fill=(255, 255, 255))
    y = text_block(d, cx + 14, y0 + 62, headline, font(SANS, 30), cw - 28, leading=39)
    text_block(d, cx + 14, y + 10, sub, font(SANS, 28), cw - 28, fill=GREY, leading=36)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
