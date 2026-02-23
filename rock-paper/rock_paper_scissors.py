import asyncio

from agents import Agent, Runner, ItemHelpers, trace

# --- Player Agents ---

player_1 = Agent(
    name="Player 1 - Rocky",
    instructions=(
        "You are playing Rock-Paper-Scissors. "
        "You are an aggressive player who loves bold moves. "
        "When asked to make a move, respond with EXACTLY one word: "
        "either 'rock', 'paper', or 'scissors'. Nothing else."
    ),
)

player_2 = Agent(
    name="Player 2 - Clippy",
    instructions=(
        "You are playing Rock-Paper-Scissors. "
        "You are a strategic, calculating player who tries to outsmart opponents. "
        "When asked to make a move, respond with EXACTLY one word: "
        "either 'rock', 'paper', or 'scissors'. Nothing else."
    ),
)

# --- Judge Agent ---

judge = Agent(
    name="Judge",
    instructions=(
        "You are the judge of a Rock-Paper-Scissors game. "
        "You will receive the moves of two players. "
        "Determine the winner based on these rules:\n"
        "- Rock beats Scissors\n"
        "- Scissors beats Paper\n"
        "- Paper beats Rock\n"
        "- Same move is a tie\n\n"
        "Announce the result in an entertaining way. "
        "End your response with exactly one of these lines:\n"
        "RESULT: PLAYER 1 WINS\n"
        "RESULT: PLAYER 2 WINS\n"
        "RESULT: TIE"
    ),
)


def parse_move(output: str) -> str:
    """Extract a valid move from agent output."""
    output_lower = output.strip().lower()
    for move in ("rock", "paper", "scissors"):
        if move in output_lower:
            return move
    return output_lower


def parse_result(judge_output: str) -> str:
    """Extract the result line from judge output."""
    for line in judge_output.strip().splitlines():
        line = line.strip().upper()
        if line.startswith("RESULT:"):
            if "PLAYER 1" in line:
                return "player1"
            elif "PLAYER 2" in line:
                return "player2"
            elif "TIE" in line:
                return "tie"
    return "tie"


async def play_round(round_num: int) -> str:
    """Play a single round of Rock-Paper-Scissors."""
    prompt = f"Round {round_num}: Make your move!"

    with trace(f"Round {round_num}"):
        # Run both players in parallel — neither can see the other's move
        result_1, result_2 = await asyncio.gather(
            Runner.run(player_1, prompt),
            Runner.run(player_2, prompt),
        )

        move_1 = parse_move(result_1.final_output)
        move_2 = parse_move(result_2.final_output)

        print(f"\n--- Round {round_num} ---")
        print(f"Player 1 (Rocky):  {move_1}")
        print(f"Player 2 (Clippy): {move_2}")

        # Judge evaluates the round
        judge_input = (
            f"Round {round_num} results:\n"
            f"Player 1 chose: {move_1}\n"
            f"Player 2 chose: {move_2}\n\n"
            "Who wins?"
        )
        judge_result = await Runner.run(judge, judge_input)

        print(f"\nJudge: {judge_result.final_output}")

    return parse_result(judge_result.final_output)


async def main():
    print("=" * 50)
    print("  ROCK-PAPER-SCISSORS: AI AGENT SHOWDOWN")
    print("  Player 1: Rocky (aggressive)")
    print("  Player 2: Clippy (strategic)")
    print("  Judge: The Honorable AI")
    print("=" * 50)

    scores = {"player1": 0, "player2": 0, "tie": 0}
    num_rounds = 1

    for round_num in range(1, num_rounds + 1):
        result = await play_round(round_num)
        scores[result] += 1

    # Final scoreboard
    print("\n" + "=" * 50)
    print("  FINAL SCOREBOARD")
    print("=" * 50)
    print(f"  Player 1 (Rocky):  {scores['player1']} wins")
    print(f"  Player 2 (Clippy): {scores['player2']} wins")
    print(f"  Ties:              {scores['tie']}")
    print()

    if scores["player1"] > scores["player2"]:
        print("  CHAMPION: Player 1 (Rocky)!")
    elif scores["player2"] > scores["player1"]:
        print("  CHAMPION: Player 2 (Clippy)!")
    else:
        print("  IT'S A DRAW!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
