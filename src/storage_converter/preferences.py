import json

from . import data_store


DEFAULT_PREFERENCES = {
    "operation": "conversion",
    "default_operation": "conversion",
    "source_units": ["GB - GigaByte"],
    "default_input_unit": "GB - GigaByte",
    "default_second_input_unit": "GB - GigaByte",
    "result_unit": "GiB - GibiByte",
    "default_result_unit": "GiB - GibiByte",
    "theme": "light",
    "language": "en",
    "history_enabled": True,
    "history_max_entries": 10,
}


def save_preferences(path, preferences):
    data_store.save_json(
        path,
        preferences,
    )


def load_preferences(path):
    if not path.exists():
        return DEFAULT_PREFERENCES.copy()

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            preferences = json.load(file)

    except (
        OSError,
        json.JSONDecodeError,
    ):
        return DEFAULT_PREFERENCES.copy()

    if not isinstance(preferences, dict):
        return DEFAULT_PREFERENCES.copy()

    return preferences

def validate_preferences(
    loaded_preferences,
    valid_operations,
    valid_units,
    valid_themes,
    valid_languages,
):
    validated = DEFAULT_PREFERENCES.copy()

    operation = loaded_preferences.get("operation")

    legacy_operations = {
        "Conversion": "conversion",
        "Addition": "addition",
        "Subtraction": "subtraction",
    }

    operation = legacy_operations.get(
        operation,
        operation,
    )

    if operation in valid_operations:
                validated["operation"] = operation

    default_operation = loaded_preferences.get(
        "default_operation"
    )

    if default_operation in valid_operations:
        validated["default_operation"] = default_operation


    source_units = loaded_preferences.get("source_units")

    if isinstance(source_units, list):
        validated_source_units = [
            unit
            for unit in source_units
            if unit in valid_units
        ]

        if validated_source_units:
            validated["source_units"] = validated_source_units

    default_input_unit = loaded_preferences.get(
        "default_input_unit"
    )

    if default_input_unit in valid_units:
        validated["default_input_unit"] = default_input_unit

    default_second_input_unit = loaded_preferences.get(
        "default_second_input_unit"
    )

    if default_second_input_unit in valid_units:
        validated["default_second_input_unit"] = default_second_input_unit

    result_unit = loaded_preferences.get("result_unit")

    if result_unit in valid_units:
        validated["result_unit"] = result_unit

    default_result_unit = loaded_preferences.get(
        "default_result_unit"
    )

    if default_result_unit in valid_units:
        validated["default_result_unit"] = default_result_unit

    theme = loaded_preferences.get("theme")

    if theme in valid_themes:
        validated["theme"] = theme

    language = loaded_preferences.get("language")

    if language in valid_languages:
        validated["language"] = language

    history_enabled = loaded_preferences.get(
        "history_enabled"
    )

    if isinstance(history_enabled, bool):
        validated["history_enabled"] = history_enabled

    history_max_entries = loaded_preferences.get(
        "history_max_entries"
    )

    if (
        isinstance(history_max_entries, int)
        and not isinstance(history_max_entries, bool)
        and history_max_entries > 0
    ):
        validated["history_max_entries"] = history_max_entries

    return validated