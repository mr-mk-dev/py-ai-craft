# AI Engineer Roadmap — For Java / Spring Boot Backend Engineers

Base: Java, Spring Boot, Microservices, Docker, Kubernetes, AWS, System Design
Target: AI Engineer (NOT ML Engineer / NOT Data Scientist)

---

## 1. Correction: Why "3 Different Categories" Matters

Your note was right — don't blend the paths. Corrected definitions:

| Role | Focus | Math/Stats Heavy? |
|---|---|---|
| **AI Engineer** | Builds products using existing LLMs via APIs. Software engineering + integration. | No |
| **ML Engineer** | Trains/deploys custom models (PyTorch/TensorFlow) | Yes |
| **Data Scientist** | Analysis, experiments, statistics, business insight | Yes |

→ Your roadmap should stay 90% **software engineering**, not model math. Fine-Tuning (your "later" list) is really ML-Engineer territory — keep it last, as conceptual knowledge only.

---

## 2. What You Already Have — Skip Re-learning

```
Docker, Kubernetes, AWS  → same tools, just deploy Python instead of Java
System Design skill      → directly reused in Phase 8
DI, DTOs, REST concepts  → map 1:1 to FastAPI (Phase 4)
```

You are NOT starting from zero. You're adding a language + a new integration layer on top of skills you already have.

---

## 3. Corrected Roadmap Flow

**Revision note:** the first version of this doc filed "AI Evaluation" under a "later" bucket and had no Security phase at all. Both were real gaps. Fixed here — evaluation and security aren't one final topic, they're a **parallel track** introduced early (Phase 2.5) and reinforced at every phase that follows, then given full dedicated depth in Phases 9–10.

```
 [Python Core] ──► [LLM + API Basics] ──► [Eval & Security Mindset] ──► [Prompt Engineering]
                                                     │  (parallel track — reinforced below)
                                │                    │
                                ▼                    │
                          [FastAPI]                  │
                                │                     │
                                ▼                     ▼
     [RAG Systems] ─────────────────────────► + retrieval eval, groundedness
                                │
                                ▼
     [Tool Calling → AI Agents] ────────────► + tool-call correctness, tool authorization
                                │
                                ▼
                        [MCP / A2A]
                                │
                                ▼
                 [AI App System Design]
                                │
                    ┌───────────┴───────────┐
                    ▼                        ▼
     [AI Evaluation & Reliability]     [AI Security]
      (deep dive — no longer "later")   (new — prompt injection, tenant isolation, tool authz)
                    │                        │
                    └───────────┬────────────┘
                                 ▼
   Later: [Vector DB internals] [Scaled Cloud Deploy] [Fine-Tuning]
```

**Fixes vs the original notes:**
- FastAPI moved earlier — you need it to expose/test everything from RAG onward. Fast pickup for you (~3-5 days), mirrors Spring Boot.
- **Evaluation** is no longer a late afterthought — introduced as a mindset early, reinforced inside RAG and Agents, then given a full phase.
- **Security** was missing entirely before — now its own phase, sitting right where System Design hands off to production.

---

## Phase 1 — Python Core (1–2 weeks)

- Async/await, decorators, type hints, virtualenv, pip
- JSON handling, file I/O, `requests`/`httpx`, basic OOP
- **Java → Python map:**
  - `CompletableFuture` → `async/await`
  - `@RestController` → decorators (`@app.get`)
  - Maven/Gradle deps → `pip` / `venv`
- Example: an async function to call an external API — same mental model as a Java async service call.

---

## Phase 2 — LLM + API Fundamentals (1 week)

**Block diagram:**
```
 Your App ──► LLM Provider API (OpenAI/Anthropic/etc.)
     │                │
  system prompt    tokens in
  user prompt      tokens out
     │                │
     └──── Response (streamed or full) ◄──┘
```

Topics:
- **Tokens** — cost & limits are measured in tokens, not characters
- **Context window** — max tokens model can "see" at once (prompt + history + output)
- **Temperature/top_p** — randomness control (0 = deterministic, 1 = creative)
- **Message roles** — `system`, `user`, `assistant`
- **Streaming** — token-by-token response (like SSE, which you likely know)
- **Structured output** — forcing JSON responses (important for backend integration)

Example: setting `temperature=0` for a backend service that must return consistent, parseable output — vs `temperature=0.7` for a chat feature.

---

## Phase 2.5 — Evaluation & Security Mindset (2–3 days, conceptual only)

Not a skill to master yet — a lens to hold from here on. Traditional backend has unit/integration tests, SLIs/SLOs, error rates. AI systems need those **plus**:

- **Reliability question:** "How do I know this system gave the right answer?" (not just "did it return 200 OK")
- **Security question:** "Can user input make this system do something it shouldn't?"

Keep these two questions in mind at every phase below — you'll see "eval" and "security" callouts inside RAG (Phase 5) and Agents (Phase 6) before the topics get full dedicated depth in Phases 9–10.

---

## Phase 3 — Prompt Engineering (3–5 days)

- Zero-shot vs few-shot prompting
- Chain-of-thought (ask model to reason step-by-step)
- Prompt templates (parameterized, like a query template)
- System prompt design — this is your main "config" lever as a backend engineer

---

## Phase 4 — FastAPI (3–5 days)

- Routes ≈ `@RestController` endpoints
- Pydantic models ≈ DTOs/request validation
- Dependency injection ≈ Spring's `@Autowired`
- Async endpoints — natural fit given Phase 1

This becomes the wrapper you put around every AI feature you build next.

---

## Phase 5 — RAG (Retrieval-Augmented Generation) (2–3 weeks)

**Pipeline block diagram:**
```
Documents → Chunking → Embeddings → Vector DB (store)
                                          │
User Query → Embedding ──────────────► Similarity Search
                                          │
                                    Top-K chunks
                                          │
                              (optional) Reranking
                                          │
                              LLM + Retrieved Context
                                          │
                                       Answer
```

Topics:
- **Chunking strategies** — fixed-size, recursive, semantic
- **Embeddings** — turning text into vectors (OpenAI, Cohere, open-source models)
- **Vector DBs** — Pinecone, Qdrant, Weaviate, Milvus, **pgvector** (extension for Postgres — you already know Postgres, easiest entry point)
- **Hybrid search** — combining vector similarity + keyword search
- **Reranking** — reordering retrieved chunks for relevance
- **Evaluation (early look, deepened in Phase 9)** — retrieval precision/recall, answer correctness, **groundedness** (is the answer actually supported by retrieved text?), **hallucination detection**, citation correctness
- **Security (early look, deepened in Phase 10)** — indirect prompt injection: a malicious instruction hidden inside a *retrieved document* can hijack the LLM. RAG is a common attack surface because you're feeding untrusted content straight into the prompt.

Example: instead of a `SELECT ... WHERE` query, RAG does a `SELECT ... ORDER BY vector_distance` — same DB instincts, new query type.

---

## Phase 6 — Function/Tool Calling → AI Agents (2–3 weeks)

Your notes jumped straight to "Agent Framework" — **tool/function calling is the prerequisite skill**, add it explicitly.

**Agent loop diagram (ReAct pattern):**
```
User Query
    │
    ▼
LLM decides: "I need a tool" ──► Calls Tool (API/DB/function)
    │                                    │
    ▼                                    ▼
  (loop until done) ◄──────────── Tool Result returned to LLM
    │
    ▼
Final Answer
```

Frameworks (know the difference, don't learn all 4 deeply at once):
- **LangChain** — general-purpose toolkit, most common starting point
- **LangGraph** — stateful, graph-based orchestration for complex flows
- **CrewAI** — role-based multi-agent teams
- **AutoGen** (Microsoft) — conversational multi-agent systems

Start with LangChain + LangGraph as your learning base — but check current docs before committing to one for a real project; the OpenAI Agents SDK and Google ADK have both matured fast and are now standard comparison points, and the original AutoGen lineage has split (Microsoft's AutoGen vs. the community-run "AG2" fork).

- **Evaluation (early look)** — tool-call correctness: did the agent pick the *right* tool with the *right* arguments? Wrong tool selection is the most common agent failure mode.
- **Security (early look)** — tool authorization: an agent with a "delete file" or "send email" tool needs the same permission checks you'd put on any backend action. Never let the LLM's output alone decide whether a destructive action runs — gate it the way you'd gate any privileged API call.

---

## Phase 7 — MCP & A2A (1 week)

- **MCP (Model Context Protocol, by Anthropic)** — standardized way for an AI app to connect to external tools/data sources. Think "USB-C port for AI" instead of writing a custom integration per tool.
- **A2A (Agent2Agent, by Google)** — protocol letting agents from different systems communicate with each other.

```
AI App ──► MCP Server ──► Tool / Database / API
```

This is newer, high-signal knowledge for 2026 job market — good differentiator on a resume.

---

## Phase 8 — AI Application System Design (ongoing — this is your strength)

This is where your existing System Design skill pays off directly.

```
Client → API Gateway → AI Service (FastAPI)
                             │
                     Semantic Cache check
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
           RAG Pipeline           LLM Provider (w/ fallback model)
                  │                     │
                  └─────────┬───────────┘
                             ▼
                        Guardrails
                    (content filter, PII check)
                             ▼
                          Response
                             │
                (Docker + K8s + AWS — you already know this layer)
```

New-to-you concepts: semantic caching, rate limiting per user/tenant, model fallback chains, LLM call observability/tracing, cost tracking per request, latency management via streaming.

---

## Phase 9 — AI Evaluation & Reliability Engineering (1–2 weeks)

**Promoted out of "later" — this is where the early looks from Phases 5 & 6 get real depth.**

```
                    AI Application
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          Production             Evaluation
              │                     │
        traces/logs             golden test dataset
        latency                 retrieval score
        cost                    answer/groundedness score
        errors                  regression tests (per prompt/model change)
              │                     │
              └──────────┬──────────┘
                         ▼
                   Improvement
```

Topics:
- **Golden/test datasets** — a fixed set of question→expected-answer pairs, run on every change
- **LLM-as-a-judge** — using a second LLM call to score correctness/groundedness at scale
- **Regression testing for prompts** — treat prompt changes like code changes; re-run the eval suite
- **Tracing** — log every LLM call (input, output, latency, cost, tokens) per request, same instinct as distributed tracing in microservices
- **Feedback loops** — capturing production failures back into the golden dataset

Example: before you ship a prompt tweak or swap models, run it against your golden dataset the same way you'd run a regression suite before merging a PR.

---

## Phase 10 — AI Security (3–5 days)

**New phase — this was missing entirely before, and it's a natural fit given your backend/auth background.**

- **Prompt injection** — user input tricks the LLM into ignoring its system prompt
- **Indirect prompt injection** — malicious instructions hidden in a retrieved document, a web page, or a tool's output (harder to catch — the attacker never talks to your app directly)
- **Data leakage** — LLM exposing another user's data via context bleed or bad prompt construction
- **Tenant isolation** — in a multi-tenant app, make sure retrieval/tools can never cross tenant boundaries (same principle as row-level security you already know from Postgres)
- **Tool authorization** — gate any tool that mutates state behind the same permission checks you'd use for a normal API call; never trust the LLM's decision alone
- **Sensitive-data handling** — PII redaction before sending data to a third-party LLM provider

Example: treat every piece of retrieved/tool-returned text as **untrusted input**, the same mental model as sanitizing user input in a traditional web app — except here the "user input" can arrive indirectly, through a document your RAG system pulled in.

---

## Later to Learn

- **Vector DB Deep Dive** — indexing internals (HNSW, IVF)
- **Cloud Deployment at Scale** — applying your AWS/K8s skill to high-throughput AI services
- **Fine-Tuning** (LoRA/QLoRA) — conceptual only; this is ML-Engineer territory, not core AI-Engineer work

---

## Suggested Timeline (part-time pace)

| Phase | Duration |
|---|---|
| 1–3: Python + LLM API + Eval/Security mindset + Prompting | 2–3 weeks |
| 4: FastAPI | ~1 week |
| 5: RAG (incl. retrieval eval, injection-via-documents) | 2–3 weeks |
| 6: Agents (incl. tool-call eval, tool authz) | 2–3 weeks |
| 7: MCP/A2A | 1 week |
| 8: System Design | ongoing (parallel with all above) |
| 9: AI Evaluation & Reliability (deep dive) | 1–2 weeks |
| 10: AI Security (deep dive) | ~1 week |
| **Total core path** | **~13–15 weeks** |
