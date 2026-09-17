# Storage Unit Converter 2.0 Architecture

## Purpose

Storage Unit Converter 2.0 introduces a more modular architecture to support the desktop redesign, application settings, localization and future interfaces while preserving the existing conversion engine and CLI.

The goal is to improve maintainability without introducing unnecessary architectural complexity.

## Architecture principles

### Keep core logic independent from the user interface

Conversion, persistence and data-processing logic must not depend on Tkinter.

This allows the same core functionality to be reused by:

- the desktop GUI
- the existing CLI
- the future TUI
- future integrations

### Separate responsibilities

UI construction, themes, preferences, localization and persistence should be handled by dedicated modules rather than remaining concentrated in `app.py`.

### Preserve CLI compatibility

The existing CLI must continue to use the same conversion engine.

The v2 desktop redesign must not require GUI-specific dependencies in the CLI.

### Keep the architecture lightweight

SuC 2.0 should not introduce unnecessary frameworks or complex architectural patterns.

Python and Tkinter remain the foundation of the desktop application.

## Proposed package structure

```text
src/storage_converter/
├── __init__.py
├── app.py
├── cli.py
├── converter.py
├── preferences.py
├── history_store.py
├── data_store.py
├── units_decimal.json
├── units_binary.json
├── localization/
│   ├── __init__.py
│   ├── manager.py
│   ├── en.json
│   └── fr.json
└── ui/
    ├── __init__.py
    ├── main_window.py
    ├── theme.py
    ├── settings_window.py
    └── widgets.py
```

Some modules may be introduced only when they contain meaningful functionality.

Empty abstraction layers should be avoided.

## Module responsibilities

### `app.py`

Application entry point.

Responsibilities:

- initialize the application
- load preferences
- create the main window
- start the Tkinter event loop

Business logic should not live here.

### `converter.py`

Core storage conversion engine.

Responsibilities:

- decimal and binary storage conversions
- reusable calculation logic

This module must remain independent from Tkinter.

### `preferences.py`

Centralized preference handling.

Responsibilities:

- default preferences
- loading
- validation
- saving
- preference schema versioning
- future migration between preference formats

### `history_store.py`

Persistent calculation history storage.

The existing dedicated history layer should remain isolated from the GUI.

### `data_store.py`

Low-level persistent JSON storage.

Responsibilities include safe and atomic file writes.

### `localization/manager.py`

Localization manager.

Responsibilities:

- active language
- translation resource loading
- translation lookup
- missing-key fallback
- language switching

Application code should use stable translation keys rather than hard-coded user-facing strings.

Example:

```python
tr("button.calculate")
```

### `localization/en.json`

English translation resources.

### `localization/fr.json`

French translation resources.

English should act as the default/fallback language.

### `ui/main_window.py`

Main desktop application interface.

A dedicated application/window class should coordinate the desktop UI.

Possible class:

```python
class StorageConverterApp:
    ...
```

Responsibilities:

- construct the main interface
- react to user actions
- coordinate UI state
- call core services

It should not directly implement persistence or conversion algorithms.

### `ui/theme.py`

Theme definitions and application.

Responsibilities:

- Light theme
- Dark theme
- ttk styles
- theme-related UI helpers

### `ui/settings_window.py`

Settings interface.

Initial settings areas may include:

- language
- theme
- default operation
- default units
- history behavior
- session restoration

### `ui/widgets.py`

Reusable custom interface components.

Potential components include:

- dynamic value rows
- unit selectors
- multi-unit result components

This module should only be introduced when reusable widgets actually exist.

## Preferences schema

SuC 2.0 should move toward a structured preference format.

Example:

```json
{
  "version": 2,
  "general": {
    "language": "en",
    "theme": "dark"
  },
  "conversion": {
    "default_source_unit": "GB - GigaByte",
    "default_result_unit": "GiB - GibiByte",
    "remember_recent_units": true
  },
  "history": {
    "enabled": true,
    "max_entries": 50
  },
  "interface": {
    "remember_row_count": true
  }
}
```

The final schema may evolve during implementation.

Existing 1.x preferences should be migrated safely where practical.

## Localization structure

User-facing strings should use stable keys.

Example English resource:

```json
{
  "app.title": "Storage Unit Converter",
  "button.calculate": "Calculate",
  "button.reset": "Reset",
  "button.copy": "Copy",
  "section.history": "History"
}
```

Example French resource:

```json
{
  "app.title": "Convertisseur d’unités de stockage",
  "button.calculate": "Calculer",
  "button.reset": "Réinitialiser",
  "button.copy": "Copier",
  "section.history": "Historique"
}
```

## Dependency direction

Core modules must not import desktop UI modules.

Preferred direction:

```text
converter
preferences
history_store
data_store
localization
     ↓
desktop UI / CLI / future TUI
```

The UI may depend on core services.

Core services must not depend on the UI.

## Migration strategy

The architectural migration should be incremental.

### Phase 1 — Introduce structure

- create architecture documentation
- introduce dedicated module directories
- keep existing application behavior unchanged

### Phase 2 — Extract theme handling

- move theme definitions out of `app.py`
- preserve current Light and Dark behavior

### Phase 3 — Extract preferences

- centralize preference defaults
- loading
- validation
- persistence
- prepare migration from 1.x preferences

### Phase 4 — Introduce localization

- implement translation manager
- add English and French resources
- replace hard-coded user-facing strings progressively

### Phase 5 — Introduce application class

- move GUI construction into the dedicated UI layer
- reduce global Tkinter state
- preserve existing behavior during migration

### Phase 6 — Redesign the interface

Only after the technical architecture is stable should the visual redesign begin.

## Testing strategy

Existing conversion, CLI, persistence and history tests must continue to pass throughout the migration.

Additional tests should be introduced for:

- preference validation
- preference migration
- localization fallback
- translation loading
- settings persistence
- new UI-independent logic

## Out of scope

The SuC 2.0 architecture does not require:

- a new GUI framework
- a database
- an ORM
- dependency injection frameworks
- plugin architecture
- cloud services
- external APIs
- a TUI implementation

Those features may be considered in later releases.

### Notes

The architecture should remain pragmatic.

Modules should be created because they have clear responsibilities, not simply to increase abstraction.

The objective is to make SuC easier to maintain and extend while preserving the simplicity of the current project.