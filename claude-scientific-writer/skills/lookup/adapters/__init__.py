"""
Adapters for different literature search backends.
"""

from .zotero_adapter import ZoteroAdapter
from .research_adapter import ResearchAdapter

__all__ = ["ZoteroAdapter", "ResearchAdapter"]
