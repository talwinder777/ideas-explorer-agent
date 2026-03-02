# ideas-explorer-agent

Agentic idea scout project for discovering pain-point posts and turning them into potential AI/agent business opportunities.

## Current status

- Restructured to an `app/` + `agents/` architecture.
- Current working pipeline is **Reddit RSS scout** -> normalized JSON output.
- Future stages (`idea_filter`, `opportunity_analysis`) are scaffolded and ready for implementation.

## Run

From repo root:

```bash
python -m pip install -r requirements.txt
python -m app.main --reddit-subreddit SaaS --reddit-limit 20 --out data/raw_items.json
```

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
