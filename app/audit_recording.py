"""Audit Recording module: append protected audit events."""

from typing import Any, Mapping


def record_audit_event(
    user_id: str,
    action: str,
    *,
    patient_id: str | None,
    record_id: str | None,
    occurred_at: Any,
    audit_store: Any,
) -> None:
    """Record an auditable event with actor, action, applicable reference, and timestamp."""
    raise NotImplementedError
