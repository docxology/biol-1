"""Lab dashboard generation for BIOL-1 course."""

from .main import (
    LabDashboardSpec,
    SPECS,
    render_all_dashboards,
    render_dashboard,
)

__all__ = [
    "LabDashboardSpec",
    "SPECS",
    "render_dashboard",
    "render_all_dashboards",
]
