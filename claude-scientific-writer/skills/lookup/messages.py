"""
Messages and logging for literature lookup.
"""

# Message templates for different scenarios
SEARCH_MESSAGES = {
    "local_search_start": "Searching local Zotero library...",
    "local_search_found": "Found {count} papers in local library",
    "local_search_empty": "No papers found in local library",
    "fallback_triggered": "No local results. Searching external databases...",
    "fallback_success": "Found {count} additional papers from external search",
    "fallback_failed": "External search failed: {error}",
    "fallback_not_available": (
        "External search not available (missing OPENROUTER_API_KEY). "
        "Continuing with available local results."
    ),
    "search_complete": "Search complete: {count} papers found",
    "writing_with_available": "Writing with {count} available citations...",
}


def format_message(key: str, **kwargs) -> str:
    """Format a message with the given key and parameters"""
    template = SEARCH_MESSAGES.get(key, key)
    try:
        return template.format(**kwargs)
    except KeyError:
        return template


def log_search_event(logger, event: str, **kwargs):
    """Log a search event with formatted message"""
    message = format_message(event, **kwargs)
    if logger:
        logger.info(message)
    return message


class LookupLogger:
    """Logger for literature lookup operations"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.events = []

    def log(self, message: str, level: str = "info"):
        """Log a message"""
        entry = {"level": level, "message": message}
        self.events.append(entry)
        if self.verbose:
            print(f"[{level.upper()}] {message}")

    def local_search_start(self, query: str):
        """Log local search start"""
        self.log(format_message("local_search_start"), "info")

    def local_search_found(self, count: int):
        """Log local search results"""
        self.log(format_message("local_search_found", count=count), "info")

    def local_search_empty(self):
        """Log empty local results"""
        self.log(format_message("local_search_empty"), "info")

    def fallback_triggered(self):
        """Log fallback trigger"""
        self.log(format_message("fallback_triggered"), "info")

    def fallback_success(self, count: int):
        """Log fallback success"""
        self.log(format_message("fallback_success", count=count), "info")

    def fallback_failed(self, error: str):
        """Log fallback failure"""
        self.log(
            format_message("fallback_failed", error=error),
            "warning"
        )

    def fallback_not_available(self):
        """Log fallback not available"""
        self.log(format_message("fallback_not_available"), "warning")

    def search_complete(self, count: int):
        """Log search complete"""
        self.log(format_message("search_complete", count=count), "info")

    def writing_with(self, count: int):
        """Log writing with available citations"""
        self.log(format_message("writing_with_available", count=count), "info")
