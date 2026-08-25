# 01 - Prompt Fundamentals: The 5-Part Prompt Architecture

> **Welcome to Phase 4: Prompt Engineering & Reasoning Workflows!**  
> **Mental Model**:  
> Think of Prompt Engineering like **directing a world-class Hollywood actor**:  
> * An LLM possesses vast knowledge, but if the director simply yells *"Act!"*, the actor will do something generic, unpredictable, and vague.  
> * A master director provides crystal-clear direction:  
>   1. **The Persona**: *"You are a seasoned senior forensic accountant."*  
>   2. **The Context**: *"You are auditing an irregular Q3 revenue ledger."*  
>   3. **The Task**: *"Identify the top 3 tax compliance violations."*  
>   4. **The Constraints**: *"Do NOT use legal jargon. Keep it under 150 words."*  
>   5. **The Output Format**: *"Output as a 3-column markdown table."*  
> Prompt engineering is not "magic words"—it is **rigorous specification engineering**.

---

## 📑 Table of Contents
1. [The 5-Part Prompt Architecture](#1-the-5-part-prompt-architecture)
2. [Dissecting the 5 Core Components](#2-dissecting-the-5-core-components)
3. [The Power of Structural Delimiters (XML Tags)](#3-the-power-of-structural-delimiters-xml-tags)
4. [Positive vs. Negative Constraints (The Pink Elephant Rule)](#4-positive-vs-negative-constraints-the-pink-elephant-rule)
5. [Audience, Tone & Style Calibration](#5-audience-tone--style-calibration)
6. [Dynamic Python Prompt Builders](#6-dynamic-python-prompt-builders)
7. [Master Cheat Sheet & Reference Table](#7-master-cheat-sheet--reference-table)

---

## 1. The 5-Part Prompt Architecture

Every high-performing enterprise prompt is constructed from **5 modular building blocks**:

```mermaid
flowchart TD
    Prompt["<b>The 5-Part Enterprise Prompt</b>"]
    Prompt --> P1["<b>1. Role & Persona</b><br>Sets expertise, vocabulary register, and domain perspective"]
    Prompt --> P2["<b>2. Context & Background</b><br>Grounding facts, retrieved RAG data, and scenario details"]
    Prompt --> P3["<b>3. Clear Task Directive</b><br>Unambiguous action verb (Extract, Classify, Audit, Draft)"]
    Prompt --> P4["<b>4. Negative & Positive Constraints</b><br>Strict rules, word limits, and boundaries"]
    Prompt --> P5["<b>5. Output Format Specification</b><br>Markdown table, JSON schema, or bullet points"]
```

---

## 2. Dissecting the 5 Core Components

```mermaid
flowchart LR
    subgraph Anatomy["Anatomy of a Production Prompt"]
        direction TB
        R["<b>1. Role:</b> 'You are a Senior Security Engineer specializing in OAuth2.'"]
        C["<b>2. Context:</b> '<api_spec>POST /oauth/token ...</api_spec>'"]
        T["<b>3. Task:</b> 'Audit the specification above for token leakage vulnerabilities.'"]
        G["<b>4. Constraints:</b> 'List only High and Critical severity findings. Be concise.'"]
        O["<b>5. Format:</b> 'Output findings as: [Severity] | [Vulnerability] | [Remediation]'"]
    end
```

### The 5 Components Reference Matrix:

| Component | Purpose | Example |
| :--- | :--- | :--- |
| **1. Role / Persona** | Primes the LLM's attention weights to relevant technical domains. | *"You are an expert PostgreSQL DBA."* |
| **2. Context** | Supplies the specific data the model must reason over. | *"Here is the slow-query EXPLAIN plan: `...`"* |
| **3. Task Directive** | Tells the model exactly what action to execute. | *"Analyze the index scans and suggest 2 indexing optimizations."* |
| **4. Constraints** | Prevents unwanted hallucination, verbosity, or off-topic drift. | *"Do NOT suggest sharding. Focus only on B-Tree indexes."* |
| **5. Output Format** | Specifies the exact layout of the final answer. | *"Return valid SQL `CREATE INDEX` statements followed by a 1-sentence rationale."* |

---

## 3. The Power of Structural Delimiters (XML Tags)

When prompts contain documents, instructions, and examples all mixed together, the model can get confused about where instructions end and data begins.

**Structural Delimiters (especially XML tags)** create clean walls between data blocks:

```mermaid
flowchart TD
    subgraph DelimitedPrompt["XML Delimited Prompt Layout"]
        direction TB
        D1["<system_instructions><br>Analyze customer feedback sentiment.<br></system_instructions>"]
        D2["<context_guidelines><br>Positive: 4-5 stars. Negative: 1-2 stars.<br></context_guidelines>"]
        D3["<customer_review><br>The package arrived 2 days late, but the product is great!<br></customer_review>"]
    end
```

### Why Anthropic Claude & OpenAI Love XML Delimiters:
1. **Zero Ambiguity**: The model knows with 100% certainty that text inside `<review>...</review>` is user data.
2. **Injection Defense**: Delimiters prevent user data from breaking out into system instructions.
3. **Targeted Referencing**: You can tell the model: *"Refer strictly to the facts inside `<document>`."*

---

## 4. Positive vs. Negative Constraints (The Pink Elephant Rule)

> 🐘 **The Psychological LLM Quirk:**  
> If you tell a human *"Do NOT think of a pink elephant"*, the first thing they picture is a pink elephant.  
> LLMs behave similarly! If you write *"Do NOT apologize and do NOT say 'Sure, I can help with that!'"*, the probability of those very tokens increases because they are present in the context.

```mermaid
flowchart LR
    subgraph Negative["❌ Brittle Negative Prompting"]
        N1["'Do NOT write intro fluff or apologies.'"] --> N2["Model often replies: 'I will not apologize. Here is the answer...'"]
    end

    subgraph Positive["✅ Robust Positive Directives"]
        P1["'Begin your response immediately with the raw SQL code block.'"] --> P2["Model immediately outputs: '```sql SELECT...'"]
    end
```

### Prompt Transformation Table:

| ❌ Weak Negative Prompt | ✅ Strong Positive Directive |
| :--- | :--- |
| *"Don't make the explanation too long."* | *"Explain this in exactly 2 concise sentences."* |
| *"Don't include introductory pleasantries."* | *"Begin immediately with the bulleted list."* |
| *"Don't hallucinate or guess."* | *"Rely strictly on the text inside `<context>`. If unknown, respond with 'DATA_NOT_FOUND'."* |
| *"Don't use complicated words."* | *"Explain this using vocabulary suitable for an 8th-grade student."* |

---

## 5. Audience, Tone & Style Calibration

A single prompt can be tailored to completely different audiences simply by shifting the persona and tone:

```mermaid
flowchart TD
    Incident["Incident: Production Database Outage for 15 Minutes"]
    
    Incident --> ToneA["<b>Audience A: Board of Directors</b><br>Tone: Executive, concise, financial impact, SLA recovery"]
    Incident --> ToneB["<b>Audience B: Engineering Team</b><br>Tone: Technical, root cause, stack trace, remediation steps"]
    Incident --> ToneC["<b>Audience C: Public Status Page</b><br>Tone: Empathetic, transparent, reassuring, non-technical"]
```

---

## 6. Dynamic Python Prompt Builders

In production, never build prompts using messy string concatenation (`+`). Use typed Python functions or Jinja templates:

```python
def build_expert_prompt(
    role: str,
    context_data: str,
    task: str,
    output_format: str,
    constraints: list[str]
) -> str:
    """Assembles a clean, XML-delimited production prompt."""
    
    formatted_constraints = "\n".join(f"- {c}" for c in constraints)
    
    return f"""<role>
You are a {role}.
</role>

<context>
{context_data}
</context>

<task>
{task}
</task>

<constraints>
{formatted_constraints}
</constraints>

<output_format>
{output_format}
</output_format>"""

# Example Usage:
prompt = build_expert_prompt(
    role="Senior Staff Python Engineer",
    context_data="def sum(a,b): return a+b",
    task="Review the code for type annotations and docstrings.",
    output_format="Return the refactored code block followed by a 1-line explanation.",
    constraints=[
        "Use Python 3.12 modern type hints.",
        "Begin immediately with the python code fence."
    ]
)

print(prompt)
```

---

## 7. Master Cheat Sheet & Reference Table

| Pillar | Principle | Production Best Practice |
| :--- | :--- | :--- |
| **The 5-Part Formula** | Role + Context + Task + Constraints + Format | Include all 5 components in every core production prompt. |
| **Structural Delimiters**| XML Tags (`<context>`, `<task>`) | Use tags to clearly separate untrusted data from system instructions. |
| **Directive Framing** | Positive Directives > Negative Begging | Tell the model *what to do first* rather than *what not to do*. |
| **Grounding Anchor** | Fallback string for missing info | Instruct the model to say `"NOT_IN_CONTEXT"` if facts are missing. |

---

## 🎯 Next Step in Phase 4
Now that you have mastered Prompt Fundamentals, we will advance to **[02 - Zero-Shot Prompting](file:///home/user2/PythonProject/Python-for-ai-engineering/04-prompt-engineering/02-zero-shot)** to master direct instruction execution and task decomposition!
