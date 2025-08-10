from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"],
                "transport":"stdio",
            },

            "weather":{
                "url":"http://localhost:8000/mcp",
                "args":["weather.py"],
                "transport":"streamable-http",
            }
        }
    )

    import os
    GROQ_API_KEY="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"

    tools=await client.get_tools()
    model=ChatGroq(model="qwen/qwen3-32b")
    agent=create_react_agent(
        model,tools
    )

    math_response=await agent.invoke(
        {"messages": [{"role":"user","content":"What is 2+2?"}]}
    )

    print("Math Response:",math_response["messages"][-1]["content"])

asyncio.run(main())