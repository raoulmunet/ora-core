# Contributing

Contributions are welcome.

## Development

```bash
git clone https://github.com/raoulmunet/ora-core.git
cd ora-core
python -m pip install -e ".[dev]"
pytest
```

## Compatibility rule

Any change that introduces syntax or behavior specific to Oracle Database 19c, 23ai or 26ai must document the affected versions in both tests and user-facing documentation.

## Pull requests

Keep changes focused, include tests for parser behavior, and prefer explicit limitations over heuristic guesses that could produce misleading analysis.
