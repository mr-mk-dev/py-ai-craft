# 05 - MCP Server Implementation: Low-Level SDK, FastMCP & Transports

> **Mental Model**:  
> Think of an MCP Server like a **sovereign diplomatic embassy**:  
> * **The Decoupled Micro-Service**: An MCP Server is a standalone, isolated software process. It doesn't care whether the client on the other end is Claude Desktop, Cursor, Antigravity, or an internal microservice.  
> * **The Diplomatic Cables (Transports)**: It receives incoming JSON-RPC requests via local standard input/output (**`stdio`**) or over remote cloud networks (**`SSE / HTTP`**).  
> * It maintains its own private database connection pools, validates caller arguments, executes tools safely, and returns standardized response envelopes.

---

## 📑 Table of Contents
1. [Low-Level SDK vs. High-Level FastMCP](#1-low-level-sdk-vs-high-level-fastmcp)
2. [The stdio Subprocess Transport (Zero-Latency Local)](#2-the-stdio-subprocess-transport-zero-latency-local)
3. [The SSE / HTTP Remote Transport (Cloud Microservices)](#3-the-sse--http-remote-transport-cloud-microservices)
4. [Server Lifespan & Persistent Connection Pools](#4-server-lifespan--persistent-connection-pools)
5. [Connecting to Claude Desktop & Cursor (Config Integration)](#5-connecting-to-claude-desktop--cursor-config-integration)
6. [Building a Dual-Transport Production MCP Server in Python](#6-building-a-dual-transport-production-mcp-server-in-python)
7. [Master Cheat Sheet & Reference Table](#7-master-cheat-sheet--reference-table)

---

## 1. Low-Level SDK vs. High-Level FastMCP

The official Python MCP library provides **two implementation tiers**:

```mermaid
flowchart TD
    Choice["Choosing Your MCP Server Framework"]
    
    Choice --> Low["<b>Low-Level SDK (<code>mcp.server.lowlevel.Server</code>)</b><br>• Manual <code>list_tools</code> & <code>call_tool</code> handler dispatch<br>• Explicit control over capability negotiation & raw JSON-RPC<br>• <i>Best for: Custom gateways, enterprise proxy middleware</i>"]
    
    Choice --> Fast["<b>High-Level FastMCP (<code>from mcp.server.fastmcp import FastMCP</code>)</b><br>• Pythonic decorators (<code>@mcp.tool()</code>, <code>@mcp.resource()</code>)<br>• Automatic Pydantic schema generation & docstring parsing<br>• <i>Best for: 95% of production tools, APIs, and microservices</i>"]
```

---

## 2. The `stdio` Subprocess Transport (Zero-Latency Local)

In `stdio` transport, the Host application (e.g. Claude Desktop or Cursor) **spawns your Python script as a child process**:

```mermaid
flowchart LR
    Host["Host Application (Parent Process)"] 
    <-->|stdin / stdout (Pipe)| 
    Server["Python MCP Server (Child Process)<br><code>python server.py</code>"]
```

> ⚠️ **The Cardinal Rule of stdio Servers:**  
> **NEVER write `print("debug log")` to standard output!**  
> `print()` pollutes `stdout`, which corrupts the JSON-RPC wire parser. Always use `sys.stderr.write()` or Python's standard `logging` module!

---

## 3. The `SSE / HTTP` Remote Transport (Cloud Microservices)

For cloud deployments where tools run on AWS/GCP, MCP uses **Server-Sent Events (SSE)**:

```mermaid
sequenceDiagram
    autonumber
    participant Client as MCP Client (Remote)
    participant Gateway as FastAPI MCP Server (Port 8000)

    Client->>Gateway: `GET /sse` (Establishes SSE stream for push events)
    Gateway-->>Client: Returns `endpoint: /messages?session_id=abc`
    
    Client->>Gateway: `POST /messages?session_id=abc` (JSON-RPC Request: `tools/call`)
    Gateway-->>Client: Emits JSON-RPC Response over the open `/sse` stream!
```

---

## 4. Server Lifespan & Persistent Connection Pools

Never connect to PostgreSQL or Redis on every tool call. Initialize connection pools during **Server Startup**:

```mermaid
flowchart TD
    Boot["Server Process Startup"] --> LifespanStart["<b>Lifespan Startup Hook:</b><br>• Initialize async PostgreSQL connection pool<br>• Warm up in-memory vector cache"]
    
    LifespanStart --> Serve["Active MCP Request Handling (Reusing warm connection pool!)"]
    
    Serve --> Shutdown["Host Disconnects / SIGINT"]
    Shutdown --> LifespanEnd["<b>Lifespan Teardown Hook:</b><br>• Gracefully close all DB connections & flush logs"]
```

---

## 5. Connecting to Claude Desktop & Cursor (Config Integration)

To connect Claude Desktop or Cursor to your local MCP server, add this entry to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "enterprise_db_server": {
      "command": "python",
      "args": [
        "/home/user2/PythonProject/Python-for-ai-engineering/08-mcp-a2a/05-mcp-server/server.py"
      ],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/proddb",
        "ENVIRONMENT": "production"
      }
    }
  }
}
```

---

## 6. Building a Dual-Transport Production MCP Server in Python

Here is a complete, production-grade MCP server supporting both **`stdio` (Local)** and **`sse` (Cloud HTTP)** modes:

```python
from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
import sys
import os

# --- 1. Lifespan Connection Pool Management ---
@asynccontextmanager
async def server_lifespan(server: FastMCP):
    sys.stderr.write("🚀 [LIFESPAN] Initializing database connection pool...\n")
    # Simulated connection pool setup
    db_pool = {"connected": True, "active_sessions": 0}
    
    yield {"db": db_pool} # State available to tools
    
    sys.stderr.write("🛑 [LIFESPAN] Gracefully draining database pool...\n")

# --- 2. Initialize FastMCP with Lifespan ---
mcp = FastMCP("enterprise_production_server", lifespan=server_lifespan)

# --- 3. Production Tools ---
@mcp.tool()
def get_cluster_health() -> dict:
    """Check Kubernetes cluster and database health metrics."""
    return {
        "status": "HEALTHY",
        "cpu_usage_pct": 34.2,
        "memory_free_mb": 4096,
        "db_latency_ms": 1.8
    }

@mcp.tool()
def query_financial_metrics(quarter: str, metric: str) -> dict:
    """Retrieve financial KPIs for a specific quarter.
    
    Args:
        quarter: Financial quarter, e.g. 'Q1', 'Q2', 'Q3', 'Q4'.
        metric: Target KPI name, e.g. 'revenue', 'churn_rate', 'ebitda'.
    """
    sys.stderr.write(f"🔍 [LOG] Querying metric '{metric}' for quarter '{quarter}'\n")
    return {
        "quarter": quarter.upper(),
        "metric": metric.lower(),
        "value": 14200000.00,
        "currency": "USD"
    }

# --- 4. Switchable Transport Runner ---
if __name__ == "__main__":
    # Check if run as cloud web service or local stdio
    transport_mode = os.getenv("MCP_TRANSPORT", "stdio").lower()
    
    if transport_mode == "sse":
        sys.stderr.write("🌐 Starting FastMCP on SSE / HTTP (Port 8000)...\n")
        mcp.run(transport="sse", host="0.0.0.0", port=8000)
    else:
        sys.stderr.write("⚡ Starting FastMCP on stdio pipe...\n")
        mcp.run(transport="stdio")
```

---

## 7. Master Cheat Sheet & Reference Table

| Transport / Flag | Setting | Recommended Usage |
| :--- | :--- | :--- |
| **`transport="stdio"`** | Standard In/Out | Local IDEs (Cursor, Claude Desktop, Antigravity). |
| **`transport="sse"`** | HTTP + SSE stream | Multi-tenant cloud deployments & remote microservices. |
| **Logging Rule** | Use `sys.stderr.write` | **Never write plain `print()` to stdout in stdio mode.** |
| **Lifespan Context** | `@asynccontextmanager` | Manage persistent DB pools and cleanup on shutdown. |

---

## 🎯 Next Step in Phase 8
Now that you have mastered building production MCP servers, we will advance to **[06 - MCP Client](file:///home/user2/PythonProject/Python-for-ai-engineering/08-mcp-a2a/06-mcp-client)** to master building programmatic Python MCP clients that connect to servers, inspect schemas, and execute tools in autonomous loops!
