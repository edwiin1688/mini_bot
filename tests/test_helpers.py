"""Tests for utils.helpers module."""
import pytest
from pathlib import Path
from minibot.utils.helpers import ensure_dir, safe_filename, timestamp


class TestEnsureDir:
    def test_ensure_dir_creates_directory(self, tmp_path):
        target = tmp_path / "subdir" / "nested"
        result = ensure_dir(target)
        assert result.exists()
        assert result.is_dir()

    def test_ensure_dir_returns_path(self, tmp_path):
        target = tmp_path / "test_dir"
        result = ensure_dir(target)
        assert result == target


class TestSafeFilename:
    def test_safe_filename_removes_invalid_chars(self):
        result = safe_filename("file<>name?.txt")
        assert "<" not in result
        assert ">" not in result
        assert "?" not in result

    def test_safe_filename_strips_whitespace(self):
        result = safe_filename("  filename.txt  ")
        assert result == "filename.txt"

    def test_safe_filename_keeps_valid_chars(self):
        result = safe_filename("valid-file_123.txt")
        assert result == "valid-file_123.txt"


class TestTimestamp:
    def test_timestamp_returns_iso_format(self):
        result = timestamp()
        assert "T" in result
        assert ":" in result

    def test_timestamp_contains_date_and_time(self):
        result = timestamp()
        parts = result.split("T")
        assert len(parts) == 2
        assert "-" in parts[0]
        assert ":" in parts[1]
