"""Unit tests for File Report generation module."""

from pathlib import Path
import tempfile
import unittest

from src.file_report import generate_file_report


class TestFileReport(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_file_report_basic(self):
        # Create test directory structure
        sub_dir = self.temp_path / "subdir"
        sub_dir.mkdir()

        file1 = self.temp_path / "file1.txt"
        file1.write_text("Hello World", encoding="utf-8")  # 11 bytes

        file2 = sub_dir / "file2.py"
        file2.write_text("print('test')", encoding="utf-8")  # 13 bytes

        file3 = self.temp_path / "no_ext_file"
        file3.write_text("123", encoding="utf-8")  # 3 bytes

        report = generate_file_report(self.temp_path, include_timestamp=True)

        self.assertEqual(report["directory"], str(self.temp_path))
        self.assertEqual(report["total_files"], 3)
        self.assertEqual(report["total_directories"], 1)
        self.assertEqual(report["total_size_bytes"], 27)

        self.assertIn(".py", report["extensions"])
        self.assertIn(".txt", report["extensions"])
        self.assertIn("no_extension", report["extensions"])

        self.assertEqual(report["files_per_extension"][".txt"], 1)
        self.assertEqual(report["files_per_extension"][".py"], 1)
        self.assertEqual(report["files_per_extension"]["no_extension"], 1)

        self.assertIsNotNone(report["largest_file"])
        self.assertEqual(report["largest_file"]["path"], str(file2))
        self.assertEqual(report["largest_file"]["size_bytes"], 13)

        self.assertIsNotNone(report["generated_at"])

    def test_file_report_no_timestamp(self):
        report = generate_file_report(self.temp_path, include_timestamp=False)
        self.assertIsNone(report["generated_at"])

    def test_file_report_nonexistent_directory(self):
        nonexistent = self.temp_path / "nonexistent"

        with self.assertRaises(FileNotFoundError):
            generate_file_report(nonexistent)

    def test_file_report_path_is_file(self):
        file_path = self.temp_path / "sample.txt"
        file_path.write_text("data", encoding="utf-8")

        with self.assertRaises(ValueError):
            generate_file_report(file_path)


if __name__ == "__main__":
    unittest.main()

