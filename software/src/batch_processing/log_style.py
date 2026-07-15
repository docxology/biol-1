"""Logging style constants and utilities for visually enhanced pipeline output.

Provides emoji mappings and formatting helpers for consistent, readable logging
across the publish pipeline.
"""

# Format type emoji
FORMAT_EMOJI = {
    "pdf": "📄",
    "docx": "📝",
    "mp3": "🔊",
    "html": "🌐",
    "txt": "📋",
    "md": "📑",
}

# Content type emoji
CONTENT_EMOJI = {
    "module": "📚",
    "syllabus": "📅",
    "lab": "🧪",
    "exam": "📝",
    "test": "📝",
    "practice_test": "📝",
    "slide": "🎯",
    "dashboard": "📊",
    "website": "🌐",
}

# Status emoji
STATUS_EMOJI = {
    "success": "✅",
    "warning": "⚠️",
    "error": "❌",
    "processing": "🔄",
    "cleaning": "🧹",
    "validating": "🔍",
    "publishing": "📦",
    "copying": "📋",
    "flattening": "📁",
    "pushing": "🚀",
}

def format_summary(counts: dict[str, int], show_zero: bool = False) -> str:
    """Format output counts as a compact emoji-annotated string.
    
    Args:
        counts: Dict mapping format name to count (e.g., {"pdf": 2, "docx": 2})
        show_zero: If False, omit formats with zero count
        
    Returns:
        Compact string like "📄 2  📝 2  📑 2"
    """
    parts = []
    # Order: pdf, docx, md, html, mp3, txt
    format_order = ["pdf", "docx", "md", "html", "mp3", "txt"]
    
    for fmt in format_order:
        count = counts.get(fmt, 0)
        if count > 0 or show_zero:
            emoji = FORMAT_EMOJI.get(fmt, "📄")
            parts.append(f"{emoji} {count}")
    
    return "  ".join(parts) if parts else "—"


