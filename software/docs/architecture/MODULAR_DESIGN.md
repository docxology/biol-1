# Modular Design Principles

> **Navigation**: [← README](README.md) | [Layers](LAYERS.md) | [Interface Contracts](INTERFACE_CONTRACTS.md) | [../ARCHITECTURE.md](../ARCHITECTURE.md)

The five core design principles that guide the cr-bio software architecture.

---

## 1. Self-Contained Modules

Each package contains all code, configuration, and logic needed for its
purpose. No reliance on internal implementation details of other packages.

- **Public API**: All external access through `main.py` functions
- **Internal implementation**: Helper functions in `utils.py` (private)
- **Configuration**: Module-specific constants in `config.py`
- **No shared mutable state**: Modules never share mutable state

```python
# Each package has this shape:
package_name/
├── __init__.py     # Re-exports public API
├── main.py         # Public functions
├── utils.py        # Private helpers
├── config.py       # Constants
├── README.md       # Overview
└── AGENTS.md       # Technical docs
```

---

## 2. Clear Boundaries

Well-defined boundary between public interface and internal implementation.

- **Public interface**: Functions in `main.py` are the only entry point
- **Private implementation**: `utils.py` functions are module-internal
- **Configuration interface**: `config.py` exposes constants, not logic
- **Documentation**: Boundaries documented in each package's `AGENTS.md`

---

## 3. Minimal Dependencies

Modules minimize dependencies on other modules. When dependencies exist,
they are explicit and documented.

- **Layer 0**: No imports from sibling packages (stdlib / `shared` only)
- **Layer 1**: External libraries + `shared` only
- **Layer 2**: Layer 1 only
- **Layer 3**: Any lower layer
- **Layer 4**: Any lower layer

All inter-module dependencies are documented in each package's `AGENTS.md`
and verified by `test_dependencies.py`.

---

## 4. Composable Design

Modules can be combined in various ways to create different workflows.

- **Sequential**: Output of one module feeds into another
- **Parallel**: Multiple modules process different inputs simultaneously
- **Conditional**: Modules invoked based on validation results
- **Orchestration**: Higher-level modules coordinate lower-level modules

See [../ORCHESTRATION.md](../ORCHESTRATION.md) for composition patterns.

---

## 5. Testable in Isolation

Each module can be tested independently without requiring other modules.

- **Unit tests**: Test individual functions in isolation
- **Integration tests**: Test module interactions explicitly
- **No hidden dependencies**: All dependencies are explicit
- **Real-first testing**: Real implementations by default; doubles only
  at documented external-service boundaries

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [LAYERS.md](LAYERS.md) | Layer architecture |
| [INTERFACE_CONTRACTS.md](INTERFACE_CONTRACTS.md) | Interface contracts |
| [TESTING_STRATEGY.md](TESTING_STRATEGY.md) | Testing approach |
| [../ARCHITECTURE.md](../ARCHITECTURE.md) | System architecture |
