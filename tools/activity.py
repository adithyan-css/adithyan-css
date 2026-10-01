"""Renders assets/activity.svg from the live GitHub contribution calendar.
A highlighter sweeps the year and inks each day as it passes.
Run:  python activity.py [username]   (also run daily by .github/workflows/activity.yml)"""
import re
import sys
import urllib.request
from datetime import date, datetime, timezone
from make import (Doc, save, sheet, rule, star, CSS, PAPER, INK, INK2, GREY, MARK,
                  SERIF, SERIFI, MONO, MONOB)

USER = sys.argv[1] if len(sys.argv) > 1 else "adithyan-css"


def fetch(user):
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "profile-activity"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    days = {}
    for m in re.finditer(r'data-date="([\d-]+)"\s+id="([^"]+)"[^>]*data-level="(\d)"', html):
        days[m.group(2)] = [date.fromisoformat(m.group(1)), int(m.group(3)), 0]
    for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        if m.group(1) in days:
            n = re.match(r"([\d,]+) contribution", m.group(2))
            days[m.group(1)][2] = int(n.group(1).replace(",", "")) if n else 0
    return sorted(days.values())


def streak(days):
    best = cur = 0
    for _, _, c in days:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    return best


def render(days):
    W, H = 1000, 352
    d = Doc()
    start = days[0][0]
    cols = (days[-1][0] - start).days // 7 + 1
    cell, gap = 12.5, 3.6
    pitch = cell + gap
    x0 = 76
    y0 = 92
    gw = cols * pitch - gap
    step, cycle = 0.07, 11.0
    sweep = cols * step

    css = CSS + f"""
.ink{{animation:ink {cycle}s linear infinite both}}
@keyframes ink{{0%{{opacity:0;transform:scale(.4)}}3%{{opacity:1;transform:scale(1)}}82%{{opacity:1;transform:scale(1)}}86%,100%{{opacity:0;transform:scale(.4)}}}}
.ink{{transform-box:fill-box;transform-origin:center}}
.pen{{animation:pen {cycle}s linear infinite}}
@keyframes pen{{0%{{transform:translateX(0);opacity:1}}{sweep/cycle*100:.1f}%{{transform:translateX({gw+8:.1f}px);opacity:1}}{sweep/cycle*100+2:.1f}%,100%{{transform:translateX({gw+8:.1f}px);opacity:0}}}}
.ring{{animation:ring 1.6s ease-in-out infinite}}@keyframes ring{{50%{{opacity:.35}}}}
"""
    b = sheet(W, H)
    b += d.text(MONOB, "ACTIVITY", 26, 24, 11, fill=INK, ls=.08)
    b += d.text(MONO, "— THE LAST TWELVE MONTHS, INKED ONE DAY AT A TIME",
                26 + MONOB.width("ACTIVITY", 11, .08) + 8, 24, 11, fill=GREY, ls=.04)
    today = datetime.now(timezone.utc).date().isoformat()
    b += d.text(MONO, f"UPDATED {today}", W - 26, 24, 11, fill=INK, anchor="end", ls=.08)
    b += rule(37, W)

    # month + weekday labels
    seen = set()
    for dt, _, _ in days:
        if dt.day <= 7 and dt.weekday() == 6 and (dt.year, dt.month) not in seen:
            seen.add((dt.year, dt.month))
            col = (dt - start).days // 7
            if col < cols - 2:
                b += d.text(MONO, dt.strftime("%b").upper(), x0 + col*pitch, y0 - 12, 9.5, fill=GREY, ls=.06)
    for r, lbl in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b += d.text(MONO, lbl, x0 - 12, y0 + r*pitch + cell - 2, 9, fill=GREY, anchor="end", ls=.06)

    # cells
    busiest = max(days, key=lambda t: t[2])
    shades = {1: .28, 2: .52, 3: .78, 4: 1}
    for dt, lvl, cnt in days:
        delta = (dt - start).days
        col, row = delta // 7, delta % 7
        x, y = x0 + col*pitch, y0 + row*pitch
        b += f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2" stroke="#d3cbbb" stroke-width="1"/>'
        if lvl:
            b += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2" fill="{INK}" '
                  f'fill-opacity="{shades[lvl]}" class="ink" style="animation-delay:{col*step:.2f}s"/>')
        if busiest[2] and (dt, cnt) == (busiest[0], busiest[2]):
            bx, by = x + cell/2, y + cell/2
            b += f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{cell*.95:.1f}" stroke="{MARK}" stroke-width="3" class="ring"/>'

    # highlighter pen
    gh = 7*pitch - gap
    b += (f'<g class="pen"><rect x="{x0-10}" y="{y0-6}" width="14" height="{gh+12:.1f}" rx="3" '
          f'fill="{MARK}" fill-opacity=".75" style="mix-blend-mode:multiply"/>'
          f'<rect x="{x0-10}" y="{y0-12}" width="14" height="6" rx="1" fill="{INK}"/></g>')

    # legend
    ly = y0 + gh + 22
    lx = x0 + gw
    b += d.text(MONO, "MORE", lx, ly + 9, 9, fill=GREY, anchor="end", ls=.06)
    lx -= MONO.width("MORE", 9, .06) + 8
    for lvl in (4, 3, 2, 1, 0):
        lx -= cell
        fill = f'fill="{INK}" fill-opacity="{shades[lvl]}"' if lvl else ""
        b += f'<rect x="{lx:.1f}" y="{ly}" width="{cell}" height="{cell}" rx="2" stroke="#d3cbbb" {fill}/>'
        lx -= 3.6
    b += d.text(MONO, "LESS", lx - 4, ly + 9, 9, fill=GREY, anchor="end", ls=.06)
    b += f'<circle cx="{x0+6}" cy="{ly+6}" r="6" stroke="{MARK}" stroke-width="3"/>'
    lbl = f"busiest day — {busiest[2]} on {busiest[0].strftime('%b %d').replace(' 0', ' ')}" if busiest[2] else "a quiet year, so far"
    b += d.text(SERIFI, lbl, x0 + 20, ly + 11, 17, fill=INK2)

    # stats
    total = sum(c for _, _, c in days)
    active = sum(1 for _, _, c in days if c)
    stats = [(f"{total:,}", "CONTRIBUTIONS IN A YEAR"), (str(active), "DAYS WITH COMMITS"),
             (str(streak(days)), "LONGEST STREAK, DAYS"), (str(busiest[2]), "MOST IN ONE DAY")]
    b += rule(268, W)
    cw = (W - 3) / 4
    for i, (v, cap) in enumerate(stats):
        x = 1.5 + i*cw
        if i:
            b += f'<path d="M{x:.1f} 268V{H-1.5}" stroke="{INK}" stroke-width="1.2"/>'
        b += d.text(SERIF, v, x + 24, 322, 46, fill=INK)
        b += d.text(MONO, cap, x + 30 + SERIF.width(v, 46), 318, 9.5, fill=GREY, ls=.06)
    b += star(W - 30, 290, 7)
    save("activity.svg", d.render(W, H, b, css, "Activity — the last twelve months"))


if __name__ == "__main__":
    render(fetch(USER))
