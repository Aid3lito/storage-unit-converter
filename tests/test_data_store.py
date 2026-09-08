import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from storage_converter import data_store


class TestDataStore(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp_dir.name)
        self.file_path = self.directory / "data.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_json_creates_file(self):
        data = {
            "operation": "Conversion",
            "result_unit": "GiB - GibiByte"
        }

        result = data_store.save_json(
            self.file_path,
            data
        )

        self.assertTrue(result)
        self.assertTrue(
            self.file_path.exists()
        )

    def test_save_json_writes_expected_data(self):
        data = {
            "history": [
                "100 GB → 93.132 GiB"
            ]
        }

        result = data_store.save_json(
            self.file_path,
            data
        )

        self.assertTrue(result)

        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            saved_data = json.load(file)

        self.assertEqual(
            saved_data,
            data
        )

    def test_save_json_creates_parent_directory(self):
        nested_file = (
            self.directory
            / "nested"
            / "folder"
            / "data.json"
        )

        result = data_store.save_json(
            nested_file,
            {"value": 42}
        )

        self.assertTrue(result)
        self.assertTrue(
            nested_file.exists()
        )

    def test_save_json_replaces_existing_file(self):
        original_data = {
            "value": "old"
        }

        new_data = {
            "value": "new"
        }

        self.file_path.write_text(
            json.dumps(original_data),
            encoding="utf-8"
        )

        result = data_store.save_json(
            self.file_path,
            new_data
        )

        self.assertTrue(result)

        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            saved_data = json.load(file)

        self.assertEqual(
            saved_data,
            new_data
        )

    def test_replace_failure_preserves_original_file(self):
        original_data = {
            "value": "original"
        }

        self.file_path.write_text(
            json.dumps(original_data),
            encoding="utf-8"
        )

        with patch(
            "storage_converter.data_store.os.replace",
            side_effect=OSError("replace failed")
        ):
            result = data_store.save_json(
                self.file_path,
                {"value": "new"}
            )

        self.assertFalse(result)

        with self.file_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            saved_data = json.load(file)

        self.assertEqual(
            saved_data,
            original_data
        )

    def test_replace_failure_removes_temporary_file(self):
        self.file_path.write_text(
            "{}",
            encoding="utf-8"
        )

        with patch(
            "storage_converter.data_store.os.replace",
            side_effect=OSError("replace failed")
        ):
            result = data_store.save_json(
                self.file_path,
                {"value": "new"}
            )

        self.assertFalse(result)

        temporary_files = list(
            self.directory.glob("*.tmp")
        )

        self.assertEqual(
            temporary_files,
            []
        )


if __name__ == "__main__":
    unittest.main()