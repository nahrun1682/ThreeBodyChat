# utils/log_utils.py
"""
Utility functions for logging
"""

def truncate(text: str, limit: int = 100) -> str:
    """
    Truncate the given text to the specified limit (characters). Append an ellipsis if truncated.
    Collapse whitespace and newlines into single spaces for log readability.
    """
    if text is None:
        return text
    # collapse all whitespace (including newlines, tabs) into single spaces
    clean = ' '.join(text.split())
    return clean if len(clean) <= limit else clean[:limit] + "…"
