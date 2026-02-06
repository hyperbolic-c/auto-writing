"""
Literature Lookup Module

Unified interface for searching literature from multiple sources:
- Zotero local library (zotero-mcp) - primary/default
- External search (research-lookup) - fallback when configured
"""

from .models import (
    PaperEntry,
    SearchOptions,
    FallbackInfo,
    StandardLiteratureResult,
    SearchResult,
)
from .config import LookupConfig
from .unified import UnifiedLiteratureLookup

__all__ = [
    "PaperEntry",
    "SearchOptions",
    "FallbackInfo",
    "StandardLiteratureResult",
    "SearchResult",
    "LookupConfig",
    "UnifiedLiteratureLookup",
]
