"""
Research-Lookup adapter for external search.
"""

import re
from typing import Optional
from ..models import PaperEntry, SearchResult


class ResearchAdapter:
    """Adapter for research-lookup (Perplexity Sonar via OpenRouter)"""

    def __init__(self):
        self._available = None

    def is_available(self) -> bool:
        """Check if research-lookup is available"""
        if self._available is None:
            try:
                import os
                if not os.getenv("OPENROUTER_API_KEY"):
                    self._available = False
                    return False

                # Try to initialize ResearchLookup
                from skills.research_lookup.research_lookup import ResearchLookup
                ResearchLookup()
                self._available = True
            except Exception:
                self._available = False
        return self._available

    def search(self, query: str) -> SearchResult:
        """
        External search using ResearchLookup.

        Returns unified SearchResult.
        """
        if not self.is_available():
            return SearchResult(papers=[], errors=["Research-Lookup not available"])

        try:
            from skills.research_lookup.research_lookup import ResearchLookup

            client = ResearchLookup()
            result = client.lookup(query)

            if not result.get("success", False):
                return SearchResult(
                    papers=[],
                    errors=[result.get("error", "Unknown error")]
                )

            # Parse results
            papers = []
            citations = result.get("citations", [])

            for i, citation in enumerate(citations):
                paper = self._parse_citation(citation, i)
                papers.append(paper)

            # Try to get BibTeX for DOIs found
            dois = [p.doi for p in papers if p.doi]
            if dois:
                bibtex_entries = self._fetch_bibtex_from_dois(dois)
                for paper, bibtex in zip(papers, bibtex_entries):
                    if bibtex:
                        paper.bibtex = bibtex

            return SearchResult(papers=papers)

        except Exception as e:
            return SearchResult(papers=[], errors=[f"Research-Lookup failed: {str(e)}"])

    def _parse_citation(self, citation: dict, index: int) -> PaperEntry:
        """Parse a citation into PaperEntry"""
        # Extract title
        title = citation.get("title", "")

        # Extract URL and DOI
        url = citation.get("url", "")
        doi = self._extract_doi(url)

        # Extract date/year
        date_str = citation.get("date", "")
        year = self._parse_year(date_str)

        # Generate citation key
        key = f"external_{index}"

        # Generate basic BibTeX
        bibtex = self._generate_bibtex(citation, key, year)

        return PaperEntry(
            key=key,
            title=title,
            authors=[],  # Research-Lookup doesn't provide authors
            year=year,
            doi=doi,
            url=url,
            bibtex=bibtex,
        )

    def _extract_doi(self, url: str) -> Optional[str]:
        """Extract DOI from URL"""
        if not url:
            return None
        match = re.search(r"10\.\d{4,}/[^\s]+", url)
        return match.group() if match else None

    def _parse_year(self, date_str: str) -> int:
        """Extract year from date string"""
        import re
        match = re.search(r"\d{4}", date_str or "")
        return int(match.group()) if match else 0

    def _generate_bibtex(self, citation: dict, key: str, year: int) -> str:
        """Generate basic BibTeX entry"""
        title = citation.get("title", "").replace("{", "").replace("}", "")
        url = citation.get("url", "")

        if not title:
            return ""

        return f"""@misc{{{key},
  title = {{{title}}},
  year = {{{year}}},
  url = {{{url}}}
}}"""

    def _fetch_bibtex_from_dois(self, dois: list[str]) -> list[str]:
        """Fetch BibTeX entries from DOIs using CrossRef API"""
        import requests

        bibtex_entries = []

        for doi in dois:
            try:
                url = f"https://doi.org/{doi}"
                headers = {"Accept": "application/x-bibtex"}

                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    bibtex_entries.append(response.text.strip())
                else:
                    bibtex_entries.append("")
            except Exception:
                bibtex_entries.append("")

        return bibtex_entries
