# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

### Added

- Added keyboard shortcut for adding values in Addition and Subtraction modes
- Added numpad support for the add-value shortcut

## [1.3.0] - 2026-09-08

### Added

- Added keyboard shortcut for swapping source and result units in Conversion mode
- Added persistent basic user preferences for the selected operation, source units and result unit
- Added automatic creation and recovery of the preferences file
- Added `--version` support to both `suc` and `storage-unit-converter`
- Added automated tests for persistent history handling
- Added atomic JSON writes for user data files
- Added automated tests for user data write failures and recovery

### Changed

- Improved keyboard focus and navigation throughout the graphical interface
- Improved Tab and Shift + Tab navigation across input fields and controls
- Improved focus behavior when switching operation modes and using Reset
- Hidden unnecessary row deletion controls in Conversion mode
- Improved CLI help with clearer structure, examples and the complete list of supported units
- Centralized persistent history storage in a dedicated module
- Hardened history and preferences persistence against interrupted or failed writes
- Updated package version metadata to 1.3.0

## [1.2.0] - 2026-09-07

### Added

- Added `suc units` command to display all supported decimal and binary storage units
- Added a source/target unit swap action in Conversion mode
- Added persistent conversion history between application sessions

## [1.1.0] - 2026-09-07

### Added

- Added standalone CLI binaries to pre-built release archives for macOS, Windows and Linux
- Added automated smoke tests for standalone CLI binaries in cross-platform build workflows

### Changed

- Clarified GUI and CLI distribution methods in the README
- Documented standalone CLI usage for pre-built release archives
- Recommended `pipx` for end-user CLI installation from source
- Improved initial window sizing across macOS, Windows and Linux

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