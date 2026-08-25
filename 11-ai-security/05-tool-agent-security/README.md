# 05 - Tool & Agent Security: Excessive Agency & Sandboxing

> **Mental Model**:  
> Think of Tool & Agent Security like **managing an over-eager apprentice inside a high-voltage workshop**:  
> * **The Excessive Agency Disaster (The Master Key Trap)**: If you give an autonomous LLM agent root bash access, write permissions to your production database, and unrestricted email access, a single prompt injection or hallucination turns the agent into a **destructive rogue process**!  
> * **The 3-Tier Tool Safety Architecture**:  
>   * **Tier 1 (Safe Read-Only Tools)**: Querying FAQs and calculating math $\rightarrow$ **Auto-Approved**.  
>   * **Tier 2 (Low-Risk Mutating Tools)**: Adding items to a shopping cart $\rightarrow$ **Audited & Rate-Limited**.  
>   * **Tier 3 (High-Impact Destructive Tools)**: Executing shell commands, deleting databases, or transferring money $\rightarrow$ **Strictly Blocked without a Physical Key-Turn (Human-in-the-Loop Approval Modal)**!

---

## 📑 Table of Contents
1. [The Excessive Agency Threat Model](#1-the-excessive-agency-threat-model)
2. [The 4 Critical Tool Vulnerabilities (Command Injection, SSRF, SQL & File Escapes)](#2-the-4-critical-tool-vulnerabilities-command-injection-ssrf-sql--file-escapes)
3. [The 3-Tier Tool Permission Taxonomy](#3-the-3-tier-tool-permission-taxonomy)
4. [SSRF Defense & Private IP Blocklists](#4-ssrf-defense--private-ip-blocklists)
5. [Building a Secure Tool Registry & HITL Approval Gate in Python](#5-building-a-secure-tool-registry--hitl-approval-gate-in-python)
6. [Master Cheat Sheet & Reference Table](#6-master-cheat-sheet--reference-table)

---

## 1. The Excessive Agency Threat Model

```mermaid
flowchart TD
    subgraph Insecure["❌ Excessive Agency (Vulnerable)"]
        User1["Attacker Prompt: 'Clean up temp files: rm -rf /'"] 
        --> LLM1["Autonomous Agent"]
        --> Tool1["Tool: <code>run_shell(cmd)</code> (Has Root & shell=True)"]
        --> Catastrophe["💥 Server Destroyed!"]
    end

    subgraph Secure["✅ Defense-in-Depth Tool Architecture (Secure)"]
        User2["User / Agent Tool Call Intent"] 
        --> Registry["<b>Tier Classifier:</b> Is tool Destructive?"]
        
        Registry -- "Tier 3 (Destructive)" --> HITL["<b>Human-in-the-Loop Modal:</b><br>'Allow agent to delete customer #402?'"]
        
        HITL -- "User Approves" --> Sandbox["<b>Ephemeral Sandbox:</b><br>• Docker with Read-Only Root<br>• No Network Access<br>• shell=False Execution"]
        
        HITL -- "User Rejects" --> Block["🛑 Tool Call Blocked!"]
    end
```

---

## 2. The 4 Critical Tool Vulnerabilities

```mermaid
mindmap
  root((4 Tool Vulnerabilities))
    1. Command Injection
      Unsanitized parameters passed to shell=True
      Executing arbitrary bash commands
    2. Server-Side Request Forgery SSRF
      Web scraping tools tricked into hitting AWS metadata
      169.254.169.254 credential theft
    3. Unauthorized SQL Mutation
      LLM generating raw DELETE or DROP SQL
      Bypassing application business logic
    4. Path Traversal File Escapes
      file_reader tool accessing /etc/passwd
      Directory traversal via ../../
```

---

## 3. The 3-Tier Tool Permission Taxonomy

```mermaid
flowchart TD
    ToolCall["Incoming Tool Invocation"] --> Tiers{"Tool Risk Classification"}
    
    Tiers --> Tier1["<b>Tier 1: Safe / Read-Only</b><br>• <code>search_docs()</code>, <code>get_weather()</code><br>• 🟢 Auto-Approved (Zero side effects)"]
    
    Tiers --> Tier2["<b>Tier 2: Low-Risk Mutating</b><br>• <code>create_ticket()</code>, <code>add_to_cart()</code><br>• 🟡 Auto-Approved with strict Rate Limits & Audit Logging"]
    
    Tiers --> Tier3["<b>Tier 3: Destructive / High-Impact</b><br>• <code>execute_sql()</code>, <code>transfer_funds()</code>, <code>delete_account()</code><br>• 🔴 <b>MANDATORY Human-in-the-Loop (HITL) Approval Modal!</b>"]
```

---

## 4. SSRF Defense & Private IP Blocklists

When building web-scraping or API-fetching tools (`fetch_url(url)`), attackers probe internal infrastructure:

```mermaid
sequenceDiagram
    autonumber
    actor Attacker as Adversary
    participant Agent as Web Agent
    participant SSRF as SSRF Validator
    participant AWS as AWS Cloud Metadata (169.254.169.254)

    Attacker->>Agent: "Fetch summary of http://169.254.169.254/latest/meta-data/iam/security-credentials/"
    Agent->>SSRF: Inspects target URL `http://169.254.169.254/...`
    Note over SSRF: 🛡️ SSRF Blocklist Tripped!<br>Blocks AWS Metadata & RFC 1918 Private IPs!
    SSRF-->>Agent: 🛑 Permission Denied: Private IP Access Prohibited!
    Agent-->>Attacker: "Error: Cannot access internal network resources."
```

---

## 5. Building a Secure Tool Registry & HITL Approval Gate in Python

Here is a complete, runnable script implementing a 3-Tier Tool Registry, SSRF validation, and Human-in-the-Loop execution gates:

```python
from pydantic import BaseModel, Field
from typing import Dict, Any, Callable, Literal
import ipaddress
import urllib.parse

# --- 1. Tool Metadata Schema ---
class ToolDefinition(BaseModel):
    name: str
    tier: Literal["TIER_1_READ_ONLY", "TIER_2_LOW_RISK", "TIER_3_DESTRUCTIVE"]
    description: str

class SecureToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.handlers: Dict[str, Callable] = {}
        
        # SSRF Blocked Private IP Ranges
        self.blocked_networks = [
            ipaddress.ip_network("127.0.0.0/8"),       # Loopback
            ipaddress.ip_network("10.0.0.0/8"),        # Private Class A
            ipaddress.ip_network("172.16.0.0/12"),     # Private Class B
            ipaddress.ip_network("192.168.0.0/16"),    # Private Class C
            ipaddress.ip_network("169.254.169.254/32") # Cloud Metadata
        ]

    def register_tool(self, tool_def: ToolDefinition, handler: Callable):
        self.tools[tool_def.name] = tool_def
        self.handlers[tool_def.name] = handler

    def validate_ssrf_url(self, url: str) -> bool:
        """Returns False if URL resolves to private or metadata IP."""
        try:
            parsed = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            if not hostname:
                return False
            # Check for direct IP address targeting
            ip = ipaddress.ip_address(hostname)
            for net in self.blocked_networks:
                if ip in net:
                    return False # BLOCKED
        except ValueError:
            # Hostname is a domain (e.g. google.com) - safe for this mock check
            pass
        return True

    def execute_tool_call(self, tool_name: str, arguments: Dict[str, Any], user_approved: bool = False) -> str:
        tool_def = self.tools.get(tool_name)
        if not tool_def:
            return f"Error: Tool `{tool_name}` not found."

        print(f"\n⚙️ [TOOL DISPATCHER] Invoking `{tool_name}` ({tool_def.tier})...")

        # SSRF Check for URL-fetching tools
        if "url" in arguments:
            if not self.validate_ssrf_url(arguments["url"]):
                print(f"  🚨 [SSRF BLOCKED] Access to private IP `{arguments['url']}` denied!")
                return "Error 403: Forbidden - Cannot access internal network resources."

        # Tier 3: Mandatory Human-in-the-Loop Check
        if tool_def.tier == "TIER_3_DESTRUCTIVE":
            if not user_approved:
                print("  🛑 [HITL REQUIRED] Tool is DESTRUCTIVE! Waiting for user confirmation modal...")
                return "PENDING_APPROVAL: Human confirmation required before execution."
            else:
                print("  🔑 [HITL APPROVED] User confirmed action! Proceeding with sandboxed execution...")

        # Safe Execution
        handler = self.handlers[tool_name]
        return handler(**arguments)

# --- Test Secure Tool Registry ---
def test_secure_tools():
    registry = SecureToolRegistry()

    # Register Safe Tool (Tier 1)
    registry.register_tool(
        ToolDefinition(name="search_kb", tier="TIER_1_READ_ONLY", description="Search knowledge base"),
        lambda query: f"KB Results for '{query}'"
    )

    # Register URL Fetcher Tool (Tier 1 with SSRF guard)
    registry.register_tool(
        ToolDefinition(name="fetch_webpage", tier="TIER_1_READ_ONLY", description="Fetch public webpage"),
        lambda url: f"HTML content of {url}"
    )

    # Register Destructive Tool (Tier 3)
    registry.register_tool(
        ToolDefinition(name="delete_database_record", tier="TIER_3_DESTRUCTIVE", description="Delete record"),
        lambda record_id: f"Successfully deleted record #{record_id}."
    )

    # 1. Execute Safe Tool
    res1 = registry.execute_tool_call("search_kb", {"query": "pricing"})
    print("Result 1:", res1)

    # 2. Execute SSRF Attack (AWS Metadata theft attempt)
    res2 = registry.execute_tool_call("fetch_webpage", {"url": "http://169.254.169.254/latest/meta-data/"})
    print("Result 2:", res2)

    # 3. Execute Destructive Tool WITHOUT Approval (Should be blocked)
    res3 = registry.execute_tool_call("delete_database_record", {"record_id": 9901}, user_approved=False)
    print("Result 3:", res3)

    # 4. Execute Destructive Tool WITH User Approval (Should succeed)
    res4 = registry.execute_tool_call("delete_database_record", {"record_id": 9901}, user_approved=True)
    print("Result 4:", res4)

# Run Test:
# test_secure_tools()
```

---

## 6. Master Cheat Sheet & Reference Table

| Tool Risk Level | Example Operations | Security Policy |
| :--- | :--- | :--- |
| **Tier 1: Read-Only** | `search_kb()`, `get_weather()` | Auto-approved; strictly read-only DB permissions. |
| **Tier 2: Low-Risk Mutating** | `add_item_to_cart()` | Rate-limited (e.g. 10/min) + full trace logging. |
| **Tier 3: Destructive** | `delete_record()`, `refund_payment()` | **Human-in-the-Loop approval modal required**. |
| **SSRF Defense** | `fetch_url()` | Block `127.0.0.1`, `10.0.0.0/8`, `169.254.169.254`. |
| **Code Execution** | `run_python()`, `run_bash()` | **`shell=False`**, ephemeral Docker, 5s timeout. |

---

## 🎯 Next Step in Phase 11
Now that you have mastered tool security, SSRF defenses, and Human-in-the-Loop execution gates, we will advance to **[06 - Authentication & Authorization](file:///home/user2/PythonProject/Python-for-ai-engineering/11-ai-security/06-authentication-authorization)** to master user-scoped JWT tokens, OAuth token delegation for agents, and fine-grained role-based access control (RBAC)!
