"""
Example usage and configuration for Research Agent
Demonstrates how to use the research agent programmatically
"""

from research_agent import research_topic, break_down_query
from datetime import datetime
import os


def run_single_research(topic: str, save_report: bool = True) -> str:
    """
    Run a single research on a topic and optionally save the report.
    
    Args:
        topic: The research topic
        save_report: Whether to save the report to file
    
    Returns:
        The generated report
    """
    report = research_topic(topic)
    
    if save_report:
        filename = f"report_{topic.replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w") as f:
            f.write(report)
        print(f"\n💾 Report saved to: {filename}")
    
    return report


def batch_research(topics: list[str], output_dir: str = "./reports") -> dict[str, str]:
    """
    Run research on multiple topics and save all reports.
    
    Args:
        topics: List of research topics
        output_dir: Directory to save reports
    
    Returns:
        Dictionary mapping topics to reports
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    reports = {}
    
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*60}")
        print(f"Batch Research: {i}/{len(topics)}")
        print(f"{'='*60}")
        
        report = research_topic(topic)
        reports[topic] = report
        
        # Save report
        filename = os.path.join(
            output_dir,
            f"report_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        with open(filename, "w") as f:
            f.write(report)
        print(f"✅ Report saved to: {filename}")
    
    return reports


def analyze_topic_structure(topic: str) -> list[str]:
    """
    Show how a topic will be decomposed without running full research.
    Useful for planning or understanding research structure.
    
    Args:
        topic: The research topic
    
    Returns:
        List of sub-questions
    """
    print(f"\n📋 Research Structure for: {topic}")
    print("="*60)
    
    sub_questions = break_down_query(topic)
    
    print(f"This topic will be researched through {len(sub_questions)} sub-questions:\n")
    for i, q in enumerate(sub_questions, 1):
        print(f"{i}. {q}")
    
    return sub_questions


# Example research topics
EXAMPLE_TOPICS = [
    "Machine learning in healthcare",
    "Climate change mitigation strategies",
    "Future of remote work",
    "Cryptocurrency regulation",
    "Mental health in the workplace",
    "Renewable energy adoption",
    "Artificial intelligence ethics",
    "Supply chain optimization",
]


def main():
    """Main function showing different usage examples."""
    
    print("\n" + "="*60)
    print("Research Agent - Example Usage")
    print("="*60)
    
    print("\nChoose an option:")
    print("1. Run single research (interactive)")
    print("2. Run single research with predefined topic")
    print("3. Analyze topic structure (no full research)")
    print("4. Run batch research on multiple topics")
    print("5. View example topics")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        topic = input("Enter topic: ").strip()
        if topic:
            report = run_single_research(topic, save_report=True)
            print("\n" + "="*60)
            print(report)
    
    elif choice == "2":
        print("\nAvailable topics:")
        for i, topic in enumerate(EXAMPLE_TOPICS, 1):
            print(f"{i}. {topic}")
        
        idx = input("Select topic (1-8): ").strip()
        try:
            topic = EXAMPLE_TOPICS[int(idx) - 1]
            report = run_single_research(topic, save_report=True)
            print("\n" + "="*60)
            print(report)
        except (ValueError, IndexError):
            print("Invalid selection")
    
    elif choice == "3":
        topic = input("Enter topic to analyze: ").strip()
        if topic:
            analyze_topic_structure(topic)
    
    elif choice == "4":
        print("\nBatch Research Mode")
        print("Enter topics (one per line, empty line to finish):")
        topics = []
        while True:
            topic = input().strip()
            if not topic:
                break
            topics.append(topic)
        
        if topics:
            output_dir = f"batch_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            reports = batch_research(topics, output_dir=output_dir)
            print(f"\n✅ All reports saved to: {output_dir}")
    
    elif choice == "5":
        print("\nExample Research Topics:")
        print("="*60)
        for topic in EXAMPLE_TOPICS:
            print(f"• {topic}")
    
    elif choice == "6":
        print("\nGoodbye!")
        return
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    # Uncomment to run different examples:
    
    # Example 1: Single research
    # report = run_single_research("Artificial Intelligence in Education")
    
    # Example 2: Analyze topic structure
    # sub_questions = analyze_topic_structure("Climate Change Impacts")
    
    # Example 3: Batch research
    # topics = ["Electric Vehicles", "Renewable Energy", "Smart Cities"]
    # reports = batch_research(topics)
    
    # Example 4: Interactive menu
    main()
