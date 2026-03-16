# ideas-explorer-agent

Agentic idea scout project for discovering pain-point posts and turning them into potential AI/agent business opportunities.

## Current status

- Restructured to a compatibility-first architecture with canonical modules in `idea_agent_app/` and `llm_clients/`.
- Existing `app/` paths are preserved as backward-compatible wrappers.
- `agents/idea_agent.py` is now the primary runnable flow for **Reddit RSS scout -> LLM pain-signal filtering**.

## Run

### Primary entrypoint (idea agent)

From repo root:

```bash
python -m agents.idea_agent --reddit-subreddit SaaS --reddit-limit 20 --raw-out data/raw_items.json --out data/pain_candidates.json
```

Include all analyzed rows (not only candidates):

```bash
python -m agents.idea_agent --reddit-subreddit SaaS --reddit-limit 20 --raw-out data/raw_items.json --out data/pain_analysis_all.json --include-all
```

### Top-level dispatcher (future multi-agent)

```bash
python -m main --agent idea_agent --reddit-subreddit SaaS --reddit-limit 20 --raw-out data/raw_items.json --out data/pain_candidates.json
```

### Compatibility entrypoint

From repo root:

```bash
python -m pip install -r requirements.txt
python -m app.main --reddit-subreddit SaaS --reddit-limit 20 --out data/raw_items.json --analyzed-out data/pain_candidates.json
```

## LLM provider setup (for pain-signal filtering)

Set the provider first:

```bash
set LLM_PROVIDER=ollama
```

PowerShell equivalent:

```powershell
$env:LLM_PROVIDER="ollama"
```

### Ollama local setup (recommended for local runs)

Make sure Ollama is running locally and your model is available:

```bash
ollama run qwen3:14b
```

Then set:

```bash
set LLM_PROVIDER=ollama
set OLLAMA_BASE_URL=http://localhost:11434
set OLLAMA_MODEL=qwen3:14b
set OLLAMA_TIMEOUT_SECONDS=180
set PAIN_SIGNAL_THRESHOLD=6
```

PowerShell equivalent:

```powershell
$env:LLM_PROVIDER="ollama"
$env:OLLAMA_BASE_URL="http://localhost:11434"
$env:OLLAMA_MODEL="qwen3:14b"
$env:OLLAMA_TIMEOUT_SECONDS="180"
$env:PAIN_SIGNAL_THRESHOLD="6"
```

### OpenAI setup (optional)

Set environment variables before running LLM-powered evaluation paths:

```bash
set LLM_PROVIDER=openai
set OPENAI_API_KEY=your_api_key_here
set OPENAI_MODEL=gpt-4.1-mini
set OPENAI_TIMEOUT_SECONDS=30
set PAIN_SIGNAL_THRESHOLD=6
```

PowerShell equivalent:

```powershell
$env:LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your_api_key_here"
$env:OPENAI_MODEL="gpt-4.1-mini"
$env:OPENAI_TIMEOUT_SECONDS="30"
$env:PAIN_SIGNAL_THRESHOLD="6"
```

## Run LLM pain-signal analysis

After generating raw items, run:

```bash
python -m scripts.run_pain_filter --in data/raw_items_after_env.json --out data/pain_candidates.json
```

If you want to include every input row (not just candidates):

```bash
python -m scripts.run_pain_filter --in data/raw_items_after_env.json --out data/pain_analysis_all.json --include-all
```

This command explicitly uses the LLM path:
`app.idea_filter.evaluator -> app.idea_filter.llm_client`

Canonical path after restructure:
`idea_agent_app.idea_filter_agent.evaluator -> llm_clients.llm_client`

The evaluator input/output contract is unchanged regardless of provider.

Alternative script entrypoints:

```bash
python -m scripts.run_agent
python -m scripts.run_scraper --reddit-subreddit SaaS --reddit-limit 20 --out data/raw_items.json
```

Backward-compatibility entrypoint (kept temporarily):

```bash
python -m skills.source_scout.run --reddit-subreddit SaaS --reddit-limit 20
```

## Structure notes

- Canonical app package: `idea_agent_app/`
  - `idea_filter_agent/`
  - `idea_scraper/`
  - `opportunity_analysis_agent/`
  - `database/`
  - `models/`
  - `orchestrator/`
- Canonical reusable LLM clients: `llm_clients/`
- Backward-compatible wrappers retained in `app/`.

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Project tracking

See `ROADMAP.md` for milestone status, architecture diagram, and changelog.
