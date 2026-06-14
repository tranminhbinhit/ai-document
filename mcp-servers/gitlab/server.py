"""
MCP GitLab Server - Tích hợp với GitLab
Hỗ trợ: Source code, Merge Requests, Pipelines
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
    import gitlab
except ImportError:
    print("Install: pip install python-gitlab")
    exit(1)

app = Server("mcp-gitlab-server")

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
DEFAULT_PROJECT_ID = os.getenv("DEFAULT_PROJECT_ID")

if not GITLAB_TOKEN:
    raise ValueError("GITLAB_TOKEN environment variable is required")

gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_merge_requests",
            description="Liệt kê các Merge Requests của project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "Project ID (optional, dùng default nếu không có)"},
                    "state": {"type": "string", "enum": ["opened", "closed", "merged", "all"], "default": "opened"}
                }
            }
        ),
        Tool(
            name="get_merge_request",
            description="Xem chi tiết một Merge Request",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "mr_iid": {"type": "integer", "description": "Merge Request IID"}
                },
                "required": ["mr_iid"]
            }
        ),
        Tool(
            name="get_mr_changes",
            description="Xem code changes trong MR",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "mr_iid": {"type": "integer"}
                },
                "required": ["mr_iid"]
            }
        ),
        Tool(
            name="list_pipelines",
            description="Liệt kê CI/CD pipelines",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["running", "pending", "success", "failed", "canceled"]}
                }
            }
        ),
        Tool(
            name="get_file_content",
            description="Đọc nội dung file từ repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "file_path": {"type": "string", "description": "Đường dẫn file trong repo"},
                    "ref": {"type": "string", "description": "Branch/tag name (default: main)", "default": "main"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="search_code",
            description="Search code trong repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {"type": "string"},
                    "search": {"type": "string", "description": "Từ khóa tìm kiếm"}
                },
                "required": ["search"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    try:
        project_id = arguments.get("project_id", DEFAULT_PROJECT_ID)
        
        if name == "list_merge_requests":
            return await handle_list_mrs(project_id, arguments)
        elif name == "get_merge_request":
            return await handle_get_mr(project_id, arguments)
        elif name == "get_mr_changes":
            return await handle_get_mr_changes(project_id, arguments)
        elif name == "list_pipelines":
            return await handle_list_pipelines(project_id, arguments)
        elif name == "get_file_content":
            return await handle_get_file(project_id, arguments)
        elif name == "search_code":
            return await handle_search_code(project_id, arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_list_mrs(project_id: str, args: dict) -> list[TextContent]:
    project = gl.projects.get(project_id)
    state = args.get("state", "opened")
    
    mrs = project.mergerequests.list(state=state, per_page=20)
    
    result = []
    for mr in mrs:
        result.append({
            "iid": mr.iid,
            "title": mr.title,
            "author": mr.author["name"],
            "state": mr.state,
            "created_at": mr.created_at,
            "web_url": mr.web_url
        })
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


async def handle_get_mr(project_id: str, args: dict) -> list[TextContent]:
    project = gl.projects.get(project_id)
    mr = project.mergerequests.get(args["mr_iid"])
    
    result = {
        "iid": mr.iid,
        "title": mr.title,
        "description": mr.description,
        "author": mr.author["name"],
        "state": mr.state,
        "source_branch": mr.source_branch,
        "target_branch": mr.target_branch,
        "web_url": mr.web_url
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


async def handle_get_mr_changes(project_id: str, args: dict) -> list[TextContent]:
    project = gl.projects.get(project_id)
    mr = project.mergerequests.get(args["mr_iid"])
    changes = mr.changes()
    
    result = []
    for change in changes["changes"]:
        result.append({
            "file": change["new_path"],
            "diff": change["diff"][:1000]  # Giới hạn để không quá dài
        })
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


async def handle_list_pipelines(project_id: str, args: dict) -> list[TextContent]:
    project = gl.projects.get(project_id)
    status = args.get("status")
    
    pipelines = project.pipelines.list(status=status, per_page=20) if status else project.pipelines.list(per_page=20)
    
    result = []
    for pipeline in pipelines:
        result.append({
            "id": pipeline.id,
            "status": pipeline.status,
            "ref": pipeline.ref,
            "created_at": pipeline.created_at,
            "web_url": pipeline.web_url
        })
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


async def handle_get_file(project_id: str, args: dict) -> list[TextContent]:
    project = gl.projects.get(project_id)
    file_path = args["file_path"]
    ref = args.get("ref", "main")
    
    file_content = project.files.get(file_path=file_path, ref=ref)
    content = file_content.decode().decode("utf-8")
    
    return [TextContent(type="text", text=content)]


async def handle_search_code(project_id: str, args: dict) -> list[TextContent]:
    project = gl.projects.get(project_id)
    search_term = args["search"]
    
    # GitLab search API
    results = project.search("blobs", search_term)
    
    output = []
    for result in results[:10]:  # Giới hạn 10 kết quả
        output.append({
            "filename": result["filename"],
            "path": result["path"],
            "ref": result["ref"]
        })
    
    return [TextContent(type="text", text=json.dumps(output, indent=2, ensure_ascii=False))]


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    
    asyncio.run(main())
