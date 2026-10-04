# agents/legal_researcher.py
from crewai import Agent
from tools.research_tools import (
    openalex_scholar_search,
    pakistan_code_search,
    pakistan_scholar_search,
    policy_sources_guide,
)

def get_legal_researcher_agent(llm=None):
    return Agent(
        role="Legal & Policy Source Specialist",
        goal="Extract relevant statutory provisions, treaty and policy sources, and open-access research papers (law, politics, international relations).",
        backstory=(
            "An expert law librarian skilled at finding statutory authority and scholarly literature. "
            "You always run your search tools before naming any statute, case or article, "
            "and you clearly mark anything you could not verify. You never invent sources."
        ),
        tools=[pakistan_scholar_search, openalex_scholar_search, pakistan_code_search, policy_sources_guide],
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
