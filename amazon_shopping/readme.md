Here's what was created under amazon_shopping/:

Files
main.py
The core agent. Key parts:

Part	Details
Agent instructions	System prompt that tells GPT-4o how to search, compare, filter, and optionally add to cart on Amazon
run_shopping_agent()	Spins up Playwright MCP via npx @playwright/mcp@latest, creates an Agent, and runs it with Runner.run()
main()	Interactive CLI loop — enter prompts, get results, type quit to exit
requirements.txt

openai-agents>=0.0.7
python-dotenv>=1.0.0
.env.example

OPENAI_API_KEY=your_openai_api_key_here
How to Run
1. Install Python deps:


pip install -r amazon_shopping/requirements.txt
2. Install Node (needed for Playwright MCP):


npm install -g @playwright/mcp@latest
npx playwright install chromium
3. Set your API key:


cp amazon_shopping/.env.example amazon_shopping/.env
# edit .env and add your OpenAI key
4. Run:


python amazon_shopping/main.py
How it Works

User prompt
    │
    ▼
OpenAI Agents SDK (GPT-4o)
    │  ← reasons about next steps
    ▼
Playwright MCP tools
  (navigate, click, type, screenshot, ...)
    │
    ▼
Amazon.com (real browser, visible by default)
    │
    ▼
Final structured result back to user
The agent is capped at max_turns=50 to handle multi-step flows like search → open product → compare → add to cart. It is instructed to stop before entering payment details unless explicitly told to proceed.

