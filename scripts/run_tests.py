"""Test execution runner for Eagle Eye."""

import sys
from pathlib import Path
import pytest

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if __name__ == "__main__":
    print("=" * 60)
    print("[EAGLE EYE] Running Test Suite")
    print("=" * 60)
    exit_code = pytest.main(["-v", str(BASE_DIR / "tests")])
    sys.exit(exit_code)
