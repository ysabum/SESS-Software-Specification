"""Patient Records module: categorize, search, and filter patient-scoped records."""

from typing import Any, Mapping, Sequence


def organize_patient_records(
    patient_id: str,
    source_records: Sequence[Mapping[str, Any]],
    *,
    clock: Any,
) -> Mapping[str, Any]:
    """Organize available PHI into the predefined SESS categories."""
    raise NotImplementedError


def search_patient_records(
    patient_id: str,
    search_term: str | None,
    filters: Mapping[str, Any],
    *,
    user_id: str,
    clock: Any,
) -> Mapping[str, Any]:
    """Search/filter records within one patient after patient access is authorized."""
    raise NotImplementedError
