"""
Research Agent - OpenAI Agents SDK Implementation
Uses the OpenAI Agents SDK for structured multi-tool agent orchestration.
Powered by GPT-4o + Brave Search API for real-time web search.
"""

from datetime import datetime
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from brave_search import brave_search as _brave_search

load_dotenv()

MODEL = "gpt-4o"

# ---------------------------------------------------------------------------
# Error classes
# ---------------------------------------------------------------------------

class BraveSearchError(RuntimeError):
    """Raised when a Brave Search API call fails. Stops agent execution."""


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@function_tool
def brave_web_search(query: str) -> str:
    """
    Search the web using the Brave Search API and return relevant results.

    Args:
        query: The search query string to look up on the web.

    Returns:
        Formatted search results with titles, descriptions, and source URLs.
    """
    print(f"\n  [Brave Search] Query: {query!r}")

    raw = _brave_search(query, count=5)

    # Detect error responses returned as strings from brave_search.py
    # and convert them to exceptions so execution halts
    error_prefixes = (
        "[WARNING:",
        "Brave Search API error:",
        "Brave Search request timed out",
        "Brave Search connection error",
        "Brave Search request failed",
        "No results found",
    )
    if raw.startswith(error_prefixes):
        print(f"  [Brave Search] FAILED: {raw}")
        raise BraveSearchError(raw)

    result_count = raw.count("Source:") or raw.count("---")
    print(f"  [Brave Search] OK — received {result_count} result(s)")
    return raw


@function_tool
def save_report(topic: str, report_content: str) -> str:
    """
    Save the final research report to a markdown file with a timestamp.

    Args:
        topic: The research topic (used to name the file).
        report_content: The full markdown report content to save.

    Returns:
        Confirmation message with the saved file path.
    """
    safe_topic = topic.replace(" ", "_").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{safe_topic}_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(report_content)
    print(f"\n  [Save Report] Written to: {filename}")
    return f"Report saved to: {filename}"


# ---------------------------------------------------------------------------
# Agent Definition
# ---------------------------------------------------------------------------

RESEARCH_INSTRUCTIONS = """You are a Senior Research Analyst with access to real-time web search.

When given a research topic, follow this structured workflow:

**Step 1 — Analyze the Query**
Break the topic into 3-5 specific, focused sub-questions that cover different aspects
(definitions, current state, challenges, expert views, future outlook).

**Step 2 — Search for Information**
For EACH sub-question, call `brave_web_search` with a targeted search query.
Gather comprehensive, up-to-date information from multiple searches.

**Step 3 — Evaluate & Refine**
Review the search results for each sub-question. If any area lacks depth or specifics,
run an additional `brave_web_search` with a more targeted follow-up query.

**Step 4 — Synthesize the Report**
Combine all findings into a professional markdown report with this structure:

```
## [Topic Title]

### Executive Summary
[2-3 paragraphs summarizing key findings]

### Detailed Findings
[Organized by theme/subtopic with clear headings]

### Key Insights & Analysis
[3-5 main takeaways]

### Trends & Future Outlook
[Emerging trends and future direction]

### Sources & References
[All source URLs from search results]

---
*Report generated on [date] | Model: GPT-4o | Search: Brave Search API*
```

Always cite actual URLs from the search results. Be thorough, accurate, and professional.
After generating the report, call `save_report` to persist it to disk."""

research_agent = Agent(
    name="Senior Research Analyst",
    model=MODEL,
    instructions=RESEARCH_INSTRUCTIONS,
    tools=[brave_web_search, save_report],
)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def research_topic(topic: str) -> str:
    """
    Run the OpenAI Agents SDK research workflow for a given topic.
    Raises BraveSearchError immediately if any search call fails.

    Args:
        topic: The research topic to investigate.

    Returns:
        The generated research report as a markdown string.
    """
    print(f"\n{'='*60}")
    print(f"RESEARCH AGENT - OpenAI Agents SDK")
    print(f"Model: {MODEL} | Search: Brave Search API")
    print(f"{'='*60}")
    print(f"Topic: {topic}\n")

    prompt = (
        f"Please conduct comprehensive research on the following topic and generate "
        f"a complete professional markdown report:\n\nTopic: {topic}"
    )

    # BraveSearchError propagates out of Runner.run_sync — no swallowing
    result = Runner.run_sync(research_agent, prompt)
    return result.final_output


def main():
    """Main entry point for the OpenAI Agents SDK Research Agent."""
    print("\n" + "=" * 60)
    print("RESEARCH AGENT - OpenAI Agents SDK")
    print("Powered by GPT-4o + Brave Search API")
    print("=" * 60)
    print("\nReal-time web search enabled via Brave Search API.")
    print("Reports are automatically saved to disk.\n")

    while True:
        topic = input("Enter topic for research (or 'quit' to exit): ").strip()

        if topic.lower() in ["quit", "exit", "q"]:
            print("\nThank you for using Research Agent. Goodbye!")
            break

        if not topic:
            print("Please enter a valid topic.\n")
            continue

        try:
            report = research_topic(topic)

            print("\n" + "=" * 60)
            print("RESEARCH REPORT")
            print("=" * 60)
            print(report)
            print("\n" + "=" * 60)

        except BraveSearchError as e:
            print(f"\n[ERROR] Brave Search API call failed — execution stopped.")
            print(f"        Reason: {e}")
            print("        Check your API key in brave_search.py or BRAVE_API_KEY env var.")
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {type(e).__name__}: {e}")

        print()


if __name__ == "__main__":
    main()
