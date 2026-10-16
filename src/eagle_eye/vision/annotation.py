"""Visual annotation and evidence marking tools for cabinet photos.

Owned by: MEMBER 2 (Computer Vision)
"""

from typing import Tuple, Optional
import cv2
import numpy as np


def draw_bounding_box(
    image: np.ndarray,
    bbox: Tuple[int, int, int, int],
    label: Optional[str] = None,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2,
) -> np.ndarray:
    """Draw a bounding box and optional text label on an image.

    Parameters
    ----------
    image : np.ndarray
        Source image.
    bbox : Tuple[int, int, int, int]
        Bounding box coordinates (x1, y1, x2, y2).
    label : Optional[str]
        Text label to display above or inside the box.
    color : Tuple[int, int, int]
        BGR color tuple (default is green).
    thickness : int
        Border line thickness.

    Returns
    -------
    np.ndarray
        Annotated copy of the image.
    """
    annotated = image.copy()
    x1, y1, x2, y2 = bbox
    cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)

    if label:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)
        # Background box for readable text
        bg_y1 = max(0, y1 - text_h - 6)
        cv2.rectangle(
            annotated,
            (x1, bg_y1),
            (x1 + text_w + 4, bg_y1 + text_h + 4),
            color,
            cv2.FILLED,
        )
        # White text on colored background
        cv2.putText(
            annotated,
            label,
            (x1 + 2, bg_y1 + text_h + 1),
            font,
            font_scale,
            (255, 255, 255),
            font_thickness,
            lineType=cv2.LINE_AA,
        )

    return annotated


def draw_issue_marker(
    image: np.ndarray,
    point: Tuple[int, int],
    marker_id: int,
    color: Tuple[int, int, int] = (0, 0, 255),
    radius: int = 16,
) -> np.ndarray:
    """Draw a numbered circular issue marker on an image.

    Parameters
    ----------
    image : np.ndarray
        Source image.
    point : Tuple[int, int]
        Center (x, y) coordinates.
    marker_id : int
        Numerical marker ID to show inside the circle.
    color : Tuple[int, int, int]
        BGR color for the marker circle (default is red).
    radius : int
        Circle radius in pixels.

    Returns
    -------
    np.ndarray
        Annotated copy of the image.
    """
    annotated = image.copy()
    cx, cy = point

    # Draw filled circle
    cv2.circle(annotated, (cx, cy), radius, color, cv2.FILLED)
    # White border
    cv2.circle(annotated, (cx, cy), radius, (255, 255, 255), 2)

    # Number text centered
    text = str(marker_id)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    tx = cx - (text_w // 2)
    ty = cy + (text_h // 2)
    cv2.putText(
        annotated,
        text,
        (tx, ty),
        font,
        font_scale,
        (255, 255, 255),
        font_thickness,
        lineType=cv2.LINE_AA,
    )

    return annotated
