# 01 - Tool Calling Fundamentals: JSON Schemas & Model Intent

> **Welcome to Phase 7: Tools & Autonomous Agents!**  
> **Mental Model**:  
> Think of Tool Calling like a **brilliant strategist working with a robotic field assistant**:  
> * **The LLM (The Strategist)**: Has encyclopedic reasoning ability, but is physically trapped in a dark room with **no internet access, no database connection, and no calculator**.  
> * **The Big Myth**: The LLM *does NOT execute your Python code on its servers!*  
> * **The Reality (Tool Calling)**: When you provide a list of available tools, the LLM recognizes when it needs external information. It pauses text generation and outputs a **structured JSON blueprint** (*"Please execute `fetch_weather(city='Tokyo')`"*).  
> * **Your Python Runtime (The Robotic Hands)**: Reads the LLM's blueprint, executes the actual Python function, and feeds the results back to the LLM to synthesize the final answer.

---

## 📑 Table of Contents
1. [The Cardinal Law: LLMs Don't Run Code](#1-the-cardinal-law-llms-dont-run-code)
2. [The Anatomy of a JSON Schema Tool Declaration](#2-the-anatomy-of-a-json-schema-tool-declaration)
3. [Controlling Execution with tool_choice](#3-controlling-execution-with-tool_choice)
4. [Single vs. Parallel Tool Calling](#4-single-vs-parallel-tool-calling)
5. [Auto-Generating Tool Schemas from Pydantic in Python](#5-auto-generating-tool-schemas-from-pydantic-in-python)
6. [Master Cheat Sheet & Reference Table](#6-master-cheat-sheet--reference-table)

---

## 1. The Cardinal Law: LLMs Don't Run Code

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant App as Your Python Backend
    participant LLM as OpenAI / Anthropic Model
    participant API as External Weather API

    User->>App: "What is the temperature in Tokyo right now?"
    App->>LLM: Sends prompt + JSON Schema for `get_weather` tool
    Note over LLM: Model recognizes it lacks live data.<br>Generates tool call intent JSON!
    LLM-->>App: Emits `tool_calls`: `get_weather(city='Tokyo')`
    Note over App: ⚡ YOUR PYTHON CODE EXECUTES THE TOOL!
    App->>API: `requests.get('https://api.weather.com/tokyo')`
    API-->>App: `{"temp": "18C", "condition": "Sunny"}`
    App->>LLM: Injects tool result as a `role: 'tool'` message
    LLM-->>App: Synthesizes final response: "It is currently 18°C and sunny in Tokyo."
    App-->>User: Delivers final answer
```

---

## 2. The Anatomy of a JSON Schema Tool Declaration

To teach an LLM what tools it can call, you provide an array of **OpenAPI-compliant JSON Schema objects**:

```mermaid
flowchart TD
    ToolDeclaration["Tool Declaration Object"]
    ToolDeclaration --> Type["<b>type: 'function'</b>"]
    ToolDeclaration --> Func["<b>function:</b>"]
    
    Func --> Name["<b>name: 'get_stock_price'</b><br>Exact Python function identifier"]
    Func --> Desc["<b>description: 'Fetches live market price for a stock ticker.'</b><br>🚨 <i>Acts as prompt engineering for function selection!</i>"]
    Func --> Params["<b>parameters:</b> (JSON Schema Object)"]
    
    Params --> Props["<b>properties:</b><br>• ticker: string (e.g. 'AAPL')<br>• currency: enum ['USD', 'EUR']"]
    Params --> Req["<b>required: ['ticker']</b>"]
```

### The JSON Schema Specification:
```python
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Retrieves the real-time trading price and currency for a stock ticker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The equity ticker symbol, e.g. AAPL, NVDA, TSLA."
                    },
                    "currency": {
                        "type": "string",
                        "enum": ["USD", "EUR", "GBP"],
                        "default": "USD",
                        "description": "Target fiat currency code."
                    }
                },
                "required": ["ticker"]
            }
        }
    }
]
```

---

## 3. Controlling Execution with `tool_choice`

You can control *if* and *how* the LLM selects tools using the **`tool_choice`** parameter:

```mermaid
flowchart TD
    Choice["tool_choice Modes"]
    
    Choice --> Auto["<b>tool_choice='auto' (Default)</b><br>The model intelligently decides whether to chat normally OR call 1+ tools."]
    
    Choice --> Req["<b>tool_choice='required'</b><br>Forces the model to call AT LEAST ONE tool (Cannot reply with plain text!)."]
    
    Choice --> Specific["<b>tool_choice={'type': 'function', ...}</b><br>Forces the model to call ONE specific named function."]
    
    Choice --> NoneMode["<b>tool_choice='none'</b><br>Disables all tool calling; forces regular conversational text output."]
```

### `tool_choice` Quick Reference:

| `tool_choice` Setting | Model Behavior | Best Use Case |
| :--- | :--- | :--- |
| **`"auto"`** | Model chooses between direct text reply or calling tools. | Standard conversational assistants. |
| **`"required"`** | Model **must** call a tool; cannot generate plain text. | Data extraction pipelines, agent step loops. |
| **`{"name": "func_name"}`** | Model **must** call this exact specific tool. | Forced single-step workflows (e.g. form filling). |
| **`"none"`** | Model ignores tools and only writes regular text. | Temporarily disabling tools during error states. |

---

## 4. Single vs. Parallel Tool Calling

Modern frontier models support **Parallel Tool Calling**, generating multiple independent tool invocations in a single response turn:

```mermaid
flowchart TD
    UserQuery["User: 'Compare the stock prices of Apple, Microsoft, and Nvidia.'"] 
    --> LLM["LLM Generates 3 Parallel Tool Calls in 1 Turn:"]
    
    LLM --> T1["tool_call_1: <code>get_stock_price(ticker='AAPL')</code>"]
    LLM --> T2["tool_call_2: <code>get_stock_price(ticker='MSFT')</code>"]
    LLM --> T3["tool_call_3: <code>get_stock_price(ticker='NVDA')</code>"]
    
    T1 & T2 & T3 --> Exec["⚡ Python executes all 3 API calls concurrently with <code>asyncio.gather</code>!"]
```

---

## 5. Auto-Generating Tool Schemas from Pydantic in Python

Writing JSON Schema dictionaries manually is tedious and error-prone. Use **Pydantic** to auto-generate schemas:

```python
from pydantic import BaseModel, Field
from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "mock-key"))

# 1. Define Tool Arguments Schema in Pydantic
class StockPriceArgs(BaseModel):
    ticker: str = Field(description="The stock ticker symbol, e.g. AAPL or MSFT.")
    include_volume: bool = Field(default=False, description="Whether to include daily trading volume.")

# 2. Convert to OpenAI Tool Definition
stock_tool = {
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Fetch real-time stock valuation and pricing.",
        "parameters": StockPriceArgs.model_json_schema()
    }
}

# 3. Submit Request to LLM with Tool Definition
def test_tool_calling(user_prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_prompt}],
        tools=[stock_tool],
        tool_choice="auto"
    )

    message = response.choices[0].message
    if message.tool_calls:
        print(f"🤖 LLM requested {len(message.tool_calls)} tool call(s):")
        for tool_call in message.tool_calls:
            print(f"  • Tool: {tool_call.function.name}")
            print(f"  • Arguments JSON: {tool_call.function.arguments}")
            args = json.loads(tool_call.function.arguments)
            print(f"  • Parsed Python dict: {args}")
    else:
        print(f"💬 Direct text reply: {message.content}")

# Test Tool Invocation:
# test_tool_calling("What is Apple's current stock price?")
```

---

## 6. Master Cheat Sheet & Reference Table

| Parameter / Object | Role in Tool Calling |
| :--- | :--- |
| **`tools=[...]`** | Array of available function schemas passed to the LLM. |
| **`tool_calls`** | Array of requested tool executions returned inside `response.choices[0].message`. |
| **`tool_call.id`** | Unique tracking ID (e.g. `call_abc123`) used to link tool outputs. |
| **`tool_call.function.arguments`**| Stringified JSON containing the validated arguments. |
| **`tool_choice="auto"`** | Allows the model to autonomously decide when to invoke tools. |

---

## 🎯 Next Step in Phase 7
Now that you understand tool declarations and JSON schemas, we will advance to **[02 - Tool Calling Flow](file:///home/user2/PythonProject/Python-for-ai-engineering/07-tools-agents/02-tool-calling-flow)** to master the multi-turn conversational loop, tool message roles, and roundtrip result injection!
