"""Generates the SVG artwork for the adithyan-css profile README.
Theme: projects in orbit — deep space navy, amber + coral.
Run:  python make.py   (writes ../assets/*.svg)"""
import math
import random
from pathlib import Path
from svgtext import Face, Doc

OUT = Path(__file__).parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# ── tokens ────────────────────────────────────────────────────────────────
SPACE, SPACE2 = "#0a0c1b", "#11142b"
LINE = "#252a4a"
TEXT, SOFT, MUTED = "#f4f1ea", "#c3c0d6", "#7c7a9a"
AMBER, CORAL = "#ffb547", "#ff7a59"

DISPLAY = Face("dp", "SpaceGrotesk.ttf", wght=700)
BODY = Face("bd", "SpaceGrotesk.ttf", wght=400)
MONO = Face("mo", "SpaceMono.ttf")
MONOB = Face("mb", "SpaceMono-Bold.ttf")

GH = "https://github.com/adithyan-css/"
PROJECTS = [
    dict(key="rs", name="RiderShield AI", short="RiderShield", cat="EDGE AI", color="#ffb547",
         line="Sees the crash before the rider does: vision on a Raspberry Pi.",
         stats=[("Inference", "15 FPS"), ("Latency budget", "<100 ms"), ("Model", "INT8")],
         tags=["TFLite", "ESP32", "MQTT", "Flutter"], url=GH + "RIDERSHIELD_AI"),
    dict(key="ag", name="AgriPrice AI", short="AgriPrice", cat="FORECAST", color="#b5e853",
         line="Tells farmers when to sell, and how sure it is about it.",
         stats=[("Ensemble", "3 models"), ("Horizon", "7 days"), ("Markets", "92")],
         tags=["Chronos", "Prophet", "NestJS", "Flutter"], url=GH + "Agri_app"),
    dict(key="rg", name="RoboGuard", short="RoboGuard", cat="ROBOTICS", color="#ff7a59",
         line="Hears a motor failing before it fails, and watches the zone around it.",
         stats=[("Early warning", "10–30 steps"), ("Telemetry", "10 Hz"), ("Vision", "YOLOv8")],
         tags=["LSTM", "YOLOv8", "FastAPI", "React"], url=GH + "RoboGuard"),
    dict(key="hx", name="Helix", short="Helix", cat="AUTONOMY", color="#6ec6ff",
         line="Software that attacks itself, heals, and remembers the fix.",
         stats=[("Immune memory", "1536-d"), ("Cognition", "27B LLM"), ("Heal loop", "4 stages")],
         tags=["TypeScript", "MongoDB", "Groq", "n8n"], url=GH + "Helix"),
    dict(key="kv", name="Kaaval", short="Kaaval", cat="SECURITY", color="#ff6f9c",
         line="Every request signed by a key that never leaves the browser.",
         stats=[("Checks / request", "7"), ("Key", "P-256"), ("Tests passing", "162")],
         tags=["Web Crypto", "WebAuthn", "FastAPI", "Next.js"], url=GH + "Kaaval"),
    dict(key="sr", name="Smart Rover", short="Smart Rover", cat="IOT", color="#f4d58d",
         line="A control station the rover serves from its own access point.",
         stats=[("Frameworks", "0"), ("Link", "WebSocket"), ("App size", "3 files")],
         tags=["JavaScript", "WebSocket", "ESP32"], url="https://smart-rover-opal.vercel.app"),
]


def save(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")
    print(f"{name:20s} {len(svg)/1024:6.1f} KB")


def stars(rnd, W, H, n=150, twinkle=24):
    s = ""
    for i in range(n):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.choice([.6, .7, .9, 1.1, 1.4])
        cls = f' class="tw" style="animation-delay:{rnd.uniform(0, 4):.1f}s"' if i < twinkle else ""
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"{cls}/>'
    return s


TW_CSS = ".tw{animation:tw 3.2s ease-in-out infinite}@keyframes tw{50%{opacity:.05}}"


# ══════════════════════════════════════════════════════════════════════════
# ORBIT HERO
# ══════════════════════════════════════════════════════════════════════════
def orbit():
    W, H = 1000, 520
    d = Doc()
    rnd = random.Random(9)
    cx, cy = W/2, 262
    css = TW_CSS + """
.sun{animation:sun 5s ease-in-out infinite}@keyframes sun{50%{opacity:.7}}
.in{animation:in 1.1s cubic-bezier(.2,.7,.2,1) both}@keyframes in{from{opacity:0;transform:translateY(10px)}}
"""
    b = ('<defs>'
         f'<radialGradient id="bg" cx=".5" cy=".5" r=".75"><stop offset="0" stop-color="#1a1840"/><stop offset=".6" stop-color="{SPACE}"/></radialGradient>'
         f'<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{AMBER}" stop-opacity=".5"/>'
         f'<stop offset=".45" stop-color="{CORAL}" stop-opacity=".16"/><stop offset="1" stop-color="{CORAL}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="nm" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#ffe6bf"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>'
         '<radialGradient id="shade" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".5"/>'
         '<stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient>'
         f'<clipPath id="cl"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
         '</defs>')
    b += f'<g clip-path="url(#cl)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{stars(rnd, W, H)}'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="300" ry="190" fill="url(#sun)" class="sun"/>'

    orbits = [(300, 120), (342, 148), (382, 174), (420, 198), (455, 220), (488, 240)]
    for i, ((rx, ry), p) in enumerate(zip(orbits, PROJECTS)):
        ring = f"M{cx-rx} {cy}A{rx} {ry} 0 1 0 {cx+rx} {cy}A{rx} {ry} 0 1 0 {cx-rx} {cy}"
        b += f'<path d="{ring}" stroke="{p["color"]}" stroke-opacity=".22" stroke-dasharray="{"3 7" if i % 2 else "none"}"/>'
        dur = 40 + i*8
        lbl = d.text(MONOB, p["short"].upper(), 17, 4, 11, fill=p["color"], ls=.08)
        r = 7 + (i % 3)
        b += (f'<g><circle r="17" fill="{p["color"]}" opacity=".14"/><circle r="{r}" fill="{p["color"]}"/>'
              f'<circle r="{r}" fill="url(#shade)"/>{lbl}'
              f'<animateMotion dur="{dur}s" begin="-{dur*i/6 + 4:.1f}s" repeatCount="indefinite" path="{ring}"/></g>')

    size = 72
    while DISPLAY.width("ADITHYAN C S S", size, -.01) > 600:
        size -= 1
    b += (f'<g class="in">{d.text(MONO, "SIX PROJECTS IN ORBIT", cx, cy - 60, 12, fill=AMBER, anchor="middle", ls=.3)}</g>'
          f'<g class="in" style="animation-delay:.15s">{d.text(DISPLAY, "ADITHYAN C S S", cx, cy + 22, size, fill="url(#nm)", anchor="middle", ls=-.01)}</g>'
          f'<g class="in" style="animation-delay:.3s">{d.text(BODY, "edge AI · forecasting · robotics · security · self-healing software", cx, cy + 58, 16, fill=SOFT, anchor="middle")}</g>')
    b += "</g>"
    b += f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" stroke="{LINE}"/>'
    save("orbit.svg", d.render(W, H, b, css, "Adithyan C S S: six projects in orbit"))


# ══════════════════════════════════════════════════════════════════════════
# PROJECT CARDS — one illustration each
# ══════════════════════════════════════════════════════════════════════════
def art_rs(c, x, y):
    s = (f'<path d="M{x} {y-56}L{x+48} {y-38}V{y+2}Q{x+48} {y+42} {x} {y+62}Q{x-48} {y+42} {x-48} {y+2}V{y-38}Z" '
         f'fill="{c}" fill-opacity=".1" stroke="{c}" stroke-width="2"/>')
    s += f'<path d="M{x} {y-24}V{y+44}" stroke="{c}" stroke-width="2" stroke-dasharray="6 6" class="lane"/>'
    s += f'<path d="M{x-6} {y-24}L{x-30} {y+40}M{x+6} {y-24}L{x+30} {y+40}" stroke="{c}" stroke-opacity=".5" stroke-width="1.5"/>'
    s += (f'<g class="bob"><rect x="{x-13}" y="{y-4}" width="26" height="15" rx="3" fill="{SPACE}" stroke="{TEXT}" stroke-width="1.5"/>'
          f'<path d="M{x-20} {y-4}V{y-11}H{x-13}M{x+13} {y-11}H{x+20}V{y-4}M{x+20} {y+11}V{y+18}H{x+13}M{x-13} {y+18}H{x-20}V{y+11}" stroke="{c}" stroke-width="2"/></g>')
    return s, (".lane{animation:lane .7s linear infinite}@keyframes lane{to{stroke-dashoffset:-12}}"
               ".bob{animation:bob 2.4s ease-in-out infinite}@keyframes bob{50%{transform:translate(2px,3px)}}")


def art_ag(c, x, y):
    pts = [(x-62, y+30), (x-44, y+18), (x-30, y+24), (x-14, y+6), (x, y+10)]
    hist = "M" + "L".join(f"{a} {b}" for a, b in pts)
    s = (f'<path d="M{x-66} {y+46}H{x+66}" stroke="{LINE}" stroke-width="1.5"/>'
         f'<path d="M{x} {y+10}L{x+62} {y-46}L{x+62} {y+14}Z" fill="{c}" fill-opacity=".18" class="fan"/>'
         f'<path d="{hist}" stroke="{SOFT}" stroke-width="2" stroke-linejoin="round"/>'
         f'<path d="M{x} {y+10}L{x+62} {y-16}" stroke="{c}" stroke-width="2.5" stroke-dasharray="70" class="draw"/>'
         f'<path d="M{x} {y-50}V{y+46}" stroke="{MUTED}" stroke-dasharray="2 4"/>')
    leaf = (f'<g class="sway"><path d="M{x-40} {y-22}Q{x-40} {y-52} {x-12} {y-56}Q{x-10} {y-28} {x-40} {y-22}Z" fill="{c}" fill-opacity=".85"/>'
            f'<path d="M{x-40} {y-22}Q{x-30} {y-40} {x-14} {y-52}" stroke="{SPACE}" stroke-width="1.5"/></g>')
    css = (".draw{animation:draw 3s ease-out infinite}@keyframes draw{0%{stroke-dashoffset:70}50%,100%{stroke-dashoffset:0}}"
           ".fan{transform-box:fill-box;transform-origin:left center;animation:fan 3s ease-out infinite}@keyframes fan{0%{transform:scaleY(.1)}50%,100%{transform:scaleY(1)}}"
           ".sway{transform-box:fill-box;transform-origin:left bottom;animation:sway 3s ease-in-out infinite}@keyframes sway{50%{transform:rotate(-6deg)}}")
    return s + leaf, css


def art_rg(c, x, y):
    bx, by = x - 30, y + 44
    s = f'<rect x="{bx-26}" y="{by}" width="52" height="12" rx="3" fill="{c}" fill-opacity=".25" stroke="{c}" stroke-width="1.5"/>'
    s += (f'<path d="M{bx} {by}L{bx} {by-46}" stroke="{TEXT}" stroke-width="7" stroke-linecap="round"/>'
          f'<g><path d="M{bx} {by-46}L{bx+52} {by-70}" stroke="{TEXT}" stroke-width="6" stroke-linecap="round"/>'
          f'<path d="M{bx+52} {by-70}l10 -6M{bx+52} {by-70}l10 6" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'
          f'<animateTransform attributeName="transform" type="rotate" values="0 {bx} {by-46};-14 {bx} {by-46};0 {bx} {by-46}" dur="3s" repeatCount="indefinite"/></g>'
          f'<circle cx="{bx}" cy="{by-46}" r="6" fill="{c}"/><circle cx="{bx}" cy="{by}" r="6" fill="{c}"/>')
    s += (f'<g class="warn"><path d="M{x+46} {y+8}L{x+64} {y+40}H{x+28}Z" fill="{c}"/>'
          f'<path d="M{x+46} {y+18}V{y+29}" stroke="{SPACE}" stroke-width="3" stroke-linecap="round"/><circle cx="{x+46}" cy="{y+35}" r="1.8" fill="{SPACE}"/></g>')
    return s, ".warn{animation:warn 1.2s steps(1) infinite}@keyframes warn{50%{opacity:.25}}"


def art_hx(c, x, y):
    A, P = 30, 64

    def strand(ph):
        return "M" + "L".join(f"{x + A*math.sin(2*math.pi*t/P + ph):.1f} {y - 96 + t}" for t in range(0, 2*P + 66, 2))
    rungs = ""
    for k, t in enumerate(range(0, 2*P + 64, 10)):
        x1 = x + A*math.sin(2*math.pi*t/P)
        x2 = x + A*math.sin(2*math.pi*t/P + math.pi)
        col = CORAL if k % 6 == 2 else c
        rungs += f'<path d="M{x1:.1f} {y-96+t}H{x2:.1f}" stroke="{col}" stroke-opacity=".7" stroke-width="2"/>'
    s = (f'<g class="hx">{rungs}<path d="{strand(0)}" stroke="{c}" stroke-width="2.5"/>'
         f'<path d="{strand(math.pi)}" stroke="{TEXT}" stroke-width="2" stroke-opacity=".7"/></g>')
    return s, f".hx{{animation:hx 4s linear infinite}}@keyframes hx{{to{{transform:translateY({P}px)}}}}"


def art_kv(c, x, y):
    s = (f'<path d="M{x-24} {y-8}V{y-26}A24 24 0 0 1 {x+24} {y-26}V{y-8}" stroke="{TEXT}" stroke-width="6" stroke-linecap="round"/>'
         f'<rect x="{x-38}" y="{y-10}" width="76" height="60" rx="10" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-width="2"/>'
         f'<circle cx="{x}" cy="{y+14}" r="7" fill="{c}"/><path d="M{x} {y+18}V{y+32}" stroke="{c}" stroke-width="5" stroke-linecap="round"/>')
    wave = "M" + "L".join(f"{x-64 + i*3} {y+66 + 5*math.sin(i*.7)*math.sin(i*.15):.1f}" for i in range(44))
    s += f'<path d="{wave}" stroke="{c}" stroke-width="1.8" stroke-dasharray="160" class="sig"/>'
    s += f'<g class="ring"><circle cx="{x}" cy="{y+14}" r="7" stroke="{c}" stroke-width="2"/></g>'
    css = (".sig{animation:sig 2.6s ease-in-out infinite}@keyframes sig{0%{stroke-dashoffset:160}60%,100%{stroke-dashoffset:0}}"
           ".ring{transform-box:fill-box;transform-origin:center;animation:ring 2s ease-out infinite}@keyframes ring{from{transform:scale(1);opacity:1}to{transform:scale(3.5);opacity:0}}")
    return s, css


def art_sr(c, x, y):
    s = "".join(f'<path d="M{x+18-r} {y-14}A{r} {r} 0 0 1 {x+18+r} {y-14}" stroke="{c}" stroke-opacity="{.75 - r/100:.2f}" '
                f'stroke-width="1.5" class="ping" style="animation-delay:{r/60:.2f}s"/>' for r in (16, 30, 44))
    s += f'<path d="M{x+18} {y-14}V{y+4}" stroke="{TEXT}" stroke-width="2"/><circle cx="{x+18}" cy="{y-14}" r="3" fill="{c}"/>'
    s += f'<rect x="{x-46}" y="{y+4}" width="92" height="28" rx="7" fill="{c}" fill-opacity=".22" stroke="{c}" stroke-width="2"/>'
    for wx in (x-28, x+28):
        s += (f'<g><circle cx="{wx}" cy="{y+40}" r="13" fill="{SPACE}" stroke="{TEXT}" stroke-width="2.5"/>'
              f'<path d="M{wx-13} {y+40}H{wx+13}M{wx} {y+27}V{y+53}" stroke="{TEXT}" stroke-width="1.5"/>'
              f'<animateTransform attributeName="transform" type="rotate" from="0 {wx} {y+40}" to="360 {wx} {y+40}" dur="2s" repeatCount="indefinite"/></g>')
    s += f'<path d="M{x-80} {y+54}H{x+80}" stroke="{LINE}" stroke-width="2" stroke-dasharray="10 8" class="ground"/>'
    css = (".ping{animation:ping 1.8s ease-in-out infinite}@keyframes ping{50%{opacity:.1}}"
           ".ground{animation:ground .8s linear infinite}@keyframes ground{to{stroke-dashoffset:18}}")
    return s, css


ARTS = dict(rs=art_rs, ag=art_ag, rg=art_rg, hx=art_hx, kv=art_kv, sr=art_sr)


def card(i, p):
    W, H = 320, 452
    d = Doc()
    c = p["color"]
    art, acss = ARTS[p["key"]](c, W/2, 138)
    css = acss + f""".sheen{{animation:sheen 6s ease-in-out {i*0.7:.1f}s infinite}}
@keyframes sheen{{0%,70%{{transform:translateX(-360px)}}100%{{transform:translateX(420px)}}}}"""
    b = ('<defs>'
         f'<linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SPACE2}"/><stop offset="1" stop-color="{SPACE}"/></linearGradient>'
         f'<radialGradient id="ag" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="{c}" stop-opacity=".22"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
         '<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
         '<stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="cc"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
         f'<clipPath id="aw"><rect x="22" y="56" width="{W-44}" height="166" rx="12"/></clipPath>'
         '</defs>')
    b += f'<g clip-path="url(#cc)"><rect width="{W}" height="{H}" fill="url(#cg)"/>'
    b += f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="13" stroke="{c}" stroke-opacity=".28"/>'
    b += d.text(MONOB, f"No.{i:02d}", 26, 38, 12, fill=c, ls=.06)
    cw = MONOB.width(p["cat"], 10, .1) + 18
    b += f'<rect x="{W-26-cw:.1f}" y="24" width="{cw:.1f}" height="20" rx="10" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-opacity=".5"/>'
    b += d.text(MONOB, p["cat"], W-26-cw/2, 38, 10, fill=c, anchor="middle", ls=.1)
    b += f'<rect x="22" y="56" width="{W-44}" height="166" rx="12" fill="{SPACE}" stroke="{LINE}"/>'
    b += f'<rect x="22" y="56" width="{W-44}" height="166" rx="12" fill="url(#ag)"/>'
    b += f'<g clip-path="url(#aw)">{art}</g>'
    size = 28
    while DISPLAY.width(p["name"], size) > W - 52:
        size -= 1
    b += d.text(DISPLAY, p["name"], 26, 262, size, fill=TEXT)
    b += d.lines(BODY, BODY.wrap(p["line"], 14, W - 52)[:2], 26, 288, 14, 19, fill=SOFT)
    for j, (k, v) in enumerate(p["stats"]):
        y = 338 + j*24
        kw = MONO.width(k, 11)
        vw = DISPLAY.width(v, 16)
        b += d.text(MONO, k, 26, y, 11, fill=MUTED)
        b += f'<path d="M{26 + kw + 8:.1f} {y-4}H{W - 26 - vw - 8:.1f}" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="1 4" stroke-linecap="round"/>'
        b += d.text(DISPLAY, v, W - 26, y + 1, 16, fill=c if j == 0 else TEXT, anchor="end")
    x = 26
    for t in p["tags"]:
        tw = MONO.width(t, 10) + 16
        if x + tw > W - 24:
            break
        b += f'<rect x="{x:.1f}" y="{H-50}" width="{tw:.1f}" height="22" rx="11" stroke="{LINE}" stroke-width="1.2"/>'
        b += d.text(MONO, t, x + 8, H - 35, 10, fill=SOFT)
        x += tw + 6
    b += f'<g class="sheen"><rect x="-40" y="0" width="140" height="{H}" fill="url(#sh)" transform="skewX(-18)"/></g>'
    b += "</g>"
    b += f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="20" stroke="{c}" stroke-opacity=".55" stroke-width="1.5"/>'
    save(f"card-{i:02d}.svg", d.render(W, H, b, css, p["name"]))


# ══════════════════════════════════════════════════════════════════════════
# TECH CONSTELLATION — which tools power which project
# ══════════════════════════════════════════════════════════════════════════
LEFT = [
    ("Python", "rs ag rg kv"), ("PyTorch · LSTM", "rg"), ("TensorFlow Lite", "rs"), ("YOLOv8 · OpenCV", "rg"),
    ("Chronos · Prophet", "ag"), ("Groq LLMs", "hx kv"), ("Raspberry Pi", "rs"), ("ESP32", "rs sr"),
    ("MQTT", "rs"), ("JavaScript", "sr"),
]
RIGHT = [
    ("FastAPI", "rs rg kv"), ("WebSockets", "rs rg sr"), ("NestJS", "ag"), ("MongoDB", "rs hx"),
    ("PostgreSQL", "ag"), ("Flutter", "rs ag"), ("React", "rs rg"), ("Next.js", "hx kv"),
    ("Web Crypto · WebAuthn", "kv"), ("n8n", "hx"),
]


def constellation():
    W, H = 1000, 470
    d = Doc()
    rnd = random.Random(4)
    css = TW_CSS + """
.flow{animation:flow 2.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}
.pulse{animation:pulse 2.6s ease-in-out infinite}@keyframes pulse{50%{opacity:.35}}
"""
    b = (f'<defs><clipPath id="cl"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
         f'<radialGradient id="bg" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="#15173a"/><stop offset="1" stop-color="{SPACE}"/></radialGradient></defs>'
         f'<g clip-path="url(#cl)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{stars(rnd, W, H, 90, 14)}')
    b += d.text(MONOB, "TECH CONSTELLATION", 28, 36, 12, fill=AMBER, ls=.2)
    b += d.text(MONO, "each line = a tool shipped in that project", W - 28, 36, 11, fill=MUTED, anchor="end")
    cx = W/2
    py0, pstep = 98, 62
    ppos = {p["key"]: (cx, py0 + i*pstep) for i, p in enumerate(PROJECTS)}
    pcol = {p["key"]: p["color"] for p in PROJECTS}
    ty0 = 76
    tstep = (H - 42 - ty0) / (len(LEFT) - 1)

    def side(items, x, anchor, sign):
        s, links = "", ""
        for j, (name, keys) in enumerate(items):
            y = ty0 + j*tstep
            ks = keys.split()
            r = 2.6 + len(ks)*1.2
            for k in ks:
                px, pyy = ppos[k]
                ex = px + sign*78
                links += (f'<path d="M{x} {y:.1f}C{x - sign*120:.1f} {y:.1f} {ex + sign*120:.1f} {pyy} {ex:.1f} {pyy}" '
                          f'stroke="{pcol[k]}" stroke-opacity=".42" stroke-width="1.3" stroke-dasharray="4 8" class="flow"/>')
            s += f'<circle cx="{x}" cy="{y:.1f}" r="{r:.1f}" fill="{TEXT}"/><circle cx="{x}" cy="{y:.1f}" r="{r+5:.1f}" stroke="{TEXT}" stroke-opacity=".2"/>'
            s += d.text(MONO, name, x + sign*16, y + 4, 12.5, fill=SOFT, anchor=anchor)
        return links, s

    l1, s1 = side(LEFT, 250, "end", -1)
    l2, s2 = side(RIGHT, W - 250, "start", 1)
    b += l1 + l2 + s1 + s2
    for i, p in enumerate(PROJECTS):
        px, pyy = ppos[p["key"]]
        w = DISPLAY.width(p["short"], 15) + 40
        b += f'<path d="M{px - 78} {pyy}H{px + 78}" stroke="{p["color"]}" stroke-opacity=".5" stroke-width="1.3"/>'
        b += (f'<rect x="{px - w/2:.1f}" y="{pyy - 17}" width="{w:.1f}" height="34" rx="17" fill="{SPACE}" stroke="{p["color"]}" stroke-width="1.5"/>'
              f'<circle cx="{px - w/2 + 16:.1f}" cy="{pyy}" r="4" fill="{p["color"]}" class="pulse" style="animation-delay:{i*.4:.1f}s"/>')
        b += d.text(DISPLAY, p["short"], px + 8, pyy + 5.5, 15, fill=TEXT, anchor="middle")
    b += "</g>"
    b += f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" stroke="{LINE}"/>'
    save("constellation.svg", d.render(W, H, b, css, "Tech constellation"))


# ══════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════
def footer():
    W, H = 1000, 90
    d = Doc()
    rnd = random.Random(2)
    path = f"M60 45H{W - 60}"
    b = (f'<defs><clipPath id="cl"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>'
         f'<g clip-path="url(#cl)"><rect width="{W}" height="{H}" fill="{SPACE}"/>{stars(rnd, W, H, 70, 20)}')
    b += f'<path d="M60 45H{W/2 - 190}M{W/2 + 190} 45H{W-60}" stroke="{LINE}" stroke-dasharray="2 6"/>'
    b += d.text(MONO, "END OF TRANSMISSION", W/2, 50, 13, fill=SOFT, anchor="middle", ls=.35)
    b += f'<circle r="4" fill="{AMBER}"><animateMotion dur="9s" repeatCount="indefinite" path="{path}"/></circle>'
    b += "</g>" + f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" stroke="{LINE}"/>'
    save("footer.svg", d.render(W, H, b, TW_CSS, "end of transmission"))


if __name__ == "__main__":
    orbit()
    for i, p in enumerate(PROJECTS, 1):
        card(i, p)
    constellation()
    footer()
