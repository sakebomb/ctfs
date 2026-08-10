# CTF Portfolio

Organized solutions, tools, and lessons from capture-the-flag competitions. Focus on teaching problem-solving approaches and building reusable tooling.

**Author:** [sakebomb](https://github.com/sakebomb)

## Featured Projects

### DEF CON 34 - HalCTF (Aug 2026) - 13th Place
**Autonomous AI Agent CTF** - Built 6 specialized agents solving challenges via LLM reasoning, MCP integration, and exploit automation.

[Full Repository](https://github.com/sakebomb/halctf) | [Quick Summary](./defcon/2026-halctf/summary.md)

**Key Challenges Solved:**
- Kanto Region (450pts) - SAT solving, ECDSA forgery, nested SSRF
- Rogue Intelligence - Multi-layer LLM jailbreaking with rotating flags
- Hac-Man (50pts) - LLM-guided magic word discovery
- The Odyssey (5/6 puzzles) - SSRF, XOR crypto, statistical oracles
- Turing's Labyrinth (9 puzzles implemented)

**Tech:** Python, Docker, OpenAI API, Model Context Protocol (MCP), pwntools

**Unique Aspects:**
- All challenges solved by autonomous agents (no human interaction)
- Multi-stage Docker builds (415MB → 172MB optimization)
- ReAct-style reasoning loops
- Quota-aware retry logic (25 wrong answers per 2h window)

---

## All Competitions

Organized **by event, then year** (e.g. `defcon/2024/`, `shmoocon/2025/`). Large challenge
files are archived privately and not included in this repo — the writeup is the deliverable.

| Year | Event | Writeup | Status |
|------|-------|---------|--------|
| 2026 | DEF CON 34 - HalCTF | [Full Repo](https://github.com/sakebomb/halctf) · [dir](./defcon/2026-halctf/) | Complete |
| 2025 | Cyphercon | [writeup](./cyphercon/2025/writeup.md) | Scaffold |
| 2025 | Shmoocon | [writeup](./shmoocon/2025/writeup.md) | Scaffold (notes) |
| 2024 | DEF CON 32 | [writeup](./defcon/2024/writeup.md) | Scaffold |
| 2024 | Cyphercon | [writeup](./cyphercon/2024/writeup.md) | Scaffold |
| 2024 | Chrononaut | [writeup](./chrononaut/2024/writeup.md) | Scaffold |
| 2024 | Shmoocon | [writeup](./shmoocon/2024/writeup.md) | Scaffold (notes) |
| 2023 | DEF CON 31 | [writeup](./defcon/2023/writeup.md) | Scaffold |
| 2023 | Hackfortress | [writeup](./hackfortress/2023/writeup.md) | Scaffold |
| 2022 | DEF CON 30 | [writeup](./defcon/2022/writeup.md) | Scaffold |
| 2022 | Shmoocon | (artifacts only) | Artifacts |
| 2020 | DEF CON 28 Safe Mode | [writeup](./defcon/2020-safemode/writeup.md) | Scaffold |

## By Category

### AI Security
- [HalCTF - Full Competition](./defcon/2026-halctf/) - Autonomous agent development, LLM jailbreaking

### Web Exploitation
- [Kanto - Silph Co](./categories/web.md#silph-co) - Nested SSRF chain
- [Odyssey - Scylla](./categories/web.md#scylla) - SSRF with depth tracking

### Cryptography
- [Kanto - Indigo Plateau](./categories/crypto.md#indigo-plateau) - ECDSA signature forgery
- [Odyssey - Aeolus](./categories/crypto.md#aeolus) - XOR key recovery with known plaintext

### Binary Exploitation
- [Labyrinth - Achilles Heel](./categories/pwn.md#achilles-heel) - Blind ret2win (no binary)

### Miscellaneous
- [Kanto - Cerulean Cave](./categories/misc.md#cerulean-cave) - SAT solver with off-by-one indexing
- [Odyssey - Tiresias](./categories/misc.md#tiresias) - Binary search with signed oracle
- [Odyssey - Cattle](./categories/misc.md#cattle) - Statistical majority vote oracle

## Statistics

- **Competitions:** 1 (2026)
- **Total Points:** 500+ (confirmed)
- **Challenges Solved:** 15+ documented
- **Agent Repositories:** 6 specialized agents
- **Focus Areas:** AI security, autonomous exploitation, web vulnerabilities

## Tools & Resources

### Reusable Tools
- [Agent Framework Template](./tools/agent-template/) - ReAct loop + MCP integration
- [Test Harness](./tools/test-harness/) - Local CTF agent testing
- [Common Patterns](./tools/patterns/) - Frequently used exploit patterns

### Guides
- [Publishing CTF Repos](https://github.com/sakebomb/halctf/blob/main/CTF_PUBLISHING_CHECKLIST.md) - Clean, professional publication workflow
- [Lessons Learned](./lessons-learned.md) - Meta-lessons across competitions

## Philosophy

### Teaching Focus
Writeups emphasize:
- **Problem-solving approach** over just flag dumps
- **Reusable techniques** that transfer to other challenges
- **Failure analysis** - what didn't work and why
- **Tool development** - building for automation and reuse

### Code Quality
All published code includes:
- Comprehensive documentation
- Clean architecture and patterns
- Security disclaimers for CTF-specific unsafe patterns
- Docker-based reproducibility

## Future Competitions

Planning to participate in:
- DEF CON 35 (2027)
- Various online CTFs (as time permits)

**Goal:** 1-3 substantial CTFs per year with high-quality documentation.

## Contact

- **GitHub:** [@sakebomb](https://github.com/sakebomb)
- **Website:** [madx.co](https://madx.co)

## Contributing

Found an error or have a suggestion? Open an issue or PR on the specific repository.

## License

Individual repositories have their own licenses (typically MIT). See each repo for details.

---

**Last Updated:** August 2026 (DEF CON 34 HalCTF)
