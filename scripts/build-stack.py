#!/usr/bin/env python3
"""Builds assets/stack.svg. Fonts are copied from assets/header.svg."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = "".join(re.findall(r"@font-face\{[^}]*\}", (ROOT / "assets/header.svg").read_text()))
MONO = "font-family:JB, ui-monospace, Menlo, Consolas, monospace"

ROWS = [
    ("core languages", [("C++", "#FEE123", True), ("C", "#A8B9CC"), ("Python", "#4B8BBE"),
                        ("TypeScript", "#3178C6"), ("JavaScript", "#F7DF1E"), ("SQL", "#E38C00")]),
    ("systems + tooling", [("Linux", "#FCC624"), ("CMake", "#4C9BD6"), ("GDB", "#C73E3E"),
                           ("Git", "#F05032"), ("Docker", "#2496ED"), ("Bash", "#4EAA25")]),
    ("networking", [("TCP/IP", "#2DD4BF"), ("Socket programming", "#38BDF8"), ("Wireshark", "#1679A7")]),
    ("apps + web", [("React", "#61DAFB"), ("Next.js", "#E6E6E6"), ("Tauri", "#FFC131"),
                    ("Tailwind", "#38BDF8"), ("Cloudflare", "#F6821F")]),
]

def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;")

alt = "Tech stack: " + ". ".join(f"{label}: {', '.join(c[0] + (' (primary)' if len(c) > 2 else '') for c in chips)}" for label, chips in ROWS) + "."
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320" role="img" aria-label="{esc(alt)}">',
     f'<title>{esc(alt)}</title><style>{FONTS}</style>',
     '<rect width="1280" height="320" rx="22" fill="#0C1611"/>',
     '<rect x="1" y="1" width="1278" height="318" rx="21" fill="none" stroke="#1F3529" stroke-width="2"/>']
for i, (label, chips) in enumerate(ROWS):
    y = 40 + 62 * i
    s.append(f'<text x="48" y="{y + 26}" style="{MONO};font-size:17px" fill="#5E7A68"><tspan fill="#FEE123">#</tspan> {esc(label)}</text>')
    x = 290.0
    for chip in chips:
        name, color = chip[0], chip[1]
        primary = len(chip) > 2
        size, weight, per = (19, 700, 11.4) if primary else (17, 400, 10.2)
        w = round(len(name) * per + 50)
        if primary:
            s.append(f'<rect x="{x:g}" y="{y}" width="{w}" height="40" rx="20" fill="#FEE123" stroke="#FEE123" stroke-width="1.5"/>')
            s.append(f'<circle cx="{x + 22:g}" cy="{y + 20}" r="6" fill="#0C1611"/>')
            s.append(f'<text x="{x + 36:g}" y="{y + 26}" style="{MONO};font-size:{size}px;font-weight:{weight}" fill="#0C1611">{esc(name)}</text>')
        else:
            s.append(f'<rect x="{x:g}" y="{y}" width="{w}" height="40" rx="20" fill="#12211A" stroke="#1F3529" stroke-width="1.5"/>')
            s.append(f'<circle cx="{x + 22:g}" cy="{y + 20}" r="6" fill="{color}"/>')
            s.append(f'<text x="{x + 36:g}" y="{y + 26}" style="{MONO};font-size:{size}px;font-weight:{weight}" fill="#F4EFD8">{esc(name)}</text>')
        x += w + 12.2
    assert x < 1240, f"row '{label}' overflows ({x:.0f}px)"
s.append("</svg>")
(ROOT / "assets/stack.svg").write_text("".join(s))
print("wrote assets/stack.svg")
