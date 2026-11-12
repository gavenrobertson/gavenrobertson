#!/usr/bin/env python3
"""Builds project and client cards in assets/ (640x340, shared style).
Fonts are copied from assets/header.svg so nothing extra is needed."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "assets/header.svg").read_text()
FONTS = "".join(re.findall(r"@font-face\{[^}]*\}", src))
STYLE = (FONTS +
  ".pulse{animation:pulse 2.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}"
  "@keyframes pulse{0%,100%{opacity:.25;transform:scale(1)}50%{opacity:0;transform:scale(2.4)}}"
  ".live{animation:live 1.6s ease-in-out infinite}@keyframes live{50%{opacity:.35}}"
  ".tab{animation:tab 6s steps(1) infinite}@keyframes tab{0%,33%{opacity:1}34%,100%{opacity:0}}"
  ".tab2{animation:tab2 6s steps(1) infinite}@keyframes tab2{0%,33%{opacity:0}34%,66%{opacity:1}67%,100%{opacity:0}}"
  ".tab3{animation:tab3 6s steps(1) infinite}@keyframes tab3{0%,66%{opacity:0}67%,100%{opacity:1}}"
  "@media (prefers-reduced-motion:reduce){.pulse,.live,.tab,.tab2,.tab3{animation:none}.tab2,.tab3{opacity:0}}")
MONO = "font-family:JB, ui-monospace, Menlo, Consolas, monospace"
SANS = "font-family:BG, 'Segoe UI', Helvetica, Arial, sans-serif"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def card(name, title, title_size, eyebrow, desc, tags, art, bg, border, accent, text, muted, chip):
    alt = f"{title}: {' '.join(desc)}"
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="340" viewBox="0 0 640 340" role="img" aria-label="{esc(alt)}">',
         f'<title>{esc(alt)}</title><style>{STYLE}</style>',
         f'<rect width="640" height="340" rx="20" fill="{bg}"/>',
         f'<rect x="1" y="1" width="638" height="338" rx="19" fill="none" stroke="{border}" stroke-width="2"/>',
         art,
         f'<circle class="pulse" cx="45" cy="52" r="5" fill="#4CD964"/><circle cx="45" cy="52" r="5" fill="#4CD964"/>',
         f'<text x="60" y="57" style="{MONO};font-weight:700;font-size:14px;letter-spacing:1.5px" fill="{accent}">{esc(eyebrow)}</text>',
         f'<text x="38" y="112" style="{SANS};font-weight:800;font-size:{title_size}px;letter-spacing:-.8px" fill="{text}">{esc(title)}</text>']
    for i, line in enumerate(desc):
        s.append(f'<text x="40" y="{152 + 28*i}" style="{SANS};font-weight:400;font-size:20px" fill="{muted}">{esc(line)}</text>')
    x = 40
    for t in tags:
        w = len(t) * 9 + 16
        s.append(f'<rect x="{x}" y="270" width="{w}" height="34" rx="17" fill="{chip}" stroke="{border}" stroke-width="1.5"/>')
        s.append(f'<text x="{x + w/2}" y="292" text-anchor="middle" style="{MONO};font-size:15px" fill="{text}">{esc(t)}</text>')
        x += w + 10.25
    s.append("</svg>")
    (ROOT / "assets" / f"card-{name}.svg").write_text("".join(s))
    print("wrote", f"assets/card-{name}.svg")

# --- Redemption Church: a phone with a LIVE badge and the tabbed connect section ---
R = dict(bg="#1A0D12", border="#3D1F2B", accent="#FF8FA3", text="#FFF1F3", muted="#C9A2AD", chip="#2A141D")
phone = f'''<g transform="translate(440 30)">
<rect x="0" y="0" width="156" height="280" rx="22" fill="#120A0E" stroke="{R['border']}" stroke-width="2"/>
<rect x="8" y="8" width="140" height="264" rx="16" fill="#1F1016"/>
<rect x="56" y="14" width="44" height="6" rx="3" fill="#120A0E"/>
<rect x="22" y="34" width="60" height="8" rx="4" fill="#FFF1F3" opacity=".9"/>
<rect x="22" y="48" width="92" height="5" rx="2.5" fill="#C9A2AD" opacity=".5"/>
<rect x="22" y="66" width="112" height="22" rx="11" fill="#3A1420"/>
<circle class="live" cx="36" cy="77" r="4.5" fill="#FF4D6D"/>
<text x="46" y="81" style="{MONO};font-weight:700;font-size:10.5px;letter-spacing:1px" fill="#FF8FA3">LIVE NOW</text>
<text x="108" y="81" style="{MONO};font-size:9.5px" fill="#C9A2AD">SUN</text>
<g>
<rect x="22" y="102" width="34" height="18" rx="9" fill="#FF8FA3"/><rect x="60" y="102" width="34" height="18" rx="9" fill="#2A141D"/><rect x="98" y="102" width="36" height="18" rx="9" fill="#2A141D"/>
<text x="39" y="114.5" text-anchor="middle" style="{MONO};font-size:9px;font-weight:700" fill="#1A0D12">Kids</text>
<text x="77" y="114.5" text-anchor="middle" style="{MONO};font-size:9px" fill="#C9A2AD">Youth</text>
<text x="116" y="114.5" text-anchor="middle" style="{MONO};font-size:9px" fill="#C9A2AD">Groups</text>
</g>
<g class="tab2"><rect x="22" y="102" width="34" height="18" rx="9" fill="#2A141D"/><rect x="60" y="102" width="34" height="18" rx="9" fill="#FF8FA3"/>
<text x="39" y="114.5" text-anchor="middle" style="{MONO};font-size:9px" fill="#C9A2AD">Kids</text>
<text x="77" y="114.5" text-anchor="middle" style="{MONO};font-size:9px;font-weight:700" fill="#1A0D12">Youth</text></g>
<g class="tab3"><rect x="22" y="102" width="34" height="18" rx="9" fill="#2A141D"/><rect x="98" y="102" width="36" height="18" rx="9" fill="#FF8FA3"/>
<text x="39" y="114.5" text-anchor="middle" style="{MONO};font-size:9px" fill="#C9A2AD">Kids</text>
<text x="116" y="114.5" text-anchor="middle" style="{MONO};font-size:9px;font-weight:700" fill="#1A0D12">Groups</text></g>
<rect x="22" y="130" width="112" height="7" rx="3.5" fill="#C9A2AD" opacity=".45"/>
<rect x="22" y="143" width="96" height="7" rx="3.5" fill="#C9A2AD" opacity=".3"/>
<rect x="22" y="156" width="104" height="7" rx="3.5" fill="#C9A2AD" opacity=".3"/>
<rect x="22" y="180" width="112" height="30" rx="8" fill="#2A141D" stroke="{R['border']}"/>
<text x="30" y="193" style="{MONO};font-size:9px" fill="#C9A2AD">sermon</text>
<text x="30" y="204" style="{MONO};font-size:9.5px;font-weight:700" fill="#FFF1F3">Latest message</text>
<rect x="22" y="216" width="112" height="30" rx="8" fill="#2A141D" stroke="{R['border']}"/>
<text x="30" y="229" style="{MONO};font-size:9px" fill="#C9A2AD">bulletin</text>
<text x="30" y="240" style="{MONO};font-size:9.5px;font-weight:700" fill="#FFF1F3">November.pdf</text>
<rect x="60" y="258" width="36" height="4" rx="2" fill="#FFF1F3" opacity=".5"/>
</g>'''
card("redemption-church", "Redemption Church", 33, "REDEMPTIONCHURCHFAMILY.COM",
     ["Pentecostal church in Montgomery.", "Events, sermons and bulletins, with", "a Live Now badge on service days."],
     ["Montgomery, AL", "Live stream", "Sermons"], phone, **R)

# --- Capital City Church of God: a little chapel with service-time chips ---
C = dict(bg="#08191B", border="#174044", accent="#5EEAD4", text="#ECFEFF", muted="#9AC9C5", chip="#0E2A2C")
chapel = f'''<g transform="translate(430 34)">
<circle cx="92" cy="86" r="70" fill="#0E2A2C"/>
<path d="M92 24 L92 6 M84 12 H100" stroke="{C['accent']}" stroke-width="3.5" stroke-linecap="round"/>
<path d="M76 70 L92 30 L108 70 Z" fill="#5EEAD4"/>
<rect x="78" y="70" width="28" height="56" fill="#9AC9C5"/>
<path d="M44 126 L44 90 L22 108 L22 126 Z" fill="#9AC9C5" opacity=".55"/>
<path d="M140 126 L140 90 L162 108 L162 126 Z" fill="#9AC9C5" opacity=".55"/>
<rect x="44" y="92" width="34" height="34" fill="#9AC9C5" opacity=".8"/>
<rect x="106" y="92" width="34" height="34" fill="#9AC9C5" opacity=".8"/>
<path d="M44 92 L61 76 L78 92 Z M106 92 L123 76 L140 92 Z" fill="#5EEAD4" opacity=".9"/>
<path d="M86 126 V108 a6 6 0 0 1 12 0 V126 Z" fill="#08191B"/>
<rect x="54" y="102" width="8" height="12" rx="4" fill="#08191B"/><rect x="122" y="102" width="8" height="12" rx="4" fill="#08191B"/>
<rect x="16" y="126" width="152" height="4" rx="2" fill="#174044"/>
<rect x="8" y="166" width="82" height="26" rx="13" fill="#0E2A2C" stroke="{C['border']}" stroke-width="1.5"/>
<text x="49" y="183" text-anchor="middle" style="{MONO};font-size:11px;font-weight:700" fill="#5EEAD4">SUN 11:00</text>
<rect x="98" y="166" width="78" height="26" rx="13" fill="#0E2A2C" stroke="{C['border']}" stroke-width="1.5"/>
<text x="137" y="183" text-anchor="middle" style="{MONO};font-size:11px;font-weight:700" fill="#5EEAD4">WED 6:00</text>
<text x="92" y="218" text-anchor="middle" style="{MONO};font-size:10.5px;letter-spacing:1px" fill="#9AC9C5">SALEM · OREGON</text>
</g>'''
card("capital-city-church", "Capital City Church of God", 29, "CAPITALCITYCHURCHOFGOD.COM",
     ["Homepage redesign for a church in", "Salem, Oregon that puts visitors", "and service times first."],
     ["Salem, OR", "Redesign", "Service times"], chapel, **C)

# --- EHS Now: hard hat and a safety-program checklist ---
E = dict(bg="#121417", border="#2B313A", accent="#86EFAC", text="#F3F5F7", muted="#A3ACB8", chip="#1B2026")
hardhat = f'''<g transform="translate(436 30)">
<rect x="0" y="0" width="176" height="236" rx="18" fill="#1B2026" stroke="{E['border']}" stroke-width="2"/>
<path d="M58 78 a30 30 0 0 1 60 0 v10 H58 Z" fill="#FFC53D"/>
<rect x="82" y="44" width="12" height="18" rx="3" fill="#FFC53D"/>
<rect x="46" y="86" width="84" height="12" rx="6" fill="#F5B000"/>
<text x="88" y="122" text-anchor="middle" style="{MONO};font-size:10.5px;letter-spacing:1px" fill="{E['muted']}">SAFETY PROGRAM</text>
<g style="{MONO};font-size:11px" fill="{E['text']}">
<rect x="22" y="134" width="13" height="13" rx="3" fill="#86EFAC"/><path d="M25 140.5 l2.5 2.5 l5.5 -6" stroke="#121417" stroke-width="2" fill="none"/>
<text x="43" y="145">OSHA requirements</text>
<rect x="22" y="156" width="13" height="13" rx="3" fill="#86EFAC"/><path d="M25 162.5 l2.5 2.5 l5.5 -6" stroke="#121417" stroke-width="2" fill="none"/>
<text x="43" y="167">20+ templates</text>
<rect x="22" y="178" width="13" height="13" rx="3" fill="#86EFAC"/><path d="M25 184.5 l2.5 2.5 l5.5 -6" stroke="#121417" stroke-width="2" fill="none"/>
<text x="43" y="189">CSP consultation</text>
<rect x="22" y="200" width="13" height="13" rx="3" fill="none" stroke="#86EFAC" stroke-width="1.5"/>
<text x="43" y="211" fill="{E['muted']}">Gap analysis</text>
</g>
<rect x="22" y="222" width="132" height="4" rx="2" fill="{E['border']}"/><rect class="live" x="22" y="222" width="99" height="4" rx="2" fill="#86EFAC"/>
</g>'''
card("ehs-now", "EHS Now", 33, "EHSNOW.NET",
     ["Environmental health and safety", "consulting with a custom OSHA", "safety program builder."],
     ["Tri-Cities, WA", "OSHA", "Consulting"], hardhat, **E)

# --- Portfolio: a browser window with the site's hero ---
P = dict(bg="#0E1220", border="#2A3558", accent="#7FB2FF", text="#EEF2FF", muted="#9AA6C8", chip="#18203A")
browser = f'''<g transform="translate(428 40)">
<rect x="0" y="0" width="184" height="216" rx="12" fill="#161C33" stroke="{P['border']}" stroke-width="2"/>
<path d="M0 30 H184" stroke="{P['border']}" stroke-width="2"/>
<circle cx="16" cy="15" r="4" fill="#FF6B5E" opacity=".85"/><circle cx="30" cy="15" r="4" fill="#FEE123" opacity=".85"/><circle cx="44" cy="15" r="4" fill="#4CD07D" opacity=".85"/>
<rect x="58" y="8" width="112" height="14" rx="7" fill="#0E1220"/>
<text x="114" y="18.5" text-anchor="middle" style="{MONO};font-size:9px" fill="{P['muted']}">gavenrobertson.dev</text>
<text x="18" y="66" style="{SANS};font-weight:800;font-size:17px;letter-spacing:-.4px" fill="{P['text']}">Gaven Robertson</text>
<text x="18" y="84" style="{MONO};font-size:9.5px" fill="{P['accent']}">software engineer</text>
<rect x="18" y="98" width="130" height="5" rx="2.5" fill="{P['muted']}" opacity=".45"/>
<rect x="18" y="109" width="104" height="5" rx="2.5" fill="{P['muted']}" opacity=".3"/>
<rect x="18" y="126" width="62" height="18" rx="9" fill="{P['accent']}"/>
<text x="49" y="138.5" text-anchor="middle" style="{MONO};font-size:9px;font-weight:700" fill="#0E1220">projects</text>
<rect x="18" y="160" width="44" height="38" rx="6" fill="#0E1220" stroke="{P['border']}"/>
<rect x="70" y="160" width="44" height="38" rx="6" fill="#0E1220" stroke="{P['border']}"/>
<rect x="122" y="160" width="44" height="38" rx="6" fill="#0E1220" stroke="{P['border']}"/>
<rect x="26" y="168" width="20" height="4" rx="2" fill="{P['accent']}" opacity=".9"/><rect x="26" y="178" width="28" height="4" rx="2" fill="{P['muted']}" opacity=".4"/>
<rect x="78" y="168" width="20" height="4" rx="2" fill="#F9A8D4" opacity=".9"/><rect x="78" y="178" width="28" height="4" rx="2" fill="{P['muted']}" opacity=".4"/>
<rect x="130" y="168" width="20" height="4" rx="2" fill="#A5F3FC" opacity=".9"/><rect x="130" y="178" width="28" height="4" rx="2" fill="{P['muted']}" opacity=".4"/>
</g>'''
card("portfolio", "Gaven Robertson", 33, "GAVENROBERTSON.DEV",
     ["My portfolio: who I am, what", "I've built, and how to get", "in touch."],
     ["React", "three.js", "Blender"], browser, **P)
