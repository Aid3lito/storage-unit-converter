import json
from pathlib import Path


DEFAULT_LANGUAGE = "en"


class LocalizationManager:
    def __init__(
        self,
        resources_directory,
        language=DEFAULT_LANGUAGE,
        fallback_language=DEFAULT_LANGUAGE,
    ):
        self.resources_directory = Path(resources_directory)
        self.fallback_language = fallback_language
        self.language = language

        self._fallback_translations = self._load_language(
            fallback_language
        )

        self._translations = self._load_language(
            language
        )

    def _language_path(self, language):
        return self.resources_directory / f"{language}.json"

    def _load_language(self, language):
        path = self._language_path(language)

        try:
            with path.open(
                "r",
                encoding="utf-8",
            ) as file:
                translations = json.load(file)

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return {}

        if not isinstance(translations, dict):
            return {}

        return translations

    def set_language(self, language):
        self.language = language
        self._translations = self._load_language(language)

    def translate(self, key):
        if key in self._translations:
            return self._translations[key]

        if key in self._fallback_translations:
            return self._fallback_translations[key]

        return key