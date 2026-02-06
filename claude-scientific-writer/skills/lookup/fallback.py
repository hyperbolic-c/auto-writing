"""
Fallback strategy logic for literature search.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class FallbackReason(Enum):
    """Reasons for fallback"""
    LOCAL_EMPTY = "local_results_empty"
    EXTERNAL_UNAVAILABLE = "external_unavailable"


@dataclass
class FallbackDecision:
    """Result of fallback decision"""
    should_fallback: bool
    reason: FallbackReason
    local_count: int
    message: str


def decide_fallback(
    local_count: int,
    external_available: bool,
    fallback_on_empty: bool = True
) -> FallbackDecision:
    """
    Decide whether to fallback to external search.

    Args:
        local_count: Number of local results
        external_available: Whether external search is configured
        fallback_on_empty: Whether to fallback when no local results

    Returns:
        FallbackDecision with the result
    """
    # Check external availability
    if not external_available:
        return FallbackDecision(
            should_fallback=False,
            reason=FallbackReason.EXTERNAL_UNAVAILABLE,
            local_count=local_count,
            message=(
                "External search not available (missing OPENROUTER_API_KEY). "
                "Continuing with available local results."
            )
        )

    # Only fallback when 0 results and enabled
    if local_count == 0 and fallback_on_empty:
        return FallbackDecision(
            should_fallback=True,
            reason=FallbackReason.LOCAL_EMPTY,
            local_count=local_count,
            message="No local results. Falling back to external search."
        )

    # Have results, no fallback needed
    return FallbackDecision(
        should_fallback=False,
        reason=FallbackReason.LOCAL_EMPTY,
        local_count=local_count,
        message=f"Found {local_count} local result(s). No fallback needed."
    )
