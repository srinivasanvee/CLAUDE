"""
Advanced Research Agent using LangGraph
A graph-based state machine approach to research task orchestration.
Powered by OpenAI GPT-4o + Brave Search API for real-time web search.
"""

import json
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.graph import CompiledGraph
from typing_extensions import TypedDict
from brave_search import brave_search

load_dotenv()


class ResearchState(TypedDict):
    """State object for research agent."""
    topic: str
    sub_questions: list[str]
    findings: dict[str, str]
    evaluation_results: dict[str, bool]
    final_report: str
    current_step: int


class ResearchAgentGraph:
    """Research Agent implemented as a LangGraph state machine."""

    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4o"
        self.graph = self._build_graph()

    def _chat(self, prompt: str, max_tokens: int = 1000) -> str:
        """Helper to call OpenAI chat completions."""
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

    def _build_graph(self) -> CompiledGraph:
        """Build the LangGraph workflow."""
        graph_builder = StateGraph(ResearchState)

        # Add nodes
        graph_builder.add_node("analyze_query", self.analyze_query)
        graph_builder.add_node("search_findings", self.search_findings)
        graph_builder.add_node("evaluate_findings", self.evaluate_findings)
        graph_builder.add_node("synthesize_report", self.synthesize_report)

        # Add edges
        graph_builder.add_edge(START, "analyze_query")
        graph_builder.add_edge("analyze_query", "search_findings")
        graph_builder.add_edge("search_findings", "evaluate_findings")
        graph_builder.add_edge("evaluate_findings", "synthesize_report")
        graph_builder.add_edge("synthesize_report", END)

        return graph_builder.compile()

    def analyze_query(self, state: ResearchState) -> ResearchState:
        """Step 1: Break down the user's request into sub-questions."""
        print("\nStep 1: Analyzing request and generating sub-questions...")

        prompt = f"""You are a research analyst. Break down this research topic into 3-5 specific, focused sub-questions.

Topic: {state['topic']}

Respond with a JSON array of exactly 3-5 sub-questions. Example:
["Question 1?", "Question 2?", "Question 3?"]

IMPORTANT: Return ONLY the JSON array, no other text."""

        response_text = self._chat(prompt, max_tokens=1000)
        try:
            sub_questions = json.loads(response_text)
        except json.JSONDecodeError:
            sub_questions = [
                f"What are the key concepts related to {state['topic']}?",
                f"What are recent developments in {state['topic']}?",
                f"What are the challenges in {state['topic']}?",
                f"What is the future outlook for {state['topic']}?",
            ]

        state["sub_questions"] = sub_questions
        state["findings"] = {}
        state["evaluation_results"] = {}

        print(f"Generated {len(sub_questions)} sub-questions")
        for i, q in enumerate(sub_questions, 1):
            print(f"   {i}. {q}")

        return state

    def search_findings(self, state: ResearchState) -> ResearchState:
        """Step 2: Search for information on each sub-question using Brave Search."""
        print("\nStep 2: Searching for information via Brave Search...")

        for i, question in enumerate(state["sub_questions"], 1):
            print(f"   Researching sub-question {i}/{len(state['sub_questions'])}...")

            # Real-time web search via Brave
            raw_results = brave_search(question, count=5)

            # Summarize with GPT-4o
            prompt = f"""You are a research analyst. Using the following real-time web search results, provide a comprehensive, factual summary.

Research Question: {question}

Web Search Results:
{raw_results}

Synthesize into a detailed, factual response including key statistics, expert views, and recent developments. Reference source URLs where relevant."""

            state["findings"][question] = self._chat(prompt, max_tokens=1500)

        print(f"Completed searches for all sub-questions")
        return state

    def evaluate_findings(self, state: ResearchState) -> ResearchState:
        """Step 3: Evaluate findings and perform secondary searches if needed."""
        print("\nStep 3: Evaluating findings and refining as needed...")

        for question, findings in state["findings"].items():
            prompt = f"""Review these findings for: "{question}"

Findings:
{findings}

Are these comprehensive? Answer only: "SUFFICIENT" or "NEEDS_REFINEMENT"."""

            evaluation = self._chat(prompt, max_tokens=300)
            is_sufficient = "SUFFICIENT" in evaluation
            state["evaluation_results"][question] = is_sufficient

            if not is_sufficient:
                print(f"   Refining findings for: {question[:50]}...")

                # Run a follow-up Brave search with a more targeted query
                followup_query = f"{question} detailed analysis statistics 2025"
                followup_raw = brave_search(followup_query, count=5)

                followup_prompt = f"""For "{question}", provide additional specific details, examples, and recent case studies using these supplementary search results:

{followup_raw}

Focus on what was missing or vague in the original findings:
{findings}"""

                additional = self._chat(followup_prompt, max_tokens=1000)
                state["findings"][question] += "\n\n**Additional Details:**\n" + additional

        print(f"Evaluation complete")
        return state

    def synthesize_report(self, state: ResearchState) -> ResearchState:
        """Step 4: Synthesize all findings into a structured report."""
        print("\nStep 4: Synthesizing findings into comprehensive report...")

        findings_text = ""
        for question, findings in state["findings"].items():
            findings_text += f"\n**Research Question:** {question}\n\n{findings}\n\n{'-'*40}\n"

        prompt = f"""Create a professional markdown research report based on these findings gathered from real-time web searches.

Topic: {state['topic']}

Research Findings:
{findings_text}

Structure the report as follows:

## {state['topic']}

### Executive Summary
[2-3 paragraphs summarizing the key findings]

### Detailed Findings
[Organize findings by logical themes and subtopics. Use clear headings and formatting.]

### Key Insights & Analysis
[3-5 main takeaways from the research]

### Trends & Future Outlook
[What's emerging and what's the future direction]

### Sources & References
[List all source URLs mentioned in the findings]

---
*Report generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')} | Model: GPT-4o | Search: Brave Search API*

Make the report professional, comprehensive, and actionable."""

        state["final_report"] = self._chat(prompt, max_tokens=4000)
        print(f"Report synthesis complete")
        return state

    def run(self, topic: str) -> str:
        """Execute the research workflow."""
        initial_state: ResearchState = {
            "topic": topic,
            "sub_questions": [],
            "findings": {},
            "evaluation_results": {},
            "final_report": "",
            "current_step": 0,
        }

        print(f"\n{'='*60}")
        print(f"RESEARCH AGENT - Advanced LangGraph Version")
        print(f"Model: GPT-4o | Search: Brave Search API")
        print(f"{'='*60}")
        print(f"Topic: {topic}")

        final_state = self.graph.invoke(initial_state)
        return final_state["final_report"]


def main():
    """Main entry point for the advanced research agent."""
    agent = ResearchAgentGraph()

    while True:
        print("\n" + "=" * 60)
        print("Advanced Research Agent (LangGraph + GPT-4o + Brave Search)")
        print("=" * 60)

        topic = input("\nEnter topic for research (or 'quit' to exit): ").strip()

        if topic.lower() in ["quit", "exit", "q"]:
            print("\nThank you for using Research Agent. Goodbye!")
            break

        if not topic:
            print("Please enter a valid topic.")
            continue

        try:
            report = agent.run(topic)

            # Display the report
            print("\n" + "=" * 60)
            print("RESEARCH REPORT")
            print("=" * 60)
            print(report)
            print("\n" + "=" * 60)

            # Ask if user wants to save
            save = input("\nSave this report? (yes/no): ").strip().lower()
            if save in ["yes", "y"]:
                filename = f"report_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(filename, "w") as f:
                    f.write(report)
                print(f"Report saved to: {filename}")

        except Exception as e:
            print(f"Error during research: {e}")


if __name__ == "__main__":
    main()
