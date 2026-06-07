# ************************ Basic mcp server ******************
import random
from fastmcp import FastMCP
import json


# create FastMCP server instance
mcp= FastMCP(name='Simple Calculator Server')

# Tool: Generate a random number
@mcp.tool
def random_number(min_val:int=1, max_val:int=100)-> int:
    """
    Generate a random number within a range.

    Args:
        min_val: Minimum value (default: 1)
        max_val: Maxmum value (default: 100)
    
    Returns:
        A random integer between min_val and max_val

    """
    return random.randint(min_val, max_val)


# Tool: add two numbers
@mcp.tool
def add_numbers(a:float, b:float)-> float:
    """
    Add two numbers together.

    Args:
        a: First number
        b: second number
    Return:
        The sum of a and b
    """
    return a+b

# Resource: server information
@mcp.resource("info://server")
def server_info()->str:
    "Get information about this server."
    info= {
        "name": "Simple calculator Server",
        "version": "1.0.0",
        "description":"A basic MCP server with math tools",
        "tools":["add_numbers","random_number" ],
        "author": "Aditya Kumar"
    }
    return json.dumps(info, indent=2)


# start the server
if __name__ == "__main__":
    # mcp.run() # only means we are seting transport "stdio"
    mcp.run(transport='http', host='0.0.0.0', port= 8000) # for remote server we get to see changes here
