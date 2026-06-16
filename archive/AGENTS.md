# Archive Technical Documentation

`archive/` stores historical course snapshots. It is not an active publish
source.

## Layout

```
archive/
└── spring-2026/
    ├── course_development/   # Historical BIOL-1 and BIOL-8 source trees
    └── PUBLISHED/            # Historical generated public snapshots
```

## Rules

- Active authoring happens under [`../course_development/`](../course_development/).
- Active publication happens under [`../PUBLISHED/`](../PUBLISHED/).
- Archived `PUBLISHED/` trees are preserved for reference and are not subtree
  push targets.
- Archived `private/` folders retain the same confidentiality rules as active
  private course folders.

## Related

- [Spring 2026 archive](spring-2026/README.md)
- [Repository technical documentation](../AGENTS.md)

