# ************************ Basic mcp server ******************
# import random
# from fastmcp import FastMCP
# import json


# # create FastMCP server instance
# mcp= FastMCP(name='Simple Calculator Server')

# # Tool: Generate a random number
# @mcp.tool
# def random_number(min_val:int=1, max_val:int=100)-> int:
#     """
#     Generate a random number within a range.

#     Args:
#         min_val: Minimum value (default: 1)
#         max_val: Maxmum value (default: 100)
    
#     Returns:
#         A random integer between min_val and max_val

#     """
#     return random.randint(min_val, max_val)


# # Tool: add two numbers
# @mcp.tool
# def add_numbers(a:float, b:float)-> float:
#     """
#     Add two numbers together.

#     Args:
#         a: First number
#         b: second number
#     Return:
#         The sum of a and b
#     """
#     return a+b

# # Resource: server information
# @mcp.resource("info://server")
# def server_info()->str:
#     "Get information about this server."
#     info= {
#         "name": "Simple calculator Server",
#         "version": "1.0.0",
#         "description":"A basic MCP server with math tools",
#         "tools":["add_numbers","random_number" ],
#         "author": "Aditya Kumar"
#     }
#     return json.dumps(info, indent=2)


# # start the server
# if __name__ == "__main__":
#     # mcp.run() # only means we are seting transport "stdio"
#     mcp.run(transport='http', host='0.0.0.0', port= 8000) # for remote server we get to see changes here





#********************* Expense remote server ******************************

# from fastmcp import FastMCP
# import os
# import sqlite3
# import json

# DB_PATH= os.path.join(os.path.dirname(__file__), "expenses.db")
# CATEGORIES_PATH= os.path.join(os.path.dirname(__file__), "categories.json")

# mcp= FastMCP("ExpenseTracker")

# def init_db():
#     with sqlite3.connect(DB_PATH) as c: # c->onnection object 
#         c.execute(
#             """
#         CREATE TABLE IF NOT EXISTS expenses(
#             id  INTEGER PRIMARY KEY AUTOINCREMENT,
#             date TEXT NOT NULL,
#             amount REAL NOT NULL,
#             category TEXT NOT NULL,
#             subcategory TEXT DEFAULT '',
#             note TEXT DEFAULT ''
#         )

#             """
#         )

# init_db()

# @mcp.tool
# def add_expense(date, amount,category, subcategory="", note=""):
#     """ For adding new expense to the database """
#     with sqlite3.connect(DB_PATH) as c:
#         cur= c.execute(
#             "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
#             (date, amount, category, subcategory, note)
#         )
#         return {"status":"ok", "id": cur.lastrowid}
    
# @mcp.tool
# def list_expenses(start_date, end_date):
#     """ List all expenses from the database. """
#     with sqlite3.connect(DB_PATH) as c:
#         cur= c.execute(
#             """SELECT id, date, amount, category, subcategory, note 
#             FROM expenses 
#             WHERE date BETWEEN ? AND ?
#             ORDER BY id ASC""",
#             (start_date, end_date)
#         )
#         cols= [d[0] for d in cur.description]
#         return [dict(zip(cols, r)) for r in cur.fetchall()]


# @mcp.tool
# def summarize(start_date, end_date, category=None):
#     """Summarize expenses by category within an inclusive date range."""
#     with sqlite3.connect(DB_PATH) as c:
#         query= (
#             """
#             SELECT category, sum(amount) AS total_amount
#             from expenses
#             WHERE date between ? and ?
#             """
#         )

#         params= [start_date, end_date]
#         if category:
#             query+= "AND category= ?"
#             params.append(category)

#         query+= "GROUP BY category ORDER BY category ASC"

#         cur= c.execute(query, params)
#         cols= [d[0] for d in cur.description]
#         return [ dict(zip(cols, r)) for r in cur.fetchall()]
    

# @mcp.tool
# def edit_expense(id, date=None, amount=None, category=None, subcategory=None, note=None):
#     """ Edit expense by id """
#     with sqlite3.connect(DB_PATH) as c:
#         query= (
#             """ 
#             UPDATE expenses
#             SET
#             """
#         )
#         param=[]

#         if date:
#             query+="date=?"
#             param.append(date)
#         if amount:
#             if date:
#                 query+=",amount=?"
#             else:
#                 query+="amount=?"

#             param.append(amount)
#         if category:
#             if date or amount:
#                 query+=",category=?"
#             else:
#                 query+="category=?"

#             param.append(category)
#         if subcategory:
#             if date or amount or category:
#                 query+=",subcategory=?"
#             else:
#                 query+="subcategory=?"

#             param.append(subcategory)
#         if note:
#             if date or amount or category or note:
#                 query+=",note=?"
#             else:
#                 query+="note=?"

#             param.append(note)


#         query+= "WHERE id=?"
#         param.append(id)

#         cur= c.execute(query, param)
#         c.commit()

#         return {"status":"ok", "id":id}


# @mcp.tool
# def delete_expense(id):
#     """ Delete expense by id """
#     with sqlite3.connect(DB_PATH) as c:
#         cur= c.execute(
#             """
#             DELETE FROM expenses WHERE id= ?
#             """,
#             (id,)
#         )
#         if cur.rowcount==0:
#             return {"status":"error", "message":f"Expense {id} not found"}
#         c.commit()

    
#     return {"status":"ok", 'deleted_id':id}
        


    
# @mcp.resource("expense://categories", mime_type="application/json")
# def categories():
#     "Read fresh each time so you can edit the file without restarting"
#     with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
#         return f.read()



# # Resource: server information
# @mcp.resource("info://server")
# def server_info()->str:
#     "Get information about this server."
#     info= {
#         "name": "Simple calculator Server",
#         "version": "1.0.0",
#         "description":"A basic MCP server with math tools",
#         "tools":["add_numbers","random_number" ],
#         "author": "Aditya Kumar"
#     }
#     return json.dumps(info, indent=2)


# # start the server
# if __name__ == "__main__":
#     # mcp.run() # only means we are seting transport "stdio"
#     mcp.run(transport='http', host='0.0.0.0', port= 8000) # for remote server we get to see changes here




# *************** Solve first flow(mcp server is syncronus in the nature) ****************
from fastmcp import FastMCP
import os 
import aiosqlite  # changed: sqlite to aiosqlite
import tempfile
import asyncio
from typing import Union

# Use temporary directory which should be writable

TEMP_DIR= tempfile.gettempdir()
DB_PATH= os.path.join(TEMP_DIR, 'expenses.db')
CATEGORIES_PATH= os.path.join(os.path.dirname(__file__), "categories.json")

print(f"Database path: {DB_PATH}")

mcp= FastMCP('ExpenseTracker')


async def init_db(): # changed: add async
    try:
        # Changed: sqlite3.connect -> aiosqlite.connect
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
            """)
            await db.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise


# Initialize database at module level
# asyncio.run(init_db())


# Add Expense
@mcp.tool
async def add_expense(
    date: str,
    amount: Union[int,float,str],
    category: str,
    subcategory: str = "",
    note: str = ""
):
    await init_db()

    """Add a new expense."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """
            INSERT INTO expenses
            (date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (date, amount, category, subcategory, note)
        )

        await db.commit()

        return {
            "status": "ok",
            "id": cur.lastrowid
        }
    

# List expense

@mcp.tool
async def list_expenses(start_date: str, end_date: str):
    """List expenses between dates."""
    await init_db()

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cur = await db.execute(
            """
            SELECT id, date, amount,
                   category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )

        rows = await cur.fetchall()

        return [dict(row) for row in rows]
    
# Summarize
@mcp.tool
async def summarize(start_date: str,
                    end_date: str,
                    category: str | None = None):
    """Summarize expenses by category."""

    await init_db()

    query = """
        SELECT category,
               SUM(amount) AS total_amount
        FROM expenses
        WHERE date BETWEEN ? AND ?
    """

    params = [start_date, end_date]

    if category:
        query += " AND category = ?"
        params.append(category)

    query += """
        GROUP BY category
        ORDER BY category ASC
    """

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cur = await db.execute(query, params)
        rows = await cur.fetchall()

        return [dict(row) for row in rows]

# Delete Expense
@mcp.tool
async def delete_expense(id: int):
    """Delete expense by id."""

    await init_db()

    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM expenses WHERE id = ?",
            (id,)
        )

        await db.commit()

        if cur.rowcount == 0:
            return {
                "status": "error",
                "message": f"Expense {id} not found"
            }

        return {
            "status": "ok",
            "deleted_id": id
        }
    
    
# Dynamic UPDATE Query (Cleaner Version)

@mcp.tool
async def edit_expense(
    id: int,
    date: str | None = None,
    amount: float | None = None,
    category: str | None = None,
    subcategory: str | None = None,
    note: str | None = None,
):
    """Edit an expense."""

    await init_db()

    updates = []
    params = []

    fields = {
        "date": date,
        "amount": amount,
        "category": category,
        "subcategory": subcategory,
        "note": note,
    }

    for field, value in fields.items():
        if value is not None:
            updates.append(f"{field}=?")
            params.append(value)

    if not updates:
        return {
            "status": "error",
            "message": "No fields provided"
        }

    params.append(id)

    query = f"""
        UPDATE expenses
        SET {", ".join(updates)}
        WHERE id = ?
    """

    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(query, params)
        await db.commit()

        if cur.rowcount == 0:
            return {
                "status": "error",
                "message": f"Expense {id} not found"
            }

    return {
        "status": "ok",
        "id": id
    }

# Categories Resource
@mcp.resource(
    "expense://categories",
    mime_type="application/json"
)
async def categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()
    

# start the server
if __name__ == "__main__":
    # asyncio.run(init_db())
    # mcp.run() # only means we are seting transport "stdio"
    mcp.run(transport='http', host='0.0.0.0', port= 8000) # for remote server we get to see changes here
