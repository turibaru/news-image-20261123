#!/usr/bin/env python3
"""Render the front page for make.fun bounty news-image-20261123.

Deterministic: no randomness, no clock, no network. Stdlib + PIL only.
Draws a dense 1024x1024 newspaper front page and saves entry.png
next to this script.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (253, 253, 246)
INK = (17, 17, 17)
RED = (158, 43, 37)
GREY = (85, 85, 85)
FAINT = (236, 234, 224)
MARGIN = 28
GUTTER = 20
COL_W = (W - 2 * MARGIN - GUTTER) // 2  # 474

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
]


def find_font(names):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None


SERIF_B = find_font(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"])
SERIF = find_font(["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"])
SANS_B = find_font(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"])
SANS = find_font(["DejaVuSans.ttf", "LiberationSans-Regular.ttf"])


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_h(draw, text, fnt, max_w, leading):
    return len(wrap(draw, text, fnt, max_w)) * leading


def draw_wrapped(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- data
MAIN_HEADLINE = "COP31 COLLAPSES"
MAIN_SUB = (
    "Climate talks fail after record overtime as fossil-fuel deadlock "
    "splits nations; EU rejects any deal without a phase-out"
)
MAIN_SUMMARY = (
    "Talks ran into record overtime before collapsing without agreement.\n"
    "The split leaves the summit with no agreed text on phasing out fossil fuels."
)

SUB_LEADS = [
    (
        "TANKERS BURN IN THE STRAIT OF HORMUZ",
        "At least three tankers struck Fri\u2013Sat; two more hit mines on Sunday. "
        "Shipping attacks at highest level since the war began. US hawks urge "
        "new strikes on Iran; Trump says no rush.",
    ),
    (
        "POLAND: THREE OBJECTS WERE RUSSIAN MISSILES",
        "Warsaw confirms debris from Friday was Russian cruise missiles; "
        "NATO to meet.",
    ),
]

TIMELINE = [
    "21:30 UTC 22 Nov \u2014 Netanyahu\u2013Eisenkot talks end with no deal on a government",
    "22:30 UTC 22 Nov \u2014 Drone strikes hit Khartoum; WHO pleads for peace in Ebola-hit DR Congo",
    "00:00 UTC \u2014 24 civilians killed in fresh South Sudan violence",
    "01:00 UTC \u2014 Kim: North Korea seeks security, not supremacy",
    "01:56 UTC \u2014 Trump to speak on US families at the Justice Dept., 16:30 EST",
    "02:00 UTC \u2014 Albanese: COP31 failure a sign of \u2018difficult geopolitical times\u2019",
]

# (headline, summary, tag or "")
SECTIONS = [
    ("MIDDLE EAST", [
        ("HOUTHIS CLAIM STRIKES ON SAUDI REFINERY",
         "Houthis claim hits on a Saudi oil refinery and radar; at least 6 injured.", ""),
        ("IRAN STRIKE WOUNDS TWO IN BAHRAIN",
         "Saudi Arabia condemns \u2018criminal\u2019 attacks after an Iran strike wounds two in Bahrain.", ""),
        ("SETTLERS TORCH 12 VEHICLES IN WEST BANK",
         "Suspected settlers burn cars and spray graffiti in four villages near Ramallah.", ""),
        ("ISRAEL COALITION TALKS FAIL",
         "Netanyahu and Eisenkot end talks without a deal on forming a government.", "SUN 22 NOV"),
        ("SAUDI COALITION INTERCEPTS HOUTHI MISSILE",
         "Saudi-led coalition says it intercepted a Houthi missile in the western region.", ""),
    ]),
    ("EUROPE", [
        ("DRONE KILLS 2 IN DYMER, 11 MISSING",
         "Russian drone hits a five-storey block north of Kyiv; two children among the missing.", ""),
        ("SIX KILLED IN KYIV REGION STRIKES",
         "Russian strikes in the Kyiv region kill at least six, Ukraine says.", ""),
        ("RUSSIAN CARGO SHIP STILL BURNING OFF FINLAND",
         "A Russian cargo ship remains on fire days after an attack.", ""),
        ("THOUSANDS MARCH IN LISBON",
         "Living costs fuel anger as thousands march in the Portuguese capital.", ""),
        ("UK TO BUILD UKRAINIAN DRONES",
         "Britain to produce Ukrainian drones under a new agreement.", ""),
    ]),
    ("ASIA-PACIFIC", [
        ("TAIWAN BANS SHORT SELLING BELOW FLAT PRICE",
         "Regulator acts from today as shares fell 17.5% in a week; index closed at 36,033.", ""),
        ("ASIAN MARKETS ON ALERT",
         "KOSPI falls 4%; Shanghai slips below 3,500; US stocks plunged on Friday.", ""),
        ("LAHORE WORLD\u2019S MOST POLLUTED CITY AGAIN",
         "AQI hits 538 on Sunday morning, IQAir data show.", "SUN 22 NOV"),
        ("SHURI CASTLE REOPENS",
         "Okinawa celebrates the restored main hall, seven years after the 2019 fire.", ""),
        ("FACTORY FIRE IN CIKANDE, BANTEN",
         "Rescuers recover bodies after a candy factory fire; dozens missing.", ""),
        ("SOUTH KOREA MINISTER QUITS OVER AI CHEATING",
         "Education minister resigns in an AI-driven exam cheating scandal.", ""),
        ("INDIA PUSH FOR WIN IN FIRST TEST",
         "New Zealand 157/4 at lunch on day five in the first Test.", ""),
        ("SINGAPORE PM TO VISIT AUSTRALIA",
         "PM Wong travels from today for the annual leaders\u2019 meeting.", ""),
    ]),
    ("AMERICAS", [
        ("EL CHAPO ISIDRO CAPTURED; 11 DEAD",
         "Mexican forces seize the FBI most-wanted cartel boss in Sinaloa; 7 gunmen and 4 soldiers killed.", ""),
        ("BOLSONARO IN INTENSIVE CARE",
         "Ex-president, 71, hospitalised with a near-complete bowel obstruction.", ""),
        ("FATHER AND DAUGHTER HELD BY ICE",
         "Pair detained at Seattle airport en route to a family baptism, lawyer says.", ""),
        ("TRUMP TO SPEAK ON US FAMILIES",
         "President to deliver remarks at the Justice Department at 16:30 EST.", ""),
        ("TRUMP\u2019S THIRD BID ON MIGRANT PROTECTIONS",
         "President asks the Supreme Court again to end Venezuelan migrant protections.", ""),
    ]),
    ("AFRICA", [
        ("UKRAINIAN DRONES HIT RUSSIAN SHIP IN BENGHAZI",
         "Corvette Merkury severely damaged and later capsized; 10 injured, Libyan officials say.", ""),
        ("DRONE STRIKES HIT KHARTOUM",
         "Strikes damage a UN facility with staff inside; 3 killed in Omdurman.", "SUN 22 NOV"),
        ("24 CIVILIANS KILLED IN SOUTH SUDAN",
         "Fresh violence kills 24, officials say.", ""),
        ("35 KILLED IN NIGERIA REVENGE ATTACKS",
         "35 Fulanis killed in Kano, officials say.", ""),
        ("WHO PLEADS FOR PEACE IN EBOLA-HIT CONGO",
         "WHO chief urges peace in the Ebola-hit DR Congo area.", ""),
    ]),
    ("MARKETS & TECH", [
        ("NVIDIA CHIEF STEPS DOWN",
         "Jensen Huang leaves as CEO; board rules out his return.", ""),
        ("NVIDIA SPY AFFAIR",
         "Alice Huang was in contact with a Chinese spy agency officer, NYT reports, citing US intelligence.", ""),
        ("GOLD NEARS $3,603 AN OUNCE",
         "Spot gold extends gains, up nearly 2%.", ""),
        ("SAMSUNG SECURITIES HACKED",
         "Broker hit by a hack leaking personal data, Yonhap reports.", ""),
        ("WERIDE EYES 1,000 ROBOTAXIS IN EUROPE",
         "Chinese self-driving firm plans a 1,000-vehicle European fleet, CEO says.", ""),
    ]),
    ("SPORT, SCIENCE & CULTURE", [
        ("MARQUEZ WINS RECORD-TYING EIGHTH TITLE",
         "Marc Marquez seals an eighth MotoGP crown in Portugal, level with Agostini.", ""),
        ("LIVERPOOL 4\u20130 MAN UTD",
         "Pochettino\u2019s debut as United boss ends in a rout at Anfield; Yoro sent off in 8 minutes.", "SUN 22 NOV"),
        ("YOUNGEST WORLD CHESS FINAL BEGINS",
         "Gukesh defends his title against Sindarov in Geneva; Game 1 starts today.", ""),
        ("THITIKUL WINS CME FOR THIRD STRAIGHT YEAR",
         "Jeeno Thitikul takes the LPGA season finale in Florida again.", ""),
        ("BEPICOLOMBO ENTERS MERCURY ORBIT",
         "European-Japanese craft reaches Mercury after eight years \u2014 only the second mission ever.", "SAT 21 NOV"),
        ("GOLDEN HORSE HONOURS \u2018THE VIOLINIST\u2019",
         "Singapore film wins Best Animated Feature and Best Adapted Screenplay.", ""),
    ]),
    ("WORLD", [
        ("128 STATES BACK RULES ON KILLER ROBOTS",
         "Nations agree to pursue international rules on lethal autonomous weapons by 2028.", ""),
    ]),
]

# Two balanced columns (20 stories each) so both fit the page.
LEFT_COLS = ["MIDDLE EAST", "EUROPE", "AMERICAS", "MARKETS & TECH"]
RIGHT_COLS = ["ASIA-PACIFIC", "AFRICA", "SPORT, SCIENCE & CULTURE", "WORLD"]

FOOTER = (
    "Sources: AP \u2022 Reuters \u2022 AFP \u2022 BBC \u2022 Al Jazeera \u2022 The Hindu "
    "\u2022 NYT \u2022 Yonhap \u2014 The world's news as reported on Monday 23 November 2026 (UTC)."
)


def section_height(draw, titles, hl_size, sm_size):
    """Total height of a column of sections at the given font sizes."""
    hl = font(SANS_B, hl_size)
    sm = font(SANS, sm_size)
    hd = font(SANS_B, 12)
    total = 0
    by_title = dict(SECTIONS)
    for t in titles:
        total += 15 + 1 + 4  # header text + rule + gap
        for headline, summary, _tag in by_title[t]:
            total += text_h(draw, headline, hl, COL_W, hl_size + 2)
            total += text_h(draw, summary, sm, COL_W, sm_size + 2)
            total += 2  # gap between stories
        total += 6  # gap after section
    return total


def draw_column(draw, x, titles, y, hl_size, sm_size):
    hl = font(SANS_B, hl_size)
    sm = font(SANS, sm_size)
    hd = font(SANS_B, 12)
    tag_f = font(SANS_B, 9)
    by_title = dict(SECTIONS)
    for t in titles:
        draw.text((x, y), t, font=hd, fill=RED)
        y += 15
        draw.line([(x, y), (x + COL_W, y)], fill=RED, width=1)
        y += 5
        for headline, summary, tag in by_title[t]:
            y = draw_wrapped(draw, x, y, headline, hl, COL_W, hl_size + 2)
            if tag:
                tw = draw.textlength(tag, font=tag_f)
                draw.text((x + COL_W - tw, y - (hl_size + 2)), tag,
                          font=tag_f, fill=RED)
            y = draw_wrapped(draw, x, y, summary, sm, COL_W, sm_size + 2, fill=GREY)
            y += 2
        y += 6
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = 8
    # Masthead
    mast = font(SERIF_B, 42)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=mast)) / 2, y), title,
           font=mast, fill=RED)
    y += 50
    date_f = font(SANS_B, 13)
    dateline = "Monday, 23 November 2026  \u2022  43 STORIES \u2022 5 REGIONS \u2022 DATE-CHECKED"
    d.text(((W - d.textlength(dateline, font=date_f)) / 2, y), dateline,
           font=date_f, fill=INK)
    y += 19
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RED, width=3)
    y += 8

    # Main story
    main_f = font(SERIF_B, 36)
    d.text((MARGIN, y), MAIN_HEADLINE, font=main_f, fill=INK)
    y += 43
    y = draw_wrapped(d, MARGIN, y, MAIN_SUB, font(SANS, 14),
                     W - 2 * MARGIN, 17)
    y += 2
    y = draw_wrapped(d, MARGIN, y, MAIN_SUMMARY, font(SANS, 11),
                     W - 2 * MARGIN, 13, fill=GREY)
    y += 4
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
    y += 7

    # Two sub-leads side by side
    sub_hl = font(SANS_B, 15)
    sub_tx = font(SANS, 11)
    tops = []
    for i, (hl, body) in enumerate(SUB_LEADS):
        x = MARGIN + i * (COL_W + GUTTER)
        yy = draw_wrapped(d, x, y, hl, sub_hl, COL_W, 18)
        yy = draw_wrapped(d, x, yy + 2, body, sub_tx, COL_W, 13, fill=GREY)
        tops.append(yy)
    y = max(tops) + 8

    # Timeline strip (2 columns x 3 rows, grey block)
    tl_f = font(SANS, 9)
    tl_hd = font(SANS_B, 11)
    wrapped = [wrap(d, item, tl_f, COL_W) for item in TIMELINE]
    row_h = []
    for r in range(3):
        row_h.append(max(len(wrapped[r * 2]), len(wrapped[r * 2 + 1])) * 11)
    strip_h = 15 + sum(row_h) + 2 * 4 + 8
    d.rectangle([(MARGIN, y), (W - MARGIN, y + strip_h)], fill=FAINT)
    d.text((MARGIN + 8, y + 4), "TIMELINE \u2014 UTC", font=tl_hd, fill=RED)
    ty = y + 19
    for r in range(3):
        for c in range(2):
            x = MARGIN + 8 + c * (COL_W + GUTTER)
            ly = ty
            for line in wrapped[r * 2 + c]:
                d.text((x, ly), line, font=tl_f, fill=INK)
                ly += 11
        ty += row_h[r] + 4
    y = y + strip_h + 8

    # Sections: pick the largest font pair that fits the remaining space.
    footer_h = 18
    avail = (H - 4) - footer_h - 6 - y
    chosen = None
    for hl_size, sm_size in [(13, 11), (12, 10), (12, 9)]:
        need = max(section_height(d, LEFT_COLS, hl_size, sm_size),
                   section_height(d, RIGHT_COLS, hl_size, sm_size))
        if need <= avail:
            chosen = (hl_size, sm_size)
            break
    if chosen is None:
        chosen = (12, 9)
    draw_column(d, MARGIN, LEFT_COLS, y, chosen[0], chosen[1])
    draw_column(d, MARGIN + COL_W + GUTTER, RIGHT_COLS, y,
                chosen[0], chosen[1])

    # Footer
    ft = font(SANS, 10)
    d.line([(MARGIN, H - 4 - footer_h), (W - MARGIN, H - 4 - footer_h)],
           fill=INK, width=1)
    d.text(((W - d.textlength(FOOTER, font=ft)) / 2, H - 4 - footer_h + 4),
           FOOTER, font=ft, fill=GREY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    if size > 400 * 1024:
        small = img.convert("P", palette=Image.ADAPTIVE, colors=256)
        small.save(OUT, optimize=True)
        size = os.path.getsize(OUT)
    print("entry.png: %d bytes" % size)


if __name__ == "__main__":
    main()
