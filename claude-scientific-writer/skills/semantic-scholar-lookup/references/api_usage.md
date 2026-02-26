# Semantic Scholar API Usage Notes

## Endpoints Used

- `GET /graph/v1/paper/search`
- `POST /graph/v1/paper/batch`
- `GET /recommendations/v1/papers/forpaper/{paper_id}`

## Fields Strategy

Request only required fields to reduce payload size:

- `paperId`
- `title`
- `abstract`
- `authors`
- `year`
- `venue`
- `citationCount`
- `externalIds`
- `url`
- `tldr`

## Rate Limit Policy

Service-level constraint: 1 request/second cumulative across all endpoints.

Implementation defaults:

- Target send rate: `0.8 req/s`
- Minimum interval between any two API requests: `1.25s`
- Retry on `429`: use `Retry-After`; fallback `2s -> 4s -> 8s`
- Retry on `5xx`: `2s -> 4s -> 8s`

## Traceability Policy

A citation is considered traceable if at least one identifier exists:

- `paperId`, or
- `externalIds.DOI`, or
- canonical paper `url`

Default output excludes non-traceable papers.

## Suggested Query Pattern

Use focused topic statements instead of broad keywords, and optionally constrain years:

- Example: `"causal relationship between sleep deprivation and insulin resistance"`
- Add year filter when current evidence is required.
