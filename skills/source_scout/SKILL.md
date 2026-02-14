# Source Scout Skill

## Purpose
Collect raw posts/items from public sources and normalize them into a shared `RawItem` schema.

## Inputs
- config: sources to scan, limits per source, recency window (optional)

## Outputs
- List[RawItem] normalized items

## RawItem Schema
- `source` (string)
- `source_type` (`api` | `rss`)
- `title` (required)
- `url` (required)
- `text` (string, default empty)
- `author` (optional)
- `created_at` (optional)
- `score` (optional)
- `comments_count` (optional)
- `tags` (list[string])
- `extra` (object)

## Normalization rules
- Always provide: source, source_type, title, url, text, tags
- created_at/score/comments_count are optional and null if unknown
- Put source-specific fields in extra

## Sources (initial)
- Hacker News (Algolia API)
- RSS feeds (Reddit RSS, Product Hunt RSS, etc.)

## Quality bar
- No empty titles/urls
- Deduplicate by url (best-effort)

## Failure handling
- If one source fails, continue others and return partial results
