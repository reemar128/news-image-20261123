#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page, 1024x1024 PNG.

Newspaper style, like the entries leading the sister bounty:
35 stories, 7 regions, every one happened or first reported on
Monday 23 November 2026 (UTC), with a date check at the foot.
Stories verified against AP / Reuters / AFP / Al Jazeera, Cricinfo,
ICC, Korea Customs, Nature and the OneTurn daily edition.

Deliberately LEFT OUT (earlier days, however big):
COP31 collapse, Marquez 8th MotoGP title, Alcaraz ATP Finals,
Liverpool 4-0 Man Utd (all Sun 22 Nov); 'El Chapo Isidro' capture,
Mount Mayon eruption (Fri 21 Nov); Lagarde resignation (29 Oct);
Korea exports top $1 trillion (Thu 19 Nov); Riemann proof claim
(Fri 20 Nov) and its verification (Sat 21 Nov).

Deterministic: solid colours + DejaVu fonts only, no randomness,
no network, no timestamps. Re-running writes identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (245, 239, 224)
PAPER = (255, 252, 244)
NAVY = (16, 34, 56)
INK = (22, 26, 32)
GREY = (88, 92, 98)
RED = (172, 28, 28)
TEAL = (0, 102, 102)
GOLD = (214, 158, 0)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_SERIF = lambda s: font("DejaVuSerif-Bold", s)
F_SANS = lambda s: font("DejaVuSans", s)
F_SANSB = lambda s: font("DejaVuSans-Bold", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(text, fnt, x, y, max_w, fill, lh=None):
    h = lh or int(fnt.size * 1.28)
    for ln in wrap(text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += h
    return y

def centre(text, fnt, y, fill, x0=0, x1=W):
    w = d.textlength(text, font=fnt)
    d.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)

# ---------- top bar ----------
d.rectangle([0, 0, W, 26], fill=NAVY)
centre("THE WORLD IN ONE DAY  •  35 STORIES  •  7 REGIONS  •  EVERY ONE DATED MONDAY 23 NOVEMBER 2026",
       F_SANSB(13), 5, (255, 255, 255))

# ---------- masthead ----------
d.text((24, 30), "Monday 23 November 2026", font=F_SERIF(48), fill=INK)
d.text((24, 88), "AI sell-off hits markets  •  Dymer toll rises to 15  •  Merkury sinks in Benghazi",
       font=F_SERIF(18), fill=RED)
d.line([24, 118, W - 24, 118], fill=INK, width=2)

# ---------- numbers strip ----------
nums = [("−5.06%", "Nikkei falls"),
        ("−3.7%", "S&P 500 falls"),
        ("15", "killed in Dymer"),
        ("120", "overs NZ bat out"),
        ("8,320", "drug-war deaths"),
        ("$77.4bn", "Korea exports, Nov 1–20")]
x = 24
bw = (W - 48 - 5 * 8) / 6
for n, lab in nums:
    d.rectangle([x, 126, x + bw, 168], fill=PAPER, outline=(200, 190, 160))
    centre(n, F_SANSB(22), 129, RED, x, x + bw)
    centre(lab, F_SANS(10), 154, GREY, x, x + bw)
    x += bw + 8

# ---------- region bar ----------
regs = [("EUROPE", (30, 90, 160)), ("MIDDLE EAST", RED), ("ASIA-PACIFIC", (204, 120, 0)),
        ("AMERICAS", TEAL), ("AFRICA", (34, 120, 70)), ("OCEANIA", (110, 60, 140)),
        ("WORLD", (90, 90, 90))]
x = 24
rw = (W - 48) / 7
for name, col in regs:
    d.rectangle([x, 176, x + rw - 2, 196], fill=col)
    centre(name, F_SANSB(11), 181, (255, 255, 255), x, x + rw - 2)
    x += rw

# ---------- scenes (flat, drawn in code) ----------
def scene_markets(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 22, 40))
    for gy in (24, 48, 72):
        d.line([x + 10, y + gy, x + w - 10, y + gy], fill=(40, 55, 80), width=1)
    # falling bars
    bars = [(20, 30), (60, 42), (100, 38), (140, 55), (180, 62), (220, 74), (260, 84)]
    for bx, bh in bars:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + 22, y + h - 14], fill=(172, 28, 28))
    # falling line
    pts = [(x + 20, y + 22), (x + 70, y + 34), (x + 120, y + 30), (x + 170, y + 48),
           (x + 220, y + 56), (x + 270, y + 72)]
    d.line(pts, fill=(255, 210, 90), width=3)
    for px_, py_ in pts:
        d.ellipse([px_ - 3, py_ - 3, px_ + 3, py_ + 3], fill=(255, 210, 90))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(30, 45, 70))
    d.text((x + 10, y + h - 13), "NIKKEI −5.06%   S&P −3.7%   GOLD +2.72%", font=F_SANSB(9), fill=(255, 255, 255))

def scene_ukraine(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 44))
    for sx, sy in [(20, 12), (70, 30), (140, 10), (210, 26), (270, 14), (110, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # apartment block, lit windows, one dark collapsed corner
    d.rectangle([x + 18, y + 30, x + 108, y + h], fill=(52, 58, 74))
    for r in range(4):
        for c in range(3):
            col = (255, 200, 80) if (r + c) % 2 else (30, 34, 48)
            d.rectangle([x + 28 + c * 28, y + 40 + r * 18, x + 44 + c * 28, y + 52 + r * 18], fill=col)
    d.polygon([(x + 108, y + 30), (x + 150, y + h), (x + 108, y + h)], fill=(30, 34, 48))
    # rescue lights at the rubble
    for lx in (170, 210, 250):
        d.polygon([(x + lx, y + h - 34), (x + lx - 8, y + h - 14), (x + lx + 8, y + h - 14)],
                  fill=(255, 220, 120))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(20, 28, 50))

def scene_sink(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 44, 84))
    d.ellipse([x + w - 60, y + 10, x + w - 20, y + 50], fill=(240, 230, 200))
    # listing corvette
    d.polygon([(x + 30, y + h - 52), (x + 230, y + h - 70), (x + 250, y + h - 44),
               (x + 60, y + h - 38)], fill=(70, 74, 82))
    d.rectangle([x + 120, y + h - 92, x + 160, y + h - 68], fill=(120, 124, 132))
    d.rectangle([x + 138, y + h - 108, x + 146, y + h - 92], fill=(120, 124, 132))
    # fire + smoke at the waterline
    for fx, fy, fs in [(70, 40, 20), (95, 34, 26), (120, 42, 18)]:
        d.polygon([(x + fx, y + h - fy - fs), (x + fx - fs // 2, y + h - fy),
                   (x + fx + fs // 2, y + h - fy)], fill=(255, 140, 0))
    for sx, sy, sr in [(80, 26, 9), (110, 18, 11), (140, 28, 8)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(90, 90, 90))
    # waves
    for wx in range(0, w, 44):
        d.arc([x + wx, y + h - 22, x + wx + 40, y + h - 2], 180, 360, fill=(120, 170, 220), width=2)
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(10, 30, 60))

def scene_mini(x, y, w, h, kind):
    skies = {"talks": (30, 90, 160), "plane": (90, 150, 200), "cricket": (40, 120, 60),
             "storm": (70, 70, 80), "fire": (60, 30, 30), "gaza": (180, 170, 140)}
    d.rectangle([x, y, x + w, y + h], fill=skies[kind])
    if kind == "talks":
        for bx in (30, w - 62):
            d.rectangle([x + bx, y + 16, x + bx + 32, y + h - 8], fill=(255, 255, 255))
            d.rectangle([x + bx + 6, y + 20, x + bx + 26, y + 28], fill=(30, 90, 160))
        d.ellipse([x + w // 2 - 8, y + 8, x + w // 2 + 8, y + 24], fill=(255, 210, 90))
    elif kind == "plane":
        d.ellipse([x + 40, y + 16, x + w - 40, y + 30], fill=(255, 255, 255))
        d.polygon([(x + w // 2 - 10, y + 22), (x + w // 2 + 60, y + 34), (x + w // 2 + 10, y + 30)],
                  fill=(220, 220, 220))
        d.polygon([(x + w // 2 - 30, y + 22), (x + w // 2 - 60, y + 30), (x + w // 2 - 20, y + 30)],
                  fill=(220, 220, 220))
        for wx in range(60, w - 50, 18):
            d.ellipse([x + wx, y + 19, x + wx + 5, y + 24], fill=(30, 90, 160))
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(200, 210, 220))
    elif kind == "cricket":
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 160, 80))
        d.rectangle([x + w // 2 - 4, y + 8, x + w // 2 + 4, y + h - 16], fill=(220, 180, 120))
        d.ellipse([x + w - 30, y + 12, x + w - 16, y + 26], fill=(200, 30, 30))
    elif kind == "storm":
        d.ellipse([x + 30, y + 6, x + 110, y + 26], fill=(40, 40, 50))
        d.ellipse([x + 70, y + 2, x + 150, y + 22], fill=(50, 50, 60))
        for rx in range(40, w - 20, 22):
            d.line([x + rx, y + 30, x + rx - 6, y + 42], fill=(150, 200, 255), width=2)
        d.polygon([(x + w - 60, y + 12), (x + w - 44, y + 30), (x + w - 56, y + 30),
                   (x + w - 38, y + 46), (x + w - 62, y + 46)], fill=(255, 220, 0))
    elif kind == "fire":
        d.polygon([(x + w // 2, y + 6), (x + w // 2 - 26, y + h - 8), (x + w // 2 + 26, y + h - 8)],
                  fill=(255, 140, 0))
        d.polygon([(x + w // 2, y + 24), (x + w // 2 - 12, y + h - 8), (x + w // 2 + 12, y + h - 8)],
                  fill=(255, 220, 0))
    elif kind == "gaza":
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 120, 120))
        d.rectangle([x + 16, y + 20, x + w - 16, y + 40], fill=(255, 255, 255))
        d.rectangle([x + 16, y + 20, x + w - 16, y + 28], fill=(220, 60, 60))
        d.ellipse([x + 30, y + 40, x + 46, y + 52], fill=(10, 10, 10))
        d.ellipse([x + w - 46, y + 40, x + w - 30, y + 52], fill=(10, 10, 10))

# ---------- top 3 panels ----------
top = [
    ("1  •  MARKETS  •  AI SELL-OFF", "Markets slide on AI fears",
     "Nikkei falls 5.06% and the S&P 500 3.7% as AI shares slide; gold jumps 2.72% as investors flee to safety.", scene_markets),
    ("2  •  DYMER, UKRAINE  •  RESCUE", "Dymer toll rises to 15",
     "A 7-year-old boy is pulled alive from the rubble after 14 hours as rescuers dig through the block hit on Sunday.", scene_ukraine),
    ("3  •  BENGHAZI  •  NAVY", "Russian corvette sinks",
     "The Merkury sinks at Benghazi after a suspected Ukrainian sea-drone strike; Zelenskyy says Ukraine did it.", scene_sink),
]
px, py, pw, ph, pgap = 24, 204, 312, 226, 16
for i, (kick, head, body, scene) in enumerate(top):
    x = px + i * (pw + pgap)
    d.rectangle([x, py, x + pw, py + ph], fill=PAPER, outline=(200, 190, 160))
    scene(x + 1, py + 1, pw - 2, 96)
    d.text((x + 10, py + 104), kick, font=F_SANSB(11), fill=RED)
    yy = para(head, F_SERIF(21), x + 10, py + 122, pw - 20, INK, lh=23)
    para(body, F_SANS(13), x + 10, yy + 4, pw - 20, GREY, lh=16)

# ---------- second row: 6 cards ----------
cards = [
    ("4  MOSCOW  •  DIPLOMACY", "US envoys head to Moscow",
     "Kushner and Witkoff fly on after Abu Dhabi talks end.", "talks"),
    ("5  UNITED STATES  •  AVIATION", "Flights resume after outage",
     "FAA ground stop ends; US air traffic normalising.", "plane"),
    ("6  WELLINGTON  •  CRICKET", "NZ bat out a draw",
     "Mitchell 49*, Phillips 26*; 120 overs after India's 720/9.", "cricket"),
    ("7  TUPANCIRETA  •  STORM", "Storm devastates town",
     "A supercell hits Tupancireta, Brazil; thousands displaced.", "storm"),
    ("8  SERANG, INDONESIA  •  FIRE", "Fire toll confirmed at 24",
     "Search goes on at the candy factory as the toll climbs.", "fire"),
    ("9  GAZA  •  REPORT", "Gaza a 'toxic wasteland'",
     "A new report details contamination left by the war.", "gaza"),
]
cx, cy, cw, ch = 24, 442, 312, 146
for i, (kick, head, body, kind) in enumerate(cards):
    x = cx + (i % 3) * (cw + pgap)
    y = cy + (i // 3) * (ch + 10)
    d.rectangle([x, y, x + cw, y + ch], fill=PAPER, outline=(200, 190, 160))
    scene_mini(x + 1, y + 1, cw - 2, 48, kind)
    d.text((x + 10, y + 56), kick, font=F_SANSB(11), fill=RED)
    yy = para(head, F_SERIF(17), x + 10, y + 74, cw - 20, INK, lh=19)
    para(body, F_SANS(12), x + 10, yy + 3, cw - 20, GREY, lh=14)

# ---------- also list ----------
ly = 752
d.text((24, ly), "ALSO ON MONDAY 23 NOVEMBER", font=F_SANSB(14), fill=INK)
d.line([24, ly + 20, W - 24, ly + 20], fill=INK, width=1)
also_left = [
    "10  NATO to meet after Poland confirms 3 Russian missiles hit it.",
    "11  Drone attacks kill 5 children in Khartoum and Omdurman.",
    "12  Paramilitary attack kills at least 24 in South Sudan.",
    "13  Thousands rally in Istanbul against media takeover.",
    "14  Houthis claim Saudi refinery attack; Saudi strike hits Hodeida.",
    "15  Belgium airports to shut in anti-austerity strike.",
    "16  Bolsonaro in intensive care with intestinal obstruction.",
    "17  Philippines documents 8,320 drug-war deaths, 2016–2022.",
    "18  Australian broadcaster Molly Meldrum dies at 83.",
    "19  Lebanese villagers return as a pilot ceasefire begins.",
    "20  China sets 2030 goals for elder and childcare.",
    "21  Taiwan stocks swing 1,578 points; TSMC turns higher.",
    "22  Taiwan bans short selling below flat price from the 23rd.",
]
also_right = [
    "23  Korea Nov exports hit record $77.4bn in 20 days.",
    "24  Meta's Wang: AI superintelligence is 'arriving'.",
    "25  Suspected Chinese hackers use AI tool Cairn on universities.",
    "26  France's top candidates both question Ukraine aid.",
    "27  Trump: Iran attacks at a year-long high.",
    "28  Fighting near Ebola area in DR Congo disrupts response.",
    "29  UK: Burnham defends EU deal; CBI presses private investment.",
    "30  Italy examines ex-police chief's papers after his death.",
    "31  French students prepare nationwide protests.",
    "32  EU and Canada plan closer AI cooperation.",
    "33  Suspected arson fire at German drone-test site.",
    "34  Attacks on West Bank medics surge 350%, rights group says.",
    "35  US intelligence chief defends Trump's 'Putin friend' remark.",
]
y = ly + 28
for t in also_left:
    y = para(t, F_SANS(10), 24, y, 470, INK, lh=12) + 1
y = ly + 28
for t in also_right:
    y = para(t, F_SANS(10), 512, y, 488, INK, lh=12) + 1

# ---------- date check + footer ----------
d.rectangle([24, 962, W - 24, 998], fill=(255, 255, 255), outline=RED)
d.text((32, 968), "DATE CHECK", font=F_SANSB(12), fill=RED)
para("Every story here happened or was first reported on Mon 23 Nov 2026 (UTC). Left out: COP31 collapse, Marquez title, Alcaraz, Liverpool 4–0 (22 Nov); El Chapo capture, Mayon eruption (21 Nov); Lagarde resignation (29 Oct); Korea $1T exports, Riemann claim (19–20 Nov).",
     F_SANS(10), 128, 968, W - 152, INK, lh=13)
centre("Sources: Reuters  •  AP  •  AFP  •  Al Jazeera  •  Cricinfo  •  ICC  •  Korea Customs  •  Nature  —  Scenes are drawn illustrations, not photographs.",
       F_SANS(10), 1004, GREY)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
