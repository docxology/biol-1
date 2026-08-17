"""Configuration for schedule processing."""

# Supported schedule output formats
SUPPORTED_OUTPUT_FORMATS: list[str] = ["pdf", "html", "docx", "txt", "mp3"]

# Schedule file patterns
SCHEDULE_FILE_PATTERNS: list[str] = ["Schedule.md", "schedule.md", "*schedule*.md"]

# Table column mappings for schedule parsing
SCHEDULE_COLUMNS: dict[str, int] = {
    "week": 0,
    "date": 1,
    "topic": 2,
    "notes": 3,
}

# Default schedule table headers
DEFAULT_HEADERS: list[str] = ["Week", "Date", "Topic", "Notes"]
