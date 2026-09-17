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