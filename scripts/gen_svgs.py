"""Generate the CV page SVG assets in dark and light variants.

The README picks a variant with <picture> + prefers-color-scheme.
Client work is shown as anonymised structure only: no client names, no data.

Usage: python scripts/gen_svgs.py assets
"""
import sys
from pathlib import Path

FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
W, MARGIN = 1000, 40

THEMES = {
    "dark": dict(BG0="#0d1117", BG1="#161b22", CARD="#0d1117", BORDER="#30363d", TEXT="#e6edf3",
                 MUTED="#8b949e", ACCENT="#3ecf8e", BLUE="#58a6ff", PURPLE="#bc8cff",
                 ORANGE="#f0883e", GOLD="#e3b341", DOT="#ffffff"),
    "light": dict(BG0="#ffffff", BG1="#f6f8fa", CARD="#ffffff", BORDER="#d0d7de", TEXT="#1f2328",
                  MUTED="#59636e", ACCENT="#1a7f37", BLUE="#0969da", PURPLE="#8250df",
                  ORANGE="#bc4c00", GOLD="#9a6700", DOT="#000000"),
}
T: dict = {}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=13, color=None, weight=400, anchor="start", font=FONT, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color or T["TEXT"]}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def defs() -> str:
    return f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{T['BG0']}"/><stop offset="100%" stop-color="{T['BG1']}"/>
  </linearGradient>
  <radialGradient id="glow" cx="90%" cy="0%" r="65%">
    <stop offset="0%" stop-color="{T['ACCENT']}" stop-opacity="0.16"/>
    <stop offset="100%" stop-color="{T['ACCENT']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1" fill="{T['DOT']}" fill-opacity="0.05"/>
  </pattern>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="{T['MUTED']}"/>
  </marker>
</defs>"""


def frame(w, h, x=0, y=0) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#bg)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#dots)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="url(#glow)"/>'
            f'<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="15.5" fill="none" '
            f'stroke="{T["BORDER"]}" stroke-width="1.5"/>')


def svg(h, body, label) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
            f'role="img" aria-label="{esc(label)}">\n{defs()}\n{body}\n</svg>\n')


def chip(x, y, label, color=None, size=12) -> tuple[str, float]:
    w = 18 + len(label) * size * 0.56
    c = color or T["BORDER"]
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="{T["CARD"]}" stroke="{c}"/>'
            + text(x + w / 2, y + 17.5, label, size, T["TEXT"], anchor="middle")), w


def chips(x, y, labels, color=None, size=12) -> str:
    out = []
    for lab in labels:
        s, w = chip(x, y, lab, color, size)
        out.append(s)
        x += w + 8
    return "".join(out)


# ---------------------------------------------------------------- header
def header() -> str:
    h = 230
    body = [frame(W, h)]
    body.append(text(MARGIN + 8, 62, "CURRICULUM VITAE", 12, T["ACCENT"], 700, font=MONO, extra='letter-spacing="2"'))
    body.append(text(MARGIN + 8, 108, "Jaideep Gupta", 42, T["TEXT"], 800))
    body.append(text(MARGIN + 8, 142, "Tableau Developer · Analytics Engineering", 20, T["ACCENT"], 600))
    body.append(text(MARGIN + 8, 170, "4+ years of BI across healthcare, real estate, ed-tech and enterprise", 14, T["MUTED"]))
    body.append(chips(MARGIN + 8, 186, ["Tableau", "Tableau Next", "Power BI", "SQL", "dbt", "Databricks"], size=11.5))
    # decorative mini dashboard: bars + trend line
    bx, by, bw, bh = 700, 52, 252, 126
    body.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="{T["CARD"]}" stroke="{T["BORDER"]}"/>')
    body.append(f'<rect x="{bx + 16}" y="{by + 16}" width="70" height="7" rx="3.5" fill="{T["MUTED"]}" opacity="0.6"/>')
    vals = [38, 52, 44, 66, 58, 80, 72, 92]
    colors = [T["BLUE"], T["BLUE"], T["PURPLE"], T["PURPLE"], T["ORANGE"], T["GOLD"], T["ACCENT"], T["ACCENT"]]
    pts = []
    for i, (v, c) in enumerate(zip(vals, colors)):
        x = bx + 22 + i * 28
        hh = v * 0.8
        y = by + bh - 14 - hh
        body.append(f'<rect x="{x}" y="{y:.1f}" width="16" height="{hh:.1f}" rx="3" fill="{c}" opacity="0.85">'
                    f'<animate attributeName="height" from="0" to="{hh:.1f}" dur="1.2s" begin="{i * 0.08:.2f}s" fill="freeze"/>'
                    f'<animate attributeName="y" from="{by + bh - 14}" to="{y:.1f}" dur="1.2s" begin="{i * 0.08:.2f}s" fill="freeze"/></rect>')
        pts.append(f"{x + 8},{y - 8:.1f}")
    body.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{T["TEXT"]}" stroke-width="1.6" '
                f'stroke-linejoin="round" opacity="0.55"/>')
    return svg(h, "\n".join(body), "Jaideep Gupta, Tableau Developer and Analytics Engineering. 4+ years of BI across healthcare, real estate, ed-tech and enterprise.")


# ---------------------------------------------------------------- stats
def stats() -> str:
    h = 116
    tiles = [("11", "client engagements"), ("6+", "industries served"),
             ("8-hospital", "Tableau analytics app"), ("6", "Tableau Next POCs")]
    gap = 16
    tw = (W - gap * 3) / 4
    body = []
    for i, (big, lab) in enumerate(tiles):
        x = i * (tw + gap)
        body.append(f'<rect x="{x + .75:.1f}" y=".75" width="{tw - 1.5:.1f}" height="{h - 1.5}" rx="14" fill="url(#bg)" '
                    f'stroke="{T["BORDER"]}" stroke-width="1.5"/>'
                    f'<rect x="{x + 24:.1f}" y="24" width="28" height="4" rx="2" fill="{T["ACCENT"]}"/>')
        body.append(text(x + 24, 68, big, 30, T["TEXT"], 800))
        body.append(text(x + 24, 94, lab, 13, T["MUTED"]))
    return svg(h, "\n".join(body), "11 client engagements; 6+ industries served; 8-hospital Tableau analytics app; 6 Tableau Next POCs")


# ---------------------------------------------------------------- timeline
def timeline() -> str:
    h = 190
    start, end = 2022 * 12 + 5, 2026 * 12 + 11  # Jun 2022 .. Nov 2026 (month index)
    x0, x1 = MARGIN + 10, W - MARGIN - 10

    def X(y, m):
        return x0 + (y * 12 + m - 1 - start) / (end - start) * (x1 - x0)

    roles = [  # (title, org, dates, start(y,m), end(y,m), colour key)
        ("SME → Product Analyst", "TutorBin", "Jun 2022 – Dec 2023", (2022, 6), (2023, 12), "PURPLE"),
        ("Assoc. Solution Leader", "Brane Enterprises", "Jan – Sep 2024", (2024, 1), (2024, 9), "ORANGE"),
        ("Data Analyst", "Freelance", "Sep 2024 – Aug 2025", (2024, 9), (2025, 8), "GOLD"),
        ("Tableau Developer", "Kloudrac Group", "Aug 2025 – Present", (2025, 8), (2026, 11), "ACCENT"),
    ]
    body = [frame(W, h)]
    body.append(text(MARGIN + 8, 40, "Career timeline", 16, T["TEXT"], 700))
    ly = 104
    body.append(f'<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{T["BORDER"]}" stroke-width="2"/>')
    for i, (title, org, dates, s, e, ck) in enumerate(roles):
        a, b = X(*s) + 3, X(*e) - 3
        c = T[ck]
        mid = (a + b) / 2
        body.append(f'<rect x="{a:.1f}" y="{ly - 7}" width="{b - a:.1f}" height="14" rx="7" fill="{c}" opacity="0.9"/>')
        body.append(text(mid, ly - 20, title, 13, c, 700, "middle"))
        body.append(text(mid, ly + 32, org, 13, T["TEXT"], 600, "middle"))
        body.append(text(mid, ly + 50, dates, 11.5, T["MUTED"], anchor="middle"))
    nx = X(2026, 11) - 3
    body.append(f'<circle cx="{nx:.1f}" cy="{ly}" r="6" fill="{T["ACCENT"]}"/>'
                f'<circle cx="{nx:.1f}" cy="{ly}" r="6" fill="none" stroke="{T["ACCENT"]}">'
                f'<animate attributeName="r" values="6;13" dur="1.8s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.8;0" dur="1.8s" repeatCount="indefinite"/></circle>')
    return svg(h, "\n".join(body), "Career timeline: TutorBin Jun 2022 to Dec 2023, Brane Enterprises Jan to Sep 2024, Freelance Sep 2024 to Aug 2025, Kloudrac Group Aug 2025 to present.")


# ---------------------------------------------------------------- case studies
def box(x, y, w, h, title, sub, color) -> str:
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="10" fill="{T["CARD"]}" stroke="{color}" stroke-width="1.5"/>'
            + text(x + w / 2, y + h / 2 - 2, title, 13, color, 700, "middle")
            + text(x + w / 2, y + h / 2 + 15, sub, 10.5, T["MUTED"], anchor="middle"))


def arrow(x1, y1, x2, y2) -> str:
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{T["MUTED"]}" '
            f'stroke-width="1.4" marker-end="url(#arrow)"/>')


def case_studies() -> str:
    h = 470
    pw, gap = (W - 16) / 2, 16
    body = []

    # ---- panel A: healthcare app
    ax = 0
    body.append(frame(pw, h, ax, 0))
    body.append(text(ax + 24, 40, "Healthcare · doctor-referral analytics app", 15, T["TEXT"], 700))
    body.append(text(ax + 24, 60, "5-page Tableau app · 8 hospitals · 30K+ visits · 45+ reps", 12, T["MUTED"]))
    bw, bh = 136, 52
    cx = ax + pw / 2
    body.append(box(cx - 90, 82, 180, bh, "Home", "YTD KPIs + KPI glossary", T["ACCENT"]))
    row_y = 186
    xs = [ax + 22 + i * (bw + 12) for i in range(3)]
    pages = [("Bird's-eye", "hospital cards", T["BLUE"]), ("Unit comparison", "MoM · leaderboard", T["PURPLE"]),
             ("Digital outreach", "chatbot engagement", T["ORANGE"])]
    for x, (t_, s_, c_) in zip(xs, pages):
        body.append(arrow(cx, 82 + bh, x + bw / 2, row_y - 2))
        body.append(box(x, row_y, bw, bh, t_, s_, c_))
    body.append(arrow(xs[0] + bw / 2, row_y + bh, xs[1] + bw / 2 - 30, 290 - 2))
    body.append(arrow(xs[1] + bw / 2, row_y + bh, xs[1] + bw / 2, 290 - 2))
    body.append(box(xs[1] - 30, 290, bw + 60, bh, "Rep drill-down", "user-level visits & referrals", T["GOLD"]))
    body.append(text(xs[1] + bw / 2 + 8, 270, "click-through", 10.5, T["MUTED"], font=MONO))
    body.append(f'<line x1="{ax + 22}" y1="372" x2="{ax + pw - 22}" y2="372" stroke="{T["BORDER"]}"/>')
    body.append(chips(ax + 22, 388, ["drill-through", "parameters", "MoM calcs"]))
    body.append(chips(ax + 22, 422, ["6 standardised KPIs", "dynamic callouts"]))

    # ---- panel B: real-estate suite
    bx = pw + gap
    body.append(frame(pw, h, bx, 0))
    body.append(text(bx + 24, 40, "Real estate · revenue & sales suite", 15, T["TEXT"], 700))
    body.append(text(bx + 24, 60, "executive dashboards · 15+ projects · quarterly view", 12, T["MUTED"]))
    cxb = bx + pw / 2
    body.append(box(cxb - 150, 82, 300, bh, "Revenue & Sales Agreement", "booked · collected · pending · vs target", T["ACCENT"]))
    xsb = [bx + 22 + i * (bw + 12) for i in range(3)]
    linked = [("Pipeline", "linked dashboard", T["BLUE"]), ("Lead generation", "linked dashboard", T["PURPLE"]),
              ("Project view", "sold vs unsold stock", T["ORANGE"])]
    for x, (t_, s_, c_) in zip(xsb, linked):
        body.append(arrow(cxb, 82 + bh, x + bw / 2, row_y - 2))
        body.append(box(x, row_y, bw, bh, t_, s_, c_))
    body.append(text(bx + 24, 278, "5-level sales hierarchy filters", 12, T["MUTED"], font=MONO))
    lvl = ["HOD", "L1", "L2", "L3", "L4", "L5"]
    x = bx + 24
    for i, l in enumerate(lvl):
        s, w = chip(x, 292, l, T["GOLD"])
        body.append(s)
        if i < len(lvl) - 1:
            body.append(text(x + w + 9, 310, "›", 15, T["MUTED"], anchor="middle"))
        x += w + 18
    body.append(f'<line x1="{bx + 22}" y1="372" x2="{bx + pw - 22}" y2="372" stroke="{T["BORDER"]}"/>')
    body.append(chips(bx + 22, 388, ["QoQ comparisons", "billed vs non-billed"]))
    body.append(chips(bx + 22, 422, ["revenue vs target", "inventory tracking"]))

    return svg(h, "\n".join(body), "Anonymised case studies. Healthcare: 5-page Tableau app from a home page with KPI glossary to bird's-eye hospital view, unit comparison and digital outreach, with click-through to rep drill-down. Real estate: executive revenue and sales agreement dashboard linked to pipeline, lead generation and project views, filtered by a 5-level sales hierarchy.")


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for theme, suffix in (("dark", ""), ("light", "-light")):
        T.clear()
        T.update(THEMES[theme])
        for name, fn in (("header", header), ("stats", stats), ("timeline", timeline), ("case-studies", case_studies)):
            (out / f"{name}{suffix}.svg").write_text(fn(), encoding="utf-8")
    print("wrote", sorted(p.name for p in out.iterdir()))
