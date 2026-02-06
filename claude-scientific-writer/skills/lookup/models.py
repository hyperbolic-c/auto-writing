"""
Data models for literature lookup.
"""

from dataclasses import dataclass, field
from typing import Literal, Optional
from datetime import datetime


@dataclass
class PaperEntry:
    """Single paper entry"""
    # Unique identifier
    key: str
    source_item_key: Optional[str] = None

    # Core metadata
    title: str
    authors: list[str]
    year: int
    journal: Optional[str] = None

    # Identifiers
    doi: Optional[str] = None
    url: Optional[str] = None

    # Additional info
    abstract: Optional[str] = None
    tags: Optional[list[str]] = None

    # BibTeX citation
    bibtex: str = ""

    # Quality metrics (research-lookup only)
    citation_count: Optional[int] = None
    venue_tier: Optional[str] = None


@dataclass
class SearchOptions:
    """Search options"""
    limit: int = 10
    include_abstract: bool = True
    fallback_enabled: bool = True
    min_results_threshold: int = 1  # Only 0 results triggers fallback


@dataclass
class FallbackInfo:
    """Fallback information"""
    triggered: bool = False
    reason: Optional[str] = None
    external_results_count: int = 0
    external_source: Optional[str] = None


@dataclass
class SearchResult:
    """Search result container"""
    papers: list[PaperEntry] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class StandardLiteratureResult:
    """Unified search result"""
    query: str
    source: Literal["zotero", "research-lookup", "none"]
    papers: list[PaperEntry]
    total_count: int
    search_performed: Literal["local_only", "local_with_fallback"]
    fallback_info: FallbackInfo = field(default_factory=FallbackInfo)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return self.total_count > 0

    @property
    def local_count(self) -> int:
        """Count of local (Zotero) papers"""
        return sum(1 for p in self.papers if self.source == "zotero" or
                   (self.fallback_info.triggered and
                    self.papers.index(p) < self.fallback_info.external_results_count))
