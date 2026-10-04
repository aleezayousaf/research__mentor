"""Look and feel of ResearchMentor AI.

Change colours here and the whole app updates. Each stage has two colours:
a lighter one and a darker one (they make the 3D gradient).
"""

# ---- Main legal palette (navy, burgundy, gold, ivory) ----
NAVY = "#0B1F3A"
NAVY_2 = "#16335C"
BURGUNDY = "#7A1F2B"
GOLD = "#C9A227"
GOLD_LIGHT = "#F3D675"

# ---- One colour pair + icon per tab: (key, icon, light, dark, tab label, title, subtitle) ----
STAGES = [
    ("guidance", "💡", "#E8B12A", "#A87100", "💡 Guidance & Q&A Hub",
     "Guidance & Q&A Hub", "Ask any research question and choose how you want to learn."),
    ("p1", "🔭", "#2AA6B8", "#136579", "🔭 1. Observation & Topic",
     "Stage 1 · Observation & Topic", "Turn something you noticed in the real world into a research topic."),
    ("p2", "🧭", "#8A78D0", "#4B3B93", "🧭 2. Methodology & Gap",
     "Stage 2 · Methodology & Gap", "Choose a method and learn what belongs in each paragraph."),
    ("p3", "📚", "#2FA37B", "#146B4D", "📚 3. Sources",
     "Stage 3 · Sources", "Find scholarship and official sources, Pakistan first."),
    ("p4", "✍️", "#D0536A", "#7E1F2E", "✍️ 4. Argument Writing",
     "Stage 4 · Argument & Writing", "IRAC for law; claim, evidence and analysis for politics and IR."),
    ("p5", "🔖", "#EE9347", "#A9501A", "🔖 5. Citation Check",
     "Stage 5 · Citation Check", "OSCOLA, Bluebook, APA, Chicago or Harvard."),
    ("p6", "🎓", "#4A8BE0", "#1B4A94", "🎓 6. Publishing Match",
     "Stage 6 · Publishing Match", "Check anonymisation and find journals that fit your work."),
]
_BY_KEY = {s[0]: s for s in STAGES}
TAB_LABELS = [s[4] for s in STAGES]


def _flat(html: str) -> str:
    """Remove line breaks and indentation so Streamlit never treats the HTML as code."""
    return "".join(line.strip() for line in html.strip().splitlines())


def _tab_colour_css() -> str:
    rules = []
    for i, s in enumerate(STAGES, start=1):
        rules.append(
            f'div[data-baseweb="tab-list"] button[role="tab"]:nth-of-type({i})'
            f"{{--c1:{s[2]};--c2:{s[3]};}}"
        )
    return "\n".join(rules)


_BASE_CSS = """
.stApp {
  background:
    radial-gradient(1100px 480px at 88% -8%, #F6EBCB 0%, rgba(246,235,203,0) 62%),
    linear-gradient(180deg, #FBF7EE 0%, #F3ECDC 100%);
}
.block-container { padding-top: 1.4rem; max-width: 1200px; }
h1, h2, h3 { font-family: Georgia, 'Times New Roman', serif; color: #0B1F3A !important; }
hr { border: 0; height: 3px; background: linear-gradient(90deg, transparent, #C9A227, transparent); }

/* ---------- Fix Widget Labels & Radio Buttons ---------- */
div[data-testid="stWidgetLabel"] label,
div[data-testid="stWidgetLabel"] p,
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] p,
.stMarkdown p,
p, span {
  color: #0B1F3A !important;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #EEF2F8 0%, #E3EAF4 100%);
  border-right: 4px solid #C9A227;
  box-shadow: 6px 0 18px rgba(11,31,58,.12);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: #0B1F3A !important;
}

.brand {
  display: flex; align-items: center; gap: 12px; padding: 14px 16px; margin-bottom: 14px;
  border-radius: 18px; color: #fff !important;
  background: linear-gradient(135deg, #0B1F3A, #16335C);
  border: 1.5px solid rgba(243,214,117,.65);
  box-shadow: 0 5px 0 #06142A, 0 12px 20px rgba(11,31,58,.30), inset 0 1px 0 rgba(255,255,255,.2);
}
.brand p, .brand span, .brand-name, .brand-tag {
  color: #fff !important;
}

/* ---------- Inputs look pressed-in ---------- */
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
  border-radius: 12px !important; background: #fff !important; border: 1.5px solid #D9C98F !important;
  box-shadow: inset 0 2px 6px rgba(11,31,58,.14) !important;
  color: #0B1F3A !important;
}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
  color: #0B1F3A !important;
}
"""

def inject_css() -> str:
    """Returns the <style> block. Show it with st.markdown(..., unsafe_allow_html=True)."""
    css = " ".join(f"{_BASE_CSS} {_tab_colour_css()}".split())
    return f"<style>{css}</style>"


def _scales_svg() -> str:
    return _flat("""
    <svg viewBox="0 0 200 200" width="170" height="170" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Scales of justice">
    <defs>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FFEDA8"/><stop offset=".5" stop-color="#DAA93A"/><stop offset="1" stop-color="#8A6410"/>
    </linearGradient>
    <filter id="sh" x="-25%" y="-25%" width="150%" height="150%">
    <feDropShadow dx="0" dy="7" stdDeviation="5" flood-color="#000" flood-opacity=".45"/>
    </filter>
    </defs>
    <g filter="url(#sh)">
    <rect x="96" y="28" width="8" height="132" rx="4" fill="url(#gold)"/>
    <circle cx="100" cy="28" r="10" fill="url(#gold)"/>
    <rect x="28" y="44" width="144" height="8" rx="4" fill="url(#gold)"/>
    <path d="M40 50 L14 112 M40 50 L66 112 M160 50 L134 112 M160 50 L186 112" stroke="#F3D675" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <path d="M10 112 Q40 144 70 112 Z" fill="url(#gold)"/>
    <path d="M130 112 Q160 144 190 112 Z" fill="url(#gold)"/>
    <rect x="70" y="158" width="60" height="11" rx="5" fill="url(#gold)"/>
    <rect x="58" y="168" width="84" height="14" rx="6" fill="url(#gold)"/>
    </g>
    </svg>
    """)


def hero_html() -> str:
    chips = ["⚖️ Law", "🏛️ Socio-Legal Studies", "🗳️ Political Science",
             "🌍 International Relations", "📜 Public Policy"]
    chip_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    return _flat(f"""
    <div class="hero">
    <div>
    <div class="hero-kicker">PAKISTAN FIRST · WORLD READY</div>
    <div class="hero-title">ResearchMentor AI</div>
    <div class="hero-sub">Your step-by-step mentor from first idea to published paper. It coaches you; it never writes your assignment for you.</div>
    <div class="chips">{chip_html}</div>
    </div>
    <div class="hero-art">{_scales_svg()}</div>
    </div>
    """)


def sidebar_brand() -> str:
    return _flat("""
    <div class="brand">
    <div class="brand-icon">⚖️</div>
    <div><div class="brand-name">ResearchMentor</div><div class="brand-tag">LAW · POLITICS · IR</div></div>
    </div>
    """)


def section_header(key: str) -> str:
    _, icon, c1, c2, _, title, subtitle = _BY_KEY[key]
    return _flat(f"""
    <div class="sec-head">
    <div class="icon3d" style="--c1:{c1};--c2:{c2};"><span>{icon}</span></div>
    <div><div class="sec-title">{title}</div><div class="sec-sub">{subtitle}</div></div>
    </div>
    """)
