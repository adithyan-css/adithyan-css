"""Generates the SVG panels for the adithyan-css profile README.
Design: an editorial project index — paper, ink, one highlighter.
Run:  python make.py   (writes ../assets/*.svg)"""
from pathlib import Path
from svgtext import Face, Doc

OUT = Path(__file__).parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# ── tokens ────────────────────────────────────────────────────────────────
PAPER, INK, INK2, GREY, MARK = "#f2ede3", "#141414", "#3d3a35", "#7d776c", "#ffe24a"

SERIF = Face("sf", "InstrumentSerif.ttf")
SERIFI = Face("si", "InstrumentSerif-Italic.ttf")
SANS = Face("sr", "InterTight.ttf", wght=400)
SANSB = Face("sb", "InterTight.ttf", wght=800)
MONO = Face("mo", "PlexMono.ttf")
MONOB = Face("mb", "PlexMono-SemiBold.ttf")

CSS = """
.mk{transform-box:fill-box;transform-origin:left center;animation:mk .9s cubic-bezier(.65,0,.2,1) both}
@keyframes mk{from{transform:scaleX(0)}}
.nudge{animation:nudge 1.6s ease-in-out infinite}
@keyframes nudge{50%{transform:translateX(5px)}}
"""


def save(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")
    print(f"{name:24s} {len(svg)/1024:6.1f} KB")


def sheet(W, H):
    return f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>'


def rule(y, W, x0=1.5):
    return f'<path d="M{x0} {y}H{W-x0}" stroke="{INK}" stroke-width="1.2"/>'


def marker(x, base, w, size, delay=0.0):
    return (f'<rect x="{x-4:.1f}" y="{base - size*.42:.1f}" width="{w+8:.1f}" height="{size*.5:.1f}" '
            f'fill="{MARK}" class="mk" style="animation-delay:{delay}s"/>')


def arrow(x, y, color=INK):
    return f'<path d="M{x} {y}H{x+18}M{x+12} {y-6}L{x+18} {y}L{x+12} {y+6}" stroke="{color}" stroke-width="1.6"/>'


def star(cx, cy, r, color=MARK):
    p = (f"M{cx} {cy-r}Q{cx} {cy} {cx+r} {cy}Q{cx} {cy} {cx} {cy+r}"
         f"Q{cx} {cy} {cx-r} {cy}Q{cx} {cy} {cx} {cy-r}Z")
    return f'<path d="{p}" fill="{color}"/>'


# ══════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════
def header(projects):
    W, H = 1000, 372
    d = Doc()
    b = sheet(W, H)
    b += d.text(MONOB, "SELECTED WORK", 26, 25, 11, fill=INK, ls=.08)
    b += d.text(MONO, "— AN INDEX OF THINGS I’VE BUILT", 26 + MONOB.width("SELECTED WORK", 11, .08) + 8, 25, 11, fill=GREY, ls=.04)
    b += d.text(MONO, f"NO. 01 — {len(projects):02d}", W - 26, 25, 11, fill=INK, anchor="end", ls=.08)
    b += rule(38, W)

    b += d.text(SERIF, "Adithyan C S S", 22, 152, 118, fill=INK)
    nx = 22 + SERIF.width("Adithyan C S S", 118) + 18
    b += d.text(SERIFI, "builds systems", nx, 108, 30, fill=INK2)
    b += d.text(SERIFI, "that sense, predict", nx, 138, 30, fill=INK2)
    b += d.text(SERIFI, "& recover.", nx, 168, 30, fill=INK2)

    l1a, l1b = "Six projects, ", "designed and built end to end"
    l1c = " — edge AI on a Raspberry Pi,"
    l2 = "price forecasting, robot safety, session security and software that heals itself."
    s, y1 = 20, 214
    xb = 26 + SANS.width(l1a, s)
    b += marker(xb, y1, SANS.width(l1b, s), s, .3)
    b += d.text(SANS, l1a + l1b + l1c, 26, y1, s, fill=INK)
    b += d.text(SANS, l2, 26, y1 + 28, s, fill=INK)

    # ticker band
    ty, th = 268, 48
    b += f'<rect x="1.5" y="{ty}" width="{W-3}" height="{th}" fill="{INK}"/>'
    items, seq, x = [p["name"].upper() for p in projects], "", 0.0
    for it in items:
        seq += d.text(SANSB, it, x, ty + 31, 19, fill=PAPER, ls=.02)
        x += SANSB.width(it, 19, .02) + 26
        seq += star(x, ty + th/2, 7)
        x += 26
    seqw = x
    reps = int(W // seqw) + 2
    tick = "".join(f'<g transform="translate({i*seqw:.1f} 0)">{seq}</g>' for i in range(reps))
    b += (f'<defs><clipPath id="tk"><rect x="1.5" y="{ty}" width="{W-3}" height="{th}"/></clipPath></defs>'
          f'<g clip-path="url(#tk)"><g class="tick">{tick}</g></g>')
    css = CSS + f".tick{{animation:tick {seqw/38:.1f}s linear infinite}}@keyframes tick{{to{{transform:translateX(-{seqw:.1f}px)}}}}"

    # category legend
    cw = (W - 3) / len(projects)
    for i, p in enumerate(projects):
        x = 1.5 + i*cw
        if i:
            b += f'<path d="M{x:.1f} {ty+th}V{H-1.5}" stroke="{INK}" stroke-width="1.2"/>'
        b += d.text(MONOB, f"{i+1:02d}", x + 16, ty + th + 34, 11, fill=INK)
        b += d.text(MONO, p["cat"], x + 42, ty + th + 34, 10.5, fill=INK2, ls=.04)
    save("header.svg", d.render(W, H, b, css, "Adithyan C S S — selected work"))


# ══════════════════════════════════════════════════════════════════════════
# PROJECT SHEET
# ══════════════════════════════════════════════════════════════════════════
def project(i, n, p):
    W, H = 1000, 352
    d = Doc()
    b = sheet(W, H)
    idx = f"{i:02d}"
    # top strip
    b += d.text(MONOB, f"PROJECT {idx}", 26, 24, 11, fill=INK, ls=.08)
    b += d.text(MONO, f"/ {n:02d}", 26 + MONOB.width(f"PROJECT {idx}", 11, .08) + 8, 24, 11, fill=GREY)
    b += d.text(MONO, p["kind"], W - 26, 24, 11, fill=INK, anchor="end", ls=.08)
    b += rule(37, W)

    # left: outlined numeral + italic one-liner
    ns = 170
    k = ns / SERIF.upm
    b += d.text(SERIF, idx, 22, 196, ns, fill="none",
                extra=f' stroke="{INK}" stroke-width="{1.3/k:.1f}"')
    b += d.lines(SERIFI, SERIFI.wrap(p["line"], 22, 165), 26, 240, 22, 25, fill=INK2)

    # middle
    MX, MW = 224, 386
    size = 42
    while SANSB.width(p["name"], size, -.01) > MW:
        size -= 1
    b += d.text(SANSB, p["name"], MX, 98, size, fill=INK, ls=-.01)
    b += d.lines(SANS, SANS.wrap(p["desc"], 15, MW)[:4], MX, 132, 15, 21.5, fill=INK2)
    cw = MW / 3
    for j, (v, cap) in enumerate(p["metrics"]):
        x = MX + j*cw
        vw = SERIF.width(v, 46)
        if j == 0:
            b += marker(x, 254, vw, 46, .5)
        b += d.text(SERIF, v, x, 254, 46, fill=INK)
        b += d.lines(MONO, MONO.wrap(cap, 9.5, cw - 14)[:2], x, 274, 9.5, 12.5, fill=GREY)

    # right: architecture figure
    RX = 640
    b += f'<path d="M{RX-14} 52V292" stroke="{INK}" stroke-width=".8" stroke-dasharray="2 4"/>'
    b += d.text(MONOB, "ARCHITECTURE", RX, 64, 10, fill=INK, ls=.1)
    b += d.text(MONO, f"FIG. {idx}", W - 28, 64, 10, fill=GREY, anchor="end", ls=.1)
    ny, nh, gap = 78, 28, 9
    lx = RX + 8
    nodes = p["arch"]
    c0, c1 = ny + nh/2, ny + (len(nodes)-1)*(nh+gap) + nh/2
    b += f'<path d="M{lx} {c0}V{c1}" stroke="{INK}" stroke-width="1.2"/>'
    for j, label in enumerate(nodes):
        y = ny + j*(nh+gap)
        core = j == p["core"]
        b += f'<path d="M{lx} {y+nh/2}H{RX+22}" stroke="{INK}" stroke-width="1.2"/>'
        b += f'<circle cx="{lx}" cy="{y+nh/2}" r="3" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>'
        b += (f'<rect x="{RX+22}" y="{y}" width="{W-28-RX-22}" height="{nh}" rx="3" '
              f'fill="{MARK if core else PAPER}" stroke="{INK}" stroke-width="1.2"/>')
        b += d.text(MONOB if core else MONO, label, RX+34, y+18.5, 11, fill=INK)
    b += (f'<circle r="4.5" fill="{INK}"><animateMotion dur="{.7*len(nodes):.1f}s" repeatCount="indefinite" '
          f'path="M{lx} {c0}V{c1}" keyPoints="0;1;1" keyTimes="0;.8;1" calcMode="linear"/></circle>')
    b += d.lines(MONO, MONO.wrap(" / ".join(p["stack"]), 10, W - 28 - RX)[:2], RX, 278, 10, 14, fill=GREY)

    # bottom strip
    b += rule(306, W)
    b += d.text(MONO, p["url"].replace("https://", ""), 26, 334, 11, fill=INK2)
    cta = p.get("cta", "VIEW REPOSITORY")
    b += d.text(MONOB, cta, W - 56, 334, 11, fill=INK, anchor="end", ls=.08)
    b += f'<g class="nudge">{arrow(W - 46, 330)}</g>'
    save(f"project-{idx}.svg", d.render(W, H, b, CSS, p["name"]))


# ══════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════
def footer(n):
    W, H = 1000, 96
    d = Doc()
    b = sheet(W, H)
    b += d.text(SERIFI, "fin.", 24, 64, 50, fill=INK)
    msg = f"{n} SELECTED PROJECTS  ·  EVERYTHING ELSE LIVES IN REPOSITORIES"
    b += d.text(MONO, msg, W/2 + 20, 54, 11, fill=INK2, anchor="middle", ls=.06)
    b += star(W - 80, 48, 9, MARK)
    b += f'<g class="nudge">{arrow(W - 56, 48)}</g>'
    save("footer.svg", d.render(W, H, b, CSS, "fin."))


GH = "https://github.com/adithyan-css/"
PROJECTS = [
    dict(name="RiderShield AI", cat="EDGE AI", kind="REAL-TIME COLLISION DETECTION",
         line="Sees the crash before the rider does.",
         desc="On-device collision detection for riders. A quantized MobileNetV2 runs on a Raspberry Pi inside the latency budget, and an IoT pipeline carries every event from the bike to a phone and an ops dashboard.",
         metrics=[("15", "FPS inference on the edge"), ("<100", "ms end-to-end budget"), ("INT8", "quantized model")],
         arch=["Camera · Raspberry Pi", "MobileNetV2 · TFLite INT8", "ESP32 bike node → MQTT", "FastAPI · MongoDB · Redis", "Flutter app · React ops"],
         core=1, stack=["TensorFlow Lite", "Python", "ESP32", "MQTT", "FastAPI", "Flutter", "React"],
         url=GH + "RIDERSHIELD_AI"),
    dict(name="AgriPrice AI", cat="FORECAST", kind="CROP PRICE INTELLIGENCE",
         line="Tells farmers when to sell, and how sure it is.",
         desc="Live mandi prices, 7-day forecasts and sell-or-wait calls for Indian farmers. An ensemble of models handles non-stationary prices and every prediction ships with a confidence band.",
         metrics=[("3", "model families, one ensemble"), ("7-day", "forecasts with intervals"), ("92", "Tamil Nadu markets")],
         arch=["Mandi price feeds", "Chronos · Prophet · Regression", "Ensemble + confidence bands", "NestJS API · PostgreSQL", "Flutter app"],
         core=2, stack=["Python", "Chronos", "Prophet", "NestJS", "PostgreSQL", "Flutter"],
         url=GH + "Agri_app"),
    dict(name="RoboGuard", cat="ROBOTICS", kind="PREDICTIVE FAULT DETECTION",
         line="Hears a motor failing before it fails.",
         desc="Mission control for robots. An LSTM reads motor time-series and raises a warning before failure, YOLOv8 watches the safety zones around the machine, and everything streams live to the dashboard.",
         metrics=[("10–30", "steps of early warning"), ("10 Hz", "telemetry stream"), ("v8", "YOLO zone monitor")],
         arch=["Motor telemetry · camera", "LSTM fault predictor", "YOLOv8 zone monitor", "FastAPI · WebSockets", "React mission control"],
         core=1, stack=["PyTorch", "YOLOv8", "OpenCV", "FastAPI", "WebSockets", "React"],
         url=GH + "RoboGuard"),
    dict(name="Helix", cat="AUTONOMY", kind="SELF-HEALING SOFTWARE",
         line="Software that heals itself, and remembers.",
         desc="A living layer for AI-built software. It attacks itself on purpose, patches what it finds, and stores each fix as immune memory, so a vulnerability that was fixed can’t quietly come back.",
         metrics=[("1536", "dim immune memory"), ("27B", "model as cognition"), ("4", "stages per heal loop")],
         arch=["Red-team attack runs", "Scan → heal → patch → promote", "Immune memory · vector search", "Qwen3.6-27B via Groq + fallback", "n8n reflex arcs"],
         core=1, stack=["TypeScript", "MongoDB Atlas", "Groq", "n8n", "Next.js"],
         url=GH + "Helix"),
    dict(name="Kaaval", cat="SECURITY", kind="SESSION HIJACK DEFENCE",
         line="A stolen cookie is no longer a key.",
         desc="Stops adversary-in-the-middle session theft. Every request is signed by a non-exportable key that never leaves the browser, and the gateway re-verifies it each time, so a lifted cookie alone gets refused.",
         metrics=[("P-256", "non-exportable keys"), ("7", "checks per request"), ("162", "tests passing")],
         arch=["Browser SDK · Web Crypto key", "Signed request + single-use nonce", "Gateway · 7 ordered checks", "Radar · Guardian policy", "Live dashboard over SSE"],
         core=2, stack=["TypeScript", "WebAuthn", "FastAPI", "SQLite", "Next.js", "Groq"],
         url=GH + "Kaaval"),
    dict(name="Smart Rover", cat="IOT", kind="ROVER CONTROL STATION",
         line="A control room the rover hosts itself.",
         desc="Real-time control, live telemetry, safety monitoring and autonomous-decision views for an ESP32 rover. Zero frameworks and zero CDNs, so the whole station runs from the rover’s own access point.",
         metrics=[("0", "frameworks or CDNs"), ("WS", "live control link"), ("3", "files, whole app")],
         arch=["ESP32 rover · sensors", "WebSocket link", "Telemetry engine", "Safety + decision monitor", "Control station UI"],
         core=2, stack=["JavaScript", "HTML", "CSS", "WebSocket", "ESP32"],
         url="https://smart-rover-opal.vercel.app", cta="OPEN LIVE DEMO"),
]

if __name__ == "__main__":
    header(PROJECTS)
    for i, p in enumerate(PROJECTS, 1):
        project(i, len(PROJECTS), p)
    footer(len(PROJECTS))
