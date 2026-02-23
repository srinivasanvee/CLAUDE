"""
Research Agent - A Senior Research Analyst Agent
Provides deep, factual, and synthesized reports on any topic.
"""

import anthropic
import json
from datetime import datetime

# Initialize Anthropic client
client = anthropic.Anthropic()
MODEL_NAME = "claude-3-5-sonnet-20241022"


def break_down_query(topic: str) -> list[str]:
    """
    Analyze the user's request and break it down into 3-5 sub-questions.
    """
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""You are a research analyst. Break down this research topic into 3-5 specific, focused sub-questions that would help you gather comprehensive information about it.

Topic: {topic}

Respond with a JSON array of exactly 3-5 sub-questions (strings). Example format:
["Sub-question 1?", "Sub-question 2?", "Sub-question 3?"]

IMPORTANT: Return ONLY the JSON array, no other text.""",
            }
        ],
    )
    
    response_text = message.content[0].text.strip()
    try:
        sub_questions = json.loads(response_text)
        return sub_questions
    except json.JSONDecodeError:
        # Fallback: create generic sub-questions
        return [
            f"What are the key concepts and definitions related to {topic}?",
            f"What is the current state and recent developments in {topic}?",
            f"What are the main challenges and opportunities in {topic}?",
            f"What are expert perspectives and best practices related to {topic}?",
            f"What is the future outlook for {topic}?"
        ]


def search_for_information(query: str) -> str:
    """
    Simulate web search by using Claude to generate search results.
    In a real implementation, this would use an actual search API.
    """
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": f"""You are a web search engine that returns comprehensive information. 
                
Search query: {query}

Provide a detailed, factual response with key information, statistics, and recent developments related to this query. 
Include specific sources/references where possible.""",
            }
        ],
    )
    
    return message.content[0].text


def evaluate_and_refine(
    original_question: str, initial_findings: str
) -> str:
    """
    Evaluate if findings are satisfactory. If vague, perform targeted follow-up.
    """
    # Check if we need more specific information
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Review these research findings for the question: "{original_question}"

Initial findings:
{initial_findings}

Are these findings comprehensive and specific enough? If not, what specific follow-up question would get better information? 
Respond with either "SUFFICIENT" or "NEEDS_FOLLOWUP: [specific follow-up question]" """,
            }
        ],
    )
    
    evaluation = message.content[0].text.strip()
    
    if "SUFFICIENT" in evaluation:
        return initial_findings
    elif "NEEDS_FOLLOWUP" in evaluation:
        # Extract the follow-up question
        followup = evaluation.split("NEEDS_FOLLOWUP:")[-1].strip()
        followup_findings = search_for_information(followup)
        return f"{initial_findings}\n\n**Follow-up findings:** {followup_findings}"
    
    return initial_findings


def synthesize_report(
    topic: str, sub_questions: list[str], findings_by_question: dict[str, str]
) -> str:
    """
    Combine all findings into a structured Markdown report.
    """
    findings_text = ""
    for question, findings in findings_by_question.items():
        findings_text += f"\n**Question:** {question}\n{findings}\n"
    
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=3000,
        messages=[
            {
                "role": "user",
                "content": f"""You are a research synthesizer. Create a professional, well-structured markdown report based on the following research findings.

Topic: {topic}

Research findings from sub-questions:
{findings_text}

Create a report with the following structure:
## [Topic Title]
### Executive Summary
[Brief 2-3 paragraph overview of the topic]

### Detailed Findings
[Organize findings logically by theme/subtopic]

### Key Takeaways
[3-5 main insights]

### Sources & References
[List any sources mentioned in the findings]

Make the report professional, comprehensive, and well-organized. Use markdown formatting appropriately.""",
            }
        ],
    )
    
    return message.content[0].text


def research_topic(topic: str) -> str:
    """
    Main research flow: Analyze -> Search -> Evaluate -> Synthesize
    """
    print(f"\n{'='*60}")
    print(f"Starting Research on: {topic}")
    print(f"{'='*60}\n")
    
    # Step 1: Break down the query
    print("📋 Step 1: Analyzing request and generating sub-questions...")
    sub_questions = break_down_query(topic)
    print(f"Generated {len(sub_questions)} sub-questions:")
    for i, q in enumerate(sub_questions, 1):
        print(f"  {i}. {q}")
    
    # Step 2: Search for information on each sub-question
    print("\n🔍 Step 2: Searching for information...")
    findings_by_question = {}
    for i, question in enumerate(sub_questions, 1):
        print(f"  Researching sub-question {i}/{len(sub_questions)}...")
        initial_findings = search_for_information(question)
        
        # Step 3: Evaluate and refine if needed
        print(f"    Evaluating findings...")
        refined_findings = evaluate_and_refine(question, initial_findings)
        findings_by_question[question] = refined_findings
    
    # Step 4: Synthesize into report
    print("\n📊 Step 3: Synthesizing findings into report...")
    report = synthesize_report(topic, sub_questions, findings_by_question)
    
    return report


def main():
    """Main entry point for the Research Agent."""
    print("\n" + "="*60)
    print("🔬 RESEARCH AGENT - Senior Research Analyst")
    print("="*60)
    print("\nWelcome! I will provide deep, factual, and synthesized reports")
    print("on any topic you provide.\n")
    
    while True:
        topic = input("Enter topic for research (or 'quit' to exit): ").strip()
        
        if topic.lower() in ["quit", "exit", "q"]:
            print("\nThank you for using Research Agent. Goodbye!")
            break
        
        if not topic:
            print("Please enter a valid topic.\n")
            continue
        
        # Perform the research
        report = research_topic(topic)
        
        # Display the report
        print("\n" + "="*60)
        print("RESEARCH REPORT")
        print("="*60)
        print(report)
        print("\n" + "="*60)
        
        # Ask if user wants to save the report
        save = input("\nWould you like to save this report? (yes/no): ").strip().lower()
        if save in ["yes", "y"]:
            filename = f"report_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(filename, "w") as f:
                f.write(report)
            print(f"Report saved to: {filename}")
        
        print()


if __name__ == "__main__":
    main()
