"""
GCP CloudOps Lens - Phase 1 MCP Server
Minimal milestone: one tool, discover_resources(), backed by Cloud Asset Inventory.

Written for mcp SDK v2.0.0+ (uses MCPServer, the renamed FastMCP).
If you're on mcp<2.0, use: from mcp.server.fastmcp import FastMCP as MCPServer instead.

Run with:
    python server.py

Requires:
    pip install mcp google-cloud-asset
    gcloud auth application-default login
"""

from google.cloud import asset_v1
from mcp.server.mcpserver import MCPServer

# ---- CONFIG ----
PROJECT_ID = "project-c98d2dac-2409-44bd-aba"
PROJECT_RESOURCE = f"projects/{PROJECT_ID}"

mcp = MCPServer("gcp-cloudops-lens")


@mcp.tool()
def discover_resources() -> str:
    """Discover all resources currently running in the GCP project using
    Cloud Asset Inventory. Returns resources grouped by type (Compute Engine,
    GKE, Cloud Run, Cloud SQL, Storage, etc.)."""
    client = asset_v1.AssetServiceClient()

    request = asset_v1.ListAssetsRequest(
        parent=PROJECT_RESOURCE,
        content_type=asset_v1.ContentType.RESOURCE,
        page_size=500,
    )

    grouped = {}
    try:
        for asset in client.list_assets(request=request):
            asset_type = asset.asset_type
            name = asset.name.split("/")[-1]
            grouped.setdefault(asset_type, []).append(name)
    except Exception as e:
        return f"Error querying Cloud Asset Inventory: {e}"

    if not grouped:
        return (
            f"No resources found in project '{PROJECT_ID}'. "
            "(Project may be empty, or Asset Inventory API may still be "
            "propagating — can take a few minutes after first enabling.)"
        )

    lines = [f"Found resources in project '{PROJECT_ID}':\n"]
    total = 0
    for asset_type, names in sorted(grouped.items()):
        lines.append(f"\n{asset_type} ({len(names)}):")
        for n in names:
            lines.append(f"  - {n}")
        total += len(names)

    lines.append(f"\n\nTotal resources: {total}")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport
