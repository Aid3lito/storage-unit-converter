import json

from storage_converter import preferences


def test_load_preferences_returns_defaults_when_file_is_missing(tmp_path):
    path = tmp_path / "preferences.json"

    result = preferences.load_preferences(path)

    assert result == preferences.DEFAULT_PREFERENCES


def test_load_preferences_reads_valid_json(tmp_path):
    path = tmp_path / "preferences.json"

    expected = {
        "operation": "addition",
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
        "operation": "conversion",
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
        "operation": "addition",
        "default_operation": "subtraction",
        "source_units": [
            "MB - MegaByte",
            "GB - GigaByte",
        ],
        "default_input_unit": "MB - MegaByte",
        "default_second_input_unit": "MB - MegaByte",
        "result_unit": "TB - TeraByte",
        "default_result_unit": "TB - TeraByte",
        "theme": "dark",
        "language": "fr",
        "history_enabled": False,
    }

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {
            "MB - MegaByte",
            "GB - GigaByte",
            "TB - TeraByte",
            "GiB - GibiByte",
        },
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result == loaded


def test_validate_preferences_replaces_invalid_operation():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["operation"] = "Invalid"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["operation"] == "conversion"


def test_validate_preferences_filters_invalid_source_units():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["source_units"] = [
        "GB - GigaByte",
        "Invalid unit",
    ]

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["source_units"] == ["GB - GigaByte"]


def test_validate_preferences_replaces_invalid_result_unit():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["result_unit"] = "Invalid unit"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["result_unit"] == "GiB - GibiByte"


def test_validate_preferences_replaces_invalid_theme():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["theme"] = "purple"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["theme"] == "light"

def test_validate_preferences_migrates_legacy_operation_value():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["operation"] = "Subtraction"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["operation"] == "subtraction"

def test_validate_preferences_migrates_legacy_conversion_value():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["operation"] = "Conversion"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["operation"] == "conversion"


def test_validate_preferences_migrates_legacy_addition_value():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["operation"] = "Addition"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["operation"] == "addition"

def test_validate_preferences_accepts_valid_language():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["language"] = "fr"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["language"] == "fr"


def test_validate_preferences_replaces_invalid_language():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["language"] = "invalid"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["language"] == "en"

def test_validate_preferences_accepts_valid_default_operation():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["default_operation"] = "subtraction"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["default_operation"] == "subtraction"


def test_validate_preferences_replaces_invalid_default_operation():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["default_operation"] = "invalid"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["default_operation"] == "conversion"


def test_validate_preferences_accepts_valid_default_input_unit():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["default_input_unit"] = "GiB - GibiByte"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["default_input_unit"] == "GiB - GibiByte"


def test_validate_preferences_replaces_invalid_default_input_unit():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["default_input_unit"] = "invalid"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["default_input_unit"] == "GB - GigaByte"

def test_validate_preferences_accepts_valid_default_result_unit():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["default_result_unit"] = "GB - GigaByte"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["default_result_unit"] == "GB - GigaByte"


def test_validate_preferences_replaces_invalid_default_result_unit():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["default_result_unit"] = "invalid"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["default_result_unit"] == "GiB - GibiByte"


def test_validate_preferences_accepts_valid_history_enabled():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["history_enabled"] = False

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["history_enabled"] is False


def test_validate_preferences_replaces_invalid_history_enabled():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["history_enabled"] = "invalid"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["history_enabled"] is True


def test_validate_preferences_accepts_valid_default_second_input_unit():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["default_second_input_unit"] = "GiB - GibiByte"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["default_second_input_unit"] == "GiB - GibiByte"


def test_validate_preferences_replaces_invalid_default_second_input_unit():
    loaded = preferences.DEFAULT_PREFERENCES.copy()
    loaded["default_second_input_unit"] = "invalid"

    result = preferences.validate_preferences(
        loaded,
        {"conversion", "addition", "subtraction"},
        {"GB - GigaByte", "GiB - GibiByte"},
        {"light", "dark"},
        {"en", "fr"},
    )

    assert result["default_second_input_unit"] == "GB - GigaByte"