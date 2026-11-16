"""SESS single-deployable web application entry point."""

import hashlib
import hmac
import secrets
from typing import Any, Mapping

from fastapi import FastAPI
from app.web_interface import router


# ---------------------------------------------------------------------------
# DEVELOPMENT-ONLY wiring for the Identity and Access collaborators.
# The spec leaves the real identity provider and session store to the
# deploying organization (architecture.md, contracts.md section 4). These
# in-memory stand-ins exist so the login route can run end to end; replace
# them with the organization's implementations before real use. The demo
# account below carries no permissions because the role matrix is undefined.
# ---------------------------------------------------------------------------
_DEMO_USERNAME = "clinician"
_DEMO_PASSWORD = "valid-password"
_PBKDF2_ITERATIONS = 200_000


def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS)


class InMemoryIdentityProvider:
    """Development identity provider. Raises ``PermissionError`` on rejected credentials."""

    def __init__(self, users: Mapping[str, tuple[str, list[str]]]) -> None:
        self._users: dict[str, tuple[bytes, bytes, list[str]]] = {}
        for username, (password, permissions) in users.items():
            salt = secrets.token_bytes(16)
            self._users[username] = (salt, _hash_password(password, salt), permissions)
        # Used for unknown usernames so the check costs the same either way.
        self._dummy_salt = secrets.token_bytes(16)
        self._dummy_hash = _hash_password(secrets.token_urlsafe(16), self._dummy_salt)

    def authenticate(self, username: str, password: str) -> Mapping[str, Any]:
        record = self._users.get(username)
        salt, expected, permissions = record or (self._dummy_salt, self._dummy_hash, [])
        matches = hmac.compare_digest(_hash_password(password, salt), expected)
        if record is None or not matches:
            raise PermissionError("invalid credentials")
        return {"user_id": username, "permissions": list(permissions)}


class InMemorySessionStore:
    """Development session store."""

    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}

    def create(self, session: Mapping[str, Any]) -> Mapping[str, Any]:
        self._sessions[session["session_id"]] = dict(session)
        return self._sessions[session["session_id"]]

    def get(self, session_id: str) -> Mapping[str, Any] | None:
        return self._sessions.get(session_id)

    def update(self, session: Mapping[str, Any]) -> Mapping[str, Any]:
        if session["session_id"] not in self._sessions:
            raise KeyError(session["session_id"])
        self._sessions[session["session_id"]] = dict(session)
        return self._sessions[session["session_id"]]

    def end(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)


app = FastAPI(
    title="SESS",
    version="0.1.0",
    description="Runnable API skeleton. Business operations are intentionally unimplemented.",
)

app.state.identity_provider = InMemoryIdentityProvider({_DEMO_USERNAME: (_DEMO_PASSWORD, [])})
app.state.session_store = InMemorySessionStore()
# Development default; the deploying organization configures the real value (NFR-001).
app.state.inactivity_timeout_seconds = 900

app.include_router(router)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"application": "SESS", "status": "skeleton"}
