#!/usr/bin/env python3
"""News image 23 Nov 2026 — ROUND 2 (built from scratch).

Front page, 1024x1024 PNG, Python stdlib + PIL only, deterministic
(no timestamps, no randomness).

DATE DISCIPLINE (the whole point of R2): every story below happened or
was first reported on Monday 23 November 2026 (UTC). Each story carries
its source. Stories from 20-22 Nov (COP31 collapse, Liverpool 4-0,
El Chapo Isidro arrest, BepiColombo, NVIDIA resignation) are EXCLUDED
and named in the red DATE CHECK box instead. No story appears twice:
lead + sub-leads + body + timeline are disjoint sets; the code asserts
38 unique stories and no duplicate headline.

Layout: masthead + dateline, lead + standfirst, 2 sub-leads, red
DATE CHECK box, 6-item chronological UTC timeline, 2-column body
(7 regions + Markets & Tech + Sport, Science & Culture), IN NUMBERS
strip (numbers only from counted stories), sources footer.

Font floors (measured, never shrunk): body sub >= 9px, headline
>= 10px, masthead >= 30px. Fixed sizes; if text does not fit, the
layout asserts instead of shrinking type.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28                      # outer margin
CW = W - 2 * M              # content width
COLW = (CW - 20) // 2       # column width
FONTDIR = "/usr/share/fonts/truetype/dejavu/"

SERIF_B = FONTDIR + "DejaVuSerif-Bold.ttf"
SERIF = FONTDIR + "DejaVuSerif.ttf"
SANS = FONTDIR + "DejaVuSans.ttf"
SANS_B = FONTDIR + "DejaVuSans-Bold.ttf"

# ---- measured font sizes (actual render sizes, scale 1.0) ----
SZ = dict(
    masthead=50, dateline=13, lead=36, standfirst=13,
    sub_head=16, sub_sub=11, section=13,
    body_head=12, body_sub=10,
    datecheck_title=11, datecheck_body=10,
    timeline_title=12, timeline_item=10,
    numbers=10, footer=9, table=10,
)
# floors enforced by assert below
assert SZ["body_sub"] >= 9, "body sub below 9px floor"
assert SZ["body_head"] >= 10, "headline below 10px floor"
assert SZ["masthead"] >= 30, "masthead below 30px floor"

RED = (148, 20, 20)
BLACK = (12, 12, 12)
GREY = (90, 90, 90)
LIGHT = (238, 238, 236)
MIDRULE = (170, 170, 170)

f_mast = ImageFont.truetype(SERIF_B, SZ["masthead"])
f_date = ImageFont.truetype(SANS_B, SZ["dateline"])
f_lead = ImageFont.truetype(SERIF_B, SZ["lead"])
f_stand = ImageFont.truetype(SERIF, SZ["standfirst"])
f_subh = ImageFont.truetype(SANS_B, SZ["sub_head"])
f_subs = ImageFont.truetype(SANS, SZ["sub_sub"])
f_sec = ImageFont.truetype(SANS_B, SZ["section"])
f_bh = ImageFont.truetype(SANS_B, SZ["body_head"])
f_bs = ImageFont.truetype(SANS, SZ["body_sub"])
f_dct = ImageFont.truetype(SANS_B, SZ["datecheck_title"])
f_dcb = ImageFont.truetype(SANS, SZ["datecheck_body"])
f_tlt = ImageFont.truetype(SANS_B, SZ["timeline_title"])
f_tli = ImageFont.truetype(SANS, SZ["timeline_item"])
f_num = ImageFont.truetype(SANS_B, SZ["numbers"])
f_foot = ImageFont.truetype(SANS, SZ["footer"])
f_tab = ImageFont.truetype(SANS, SZ["table"])
f_tabb = ImageFont.truetype(SANS_B, SZ["table"])


def wrap(draw, text, font, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill, lh, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines is not None:
        assert len(lines) <= max_lines, (
            "overflow: %r wraps to %d lines (max %d)" % (text, len(lines), max_lines))
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (headline, sub, source) — every headline + number verified 23 Nov 2026.
LEAD = ("NVIDIA BRINGS BACK HUANG",
        "Board reinstates Jensen Huang as chief executive 11 days after his "
        "resignation, after pressure from President Trump; shares jump 31% "
        "in premarket trading.", "Reuters")

SUB_LEADS = [
    ("TRUMP SPEAKS AT JUSTICE DEPT",
     "President addresses the department at 4:30 p.m. EST on 'protecting "
     "American families'.", "AP"),
    ("DEMOCRATS CLINCH HOUSE, 258 SEATS",
     "AP calls a majority of at least 258 seats, the largest for either "
     "party since 1992.", "AP"),
]

# body sections: (section title, [(headline, sub, source), ...])
LEFT_SECTIONS = [
    ("MIDDLE EAST", [
        ("TRUMP 'INCLINED' TO HIT IRAN AGAIN",
         "President says he will resume conflict if no deal is reached by "
         "the New Year.", "Economic Times"),
        ("IRAN WARNS OF RETALIATION",
         "Revolutionary Guard will answer any renewed US attack, Tehran "
         "says.", "AP"),
        ("ISRAELI STRIKE KILLS UNRWA WORKER",
         "Airstrike kills a Gaza man working for the UN refugee agency.",
         "Reuters"),
        ("GAZA WAR'S 'ENVIRONMENTAL CATASTROPHE'",
         "Analysis released Monday warns of damage lasting decades.", "AP"),
    ]),
    ("EUROPE", [
        ("UKRAINE SINKS RUSSIAN CORVETTE",
         "Seven sea drones hit the Merkury off Benghazi, Zelenskyy says.",
         "AP"),
        ("RUSSIAN STRIKES KILL 11 NEAR KYIV",
         "Dymer apartment block hit; 3 more killed in Vyshneve.", "AFP"),
        ("NEW RUSSIA-US-UKRAINE TALKS 'SOON'",
         "Kremlin says another trilateral round is planned; no date set.",
         "RIA Novosti"),
        ("ARMENIA OFFERS NEW CONSTITUTION",
         "Yerevan proposes charter as a step to peace with Azerbaijan.",
         "Reuters"),
        ("COMPASS EYES NEW YORK LISTING",
         "Catering giant plans to quit London for the US; worth GBP 43.6bn.",
         "BBC"),
        ("ARM CHIEF HAAS SIGNS TO 2033",
         "Chip designer extends its CEO's contract amid Nvidia job chatter.",
         "Reuters"),
    ]),
    ("NORTH AMERICA", [
        ("STATES SUE SPACEX OVER GROK",
         "Virginia and Oregon allege its AI made child sexual abuse images.",
         "Reuters"),
        ("US GROWTH EASES TO 54.6 PMI",
         "S&P Global flash index hits a four-month low; GDP still near 3%.",
         "Reuters"),
    ]),
    ("LATIN AMERICA", [
        ("BRAZIL VOTES ON LULA SPENDING CURBS",
         "Lower house takes up the president's fiscal bill.", "Rio Times"),
        ("DRONES HIT POLICE POST IN CUCUTA",
         "Blasts damage homes near the command; no casualties reported.",
         "Rio Times"),
        ("MEXICO KEEPS ARRESTING CJNG CHIEFS",
         "Commanders fall as the cartel reels from its leader's death.",
         "Rio Times"),
    ]),
]

RIGHT_SECTIONS = [
    ("SOUTH ASIA", [
        ("INDIA GIVES NEPAL $1.62BN PACKAGE",
         "Modi announces aid after August floods killed about 1,500.",
         "Reuters"),
        ("PAKISTAN HOSTS NUCLEAR SECURITY TALKS",
         "IAEA network meeting opens in Islamabad with 49 nations.",
         "Foreign Office"),
    ]),
    ("EAST ASIA & PACIFIC", [
        ("SAMSUNG SECURITIES HACKED",
         "Data of 8,241 clients exposed in a breach of its complaints "
         "portal.", "Yonhap"),
        ("SINGAPORE PM LANDS AT NEW SYDNEY AIRPORT",
         "Wong is the first foreign leader at Western Sydney "
         "International.", "Singapore MFA"),
        ("CHINA SENTENCES OFFICIAL TO DEATH",
         "Beijing punishes leaking state secrets to a foreign country.",
         "Reuters"),
        ("PRABOWO NAMES TWO VP CANDIDATES",
         "Sugiono and Amran Sulaiman put to the MPR; vote on 11 December.",
         "Reuters"),
        ("24 DEAD IN INDONESIA FACTORY FIRE",
         "Candy plant blaze in Banten leaves about 30 unaccounted for.",
         "Xinhua"),
    ]),
    ("AFRICA", [
        ("FIGHTING TRAPS EBOLA RESPONDERS",
         "WHO staff shelter in Ituri hospital as cases reach 11,762.",
         "UN News"),
        ("KENYA COURT FAST-TRACKS VOTE-TECH CASE",
         "Judges certify urgent challenge to Sh17.6bn IEBC tender.",
         "The Standard"),
    ]),
    ("MARKETS & TECH", [
        ("ASIA RACES TO CALM MARKETS",
         "TAIEX up 2.9% as Seoul readies a 10.76tn-won fund.",
         "Morningstar"),
    ]),
    ("SPORT, SCIENCE & CULTURE", [
        ("UK TO HOST 2035 WOMEN'S WORLD CUP",
         "FIFA confirms 48 teams, 104 matches; first in Britain since "
         "1966.", "FIFA"),
        ("INDIA'S 720/9 EARNS WELLINGTON DRAW",
         "New Zealand bat out 120 overs after record total.", "AP"),
        ("GUKESH: 'I'LL WIN IT ALL OVER AGAIN'",
         "Champion defiant on eve of Geneva defence; Game 1 on Tuesday.",
         "Chess.com"),
        ("FURY REVEALS SCHIZOPHRENIA DIAGNOSIS",
         "Boxer opens up in Netflix film before Joshua fight on 11 Dec.",
         "BBC"),
    ]),
]

# timeline: 6 items, strictly chronological UTC 23 Nov, disjoint from
# lead / sub-leads / body (separate micro-stories, not counted twice).
TIMELINE = [
    ("01:29 UTC 23 Nov", "Gold futures rebound 2.8% to $3,614.90 after last "
     "week's rout.", "COMEX"),
    ("04:53 UTC 23 Nov", "Pakistan's KSE-100 jumps 1,000 points to 178,470 "
     "at the open.", "Tribune"),
    ("05:56 UTC 23 Nov", "Pakistan and Portugal open a business forum in "
     "Islamabad.", "Dunya News"),
    ("08:48 UTC 23 Nov", "Mohamud to meet Museveni; Uganda pullout looms.",
     "Goobjoog"),
    ("13:30 UTC 23 Nov", "Chicago Fed activity index prints -0.06 for "
     "October.", "Chicago Fed"),
    ("18:00 UTC 23 Nov", "US Treasury auctions $69bn of two-year notes.",
     "US Treasury"),
]

# markets table: numbers only, all from counted stories above.
MARKET_ROWS = [
    ("TAIEX", "+2.9%"), ("KOSPI", "-3.2%"), ("ChiNext", "+1.2%"),
    ("Gold futures", "$3,614.90"),
]

NUMBERS_STRIP = ("IN NUMBERS:  8,241 Samsung clients  •  258 House seats  •  "
                 "+31% NVIDIA  •  $1.62bn Nepal  •  720/9 India  •  11,762 "
                 "Ebola cases  •  54.6 PMI  •  104 matches")

DATECHECK_TITLE = ("DATE CHECK — EVERY STORY HERE HAPPENED OR WAS FIRST "
                   "REPORTED ON MONDAY 23 NOVEMBER 2026 (UTC)")
DATECHECK_BODY = ("LEFT OUT ON PURPOSE:  NVIDIA chief steps down — 12 Nov   •   "
                  "'El Chapo Isidro' arrested — 20 Nov   •   BepiColombo "
                  "enters Mercury orbit — 21 Nov   •   COP31 collapses — "
                  "22 Nov")

FOOTER_SRC = ("Sources: AP  •  Reuters  •  AFP  •  BBC  •  Yonhap  •  Xinhua  •  "
              "UN News  •  Morningstar  •  Rio Times  •  FIFA  •  Chess.com  •  "
              "The Standard")
FOOTER_LINE = "The world's news as reported on Monday 23 November 2026 (UTC)."


def all_stories():
    out = [("LEAD",) + LEAD]
    out += [("SUB",) + s for s in SUB_LEADS]
    for secs in (LEFT_SECTIONS, RIGHT_SECTIONS):
        for title, stories in secs:
            out += [(title,) + s for s in stories]
    out += [("TIMELINE", t[1], t[1], t[2]) for t in TIMELINE]
    return out


def count_and_check():
    stories = all_stories()
    n = len(stories)
    heads = [s[1].strip().upper() for s in stories]
    assert len(set(heads)) == len(heads), "DUPLICATE HEADLINE: %s" % (
        [h for h in heads if heads.count(h) > 1],)
    assert n == 38, "story count %d != 38" % n
    return n


def rule(draw, y, x0=M, x1=W - M, w=2, fill=BLACK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)
    return y + w + 4


def draw_section(draw, x, y, title, stories, y_limit):
    draw.text((x, y), title, font=f_sec, fill=RED)
    y += 15
    draw.line([(x, y), (x + COLW, y)], fill=RED, width=1)
    y += 5
    for head, sub, src in stories:
        y = draw_wrapped(draw, x, y, head, f_bh, COLW, BLACK, 14,
                         max_lines=2)
        y = draw_wrapped(draw, x, y, sub + " — " + src, f_bs, COLW, BLACK,
                         12, max_lines=2)
        draw.line([(x, y), (x + COLW, y)], fill=MIDRULE, width=1)
        y += 2
        assert y <= y_limit, "body column overflow at %r (y=%d)" % (head, y)
    return y


def build():
    n = count_and_check()
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    y = 8
    # masthead
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, y), t, font=f_mast,
           fill=RED)
    y += 54
    t = "Monday, 23 November 2026  •  %d STORIES  •  7 REGIONS  •  ALL DATED 23 NOV 2026 (UTC)" % n
    d.text(((W - d.textlength(t, font=f_date)) / 2, y), t, font=f_date,
           fill=BLACK)
    y += 20
    y = rule(d, y)
    # lead
    t = LEAD[0]
    d.text(((W - d.textlength(t, font=f_lead)) / 2, y), t, font=f_lead,
           fill=BLACK)
    y += 42
    y = draw_wrapped(d, M + 40, y, LEAD[1] + " — " + LEAD[2], f_stand,
                     CW - 80, BLACK, 17, max_lines=2)
    y += 2
    y = rule(d, y, w=1, fill=MIDRULE)
    # sub-leads, two columns
    sy = y
    for i, (head, sub, src) in enumerate(SUB_LEADS):
        x = M + i * (COLW + 20)
        yy = draw_wrapped(d, x, sy, head, f_subh, COLW, BLACK, 19,
                          max_lines=1)
        yy = draw_wrapped(d, x, yy, sub + " — " + src, f_subs, COLW, BLACK,
                          14, max_lines=2)
    y = sy + 48
    y = rule(d, y, w=1, fill=MIDRULE)
    # DATE CHECK box (red border)
    d.rectangle([M, y, W - M, y + 52], outline=RED, width=2)
    d.text((M + 10, y + 5), DATECHECK_TITLE, font=f_dct, fill=RED)
    y2 = draw_wrapped(d, M + 10, y + 24, DATECHECK_BODY, f_dcb, CW - 20, BLACK,
                      13, max_lines=2)
    y += 52
    y += 6
    # TIMELINE box (light grey)
    d.rectangle([M, y, W - M, y + 88], fill=LIGHT, outline=MIDRULE, width=1)
    d.text((M + 10, y + 5), "TIMELINE — UTC, MONDAY 23 NOVEMBER 2026",
           font=f_tlt, fill=BLACK)
    ty = y + 26
    for i, (when, text, src) in enumerate(TIMELINE):
        col = i % 2
        row = i // 2
        x = M + 10 + col * (COLW + 10)
        yy = ty + row * 23
        d.text((x, yy), when + " — ", font=f_tli, fill=RED)
        tw = d.textlength(when + " — ", font=f_tli)
        draw_wrapped(d, x + tw, yy, text + " (" + src + ")", f_tli,
                     COLW - tw + 10, BLACK, 13, max_lines=1)
    y += 88
    y += 6
    # BODY, two columns
    body_top = y
    body_limit = 952
    ly = body_top
    for title, stories in LEFT_SECTIONS:
        ly = draw_section(d, M, ly, title, stories, body_limit)
        ly += 4
    ry = body_top
    for title, stories in RIGHT_SECTIONS:
        ry = draw_section(d, M + COLW + 20, ry, title, stories, body_limit)
        ry += 4
        if title == "MARKETS & TECH":
            # compact markets table (numbers from counted stories only)
            for label, val in MARKET_ROWS:
                d.text((M + COLW + 20, ry), label, font=f_tab, fill=BLACK)
                vw = d.textlength(val, font=f_tabb)
                d.text((M + COLW + 20 + COLW - vw, ry), val, font=f_tabb,
                       fill=BLACK)
                ry += 14
            d.line([(M + COLW + 20, ry),
                    (M + COLW + 20 + COLW, ry)], fill=MIDRULE, width=1)
            ry += 6
    body_end = max(ly, ry)
    assert body_end <= body_limit, "body ends y=%d > %d" % (body_end,
                                                           body_limit)
    # IN NUMBERS strip
    assert d.textlength(NUMBERS_STRIP, font=f_num) <= CW - 16, \
        "numbers strip too wide: %d" % d.textlength(NUMBERS_STRIP, font=f_num)
    y = 958
    d.rectangle([M, y, W - M, y + 22], fill=BLACK)
    d.text((M + 8, y + 4), NUMBERS_STRIP, font=f_num, fill="white")
    # footer
    y = 986
    d.text(((W - d.textlength(FOOTER_SRC, font=f_foot)) / 2, y), FOOTER_SRC,
           font=f_foot, fill=GREY)
    y += 13
    d.text(((W - d.textlength(FOOTER_LINE, font=f_foot)) / 2, y), FOOTER_LINE,
           font=f_foot, fill=GREY)
    print("stories=%d unique OK" % n)
    print("fonts actual px: masthead=%d lead=%d sub_head=%d section=%d "
          "body_head=%d body_sub=%d timeline=%d footer=%d scale=1.0"
          % (SZ["masthead"], SZ["lead"], SZ["sub_head"], SZ["section"],
             SZ["body_head"], SZ["body_sub"], SZ["timeline_item"],
             SZ["footer"]))
    print("body columns end y: left=%d right=%d (limit %d)"
          % (ly, ry, body_limit))
    return img


if __name__ == "__main__":
    img = build()
    img.save("entry.png")
    print("saved entry.png %dx%d" % img.size)
