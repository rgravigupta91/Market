from fastmcp import FastMCP
from main import app

# Create MCP Server from Fast API
mcp = FastMCP.from_fastapi(
    app=app,
    name='DeepTicker'
)

if __name__ == "main":
    mcp.run()