"""
MCP SQL Server - Kết nối SQL Server (Read-only mode)
Hỗ trợ: Schema info, Queries
"""

import os
import json
from typing import Any

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
except ImportError:
    print("Install: pip install mcp")
    exit(1)

try:
    import pyodbc
except ImportError:
    print("Install: pip install pyodbc")
    print("Cần cài đặt ODBC Driver: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
    exit(1)

app = Server("mcp-sqlserver-server")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
READ_ONLY = os.getenv("READ_ONLY", "true").lower() == "true"


def get_connection():
    """Create SQL Server connection with proper error handling"""
    # Validate credentials
    if not all([SQL_SERVER, SQL_DATABASE, SQL_USER, SQL_PASSWORD]):
        missing = []
        if not SQL_SERVER: missing.append("SQL_SERVER")
        if not SQL_DATABASE: missing.append("SQL_DATABASE")
        if not SQL_USER: missing.append("SQL_USER")
        if not SQL_PASSWORD: missing.append("SQL_PASSWORD")
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")
    
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USER};"
        f"PWD={SQL_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    
    # Note: pyodbc doesn't have readonly parameter
    # We enforce read-only at query level
    return pyodbc.connect(conn_str, timeout=30)


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_tables",
            description="Liệt kê tất cả tables trong database",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="describe_table",
            description="Xem cấu trúc của một table (columns, types, constraints)",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Tên table"}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="get_table_relationships",
            description="Xem foreign key relationships của table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string"}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="query_readonly",
            description="Thực thi SELECT query (read-only mode)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL SELECT query"},
                    "limit": {"type": "integer", "description": "Giới hạn số rows trả về (default: 100)", "default": 100}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_table_sample",
            description="Lấy sample data từ table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["table_name"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    try:
        if name == "list_tables":
            return await handle_list_tables()
        elif name == "describe_table":
            return await handle_describe_table(arguments)
        elif name == "get_table_relationships":
            return await handle_get_relationships(arguments)
        elif name == "query_readonly":
            return await handle_query(arguments)
        elif name == "get_table_sample":
            return await handle_get_sample(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_list_tables() -> list[TextContent]:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            TABLE_SCHEMA,
            TABLE_NAME,
            TABLE_TYPE
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_SCHEMA, TABLE_NAME
    """
    
    cursor.execute(query)
    tables = []
    for row in cursor.fetchall():
        tables.append({
            "schema": row[0],
            "name": row[1],
            "type": row[2]
        })
    
    conn.close()
    return [TextContent(type="text", text=json.dumps(tables, indent=2))]


async def handle_describe_table(args: dict) -> list[TextContent]:
    table_name = args["table_name"]
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
    """
    
    cursor.execute(query, table_name)
    columns = []
    for row in cursor.fetchall():
        columns.append({
            "name": row[0],
            "type": row[1],
            "max_length": row[2],
            "nullable": row[3],
            "default": row[4]
        })
    
    conn.close()
    return [TextContent(type="text", text=json.dumps(columns, indent=2))]


async def handle_get_relationships(args: dict) -> list[TextContent]:
    table_name = args["table_name"]
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT
            fk.name AS constraint_name,
            OBJECT_NAME(fk.parent_object_id) AS table_name,
            COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS column_name,
            OBJECT_NAME(fk.referenced_object_id) AS referenced_table,
            COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS referenced_column
        FROM sys.foreign_keys fk
        INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        WHERE OBJECT_NAME(fk.parent_object_id) = ?
    """
    
    cursor.execute(query, table_name)
    relationships = []
    for row in cursor.fetchall():
        relationships.append({
            "constraint": row[0],
            "table": row[1],
            "column": row[2],
            "references_table": row[3],
            "references_column": row[4]
        })
    
    conn.close()
    return [TextContent(type="text", text=json.dumps(relationships, indent=2))]


async def handle_query(args: dict) -> list[TextContent]:
    query = args["query"].strip()
    limit = args.get("limit", 100)
    
    # Security: Chỉ cho phép SELECT
    if not query.upper().startswith("SELECT"):
        return [TextContent(type="text", text="Error: Only SELECT queries are allowed")]
    
    # Thêm TOP clause nếu chưa có
    if "TOP" not in query.upper():
        query = query.replace("SELECT", f"SELECT TOP {limit}", 1)
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Get column names
    columns = [column[0] for column in cursor.description]
    
    # Get rows
    rows = []
    for row in cursor.fetchall():
        rows.append(dict(zip(columns, row)))
    
    result = {
        "columns": columns,
        "row_count": len(rows),
        "data": rows
    }
    
    conn.close()
    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False, default=str))]


async def handle_get_sample(args: dict) -> list[TextContent]:
    table_name = args["table_name"]
    limit = args.get("limit", 10)
    
    query = f"SELECT TOP {limit} * FROM {table_name}"
    return await handle_query({"query": query, "limit": limit})


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    
    asyncio.run(main())
