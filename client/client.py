from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

model = ChatGroq(model="qwen-2.5-32b")

# server_params = StdioServerParameters(
#     command = r"C:\Users\saina\OneDrive\Desktop\Marathiaiml\Langchain MCP\.venv\Scripts\python.exe",
#     args = ["server\math_server.py"]
# )

async def main(input):
     async with MultiServerMCPClient(
        {
            "math": {
                "command": r"C:\Users\saina\OneDrive\Desktop\Marathiaiml\Langchain MCP\.venv\Scripts\python.exe",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["server\math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        agent_response = await agent.ainvoke({"messages": input})
        # weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
        return agent_response


'''
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read,write) as session:
            # Initialize the session
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            #Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages":input})
            return agent_response
'''
if __name__ == "__main__":
    input = "What is (3+5) * 3" # "what is the weather in nyc?"
    result = asyncio.run(main(input))
    # print(result)
    print(result['messages'][-1].content)


