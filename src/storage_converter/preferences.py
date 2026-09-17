import json

from . import data_store


DEFAULT_PREFERENCES = {
    "operation": "conversion",
    "source_units": ["GB - GigaByte"],
    "result_unit": "GiB - GibiByte",
    "theme": "light",
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

    source_units = loaded_preferences.get("source_units")

    if isinstance(source_units, list):
        validated_source_units = [
            unit
            for unit in source_units
            if unit in valid_units
        ]

        if validated_source_units:
            validated["source_units"] = validated_source_units

    result_unit = loaded_preferences.get("result_unit")

    if result_unit in valid_units:
        validated["result_unit"] = result_unit

    theme = loaded_preferences.get("theme")

    if theme in valid_themes:
        validated["theme"] = theme

    return validated