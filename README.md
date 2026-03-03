# ideas-explorer-agent

Agentic idea scout project for discovering pain-point posts and turning them into potential AI/agent business opportunities.

## Current status

- Restructured to an `app/` + `agents/` architecture.
- Current working pipeline is **Reddit RSS scout** -> normalized JSON output.
- OpenAI-backed `idea_filter` client is integrated for pain-signal evaluation.

## Run

From repo root:

```bash
python -m pip install -r requirements.txt
python -m app.main --reddit-subreddit SaaS --reddit-limit 20 --out data/raw_items.json
```

## OpenAI setup (for pain-signal filtering)

Set environment variables before running LLM-powered evaluation paths:

```bash
set OPENAI_API_KEY=your_api_key_here
set OPENAI_MODEL=gpt-4.1-mini
set OPENAI_TIMEOUT_SECONDS=30
set PAIN_SIGNAL_THRESHOLD=6
```

PowerShell equivalent:

```powershell
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
