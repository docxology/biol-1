# System Context {#sec:system_context}

## Project Boundary

A private Biology course source and generation repository for College of the Redwoods, including BIOL-1 source material, generated public-ready outputs, and publishing automation.

## Source Surfaces

- `course_development/`
- `PUBLISHED/`
- `archive/`
- `software/`
- `scripts/`

## Template Boundary

The private project lives in the sidecar repository. Rendering and validation run through the sibling public template checkout after `link-projects` mirrors the project into `template/projects/` as a local symlink.
