"""Web Interface module: HTTP routes for the SESS user workflows."""

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.identity_and_access import authenticate_user, validate_session

router = APIRouter()


def _not_implemented(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=501,
        content={"error": "not_implemented", "message": message},
    )


def _authentication_failed() -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "error": "authentication_failed",
            "message": "Authentication failed.",
        },
    )


def _authentication_required() -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "error": "authentication_required",
            "message": "A valid, active session is required.",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


def _require_session(request: Request) -> JSONResponse | None:
    """Return an error response unless the request carries a valid, active session.

    The session ID is read from an ``Authorization: Bearer <session_id>`` header.
    """
    scheme, _, token = request.headers.get("authorization", "").partition(" ")
    token = token.strip()
    if scheme.lower() != "bearer" or not token:
        return _authentication_required()
    try:
        validate_session(
            token,
            session_store=request.app.state.session_store,
            clock=datetime.now(timezone.utc),
            inactivity_timeout_seconds=request.app.state.inactivity_timeout_seconds,
        )
    except PermissionError:
        return _authentication_required()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "error": "session_service_unavailable",
                "message": "The session service is unavailable.",
            },
        )
    return None


@router.post("/api/authentication/sessions")
async def create_session(request: Request) -> JSONResponse:
    """FR-001: authenticate a healthcare professional."""
    try:
        payload = await request.json()
    except ValueError:
        payload = None
    username = payload.get("username") if isinstance(payload, dict) else None
    password = payload.get("password") if isinstance(payload, dict) else None
    if not isinstance(username, str) or not isinstance(password, str):
        return _authentication_failed()

    try:
        session = authenticate_user(
            username,
            password,
            identity_provider=request.app.state.identity_provider,
            session_store=request.app.state.session_store,
            clock=datetime.now(timezone.utc),
        )
    except PermissionError:
        return _authentication_failed()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "error": "identity_provider_unavailable",
                "message": "The identity provider is unavailable.",
            },
        )

    # Credentials are never returned.
    return JSONResponse(
        status_code=201,
        content={
            "session_id": session["session_id"],
            "user_id": session["user_id"],
            "permissions": session["permissions"],
            "created_at": session["created_at"].isoformat(),
            "last_activity_at": session["last_activity_at"].isoformat(),
        },
    )


@router.get("/api/patients/{patient_id}/records")
async def get_patient_records(patient_id: str, request: Request) -> JSONResponse:
    """FR-003 and FR-005: retrieve categorized patient records and apply search/filters."""
    rejection = _require_session(request)
    if rejection is not None:
        return rejection
    return _not_implemented("Patient record retrieval, categorization, and search are not implemented.")


@router.post("/api/patients/{patient_id}/summaries")
async def create_patient_summary(patient_id: str, request: Request) -> JSONResponse:
    """FR-002 and FR-006: generate a detail-level summary with source associations."""
    rejection = _require_session(request)
    if rejection is not None:
        return rejection
    return _not_implemented("Patient summary generation is not implemented.")


@router.get("/api/summaries/{summary_id}/items/{item_id}/source")
async def get_summary_item_source(
    summary_id: str, item_id: str, request: Request
) -> JSONResponse:
    """FR-004 and FR-006: authorize and resolve a summary item's source record."""
    rejection = _require_session(request)
    if rejection is not None:
        return rejection
    return _not_implemented("Summary-item source resolution is not implemented.")
