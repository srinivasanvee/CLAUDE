# Quick Start Guide - Research Agent

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd research
pip install -r requirements.txt
```

### Step 2: Set Up API Key
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-...
```

Get your API key from: https://console.anthropic.com/

### Step 3: Run the Agent
```bash
# Option A: Standard implementation (recommended for beginners)
python research_agent.py

# Option B: Advanced LangGraph version
python research_agent_langgraph.py

# Option C: Interactive examples menu
python example_usage.py
```

## 📝 How to Use

### Interactive Mode
Simply run either script and enter your research topic:
```
Enter topic for research: How does photosynthesis work?
```

The agent will:
1. Break down your question into 3-5 sub-questions
2. Research each sub-question
3. Evaluate and refine findings
4. Generate a professional report
5. Ask if you want to save it

### Programmatic Mode
Use in your own Python scripts:

```python
from research_agent import research_topic

# Run research
report = research_topic("Your Topic Here")

# Use the report
print(report)

# Or save it
with open("my_report.md", "w") as f:
    f.write(report)
```

## 💡 Example Topics to Try

- "Impact of artificial intelligence on education"
- "Electric vehicles vs traditional cars"
- "Remote work productivity studies"
- "Quantum computing breakthroughs"
- "Sustainable fashion industry"
- "Cybersecurity trends"

## 🎯 What Makes This Research Agent Special

✅ **Intelligent Decomposition** - Breaks complex topics into focused questions
✅ **Quality Evaluation** - Validates findings and refines if needed
✅ **Professional Reports** - Generates well-structured markdown documents
✅ **Easy to Use** - Interactive and programmatic interfaces
✅ **Extensible** - LangGraph version ready for custom workflows

## 📚 File Structure

```
research/
├── research_agent.py              # Standard implementation
├── research_agent_langgraph.py    # Advanced graph-based version
├── example_usage.py               # Usage examples
├── requirements.txt               # Dependencies
├── README.md                      # Full documentation
├── QUICKSTART.md                  # This file
└── .env.example                   # Configuration template
```

## 🆘 Troubleshooting

**"ModuleNotFoundError: No module named 'anthropic'"**
```bash
pip install -r requirements.txt
```

**"API key not found"**
- Check that `.env` file exists and has your API key
- Rerun: `cp .env.example .env` and edit it

**"ANTHROPIC_API_KEY not set"**
```bash
export ANTHROPIC_API_KEY=your_key_here
```

**LangGraph installation issues:**
```bash
pip install --upgrade langgraph
```

## 🔧 Configuration

Edit the Python files to customize:
- Model: Change `MODEL_NAME` to use different Claude versions
- Max tokens: Adjust `max_tokens` for different output lengths
- Report format: Modify the synthesis prompt

## 📊 Sample Output

```markdown
## Artificial Intelligence in Education

### Executive Summary
Artificial intelligence is transforming education through [...]

### Detailed Findings
#### Current Applications
- Personalized Learning Systems
- Automated Grading
- Intelligent Tutoring Systems
...

### Key Insights & Analysis
1. AI improves student engagement
2. Reduces teacher workload
...

### Trends & Future Outlook
The education sector is moving toward...

### Sources & References
- [Various academic and industry sources]
```

## 📈 Advanced Usage

### Batch Research Multiple Topics
```python
from example_usage import batch_research

topics = ["AI", "Climate Change", "Remote Work"]
reports = batch_research(topics, output_dir="./my_reports")
```

### Analyze Topic Structure
```python
from example_usage import analyze_topic_structure

sub_questions = analyze_topic_structure("Your Topic")
```

### Custom Implementation
Extend the agent for your needs:
```python
from research_agent import break_down_query, search_for_information

# Use individual functions
questions = break_down_query("Your Topic")
for q in questions:
    findings = search_for_information(q)
    # Do something with findings
```

## ⚡ Performance Tips

- **First run:** Typically takes 2-3 minutes per topic
- **Batch processing:** Process multiple topics in sequence
- **Cache results:** Save reports locally to reference later
- **Topic complexity:** Simpler, well-defined topics run faster

## 🎓 Learning Resources

- Full documentation: See [README.md](README.md)
- Anthropic Claude docs: https://docs.anthropic.com/
- LangGraph docs: https://langchain-ai.github.io/langgraph/

## 🚀 Next Steps

1. Try a simple topic first to understand the workflow
2. Explore batch research for multiple topics
3. Integrate into your own applications
4. Customize for specific research domains

## 📞 Support

If you encounter issues:
1. Check QUICKSTART.md troubleshooting section
2. Review README.md for detailed documentation
3. Verify API key is set correctly
4. Ensure Python 3.8+ is installed

---

**Ready? Run:** `python research_agent.py` and start researching! 🔬
