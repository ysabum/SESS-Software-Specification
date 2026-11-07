
from collections.abc import Mapping
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.identity_and_access import (
    authenticate_user,
    authorize_patient_access,
    validate_session,
)
from app.summary_generation import generate_patient_summary
from app.patient_records import (
    organize_patient_records,
    search_patient_records,
)
from app.source_traceability import resolve_summary_item_source
from app.audit_recording import record_audit_event

NOW = datetime(2026, 11, 7, 18, 0, tzinfo=timezone.utc)
PATIENT_ID = "patient-100"
USER_ID = "user-100"


@pytest.fixture
def client():
    return TestClient(app)


class CallSpy:
    """Records calls to an injected dependency."""
    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            return None
        return record


def assert_rejection_is_implemented(exc_info):
    # The contracts do not specify a concrete exception type.
    assert not isinstance(exc_info.value, NotImplementedError)


# ============================================================
# AT-01 / AC-001: Authentication and authorization
# ============================================================

def test_AT01_valid_credentials_return_authenticated_session_mapping():
    result = authenticate_user(
        "clinician",
        "valid-password",
        identity_provider=MagicMock(),
        session_store=MagicMock(),
        clock=NOW,
    )
    assert isinstance(result, Mapping)
    assert result


def test_AT01_invalid_credentials_rejected_without_returning_session():
    with pytest.raises(Exception) as exc:
        authenticate_user(
            "clinician",
            "wrong-password",
            identity_provider=MagicMock(),
            session_store=CallSpy(),
            clock=NOW,
        )
    assert_rejection_is_implemented(exc)


def test_AT01_unauthorized_patient_access_returns_false():
    policy = MagicMock()
    policy.is_allowed.return_value = False

    assert authorize_patient_access(
        USER_ID,
        PATIENT_ID,
        authorization_policy=policy,
        clock=NOW,
    ) is False


def test_AT01_inactive_session_is_rejected():
    with pytest.raises(Exception) as exc:
        validate_session(
            "expired-session",
            session_store=CallSpy(),
            clock=NOW,
            inactivity_timeout_seconds=900,
        )
    assert_rejection_is_implemented(exc)


# ============================================================
# AT-02 / AC-002: Patient summary generation
# ============================================================

@pytest.mark.parametrize("level", ["Brief", "Standard", "Detailed"])
def test_AT02_generate_summary_for_each_supported_detail_level(level):
    result = generate_patient_summary(
        PATIENT_ID,
        level,
        user_id=USER_ID,
        clock=NOW,
    )
    assert isinstance(result, Mapping)
    assert result


def test_AT02_unsupported_detail_level_is_rejected():
    with pytest.raises(Exception) as exc:
        generate_patient_summary(
            PATIENT_ID,
            "Ultra",
            user_id=USER_ID,
            clock=NOW,
        )
    assert_rejection_is_implemented(exc)


def test_AT02_unauthorized_patient_summary_is_rejected():
    with pytest.raises(Exception) as exc:
        generate_patient_summary(
            "patient-not-authorized",
            "Brief",
            user_id="unauthorized-user",
            clock=NOW,
        )
    assert_rejection_is_implemented(exc)


# ============================================================
# AT-03 / AC-003: Search and filtering
# ============================================================

def test_AT03_search_returns_matching_patient_records():
    result = search_patient_records(
        PATIENT_ID,
        "hypertension",
        {
            "diagnosis": "hypertension",
            "record_type": "clinical_note",
        },
        user_id=USER_ID,
        clock=NOW,
    )
    assert isinstance(result, Mapping)
    assert result


def test_AT03_invalid_search_criteria_are_rejected():
    with pytest.raises(Exception) as exc:
        search_patient_records(
            PATIENT_ID,
            "test",
            {"date_from": "not-a-date"},
            user_id=USER_ID,
            clock=NOW,
        )
    assert_rejection_is_implemented(exc)


def test_AT03_unauthorized_patient_search_is_rejected():
    with pytest.raises(Exception) as exc:
        search_patient_records(
            "patient-not-authorized",
            "diagnosis",
            {},
            user_id="unauthorized-user",
            clock=NOW,
        )
    assert_rejection_is_implemented(exc)


# ============================================================
# AT-04 / AC-004: Source-record verification
# ============================================================

def test_AT04_source_resolution_returns_source_mapping():
    result = resolve_summary_item_source(
        "summary-100",
        "item-100",
        user_id=USER_ID,
        clock=NOW,
    )
    assert isinstance(result, Mapping)
    assert result


def test_AT04_unauthorized_source_access_is_rejected():
    with pytest.raises(Exception) as exc:
        resolve_summary_item_source(
            "summary-100",
            "item-100",
            user_id="unauthorized-user",
            clock=NOW,
        )
    assert_rejection_is_implemented(exc)


def test_AT04_missing_source_item_is_rejected():
    with pytest.raises(Exception) as exc:
        resolve_summary_item_source(
            "missing-summary",
            "missing-item",
            user_id=USER_ID,
            clock=NOW,
        )
    assert_rejection_is_implemented(exc)


# ============================================================
# AT-05 / AC-005: Organize patient information
# ============================================================

def test_AT05_organize_available_patient_records_returns_mapping():
    result = organize_patient_records(
        PATIENT_ID,
        [{"source_id": "src-1", "source_value": "sample"}],
        clock=NOW,
    )
    assert isinstance(result, Mapping)
    assert result


# ============================================================
# AT-06 / AC-006: Summary traceability
# ============================================================

def test_AT06_traceability_returns_source_descriptor():
    result = resolve_summary_item_source(
        "summary-100",
        "item-100",
        user_id=USER_ID,
        clock=NOW,
    )
    assert isinstance(result, Mapping)
    assert result

    # The contract requires source reference, timestamp, and available
    # section/data-element context, but does not specify exact field names.


# ============================================================
# AT-07 / AC-007: Audit recording
# ============================================================

def test_AT07_record_summary_generation_audit_event():
    audit_store = CallSpy()

    result = record_audit_event(
        USER_ID,
        "summary_generation",
        patient_id=PATIENT_ID,
        record_id=None,
        occurred_at=NOW,
        audit_store=audit_store,
    )

    assert result is None
    assert audit_store.calls


# ============================================================
# REST API contract tests
# ============================================================

def test_AT01_api_valid_login_returns_201_and_session_data(client):
    response = client.post(
        "/api/authentication/sessions",
        json={
            "username": "clinician",
            "password": "valid-password",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body, dict) and body
    assert "password" not in body


def test_AT01_api_invalid_login_returns_401_without_session_data(client):
    response = client.post(
        "/api/authentication/sessions",
        json={
            "username": "clinician",
            "password": "wrong-password",
        },
    )

    body = response.json()
    assert "password" not in body
    assert "session_id" not in body
    assert response.status_code == 401


def test_AT03_api_records_rejects_unauthenticated_request(client):
    response = client.get(
        f"/api/patients/{PATIENT_ID}/records"
    )

    body = response.json()
    assert "records" not in body
    assert response.status_code == 401


def test_AT02_api_summary_rejects_unauthenticated_request_without_summary(client):
    response = client.post(
        f"/api/patients/{PATIENT_ID}/summaries",
        json={"detail_level": "Brief"},
    )

    body = response.json()
    assert "summary_id" not in body
    assert "summary" not in body
    assert response.status_code == 401


def test_AT04_api_source_rejects_unauthenticated_request_without_disclosure(client):
    response = client.get(
        "/api/summaries/summary-100/items/item-100/source"
    )

    body = response.json()
    assert not any(
        key in body
        for key in ("source", "source_record", "source_record_id")
    )
    assert response.status_code == 401


# ============================================================
# Skeleton placeholder checks
# These should pass until the routes are implemented.
# ============================================================

@pytest.mark.parametrize(
    "method,path,payload",
    [
        (
            "post",
            "/api/authentication/sessions",
            {"username": "clinician", "password": "valid-password"},
        ),
        (
            "get",
            f"/api/patients/{PATIENT_ID}/records",
            None,
        ),
        (
            "post",
            f"/api/patients/{PATIENT_ID}/summaries",
            {"detail_level": "Brief"},
        ),
        (
            "get",
            "/api/summaries/summary-100/items/item-100/source",
            None,
        ),
    ],
)
def test_skeleton_routes_report_documented_501_error_shape(
    client, method, path, payload
):
    request = getattr(client, method)

    if payload:
        response = request(path, json=payload)
    else:
        response = request(path)

    assert response.status_code == 501

    body = response.json()
    assert body.get("error") == "not_implemented"
    assert isinstance(body.get("message"), str)
    assert body["message"]