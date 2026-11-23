#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render entry.png (1024x1024) for news-image-20261123 v2.
Deterministic: no timestamp, no random, fixed layout.
Run: python3 render.py  -> writes entry.png next to this file.
Stdlib + PIL only.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
OUT = BASE / "entry.png"

W, H = 1024, 1024
MX = 26                      # side margin
GUTTER = 24
COL_W = (W - 2 * MX - GUTTER) // 2   # 474
TOP = 18
BOTTOM = 16

BLACK = (0, 0, 0)
RED = (158, 43, 37)
GREY_BG = (238, 238, 238)
GREY_LINE = (180, 180, 180)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE = "Monday, 23 November 2026  \u2022  47 STORIES  \u2022  7 REGIONS  \u2022  DATE-CHECKED"

LEAD_HEAD = "COP31 COLLAPSES"
LEAD_STANDFIRST = (
    "Climate talks fail after record overtime as fossil-fuel deadlock splits "
    "nations; EU rejects any deal without a phase-out."
)
LEAD_SUB = (
    "Talks ran into record overtime before collapsing without agreement. "
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
        "Warsaw confirms debris from Friday was Russian cruise missiles; NATO to meet.",
    ),
]

TIMELINE_TITLE = "TIMELINE \u2014 UTC"
TIMELINE = [
    "21:30 UTC 22 Nov \u2014 Netanyahu\u2013Eisenkot talks end with no deal on a government",
    "00:00 UTC \u2014 24 civilians killed in fresh South Sudan violence",
    "01:56 UTC \u2014 Trump to speak on US families at the Justice Dept., 16:30 EST",
    "22:30 UTC 22 Nov \u2014 Drone strikes hit Khartoum; WHO pleads for peace in Ebola-hit DR Congo",
    "01:00 UTC \u2014 Kim: North Korea seeks security, not supremacy",
    "02:00 UTC \u2014 Albanese: COP31 failure a sign of 'difficult geopolitical times'",
]

LEFT = [
    ("MIDDLE EAST", [
        ("HOUTHIS CLAIM STRIKES ON SAUDI REFINERY",
         "Houthi claim hits on a Saudi oil refinery and radar; at least 6 injured."),
        ("IRAN STRIKE WOUNDS TWO IN BAHRAIN",
         "Saudi Arabia condemns 'criminal' attacks after an Iran strike wounds two in Bahrain."),
        ("SETTLERS TORCH 12 VEHICLES IN WEST BANK",
         "Suspected settlers burn cars and spray graffiti in four villages near Ramallah."),
        ("SAUDI COALITION INTERCEPTS HOUTHI MISSILE",
         "Saudi-led coalition says it intercepted a Houthi missile in the western region."),
    ]),
    ("EUROPE", [
        ("DRONE KILLS 2 IN DYMER, 11 MISSING",
         "Russian drone hits a five-story block north of Kyiv; two children among the missing."),
        ("SIX KILLED IN KYIV REGION STRIKES",
         "Russian strikes in the Kyiv region kill at least six, Ukraine says."),
        ("RUSSIAN CARGO SHIP STILL BURNING OFF FINLAND",
         "A Russian cargo ship remains on fire days after an attack."),
        ("THOUSANDS MARCH IN LISBON",
         "Living costs fuel anger as thousands march in the Portuguese capital."),
        ("UK TO BUILD UKRAINIAN DRONES",
         "Britain to produce Ukrainian drones under a new agreement."),
    ]),
    ("NORTH AMERICA", [
        ("FATHER AND DAUGHTER HELD BY ICE",
         "Pair detained at Seattle airport en route to a family baptism, lawyer says."),
        ("TRUMP TO SPEAK ON US FAMILIES",
         "President to deliver remarks at the Justice Department at 16:30 EST."),
        ("TRUMP'S THIRD BID ON MIGRANT PROTECTIONS",
         "President asks the Supreme Court again to end Venezuelan migrant protections."),
        ("HEGSETH CURBS US\u2013CANADA DEFENCE TIES",
         "US Defence Secretary Pete Hegseth imposed new restrictions on the US-Canada "
         "defence relationship in a classified memo, the Washington Post reports."),
    ]),
    ("LATIN AMERICA", [
        ("EL CHAPO ISIDRO CAPTURED; 11 DEAD",
         "Mexican forces seize the FBI most-wanted cartel boss in Sinaloa; "
         "7 gunmen and 4 soldiers killed."),
        ("BOLSONARO IN INTENSIVE CARE",
         "Ex-president, 71, hospitalised with a near-complete bowel obstruction."),
    ]),
    ("MARKETS & TECH", [
        ("NVIDIA CHIEF STEPS DOWN",
         "Jensen Huang leaves as CEO; board rules out his return."),
        ("NVIDIA SPY AFFAIR",
         "Alice Huang was in contact with a Chinese spy agency officer, NYT reports, "
         "citing US intelligence."),
        ("GOLD NEARS $3,603 AN OUNCE",
         "Spot gold extends gains, up nearly 2%."),
        ("SAMSUNG SECURITIES HACKED",
         "Broker hit by a hack leaking personal data, Yonhap reports."),
        ("WERIDE EYES 1,000 ROBOTAXIS IN EUROPE",
         "Chinese self-driving firm plans a 1,000-vehicle European fleet, CEO says."),
    ]),
]

RIGHT = [
    ("SOUTH ASIA", [
        ("INDIA PUSH FOR WIN IN FIRST TEST",
         "New Zealand 157/4 at lunch on day five in the first Test."),
        ("PAKISTAN HALTS GOLD MINING IN KHYBER PAKHTUNKHWA",
         "Pakistan halts gold mining in Khyber Pakhtunkhwa amid a terror-financing "
         "and corruption probe."),
    ]),
    ("EAST ASIA & PACIFIC", [
        ("TAIWAN BANS SHORT SELLING BELOW FLAT PRICE",
         "Regulator acts from today as shares fell 17.5% in a week; index closed at 36,033."),
        ("ASIAN MARKETS ON ALERT",
         "KOSPI falls 4%; Shanghai slips below 3,500; US stocks plunged on Friday."),
        ("SHURI CASTLE REOPENS",
         "Okinawa celebrates the restored main hall, seven years after the 2019 fire."),
        ("FACTORY FIRE IN CIKANDE, BANTEN",
         "Rescuers recover bodies after a candy factory fire; dozens missing."),
        ("SOUTH KOREA MINISTER QUITS OVER AI CHEATING",
         "Education minister resigns after a university entrance exam cheating scandal."),
        ("SINGAPORE PM TO VISIT AUSTRALIA",
         "PM Wong travels from today for the annual leaders' meeting."),
    ]),
    ("AFRICA", [
        ("UKRAINIAN DRONES HIT RUSSIAN SHIP IN BENGHAZI",
         "Corvette Mercury severely damaged and later capsized; 10 injured, Libyan officials say."),
        ("24 CIVILIANS KILLED IN SOUTH SUDAN",
         "Fresh violence kills 24, officials say."),
        ("35 KILLED IN NIGERIA REVENGE ATTACKS",
         "35 Fulani killed in Kano, officials say."),
        ("WHO PLEADS FOR PEACE IN EBOLA-HIT CONGO",
         "WHO chief urges peace in Ebola-hit DR Congo area."),
    ]),
    ("SPORT, SCIENCE & CULTURE", [
        ("MARQUEZ WINS RECORD-TYING EIGHTH TITLE",
         "Marc M\u00e1rquez seals an eighth MotoGP crown in Portugal, level with Agostini."),
        ("YOUNGEST WORLD CHESS FINAL BEGINS",
         "Gukesh defends his title against Sindarov in Geneva; Game 1 starts today."),
        ("THITIKUL WINS CME FOR THIRD STRAIGHT YEAR",
         "Jeeno Thitikul takes the LPGA season finale in Florida again."),
        ("GOLDEN HORSE HONOURS 'THE VIOLINIST'",
         "Singapore film wins Best Animated Feature and Best Adapted Screenplay."),
        ("FIFA TO CONFIRM UK AS 2035 WOMEN'S WORLD CUP HOST",
         "FIFA is set to confirm on Monday that the UK will host the 2035 Women's "
         "World Cup \u2014 the first football World Cup in the UK since 1966."),
        ("ALCARAZ WINS FIRST ATP FINALS TITLE",
         "Carlos Alcaraz wins his first ATP Finals title, beating Alexander Zverev."),
    ]),
    ("WORLD", [
        ("128 STATES BACK RULES ON KILLER ROBOTS",
         "Nations agree to pursue international rules on lethal autonomous weapons by 2028."),
    ]),
]

WEEKEND_TITLE = "WEEKEND WIRE \u2014 reported Sat\u2013Sun 21\u201322 Nov"
WEEKEND = [
    ("ISRAEL COALITION TALKS FAIL",
     "Netanyahu and Eisenkot end talks without a deal on forming a government."),
    ("LAHORE WORLD'S MOST POLLUTED CITY AGAIN",
     "AQI hits 538 on Sunday morning, IQAir data show."),
    ("DRONE STRIKES HIT KHARTOUM",
     "Strikes damage a UN facility with staff inside; 3 killed in Omdurman."),
    ("LIVERPOOL 4\u20130 MAN UTD",
     "Pochettino's debut as United boss ends in a rout at Anfield; Yoro sent off in 8 minutes."),
    ("BEPICOLOMBO ENTERS MERCURY ORBIT",
     "European-Japanese craft reaches Mercury after eight years \u2014 only the second mission ever."),
]

NUMBERS = ("IN NUMBERS: $3,603 gold  \u2022  538 Lahore AQI  \u2022  1,000 robotaxis "
           "\u2022  128 states  \u2022  720/9 India in Wellington  \u2022  36,033 Taiwan index "
           "\u2022  4% KOSPI fall")
FOOTER = ("Sources: AP \u2022 Reuters \u2022 AFP \u2022 BBC \u2022 Al Jazeera \u2022 The Hindu "
          "\u2022 NYT \u2022 Yonhap \u2022 Washington Post \u2014 The world's news as reported "
          "on Monday 23 November 2026 (UTC).")


def count_stories():
    n = 1 + len(SUB_LEADS)  # lead + sub-leads
    n += sum(len(items) for _t, items in LEFT)
    n += sum(len(items) for _t, items in RIGHT)
    n += len(WEEKEND)
    return n


def font(path, size):
    return ImageFont.truetype(path, int(round(size)))


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to max_w pixels; returns list of lines (never empty)."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w) if cur else w
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def line_h(size, extra=2):
    return int(round(size)) + extra


def make_cfg(scale):
    """Font sizes for a scale factor; sub-baris never below 9 pt."""
    s = scale
    return {
        "masthead": max(30, round(38 * s)),
        "dateline": max(10, round(12 * s)),
        "lead": max(32, round(44 * s)),
        "standfirst": max(11, round(13 * s)),
        "lead_sub": max(10, round(11 * s)),
        "sublead_head": max(10, round(12 * s)),
        "sublead_sub": max(9, round(10 * s)),
        "timeline_title": max(10, round(11 * s)),
        "timeline_item": max(9, round(9.5 * s)),
        "section": max(10, round(11 * s)),
        "headline": max(10, round(11 * s)),
        "sub": max(9, round(10 * s)),
        "weekend_title": max(10, round(11 * s)),
        "weekend_head": max(10, round(11 * s)),
        "weekend_sub": max(9, round(9.5 * s)),
        "numbers": max(10, round(11 * s)),
        "footer": max(8, round(9 * s)),
        "gap": max(2, round(4 * s)),
    }


def compute(draw, cfg):
    """Measure every block with cfg; return (layout dict, total height)."""
    f = {
        "masthead": font(SERIF_BOLD, cfg["masthead"]),
        "dateline": font(SANS_BOLD, cfg["dateline"]),
        "lead": font(SERIF_BOLD, cfg["lead"]),
        "standfirst": font(SERIF, cfg["standfirst"]),
        "lead_sub": font(SANS, cfg["lead_sub"]),
        "sublead_head": font(SANS_BOLD, cfg["sublead_head"]),
        "sublead_sub": font(SANS, cfg["sublead_sub"]),
        "timeline_title": font(SANS_BOLD, cfg["timeline_title"]),
        "timeline_item": font(SANS, cfg["timeline_item"]),
        "section": font(SANS_BOLD, cfg["section"]),
        "headline": font(SANS_BOLD, cfg["headline"]),
        "sub": font(SANS, cfg["sub"]),
        "weekend_title": font(SANS_BOLD, cfg["weekend_title"]),
        "weekend_head": font(SANS_BOLD, cfg["weekend_head"]),
        "weekend_sub": font(SANS, cfg["weekend_sub"]),
        "numbers": font(SANS_BOLD, cfg["numbers"]),
        "footer": font(SANS, cfg["footer"]),
    }
    gap = cfg["gap"]
    lay = {"fonts": f}

    # Masthead / dateline / lead
    lay["masthead_h"] = line_h(cfg["masthead"], 6)
    lay["dateline_h"] = line_h(cfg["dateline"], 4)
    lay["lead_h"] = line_h(cfg["lead"], 6)
    lay["stand_lines"] = wrap(draw, LEAD_STANDFIRST, f["standfirst"], W - 2 * MX - 40)
    lay["stand_h"] = len(lay["stand_lines"]) * line_h(cfg["standfirst"], 2)
    lay["leadsub_lines"] = wrap(draw, LEAD_SUB, f["lead_sub"], W - 2 * MX - 40)
    lay["leadsub_h"] = len(lay["leadsub_lines"]) * line_h(cfg["lead_sub"], 2)

    # Sub-leads (2 columns)
    sub_cols = []
    for head, sub in SUB_LEADS:
        hl = wrap(draw, head, f["sublead_head"], COL_W)
        sl = wrap(draw, sub, f["sublead_sub"], COL_W)
        h = (len(hl) * line_h(cfg["sublead_head"], 2)
             + len(sl) * line_h(cfg["sublead_sub"], 1) + gap)
        sub_cols.append({"head_lines": hl, "sub_lines": sl, "h": h})
    lay["sublead_cols"] = sub_cols
    lay["sublead_h"] = max(c["h"] for c in sub_cols)

    # Timeline box: 3 rows x 2 columns, row-major so times read
    # chronologically left-to-right, top-to-bottom: (0,1), (2,3), (4,5).
    tl_col_w = (W - 2 * MX - 20 - 16) // 2
    tl_rows = []
    for r in range(3):
        row = [wrap(draw, TIMELINE[2 * r + c], f["timeline_item"], tl_col_w)
               for c in range(2)]
        tl_rows.append(row)
    tl_h = sum(max(len(lines) for lines in row)
               * line_h(cfg["timeline_item"], 1) + 2 for row in tl_rows)
    lay["timeline_rows"] = tl_rows
    lay["timeline_h"] = line_h(cfg["timeline_title"], 4) + tl_h + 14

    # Body columns
    def body_col(sections):
        secs = []
        total = 0
        for title, items in sections:
            its = []
            for head, sub in items:
                hl = wrap(draw, head, f["headline"], COL_W)
                sl = wrap(draw, sub, f["sub"], COL_W)
                hh = (len(hl) * line_h(cfg["headline"], 2)
                      + len(sl) * line_h(cfg["sub"], 1) + 3)
                its.append({"head_lines": hl, "sub_lines": sl, "h": hh})
                total += hh
            sh = line_h(cfg["section"], 5) + 3  # title + underline + gap
            secs.append({"title": title, "items": its, "h": sh})
            total += sh + gap
        return {"sections": secs, "h": total}

    lay["left"] = body_col(LEFT)
    lay["right"] = body_col(RIGHT)
    lay["body_h"] = max(lay["left"]["h"], lay["right"]["h"])

    # Weekend strip: 2 columns (left 3 items, right 2 items)
    wk_col_w = (W - 2 * MX - 20 - 16) // 2
    wk_cols = [[], []]
    for i, (head, sub) in enumerate(WEEKEND):
        hl = wrap(draw, head, f["weekend_head"], wk_col_w)
        sl = wrap(draw, sub, f["weekend_sub"], wk_col_w)
        h = (len(hl) * line_h(cfg["weekend_head"], 2)
             + len(sl) * line_h(cfg["weekend_sub"], 1) + 3)
        wk_cols[0 if i < 3 else 1].append(
            {"head_lines": hl, "sub_lines": sl, "h": h})
    wk_h = max(sum(it["h"] for it in col) for col in wk_cols)
    lay["weekend_cols"] = wk_cols
    lay["weekend_h"] = line_h(cfg["weekend_title"], 4) + wk_h + 14

    lay["numbers_lines"] = wrap(draw, NUMBERS, f["numbers"], W - 2 * MX)
    lay["numbers_h"] = len(lay["numbers_lines"]) * line_h(cfg["numbers"], 2)
    lay["footer_lines"] = wrap(draw, FOOTER, f["footer"], W - 2 * MX)
    lay["footer_h"] = len(lay["footer_lines"]) * line_h(cfg["footer"], 1)

    total = (lay["masthead_h"] + lay["dateline_h"] + 6
             + lay["lead_h"] + lay["stand_h"] + lay["leadsub_h"] + gap * 2
             + lay["sublead_h"] + gap
             + lay["timeline_h"] + gap
             + lay["body_h"] + gap
             + lay["weekend_h"] + gap
             + lay["numbers_h"] + gap
             + lay["footer_h"])
    lay["total"] = total
    return lay


def draw_centered(draw, y, lines, fnt, fill, lh):
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        draw.text(((W - w) / 2, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def main():
    assert count_stories() == 47, count_stories()
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Pick the first (largest) scale that fits the page.
    chosen = None
    for scale in (1.0, 0.97, 0.94, 0.91, 0.88, 0.85, 0.82, 0.80, 0.78):
        cfg = make_cfg(scale)
        lay = compute(draw, cfg)
        if lay["total"] <= H - TOP - BOTTOM:
            chosen = (cfg, lay)
            break
    if chosen is None:  # last resort: smallest scale, still all 47 stories
        cfg = make_cfg(0.78)
        lay = compute(draw, cfg)
    else:
        cfg, lay = chosen
    f = lay["fonts"]
    gap = cfg["gap"]
    y = TOP

    # Masthead + dateline
    y = draw_centered(draw, y, [MASTHEAD], f["masthead"], RED,
                      line_h(cfg["masthead"], 6))
    y = draw_centered(draw, y, [DATELINE], f["dateline"], BLACK,
                      line_h(cfg["dateline"], 4))
    draw.line([(MX, y + 2), (W - MX, y + 2)], fill=RED, width=2)
    y += 6

    # Lead
    y = draw_centered(draw, y, [LEAD_HEAD], f["lead"], RED,
                      line_h(cfg["lead"], 6))
    y = draw_centered(draw, y, lay["stand_lines"], f["standfirst"], BLACK,
                      line_h(cfg["standfirst"], 2))
    y = draw_centered(draw, y, lay["leadsub_lines"], f["lead_sub"], BLACK,
                      line_h(cfg["lead_sub"], 2))
    y += gap
    draw.line([(MX, y), (W - MX, y)], fill=GREY_LINE, width=1)
    y += gap

    # Sub-leads, 2 columns
    y0 = y
    for i, col in enumerate(lay["sublead_cols"]):
        x = MX + i * (COL_W + GUTTER)
        yy = y0
        yy = draw_lines(draw, x, yy, col["head_lines"], f["sublead_head"],
                        BLACK, line_h(cfg["sublead_head"], 2))
        draw_lines(draw, x, yy, col["sub_lines"], f["sublead_sub"],
                   BLACK, line_h(cfg["sublead_sub"], 1))
    y = y0 + lay["sublead_h"] + gap

    # Timeline box
    box_y = y
    draw.rectangle([MX, box_y, W - MX, box_y + lay["timeline_h"]],
                   fill=GREY_BG)
    ty = box_y + 6
    draw.text((MX + 10, ty), TIMELINE_TITLE, font=f["timeline_title"], fill=RED)
    ty += line_h(cfg["timeline_title"], 4)
    tl_col_w = (W - 2 * MX - 20 - 16) // 2
    for row in lay["timeline_rows"]:
        row_h = max(len(lines) for lines in row) * line_h(cfg["timeline_item"], 1)
        for c, lines in enumerate(row):
            x = MX + 10 + c * (tl_col_w + 16)
            draw_lines(draw, x, ty, lines, f["timeline_item"], BLACK,
                       line_h(cfg["timeline_item"], 1))
        ty += row_h + 2
    y = box_y + lay["timeline_h"] + gap

    # Body, 2 columns
    y0 = y
    for ci, col in enumerate((lay["left"], lay["right"])):
        x = MX + ci * (COL_W + GUTTER)
        yy = y0
        for sec in col["sections"]:
            draw.text((x, yy), sec["title"], font=f["section"], fill=RED)
            yy += line_h(cfg["section"], 2)
            draw.line([(x, yy), (x + COL_W, yy)], fill=RED, width=1)
            yy += 3
            for it in sec["items"]:
                yy = draw_lines(draw, x, yy, it["head_lines"], f["headline"],
                                BLACK, line_h(cfg["headline"], 2))
                yy = draw_lines(draw, x, yy, it["sub_lines"], f["sub"],
                                BLACK, line_h(cfg["sub"], 1))
                yy += 3
            yy += gap
    y = y0 + lay["body_h"] + gap

    # Weekend Wire box (2 columns inside the strip: 3 left, 2 right)
    box_y = y
    draw.rectangle([MX, box_y, W - MX, box_y + lay["weekend_h"]],
                   fill=GREY_BG)
    wy = box_y + 6
    draw.text((MX + 10, wy), WEEKEND_TITLE, font=f["weekend_title"], fill=RED)
    wy += line_h(cfg["weekend_title"], 4)
    wk_col_w = (W - 2 * MX - 20 - 16) // 2
    for i, col in enumerate(lay["weekend_cols"]):
        x = MX + 10 + i * (wk_col_w + 16)
        yy = wy
        for it in col:
            yy = draw_lines(draw, x, yy, it["head_lines"], f["weekend_head"],
                            BLACK, line_h(cfg["weekend_head"], 2))
            yy = draw_lines(draw, x, yy, it["sub_lines"], f["weekend_sub"],
                            BLACK, line_h(cfg["weekend_sub"], 1))
            yy += 3
    y = box_y + lay["weekend_h"] + gap

    # In numbers + footer
    y = draw_centered(draw, y, lay["numbers_lines"], f["numbers"], BLACK,
                      line_h(cfg["numbers"], 2))
    y += gap
    draw_centered(draw, y, lay["footer_lines"], f["footer"], BLACK,
                  line_h(cfg["footer"], 1))

    img.save(OUT, format="PNG")
    print(f"Wrote {OUT} ({W}x{H}, {count_stories()} stories)")


if __name__ == "__main__":
    main()
