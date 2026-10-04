import sys
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Startup check: make sure every project file is in the right folder.
# ---------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

REQUIRED_FILES = [
    "config.py",
    "styles.py",
    "tools/__init__.py",
    "tools/research_tools.py",
    "agents/__init__.py",
    "agents/guidance_hub.py",
    "agents/socratic_supervisor.py",
    "agents/methodology_advisor.py",
    "agents/legal_researcher.py",
    "agents/writing_coach.py",
    "agents/citation_integrator.py",
    "agents/journal_publisher.py",
]


def _find_missing_files():
    problems = []
    for name in REQUIRED_FILES:
        if (APP_DIR / name).exists():
            continue
        hint = ""
        if (APP_DIR / Path(name).name).exists():
            hint = f"  (found '{Path(name).name}' at the top level; it must be inside the '{Path(name).parent}' folder)"
        problems.append(f"{name}{hint}")
    return problems


_missing = _find_missing_files()
if _missing:
    st.set_page_config(page_title="ResearchMentor AI: setup problem", page_icon="⚠️")
    st.title("⚠️ Some project files are missing")
    st.error(
        "The app cannot start because these files are not where it expects them. "
        "This usually means a folder was not uploaded to GitHub."
    )
    st.code("\n".join(_missing))
    st.markdown(
        "**How to fix it:** open your GitHub repository and check that the main page shows "
        "the folders `agents` and `tools`, and that each folder contains the `.py` files listed above."
    )
    st.stop()

from config import (
    DEFAULT_PROVIDER,
    PROVIDERS,
    get_llm,
    setup_environment,
    test_api_key,
)
from crewai import Crew, Task
from styles import TAB_LABELS, hero_html, inject_css, section_header, sidebar_brand

# Import All Agents
from agents.guidance_hub import get_guidance_assistant_agent
from agents.socratic_supervisor import get_socratic_supervisor_agent
from agents.methodology_advisor import get_methodology_advisor_agent
from agents.legal_researcher import get_legal_researcher_agent
from agents.writing_coach import get_writing_coach_agent
from agents.citation_integrator import get_citation_integrator_agent
from agents.journal_publisher import get_journal_publisher_agent

st.set_page_config(page_title="ResearchMentor AI", page_icon="⚖️", layout="wide")
st.markdown(inject_css(), unsafe_allow_html=True)

DISCIPLINES = [
    "Law (LL.B)",
    "Socio-Legal Studies",
    "Political Science",
    "International Relations",
    "Public Policy",
]
LAW_LIKE = ("Law (LL.B)", "Socio-Legal Studies")


def discipline_brief():
    """Tells every agent which subject the student studies so advice fits their field."""
    profile = st.session_state.get("student_profile", {})
    field = profile.get("discipline", DISCIPLINES[0])
    if field in LAW_LIKE:
        note = (
            "Use legal reasoning (IRAC/CREAC), primary legal authority, and OSCOLA or Bluebook "
            "where relevant. For socio-legal work also bring in empirical and social context."
        )
    else:
        note = (
            "This student is NOT a law student. Use the vocabulary, theories and methods of "
            f"{field} (for example realism, liberalism, constructivism, institutionalism, "
            "rational choice or policy-cycle models where they fit). Use evidence-based argument "
            "(claim, evidence, analysis) instead of IRAC, and APA, Chicago or Harvard style instead "
            "of OSCOLA. Mention law only where it matters (constitutions, treaties, statutes)."
        )
    return (
        f"STUDENT CONTEXT: The student studies {field}. {note} "
        "Focus first on Pakistan, then widen to regional and global examples. "
        "Coach the student; do not write their assignment for them."
    )


def run_crew(agent, task):
    """Run one agent on one task, with a progress message and friendly errors."""
    try:
        task.description = f"{discipline_brief()}\n\n{task.description}"
    except Exception:
        pass
    try:
        with st.spinner("The agent is working. This can take a minute..."):
            crew = Crew(agents=[agent], tasks=[task], verbose=True)
            result = crew.kickoff()
        st.markdown('<div class="result-label">📜 Mentor\'s response</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(result.raw)
        return result.raw
    except Exception as error:
        text = str(error).lower()
        if "429" in text or "rate limit" in text or "resource_exhausted" in text or "quota" in text:
            st.warning(
                "You have reached this provider's free limit for now. Wait a minute, "
                "or pick a different provider or model in the sidebar and run again."
            )
        elif "401" in text or "unauthenticated" in text or "invalid api key" in text:
            st.error(
                "The provider rejected your API key. Use the sidebar link to create a fresh key, "
                "paste only the key, and press 'Test my API key'."
            )
        else:
            st.error(f"The workflow could not be completed: {error}")
        return None


# 1. Session State & Student Profile Management
if "student_profile" not in st.session_state:
    st.session_state["student_profile"] = {
        "name": "",
        "discipline": "Law (LL.B)",
        "observation": "",
        "sub_domain": "",
        "research_topic": "",
        "selected_methodology": "Doctrinal Research"
    }

if "stage1_step" not in st.session_state:
    st.session_state["stage1_step"] = 1

# Sidebar Profile Settings
with st.sidebar:
    st.markdown(sidebar_brand(), unsafe_allow_html=True)
    st.subheader("👤 Student Profile")
    st.session_state["student_profile"]["name"] = st.text_input(
        "Your Name", value=st.session_state["student_profile"]["name"], placeholder="e.g. Ayesha"
    )
    st.session_state["student_profile"]["discipline"] = st.selectbox(
        "Discipline", DISCIPLINES, help="Every agent adapts its advice to your subject."
    )
    st.session_state["student_profile"]["research_topic"] = st.text_input(
        "Working Topic", value=st.session_state["student_profile"]["research_topic"], placeholder="Set in Stage 1"
    )
    
    st.divider()
    st.subheader("🤖 AI Provider")
    provider = st.selectbox(
        "Choose a free AI provider",
        list(PROVIDERS),
        index=list(PROVIDERS).index(DEFAULT_PROVIDER),
        help="If one provider hits its free limit, switch to another here.",
    )
    provider_info = PROVIDERS[provider]
    model_label = st.selectbox("Model", list(provider_info["models"]))
    model_id = provider_info["models"][model_label]

    st.link_button(
        f"🔑 Get a free {provider_info['short']} API key",
        provider_info["key_url"],
        use_container_width=True,
    )
    st.caption(f"Sign-up page: {provider_info['key_url']}")
    st.caption(provider_info["note"])

    api_key_input = st.text_input(
        f"{provider_info['short']} API key (paste here)",
        type="password",
        key=f"api_key_{provider}",
        help=f"Or set {provider_info['env']} in your environment or Streamlit secrets.",
    )
    if st.button("Test my API key", use_container_width=True):
        key_ok, key_message = test_api_key(provider, model_id, api_key_input)
        (st.success if key_ok else st.error)(key_message)

    # Initialize API Config
    is_configured = setup_environment(provider, api_key_input)
    llm = None
    if is_configured:
        try:
            llm = get_llm(provider, model_id)
            st.success("System Configured")
        except Exception as error:
            is_configured = False
            st.error(f"Could not set up the AI model: {error}")
    else:
        st.warning(f"Please paste a {provider_info['short']} API key to run agents.")

st.markdown(hero_html(), unsafe_allow_html=True)

discipline = st.session_state["student_profile"]["discipline"]
is_law_like = discipline in LAW_LIKE

TOPIC_EXAMPLES = {
    "Law (LL.B)": "Constitutional Writs, Environmental Statutory Enforcement, or Public Trust Doctrine",
    "Socio-Legal Studies": "Access to Justice, Legal Pluralism, or Law and Gender in Practice",
    "Political Science": "Federalism and the 18th Amendment, Electoral Politics, or Civil-Military Relations",
    "International Relations": "Pakistan's Foreign Policy, Regional Security in South Asia, or Water Diplomacy and Treaties",
    "Public Policy": "Policy Implementation Gaps, Urban Governance, or Public Health Policy",
}

METHODS = {
    "law": [
        "Doctrinal Legal Research (Statutes & Case Law)",
        "Socio-Legal / Empirical Research (Surveys & Field Data)",
        "Comparative Legal Research (Cross-Jurisdictional Analysis)",
    ],
    "Political Science": [
        "Qualitative Case Study",
        "Comparative Politics (Cross-Country or Cross-Case)",
        "Quantitative Analysis (Survey or Dataset)",
        "Historical Analysis / Process Tracing",
        "Discourse & Content Analysis",
    ],
    "International Relations": [
        "Qualitative Case Study",
        "Comparative Analysis (Cross-Country)",
        "Foreign Policy Analysis",
        "Process Tracing / Historical Analysis",
        "Discourse & Content Analysis",
        "Quantitative Analysis (Datasets)",
    ],
    "Public Policy": [
        "Policy Analysis (Problem, Options, Evaluation)",
        "Case Study of Policy Implementation",
        "Comparative Policy Analysis",
        "Survey / Field Research",
        "Quantitative Evaluation (Datasets)",
    ],
}

# 2. Main Navigation Tabs (Free navigation enabled)
tab_guidance, tab_p1, tab_p2, tab_p3, tab_p4, tab_p5, tab_p6 = st.tabs(TAB_LABELS)

# -----------------------------------------------------------------------------
# TAB 0: Interactive Guidance & Q&A Hub
# -----------------------------------------------------------------------------
with tab_guidance:
    st.markdown(section_header("guidance"), unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        user_query = st.text_area("What research question or concept do you need help with?", 
                                 placeholder="e.g., How do I structure a legal literature review?")
    with col2:
        resource_mode = st.radio(
            "Resource Preference:",
            ["Supervisor Recommended Guides (Stanford, OSCOLA, APA/Chicago)", "Search Live Web Resources"],
            help="Choose between curated institutional guides or live web search."
        )
    
    if st.button("Get Guidance", key="btn_guidance"):
        if not is_configured:
            st.error("API key missing.")
        else:
            assistant = get_guidance_assistant_agent(llm)
            task = Task(
                description=(
                    f"Student Profile: {st.session_state['student_profile']}\n"
                    f"Student Query: {user_query}\n"
                    f"Resource Mode: {resource_mode}\n"
                    "Provide clear, step-by-step advice. If the student selected 'Supervisor Recommended Guides', "
                    "reference institutional hubs like Stanford Legal Writing Guides or Oxford OSCOLA. "
                    "If they selected 'Search Live Web Resources', outline ideal search queries and open-access sources."
                ),
                expected_output="Step-by-step guidance tailored to the student's question.",
                agent=assistant
            )
            run_crew(assistant, task)

# -----------------------------------------------------------------------------
# TAB 1: Step-by-Step Observation & Topic Discovery
# -----------------------------------------------------------------------------
with tab_p1:
    st.markdown(section_header("p1"), unsafe_allow_html=True)
    
    # Visual Step Tracker
    st.progress(
        33 if st.session_state["stage1_step"] == 1 else (66 if st.session_state["stage1_step"] == 2 else 100),
        text=f"Stage 1 - Step {st.session_state['stage1_step']} of 3"
    )

    # STEP 1: Observation Input
    if st.session_state["stage1_step"] == 1:
        st.subheader("Step 1: Share Your Observation")
        obs_input = st.text_area(
            "What real-world problem or situation did you notice?",
            value=st.session_state["student_profile"]["observation"],
            placeholder="e.g., Seasonal smog in Lahore causes school closures, but existing environmental regulations are rarely enforced."
        )
        
        if st.button("Submit Observation & Explore Domains", key="btn_step1"):
            if not is_configured:
                st.error("API key missing.")
            elif not obs_input.strip():
                st.warning("Please enter an observation.")
            else:
                st.session_state["student_profile"]["observation"] = obs_input
                supervisor = get_socratic_supervisor_agent(llm)
                task = Task(
                    description=(
                        f"Student Name: {st.session_state['student_profile']['name']}\n"
                        f"Student Observation: {obs_input}\n"
                        "Acknowledge the student's real-world observation. Suggest 3 specific sub-domains "
                        f"they could explore (for example: {TOPIC_EXAMPLES.get(discipline, TOPIC_EXAMPLES['Law (LL.B)'])}). "
                        "Ask 2 encouraging questions to help them choose or refine their focus area."
                    ),
                    expected_output="3 sub-domain suggestions and 2 guiding questions.",
                    agent=supervisor
                )
                output = run_crew(supervisor, task)
                if output:
                    st.session_state["stage1_subdomains"] = output
                    st.session_state["stage1_step"] = 2
                    st.rerun()

    # STEP 2: Choose Sub-Domain & Narrow Focus (Students can choose supervisor suggestions OR write their own)
    elif st.session_state["stage1_step"] == 2:
        st.subheader("Step 2: Choose or Define Your Sub-Domain Focus")
        if "stage1_subdomains" in st.session_state:
            st.info(st.session_state["stage1_subdomains"])
        
        st.markdown("**Select from supervisor suggestions or independently type your preferred focus:**")
        sub_domain_input = st.text_input(
            "Your chosen sub-domain / angle:",
            value=st.session_state["student_profile"]["sub_domain"],
            placeholder="e.g., Type one of the supervisor's 3 suggestions or write your own custom focus area"
        )
        
        col_b1, col_n1 = st.columns([1, 4])
        with col_b1:
            if st.button("← Back to Step 1"):
                st.session_state["stage1_step"] = 1
                st.rerun()
        with col_n1:
            if st.button("Proceed to Formulate Research Question"):
                if not sub_domain_input.strip():
                    st.warning("Please enter or select a sub-domain focus.")
                else:
                    st.session_state["student_profile"]["sub_domain"] = sub_domain_input
                    st.session_state["stage1_step"] = 3
                    st.rerun()

    # STEP 3: Draft and Refine Research Question
    elif st.session_state["stage1_step"] == 3:
        st.subheader("Step 3: Formulate Your Research Question")
        st.caption(f"**Original Observation:** {st.session_state['student_profile']['observation']}")
        st.caption(f"**Selected Focus Area:** {st.session_state['student_profile']['sub_domain']}")
        
        proposed_rq = st.text_area(
            "Write your research question here:",
            value=st.session_state["student_profile"]["research_topic"],
            placeholder="e.g., To what extent can Article 9 be invoked under Article 199 to compel statutory enforcement of air pollution limits in Punjab?"
        )
        
        col_b2, col_sub = st.columns([1, 4])
        with col_b2:
            if st.button("← Back to Step 2"):
                st.session_state["stage1_step"] = 2
                st.rerun()
        with col_sub:
            if st.button("Get Supervisor Feedback & Save Topic", type="primary"):
                if not is_configured:
                    st.error("API key missing.")
                elif not proposed_rq.strip():
                    st.warning("Please type a research question.")
                else:
                    st.session_state["student_profile"]["research_topic"] = proposed_rq
                    supervisor = get_socratic_supervisor_agent(llm)
                    task = Task(
                        description=(
                            f"Proposed Research Question: {proposed_rq}\n"
                            f"Observation Context: {st.session_state['student_profile']['observation']}\n"
                            f"Focus Area: {st.session_state['student_profile']['sub_domain']}\n"
                            "Provide feedback on whether this research question is specific, manageable, and actionable. "
                            "Give 2 specific recommendations to polish it further."
                        ),
                        expected_output="Constructive evaluation of the research question with actionable improvement suggestions.",
                        agent=supervisor
                    )
                    run_crew(supervisor, task)
                    st.success("✅ Topic saved to your Student Profile! You can now navigate freely to Stage 2 (Methodology) or any other tab.")

# -----------------------------------------------------------------------------
# TAB 2: Methodology & Research Gap
# -----------------------------------------------------------------------------
with tab_p2:
    st.markdown(section_header("p2"), unsafe_allow_html=True)
    
    method_choice = st.selectbox(
        "Select Research Methodology:",
        METHODS["law"] if is_law_like else METHODS.get(discipline, METHODS["Political Science"]),
        key=f"method_{discipline}",
    )
    
    research_question = st.text_input(
        "Enter your research question (auto-filled from Stage 1):",
        value=st.session_state["student_profile"]["research_topic"]
    )
    
    if st.button("Generate Paragraph-by-Paragraph Methodology Guide", key="btn_p2"):
        if not is_configured:
            st.error("API key missing.")
        elif not research_question.strip():
            st.warning("Please enter a research question or set it in Stage 1.")
        else:
            advisor = get_methodology_advisor_agent(llm)
            task = Task(
                description=(
                    f"Research Question: {research_question}\n"
                    f"Selected Methodology: {method_choice}\n"
                    "Provide a paragraph-by-paragraph breakdown for writing the methodology section:\n"
                    "- Paragraph 1: Method selection and justification.\n"
                    "- Paragraph 2: Primary and secondary sources to analyze.\n"
                    "- Paragraph 3: Analytical framework and limitations.\n"
                    "Include a section on 'What to Avoid' (e.g., confusing tools with methodology or writing a purely descriptive summary)."
                ),
                expected_output="Detailed paragraph-by-paragraph writing instructions and pitfall warnings.",
                agent=advisor
            )
            run_crew(advisor, task)

# -----------------------------------------------------------------------------
# TAB 3: Legal Sources & Retrieval
# -----------------------------------------------------------------------------
with tab_p3:
    st.markdown(section_header("p3"), unsafe_allow_html=True)
    search_query = st.text_input("Enter key terms, provisions, treaties or policy topics to search:", placeholder="e.g., Right to Life Article 9 / Indus Waters Treaty / 18th Amendment")
    
    if st.button("Search Scholarship & Official Sources", key="btn_p3"):
        if not is_configured:
            st.error("API key missing.")
        else:
            researcher = get_legal_researcher_agent(llm)
            if is_law_like:
                sources_task = (
                    f"Find legal papers and statutory provisions related to: {search_query}\n"
                    "1. Call 'Search Pakistan-Affiliated Scholarship (OpenAlex)' first.\n"
                    "2. Call 'Search Global Scholarly Literature (OpenAlex RAG)' for worldwide scholarship.\n"
                    "3. Call 'Pakistan Code Official-Source Verification Guide' for Pakistani primary law, "
                    "and tell the student to confirm statutes on the official portals.\n"
                    "Never invent a statute, case or article; mark anything unverified."
                )
            else:
                sources_task = (
                    f"Find scholarship and official sources related to: {search_query}\n"
                    "1. Call 'Search Pakistan-Affiliated Scholarship (OpenAlex)' first.\n"
                    "2. Call 'Search Global Scholarly Literature (OpenAlex RAG)' for worldwide scholarship.\n"
                    "3. Call 'Political Science & International Relations Source Guide' for official documents, "
                    "treaties and datasets, and tell the student to open and verify them.\n"
                    "4. Use 'Pakistan Code Official-Source Verification Guide' only if constitutional or statutory "
                    "provisions are relevant.\n"
                    "Never invent a source; mark anything unverified."
                )
            task = Task(
                description=sources_task,
                expected_output="Summarized primary and secondary sources with reference links.",
                agent=researcher
            )
            run_crew(researcher, task)

# -----------------------------------------------------------------------------
# TAB 4: IRAC Writing & Review
# -----------------------------------------------------------------------------
with tab_p4:
    st.markdown(section_header("p4"), unsafe_allow_html=True)
    student_draft = st.text_area("Paste a paragraph or section of your draft here:", height=150)
    
    if st.button("Review Argument & Writing", key="btn_p4"):
        if not is_configured:
            st.error("API key missing.")
        else:
            coach = get_writing_coach_agent(llm)
            if is_law_like:
                review_matrix = (
                    "1. Validation: Praise accurate factual claims (noting issue statements do not need citations).\n"
                    "2. Rule Analysis: Identify missing statutory provisions or precedents.\n"
                    "3. Side-by-Side Example: Show a concrete 'Before vs. After' table showing how to integrate proper authority."
                )
            else:
                review_matrix = (
                    "1. Validation: Praise accurate claims and well-supported points.\n"
                    "2. Evidence & Theory Analysis: Identify claims that need evidence (data, scholarship, "
                    "official documents) or a clearer theoretical framework.\n"
                    "3. Side-by-Side Example: Show a concrete 'Before vs. After' table showing how to support "
                    "a claim with evidence and a citation."
                )
            task = Task(
                description=(
                    f"Student Draft: {student_draft}\n"
                    "Perform a structural review using the 3-part matrix:\n"
                    f"{review_matrix}"
                ),
                expected_output="A 3-part pedagogical review containing a side-by-side 'Before vs. After' transformation table.",
                agent=coach
            )
            run_crew(coach, task)

# -----------------------------------------------------------------------------
# TAB 5: Citation Integrity
# -----------------------------------------------------------------------------
with tab_p5:
    st.markdown(section_header("p5"), unsafe_allow_html=True)
    unformatted_citations = st.text_area("Paste informal case citations or statutory references:", placeholder="e.g., Shehla Zia case 1994 supreme court page 693")
    citation_style = st.selectbox(
        "Select Target Style:",
        [
            "OSCOLA (UK/Commonwealth)",
            "Bluebook (US/International)",
            "APA 7th (Social Sciences)",
            "Chicago (Author-Date)",
            "Harvard",
        ],
        index=0 if is_law_like else 2,
        key=f"style_{discipline}",
    )
    
    if st.button("Format Citations", key="btn_p5"):
        if not is_configured:
            st.error("API key missing.")
        else:
            integrator = get_citation_integrator_agent(llm)
            task = Task(
                description=(
                    f"Convert these citations into standard {citation_style} style: {unformatted_citations}\n"
                    "For journal articles or books, call 'Verify Reference with Crossref' and report whether "
                    "a match was found. Law reports (e.g. PLD, SCMR) will not be in Crossref. "
                    "Do not invent missing details; flag anything that needs checking."
                ),
                expected_output=f"Standardized {citation_style} legal citations.",
                agent=integrator
            )
            run_crew(integrator, task)

# -----------------------------------------------------------------------------
# TAB 6: Publishing & Journal Matcher
# -----------------------------------------------------------------------------
with tab_p6:
    st.markdown(section_header("p6"), unsafe_allow_html=True)
    abstract_input = st.text_area("Paste your abstract and author notes for double-blind checking:")
    
    if st.button("Check Anonymization & Match Journals", key="btn_p6"):
        if not is_configured:
            st.error("API key missing.")
        else:
            publisher = get_journal_publisher_agent(llm)
            task = Task(
                description=(
                    f"Check abstract for identifying metadata and suggest 3 journals: {abstract_input}\n"
                    "Call 'Find Journals Publishing Similar Work (OpenAlex)' twice: region='pakistan' and "
                    "region='world'. Base suggestions on the results and tell the student to verify "
                    "scope, indexing (Scopus, HEC HJRS) and fees on each journal's website."
                ),
                expected_output="Anonymization report and 3 target journal recommendations.",
                agent=publisher
            )
            run_crew(publisher, task)
