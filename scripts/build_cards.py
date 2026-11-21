"""Builds the pixel-art (16-bit) SVG cards for the GitHub profile README.

Each card is a self-contained animated SVG: CSS + SMIL animations, embedded
pixel fonts (Press Start 2P and VT323, both SIL OFL) and the pixel avatar.
Run:  python3 scripts/build_cards.py        -> writes cards/*.svg
Set STATIC=1 to render the final frame without animation (for previews).
"""
import base64
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "scripts" / "assets"
OUT = Path(os.environ.get("OUT_DIR", ROOT / "cards"))
STATIC = os.environ.get("STATIC") == "1"

# 16-bit palette
BG = "#140f2d"
PANEL = "#1e1846"
PANEL2 = "#2a2160"
INK = "#0b0820"
PINK = "#ff5c8a"
GOLD = "#ffd166"
CYAN = "#4cc9f0"
GREEN = "#8ce36b"
TEXT = "#f2e9ff"
DIM = "#a59bd0"
LIGHT2 = "#3a2f80"
BUILD = "#2a2160"
STAR = None

THEME = os.environ.get("THEME", "dark")
SUFFIX = "" if THEME == "dark" else "-light"
if THEME == "light":
    BG = "#fbf5e6"
    PANEL = "#fffaf0"
    PANEL2 = "#efe7ff"
    INK = "#2b2142"
    PINK = "#d9336a"
    GOLD = "#c27c00"
    CYAN = "#1b7fb3"
    GREEN = "#2b8a3e"
    TEXT = "#2b2142"
    DIM = "#6a6090"
    LIGHT2 = "#e2d6ff"
    BUILD = "#cbbdf0"


def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


FONT_CSS = f"""
@font-face{{font-family:'PS2P';src:url(data:font/woff2;base64,{b64(ASSETS / 'pressstart2p.woff2')}) format('woff2');}}
@font-face{{font-family:'VT';src:url(data:font/woff2;base64,{b64(ASSETS / 'vt323.woff2')}) format('woff2');}}
.h{{font-family:'PS2P',monospace;}}
.t{{font-family:'VT',monospace;}}
"""

BASE_CSS = """
@keyframes pop{0%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:none}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes twinkle{0%,100%{opacity:.25}50%{opacity:1}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.pop{opacity:0;animation:pop .5s steps(4) forwards;}
.blink{animation:blink 1s steps(1) infinite;}
.tw{animation:twinkle 2.4s steps(3) infinite;}
.pulse{animation:pulse 1.2s steps(2) infinite;}
.bar{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:grow 1.2s steps(12) forwards;}
@media (prefers-reduced-motion: reduce){.pop,.bar{animation:none;opacity:1;transform:none}.blink,.tw,.pulse{animation:none}}
"""

STATIC_CSS = """
.pop,.bar,.blink,.tw,.pulse{animation:none!important;opacity:1!important;transform:none!important}
"""


def svg(w, h, body, extra_css=""):
    css = FONT_CSS + BASE_CSS + extra_css + (STATIC_CSS if STATIC else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges">'
            f'<style>{css}</style>{body}</svg>')


def frame(x, y, w, h, fill=PANEL, border=INK, light=PANEL2, b=6):
    """Pixel window with notched corners and a bevel highlight."""
    return (
        f'<rect x="{x + b}" y="{y}" width="{w - 2 * b}" height="{h}" fill="{border}"/>'
        f'<rect x="{x}" y="{y + b}" width="{w}" height="{h - 2 * b}" fill="{border}"/>'
        f'<rect x="{x + b}" y="{y + b}" width="{w - 2 * b}" height="{h - 2 * b}" fill="{fill}"/>'
        f'<rect x="{x + b}" y="{y + b}" width="{w - 2 * b}" height="{b}" fill="{light}"/>'
        f'<rect x="{x + b}" y="{y + b}" width="{b}" height="{h - 2 * b}" fill="{light}"/>'
    )


def stars(w, h, n=40, seed=7):
    import random
    r = random.Random(seed)
    out = []
    for i in range(n):
        x, y = r.randrange(10, w - 10), r.randrange(10, h - 10)
        s = r.choice([3, 3, 3, 6])
        c = r.choice([GOLD, CYAN, DIM, DIM, TEXT])
        out.append(f'<rect class="tw" style="animation-delay:{r.random() * 2.4:.2f}s" x="{x}" y="{y}" width="{s}" height="{s}" fill="{c}"/>')
    return "".join(out)


def sprite(rows, x, y, px, colors):
    """Draw a tiny pixel sprite from strings; '.' = transparent."""
    out = []
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                out.append(f'<rect x="{x + i * px}" y="{y + j * px}" width="{px}" height="{px}" fill="{colors[ch]}"/>')
    return "".join(out)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- hero
BAITEREK = [
    "........ccc.........",
    "......ccgggcc.......",
    ".....cgggggggc......",
    "....cgggwgggggc.....",
    "....cggwwgggggc.....",
    "....cgggggggggc.....",
    ".....cgggggggc......",
    "...s..cgggggc..s....",
    "...ss..ccccc..ss....",
    "....ss...s...ss.....",
    ".....ss..s..ss......",
    "......ss.s.ss.......",
    ".......sssss........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    "........sss.........",
    ".......sssss........",
    "......sssssss.......",
    ".....sssssssss......",
]


def skyline(x0, base, w):
    import random
    r = random.Random(3)
    out = []
    x = x0
    while x < x0 + w:
        bw = r.choice([36, 48, 60])
        bh = r.choice([70, 90, 110, 130, 150])
        if x0 + 150 < x < x0 + 250:
            bh = r.choice([60, 80])
        out.append(f'<rect x="{x}" y="{base - bh}" width="{bw - 6}" height="{bh}" fill="{BUILD}"/>')
        for wy in range(base - bh + 12, base - 10, 18):
            for wx in range(x + 8, x + bw - 14, 14):
                if r.random() < 0.45:
                    out.append(f'<rect class="tw" style="animation-delay:{r.random() * 2.4:.2f}s" x="{wx}" y="{wy}" width="6" height="6" fill="{GOLD}"/>')
        x += bw
    return "".join(out)


def hero():
    W, H = 1200, 420
    typed = "AI ENGINEER / ML + CV / ASTANA"
    n = len(typed)
    CW = 14.6
    steps = ";".join(str(int(CW * i)) for i in range(n + 1))
    times = ";".join(f"{i / n:.3f}" for i in range(n + 1))
    type_anim = "" if STATIC else (
        f'<animate attributeName="width" values="{steps}" keyTimes="{times}" dur="2.2s" begin="0.9s" calcMode="discrete" fill="freeze"/>')
    tower_x = 900
    body = (
        frame(0, 0, W, H, fill=BG, border=INK, light=LIGHT2) + stars(W, 260, n=30)
        + f'<g class="pop" style="animation-delay:.3s">' + skyline(700, 372, 470) + '</g>'
        + f'<g class="pop" style="animation-delay:.6s">'
        + sprite(BAITEREK, tower_x, 372 - len(BAITEREK) * 8, 8, {"c": INK, "g": GOLD, "w": TEXT if THEME == "dark" else "#fff3c4", "s": DIM})
        + '</g>'
        + f'<rect x="6" y="372" width="{W - 12}" height="42" fill="{PANEL2}"/>'
        + "".join(f'<rect x="{x}" y="380" width="24" height="6" fill="{DIM}"/>' for x in range(30, W - 30, 48))
        + f'<text class="h pop" style="animation-delay:.1s" x="60" y="92" font-size="16" fill="{PINK}">PLAYER 1</text>'
        + f'<text class="h pop" style="animation-delay:.25s" x="60" y="160" font-size="52" fill="{TEXT}">MAXIM</text>'
        + f'<text class="h pop" style="animation-delay:.4s" x="60" y="226" font-size="52" fill="{GOLD}">KIRIK</text>'
        + f'<clipPath id="ty"><rect x="60" y="250" width="{int(CW * n) if STATIC else 0}" height="40">{type_anim}</rect></clipPath>'
        + f'<text class="t" clip-path="url(#ty)" x="60" y="280" font-size="34" fill="{CYAN}">{typed}</text>'
        + f'<rect class="blink" x="{60 + int(CW * n) + 8}" y="256" width="14" height="28" fill="{CYAN}"/>'
        + f'<g class="pop" style="animation-delay:3.2s">'
          f'<rect class="pulse" x="60" y="318" width="14" height="14" fill="{GREEN}"/>'
          f'<text class="t" x="86" y="332" font-size="28" fill="{GREEN}">ONLINE: OPEN TO WORK</text></g>'
        + f'<text class="h blink" x="60" y="404" font-size="12" fill="{GOLD}">PRESS START &gt;</text>'
    )
    return svg(W, H, body)


# ---------------------------------------------------------------- quests
QUESTS = [
    dict(slug="quest-rsl", no="01", title="SIGN LANGUAGE AI", status="DEPLOYED", sc=GREEN,
         text="Russian Sign Language recognition for deaf and hard of hearing users, built for the TilMind platform. "
              "MediaPipe Holistic keypoints feed an LSTM / Transformer sequence model trained on the Slovo dataset. "
              "Runs in Docker behind Nginx on the client's server.",
         chips=["PyTorch", "MediaPipe", "OpenCV", "Docker"],
         sprite=["..aa..aa..", "..aa..aa..", "..aa.aaa..", "a.aaaaaa..", "aaaaaaaaa.", ".aaaaaaaa.",
                 "..aaaaaa..", "..aaaaaa..", "...aaaa...", "...aaaa..."], col={"a": GOLD}),
    dict(slug="quest-xzt", no="02", title="XZT-IIOT", status="RESEARCH", sc=CYAN,
         text="Explainable zero-trust access control for industrial IoT: per-request trust scoring with feature-level "
              "explanations, adversarial validation and a lightweight blockchain hash-chain audit log. "
              "Evaluated on the real Edge-IIoTset dataset.",
         chips=["Python", "scikit-learn", "SHAP"],
         sprite=["....aa....", "..aaaaaa..", ".aaaaaaaa.", ".aabbbbaa.", ".aabaabaa.", ".aabbbbaa.",
                 ".aaabbaaa.", "..aaaaaa..", "...aaaa...", "....aa...."], col={"a": CYAN, "b": INK}),
    dict(slug="quest-ais", no="03", title="TUTAS + CONSTRUCTIONOS", status="STARTUP", sc=PINK,
         text="Product structure and UX/UI design in the AIS startup, where I am CDO. Tutas is a team task manager with director "
              "and employee roles. ConstructionOS is a digital construction supervision system with an agreed "
              "two-way integration with the state platform E-Qurylys.",
         chips=["Figma", "Next.js", "UX/UI"],
         sprite=["....a.....", "...aaa....", "...aba....", "..aaaaa...", "..ababa...", ".aaaaaaa..",
                 ".abababa..", ".aaaaaaa..", ".abababa..", "aaaaaaaaa."], col={"a": PINK, "b": INK}),
    dict(slug="quest-coffee", no="04", title="COFFEE LAKE SYSTEM", status="IN PRODUCTION", sc=GOLD,
         text="Software used every day by real guests and baristas. A multilingual digital menu with WhatsApp "
              "ordering and Google Sheets as a live CMS, plus a shift-closing system: receipt photos go to Drive "
              "and the owner reviews everything in an admin panel.",
         chips=["Next.js", "Apps Script", "Sheets API"],
         sprite=["..a.a.a...", "...a.a....", "..........", "bbbbbbbb..", "bccccccbbb", "bccccccb.b",
                 "bccccccbbb", "bccccccb..", ".bbbbbb...", "aaaaaaaaa."], col={"a": DIM, "b": TEXT, "c": "#8a5a3c"}),
    dict(slug="quest-cargo", no="05", title="CARGO REQUEST AGENT", status="AI AGENT", sc=CYAN,
         text="AI agent that reads logistics WhatsApp groups, detects cargo requests and turns free text into "
              "structured JSON: route, weight, dates, contact. Normalizes cities, removes duplicates and pushes "
              "loads to a drivers' app.",
         chips=["Node.js", "Baileys", "Claude API"],
         sprite=["..........", "aaaaaa....", "abbbba....", "abbbbaccc.", "abbbbacbcc", "aaaaaaccccc",
                 "aaaaaaccccc", ".dd....dd..", ".dd....dd..", ".........."], col={"a": CYAN, "b": INK, "c": GOLD, "d": DIM}),
    dict(slug="quest-traffic", no="06", title="FAIR TRAFFIC CONTROL", status="IEEE SIST", sc=GREEN,
         text="Deep reinforcement learning agent that controls traffic lights while keeping waiting time fair "
              "across all directions, trained and tested in the SUMO simulator. Co-authored paper at IEEE SIST 2026.",
         chips=["Python", "SUMO / TraCI", "DRL"],
         sprite=["..aaaa....", "..abba....", "..abba....", "..aaaa....", "..acca....", "..acca....",
                 "..aaaa....", "..adda....", "..adda....", "..aaaa...."], col={"a": INK, "b": PINK, "c": GOLD, "d": GREEN}),
    dict(slug="quest-land", no="07", title="HIDDEN LAND CHANGES", status="IEEE SIST", sc=GREEN,
         text="Framework that decouples optical and radar satellite signals to find land surface changes hidden "
              "from either sensor alone. Paper at IEEE SIST 2026, extended with a tamper-evident blockchain "
              "provenance layer.",
         chips=["Python", "Remote sensing", "Blockchain"],
         sprite=["a........a", "aa......aa", "aaa.bb.aaa", "aaaabbaaaa", "aaa.bb.aaa", "aa..bb..aa",
                 "a...bb...a", "....bb....", "...bbbb...", "..bbbbbb.."], col={"a": CYAN, "b": DIM}),
    dict(slug="quest-shorts", no="08", title="SHORTS PIPELINE", status="TOOLING", sc=PINK,
         text="Turns long videos into ready-to-post vertical shorts: automatic subtitles with faster-whisper "
              "and cut points from scene detection. Built for my own content and client clips.",
         chips=["Python", "faster-whisper", "FFmpeg"],
         sprite=["aaaaaaaaaa", "ab.ab.ab.a", "aaaaaaaaaa", "accccccca.", "acccbccca.", "acccbbcca.",
                 "acccbccca.", "accccccca.", "aaaaaaaaaa", "ab.ab.ab.a"], col={"a": DIM, "b": PINK, "c": INK}),
]


def chip_row(items, x, y, maxx, size=24):
    out = ""
    for c in items:
        w = int(len(c) * 13.5) + 28
        if x + w > maxx:
            break
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="34" fill="{INK}"/>'
                f'<rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="28" fill="{PANEL2}"/>'
                f'<text class="t" x="{x + w / 2}" y="{y + 25}" font-size="{size}" fill="{TEXT}" text-anchor="middle">{esc(c)}</text>')
        x += w + 12
    return out


def quest(q, i):
    W, H = 590, 384
    d = f"{0.12 * (i % 2) + 0.1:.2f}s"
    body = (
        f'<g class="pop" style="animation-delay:{d}">'
        + frame(0, 0, W, H)
        + f'<text class="h" x="40" y="56" font-size="12" fill="{PINK}">QUEST {q["no"]}</text>'
        + f'<rect x="{W - 40 - len(q["status"]) * 12 - 24}" y="34" width="{len(q["status"]) * 12 + 24}" height="30" fill="{q["sc"]}"/>'
        + f'<text class="h" x="{W - 52}" y="55" font-size="11" fill="{INK}" text-anchor="end">{q["status"]}</text>'
        + f'<text class="h" x="40" y="96" font-size="{17 if len(q["title"]) > 16 else 20}" fill="{TEXT}">{q["title"]}</text>'
        + wrap_lines(q["text"], 40, 130, 40, size=25, color=DIM, lh=26)
        + sprite(q["sprite"], W - 96, 104, 6, q["col"])
        + chip_row(q["chips"], 40, 318, W - 30)
        + '</g>'
    )
    return svg(W, H, body)


def wrap_lines(txt, x, y, maxc, size=23, color=TEXT, lh=24):
    lines, cur = [], ""
    for w in txt.split():
        if len(cur) + len(w) + 1 > maxc and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return "".join(f'<text class="t" x="{x}" y="{y + k * lh}" font-size="{size}" fill="{color}">{esc(l)}</text>' for k, l in enumerate(lines))


# ---------------------------------------------------------------- stats
STATS = [("MACHINE LEARNING / CV", 0.9, PINK), ("UX / UI DESIGN", 0.85, GOLD),
         ("FRONTEND", 0.75, CYAN), ("EMBEDDED / IIOT", 0.7, GREEN)]
INVENTORY = ["Python", "PyTorch", "OpenCV", "MediaPipe", "C++", "STM32", "FreeRTOS",
             "Next.js", "React", "TypeScript", "Figma", "Docker", "Linux", "Git"]


def stats():
    W, H = 1200, 330
    body = frame(0, 0, W, H) + f'<text class="h" x="40" y="58" font-size="16" fill="{GOLD}">CHARACTER STATS</text>'
    for k, (name, v, c) in enumerate(STATS):
        y = 96 + k * 52
        body += (f'<text class="t" x="40" y="{y + 22}" font-size="28" fill="{TEXT}">{name}</text>'
                 f'<rect x="300" y="{y}" width="280" height="28" fill="{INK}"/>'
                 f'<rect class="bar" style="animation-delay:{0.2 + k * 0.2:.1f}s" x="304" y="{y + 4}" width="{int(272 * v)}" height="20" fill="{c}"/>'
                 + "".join(f'<rect x="{304 + s * 34}" y="{y + 4}" width="4" height="20" fill="{INK}"/>' for s in range(1, 8)))
    body += f'<text class="h" x="660" y="58" font-size="16" fill="{GOLD}">INVENTORY</text>'
    x, y = 660, 84
    for it in INVENTORY:
        w = int(len(it) * 13.5) + 28
        if x + w > W - 40:
            x, y = 660, y + 46
        body += (f'<g class="pop" style="animation-delay:{0.1 + INVENTORY.index(it) * 0.06:.2f}s">'
                 f'<rect x="{x}" y="{y}" width="{w}" height="34" fill="{INK}"/>'
                 f'<rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="28" fill="{PANEL2}"/>'
                 f'<text class="t" x="{x + w / 2}" y="{y + 25}" font-size="24" fill="{TEXT}" text-anchor="middle">{it}</text></g>')
        x += w + 10
    return svg(W, H, body)


# ---------------------------------------------------------------- achievements
ACH = [
    ("IEEE SIST 2026", "Fair predictive traffic signal control (co-author)", GOLD),
    ("IEEE SIST 2026", "Optical-radar hidden land change detection (co-author)", GOLD),
    ("SCOPUS", "Research papers published in Scopus-indexed venues", GOLD),
    ("GOV INTERNSHIP", "Presidential Affairs Admin. and Ministry of Digital Development", CYAN),
    ("WORLDSKILLS", "Competed in the WorldSkills championship", CYAN),
    ("CISCO + HUAWEI", "Cisco Networking and Huawei ICT Academy training", CYAN),
    ("E-QURYLYS", "Agreed state platform integration for ConstructionOS", PINK),
    ("ENACTUS", "Sign language project submitted to Enactus, Brazil", PINK),
    ("IN PRODUCTION", "Software used daily at a real coffee shop chain", PINK),
]
TROPHY = ["aaaaaaaa", "aaaaaaaa", ".aaaaaa.", "..aaaa..", "...aa...", "...aa...", "..bbbb..", ".bbbbbb."]


def achievements():
    W = 1200
    rows = (len(ACH) + 2) // 3
    H = 96 + rows * 146 + 24
    body = frame(0, 0, W, H) + f'<text class="h" x="40" y="58" font-size="16" fill="{GOLD}">ACHIEVEMENTS UNLOCKED</text>'
    body += f'<text class="h" x="{W - 40}" y="58" font-size="12" fill="{DIM}" text-anchor="end">{len(ACH)}/{len(ACH)}</text>'
    for k, (tag, txt, col) in enumerate(ACH):
        x = 40 + (k % 3) * 380
        y = 84 + (k // 3) * 146
        body += (f'<g class="pop" style="animation-delay:{0.2 + k * 0.18:.2f}s">'
                 + frame(x, y, 360, 132, fill=PANEL2, light=LIGHT2, b=4)
                 + sprite(TROPHY, x + 22, y + 30, 7, {"a": col, "b": DIM})
                 + f'<text class="h" x="{x + 94}" y="{y + 38}" font-size="11" fill="{col}">{tag}</text>'
                 + wrap_lines(txt, x + 94, y + 68, 22, size=23, lh=23)
                 + '</g>')
    return svg(W, H, body)


# ---------------------------------------------------------------- journey
JOURNEY = [("2022", "ASTANA IT", "COLLEGE"), ("2024", "GOV", "INTERNSHIP"), ("2024", "AITU", "BACHELOR"),
           ("2025", "IT SUPPORT", "ENGINEER"), ("2026", "STARTUP", "CDO"), ("2026", "ML ENG", "TILMIND"), ("2027", "NEXT", "LEVEL?")]


def journey():
    W, H = 1200, 250
    body = frame(0, 0, W, H) + f'<text class="h" x="40" y="58" font-size="16" fill="{GOLD}">WORLD MAP</text>'
    n = len(JOURNEY)
    step = (W - 160) / (n - 1)
    y = 140
    body += "".join(f'<rect x="{80 + s * 12}" y="{y - 2}" width="6" height="6" fill="{DIM}"/>' for s in range(int((W - 160) / 12) + 1))
    for k, (yr, a, b) in enumerate(JOURNEY):
        x = int(80 + k * step)
        last = k == n - 1
        col = DIM if last else (GOLD if k == n - 2 else CYAN)
        body += (f'<g class="pop" style="animation-delay:{0.2 + k * 0.25:.2f}s">'
                 f'<rect x="{x - 14}" y="{y - 14}" width="28" height="28" fill="{INK}"/>'
                 f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" fill="{col}" class="{"blink" if last else ""}"/>'
                 f'<text class="h" x="{x}" y="{y - 30}" font-size="11" fill="{PINK}" text-anchor="middle">{yr}</text>'
                 f'<text class="t" x="{x}" y="{y + 46}" font-size="24" fill="{TEXT}" text-anchor="middle">{a}</text>'
                 f'<text class="t" x="{x}" y="{y + 70}" font-size="24" fill="{DIM}" text-anchor="middle">{b}</text></g>')
    return svg(W, H, body)


# ---------------------------------------------------------------- activity (data from GitHub Action)
def activity():
    W, H = 1200, 300
    data_path = ROOT / "data" / "activity.json"
    data = json.loads(data_path.read_text()) if data_path.exists() else {"months": [], "total": 0, "streak": 0}
    months = data["months"][-12:]
    body = frame(0, 0, W, H) + f'<text class="h" x="40" y="58" font-size="16" fill="{GOLD}">XP THIS YEAR</text>'
    if months:
        body += (f'<text class="h" x="{W - 40}" y="58" font-size="14" fill="{TEXT}" text-anchor="end">'
                 f'{data["total"]} CONTRIBUTIONS  ·  BEST STREAK {data["streak"]}D</text>')
    if not months:
        body += f'<text class="h blink" x="{W / 2}" y="170" font-size="16" fill="{DIM}" text-anchor="middle">LOADING...</text>'
    if months:
        mx = max(m["count"] for m in months) or 1
        best = max(range(len(months)), key=lambda i: months[i]["count"])
        bw = (W - 80) // len(months)
        for i, m in enumerate(months):
            h = max(6, int(170 * m["count"] / mx) // 6 * 6)
            x = 40 + i * bw + 8
            c = GOLD if i == best else CYAN
            body += (f'<rect class="pop" style="animation-delay:{0.05 * i:.2f}s" x="{x}" y="{250 - h}" width="{bw - 16}" height="{h}" fill="{c}"/>'
                     f'<text class="t" x="{x + (bw - 16) / 2}" y="278" font-size="22" fill="{DIM}" text-anchor="middle">{m["label"]}</text>')
    return svg(W, H, body)


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / f"hero{SUFFIX}.svg").write_text(hero())
    for i, q in enumerate(QUESTS):
        (OUT / f"{q['slug']}{SUFFIX}.svg").write_text(quest(q, i))
    (OUT / f"stats{SUFFIX}.svg").write_text(stats())
    (OUT / f"achievements{SUFFIX}.svg").write_text(achievements())
    (OUT / f"journey{SUFFIX}.svg").write_text(journey())
    (OUT / f"activity{SUFFIX}.svg").write_text(activity())
    print("cards written to", OUT)


if __name__ == "__main__":
    if "THEME" in os.environ:
        main()
    else:
        import subprocess, sys
        for t in ("dark", "light"):
            subprocess.run([sys.executable, __file__], env={**os.environ, "THEME": t}, check=True)
