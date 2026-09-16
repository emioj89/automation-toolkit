"""Unit tests for CSV <-> JSON conversion utilities."""

import json
from pathlib import Path
import tempfile
import unittest

from src.csv_json import csv_to_json, json_to_csv


class TestCsvJson(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_csv_to_json_valid(self):
        csv_file = self.temp_path / "test.csv"
        json_file = self.temp_path / "test.json"

        csv_content = "id,name,city\n1,Alice,Madrid\n2,Böb,Barcelona\n"
        csv_file.write_text(csv_content, encoding="utf-8")

        count = csv_to_json(csv_file, json_file)
        self.assertEqual(count, 2)
        self.assertTrue(json_file.exists())

        with open(json_file, mode="r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Alice")
        self.assertEqual(data[1]["name"], "Böb")

    def test_csv_to_json_empty_file(self):
        csv_file = self.temp_path / "empty.csv"
        json_file = self.temp_path / "empty.json"

        csv_file.write_text("", encoding="utf-8")

        count = csv_to_json(csv_file, json_file)
        self.assertEqual(count, 0)

        with open(json_file, mode="r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data, [])

    def test_csv_to_json_nonexistent(self):
        nonexistent = self.temp_path / "does_not_exist.csv"
        json_out = self.temp_path / "output.json"

        with self.assertRaises(FileNotFoundError):
            csv_to_json(nonexistent, json_out)

    def test_json_to_csv_valid(self):
        json_file = self.temp_path / "test.json"
        csv_file = self.temp_path / "test.csv"

        json_data = [
            {"id": "1", "name": "Alice", "city": "Madrid"},
            {"id": "2", "name": "Böb", "city": "Barcelona", "extra": "yes"},
        ]
        json_file.write_text(json.dumps(json_data, ensure_ascii=False), encoding="utf-8")

        count = json_to_csv(json_file, csv_file)
        self.assertEqual(count, 2)
        self.assertTrue(csv_file.exists())

        csv_content = csv_file.read_text(encoding="utf-8")
        self.assertIn("id,name,city,extra", csv_content)
        self.assertIn("1,Alice,Madrid,", csv_content)
        self.assertIn("2,Böb,Barcelona,yes", csv_content)

    def test_json_to_csv_empty_array(self):
        json_file = self.temp_path / "empty.json"
        csv_file = self.temp_path / "empty.csv"

        json_file.write_text("[]", encoding="utf-8")

        count = json_to_csv(json_file, csv_file)
        self.assertEqual(count, 0)
        self.assertTrue(csv_file.exists())

    def test_json_to_csv_invalid_json(self):
        json_file = self.temp_path / "invalid.json"
        csv_file = self.temp_path / "output.csv"

        json_file.write_text("{invalid json content}", encoding="utf-8")

        with self.assertRaises(ValueError) as ctx:
            json_to_csv(json_file, csv_file)

        self.assertIn("Invalid JSON file format", str(ctx.exception))

    def test_json_to_csv_not_a_list(self):
        json_file = self.temp_path / "object.json"
        csv_file = self.temp_path / "output.csv"

        json_file.write_text('{"key": "value"}', encoding="utf-8")

        with self.assertRaises(ValueError) as ctx:
            json_to_csv(json_file, csv_file)

        self.assertIn("JSON root element must be an array of objects", str(ctx.exception))

    def test_json_to_csv_invalid_array_item(self):
        json_file = self.temp_path / "bad_array.json"
        csv_file = self.temp_path / "output.csv"

        json_file.write_text('[{"a": 1}, "string_item"]', encoding="utf-8")

        with self.assertRaises(ValueError) as ctx:
            json_to_csv(json_file, csv_file)

        self.assertIn("not a JSON object/dictionary", str(ctx.exception))

    def test_json_to_csv_nonexistent(self):
        nonexistent = self.temp_path / "does_not_exist.json"
        csv_out = self.temp_path / "output.csv"

        with self.assertRaises(FileNotFoundError):
            json_to_csv(nonexistent, csv_out)


if __name__ == "__main__":
    unittest.main()

