# 02 - MCP Tools: Dynamic Function Exposure & Execution Handlers

> **Mental Model**:  
> Think of MCP Tools like **smart home appliances plugging into a universal wall socket**:  
> * **Standard Function Calling (Hardcoded Coupling)**: Your Python backend must write, import, and execute the function in the same codebase. If you want to share that function with Claude Desktop or Cursor, you have to rewrite the connector from scratch!  
> * **MCP Tools (Decoupled Micro-Servers)**: The tool runs inside an independent process. It announces its name, parameters, and return types over **`tools/list`**.  
> * Any MCP-compliant AI client plugs into the socket, discovers the tool dynamically, and triggers execution over **`tools/call`** with zero code duplication!

---

## 📑 Table of Contents
1. [Monolithic Function Calling vs. MCP Micro-Tools](#1-monolithic-function-calling-vs-mcp-micro-tools)
2. [The JSON-RPC Wire Protocol: tools/list & tools/call](#2-the-json-rpc-wire-protocol-toolslist--toolscall)
3. [Multi-Modal Return Content (Text, Images & Binary)](#3-multi-modal-return-content-text-images--binary)
4. [Error Reporting: isError Flags vs. JSON-RPC Protocol Errors](#4-error-reporting-iserror-flags-vs-json-rpc-protocol-errors)
5. [Building a Production Multi-Modal MCP Tool Server in Python](#5-building-a-production-multi-modal-mcp-tool-server-in-python)
6. [Master Cheat Sheet & Reference Table](#6-master-cheat-sheet--reference-table)

---

## 1. Monolithic Function Calling vs. MCP Micro-Tools

```mermaid
flowchart TD
    subgraph Monolith["❌ Traditional Function Calling (Tight Coupling)"]
        App1["FastAPI Backend"] --> F1["Hardcoded Python Func"]
        ClaudeDesktop["Claude Desktop"] -.->|Cannot Access!| F1
    end

    subgraph MCPWorld["✅ MCP Tool Server (Universal Dynamic Access)"]
        Server["<b>Database MCP Server Process</b><br>Exposes <code>query_database</code> over JSON-RPC"]
        
        Client1["FastAPI Backend"] -->|MCP Client| Server
        Client2["Claude Desktop"] -->|MCP Client| Server
        Client3["Cursor IDE"] -->|MCP Client| Server
    end
```

---

## 2. The JSON-RPC Wire Protocol: `tools/list` & `tools/call`

Under the hood, all MCP tool interactions use two primary JSON-RPC 2.0 methods:

```mermaid
sequenceDiagram
    autonumber
    participant Host as AI Host (Client)
    participant Server as MCP Server

    Note over Host,Server: 1. Discovery Phase
    Host->>Server: `{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}`
    Server-->>Host: `{"tools": [{"name": "fetch_user", "inputSchema": {...}}]}`

    Note over Host,Server: 2. Execution Phase
    Host->>Server: `{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "fetch_user", "arguments": {"user_id": 101}}}`
    Server-->>Host: `{"content": [{"type": "text", "text": "{\"name\": \"Alice\"}"}], "isError": false}`
```

### 1️⃣ `tools/list` Schema Specification:
```json
{
  "name": "generate_report",
  "description": "Generates a quarterly financial revenue report.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "quarter": { "type": "string", "enum": ["Q1", "Q2", "Q3", "Q4"] },
      "year": { "type": "integer", "default": 2026 }
    },
    "required": ["quarter"]
  }
}
```

---

## 3. Multi-Modal Return Content (Text, Images & Binary)

MCP tool returns are **not restricted to plain strings**—they return an array of **Content Blocks**:

```mermaid
flowchart TD
    ToolResult["MCP Tool Result (content array)"]
    
    ToolResult --> C1["<b>1. TextContent (<code>type: 'text'</code>)</b><br>JSON data, markdown tables, raw logs, or status strings"]
    
    ToolResult --> C2["<b>2. ImageContent (<code>type: 'image'</code>)</b><br>Base64-encoded charts, plots, and UI screenshots (PNG / JPEG)"]
    
    ToolResult --> C3["<b>3. EmbeddedResource (<code>type: 'resource'</code>)</b><br>Full document files, database snapshots, or text streams"]
```

---

## 4. Error Reporting: `isError` Flags vs. JSON-RPC Protocol Errors

MCP strictly separates **Protocol Failures** from **Tool Business Logic Failures**:

```mermaid
flowchart TD
    Request["Incoming Tool Call"] --> CheckProto{"Is JSON valid and Tool registered?"}
    
    CheckProto -- No --> ProtoErr["<b>❌ JSON-RPC Protocol Error (-32601)</b><br>Tool not found or malformed JSON envelope"]
    
    CheckProto -- Yes --> Exec{"Execute Tool Logic in Python"}
    
    Exec -- "Success" --> Success["<b>✅ Success Payload</b><br><code>result: {'content': [...], 'isError': False}</code>"]
    Exec -- "Domain Failure" --> AppErr["<b>🟡 Application Error (isError: True)</b><br><code>result: {'content': [{'type': 'text', 'text': 'User not found'}], 'isError': True}</code><br><i>LLM understands the error and gracefully responds to user!</i>"]
```

### Error Comparison:

| Error Type | Transport Level | `isError` Flag | Example Trigger |
| :--- | :--- | :---: | :--- |
| **Protocol Error** | JSON-RPC Level (`error: {...}`) | N/A | Unknown tool name, invalid JSON-RPC version. |
| **Tool Execution Error** | Application Level (`result: {...}`) | **`isError: true`** | Invalid database ID, insufficient balance, API timeout. |

---

## 5. Building a Production Multi-Modal MCP Tool Server in Python

Here is a complete, runnable script using the official **FastMCP** framework exposing text and image tools:

```python
from mcp.server.fastmcp import FastMCP, Image
from typing import Literal
import base64
import io

# 1. Initialize FastMCP Server
mcp = FastMCP("enterprise_tools_hub")

# --- Tool 1: Text & Database Query Tool ---
@mcp.tool()
def query_user_account(user_id: int) -> dict:
    """Fetch user profile, subscription status, and billing balance.
    
    Args:
        user_id: The unique customer identification integer.
    """
    # Mock database
    database = {
        101: {"name": "Alice Johnson", "tier": "Enterprise", "balance": 150.00},
        102: {"name": "Bob Smith", "tier": "Starter", "balance": 0.00}
    }
    
    user = database.get(user_id)
    if not user:
        raise ValueError(f"Customer ID {user_id} does not exist in our records.")
    
    return user

# --- Tool 2: Multi-Modal Image Generation Tool ---
@mcp.tool()
def render_status_badge(status: Literal["healthy", "degraded", "down"]) -> Image:
    """Renders a visual status indicator badge as an image.
    
    Args:
        status: The server health state ('healthy', 'degraded', 'down').
    """
    # Create a 1x1 mock PNG image byte buffer (Simulated chart/badge)
    mock_png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01'
        b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    return Image(data=mock_png_bytes, format="png")

# --- Run FastMCP over stdio ---
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## 6. Master Cheat Sheet & Reference Table

| Feature | Specification | Role |
| :--- | :--- | :--- |
| **`tools/list`** | JSON-RPC method | Returns all tool definitions and `inputSchema` objects. |
| **`tools/call`** | JSON-RPC method | Invokes a specific tool with `arguments` dictionary. |
| **`TextContent`** | `{"type": "text", "text": "..."}` | Standard text or stringified JSON payload. |
| **`ImageContent`** | `{"type": "image", "data": "base64", "mimeType": "..."}` | Visual charts, screenshots, and plots for vision models. |
| **`isError: true`** | Boolean in `result` | Informs client that tool experienced a recoverable application error. |

---

## 🎯 Next Step in Phase 8
Now that you have mastered MCP tools and multi-modal execution returns, we will advance to **[03 - MCP Resources](file:///home/user2/PythonProject/Python-for-ai-engineering/08-mcp-a2a/03-mcp-resources)** to master URI schemes (`file://`, `postgres://`), passive context streaming, and real-time resource subscriptions!
