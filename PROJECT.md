# PROJECT.md — Customer Pain-Point Scout Agent (Skills-based)

## Goal
Build a personal “customer agent” that:
1) scans multiple internet resources to identify ongoing pain points people are facing,
2) evaluates whether it’s feasible to build *agents* to solve those pain points,
3) produces a report **every other day** as an **Excel (.xlsx)** sheet.

Primary outcome: a repeatable pipeline that generates actionable “agent ideas” from real user pain.

---

## Working Style
- Build in **small milestones** (one working step at a time).
- Prefer **simple Python scripts first**, then modularize into “skills”.
- Keep the repo as the source of truth for context and decisions so we can switch between chats/tools (ChatGPT ↔ Cline) without losing continuity.

---

## Tech Stack (chosen so far)
- **Editor:** VS Code
- **Version control:** Git + GitHub
- **Language:** Python (fast iteration for web collection + normalization + Excel generation)
- **LLM:** OpenAI model (selected later per task; start with a strong general model for extraction/classification)
- **Output:** Excel via `openpyxl` (or pandas → xlsx)
- **Scheduling:** to be added later (cron / GitHub Actions / local scheduler)

---

## “Skills” Approach
We will modularize the agent into reusable skills (folders). Each skill has:
- `SKILL.md` describing purpose, inputs/outputs, rules, and failure handling
- code implementing the skill
- optional examples/templates

Planned skills:
1) **Source Scout** (FIRST) — collect posts/items from sources and normalize them
2) **Pain Point Extractor** — convert messy posts into crisp pain statements + tags/persona
3) **Feasibility Rater** — score “agent-ability” + complexity + data/tool needs + risks
4) **Deduper & Clusterer** — merge similar ideas into themes
5) **Excel Reporter** — output standardized formatted .xlsx

---

## Milestones

### Milestone 1 — Source Scout (MVP)
**Objective:** Pull items from a few sources with no auth, normalize into a common schema, and save as JSON.

**Initial sources (no auth):**
- Hacker News via Algolia API (`tags=front_page`)
- Reddit via RSS (e.g., r/SaaS new feed)
- Product Hunt via RSS feed

**Output file:**
- `data/raw_items.json` — list of normalized `RawItem`s

**Normalization schema (RawItem):**
- `source` (e.g., "hn", "reddit_rss_saas", "producthunt_rss")
- `source_type` ("api" | "rss")
- `title` (required)
- `url` (required)
- `text` (snippet/summary if present, else "")
- `author` (optional)
- `created_at` (optional string; ISO preferred but not required initially)
- `score` (optional; HN points, etc.)
- `comments_count` (optional)
- `tags` (list of strings)
- `extra` (dict for source-specific fields)

**Rules:**
- Drop items missing title or url
- Best-effort dedupe by url
- If one source fails, continue others and return partial results

---

### Milestone 2 — Quality + Targeting
- Add `config.yaml` (sources, per-source limits, subreddits, keywords)
- Add recency filtering (e.g., last 48 hours where available)
- Add caching to avoid re-fetching the same items repeatedly
- Add basic rate limiting / polite fetching

---

### Milestone 3 — Pain Point Extraction
- Use an LLM prompt + guardrails to extract:
  - problem statement (1–2 lines)
  - persona (who has the problem)
  - urgency signals
  - category tags
- Store output as `data/pain_points.json` linked back to raw items.

---

### Milestone 4 — Feasibility Scoring (Agent-ability)
- Create a rubric and score fields:
  - agent feasibility (0–10)
  - complexity (L/M/H)
  - data/tools required
  - automation potential
  - risks / constraints (privacy, ToS, integrations)
  - monetization idea
  - confidence
- Store output as `data/ideas_scored.json`.

---

### Milestone 5 — Excel Report + Formatting
- Export to `.xlsx` every other day
- Columns (draft):
  - Date
  - Source
  - Link
  - Pain point
  - Persona
  - Suggested agent solution
  - Feasibility score
  - Complexity
  - Required tools/data
  - Monetization
  - Notes / risks
  - Confidence

---

### Milestone 6 — Automation
- Run schedule: every other day
- Options: cron / GitHub Actions / local scheduled task
- Keep history: compare new vs last report, show deltas

---

## Repo Structure (target)
