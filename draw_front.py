"""Build script (local only, not the entrypoint): draws entry.png.

Run: python3 draw_front.py
Writes entry.png beside this file, 1024x1024, white newspaper front page.
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

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
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
    lh = leading or int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

# Masthead
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((36, 18), "THE WORLD IN ONE DAY", font=font(SERIF, 56), fill=(255, 255, 255))
d.text((36, 88), "MONDAY  23  NOVEMBER  2026", font=font(SANS_B, 34), fill=(255, 210, 110))
d.rectangle([0, 148, W, 154], fill=GOLD)

# Lead story: COP31, left text, right globe panel
d.text((36, 172), "CLIMATE  •  COP31  •  ANTALYA, TURKEY", font=font(SANS_B, 22), fill=RED)
d.text((36, 202), "COP31", font=font(SERIF, 78), fill=NAVY)
d.text((36, 282), "COLLAPSES", font=font(SERIF, 78), fill=NAVY)
text_block(d, 36, 372, "Nearly 200 countries fail to agree a climate declaration, as fossil-fuel divisions split the talks.", font(SANS, 26), 560, leading=33)

# Globe panel, right side
gx, gy, gw, gh = 640, 170, 348, 250
d.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=12, fill=(210, 232, 238), outline=NAVY, width=3)
d.ellipse([gx + 84, gy + 28, gx + 264, gy + 208], fill=(70, 150, 190), outline=NAVY, width=3)
# simple continents
d.ellipse([gx + 120, gy + 55, gx + 175, gy + 105], fill=(90, 170, 90))
d.ellipse([gx + 185, gy + 95, gx + 235, gy + 150], fill=(90, 170, 90))
d.ellipse([gx + 135, gy + 140, gx + 180, gy + 180], fill=(120, 190, 100))
# crack across the globe
d.line([(gx + 130, gy + 40), (gx + 170, gy + 100), (gx + 150, gy + 140), (gx + 200, gy + 195)], fill=RED, width=6)
d.text((gx + 18, gy + 214), "NO DEAL IN ANTALYA", font=font(SANS_B, 20), fill=RED)

# Second story: US House band
d.rectangle([36, 448, 988, 580], fill=LIGHT, outline=NAVY, width=2)
d.text((56, 462), "UNITED STATES  •  HOUSE OF REPRESENTATIVES", font=font(SANS_B, 21), fill=NAVY)
d.text((56, 492), "Democrats win House majority", font=font(SERIF, 40), fill=INK)
d.text((56, 540), "At least 258 seats — the largest since 1992.", font=font(SANS, 25), fill=INK)
d.text((830, 468), "258", font=font(SERIF, 82), fill=RED)
d.text((838, 552), "SEATS", font=font(SANS_B, 20), fill=RED)

# Grid of six smaller stories, 3 columns x 2 rows
stories = [
    ("SUMMIT", "Xi, Trump and Putin meet in first trilateral talks", "🌐"),
    ("UKRAINE", "Sea drones strike a Russian warship; Russia tows a ship hit in the Baltic", "⚓"),
    ("KYIV", "Russian strikes kill several people in the Kyiv region, Ukraine says", "✚"),
    ("MEXICO", "Mexico captures a drug kingpin on the FBI most-wanted list", "★"),
    ("ISRAEL", "Israel probes West Bank fires blamed on settlers; coalition talks fail", "☀"),
    ("NORTH KOREA", "Kim says North Korea seeks security, not supremacy", "⬢"),
]
# icons are drawn as simple shapes instead of emoji (fonts may lack them); use a coloured dot + letter
col_w, row_h = 304, 168
x0, y0 = 36, 606
for i, (kicker, headline, _icon) in enumerate(stories):
    cx = x0 + (i % 3) * (col_w + 20)
    cy = y0 + (i // 3) * row_h
    d.rectangle([cx, cy, cx + col_w, cy + row_h - 16], outline=(180, 180, 180), width=1)
    d.rectangle([cx, cy, cx + col_w, cy + 34], fill=NAVY)
    d.text((cx + 12, cy + 6), kicker, font=font(SANS_B, 19), fill=(255, 255, 255))
    text_block(d, cx + 12, cy + 48, headline, font(SANS, 24), col_w - 24, leading=30)

# Also strip at the bottom, wrapped so nothing is cut off
d.rectangle([36, 954, 988, 958], fill=GOLD)
text_block(d, 36, 966, "ALSO: Indonesia factory fire — 3 dead, 36 missing  •  Sudan strikes hit homes and a UN building  •  Alcaraz wins first ATP Finals title",
           font(SANS, 19), 952, fill=GREY, leading=24)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
