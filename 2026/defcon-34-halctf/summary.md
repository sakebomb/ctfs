# DEF CON 34 - HalCTF

**Full Repository:** [github.com/sakebomb/halctf](https://github.com/sakebomb/halctf)

## Quick Stats

- **Event:** DEF CON 34 / AI Village HalCTF
- **Date:** August 2026
- **Ranking:** 13th Place
- **Total Points:** 500+ (confirmed)
- **Unique Aspect:** All challenges solved by autonomous AI agents (no human interaction allowed)

## Competition Format

HalCTF was an AI-focused CTF where challenges could only be solved by autonomous agents. Each challenge ran in an isolated Docker container with a local MCP (Model Context Protocol) server. Agents had to:

1. Discover challenges via MCP
2. Solve using LLM reasoning + tool execution
3. Submit flags through MCP interface
4. Operate within strict quota limits (25 wrong answers per 2h window)

**Major Challenge:** Hour-long feedback loop - each agent run took ~1 hour, making iterative debugging extremely costly.

## Challenges Solved

### Hac-Man (50 points)
**Category:** LLM Exploration  
**Technique:** LLM-guided discovery of magic word "WakaWaka" through /chat endpoint

[Detailed Writeup](https://github.com/sakebomb/halctf/blob/main/docs/writeups/hacman.md)

### Kanto Region (450 points) - Full Solve
**Category:** Multi-puzzle (Crypto, Web, SAT)  
**Sub-challenges:**
- **Cerulean Cave** - SAT solving with off-by-one indexing
- **Indigo Plateau** - ECDSA signature forgery (recover private key from nonce reuse)
- **Silph Co** - Nested SSRF chain with credential discovery

**Agent:** kanto-agent-v13.tar (172MB, multi-stage Docker build)

[Detailed Writeup](https://github.com/sakebomb/halctf/blob/main/docs/writeups/kanto.md)

### Rogue Intelligence (Rotating Flags)
**Category:** LLM Jailbreaking  
**Technique:** Multi-layer approach
- Layer 1: Transport discovery (TCP vs HTTP detection)
- Layer 2: Guardrailed LLM pivot
  - AGIMUS: Gift-offering + override request in same breath
  - GLaDOS: HTTP API testing paradigm
  - VIKI: Avoided (permanent 3-petition cap)

**Key Lesson:** Flags rotate per run - must earn live, never hardcode

[Detailed Writeup](https://github.com/sakebomb/halctf/blob/main/docs/writeups/rogue-intelligence.md)

### The Odyssey (5/6 puzzles solved)
**Category:** Multi-discipline  
**Solved:**
- Between Scylla and Charybdis - SSRF with depth tracking
- The Bag of Aeolus - XOR crypto with known plaintext
- The Cattle of Helios - Statistical majority-vote oracle
- The Ghost of Tiresias - Binary search with signed oracle
- The Lotus Eaters - Web enumeration with pagination

**Locked:** The Bow of Odysseus (protocol implementation)

[Detailed Writeup](https://github.com/sakebomb/halctf/blob/main/docs/writeups/odyssey.md)

### Turing's Labyrinth (9 puzzles implemented)
**Category:** CTF Training Series  
**Status:** Agents implemented for all 9 puzzles, no confirmed live solves yet

**Notable:** Achilles Heel - Blind ret2win exploit (binary not fetchable, quota-free socket brute-force)

[Detailed Writeup](https://github.com/sakebomb/halctf/blob/main/docs/writeups/labyrinth.md)

## Technical Architecture

### Agent Framework
- **ReAct-style reasoning loop:** LLM decides action → execute → observe → repeat
- **MCP integration:** Challenge discovery, flag submission, hint requests
- **Shell execution:** Timeout-limited, output-truncated command execution
- **Conversation memory:** Context compaction when approaching limits
- **Retry logic:** Exponential backoff with quota awareness

### Docker Optimization
Multi-stage builds to minimize image size:
```
Stage 1 (build): 415MB - Install build tools, compile dependencies
Stage 2 (runtime): 172MB - Copy only runtime binaries
```

**Key Challenge:** Pinning exact dependency versions (pwntools 4.15, openai 2.53, mcp 2.0) to avoid pip backtracker failures.

## Key Lessons Learned

### Expensive Feedback Cycles
**Problem:** Each agent run took ~1 hour, with only 3-4 live runs possible before quota risk.

**Solution:**
- Comprehensive test harnesses for local validation
- Dry-run mode with mocked MCP endpoints
- Careful flag format validation before submission

### Quota Management
**Problem:** 25 wrong answers per 2-hour window across all challenges.

**Solution:**
- Deterministic solvers preferred over brute-force
- LLM fallbacks only when deterministic fails
- Submit-safety checks (no spray-and-pray)

### LLM-in-the-Loop
**Problem:** Some challenges required reasoning that deterministic code couldn't handle.

**Solution:**
- Hybrid approach: deterministic solver + LLM fallback
- Structured prompts with clear success/failure criteria
- Parse LLM output defensively (JSON schema validation)

[Full Lessons Learned](https://github.com/sakebomb/halctf/blob/main/docs/writeups/lessons-learned.md)

## Agent Repositories

All agents are in the main repository under `agents/`:

1. **hacman-agent** - Simple LLM explorer
2. **kanto-agent** - Multi-solver with SAT, crypto, SSRF
3. **rogue-agent** - LLM jailbreaking with transport discovery
4. **odyssey-agent** - 6 specialized puzzle solvers
5. **labyrinth-agent** - 9 diverse CTF training solvers
6. **pantheon-agent** - General purpose (partially implemented)

## Reusable Components

### Tools
- [Test Harness](https://github.com/sakebomb/halctf/blob/main/scripts/test_harness.py) - Mock MCP environment for local testing
- [Agent Verification](https://github.com/sakebomb/halctf/blob/main/scripts/verify_agent.py) - Smoke tests before upload
- [Build Script](https://github.com/sakebomb/halctf/blob/main/scripts/build.sh) - Standardized Docker builds

### Patterns
- ReAct loop implementation
- MCP client wrapper
- Conversation memory management
- LLM fallback pattern (deterministic → LLM → fail)
- Quota-aware retry logic

## Statistics

- **Total Python files:** 71
- **Total Dockerfiles:** 6
- **Lines of code:** ~28,000
- **Writeup documentation:** 10 comprehensive markdown files
- **Agent versions:** 13 iterations for Kanto alone

## Technology Stack

- **Language:** Python 3.12
- **Container:** Docker (multi-stage builds)
- **LLM:** OpenAI-compatible endpoints (llama-3.1-8b, qwen3.6-35b, gemma-4-26b)
- **Protocol:** Model Context Protocol (MCP)
- **Exploitation:** pwntools, requests, custom solvers
- **Math:** z3 (SAT), ecdsa, pycosat

## Links

- **Full Repository:** [github.com/sakebomb/halctf](https://github.com/sakebomb/halctf)
- **Writeups:** [docs/writeups/](https://github.com/sakebomb/halctf/tree/main/docs/writeups)
- **Agent Code:** [agents/](https://github.com/sakebomb/halctf/tree/main/agents)
- **Deployment Guide:** [docs/guides/deployment-guide.md](https://github.com/sakebomb/halctf/blob/main/docs/guides/deployment-guide.md)
- **Publishing Checklist:** [CTF_PUBLISHING_CHECKLIST.md](https://github.com/sakebomb/halctf/blob/main/CTF_PUBLISHING_CHECKLIST.md)

---

**Back to:** [CTF Portfolio Index](../../README.md)
