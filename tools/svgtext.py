"""Outline text engine: turns strings into <use> references to glyph paths,
so the SVGs render identically on GitHub without web fonts."""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from pathlib import Path

FONT_DIR = Path(__file__).parent / "fonts"


class Face:
    def __init__(self, key, file, **axes):
        self.key = key
        font = TTFont(FONT_DIR / file)
        self.font = instantiateVariableFont(font, axes) if axes else font
        self.upm = self.font["head"].unitsPerEm
        self.cmap = self.font.getBestCmap()
        self.gs = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]
        self._paths = {}

    def glyph(self, ch):
        name = self.cmap.get(ord(ch))
        if name is None:
            raise KeyError(f"{self.key}: no glyph for {ch!r}")
        if name not in self._paths:
            pen = SVGPathPen(self.gs, ntos=lambda v: str(round(v)))
            self.gs[name].draw(pen)
            self._paths[name] = pen.getCommands()
        return name, self.hmtx[name][0], self._paths[name]

    def width(self, text, size, ls=0.0):
        """ls = letter spacing in em."""
        adv = sum(self.glyph(c)[1] for c in text) / self.upm
        return (adv + ls * max(len(text) - 1, 0)) * size

    def wrap(self, text, size, max_w, ls=0.0):
        lines, cur = [], ""
        for word in text.split(" "):
            trial = (cur + " " + word).strip()
            if cur and self.width(trial, size, ls) > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines


class Doc:
    """Collects glyph defs used across one SVG document."""

    def __init__(self):
        self.defs = {}

    def text(self, face, s, x, y, size, fill="currentColor", anchor="start",
             ls=0.0, cls=None, char_attrs=None, extra=""):
        w = face.width(s, size, ls)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        k = size / face.upm
        parts = []
        cx = 0.0
        for i, ch in enumerate(s):
            name, adv, d = face.glyph(ch)
            if d:
                gid = f"{face.key}-{name}".replace(".", "_")
                self.defs[gid] = d
                attrs = char_attrs(i, ch) if char_attrs else ""
                parts.append(
                    f'<use href="#{gid}" xlink:href="#{gid}" '
                    f'transform="translate({cx:.2f} 0) scale({k:.5f} {-k:.5f})"{attrs}/>'
                )
            cx += adv * k + ls * size
        c = f' class="{cls}"' if cls else ""
        return (f'<g transform="translate({x:.2f} {y:.2f})" fill="{fill}"{c}{extra}>'
                + "".join(parts) + "</g>")

    def lines(self, face, lines, x, y, size, lh, **kw):
        return "".join(self.text(face, ln, x, y + i * lh, size, **kw)
                       for i, ln in enumerate(lines))

    def render(self, w, h, body, style="", title=""):
        defs = "".join(f'<path id="{k}" d="{v}"/>' for k, v in self.defs.items())
        t = f"<title>{title.replace('&', '&amp;').replace('<', '&lt;')}</title>" if title else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
                f'viewBox="0 0 {w} {h}" fill="none">{t}'
                f"<style>{style}</style><defs>{defs}</defs>{body}</svg>")
