# Changelog

All notable changes to this project are documented in this file.

## [4.0.0] - 2026-04-14

### Added
- Packaging metadata via `pyproject.toml` (PEP 621 + build-system).
- CLI entrypoint command: `dobivorn-scan`.
- Docker support with `Dockerfile` and `.dockerignore`.
- CI test workflow and dedicated parser/CLI tests.
- Improved README sections for production/release usage.

### Changed
- Hardened error handling and input validation in `portscanner.py`.
- Added structured logging options (`--verbose`, `--log-file`).
- Dependency alignment by including `scapy`.

### Fixed
- Silent exception swallowing in core scan flow.
- Invalid port range and malformed CIDR handling.
