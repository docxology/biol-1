# Course-by-date projection

This package turns the canonical BIOL-1 `course_calendar.toml` map into dated
teaching handoffs. `calendar.py` owns parsing and source resolution,
`generator.py` owns copy-only material projection, and `validation.py` owns
provenance/checksum and delivery-scope checks.

The projection copies only materials marked `used = true`. Planned-but-unused
records stay visible in each `meeting.json` manifest. LectureCreate delivery
files are limited to the playable lecture and YAML. Lab dashboards are not
copied into dated materials; they remain in the canonical lab dashboard tree.
rebuildable frames, audio intermediates, hashes, and render logs are not copied.
