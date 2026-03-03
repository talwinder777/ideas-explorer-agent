# ROADMAP

Last updated: 2026-03-02
Current branch: sourceScout
Current phase: OpenAI integration for pain-signal evaluation

## Milestone Tracker

Progress: **3 / 6 complete**

| Milestone | Status | Notes |
|---|---|---|
| M1 Source Scout MVP | DONE | Initial raw item collection implemented |
| M2 Restructure to new architecture | DONE | Core code moved/reused in `app/` and `agents/` |
| M3 Reddit-only run path stabilization | DONE | New and compatibility entrypoints validated |
| M4 LLM Pain Signal skill | IN PROGRESS | OpenAI client, prompts, config, and tests added |
| M5 Opportunity analysis/ranking | PLANNED | To be implemented in `app/opportunity_analysis/` |
| M6 Reporting & automation | PLANNED | JSON + XLSX + schedule |

## High-Level Architecture

```mermaid
flowchart LR
    A[Reddit RSS Scout\napp/idea_scraper] --> B[Raw Items JSON\ndata/raw_items.json]
    B --> C[Pain Signal Filter\napp/idea_filter]
    C --> D[Opportunity Analysis\napp/opportunity_analysis]
    D --> E[Reports\nJSON/XLSX]
```

## Change Log

- 2026-03-01: Started restructure to app/agents-based layout.
- 2026-03-01: Migrated/reused Reddit scraping and model logic.
- 2026-03-01: Added new entrypoints and compatibility wrapper.
- 2026-03-02: Integrated OpenAI-backed `LLMClient` with prompt/schema normalization and fallbacks.
- 2026-03-02: Added config/env controls and unit tests for evaluator + LLM client.

## Next Actions

1. Add LLM-powered pain signal evaluator (OpenAI-backed).
2. Add ranked opportunity analysis output.
3. Add XLSX export and scheduler.
