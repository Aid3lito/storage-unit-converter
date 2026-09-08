import json
import tempfile
import unittest
from pathlib import Path

from storage_converter import history_store


class TestHistoryStore(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "history.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_empty_history(self):
        result = history_store.load_history(
            self.file_path,
            max_entries=10
        )

        self.assertEqual(result, [])

    def test_load_valid_history(self):
        data = [
            "100 GB → 93.132 GiB",
            "1 GB + 500 MB = 1.5 GB"
        ]

        self.file_path.write_text(
            json.dumps(data),
            encoding="utf-8"
        )

        result = history_store.load_history(
            self.file_path,
            max_entries=10
        )

        self.assertEqual(result, data)

    def test_load_history_respects_max_entries(self):
        data = [
            f"Entry {index}"
            for index in range(15)
        ]

        self.file_path.write_text(
            json.dumps(data),
            encoding="utf-8"
        )

        result = history_store.load_history(
            self.file_path,
            max_entries=10
        )

        self.assertEqual(len(result), 10)
        self.assertEqual(
            result,
            data[:10]
        )

    def test_invalid_entries_are_ignored(self):
        data = [
            "Valid entry",
            123,
            None,
            {"value": "invalid"},
            "Another valid entry"
        ]

        self.file_path.write_text(
            json.dumps(data),
            encoding="utf-8"
        )

        result = history_store.load_history(
            self.file_path,
            max_entries=10
        )

        self.assertEqual(
            result,
            [
                "Valid entry",
                "Another valid entry"
            ]
        )

    def test_non_list_json_returns_empty_history(self):
        self.file_path.write_text(
            json.dumps({
                "history": ["Entry"]
            }),
            encoding="utf-8"
        )

        result = history_store.load_history(
            self.file_path,
            max_entries=10
        )

        self.assertEqual(result, [])

    def test_corrupted_json_returns_empty_history(self):
        self.file_path.write_text(
            "{ invalid json",
            encoding="utf-8"
        )

        result = history_store.load_history(
            self.file_path,
            max_entries=10
        )

        self.assertEqual(result, [])

    def test_save_history_creates_file(self):
        data = [
            "100 GB → 93.132 GiB"
        ]

        history_store.save_history(
            self.file_path,
            data
        )

        self.assertTrue(
            self.file_path.exists()
        )

    def test_save_history_writes_expected_data(self):
        data = [
            "100 GB → 93.132 GiB",
            "1 GB + 500 MB = 1.5 GB"
        ]

        history_store.save_history(
            self.file_path,
            data
        )

        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            saved_data = json.load(file)

        self.assertEqual(
            saved_data,
            data
        )

    def test_save_history_creates_parent_directory(self):
        nested_file = (
            Path(self.temp_dir.name)
            / "nested"
            / "history.json"
        )

        history_store.save_history(
            nested_file,
            ["Entry"]
        )

        self.assertTrue(
            nested_file.exists()
        )


if __name__ == "__main__":
    unittest.main()