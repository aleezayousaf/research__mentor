import streamlit as st
from config import (
    DEFAULT_PROVIDER,
    PROVIDERS,
    get_llm,
    setup_environment,
    test_api_key,
)
from crewai import Crew, Process, Task

# Import All Agents
from agents.guidance_hub import get_guidance_assistant_agent
from agents.socratic_supervisor import get_socratic_supervisor_agent
from agents.methodology_advisor import get_methodology_advisor_agent
from agents.legal_researcher import get_legal_researcher_agent
from agents.writing_coach import get_writing_coach_agent
from agents.citation_integrator import get_citation_integrator_agent
from agents.journal_publisher import get_journal_publisher_agent

st.set_page_config(page_title="ResearchMentor AI", page_icon="⚖️", layout="wide")


def run_crew(agent, task):
    """Run one agent on one task, with a progress message and friendly errors."""
    try:
        with st.spinner("The agent is working. This can take a minute..."):
            crew = Crew(agents=[agent], tasks=[task], verbose=True)
            result = crew.kickoff()
        st.markdown(result.raw)
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

# 1. Session State & Student Profile Management
if "student_profile" not in st.session_state:
    st.session_state["student_profile"] = {
        "name": "",
        "discipline": "Law",
        "observation": "",
        "research_topic": "",
        "selected_methodology": "Doctrinal Research"
    }

# Sidebar Profile Settings
with st.sidebar:
    st.title("👤 Student Profile")
    st.session_state["student_profile"]["name"] = st.text_input(
        "Your Name", value=st.session_state["student_profile"]["name"], placeholder="e.g. Ayesha"
    )
    st.session_state["student_profile"]["discipline"] = st.selectbox(
        "Discipline", ["Law (LL.B)", "Socio-Legal Studies", "International Relations", "Public Policy"]
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
    st.caption(
        "Your text is sent to the chosen provider. Free tiers may use it to improve "
        "their products, so avoid confidential material."
    )

st.title("⚖️ ResearchMentor AI: Legal Research Companion")

# 2. Main Navigation Tabs
tab_guidance, tab_p1, tab_p2, tab_p3, tab_p4, tab_p5, tab_p6 = st.tabs([
    "💡 Guidance & Q&A Hub",
    "1. Observation & Topic",
    "2. Methodology & Gap",
    "3. Legal Sources",
    "4. IRAC Writing",
    "5. Citation Check",
    "6. Publishing Match"
])

# -----------------------------------------------------------------------------
# TAB 0: Interactive Guidance & Q&A Hub
# -----------------------------------------------------------------------------
with tab_guidance:
    st.header("💡 Interactive Guidance & Q&A Hub")
    st.markdown("Ask research questions and choose your preferred learning resource style.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        user_query = st.text_area("What research question or concept do you need help with?", 
                                 placeholder="e.g., How do I structure a legal literature review?")
    with col2:
        resource_mode = st.radio(
            "Resource Preference:",
            ["Supervisor Recommended Guides (Stanford, OSCOLA)", "Search Live Web Resources"],
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
# TAB 1: Observation & Topic Discovery
# -----------------------------------------------------------------------------
with tab_p1:
    st.header("Stage 1: Real-World Observation & Topic Discovery")
    st.markdown("Share a real-world legal issue or event you observed in practice or news.")
    
    observation_input = st.text_area(
        "What real-world legal problem or situation did you notice?",
        placeholder="e.g., Seasonal smog in Lahore causes school closures, but existing environmental regulations are rarely enforced."
    )
    
    if st.button("Explore Topics & Domains", key="btn_p1"):
        if not is_configured:
            st.error("API key missing.")
        else:
            st.session_state["student_profile"]["observation"] = observation_input
            supervisor = get_socratic_supervisor_agent(llm)
            task = Task(
                description=(
                    f"Student Name: {st.session_state['student_profile']['name']}\n"
                    f"Student Observation: {observation_input}\n"
                    "Acknowledge the student's real-world observation. Suggest 3 specific sub-domains "
                    "they could explore (e.g., Constitutional Writs, Environmental Statutory Enforcement, or Public Trust Doctrine). "
                    "Ask 2 encouraging questions to help them frame a clear research topic."
                ),
                expected_output="An encouraging response with 3 sub-domain suggestions and 2 guiding questions.",
                agent=supervisor
            )
            run_crew(supervisor, task)

# -----------------------------------------------------------------------------
# TAB 2: Methodology & Research Gap
# -----------------------------------------------------------------------------
with tab_p2:
    st.header("Stage 2: Methodology & Research Gap Guidance")
    
    method_choice = st.selectbox(
        "Select Legal Research Methodology:",
        ["Doctrinal Legal Research (Statutes & Case Law)", 
         "Socio-Legal / Empirical Research (Surveys & Field Data)", 
         "Comparative Legal Research (Cross-Jurisdictional Analysis)"]
    )
    
    research_question = st.text_input(
        "Enter your research question (from Stage 1):",
        value=st.session_state["student_profile"]["research_topic"]
    )
    
    if st.button("Generate Paragraph-by-Paragraph Methodology Guide", key="btn_p2"):
        if not is_configured:
            st.error("API key missing.")
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
    st.header("Stage 3: Legal Sources & Statutory Retrieval")
    search_query = st.text_input("Enter key legal terms or statutory provisions to search:", placeholder="e.g., Right to Life Article 9 Pakistan Code")
    
    if st.button("Search OpenAlex & Pakistan Code", key="btn_p3"):
        if not is_configured:
            st.error("API key missing.")
        else:
            researcher = get_legal_researcher_agent(llm)
            task = Task(
                description=(
                    f"Find legal papers and statutory provisions related to: {search_query}\n"
                    "1. Call 'Search Pakistan-Affiliated Scholarship (OpenAlex)' first.\n"
                    "2. Call 'Search Global Scholarly Literature (OpenAlex RAG)' for worldwide scholarship.\n"
                    "3. Call 'Pakistan Code Official-Source Verification Guide' for Pakistani primary law, "
                    "and tell the student to confirm statutes on the official portals.\n"
                    "Never invent a statute, case or article; mark anything unverified."
                ),
                expected_output="Summarized primary and secondary sources with reference links.",
                agent=researcher
            )
            run_crew(researcher, task)

# -----------------------------------------------------------------------------
# TAB 4: IRAC Writing & Review
# -----------------------------------------------------------------------------
with tab_p4:
    st.header("Stage 4: IRAC/CREAC Legal Writing Review")
    student_draft = st.text_area("Paste a paragraph or section of your draft here:", height=150)
    
    if st.button("Review Writing Logic", key="btn_p4"):
        if not is_configured:
            st.error("API key missing.")
        else:
            coach = get_writing_coach_agent(llm)
            task = Task(
                description=(
                    f"Student Draft: {student_draft}\n"
                    "Perform a structural review using the 3-part matrix:\n"
                    "1. Validation: Praise accurate factual claims (noting issue statements do not need citations).\n"
                    "2. Rule Analysis: Identify missing statutory provisions or precedents.\n"
                    "3. Side-by-Side Example: Show a concrete 'Before vs. After' table showing how to integrate proper authority."
                ),
                expected_output="A 3-part pedagogical review containing a side-by-side 'Before vs. After' transformation table.",
                agent=coach
            )
            run_crew(coach, task)

# -----------------------------------------------------------------------------
# TAB 5: Citation Integrity
# -----------------------------------------------------------------------------
with tab_p5:
    st.header("Stage 5: Citation Integrity & Formatting")
    unformatted_citations = st.text_area("Paste informal case citations or statutory references:", placeholder="e.g., Shehla Zia case 1994 supreme court page 693")
    citation_style = st.selectbox("Select Target Style:", ["OSCOLA (UK/Commonwealth)", "Bluebook (US/International)"])
    
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
    st.header("Stage 6: Publishing & Journal Alignment")
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