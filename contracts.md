# SESS Contracts

## 1. Module/Function Contracts

All operation bodies are intentionally unimplemented and raise `NotImplementedError`. The listed results and failure modes are the proposed contract, not implemented behavior. The EHR remains the system of record. No contract writes clinical changes to it.


### Identity and Access

| Public function / signature | Success result | Failure behavior | Spec rule served | Injected dependencies |
|---|---|---|---|---|
| `authenticate_user(username: str, password: str, *, identity_provider: IdentityProvider, session_store: SessionStore, clock: Any) -> Mapping[str, Any]` | Authenticated session containing user identity, assigned role/permissions, session ID, and activity timestamps | Reject invalid credentials, identity-provider failure is surfaced, no session is created on failure | FR-001, NFR-001, AC-001 | Identity provider, session store, clock |
| `authorize_patient_access(user_id: str, patient_id: str, *, authorization_policy: AuthorizationPolicy, clock: Any) -> bool` | `True` only when configured organizational policy permits this user to access this patient | `False` for denied access, policy evaluation errors fail closed | FR-001, FR-004, NFR-001, AC-001, AC-004 | Configurable authorization policy, clock |
| `validate_session(session_id: str, *, session_store: SessionStore, clock: Any, inactivity_timeout_seconds: int) -> Mapping[str, Any]` | Valid, active session | Expired/unknown session is ended or locked and requires authentication | NFR-001, AC-001 session-inactivity scenario | Session store, clock, configured inactivity timeout |


### EHR Connector

| Public function / signature | Success result | Failure behavior | Spec rule served | Injected dependencies |
|---|---|---|---|---|
| `retrieve_patient_records(patient_id: str, *, ehr_client: EHRClient, clock: Any) -> Mapping[str, Any]` | Record batch preserving source identifiers, original timestamps, relevant context, retrieval time, and per-category availability | EHR/network errors are surfaced, partial retrieval reports unavailable categories, uninterpretable records/fields are reported, current data is not silently represented as current when unavailable | FR-002, FR-005, NFR-006, NFR-007, AC-002 | Agreed EHR client/interface, clock |


### Patient Records

| Public function / signature | Success result | Failure behavior | Spec rule served | Injected dependencies |
|---|---|---|---|---|
| `organize_patient_records(patient_id: str, source_records: Sequence[Mapping[str, Any]], *, clock: Any) -> Mapping[str, Any]` | Patient-scoped records grouped into demographics, medical history, diagnoses, medications, allergies, procedures, laboratory results, imaging, clinical notes, hospitalizations, and recent encounters | Unsupported/uninterpretable fields are reported, incomplete/conflicting source information is retained as flagged data rather than confirmed fact | FR-005, NFR-002, NFR-007, AC-005 | Clock, source records are supplied by EHR Connector |
| `search_patient_records(patient_id: str, search_term: str \| None, filters: Mapping[str, Any], *, user_id: str, clock: Any) -> Mapping[str, Any]` | Matching records limited to the selected patient and requested criteria (date, record type, diagnosis, medication, provider, procedure, laboratory test) | Unauthorized patient access is denied, invalid criteria are rejected, retrieval failures are surfaced | FR-003, NFR-001, NFR-004, NFR-005, AC-003 | User identity, clock, authorization is enforced through Identity and Access in the request flow |


### Summary Generation

| Public function / signature | Success result | Failure behavior | Spec rule served | Injected dependencies |
|---|---|---|---|---|
| `generate_patient_summary(patient_id: str, detail_level: str, *, user_id: str, clock: Any) -> Mapping[str, Any]` | Structured summary at `Brief`, `Standard`, or `Detailed` level, each clinical item carries source association, partial/unavailable, conflicting, incomplete, and stale data are explicitly identified | Reject unsupported detail level or unauthorized patient, report EHR unavailability, if records change during retrieval and a consistent single-request summary cannot be produced, notify user and require regeneration | FR-002, FR-006, NFR-002, NFR-003, NFR-004, NFR-006, NFR-007, AC-002, AC-007 | Patient Records, Identity and Access, Source Traceability, clock, configured summary-generation implementation |


### Source Traceability

| Public function / signature | Success result | Failure behavior | Spec rule served | Injected dependencies |
|---|---|---|---|---|
| `resolve_summary_item_source(summary_id: str, item_id: str, *, user_id: str, clock: Any) -> Mapping[str, Any]` | Originating source record reference, source timestamp, and available section/data-element context, source is displayed in SESS or opened through connected EHR | Deny if current authorization check fails, report missing/unresolvable source link, source/EHR unavailability is surfaced | FR-004, FR-006, NFR-001, NFR-003, NFR-007, AC-004, AC-006 | Identity and Access authorization, EHR Connector/source resolver, clock |


### Audit Recording

| Public function / signature | Success result | Failure behavior | Spec rule served | Injected dependencies |
|---|---|---|---|---|
| `record_audit_event(user_id: str, action: str, *, patient_id: str \| None, record_id: str \| None, occurred_at: Any, audit_store: Any) -> None` | Protected append-only audit entry with user, action, applicable patient/record reference, and timestamp | Audit-store failure is surfaced to the calling workflow, audit entries cannot be altered through ordinary application operations | NFR-008, AC-007 | Protected audit store, timestamp supplied by injected clock at call site |


## 2. REST API contracts

The application is web-based, so the following routes are included. Each route maps to a public module function. Routes currently return HTTP `501` and the exact error shape `{"error":"not_implemented","message":"..."}`. Request and response details below are proposed contracts for implementation.

| Method and route | Request contract | Success contract (when implemented) | Failure contract | Mapped public function | Spec rule served |
|---|---|---|---|---|---|
| `POST /api/authentication/sessions` | JSON: `{"username": string, "password": string}` | `201` with authenticated session ID, user identity, role/permissions, and expiry/activity metadata, never return credentials | `401` invalid credentials, `503` identity provider unavailable, `501` skeleton | `Identity and Access.authenticate_user` | FR-001, NFR-001, AC-001 |
| `GET /api/patients/{patient_id}/records` | Query: optional `q`, optional filters `date_from`, `date_to`, `record_type`, `diagnosis`, `medication`, `provider`, `procedure`, `laboratory_test` | `200` patient-scoped categorized records and matching results, including source identifiers/timestamps and category availability | `401` unauthenticated/expired session, `403` unauthorized patient, `422` invalid filters, `503` EHR unavailable, `501` skeleton | `Patient Records.search_patient_records` (which uses EHR Connector retrieval and record organization) | FR-003, FR-005, NFR-001, NFR-002, NFR-004, NFR-006, NFR-007, AC-003, AC-005 |
| `POST /api/patients/{patient_id}/summaries` | JSON: `{"detail_level":"Brief"}`, allowed values: `Brief`, `Standard`, `Detailed` | `200` structured summary with detail level, per-item source links, retrieval timestamp, stale/partial/conflict indicators | `401` unauthenticated/expired session, `403` unauthorized patient, `422` invalid detail level, `503` EHR unavailable/inconsistent retrieval, `501` skeleton | `Summary Generation.generate_patient_summary` (uses Patient Records and Source Traceability) | FR-002, FR-006, NFR-001–NFR-007 as applicable, AC-002, AC-007 |
| `GET /api/summaries/{summary_id}/items/{item_id}/source` | Authenticated session, summary and item identifiers in path | `200` source record or EHR launch reference, original timestamp, and available source section/context | `401` unauthenticated/expired session, `403` unauthorized source access, `404` missing summary item/source, `503` source EHR unavailable, `501` skeleton | `Source Traceability.resolve_summary_item_source` | FR-004, FR-006, NFR-001, NFR-003, NFR-007, AC-004, AC-006 |


## 3. Requirement-to-Entry-Point Review

| Requirement | Entry point in this skeleton | Coverage note |
|---|---|---|
| FR-001 Authentication | `POST /api/authentication/sessions` → `authenticate_user`, session validation and patient authorization are additional Identity and Access contracts | Includes the acceptance criterion for inactive-session timeout through `validate_session`. |
| FR-002 Generate summary | `POST /api/patients/{patient_id}/summaries` → `generate_patient_summary` | Includes the three detail levels and partial/stale-data reporting in the contract. |
| FR-003 Search/filter | `GET /api/patients/{patient_id}/records` → `search_patient_records` | Search and filters are patient-scoped. |
| FR-004 Verify summary source | `GET /api/summaries/{summary_id}/items/{item_id}/source` → `resolve_summary_item_source` | Requires a fresh authorization check before source disclosure. |
| FR-005 Organize PHI | `GET /api/patients/{patient_id}/records` → `search_patient_records`, with `organize_patient_records` as the internal Patient Records operation | Categorization is part of record retrieval, not a separate user-facing operation. |
| FR-006 Maintain traceability | Summary route → `generate_patient_summary`, source route → `resolve_summary_item_source` | Every clinical summary item must retain an originating source association. |
| NFR-008 Auditability | Internal calls to `record_audit_event` from authentication, authorization failure, patient-record access, summary generation, source viewing, and permission-change workflows | The architecture defines Audit Recording as a recording module, not an audit-query API, therefore no additional public REST route is introduced. |

NFR-001, NFR-002, NFR-004, NFR-005, NFR-006, and NFR-007 are enforced as cross-cutting constraints on the listed entry points and module contracts, rather than by inventing standalone routes for quality attributes. The architecture does not define a public permission-administration or audit-browsing function, so this skeleton does not add one.


## 4. Explicitly Not Implemented

- No clinical write-back, prescribing, diagnosis editing, or order entry
- No EHR vendor, FHIR profile, or real EHR client selection, the agreed interface is still deployment-specific
- No identity provider, role matrix, patient-assignment policy, session store, audit database, or persistence implementation
- No AI/LLM or rule-based summarization algorithm
- No cache, local EHR replica, summary retention policy, or historical-summary API.
- No separate services or additional business modules
