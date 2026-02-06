"""
Zotero MCP adapter for literature search.
"""

from typing import Optional
from ..models import PaperEntry, SearchResult


class ZoteroAdapter:
    """Adapter for zotero-mcp"""

    def __init__(self):
        self._available = None

    def is_available(self) -> bool:
        """Check if zotero-mcp is available"""
        if self._available is None:
            try:
                # Try to call a simple zotero MCP function
                from zotero_mcp import zotero_get_collections
                zotero_get_collections(limit=1)
                self._available = True
            except Exception:
                self._available = False
        return self._available

    def semantic_search(
        self,
        query: str,
        limit: int = 10
    ) -> SearchResult:
        """
        Semantic search using zotero_semantic_search.

        Returns unified SearchResult.
        """
        try:
            from zotero_mcp import zotero_semantic_search

            result = zotero_semantic_search(query=query, limit=limit)

            # Parse results
            papers = []
            for item in result.get("results", []):
                papers.append(self._parse_item(item))

            return SearchResult(papers=papers)

        except Exception as e:
            return SearchResult(papers=[], errors=[f"Zotero semantic search failed: {str(e)}"])

    def keyword_search(
        self,
        query: str,
        limit: int = 10
    ) -> SearchResult:
        """
        Keyword search using zotero_search_items.

        Uses titleCreatorYear mode.
        """
        try:
            from zotero_mcp import zotero_search_items

            result = zotero_search_items(
                query=query,
                qmode="titleCreatorYear",
                item_type="-attachment",
                limit=limit
            )

            # Parse results
            papers = []
            for item in result.get("results", []):
                papers.append(self._parse_item(item))

            return SearchResult(papers=papers)

        except Exception as e:
            return SearchResult(papers=[], errors=[f"Zotero keyword search failed: {str(e)}"])

    def get_bibtex(self, item_key: str) -> str:
        """Get BibTeX citation for an item"""
        try:
            from zotero_mcp import zotero_get_item_metadata

            result = zotero_get_item_metadata(
                item_key=item_key,
                format="bibtex"
            )
            return result

        except Exception:
            return ""

    def _parse_item(self, item: dict) -> PaperEntry:
        """Parse a zotero item into PaperEntry"""
        # Get item key
        item_key = item.get("key") or item.get("itemKey") or item.get("item_key", "")

        # Get title
        title = item.get("title", item.get("data", {}).get("title", ""))

        # Parse authors
        authors = self._parse_authors(
            item.get("creators", item.get("data", {}).get("creators", []))
        )

        # Parse year
        year = self._parse_year(
            item.get("date", item.get("data", {}).get("date", ""))
        )

        # Parse journal
        journal = (
            item.get("containerTitle") or
            item.get("publicationTitle") or
            item.get("journal", "")
        )

        # Parse DOI
        doi = item.get("DOI", item.get("doi"))

        # Parse abstract
        abstract = item.get("abstractNote", "")

        # Parse tags
        tags = None
        if "tags" in item:
            tags = [t.get("tag", "") for t in item["tags"] if t.get("tag")]
        elif "data" in item and "tags" in item["data"]:
            tags = [t.get("tag", "") for t in item["data"]["tags"] if t.get("tag")]

        # Get BibTeX
        bibtex = ""
        if item_key:
            bibtex = self.get_bibtex(item_key)

        return PaperEntry(
            key=item_key,
            source_item_key=item_key,
            title=title,
            authors=authors,
            year=year,
            journal=journal,
            doi=doi,
            abstract=abstract if abstract else None,
            tags=tags if tags else None,
            bibtex=bibtex,
            url=item.get("url", ""),
        )

    def _parse_authors(self, creators: list) -> list[str]:
        """Parse creators list into author names"""
        authors = []
        for creator in creators:
            if creator.get("creatorType") == "author":
                first_name = creator.get("firstName", "")
                last_name = creator.get("lastName", "")
                name = f"{first_name} {last_name}".strip()
                if name:
                    authors.append(name)
        return authors

    def _parse_year(self, date_str: str) -> int:
        """Extract year from date string"""
        import re
        match = re.search(r"\d{4}", date_str or "")
        return int(match.group()) if match else 0
