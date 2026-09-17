import json

from . import data_store


DEFAULT_PREFERENCES = {
    "operation": "Conversion",
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