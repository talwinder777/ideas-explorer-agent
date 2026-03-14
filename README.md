# ideas-explorer-agent

Agentic idea scout project for discovering pain-point posts and turning them into potential AI/agent business opportunities.

## Current status

- Restructured to an `app/` + `agents/` architecture.
- Current working pipeline is **Reddit RSS scout** -> normalized JSON output.
- Configurable `idea_filter` client now supports both **OpenAI** and **local Ollama** for pain-signal evaluation.

## Run

From repo root:

```bash
python -m pip install -r requirements.txt
python -m app.main --reddit-subreddit SaaS --reddit-limit 20 --out data/raw_items.json
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

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Project tracking

See `ROADMAP.md` for milestone status, architecture diagram, and changelog.
