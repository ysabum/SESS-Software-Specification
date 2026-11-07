"""Web Interface module: HTTP routes for the SESS user workflows."""

from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


def _not_implemented(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=501,
        content={"error": "not_implemented", "message": message},
    )


@router.post("/api/authentication/sessions")
async def create_session(request: Request) -> JSONResponse:
    """FR-001: authenticate a healthcare professional."""
    return _not_implemented("Authentication contract is defined but not implemented.")


@router.get("/api/patients/{patient_id}/records")
async def get_patient_records(patient_id: str, request: Request) -> JSONResponse:
    """FR-003 and FR-005: retrieve categorized patient records and apply search/filters."""
    return _not_implemented("Patient record retrieval, categorization, and search are not implemented.")


@router.post("/api/patients/{patient_id}/summaries")
async def create_patient_summary(patient_id: str, request: Request) -> JSONResponse:
    """FR-002 and FR-006: generate a detail-level summary with source associations."""
    return _not_implemented("Patient summary generation is not implemented.")


@router.get("/api/summaries/{summary_id}/items/{item_id}/source")
async def get_summary_item_source(
    summary_id: str, item_id: str, request: Request
) -> JSONResponse:
    """FR-004 and FR-006: authorize and resolve a summary item's source record."""
    return _not_implemented("Summary-item source resolution is not implemented.")
