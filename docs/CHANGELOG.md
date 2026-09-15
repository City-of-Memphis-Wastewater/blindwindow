
# Changelog

All notable changes to this project will be documented in this file.
The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.1.4] - 2026-09-15
### Changed:
- MacOS support now functional, with self._append_queue.put() rather than elf.after_idle(), in BlindWindow._safe_append()

---

## [0.1.3] - 2026-09-15
### Changed:
- Enable ansi.strip_ansi() to handle bytes.
- Enable SystemStreamWrapper.write() to handle bytes. 

---

## [0.1.2] - 2026-09-15
### Changed:
- Python 3.9 compatbility by pinning Typer version for ranges.

---

## [0.1.1] - 2026-09-15
### Added:
- Migrated blindwindow components from maxson-gui-utils, for modular inclusion.

---

## [0.1.0] - 2026-08-27
### Added:
- Initial commit, notes on S24

---
