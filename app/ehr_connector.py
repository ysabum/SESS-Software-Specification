"""EHR Connector module: read records from the organization's agreed EHR interface."""

from typing import Any, Mapping, Protocol, Sequence


class EHRClient(Protocol):
    def get_patient_records(self, patient_id: str) -> Sequence[Mapping[str, Any]]: ...


def retrieve_patient_records(
    patient_id: str,
    *,
    ehr_client: EHRClient,
    clock: Any,
) -> Mapping[str, Any]:
    """Retrieve current EHR records while preserving source IDs, timestamps, and context."""
    raise NotImplementedError
