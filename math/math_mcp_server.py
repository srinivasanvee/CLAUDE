"""
Math MCP Server

Exposes basic arithmetic operations (add, subtract, multiply, divide)
as MCP tools via the stdio transport.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math Server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together and return the result."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the result."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together and return the result."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    Divide a by b and return the result.

    Raises:
        ValueError: If b is zero (division by zero is undefined).
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    mcp.run()
