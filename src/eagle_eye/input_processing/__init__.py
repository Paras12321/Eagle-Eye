"""Input processing module for Eagle Eye."""

from .file_loader import (
    is_valid_image_extension,
    is_valid_checklist_extension,
    parse_evidence_box,
    parse_demo_status,
    load_checklist,
    validate_checklist_file,
    load_cabinet_image,
    validate_image_file,
    get_sample_image_path,
    get_sample_checklist_path,
    load_sample_demo_data,
    checklist_to_inspection_results,
)

__all__ = [
    "is_valid_image_extension",
    "is_valid_checklist_extension",
    "parse_evidence_box",
    "parse_demo_status",
    "load_checklist",
    "validate_checklist_file",
    "load_cabinet_image",
    "validate_image_file",
    "get_sample_image_path",
    "get_sample_checklist_path",
    "load_sample_demo_data",
    "checklist_to_inspection_results",
]
