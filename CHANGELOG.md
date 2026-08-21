# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-08-21

### Added

- Cross-platform desktop application built with Python and Tkinter
- Support for macOS Intel (`x86_64`)
- Support for macOS Apple Silicon (`arm64`)
- Support for Windows 64-bit (`x86_64`)
- Support for Linux 64-bit (`x86_64`)
- Decimal and binary storage unit conversion
- Addition of multiple storage values
- Subtraction of multiple storage values
- Dynamic input rows
- Decimal and binary unit selectors
- Configurable result unit
- Calculation history
- Clipboard copy support
- Interface reset functionality
- Enter key shortcut for calculations
- Automatic number formatting
- Scientific notation for very small values
- Input validation and user-facing error messages
- JSON-based storage unit definitions
- Command-line interface
- Short `suc` command for CLI usage
- CLI support for conversion, addition, and subtraction
- Automated unit tests
- Continuous integration across Python 3.9 through 3.13
- Automated cross-platform builds with GitHub Actions
- Application icons for macOS, Windows, and source assets

### Notes

- macOS builds are currently unsigned and not notarized.
- On macOS, Gatekeeper may block the application on first launch.
- If this happens, open **System Settings → Privacy & Security** and select **Open Anyway**.