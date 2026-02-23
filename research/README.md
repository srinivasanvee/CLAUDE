# Research Agent - Senior Research Analyst

A sophisticated research agent application that breaks down complex research requests, performs comprehensive information gathering, and synthesizes findings into professional reports.

## Overview

This project provides **three implementations** of a research agent:

| File | Framework | Model | Search |
|------|-----------|-------|--------|
| `research_agent.py` | Standard Python | Claude 3.5 Sonnet | Simulated (Claude knowledge) |
| `research_agent_langgraph.py` | LangGraph state machine | GPT-4o | Brave Search API (real-time) |
| `research_agent_openai_sdk.py` | OpenAI Agents SDK | GPT-4o | Brave Search API (real-time) |

All agents follow the same operational loop:
1. **Analyze** — Break down the request into 3-5 focused sub-questions
2. **Search** — Gather information for each sub-question
3. **Evaluate** — Assess findings and perform targeted follow-ups if needed
4. **Synthesize** — Create a structured professional markdown report

---

## Installation

**1. Clone or navigate to the project directory:**
```bash
cd research
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set up API keys:**
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

Required keys per implementation:

| Key | Required by |
|-----|-------------|
| `ANTHROPIC_API_KEY` | `research_agent.py` |
| `OPENAI_API_KEY` | `research_agent_langgraph.py`, `research_agent_openai_sdk.py` |
| `BRAVE_API_KEY` | `research_agent_langgraph.py`, `research_agent_openai_sdk.py` |

Get your Brave Search API key at: https://brave.com/search/api/

---

## Usage

### 1. Standard Implementation (Claude / Anthropic)

```bash
python research_agent.py
```

- Uses Claude 3.5 Sonnet
- Sequential processing
- No external search (uses Claude's built-in knowledge)
- Good for general, evergreen topics

---

### 2. LangGraph Implementation (GPT-4o + Brave Search)

```bash
python research_agent_langgraph.py
```

- Uses GPT-4o via OpenAI API
- Graph-based state machine architecture (LangGraph)
- Real-time web search via Brave Search API
- Better for current events and up-to-date topics
- Extensible node-based design

```
Topic: Climate change impacts on agriculture

Step 1: Analyzing request and generating sub-questions...
Step 2: Searching for information via Brave Search...
Step 3: Evaluating findings and refining as needed...
Step 4: Synthesizing findings into comprehensive report...
```

---

### 3. OpenAI Agents SDK Implementation (GPT-4o + Brave Search)

```bash
python research_agent_openai_sdk.py
```

- Uses GPT-4o via OpenAI Agents SDK (`openai-agents`)
- Agent autonomously decides when and how to search
- Two tools: `brave_web_search` and `save_report`
- Reports automatically saved to disk
- Most autonomous of the three implementations

```
Topic: Quantum computing breakthroughs 2025

RESEARCH AGENT - OpenAI Agents SDK
Model: GPT-4o | Search: Brave Search API
Real-time web search enabled via Brave Search API.
```

---

## Shared Utilities

### `brave_search.py`

Shared Brave Search API utility used by the LangGraph and OpenAI SDK implementations.

```python
from brave_search import brave_search

results = brave_search("quantum computing 2025", count=5)
print(results)
```

---

## Report Output Format

```markdown
## [Topic Title]

### Executive Summary
[2-3 paragraph overview]

### Detailed Findings
[Organized by themes and subtopics]

### Key Insights & Analysis
[Main takeaways from the research]

### Trends & Future Outlook
[Emerging trends and future direction]

### Sources & References
[Cited source URLs]

---
*Report generated on [date] | Model: GPT-4o | Search: Brave Search API*
```

---

## Architecture Comparison

| Feature | Standard (`research_agent.py`) | LangGraph (`research_agent_langgraph.py`) | OpenAI SDK (`research_agent_openai_sdk.py`) |
|---------|-------------------------------|-------------------------------------------|---------------------------------------------|
| Model | Claude 3.5 Sonnet | GPT-4o | GPT-4o |
| Search | Simulated (LLM knowledge) | Brave Search API (real-time) | Brave Search API (real-time) |
| Orchestration | Sequential Python functions | LangGraph state machine | OpenAI Agents SDK |
| State Management | Dictionary | TypedDict | Agent memory |
| Autonomy | Low (fixed steps) | Medium (graph-driven) | High (agent decides) |
| Auto-save reports | Manual | Manual | Automatic (via tool) |
| Production Ready | ✓ | ✓✓ | ✓✓✓ |

---

## Dependencies

```
anthropic>=0.7.0        # Claude API (research_agent.py)
openai>=1.0.0           # OpenAI API
openai-agents>=0.0.1    # OpenAI Agents SDK
langgraph>=0.2.0        # Graph-based orchestration
requests>=2.31.0        # HTTP (Brave Search)
python-dotenv>=1.0.0    # .env file loading
typing_extensions>=4.0.0
```

---

## Error Handling

All implementations include:
- JSON parsing error handling with fallback sub-question generation
- Brave Search API error handling (auth, rate limits, timeouts)
- Graceful exception handling in `main()` loops
- User-friendly error messages

---

**Version:** 2.0
**Status:** Production Ready
