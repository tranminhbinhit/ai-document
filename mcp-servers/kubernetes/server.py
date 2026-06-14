"""
MCP Kubernetes Server - Monitor và debug K8s resources
Hỗ trợ: Logs, Pods, Deployments (Read-only)
"""

import os
import json
from typing import Any
from datetime import datetime

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
except ImportError:
    print("Install: pip install mcp")
    exit(1)

try:
    from kubernetes import client, config
except ImportError:
    print("Install: pip install kubernetes")
    exit(1)

app = Server("mcp-k8s-server")

DEFAULT_NAMESPACE = os.getenv("DEFAULT_NAMESPACE", "default")

# Load kubeconfig
try:
    config.load_kube_config()
except Exception:
    # Fallback to in-cluster config if running inside K8s
    config.load_incluster_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_pods",
            description="Liệt kê pods trong namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Namespace (default: configured default)"},
                    "label_selector": {"type": "string", "description": "Label selector (e.g., app=myapp)"}
                }
            }
        ),
        Tool(
            name="get_pod_logs",
            description="Xem logs của một pod",
            inputSchema={
                "type": "object",
                "properties": {
                    "pod_name": {"type": "string", "description": "Tên pod"},
                    "namespace": {"type": "string"},
                    "container": {"type": "string", "description": "Container name (nếu pod có nhiều containers)"},
                    "tail_lines": {"type": "integer", "description": "Số dòng log cuối (default: 100)", "default": 100},
                    "previous": {"type": "boolean", "description": "Lấy logs từ container trước (crashed)", "default": False}
                },
                "required": ["pod_name"]
            }
        ),
        Tool(
            name="describe_pod",
            description="Xem chi tiết một pod",
            inputSchema={
                "type": "object",
                "properties": {
                    "pod_name": {"type": "string"},
                    "namespace": {"type": "string"}
                },
                "required": ["pod_name"]
            }
        ),
        Tool(
            name="list_deployments",
            description="Liệt kê deployments",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            }
        ),
        Tool(
            name="get_deployment",
            description="Xem chi tiết deployment",
            inputSchema={
                "type": "object",
                "properties": {
                    "deployment_name": {"type": "string"},
                    "namespace": {"type": "string"}
                },
                "required": ["deployment_name"]
            }
        ),
        Tool(
            name="list_services",
            description="Liệt kê services",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"}
                }
            }
        ),
        Tool(
            name="get_events",
            description="Xem events trong namespace (useful để debug)",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "limit": {"type": "integer", "default": 20}
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    try:
        if name == "list_pods":
            return await handle_list_pods(arguments)
        elif name == "get_pod_logs":
            return await handle_get_logs(arguments)
        elif name == "describe_pod":
            return await handle_describe_pod(arguments)
        elif name == "list_deployments":
            return await handle_list_deployments(arguments)
        elif name == "get_deployment":
            return await handle_get_deployment(arguments)
        elif name == "list_services":
            return await handle_list_services(arguments)
        elif name == "get_events":
            return await handle_get_events(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_list_pods(args: dict) -> list[TextContent]:
    namespace = args.get("namespace", DEFAULT_NAMESPACE)
    label_selector = args.get("label_selector", "")
    
    pods = v1.list_namespaced_pod(namespace, label_selector=label_selector)
    
    result = []
    for pod in pods.items:
        result.append({
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "ready": sum(1 for c in pod.status.container_statuses or [] if c.ready),
            "total_containers": len(pod.spec.containers),
            "restarts": sum(c.restart_count for c in pod.status.container_statuses or []),
            "node": pod.spec.node_name,
            "age": str(datetime.now() - pod.metadata.creation_timestamp.replace(tzinfo=None))
        })
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]


async def handle_get_logs(args: dict) -> list[TextContent]:
    pod_name = args["pod_name"]
    namespace = args.get("namespace", DEFAULT_NAMESPACE)
    container = args.get("container")
    tail_lines = args.get("tail_lines", 100)
    previous = args.get("previous", False)
    
    logs = v1.read_namespaced_pod_log(
        name=pod_name,
        namespace=namespace,
        container=container,
        tail_lines=tail_lines,
        previous=previous
    )
    
    return [TextContent(type="text", text=logs)]


async def handle_describe_pod(args: dict) -> list[TextContent]:
    pod_name = args["pod_name"]
    namespace = args.get("namespace", DEFAULT_NAMESPACE)
    
    pod = v1.read_namespaced_pod(pod_name, namespace)
    
    result = {
        "name": pod.metadata.name,
        "namespace": pod.metadata.namespace,
        "labels": pod.metadata.labels,
        "status": {
            "phase": pod.status.phase,
            "conditions": [{"type": c.type, "status": c.status} for c in pod.status.conditions or []],
            "pod_ip": pod.status.pod_ip,
            "node": pod.spec.node_name
        },
        "containers": [
            {
                "name": c.name,
                "image": c.image,
                "ports": [{"containerPort": p.container_port, "protocol": p.protocol} for p in c.ports or []]
            }
            for c in pod.spec.containers
        ],
        "container_statuses": [
            {
                "name": cs.name,
                "ready": cs.ready,
                "restart_count": cs.restart_count,
                "state": str(cs.state)
            }
            for cs in pod.status.container_statuses or []
        ]
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]


async def handle_list_deployments(args: dict) -> list[TextContent]:
    namespace = args.get("namespace", DEFAULT_NAMESPACE)
    
    deployments = apps_v1.list_namespaced_deployment(namespace)
    
    result = []
    for deploy in deployments.items:
        result.append({
            "name": deploy.metadata.name,
            "namespace": deploy.metadata.namespace,
            "replicas": {
                "desired": deploy.spec.replicas,
                "ready": deploy.status.ready_replicas or 0,
                "available": deploy.status.available_replicas or 0
            },
            "age": str(datetime.now() - deploy.metadata.creation_timestamp.replace(tzinfo=None))
        })
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]


async def handle_get_deployment(args: dict) -> list[TextContent]:
    deployment_name = args["deployment_name"]
    namespace = args.get("namespace", DEFAULT_NAMESPACE)
    
    deploy = apps_v1.read_namespaced_deployment(deployment_name, namespace)
    
    result = {
        "name": deploy.metadata.name,
        "namespace": deploy.metadata.namespace,
        "replicas": {
            "desired": deploy.spec.replicas,
            "ready": deploy.status.ready_replicas or 0,
            "available": deploy.status.available_replicas or 0,
            "updated": deploy.status.updated_replicas or 0
        },
        "selector": deploy.spec.selector.match_labels,
        "template": {
            "containers": [
                {
                    "name": c.name,
                    "image": c.image
                }
                for c in deploy.spec.template.spec.containers
            ]
        }
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]


async def handle_list_services(args: dict) -> list[TextContent]:
    namespace = args.get("namespace", DEFAULT_NAMESPACE)
    
    services = v1.list_namespaced_service(namespace)
    
    result = []
    for svc in services.items:
        result.append({
            "name": svc.metadata.name,
            "namespace": svc.metadata.namespace,
            "type": svc.spec.type,
            "cluster_ip": svc.spec.cluster_ip,
            "ports": [{"port": p.port, "targetPort": p.target_port, "protocol": p.protocol} for p in svc.spec.ports or []]
        })
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]


async def handle_get_events(args: dict) -> list[TextContent]:
    namespace = args.get("namespace", DEFAULT_NAMESPACE)
    limit = args.get("limit", 20)
    
    events = v1.list_namespaced_event(namespace, limit=limit)
    
    result = []
    for event in events.items:
        result.append({
            "type": event.type,
            "reason": event.reason,
            "message": event.message,
            "object": f"{event.involved_object.kind}/{event.involved_object.name}",
            "count": event.count,
            "first_seen": str(event.first_timestamp),
            "last_seen": str(event.last_timestamp)
        })
    
    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    
    asyncio.run(main())
