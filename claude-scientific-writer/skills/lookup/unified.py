"""
Unified literature lookup interface.
"""

from typing import Optional
from .models import (
    StandardLiteratureResult,
    SearchOptions,
    LookupConfig,
    PaperEntry,
    FallbackInfo,
)
from .config import LookupConfig
from .adapters import ZoteroAdapter, ResearchAdapter
from .fallback import decide_fallback, FallbackReason
from .messages import LookupLogger


class UnifiedLiteratureLookup:
    """
    Unified interface for literature search.

    Primary: Zotero local library (zotero-mcp)
    Fallback: External search (research-lookup) when configured
    """

    def __init__(
        self,
        config: Optional[LookupConfig] = None,
        verbose: bool = False
    ):
        self.config = config or LookupConfig.load()
        self.logger = LookupLogger(verbose=verbose)
        self._zotero_adapter = None
        self._research_adapter = None

    @property
    def zotero_adapter(self) -> Optional[ZoteroAdapter]:
        """Lazy-load Zotero adapter"""
        if self._zotero_adapter is None:
            self._zotero_adapter = ZoteroAdapter()
            if not self._zotero_adapter.is_available():
                self._zotero_adapter = None
        return self._zotero_adapter

    @property
    def research_adapter(self) -> Optional[ResearchAdapter]:
        """Lazy-load Research-Lookup adapter"""
        if self._research_adapter is None:
            self._research_adapter = ResearchAdapter()
            if not self._research_adapter.is_available():
                self._research_adapter = None
        return self._research_adapter

    @property
    def external_available(self) -> bool:
        """Check if external search is available"""
        return self.research_adapter is not None

    def search(
        self,
        query: str,
        options: Optional[SearchOptions] = None
    ) -> StandardLiteratureResult:
        """
        Search for literature.

        Flow:
        1. Search local Zotero library first
        2. If 0 results and external is available, fallback
        3. Return unified result format
        """
        options = options or SearchOptions()
        errors = []

        # Step 1: Local search
        self.logger.local_search_start(query)
        local_result = self._search_local(query, options)
        errors.extend(local_result.errors)

        if local_result.errors:
            self.logger.log(
                f"Local search warning: {local_result.errors[0]}",
                "warning"
            )

        # Step 2: Check if fallback needed
        decision = decide_fallback(
            local_count=local_result.total_count,
            external_available=self.external_available,
            fallback_on_empty=self.config.research_lookup.fallback_on_empty
        )

        if decision.should_fallback:
            self.logger.fallback_triggered()
            return self._search_with_fallback(
                query, options, local_result, errors
            )

        # No fallback - return local results
        if local_result.total_count > 0:
            self.logger.local_search_found(local_result.total_count)
        else:
            self.logger.local_search_empty()
            self.logger.fallback_not_available()

        self.logger.search_complete(local_result.total_count)

        return local_result

    def batch_search(
        self,
        queries: list[str],
        options: Optional[SearchOptions] = None
    ) -> list[StandardLiteratureResult]:
        """Batch search - each query processed independently"""
        return [self.search(q, options) for q in queries]

    def _search_local(
        self,
        query: str,
        options: SearchOptions
    ) -> StandardLiteratureResult:
        """Search local Zotero library"""
        if self.zotero_adapter is None:
            return StandardLiteratureResult(
                query=query,
                source="none",
                papers=[],
                total_count=0,
                search_performed="local_only",
                errors=["Zotero not available"]
            )

        try:
            # Prefer semantic search
            if self.config.zotero.prefer_semantic_search:
                result = self.zotero_adapter.semantic_search(
                    query=query,
                    limit=options.limit
                )
            else:
                result = self.zotero_adapter.keyword_search(
                    query=query,
                    limit=options.limit
                )

            # Sort by year (descending)
            papers = sorted(result.papers, key=lambda p: p.year, reverse=True)

            return StandardLiteratureResult(
                query=query,
                source="zotero",
                papers=papers,
                total_count=len(papers),
                search_performed="local_only"
            )

        except Exception as e:
            return StandardLiteratureResult(
                query=query,
                source="none",
                papers=[],
                total_count=0,
                search_performed="local_only",
                errors=[f"Local search failed: {str(e)}"]
            )

    def _search_with_fallback(
        self,
        query: str,
        options: SearchOptions,
        local_result: StandardLiteratureResult,
        existing_errors: list[str]
    ) -> StandardLiteratureResult:
        """Search with fallback to external"""
        errors = list(existing_errors)

        # External search
        external_result = self._search_external(query)
        if external_result.errors:
            errors.extend(external_result.errors)

        # Combine: local first, then external
        combined_papers = local_result.papers + external_result.papers

        # Update fallback info
        fallback_info = FallbackInfo(
            triggered=True,
            reason="local_results_empty",
            external_results_count=external_result.total_count,
            external_source="research-lookup"
        )

        # Log results
        if external_result.total_count > 0:
            self.logger.fallback_success(external_result.total_count)
        else:
            self.logger.fallback_failed(external_result.errors[0] if external_result.errors else "Unknown")

        self.logger.search_complete(len(combined_papers))

        return StandardLiteratureResult(
            query=query,
            source="zotero",
            papers=combined_papers,
            total_count=len(combined_papers),
            search_performed="local_with_fallback",
            fallback_info=fallback_info,
            errors=errors
        )

    def _search_external(self, query: str) -> StandardLiteratureResult:
        """External search (research-lookup)"""
        if self.research_adapter is None:
            return StandardLiteratureResult(
                query=query,
                source="none",
                papers=[],
                total_count=0,
                errors=["External search not available"]
            )

        try:
            result = self.research_adapter.search(query)

            return StandardLiteratureResult(
                query=query,
                source="research-lookup",
                papers=result.papers,
                total_count=len(result.papers),
                search_performed="local_with_fallback",
                fallback_info=FallbackInfo(
                    triggered=True,
                    reason="local_results_empty"
                )
            )

        except Exception as e:
            return StandardLiteratureResult(
                query=query,
                source="none",
                papers=[],
                total_count=0,
                errors=[f"External search failed: {str(e)}"]
            )

    def get_citations_for_writing(
        self,
        queries: list[str],
        options: Optional[SearchOptions] = None
    ) -> list[PaperEntry]:
        """
        Get all papers from multiple queries for writing.

        Returns deduplicated list of papers.
        """
        options = options or SearchOptions()
        all_papers = []
        seen_keys = set()

        for query in queries:
            result = self.search(query, options)

            for paper in result.papers:
                # Deduplicate by key
                if paper.key not in seen_keys:
                    seen_keys.add(paper.key)
                    all_papers.append(paper)

            # Log for writing
            self.logger.writing_with(len(all_papers))

        # Sort by year (descending)
        all_papers.sort(key=lambda p: p.year, reverse=True)

        return all_papers
