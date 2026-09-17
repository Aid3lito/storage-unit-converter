import json

from storage_converter import preferences


def test_load_preferences_returns_defaults_when_file_is_missing(tmp_path):
    path = tmp_path / "preferences.json"

    result = preferences.load_preferences(path)

    assert result == preferences.DEFAULT_PREFERENCES


def test_load_preferences_reads_valid_json(tmp_path):
    path = tmp_path / "preferences.json"

    expected = {
        "operation": "Addition",
        "source_units": [
            "MB - MegaByte",
            "GB - GigaByte",
        ],
        "result_unit": "TB - TeraByte",
        "theme": "dark",
    }

    path.write_text(
        json.dumps(expected),
        encoding="utf-8",
    )

    result = preferences.load_preferences(path)

    assert result == expected


def test_load_preferences_returns_defaults_for_invalid_json(tmp_path):
    path = tmp_path / "preferences.json"

    path.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    result = preferences.load_preferences(path)

    assert result == preferences.DEFAULT_PREFERENCES


def test_load_preferences_returns_defaults_for_non_dict_json(tmp_path):
    path = tmp_path / "preferences.json"

    path.write_text(
        json.dumps(["invalid"]),
        encoding="utf-8",
    )

    result = preferences.load_preferences(path)

    assert result == preferences.DEFAULT_PREFERENCES


def test_save_preferences_writes_json(tmp_path):
    path = tmp_path / "preferences.json"

    expected = {
        "operation": "Conversion",
        "source_units": ["GB - GigaByte"],
        "result_unit": "GiB - GibiByte",
        "theme": "dark",
    }

    preferences.save_preferences(
        path,
        expected,
    )

    result = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert result == expected

def test_validate_preferences_accepts_valid_values():
    loaded = {
        "operation": "Addition",
        "source_units": [
            "MB - MegaByte",
            "GB - GigaByte",
        ],
        "result_unit": "TB - TeraByte",
        "theme": "dark",
    }

    result = preferences.validate_preferences(
        loaded,
        {"Conversion", "Addition", "Subtraction"},
        {
            "MB - MegaByte",
            "GB - GigaByte",
            "TB - TeraByte",
            "GiB - GibiByte",
        },
        {"light", "dark"},
    )

    assert result == loaded


def test_validate_preferences_replaces_invalid_operation():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["operation"] = "Invalid"

    result = preferences.validate_preferences(
        loaded,
        {"Conversion", "Addition", "Subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
    )

    assert result["operation"] == "Conversion"


def test_validate_preferences_filters_invalid_source_units():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["source_units"] = [
        "GB - GigaByte",
        "Invalid unit",
    ]

    result = preferences.validate_preferences(
        loaded,
        {"Conversion", "Addition", "Subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
    )

    assert result["source_units"] == ["GB - GigaByte"]


def test_validate_preferences_replaces_invalid_result_unit():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["result_unit"] = "Invalid unit"

    result = preferences.validate_preferences(
        loaded,
        {"Conversion", "Addition", "Subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
    )

    assert result["result_unit"] == "GiB - GibiByte"


def test_validate_preferences_replaces_invalid_theme():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["theme"] = "purple"

    result = preferences.validate_preferences(
        loaded,
        {"Conversion", "Addition", "Subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
    )

    assert result["theme"] == "light"