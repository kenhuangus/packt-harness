"""MCP 2.x Server Inspector."""
import asyncio
import sys

async def inspect():
    print("MCP 2.x Client stdio Inspector ready.")

if __name__ == "__main__":
    asyncio.run(inspect())
