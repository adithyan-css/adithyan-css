"""Renders assets/skyline.svg: the last year of contributions as an isometric city.
Run:  python skyline.py [username]   (also run daily by .github/workflows/skyline.yml)"""
import re
import sys
import urllib.request
from datetime import date, datetime, timezone
from make import Doc, save, stars, TW_CSS, DISPLAY, MONO, MONOB, SPACE, LINE, TEXT, SOFT, MUTED, AMBER
import random

USER = sys.argv[1] if len(sys.argv) > 1 else "adithyan-css"


def fetch(user):
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "profile-skyline"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    days = {}
    for m in re.finditer(r'data-date="([\d-]+)"\s+id="([^"]+)"[^>]*data-level="(\d)"', html):
        days[m.group(2)] = [date.fromisoformat(m.group(1)), int(m.group(3)), 0]
    for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        if m.group(1) in days:
            n = re.match(r"([\d,]+) contribution", m.group(2))
            days[m.group(1)][2] = int(n.group(1).replace(",", "")) if n else 0
    return sorted(days.values())


# block colours per level: (top, left face, right face)
SHADES = {
    0: ("#1b1f3d", "#14172e", "#101226"),
    1: ("#5b3a2e", "#43291f", "#331f18"),
    2: ("#b0603a", "#86462a", "#6a3720"),
    3: ("#ff8c4a", "#cc6a33", "#a65327"),
    4: ("#ffc861", "#d99d3c", "#b07d2c"),
}


def render(days):
    W, H = 1000, 460
    d = Doc()
    start = days[0][0]
    cols = (days[-1][0] - start).days // 7 + 1
    s = 12.4                         # cell edge
    cx, cy = s*0.866, s*0.34         # iso basis
    ox, oy = 40, 176
    css = TW_CSS + """
.b{transform-box:fill-box;transform-origin:50% 100%;animation:rise .7s cubic-bezier(.2,.8,.2,1.2) both}
@keyframes rise{from{transform:scaleY(0)}}
"""
    rnd = random.Random(1)
    b = (f'<defs><clipPath id="cl"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
         f'<radialGradient id="bg" cx=".35" cy=".55" r=".75"><stop offset="0" stop-color="#1b1a3f"/><stop offset="1" stop-color="{SPACE}"/></radialGradient></defs>'
         f'<g clip-path="url(#cl)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{stars(rnd, W, H, 80, 14)}')
    b += d.text(MONOB, "CONTRIBUTION SKYLINE", 28, 36, 12, fill=AMBER, ls=.2)
    b += d.text(MONO, f"last 12 months · rebuilt {datetime.now(timezone.utc).date().isoformat()}", 28, 56, 11, fill=MUTED)

    cells = []
    for dt, lvl, cnt in days:
        delta = (dt - start).days
        cells.append((delta // 7, delta % 7, lvl, cnt))
    cells.sort(key=lambda t: (t[0] + t[1], t[1]))   # back-to-front
    for col, row, lvl, cnt in cells:
        x = ox + (col - row) * cx + 7*cx
        y = oy + (col + row) * cy
        h = 2 + (min(cnt, 24) * 3.6 if cnt else 0)
        top, lf, rf = SHADES[lvl]
        p_top = f"M{x:.1f} {y-h:.1f}l{cx:.2f} {cy:.2f}l{-cx:.2f} {cy:.2f}l{-cx:.2f} {-cy:.2f}Z"
        p_l = f"M{x-cx:.1f} {y-h+cy:.1f}l{cx:.2f} {cy:.2f}v{h:.1f}l{-cx:.2f} {-cy:.2f}Z"
        p_r = f"M{x:.1f} {y-h+2*cy:.1f}l{cx:.2f} {-cy:.2f}v{h:.1f}l{-cx:.2f} {cy:.2f}Z"
        g = f'<path d="{p_l}" fill="{lf}"/><path d="{p_r}" fill="{rf}"/><path d="{p_top}" fill="{top}"/>'
        if cnt:
            b += f'<g class="b" style="animation-delay:{0.3 + col*0.035:.2f}s">{g}</g>'
        else:
            b += g

    total = sum(c for _, _, c in days)
    active = sum(1 for _, _, c in days if c)
    best = cur = 0
    for _, _, c in days:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    busiest = max(days, key=lambda t: t[2])
    weekdays = [0]*7
    for dt, _, c in days:
        weekdays[dt.weekday()] += c
    top_wd = ["Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays", "Sundays"][weekdays.index(max(weekdays))]
    stats = [(f"{total:,}", "contributions"), (str(active), "active days"), (str(best), "day best streak"),
             (str(busiest[2]), f"peak · {busiest[0].strftime('%b %d')}"), (top_wd, "most active on")]
    sx, sy = 770, 112
    b += f'<path d="M{sx-28} 84V{H-40}" stroke="{LINE}"/>'
    for i, (v, lbl) in enumerate(stats):
        y = sy + i*60
        b += d.text(DISPLAY, v, sx, y, 30 if i < 4 else 22, fill=TEXT if i else AMBER)
        b += d.text(MONO, lbl, sx, y + 20, 11, fill=MUTED)
    # legend
    lx, ly = 28, H - 30
    b += d.text(MONO, "quiet", lx, ly + 4, 10, fill=MUTED)
    lx += MONO.width("quiet", 10) + 10
    for lvl in range(5):
        b += f'<rect x="{lx}" y="{ly-6}" width="12" height="12" rx="2" fill="{SHADES[lvl][0]}"/>'
        lx += 16
    b += d.text(MONO, "busy · tower height = commits that day", lx + 4, ly + 4, 10, fill=MUTED)
    b += "</g>" + f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" stroke="{LINE}"/>'
    save("skyline.svg", d.render(W, H, b, css, "Contribution skyline"))


if __name__ == "__main__":
    render(fetch(USER))
