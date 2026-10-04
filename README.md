# ResearchMentor AI: Legal Research Companion

A step-by-step AI mentor for law and socio-legal students, with a focus on **Pakistan first, then the wider world**. Built with [CrewAI](https://docs.crewai.com/) and [Streamlit](https://streamlit.io/).

The app has seven AI helpers, one per tab:

| Tab | Helper | What it does |
|---|---|---|
| Guidance & Q&A Hub | Guidance assistant | Answers research-method and writing questions |
| 1. Observation & Topic | Socratic supervisor | Turns a real-world observation into a research topic |
| 2. Methodology & Gap | Methodology advisor | Paragraph-by-paragraph methodology guidance |
| 3. Legal Sources | Legal researcher | Finds scholarship (Pakistan first, then global) and points to official Pakistani law sources |
| 4. IRAC Writing | Writing coach | Reviews your draft using IRAC/CREAC |
| 5. Citation Check | Citation integrator | Formats OSCOLA/Bluebook citations and checks references |
| 6. Publishing Match | Journal publisher | Checks anonymisation and suggests journals |

**Free data tools (no key needed):** OpenAlex, Crossref, and links to official Pakistani legal sources (Pakistan Code, Supreme Court, National Assembly, High Courts).

## Choose your free AI provider

You need one free API key from any provider. The app shows a button with the sign-up link for whichever you pick.

| Provider | Models in the app | Get a free key |
|---|---|---|
| Gemini (Google) | Gemini 3.8 Flash, Gemini 3.5 Flash-Lite | https://aistudio.google.com/apikey |
| Groq | OpenAI gpt-oss-120b, Meta Llama 3.3 70B | https://console.groq.com/keys |
| OpenRouter | gpt-oss-120b (free), Llama 3.3 70B (free) | https://openrouter.ai/keys |
| Mistral | Mistral Small, Mistral Large | https://console.mistral.ai/api-keys |

Free tiers have daily limits and may use your text to improve their products. Do not paste confidential material. This app is an academic aid, not legal advice. Always check primary sources.

> Note: Groq (the fast free provider above) is a different company from xAI's Grok, which is paid.

## Run it on Google Colab (easiest)

1. Open `research_mentor_colab.ipynb` in [Google Colab](https://colab.research.google.com/) (File > Upload notebook).
2. Run the cells one at a time. In Step 1, upload a zip of this repository (on GitHub: green **Code** button > **Download ZIP**).
3. Open the link from Step 4, choose a provider in the sidebar, and paste your key.

## Run it on your own computer (Windows)

1. Install [Python 3.10 or newer](https://www.python.org/downloads/) (tick "Add Python to PATH").
2. Double-click `run_app.bat`. The first run installs everything.

Other systems:

```bash
pip install -U -r requirements.txt
streamlit run app.py
```

## Keeping your key safe

Never write your key into the code or upload it to GitHub. Paste it in the sidebar each time, or put it in `.streamlit/secrets.toml` (ignored by Git), for example:

```toml
GEMINI_API_KEY = "your-key-here"
```

The name must match the provider: `GEMINI_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY` or `MISTRAL_API_KEY`.

## If something goes wrong

- **401:** the key was rejected. Make a new one and paste only the key. Use **Test my API key**.
- **404:** the model was renamed or retired. Pick another model, or edit the lists in `config.py`.
- **429:** free limit reached. Wait a minute, or switch provider in the sidebar.
