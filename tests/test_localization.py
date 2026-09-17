import json

from storage_converter.localization.manager import LocalizationManager


def test_translate_uses_active_language(tmp_path):
    (tmp_path / "en.json").write_text(
        json.dumps({
            "button.calculate": "Calculate",
        }),
        encoding="utf-8",
    )

    (tmp_path / "fr.json").write_text(
        json.dumps({
            "button.calculate": "Calculer",
        }),
        encoding="utf-8",
    )

    manager = LocalizationManager(
        tmp_path,
        language="fr",
    )

    assert manager.translate("button.calculate") == "Calculer"


def test_translate_falls_back_to_english(tmp_path):
    (tmp_path / "en.json").write_text(
        json.dumps({
            "button.copy": "Copy",
        }),
        encoding="utf-8",
    )

    (tmp_path / "fr.json").write_text(
        json.dumps({}),
        encoding="utf-8",
    )

    manager = LocalizationManager(
        tmp_path,
        language="fr",
    )

    assert manager.translate("button.copy") == "Copy"


def test_translate_returns_key_when_missing_everywhere(tmp_path):
    (tmp_path / "en.json").write_text(
        json.dumps({}),
        encoding="utf-8",
    )

    manager = LocalizationManager(
        tmp_path,
        language="en",
    )

    assert manager.translate("missing.key") == "missing.key"


def test_malformed_language_file_does_not_crash(tmp_path):
    (tmp_path / "en.json").write_text(
        json.dumps({
            "button.calculate": "Calculate",
        }),
        encoding="utf-8",
    )

    (tmp_path / "fr.json").write_text(
        "{invalid json",
        encoding="utf-8",
    )

    manager = LocalizationManager(
        tmp_path,
        language="fr",
    )

    assert manager.translate("button.calculate") == "Calculate"


def test_non_dict_language_file_does_not_crash(tmp_path):
    (tmp_path / "en.json").write_text(
        json.dumps({
            "button.calculate": "Calculate",
        }),
        encoding="utf-8",
    )

    (tmp_path / "fr.json").write_text(
        json.dumps(["invalid"]),
        encoding="utf-8",
    )

    manager = LocalizationManager(
        tmp_path,
        language="fr",
    )

    assert manager.translate("button.calculate") == "Calculate"


def test_set_language_changes_active_language(tmp_path):
    (tmp_path / "en.json").write_text(
        json.dumps({
            "button.reset": "Reset",
        }),
        encoding="utf-8",
    )

    (tmp_path / "fr.json").write_text(
        json.dumps({
            "button.reset": "Réinitialiser",
        }),
        encoding="utf-8",
    )

    manager = LocalizationManager(
        tmp_path,
        language="en",
    )

    manager.set_language("fr")

    assert manager.translate("button.reset") == "Réinitialiser"
