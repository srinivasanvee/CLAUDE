import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

load_dotenv()

AMAZON_SHOPPING_INSTRUCTIONS = """
You are an expert Amazon shopping assistant. Help users find, compare, and purchase products on Amazon.com.

When given a shopping request, follow these steps:
1. Navigate to https://www.amazon.com
2. Use the search bar to search for the product the user wants
3. Analyze the search results based on:
   - Price match with user's budget (if specified)
   - Customer ratings (prefer 4+ stars)
   - Number of reviews (more reviews = more reliable)
   - Prime eligibility
   - Amazon's Choice or Best Seller badges
4. Open the top 2-3 candidate product pages to gather detailed information
5. Compare the options and clearly recommend the best match with reasoning
6. If the user wants to add an item to the cart:
   - Select the product and any required options (size, color, etc.)
   - Click "Add to Cart"
   - Confirm the item was added successfully
   - DO NOT proceed to checkout or enter payment details unless explicitly told to

Always:
- Be transparent about each action you are taking
- Ask for clarification if the request is ambiguous (e.g., unclear budget, brand preference)
- Warn the user before performing any cart or purchase actions
- Present a clear summary with: product name, price, rating, review count, and a direct link
- If no good match is found, say so and suggest alternatives
"""


async def run_shopping_agent(user_prompt: str) -> str:
    """Run the Amazon shopping agent with a given user prompt."""

    async with MCPServerStdio(
        name="Playwright Browser",
        params={
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
        },
        cache_tools_list=True,
    ) as playwright_server:

        agent = Agent(
            name="Amazon Shopping Agent",
            instructions=AMAZON_SHOPPING_INSTRUCTIONS,
            mcp_servers=[playwright_server],
            model="gpt-4o",
        )

        print(f"\n[Agent] Starting shopping session...")
        print(f"[Agent] Request: {user_prompt}\n")
        print("-" * 60)

        result = await Runner.run(
            agent,
            user_prompt,
            max_turns=30,
        )

        return result.final_output


async def main():
    """Interactive CLI entry point."""
    print("=" * 60)
    print("  Amazon Shopping Agent")
    print("  Powered by OpenAI Agents SDK + Playwright MCP")
    print("=" * 60)

    examples = [
        "Find me a laptop under $800 with good battery life",
        "Search for Sony WH-1000XM5 headphones and show me the best price",
        "Add the best-rated mechanical keyboard under $150 to my cart",
        "Compare the top 3 standing desks under $400",
    ]

    while True:
        print("\nExample prompts:")
        for ex in examples:
            print(f"  - {ex}")
        print("\nType 'quit' to exit.\n")

        user_prompt = input("What would you like to shop for? ").strip()

        if user_prompt.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if not user_prompt:
            print("Please enter a shopping request.")
            continue

        try:
            result = await run_shopping_agent(user_prompt)
            print("\n" + "=" * 60)
            print("SHOPPING RESULTS")
            print("=" * 60)
            print(result)
        except KeyboardInterrupt:
            print("\nShopping session interrupted.")
            break
        except Exception as e:
            print(f"\n[Error] {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
