"""Identity and Access module: authentication, role-based authorization, and sessions."""

import secrets
from datetime import datetime
from typing import Any, Mapping, Protocol


class IdentityProvider(Protocol):
    def authenticate(self, username: str, password: str) -> Mapping[str, Any]: ...


class AuthorizationPolicy(Protocol):
    def can_access_patient(self, user_id: str, patient_id: str) -> bool: ...


class SessionStore(Protocol):
    def create(self, session: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def get(self, session_id: str) -> Mapping[str, Any] | None: ...
    def update(self, session: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def end(self, session_id: str) -> None: ...


def authenticate_user(
    username: str,
    password: str,
    *,
    identity_provider: IdentityProvider,
    session_store: SessionStore,
    clock: Any,
) -> Mapping[str, Any]:
    """Authenticate credentials and create an authenticated session.

    The identity provider signals rejected credentials by raising
    ``PermissionError``; any other exception is an identity-provider failure and
    is surfaced unchanged. No session is created unless authentication succeeds,
    and a session store that returns ``None`` from ``create`` is treated as a failure.
    ``clock`` is a ``datetime`` value supplied fresh by the caller.
    """
    identity = identity_provider.authenticate(username, password)

    session = {
        "session_id": secrets.token_urlsafe(32),
        "user_id": identity["user_id"],
        "permissions": identity["permissions"],
        "created_at": clock,
        "last_activity_at": clock,
    }
    if session_store.create(session) is None:
        # The store did not confirm the session; do not hand out a session that
        # may not exist.
        raise RuntimeError("session store did not confirm session creation")
    return session


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
    """Validate a session and end it after the configured inactivity period.

    Raises ``PermissionError`` for an unknown session or one that has been idle
    for longer than ``inactivity_timeout_seconds`` (the session is then ended, so
    authentication is required again). A session idle for exactly the timeout is
    still valid. On success ``last_activity_at`` is refreshed to ``clock`` and the
    refreshed session is returned. ``clock`` is a ``datetime`` value.
    """
    session = session_store.get(session_id)
    if session is None:
        raise PermissionError("unknown or ended session")

    idle_seconds = (clock - session["last_activity_at"]).total_seconds()
    if idle_seconds > inactivity_timeout_seconds:
        session_store.end(session_id)
        raise PermissionError("session expired after inactivity")

    refreshed = {**session, "last_activity_at": clock}
    session_store.update(refreshed)
    return refreshed
