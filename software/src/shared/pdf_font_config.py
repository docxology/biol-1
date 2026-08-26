"""Process-wide WeasyPrint font configuration.

WeasyPrint creates one PangoFcFontMap per ``FontConfiguration``. When each
render builds its own font map and drops it mid-process, GC finalization can
destroy the map's HarfBuzz faces while a later teardown pass still walks them
(``hb_face_destroy`` -> SIGSEGV inside ``hb_ot_face_t::fini``), crashing long
pipelines intermittently (~30-50% of multi-document runs observed on the
pango 1.58 / harfbuzz 14.x Homebrew stack, macOS arm64).

Every WeasyPrint call site must pass this shared instance as ``font_config``
so exactly one stable font map exists for the process lifetime.
"""

from weasyprint.text.fonts import FontConfiguration

FONT_CONFIG = FontConfiguration()
