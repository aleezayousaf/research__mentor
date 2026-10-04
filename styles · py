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
h1, h2, h3 { font-family: Georgia, 'Times New Roman', serif; color: #0B1F3A; }
hr { border: 0; height: 3px; background: linear-gradient(90deg, transparent, #C9A227, transparent); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #EEF2F8 0%, #E3EAF4 100%);
  border-right: 4px solid #C9A227;
  box-shadow: 6px 0 18px rgba(11,31,58,.12);
}
.brand {
  display: flex; align-items: center; gap: 12px; padding: 14px 16px; margin-bottom: 14px;
  border-radius: 18px; color: #fff;
  background: linear-gradient(135deg, #0B1F3A, #16335C);
  border: 1.5px solid rgba(243,214,117,.65);
  box-shadow: 0 5px 0 #06142A, 0 12px 20px rgba(11,31,58,.30), inset 0 1px 0 rgba(255,255,255,.2);
}
.brand-icon {
  width: 46px; height: 46px; border-radius: 14px; display: flex; align-items: center; justify-content: center;
  font-size: 26px; background: linear-gradient(145deg, #FFF0B8, #D9A93A);
  box-shadow: 0 4px 0 #8A6410, inset 0 2px 3px rgba(255,255,255,.7);
}
.brand-name { font-family: Georgia, serif; font-weight: 700; font-size: 1.15rem; line-height: 1.1; color: #fff; }
.brand-tag { font-size: .72rem; letter-spacing: .12em; color: #F3D675; }

/* ---------- Hero banner ---------- */
.hero {
  display: flex; align-items: center; justify-content: space-between; gap: 24px;
  padding: 28px 34px; margin-bottom: 22px; border-radius: 24px; color: #fff;
  background:
    radial-gradient(620px 230px at 86% 0%, rgba(243,214,117,.30), transparent 62%),
    linear-gradient(135deg, #0B1F3A 0%, #16335C 55%, #7A1F2B 135%);
  border: 2px solid rgba(243,214,117,.55);
  box-shadow: 0 10px 0 #06142A, 0 26px 42px rgba(11,31,58,.35), inset 0 2px 0 rgba(255,255,255,.18);
}
.hero-kicker { letter-spacing: .22em; font-size: .75rem; color: #F3D675; font-weight: 700; }
.hero-title {
  font-family: Georgia, 'Times New Roman', serif; font-size: 2.7rem; font-weight: 700; line-height: 1.1;
  margin: .3rem 0 .5rem; color: #fff;
  text-shadow: 0 2px 0 #06142A, 0 6px 14px rgba(0,0,0,.45);
}
.hero-sub { color: #E6ECF5; font-size: 1.05rem; max-width: 650px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }
.chip {
  padding: 6px 13px; border-radius: 999px; font-size: .82rem; font-weight: 700; color: #0B1F3A;
  background: linear-gradient(180deg, #FFF3C4, #E6C04F);
  box-shadow: 0 3px 0 #8A6410, 0 6px 10px rgba(0,0,0,.25);
}
.hero-art { flex: 0 0 auto; animation: floaty 5s ease-in-out infinite; }
@keyframes floaty {
  0%, 100% { transform: translateY(0) rotate(-1.5deg); }
  50% { transform: translateY(-8px) rotate(1.5deg); }
}
@media (max-width: 760px) {
  .hero { flex-direction: column; text-align: center; padding: 22px 18px; }
  .hero-title { font-size: 2rem; }
  .hero-art svg { width: 120px; height: 120px; }
  .chips { justify-content: center; }
}

/* ---------- 3D icon tiles + section headers ---------- */
.sec-head { display: flex; align-items: center; gap: 16px; margin: 2px 0 14px; }
.icon3d {
  width: 66px; height: 66px; flex: 0 0 66px; border-radius: 19px; font-size: 34px;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(145deg, var(--c1), var(--c2));
  box-shadow:
    0 7px 0 rgba(0,0,0,.28), 0 14px 22px rgba(11,31,58,.28),
    inset 0 2px 3px rgba(255,255,255,.6), inset 0 -5px 7px rgba(0,0,0,.20);
  transform: perspective(320px) rotateX(10deg) rotateY(-10deg);
  transition: transform .25s ease;
}
.icon3d:hover { transform: perspective(320px) rotateX(0deg) rotateY(0deg) translateY(-3px); }
.icon3d span { filter: drop-shadow(0 3px 2px rgba(0,0,0,.35)); }
.sec-title { font-family: Georgia, 'Times New Roman', serif; font-size: 1.7rem; font-weight: 700; color: #0B1F3A; line-height: 1.15; }
.sec-sub { color: #4A5A70; font-size: .98rem; margin-top: 2px; }
.result-label {
  display: inline-block; margin: 12px 0 6px; padding: 5px 14px; border-radius: 999px; font-weight: 700;
  font-size: .85rem; color: #fff; background: linear-gradient(180deg, #16335C, #0B1F3A);
  box-shadow: 0 3px 0 #06142A, 0 6px 10px rgba(11,31,58,.25);
}

/* ---------- Tabs (each stage has its own colour) ---------- */
div[data-baseweb="tab-list"] { gap: 10px; flex-wrap: wrap; border-bottom: none !important; padding: 6px 4px 18px; }
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none !important; }
div[data-baseweb="tab-list"] button[role="tab"] {
  height: auto; padding: 10px 16px; background: #fff; border: 2px solid var(--c1, #C9A227); border-radius: 14px;
  box-shadow: 0 4px 0 var(--c2, #8A6410), 0 9px 14px rgba(11,31,58,.15);
  transition: transform .12s ease, box-shadow .12s ease;
}
div[data-baseweb="tab-list"] button[role="tab"] p { color: var(--c2, #0B1F3A) !important; font-weight: 700; margin: 0; }
div[data-baseweb="tab-list"] button[role="tab"]:hover { transform: translateY(-2px); }
div[data-baseweb="tab-list"] button[role="tab"][aria-selected="true"] {
  background: linear-gradient(180deg, var(--c1), var(--c2)); transform: translateY(3px);
  box-shadow: 0 1px 0 var(--c2), inset 0 3px 6px rgba(0,0,0,.28);
}
div[data-baseweb="tab-list"] button[role="tab"][aria-selected="true"] p { color: #fff !important; }

/* ---------- Pressable 3D buttons ---------- */
.stButton > button {
  border: 0; border-radius: 13px; padding: .62rem 1.3rem;
  background: linear-gradient(180deg, #A02F3F 0%, #6E1B27 100%);
  box-shadow: 0 5px 0 #4A101A, 0 11px 18px rgba(11,31,58,.28), inset 0 1px 0 rgba(255,255,255,.35);
  transition: transform .12s ease, box-shadow .12s ease;
}
.stButton > button p, .stButton > button span { color: #fff !important; font-weight: 700; margin: 0; }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 7px 0 #4A101A, 0 15px 22px rgba(11,31,58,.30), inset 0 1px 0 rgba(255,255,255,.35); }
.stButton > button:active { transform: translateY(4px); box-shadow: 0 1px 0 #4A101A, 0 3px 6px rgba(11,31,58,.25), inset 0 2px 4px rgba(0,0,0,.3); }
[data-testid="stSidebar"] .stButton > button {
  background: linear-gradient(180deg, #1F4378 0%, #0B1F3A 100%);
  box-shadow: 0 5px 0 #06142A, 0 11px 18px rgba(11,31,58,.28), inset 0 1px 0 rgba(255,255,255,.3);
}
[data-testid="stBaseLinkButton-secondary"], [data-testid="stBaseLinkButton-primary"] {
  border: 0 !important; border-radius: 13px !important;
  background: linear-gradient(180deg, #FFF0B8 0%, #E0B13E 100%) !important;
  box-shadow: 0 5px 0 #8A6410, 0 11px 18px rgba(11,31,58,.25), inset 0 1px 0 rgba(255,255,255,.7) !important;
}
[data-testid="stBaseLinkButton-secondary"] p, [data-testid="stBaseLinkButton-primary"] p { color: #0B1F3A !important; font-weight: 700; }

/* ---------- Inputs look pressed-in ---------- */
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
  border-radius: 12px !important; background: #fff !important; border: 1.5px solid #D9C98F !important;
  box-shadow: inset 0 2px 6px rgba(11,31,58,.14) !important;
}
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within, [data-baseweb="select"] > div:focus-within {
  border-color: #7A1F2B !important;
  box-shadow: inset 0 2px 6px rgba(11,31,58,.14), 0 0 0 3px rgba(122,31,43,.18) !important;
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
