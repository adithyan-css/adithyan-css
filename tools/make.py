"""Generates the SVG artwork for the adithyan-css profile README.
Run:  python make.py   (writes ../assets/*.svg)"""
import math
import random
from pathlib import Path
from svgtext import Face, Doc

OUT = Path(__file__).parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# ── tokens ────────────────────────────────────────────────────────────────
BG, BG2, PANEL = "#070b10", "#0b1219", "#0d151d"
LINE, DIMLINE = "#1c2a35", "#13202a"
TEXT, SOFT, MUTED = "#e6f1f3", "#a9c3c9", "#5f7a83"
TEAL, CYAN, MINT = "#2dd4bf", "#38bdf8", "#99f6e4"
WARN, BAD = "#fbbf24", "#fb7185"

SANSB = Face("sb", "InterTight.ttf", wght=900)
SANSM = Face("sm", "InterTight.ttf", wght=600)
MONO = Face("mo", "JetBrainsMono.ttf", wght=400)
MONOB = Face("mb", "JetBrainsMono.ttf", wght=700)


def save(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")
    print(f"{name:20s} {len(svg)/1024:6.1f} KB")


def check(x, y, s=8, color=TEAL):
    return f'<path d="M{x} {y+s*.55}L{x+s*.38} {y+s}L{x+s} {y}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'


def cross(x, y, s=8, color=BAD):
    return f'<path d="M{x} {y}L{x+s} {y+s}M{x+s} {y}L{x} {y+s}" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>'


def window(d, W, H, title, dots=(TEAL, CYAN, MUTED)):
    s = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
         f'<path d="M1 42H{W-1}" stroke="{LINE}"/>')
    for i, c in enumerate(dots):
        s += f'<circle cx="{24 + i*20}" cy="21" r="5.5" fill="{c}" opacity=".85"/>'
    s += d.text(MONO, title, W/2, 26, 12, fill=MUTED, anchor="middle")
    return s


# ══════════════════════════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════════════════════════
def banner():
    W, H = 1200, 400
    d = Doc()
    rnd = random.Random(42)
    css = """
.hot{animation:hot 2.4s ease-in-out infinite}@keyframes hot{50%{opacity:.25}}
.grid{animation:gridmv 6s linear infinite}@keyframes gridmv{to{transform:translateY(40px)}}
.wave{animation:wave 4s linear infinite}@keyframes wave{to{transform:translateX(-160px)}}
.rise{animation:rise 1s cubic-bezier(.2,.7,.2,1) both}@keyframes rise{from{opacity:0;transform:translateY(14px)}}
"""
    b = ('<defs>'
         f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#03161b"/>'
         f'<stop offset=".55" stop-color="#071a24"/><stop offset="1" stop-color="#0a0f1e"/></linearGradient>'
         f'<radialGradient id="glow" cx=".23" cy=".5" r=".45"><stop offset="0" stop-color="{TEAL}" stop-opacity=".22"/>'
         f'<stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="{TEAL}" stop-opacity=".35"/></linearGradient>'
         f'<linearGradient id="nameG" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{MINT}"/></linearGradient>'
         f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
         f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{TEAL}" opacity=".13"/></pattern>'
         '</defs>')
    b += f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#bg)"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#dots)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>'

    # perspective floor grid, bottom
    hy = 300
    floor = "".join(f'<path d="M{600 + (i-15)*20} {hy}L{600 + (i-15)*130} {H}" stroke="{TEAL}" stroke-opacity=".10"/>' for i in range(31))
    rows = "".join(f'<path d="M0 {hy + k*k*2.2 + 4:.1f}H{W}" stroke="{TEAL}" stroke-opacity=".10"/>' for k in range(1, 14))
    b += f'<g>{floor}<clipPath id="fl"><rect y="{hy}" width="{W}" height="{H-hy}"/></clipPath><g clip-path="url(#fl)"><g class="grid">{rows}</g></g></g>'

    # radar + node network, left
    cx, cy = 260, 190
    for r in (55, 105, 155):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{TEAL}" stroke-opacity=".16"/>'
    b += f'<path d="M{cx-170} {cy}H{cx+170}M{cx} {cy-170}V{cy+170}" stroke="{TEAL}" stroke-opacity=".08"/>'
    b += (f'<g><path d="M{cx} {cy}L{cx+155} {cy}A155 155 0 0 0 {cx + 155*math.cos(math.radians(-38)):.1f} {cy + 155*math.sin(math.radians(-38)):.1f}Z" fill="url(#sweep)"/>'
          f'<path d="M{cx} {cy}L{cx+155} {cy}" stroke="{TEAL}" stroke-width="1.5" stroke-opacity=".8"/>'
          f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="6s" repeatCount="indefinite"/></g>')
    nodes = []
    while len(nodes) < 15:
        a, r = rnd.uniform(0, 2*math.pi), rnd.uniform(30, 150)
        p = (cx + r*math.cos(a), cy + r*math.sin(a)*.9)
        if all(math.dist(p, q) > 42 for q in nodes):
            nodes.append(p)
    edges = []
    for i, p in enumerate(nodes):
        near = sorted(range(len(nodes)), key=lambda j: math.dist(p, nodes[j]))[1:3]
        for j in near:
            if (j, i) not in edges:
                edges.append((i, j))
    for k, (i, j) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        b += f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{TEAL}" stroke-opacity=".28"/>'
        if k % 2 == 0:
            b += (f'<circle r="2.2" fill="{MINT}"><animateMotion dur="{rnd.uniform(1.8,3.2):.1f}s" begin="{rnd.uniform(0,2):.1f}s" '
                  f'repeatCount="indefinite" path="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"/></circle>')
    for k, (x, y) in enumerate(nodes):
        hot = k % 4 == 0
        if hot:
            b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{TEAL}" opacity=".25" class="hot" style="animation-delay:{k*.3:.1f}s"/>'
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.6 if hot else 2.6}" fill="{MINT if hot else TEAL}"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="5" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="12" stroke="#fff" stroke-opacity=".4"/>'

    # text, right
    tx = 500
    b += f'<g class="rise">{d.text(MONOB, "// EDGE AI · FORECASTING · ROBOTICS · SECURITY", tx, 112, 13, fill=TEAL, ls=.14)}</g>'
    size = 104
    while SANSB.width("ADITHYAN", size, -.01) > 640:
        size -= 1
    b += f'<g class="rise" style="animation-delay:.12s">{d.text(SANSB, "ADITHYAN", tx - 4, 206, size, fill="url(#nameG)", ls=-.01)}</g>'
    k = size / SANSB.upm
    b += (f'<g class="rise" style="animation-delay:.24s">' +
          d.text(SANSB, "C S S", tx - 2, 206 + size*.9, size*.72, fill="none", ls=.02,
                 extra=f' stroke="{TEAL}" stroke-width="{1.6/(k*.72):.1f}"') + "</g>")
    tag = "building systems that sense, predict & recover."
    nx = tx + SANSB.width("C S S", size*.72, .02) + 26
    b += f'<g class="rise" style="animation-delay:.36s">{d.text(MONO, tag, nx, 206 + size*.9 - 8, 15.5, fill=SOFT)}</g>'

    # waveform strip
    wy = 345
    pts = "".join(f"{'M' if i == 0 else 'L'}{tx + i*4} {wy + 9*math.sin(i*.42)*math.sin(i*.07):.1f}" for i in range(220))
    b += (f'<clipPath id="wc"><rect x="{tx}" y="{wy-20}" width="{W-tx-40}" height="40"/></clipPath>'
          f'<g clip-path="url(#wc)"><g class="wave"><path d="{pts}" stroke="{TEAL}" stroke-opacity=".55" stroke-width="1.4"/></g></g>')
    b += "</g>"
    b += f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" stroke="{TEAL}" stroke-opacity=".25"/>'
    save("banner.svg", d.render(W, H, b, css, "Adithyan C S S — building systems that sense, predict & recover"))


# ══════════════════════════════════════════════════════════════════════════
# DIVIDER
# ══════════════════════════════════════════════════════════════════════════
def divider():
    W, H = 1000, 16
    d = Doc()
    css = ".glint{animation:glint 3.5s ease-in-out infinite}@keyframes glint{from{transform:translateX(-220px)}to{transform:translateX(1000px)}}"
    b = (f'<defs><linearGradient id="dl" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{TEAL}" stop-opacity=".5"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>'
         f'<linearGradient id="gl" x1="0" x2="1"><stop offset="0" stop-color="{MINT}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{MINT}"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></linearGradient></defs>'
         f'<rect y="7.5" width="{W}" height="1" fill="url(#dl)"/>'
         f'<g class="glint"><rect y="6.5" width="220" height="3" rx="1.5" fill="url(#gl)"/></g>'
         f'<path d="M{W/2} 3L{W/2+5} 8L{W/2} 13L{W/2-5} 8Z" fill="{TEAL}"/>')
    save("divider.svg", d.render(W, H, b, css))


# ══════════════════════════════════════════════════════════════════════════
# ABOUT — terminal that types itself
# ══════════════════════════════════════════════════════════════════════════
def terminal():
    W = 1000
    d = Doc()
    fs, lh = 14.5, 25
    script = [
        ("cmd", "whoami"),
        ("out", [("adithyan", TEXT), (" — I build systems that ", SOFT), ("sense", TEAL), (", ", SOFT),
                 ("predict", TEAL), (" and ", SOFT), ("recover", TEAL), (".", SOFT)]),
        ("cmd", "cat focus.txt"),
        ("out", [("edge AI on tiny hardware · time-series forecasting · robot safety · web security", SOFT)]),
        ("cmd", "ls ~/projects"),
        ("out", [("ridershield-ai/  ", CYAN), ("agriprice-ai/  ", CYAN), ("roboguard/  ", CYAN),
                 ("helix/  ", CYAN), ("kaaval/  ", CYAN), ("smart-rover/", CYAN)]),
        ("cmd", "./principles --list"),
        ("out", [("1. ", MUTED), ("if it isn’t real-time, it doesn’t count", SOFT)]),
        ("out", [("2. ", MUTED), ("models should fit where they run", SOFT)]),
        ("out", [("3. ", MUTED), ("design for the failure case first", SOFT)]),
    ]
    H = 62 + len(script)*lh + lh + 18
    b = window(d, W, H, "adithyan@dev: ~")
    css = ("@keyframes show{from{opacity:0}to{opacity:1}}"
           ".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}")
    prompt = "❯" if ord("❯") in MONOB.cmap else ">"
    t, y, x0 = 0.4, 72, 28
    for i, (kind, val) in enumerate(script):
        if kind == "cmd":
            tw, n = MONO.width(val, fs), len(val)
            dur = n * 0.055
            cls = f"t{i}"
            css += (f".{cls}{{animation:{cls} {dur:.2f}s steps({n}) {t:.2f}s both}}"
                    f"@keyframes {cls}{{to{{transform:translateX({tw+2:.1f}px)}}}}")
            g = (d.text(MONOB, prompt, x0, y, fs, fill=TEAL) + d.text(MONO, val, x0 + 22, y, fs, fill=TEXT)
                 + f'<rect x="{x0+20}" y="{y-fs-2}" width="{tw+40:.1f}" height="{lh}" fill="{PANEL}" class="{cls}"/>')
            b += f'<g style="animation:show .01s {t:.2f}s both">{g}</g>'
            t += dur + 0.3
        else:
            x, row = x0 + 22, ""
            for txt, col in val:
                row += d.text(MONO, txt, x, y, fs, fill=col)
                x += MONO.width(txt, fs)
            b += f'<g style="animation:show .01s {t:.2f}s both">{row}</g>'
            t += 0.2
        y += lh
    b += (f'<g style="animation:show .01s {t:.2f}s both">{d.text(MONOB, prompt, x0, y, fs, fill=TEAL)}'
          f'<rect x="{x0+22}" y="{y-fs+1}" width="9" height="{fs+3}" fill="{TEAL}" class="cur"/></g>')
    save("terminal.svg", d.render(W, H, b, css, "about"))


# ══════════════════════════════════════════════════════════════════════════
# CONSOLE — three auto-cycling project traces
# ══════════════════════════════════════════════════════════════════════════
def console():
    W, H = 1000, 380
    d = Doc()
    C = 18.0          # full cycle
    seg = C / 3
    css = f"""
.pane{{animation:pane {C}s linear infinite both}}
@keyframes pane{{0%{{opacity:0}}1.5%,31.5%{{opacity:1}}33.3%,100%{{opacity:0}}}}
.tab{{animation:tab {C}s linear infinite both}}
@keyframes tab{{0%,33.2%{{fill:{TEAL}}}33.3%,100%{{fill:{MUTED}}}}}
.bar{{animation:bar {C}s linear infinite both}}
@keyframes bar{{0%,33.2%{{opacity:1}}33.3%,100%{{opacity:0}}}}
.rv{{animation:rv {C}s linear infinite both}}
@keyframes rv{{0%{{opacity:0;transform:translateX(-6px)}}1%,100%{{opacity:1;transform:translateX(0)}}}}
.lane{{animation:lane .7s linear infinite}}@keyframes lane{{to{{stroke-dashoffset:-16}}}}
.jit{{animation:jit 2.5s ease-in-out infinite}}@keyframes jit{{50%{{transform:translate(3px,2px)}}}}
.cur{{animation:cur 4s linear infinite}}@keyframes cur{{from{{transform:translateX(0)}}to{{transform:translateX(400px)}}}}
.blink{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:.2}}}}
"""
    b = window(d, W, H, "~/console — live traces")
    tabs = ["ridershield", "roboguard", "kaaval"]
    tx = 28
    for i, t in enumerate(tabs):
        tw = MONOB.width(t, 12)
        a, z = i*100/3, (i+1)*100/3
        if i == 0:
            kf = lambda on, off: f"0%,{z-.2:.1f}%{{{on}}}{z:.1f}%,100%{{{off}}}"
        else:
            kf = lambda on, off: f"0%,{a-.2:.1f}%{{{off}}}{a:.1f}%,{z-.2:.1f}%{{{on}}}{min(z, 100):.1f}%,100%{{{off}}}" if i < 2 else f"0%,{a-.2:.1f}%{{{off}}}{a:.1f}%,99.8%{{{on}}}100%{{{off}}}"
        css += (f"@keyframes tab{i}{{{kf('fill:' + TEAL, 'fill:' + MUTED)}}}"
                f"@keyframes bar{i}{{{kf('opacity:1', 'opacity:0')}}}")
        b += f'<g style="animation:tab{i} {C}s linear infinite">{d.text(MONOB, t, tx, 72, 12)}</g>'
        b += f'<rect x="{tx}" y="80" width="{tw:.1f}" height="2" rx="1" fill="{TEAL}" style="animation:bar{i} {C}s linear infinite"/>'
        tx += tw + 30
    b += d.text(MONO, "illustrative traces · auto-cycling", W - 28, 72, 11, fill=MUTED, anchor="end")
    b += f'<path d="M1 92H{W-1}" stroke="{DIMLINE}"/>'

    def log(lines, x, y0, start):
        s = ""
        for i, parts in enumerate(lines):
            y = y0 + i*26
            xx = x
            row = ""
            for txt, col in parts:
                row += d.text(MONO, txt, xx, y, 12.5, fill=col)
                xx += MONO.width(txt, 12.5)
            s += f'<g class="rv" style="animation-delay:{start + 0.5 + i*0.55:.2f}s">{row}</g>'
        return s

    # ── pane 1: RiderShield ───────────────────────────────────────────────
    vx, vy, vw, vh = 28, 108, 400, 248
    p = f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="10" fill="{BG}" stroke="{LINE}"/>'
    hz = vy + 70
    cxr = vx + vw/2
    p += (f'<path d="M{cxr-10} {hz}L{vx+20} {vy+vh}M{cxr+10} {hz}L{vx+vw-20} {vy+vh}" stroke="{MUTED}" stroke-width="1.5"/>'
          f'<path d="M{cxr} {hz}V{vy+vh}" stroke="{SOFT}" stroke-width="2.5" stroke-dasharray="8 8" class="lane"/>'
          f'<path d="M{vx} {hz}H{vx+vw}" stroke="{LINE}"/>')
    car = (f'<rect x="{cxr-34}" y="{vy+122}" width="68" height="34" rx="6" fill="#16222c" stroke="{SOFT}"/>'
           f'<rect x="{cxr-28}" y="{vy+142}" width="12" height="5" rx="2" fill="{BAD}"/><rect x="{cxr+16}" y="{vy+142}" width="12" height="5" rx="2" fill="{BAD}"/>'
           f'<path d="M{cxr-46} {vy+124}V{vy+110}H{cxr-32}M{cxr+32} {vy+110}H{cxr+46}V{vy+124}M{cxr+46} {vy+156}V{vy+170}H{cxr+32}M{cxr-32} {vy+170}H{cxr-46}V{vy+156}" stroke="{TEAL}" stroke-width="2"/>'
           + d.text(MONOB, "car 0.94", cxr-46, vy+102, 11, fill=TEAL))
    p += f'<g class="jit">{car}</g>'
    p += d.text(MONOB, "15 FPS", vx+16, vy+24, 12, fill=TEXT) + d.text(MONO, "mobilenetv2 · int8", vx+vw-16, vy+24, 11, fill=MUTED, anchor="end")
    p += d.text(MONO, "TTC", vx+16, vy+vh-18, 11, fill=MUTED) + d.text(MONOB, "2.4 s", vx+46, vy+vh-18, 12, fill=WARN)
    p += f'<circle cx="{vx+vw-22}" cy="{vy+vh-22}" r="5" fill="{BAD}" class="blink"/>'
    lx = 460
    p += log([
        [("[pi]    ", MUTED), ("frame 1042 → tflite int8 · 61 ms", SOFT)],
        [("[pi]    ", MUTED), ("collision_risk=", SOFT), ("0.87", WARN), ("  ttc=2.4s", SOFT)],
        [("[esp32] ", MUTED), ("publish ", SOFT), ("ridershield/hazard", CYAN), (" qos=1", SOFT)],
        [("[api]   ", MUTED), ("ws broadcast → 3 riders nearby", SOFT)],
        [("[app]   ", MUTED), ("BRAKE ALERT", BAD), (" shown · haptic + voice", SOFT)],
    ], lx, 134, 0)
    p += d.text(MONO, "latency budget", lx, 292, 11, fill=MUTED) + d.text(MONOB, "61 / 100 ms", W-28, 292, 11, fill=TEAL, anchor="end")
    p += f'<rect x="{lx}" y="302" width="{W-28-lx}" height="8" rx="4" fill="{DIMLINE}"/><rect x="{lx}" y="302" width="{(W-28-lx)*.61:.0f}" height="8" rx="4" fill="{TEAL}"/>'
    p += d.text(MONO, "RiderShield AI · on-device collision detection", lx, 340, 11, fill=MUTED)
    b += f'<g class="pane" style="animation-delay:0s">{p}</g>'

    # ── pane 2: RoboGuard ─────────────────────────────────────────────────
    rnd = random.Random(5)
    p = f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="10" fill="{BG}" stroke="{LINE}"/>'
    mid = vy + 120
    fx = vx + vw - 60
    wx = fx - 110
    pts = []
    for i in range(0, vw - 20, 3):
        x = vx + 10 + i
        g = max(0, (x - wx + 60) / (fx - wx + 60))
        a = 7 + 46*g**2
        pts.append(f"{x} {mid + a*math.sin(i*.33) + rnd.uniform(-2.5, 2.5):.1f}")
    p += (f'<rect x="{wx}" y="{vy+40}" width="{fx-wx}" height="{vh-70}" fill="{WARN}" opacity=".08"/>'
          f'<path d="M{fx} {vy+40}V{vy+vh-30}" stroke="{BAD}" stroke-width="1.5" stroke-dasharray="4 4"/>'
          f'<path d="M{vx+10} {mid-58}H{vx+vw-10}" stroke="{WARN}" stroke-opacity=".5" stroke-dasharray="3 5"/>'
          f'<path d="M{"L".join(pts)}" stroke="{CYAN}" stroke-width="1.6"/>')
    p += (f'<g class="cur"><path d="M{vx+10} {vy+40}V{vy+vh-30}" stroke="{TEAL}" stroke-width="1.5"/>'
          f'<circle cx="{vx+10}" cy="{vy+40}" r="4" fill="{TEAL}"/></g>')
    p += d.text(MONOB, "motor_2 · current", vx+16, vy+24, 12, fill=TEXT) + d.text(MONO, "lstm window=64", vx+vw-16, vy+24, 11, fill=MUTED, anchor="end")
    p += d.text(MONOB, "warn", wx+6, vy+vh-14, 11, fill=WARN) + d.text(MONOB, "fault", fx+6, vy+vh-14, 11, fill=BAD)
    p += log([
        [("[tele]  ", MUTED), ("10 Hz · motor_2 current, temp, rpm", SOFT)],
        [("[lstm]  ", MUTED), ("anomaly score ", SOFT), ("0.31 → 0.72", WARN)],
        [("[lstm]  ", MUTED), ("FAULT PREDICTED", BAD), (" in ~18 steps", SOFT)],
        [("[yolo]  ", MUTED), ("person in zone B · ", SOFT), ("slow to 40%", WARN)],
        [("[ws]    ", MUTED), ("alert → mission control dashboard", SOFT)],
    ], lx, 134, seg)
    p += d.text(MONO, "early warning", lx, 292, 11, fill=MUTED) + d.text(MONOB, "10–30 steps ahead", W-28, 292, 11, fill=TEAL, anchor="end")
    for i in range(30):
        c = TEAL if i < 12 else (WARN if i < 24 else BAD)
        p += f'<rect x="{lx + i*((W-28-lx)/30):.1f}" y="302" width="{(W-28-lx)/30 - 3:.1f}" height="8" rx="2" fill="{c}" opacity="{.9 if 10 <= i <= 28 else .3}"/>'
    p += d.text(MONO, "RoboGuard · predictive fault detection", lx, 340, 11, fill=MUTED)
    b += f'<g class="pane" style="animation-delay:{seg:.1f}s">{p}</g>'

    # ── pane 3: Kaaval ────────────────────────────────────────────────────
    p = f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="10" fill="{BG}" stroke="{LINE}"/>'
    p += d.text(MONOB, "gateway · 7 checks / request", vx+16, vy+24, 12, fill=TEXT)
    checks = ["session active", "signature (P-256)", "method · origin · path", "body hash",
              "single-use nonce", "strictly increasing seq", "freshness window"]
    for i, c in enumerate(checks):
        y = vy + 50 + i*27
        g = check(vx+18, y-9, 9) + d.text(MONO, c, vx+38, y, 12.5, fill=SOFT)
        p += f'<g class="rv" style="animation-delay:{2*seg + 0.3 + i*0.35:.2f}s">{g}</g>'
    p += log([
        [("GET  /account   ", SOFT), ("signed  seq 41", MUTED), ("  → 200", TEAL)],
        [("POST /transfer  ", SOFT), ("signed  seq 42", MUTED), ("  → 200", TEAL)],
        [("GET  /account   ", SOFT), ("cookie only   ", WARN), ("→ 401 proof_absent", BAD)],
        [("GET  /account   ", SOFT), ("nonce reused  ", WARN), ("→ 401 replay", BAD)],
        [("[chronicle]     ", MUTED), ("incident #7 narrated", SOFT)],
    ], lx, 134, 2*seg)
    p += d.text(MONO, "stolen cookies accepted", lx, 292, 11, fill=MUTED) + d.text(MONOB, "0", W-28, 292, 11, fill=TEAL, anchor="end")
    p += f'<rect x="{lx}" y="302" width="{W-28-lx}" height="8" rx="4" fill="{DIMLINE}"/>'
    p += d.text(MONO, "Kaaval · per-request signed sessions", lx, 340, 11, fill=MUTED)
    b += f'<g class="pane" style="animation-delay:{2*seg:.1f}s">{p}</g>'
    save("console.svg", d.render(W, H, b, css, "console"))


if __name__ == "__main__":
    banner()
    divider()
    terminal()
    console()
