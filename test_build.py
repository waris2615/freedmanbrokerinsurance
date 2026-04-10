import unittest
from unittest.mock import patch, mock_open, MagicMock
import build
import io
import contextlib

class TestBuild(unittest.TestCase):
    def test_main_exception_handling(self):
        """Test that main() catches exceptions during file reading and prints an error message."""

        def side_effect(file, mode='r', *args, **kwargs):
            if mode == 'r' or 'r' in mode:
                raise Exception("Test Exception")
            return MagicMock()

        with patch('builtins.open', side_effect=side_effect):
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                build.main()
            output = f.getvalue()

        self.assertIn("Error reading existing files: Test Exception", output)
        self.assertIn("Build complete.", output)

    def test_main_happy_path(self):
        """Test that main() runs successfully when no exceptions are raised."""
        # Mock open to return some content
        m = mock_open(read_data="<!-- Page Header --> Some content <!-- Footer -->")
        with patch('builtins.open', m):
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                build.main()
            output = f.getvalue()

        self.assertIn("Build complete.", output)
        self.assertNotIn("Error reading existing files", output)

if __name__ == "__main__":
    unittest.main()
