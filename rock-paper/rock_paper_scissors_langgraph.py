import operator
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import END, START, StateGraph


# --- State ---

class GameState(TypedDict):
    round_num: int
    player1_move: str
    player2_move: str
    judge_verdict: str
    scores: dict
    log: Annotated[list[str], operator.add]


# --- LLM ---

llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)


# --- Helper ---

def parse_move(text: str) -> str:
    text_lower = text.strip().lower()
    for move in ("rock", "paper", "scissors"):
        if move in text_lower:
            return move
    return text_lower


# --- Node Functions ---

def player1_node(state: GameState) -> dict:
    """Player 1 (Rocky) — aggressive personality."""
    response = llm.invoke([
        SystemMessage(content=(
            "You are playing Rock-Paper-Scissors. "
            "You are an aggressive player who loves bold moves. "
            "Respond with EXACTLY one word: rock, paper, or scissors."
        )),
        HumanMessage(content=f"Round {state['round_num']}: Make your move!"),
    ])
    move = parse_move(response.content)
    return {"player1_move": move}


def player2_node(state: GameState) -> dict:
    """Player 2 (Clippy) — strategic personality."""
    response = llm.invoke([
        SystemMessage(content=(
            "You are playing Rock-Paper-Scissors. "
            "You are a strategic, calculating player who tries to outsmart opponents. "
            "Respond with EXACTLY one word: rock, paper, or scissors."
        )),
        HumanMessage(content=f"Round {state['round_num']}: Make your move!"),
    ])
    move = parse_move(response.content)
    return {"player2_move": move}


def judge_node(state: GameState) -> dict:
    """Judge evaluates both moves and declares a winner."""
    p1 = state["player1_move"]
    p2 = state["player2_move"]

    response = llm.invoke([
        SystemMessage(content=(
            "You are the judge of a Rock-Paper-Scissors game. "
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
        )),
        HumanMessage(content=(
            f"Round {state['round_num']} results:\n"
            f"Player 1 chose: {p1}\n"
            f"Player 2 chose: {p2}\n\n"
            "Who wins?"
        )),
    ])

    verdict = response.content
    # Parse result and update scores
    scores = dict(state["scores"])
    result_line = ""
    for line in verdict.strip().splitlines():
        upper = line.strip().upper()
        if upper.startswith("RESULT:"):
            result_line = upper
            break

    if "PLAYER 1" in result_line:
        scores["player1"] = scores.get("player1", 0) + 1
    elif "PLAYER 2" in result_line:
        scores["player2"] = scores.get("player2", 0) + 1
    else:
        scores["tie"] = scores.get("tie", 0) + 1

    round_log = (
        f"\n--- Round {state['round_num']} ---\n"
        f"Player 1 (Rocky):  {p1}\n"
        f"Player 2 (Clippy): {p2}\n"
        f"\nJudge: {verdict}"
    )

    return {"judge_verdict": verdict, "scores": scores, "log": [round_log]}


# --- Build the Graph ---

workflow = StateGraph(GameState)

# Add nodes
workflow.add_node("player1", player1_node)
workflow.add_node("player2", player2_node)
workflow.add_node("judge", judge_node)

# Edges: START -> both players in parallel -> judge -> END
workflow.add_edge(START, "player1")
workflow.add_edge(START, "player2")
workflow.add_edge("player1", "judge")
workflow.add_edge("player2", "judge")
workflow.add_edge("judge", END)

# Compile
graph = workflow.compile()


# --- Game Loop ---

def main():
    print("=" * 50)
    print("  ROCK-PAPER-SCISSORS: LANGGRAPH AGENT SHOWDOWN")
    print("  Player 1: Rocky (aggressive)")
    print("  Player 2: Clippy (strategic)")
    print("  Judge: The Honorable AI")
    print("=" * 50)

    num_rounds = 3
    scores = {"player1": 0, "player2": 0, "tie": 0}

    for round_num in range(1, num_rounds + 1):
        result = graph.invoke({
            "round_num": round_num,
            "player1_move": "",
            "player2_move": "",
            "judge_verdict": "",
            "scores": scores,
            "log": [],
        })

        # Print round log
        for entry in result["log"]:
            print(entry)

        scores = result["scores"]

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
    main()
