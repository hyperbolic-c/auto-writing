#!/usr/bin/env python3
"""Semantic Scholar lookup tool for research writing evidence packs.

Implements strict global throttling below 1 request/second across all endpoints.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from urllib import error, parse, request
import ssl


# Create SSL context that doesn't verify certificates (for systems with outdated certs)
_ssl_context = ssl.create_default_context()
_ssl_context.check_hostname = False
_ssl_context.verify_mode = ssl.CERT_NONE


GRAPH_BASE = "https://api.semanticscholar.org/graph/v1"
RECOMMEND_BASE = "https://api.semanticscholar.org/recommendations/v1"

DEFAULT_FIELDS = [
    "paperId",
    "title",
    "abstract",
    "authors",
    "year",
    "venue",
    "citationCount",
    "externalIds",
    "url",
    "tldr",
]

TIER1_VENUE_TOKENS = {
    "nature",
    "science",
    "cell",
    "nejm",
    "new england journal of medicine",
    "lancet",
    "jama",
    "nature medicine",
    "nature biotechnology",
}


@dataclass
class RequestStats:
    total_requests: int = 0
    retry_429_count: int = 0
    retry_5xx_count: int = 0
    slept_seconds: float = 0.0


class GlobalRateLimiter:
    """Process-wide limiter for all API calls."""

    def __init__(self, rps: float = 0.8) -> None:
        if rps <= 0:
            raise ValueError("rps must be > 0")
        self.min_interval = 1.0 / rps
        self._lock = threading.Lock()
        self._last_request_ts = 0.0

    def acquire(self) -> float:
        """Block until request can proceed. Returns sleep seconds."""
        slept = 0.0
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_request_ts
            if elapsed < self.min_interval:
                slept = self.min_interval - elapsed
                time.sleep(slept)
            self._last_request_ts = time.monotonic()
        return slept


class SemanticScholarClient:
    def __init__(
        self,
        api_key: Optional[str],
        rps: float = 0.8,
        timeout_s: int = 35,
        max_retries: int = 3,
    ) -> None:
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.stats = RequestStats()
        self._limiter = GlobalRateLimiter(rps=rps)

    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json", "User-Agent": "semantic-scholar-lookup/1.0"}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        return headers

    def _parse_retry_after(self, value: Optional[str], default_s: float) -> float:
        if not value:
            return default_s
        try:
            return max(float(value), default_s)
        except ValueError:
            return default_s

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        last_error = "unknown"
        for attempt in range(self.max_retries + 1):
            slept = self._limiter.acquire()
            self.stats.slept_seconds += slept
            self.stats.total_requests += 1

            req_url = url
            if params:
                req_url = f"{url}?{parse.urlencode(params)}"
            req_data = None
            if json_body is not None:
                req_data = json.dumps(json_body).encode("utf-8")

            req_headers = self._headers()
            if req_data is not None:
                req_headers["Content-Type"] = "application/json"

            req = request.Request(req_url, data=req_data, headers=req_headers, method=method.upper())

            try:
                with request.urlopen(req, timeout=self.timeout_s, context=_ssl_context) as resp:
                    status_code = resp.getcode()
                    raw_body = resp.read().decode("utf-8", errors="replace")
                    resp_headers = resp.headers
            except error.HTTPError as exc:
                status_code = exc.code
                raw_body = exc.read().decode("utf-8", errors="replace")
                resp_headers = exc.headers
            except error.URLError as exc:
                last_error = str(exc)
                if attempt >= self.max_retries:
                    break
                backoff = min(8.0, 2.0 ** (attempt + 1))
                time.sleep(backoff)
                self.stats.slept_seconds += backoff
                continue

            if status_code == 429:
                self.stats.retry_429_count += 1
                if attempt >= self.max_retries:
                    return {
                        "error": "rate_limited",
                        "status_code": 429,
                        "body": raw_body[:500],
                    }
                retry_after = self._parse_retry_after(resp_headers.get("Retry-After"), 2.0 ** (attempt + 1))
                time.sleep(retry_after)
                self.stats.slept_seconds += retry_after
                continue

            if 500 <= status_code < 600:
                self.stats.retry_5xx_count += 1
                if attempt >= self.max_retries:
                    return {
                        "error": "server_error",
                        "status_code": status_code,
                        "body": raw_body[:500],
                    }
                backoff = min(8.0, 2.0 ** (attempt + 1))
                time.sleep(backoff)
                self.stats.slept_seconds += backoff
                continue

            if status_code >= 400:
                return {
                    "error": "client_error",
                    "status_code": status_code,
                    "body": raw_body[:500],
                }

            try:
                return json.loads(raw_body)
            except ValueError:
                return {"error": "invalid_json", "status_code": status_code, "body": raw_body[:500]}

        return {"error": "request_failed", "detail": last_error}

    def search_papers(
        self,
        query: str,
        *,
        limit: int = 100,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "query": query,
            "limit": max(1, min(limit, 100)),
            "fields": ",".join(fields or DEFAULT_FIELDS),
        }
        if year_from and year_to:
            params["year"] = f"{year_from}-{year_to}"
        elif year_from:
            params["year"] = f"{year_from}-"
        elif year_to:
            params["year"] = f"-{year_to}"

        return self._request("GET", f"{GRAPH_BASE}/paper/search", params=params)

    def batch_papers(self, paper_ids: List[str], fields: Optional[List[str]] = None) -> Dict[str, Any]:
        if not paper_ids:
            return {"data": []}
        params = {"fields": ",".join(fields or DEFAULT_FIELDS)}
        return self._request("POST", f"{GRAPH_BASE}/paper/batch", params=params, json_body={"ids": paper_ids})

    def recommendations_for_paper(
        self,
        paper_id: str,
        *,
        limit: int = 10,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        params = {
            "limit": max(1, min(limit, 50)),
            "fields": ",".join(fields or DEFAULT_FIELDS),
        }
        return self._request("GET", f"{RECOMMEND_BASE}/papers/forpaper/{paper_id}", params=params)


class EvidenceBuilder:
    def __init__(self) -> None:
        pass

    def _norm(self, text: str) -> str:
        return " ".join((text or "").lower().split())

    def _traceable(self, paper: Dict[str, Any]) -> bool:
        external = paper.get("externalIds") or {}
        return bool(paper.get("paperId") or external.get("DOI") or paper.get("url"))

    def _venue_score(self, venue: Optional[str]) -> float:
        if not venue:
            return 0.2
        lv = venue.lower()
        return 1.0 if any(tok in lv for tok in TIER1_VENUE_TOKENS) else 0.5

    def _recency_score(self, year: Optional[int], current_year: int) -> float:
        if not year:
            return 0.0
        age = max(0, current_year - year)
        if age <= 2:
            return 1.0
        if age <= 5:
            return 0.8
        if age <= 10:
            return 0.5
        return 0.2

    def _impact_score(self, citation_count: Optional[int]) -> float:
        if not citation_count or citation_count <= 0:
            return 0.0
        return min(1.0, math.log10(citation_count + 1) / 4.0)

    def _relevance_score(self, paper: Dict[str, Any], rank: int, total: int) -> float:
        api_score = paper.get("score")
        if isinstance(api_score, (int, float)):
            return max(0.0, min(float(api_score), 1.0))
        if total <= 1:
            return 1.0
        return 1.0 - (rank / float(total))

    def dedupe(self, papers: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen: set[str] = set()
        output: List[Dict[str, Any]] = []
        for paper in papers:
            external = paper.get("externalIds") or {}
            key = paper.get("paperId") or external.get("DOI") or self._norm(paper.get("title", ""))
            if not key or key in seen:
                continue
            seen.add(key)
            output.append(paper)
        return output

    def rank(self, papers: List[Dict[str, Any]], current_year: int) -> List[Dict[str, Any]]:
        total = max(1, len(papers))
        ranked: List[Tuple[float, Dict[str, Any]]] = []

        for idx, paper in enumerate(papers):
            relevance = self._relevance_score(paper, idx, total)
            recency = self._recency_score(paper.get("year"), current_year)
            impact = self._impact_score(paper.get("citationCount"))
            venue_quality = self._venue_score(paper.get("venue"))
            final_score = 0.55 * relevance + 0.20 * recency + 0.15 * impact + 0.10 * venue_quality
            paper["_scores"] = {
                "relevance": round(relevance, 4),
                "recency": round(recency, 4),
                "citation_impact": round(impact, 4),
                "venue_quality": round(venue_quality, 4),
                "final_score": round(final_score, 4),
            }
            ranked.append((final_score, paper))

        ranked.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in ranked]

    def _excerpt(self, text: str, max_len: int = 240) -> str:
        text = " ".join((text or "").split())
        if len(text) <= max_len:
            return text
        return text[: max_len - 3] + "..."

    def build_output(self, query: str, ranked: List[Dict[str, Any]], top_n: int, stats: RequestStats) -> Dict[str, Any]:
        chosen = ranked[:top_n]
        citations: List[Dict[str, Any]] = []
        evidence_points: List[Dict[str, Any]] = []
        traceable_count = 0

        for paper in chosen:
            if self._traceable(paper):
                traceable_count += 1
            external = paper.get("externalIds") or {}
            doi = external.get("DOI")
            claim = paper.get("tldr", {}).get("text") if isinstance(paper.get("tldr"), dict) else None
            if not claim:
                claim = self._excerpt(paper.get("abstract") or "")

            citation = {
                "paperId": paper.get("paperId"),
                "title": paper.get("title"),
                "authors": [a.get("name") for a in paper.get("authors", []) if isinstance(a, dict) and a.get("name")],
                "year": paper.get("year"),
                "venue": paper.get("venue"),
                "citationCount": paper.get("citationCount"),
                "externalIds": external,
                "doi": doi,
                "url": paper.get("url") or (f"https://www.semanticscholar.org/paper/{paper.get('paperId')}" if paper.get("paperId") else None),
                "scores": paper.get("_scores", {}),
                "traceable": self._traceable(paper),
            }
            citations.append(citation)

            evidence_points.append(
                {
                    "paperId": paper.get("paperId"),
                    "title": paper.get("title"),
                    "claim": claim,
                    "why_selected": (
                        "high relevance + recency"
                        if citation["scores"].get("recency", 0.0) >= 0.8
                        else "high relevance + impact"
                    ),
                    "traceable": citation["traceable"],
                }
            )

        traceability_report = {
            "total_selected": len(chosen),
            "traceable_selected": traceable_count,
            "strict_traceability_pass": traceable_count == len(chosen),
        }

        return {
            "query_summary": {
                "query": query,
                "selected_papers": len(chosen),
                "notes": "Strict traceability enabled: papers without stable IDs are marked and can be filtered out.",
            },
            "candidate_papers": chosen,
            "evidence_points": evidence_points,
            "citations": citations,
            "limitations": self._limitations(chosen),
            "traceability_report": traceability_report,
            "rate_limit_status": {
                "target_rps": 0.8,
                "total_requests": stats.total_requests,
                "retry_429_count": stats.retry_429_count,
                "retry_5xx_count": stats.retry_5xx_count,
                "slept_seconds": round(stats.slept_seconds, 3),
            },
        }

    def _limitations(self, papers: List[Dict[str, Any]]) -> List[str]:
        limits: List[str] = []
        missing_abstract = sum(1 for p in papers if not p.get("abstract"))
        missing_doi = sum(1 for p in papers if not (p.get("externalIds") or {}).get("DOI"))
        if missing_abstract:
            limits.append(f"{missing_abstract} selected papers lack abstracts; claim extraction may be weaker.")
        if missing_doi:
            limits.append(f"{missing_doi} selected papers lack DOI; fallback identifiers were used.")
        if not limits:
            limits.append("No major metadata gaps detected in selected papers.")
        return limits


def _markdown_report(payload: Dict[str, Any]) -> str:
    lines: List[str] = []
    summary = payload.get("query_summary", {})
    lines.append("## Query")
    lines.append(str(summary.get("query", "")))
    lines.append("")

    lines.append("## Top Evidence")
    for idx, ev in enumerate(payload.get("evidence_points", []), start=1):
        lines.append(f"### {idx}) {ev.get('title', 'Untitled')}")
        lines.append(f"- paperId: {ev.get('paperId')}")
        lines.append(f"- traceable: {ev.get('traceable')}")
        lines.append(f"- why_selected: {ev.get('why_selected')}")
        lines.append(f"- claim: {ev.get('claim')}")

    lines.append("")
    lines.append("## Citations")
    for idx, c in enumerate(payload.get("citations", []), start=1):
        author_text = ", ".join(c.get("authors") or [])
        lines.append(
            f"{idx}. {author_text} ({c.get('year')}). {c.get('title')}. {c.get('venue')}. DOI: {c.get('doi') or 'N/A'} URL: {c.get('url')}"
        )

    lines.append("")
    lines.append("## Limitations")
    for item in payload.get("limitations", []):
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Rate Limit Status")
    r = payload.get("rate_limit_status", {})
    lines.append(f"- target_rps: {r.get('target_rps')}")
    lines.append(f"- total_requests: {r.get('total_requests')}")
    lines.append(f"- retry_429_count: {r.get('retry_429_count')}")
    lines.append(f"- slept_seconds: {r.get('slept_seconds')}")
    return "\n".join(lines)


def run_lookup(
    query: str,
    *,
    api_key: Optional[str],
    top_n: int,
    search_limit: int,
    year_from: Optional[int],
    year_to: Optional[int],
    include_recommendations: bool,
    seed_count: int,
    strict_traceability: bool,
) -> Dict[str, Any]:
    client = SemanticScholarClient(api_key=api_key, rps=0.8)
    builder = EvidenceBuilder()

    search = client.search_papers(query, limit=search_limit, year_from=year_from, year_to=year_to)
    if search.get("error"):
        return {"error": "search_failed", "detail": search}

    candidates = search.get("data", [])

    # Batch hydrate top search IDs to keep metadata consistent while minimizing request count.
    top_ids = [p.get("paperId") for p in candidates[: min(len(candidates), search_limit)] if p.get("paperId")]
    hydrated: List[Dict[str, Any]] = []
    if top_ids:
        batch = client.batch_papers(top_ids, fields=DEFAULT_FIELDS)
        # batch API returns list directly, not {"data": [...]}
        if isinstance(batch, list):
            hydrated = batch
        elif isinstance(batch, dict) and not batch.get("error"):
            hydrated = batch.get("data", [])

    merged = hydrated if hydrated else candidates

    if include_recommendations:
        seed_ids = [p.get("paperId") for p in merged[:seed_count] if p.get("paperId")]
        for seed in seed_ids:
            rec = client.recommendations_for_paper(seed, limit=8, fields=DEFAULT_FIELDS)
            # Handle both dict and list responses
            if isinstance(rec, list):
                rec_data = rec
            elif isinstance(rec, dict):
                if rec.get("error"):
                    continue
                rec_data = rec.get("recommendedPapers") or rec.get("data") or []
            else:
                rec_data = []
            merged.extend(rec_data)

    deduped = builder.dedupe(merged)
    ranked = builder.rank(deduped, current_year=2026)

    if strict_traceability:
        ranked = [p for p in ranked if builder._traceable(p)]

    return builder.build_output(query=query, ranked=ranked, top_n=top_n, stats=client.stats)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Semantic Scholar lookup for research writing evidence.")
    parser.add_argument("query", help="Research query")
    parser.add_argument("--limit", type=int, default=12, help="Final number of papers in evidence pack")
    parser.add_argument("--search-limit", type=int, default=100, help="Search recall size (1-100)")
    parser.add_argument("--year-from", type=int, default=None)
    parser.add_argument("--year-to", type=int, default=None)
    parser.add_argument("--seed-count", type=int, default=2, help="Seed papers for recommendations")
    parser.add_argument("--no-recommendations", action="store_true", help="Disable recommendation expansion")
    parser.add_argument("--non-strict-traceability", action="store_true", help="Allow non-traceable papers")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("-o", "--output", help="Output file path")
    return parser


def _load_dotenv() -> None:
    """Load .env file from current directory or parent directories."""
    directory = os.path.abspath(".")
    for _ in range(5):
        env_path = os.path.join(directory, ".env")
        if os.path.isfile(env_path):
            with open(env_path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and key not in os.environ:
                            os.environ[key] = value
            break
        parent = os.path.dirname(directory)
        if parent == directory:
            break
        directory = parent


def main() -> int:
    args = build_parser().parse_args()
    _load_dotenv()
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if not api_key:
        print(
            "Warning: SEMANTIC_SCHOLAR_API_KEY not set. Running in anonymous mode "
            "(stricter rate limits apply).\n"
            "To configure: create a .env file with SEMANTIC_SCHOLAR_API_KEY=your-key\n"
            "or run: export SEMANTIC_SCHOLAR_API_KEY=your-key\n"
            "Get a free key at: https://www.semanticscholar.org/product/api#api-key-form\n",
            file=sys.stderr,
        )

    result = run_lookup(
        args.query,
        api_key=api_key,
        top_n=max(1, min(args.limit, 50)),
        search_limit=max(1, min(args.search_limit, 100)),
        year_from=args.year_from,
        year_to=args.year_to,
        include_recommendations=not args.no_recommendations,
        seed_count=max(1, min(args.seed_count, 5)),
        strict_traceability=not args.non_strict_traceability,
    )

    if result.get("error"):
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(text)
        else:
            print(text)
        return 1

    out_text = json.dumps(result, ensure_ascii=False, indent=2) if args.json else _markdown_report(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out_text)
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
