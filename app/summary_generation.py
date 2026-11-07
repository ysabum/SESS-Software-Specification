"""Summary Generation module: create a structured summary at the selected detail level."""

from typing import Any, Mapping


def generate_patient_summary(
    patient_id: str,
    detail_level: str,
    *,
    user_id: str,
    clock: Any,
) -> Mapping[str, Any]:
    """Generate a summary from one retrieval request; preserve meaning and flag data gaps."""
    raise NotImplementedError
