"""Vision module for Eagle Eye."""

from .image_processor import (
    load_image_from_bytes,
    resize_image_aspect_ratio,
    extract_crop,
    save_annotated_image,
    save_evidence_crops,
    try_ocr_region,
)
from .annotation import draw_bounding_box, draw_issue_marker, draw_demo_evidence_label

__all__ = [
    "load_image_from_bytes",
    "resize_image_aspect_ratio",
    "extract_crop",
    "save_annotated_image",
    "save_evidence_crops",
    "try_ocr_region",
    "draw_bounding_box",
    "draw_issue_marker",
    "draw_demo_evidence_label",
]
