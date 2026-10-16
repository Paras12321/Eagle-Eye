"""File loading and validation utilities for images and checklists.

Owned by: MEMBER 1 (Input Processing)
"""

import os
from pathlib import Path
from typing import Union, BinaryIO
import pandas as pd

from config.settings import (
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_CHECKLIST_EXTENSIONS,
    REQUIRED_CHECKLIST_COLUMNS,
)


def is_valid_image_extension(filename: str) -> bool:
    """Check if the filename has a supported image extension (.jpg, .jpeg, .png)."""
    ext = Path(filename).suffix.lower()
    return ext in SUPPORTED_IMAGE_EXTENSIONS


def is_valid_checklist_extension(filename: str) -> bool:
    """Check if the filename has a supported checklist extension (.csv, .xlsx)."""
    ext = Path(filename).suffix.lower()
    return ext in SUPPORTED_CHECKLIST_EXTENSIONS


def load_checklist(file_source: Union[str, Path, BinaryIO]) -> pd.DataFrame:
    """Load an inspection checklist from a CSV or Excel file.

    Parameters
    ----------
    file_source : str, Path, or file-like buffer
        The path or uploaded file buffer containing the checklist.

    Returns
    -------
    pd.DataFrame
        Loaded checklist dataframe with validated columns.

    Raises
    ------
    ValueError
        If the file format is unsupported or required columns are missing.
    FileNotFoundError
        If a file path is provided that does not exist.
    """
    if isinstance(file_source, (str, Path)):
        path = Path(file_source)
        if not path.exists():
            raise FileNotFoundError(f"Checklist file not found at: {path}")
        ext = path.suffix.lower()
        if ext == ".csv":
            df = pd.read_csv(path)
        elif ext in {".xlsx", ".xls"}:
            df = pd.read_excel(path)
        else:
            raise ValueError(f"Unsupported checklist format: {ext}. Expected CSV or Excel (.xlsx).")
    else:
        # File-like object (e.g., Streamlit UploadedFile)
        filename = getattr(file_source, "name", "")
        ext = Path(filename).suffix.lower()
        if ext in {".xlsx", ".xls"}:
            df = pd.read_excel(file_source)
        else:
            # Default to CSV parser
            df = pd.read_csv(file_source)

    # Validate required columns
    missing_cols = [col for col in REQUIRED_CHECKLIST_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Checklist is missing required column(s): {missing_cols}. "
            f"Required columns are: {REQUIRED_CHECKLIST_COLUMNS}"
        )

    # Clean whitespace in string columns
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.strip()

    return df
