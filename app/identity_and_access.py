"""Identity and Access module: authentication, role-based authorization, and sessions."""

from datetime import datetime
from typing import Any, Mapping, Protocol


class IdentityProvider(Protocol):
    def authenticate(self, username: str, password: str) -> Mapping[str, Any]: ...


class AuthorizationPolicy(Protocol):
    def can_access_patient(self, user_id: str, patient_id: str) -> bool: ...


class SessionStore(Protocol):
    def create(self, session: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def get(self, session_id: str) -> Mapping[str, Any] | None: ...
    def end(self, session_id: str) -> None: ...


def authenticate_user(
    username: str,
    password: str,
    *,
    identity_provider: IdentityProvider,
    session_store: SessionStore,
    clock: Any,
) -> Mapping[str, Any]:
    """Authenticate credentials and create an authenticated session."""
    raise NotImplementedError


def authorize_patient_access(
    user_id: str,
    patient_id: str,
    *,
    authorization_policy: AuthorizationPolicy,
    clock: Any,
) -> bool:
    """Determine whether the user's assigned role permits access to this patient."""
    raise NotImplementedError


def validate_session(
    session_id: str,
    *,
    session_store: SessionStore,
    clock: Any,
    inactivity_timeout_seconds: int,
) -> Mapping[str, Any]:
    """Validate a session and end or lock it after the configured inactivity period."""
    raise NotImplementedError
