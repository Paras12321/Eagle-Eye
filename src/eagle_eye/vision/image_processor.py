"""Image processing utilities for cabinet quality inspection.

Owned by: MEMBER 2 (Computer Vision)
"""

from typing import Tuple, Union
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
