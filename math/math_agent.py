"""
Math Agent - OpenAI Agents SDK + MCP

Connects to the Math MCP server (math_mcp_server.py) via stdio transport
and uses GPT-4o to answer math questions using the server's tools.
"""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

load_dotenv()

MODEL = "gpt-4o"

MATH_SERVER_PATH = Path(__file__).parent / "math_mcp_server.py"

MATH_AGENT_INSTRUCTIONS = """You are a precise math assistant. You have access to four arithmetic tools:
- add(a, b)      — addition
- subtract(a, b) — subtraction
- multiply(a, b) — multiplication
- divide(a, b)   — division

Always use the appropriate tool(s) to compute the answer. Show each tool call you make and
present the final result clearly. For multi-step problems, chain the tools one at a time."""


async def run_math_agent(query: str) -> str:
    """Start the Math MCP server, run the agent, return the final answer."""
    async with MCPServerStdio(
        name="Math Server",
        params={
            "command": sys.executable,
            "args": [str(MATH_SERVER_PATH)],
        },
        cache_tools_list=True,
    ) as mcp_server:
        agent = Agent(
            name="Math Assistant",
            model=MODEL,
            instructions=MATH_AGENT_INSTRUCTIONS,
            mcp_servers=[mcp_server],
        )
        result = await Runner.run(agent, query)
        return result.final_output


def main():
    print("=" * 60)
    print("MATH AGENT — OpenAI Agents SDK + MCP")
    print(f"Model: {MODEL}  |  Tools: Math MCP Server (stdio)")
    print("=" * 60)
    print("Examples: '12 + 7', '(3 * 8) - 5', '100 / 4 + 6'\n")

    while True:
        query = input("Math problem (or 'quit' to exit): ").strip()

        if not query:
            continue
        if query.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        try:
            answer = asyncio.run(run_math_agent(query))
            print(f"\nAnswer: {answer}\n")
        except Exception as e:
            print(f"\n[ERROR] {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
