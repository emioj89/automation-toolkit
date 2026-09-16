"""Unit tests for the Command-Line Interface (CLI)."""

import json
from pathlib import Path
import tempfile
import unittest

from src.cli import main


class TestCli(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_file_report_output_generates_json(self):
        # Create a sample file in temp directory
        sample_file = self.temp_path / "sample.txt"
        sample_file.write_text("hello cli", encoding="utf-8")

        output_file = self.temp_path / "output_report.json"
        args = ["file-report", str(self.temp_path), "-o", str(output_file)]

        result = main(args)

        self.assertEqual(result, 0)
        self.assertTrue(output_file.exists())

    def test_file_report_output_creates_parent_directories(self):
        sample_file = self.temp_path / "data.txt"
        sample_file.write_text("data content", encoding="utf-8")

        nested_output = self.temp_path / "reports" / "generated" / "report.json"
        args = ["file-report", str(self.temp_path), "--output", str(nested_output)]

        result = main(args)

        self.assertEqual(result, 0)
        self.assertTrue(nested_output.exists())

    def test_file_report_output_valid_json(self):
        sample_file = self.temp_path / "info.log"
        sample_file.write_text("log line", encoding="utf-8")

        output_file = self.temp_path / "report.json"
        args = ["file-report", str(self.temp_path), "-o", str(output_file)]

        result = main(args)
        self.assertEqual(result, 0)

        with open(output_file, mode="r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, dict)
        self.assertEqual(data["total_files"], 1)
        self.assertIn("total_size_bytes", data)

    def test_main_returns_zero_on_success(self):
        csv_file = self.temp_path / "input.csv"
        csv_file.write_text("col1,col2\nval1,val2\n", encoding="utf-8")
        json_file = self.temp_path / "output.json"

        args = ["csv-to-json", str(csv_file), str(json_file)]
        result = main(args)

        self.assertEqual(result, 0)

    def test_main_returns_non_zero_on_nonexistent_path(self):
        nonexistent = self.temp_path / "nonexistent.csv"
        json_file = self.temp_path / "output.json"

        args = ["csv-to-json", str(nonexistent), str(json_file)]
        result = main(args)

        self.assertNotEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
