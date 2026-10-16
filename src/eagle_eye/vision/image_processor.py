"""Image processing utilities for cabinet quality inspection.

Owned by: MEMBER 2 (Computer Vision)
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import cv2
import numpy as np


def load_image_from_bytes(file_bytes: Union[bytes, bytearray]) -> np.ndarray:
    """Decode raw image bytes into an OpenCV BGR image array.

    Parameters
    ----------
    file_bytes : bytes or bytearray
        Raw image content.

    Returns
    -------
    np.ndarray
        Decoded image in OpenCV BGR format.

    Raises
    ------
    ValueError
        If bytes cannot be decoded into an image.
    """
    nparr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Failed to decode image from bytes. Ensure the file is a valid image.")
    return image


def resize_image_aspect_ratio(image: np.ndarray, max_dim: int = 1200) -> Tuple[np.ndarray, float]:
    """Resize an image maintaining its aspect ratio so its largest dimension is at most max_dim.

    Parameters
    ----------
    image : np.ndarray
        Input image.
    max_dim : int
        Maximum allowable width or height in pixels.

    Returns
    -------
    resized_image : np.ndarray
        The resized image.
    scale_factor : float
        The scale factor applied to the original dimensions.
    """
    h, w = image.shape[:2]
    if max(h, w) <= max_dim:
        return image.copy(), 1.0

    scale = max_dim / float(max(h, w))
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized, scale


def extract_crop(image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Extract an evidence crop from an image.

    Parameters
    ----------
    image : np.ndarray
        Source image.
    bbox : Tuple[int, int, int, int]
        Bounding box in (x1, y1, x2, y2) format.

    Returns
    -------
    np.ndarray
        Cropped sub-image.
    """
    x1, y1, x2, y2 = bbox
    h, w = image.shape[:2]
    x1 = max(0, min(x1, w))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h))
    y2 = max(0, min(y2, h))
    return image[y1:y2, x1:x2].copy()


# ---------------------------------------------------------------------------
#  New functions added by Member 2 for the end-to-end demo
# ---------------------------------------------------------------------------


def save_annotated_image(
    image: np.ndarray,
    output_path: Union[str, Path],
) -> str:
    """Save an annotated image to disk.

    Parameters
    ----------
    image : np.ndarray
        The annotated OpenCV BGR image to save.
    output_path : str or Path
        Destination file path (e.g. ``outputs/annotated_cabinet.png``).

    Returns
    -------
    str
        The absolute path of the saved file.

    Raises
    ------
    ValueError
        If the image is None or has zero size.
    """
    if image is None or image.size == 0:
        raise ValueError("Cannot save an empty or None image.")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), image)
    return str(out.resolve())


def save_evidence_crops(
    image: np.ndarray,
    items: list,
    output_dir: Union[str, Path],
) -> Dict[str, str]:
    """Extract and save individual evidence crop snippets for FAIL items.

    For each item that has an ``evidence_bbox`` and whose status name
    contains ``FAIL``, this function crops the region from *image* and
    writes it as a numbered PNG file inside *output_dir*.

    Parameters
    ----------
    image : np.ndarray
        The **original** (un-annotated) cabinet image in OpenCV BGR format.
    items : list
        List of ``InspectionItemResult`` objects (or any object with
        ``check_id``, ``status``, and ``evidence_bbox`` attributes).
    output_dir : str or Path
        Directory where crop files will be saved.

    Returns
    -------
    Dict[str, str]
        Mapping of ``check_id`` → saved crop file path for each FAIL item
        that had a valid bounding box.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    saved: Dict[str, str] = {}

    for item in items:
        status_val = item.status.value if hasattr(item.status, "value") else str(item.status)
        if "FAIL" not in status_val.upper():
            continue
        if item.evidence_bbox is None:
            continue

        crop = extract_crop(image, item.evidence_bbox)
        if crop.size == 0:
            continue

        fname = f"crop_{item.check_id}.png"
        crop_path = out / fname
        cv2.imwrite(str(crop_path), crop)
        saved[item.check_id] = str(crop_path.resolve())

    return saved


def try_ocr_region(
    image: np.ndarray,
    bbox: Optional[Tuple[int, int, int, int]] = None,
) -> Optional[str]:
    """Attempt lightweight OCR on a region of the image.

    Uses ``pytesseract`` if installed.  If the library is not available or
    OCR produces no readable text the function returns ``None`` so the
    caller can fall back to "Needs Manual Check".

    Parameters
    ----------
    image : np.ndarray
        Source image in OpenCV BGR format.
    bbox : Optional[Tuple[int, int, int, int]]
        If provided, OCR is run only on the cropped region ``(x1, y1, x2, y2)``.
        If ``None``, OCR is run on the full image.

    Returns
    -------
    Optional[str]
        Recognized text stripped of surrounding whitespace, or ``None``
        when OCR is unavailable or produces no output.
    """
    try:
        import pytesseract  # type: ignore
    except ImportError:
        # pytesseract is not installed — this is fine for the demo.
        return None

    region = image
    if bbox is not None:
        region = extract_crop(image, bbox)
        if region.size == 0:
            return None

    # Convert to grayscale for better OCR accuracy
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    try:
        text = pytesseract.image_to_string(gray, config="--psm 7").strip()
    except Exception:
        return None

    return text if text else None
