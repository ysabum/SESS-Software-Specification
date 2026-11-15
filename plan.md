# SESS Implementation Plan
## Baseline

`tests/test_sess_contracts.py`: **27 tests, 23 failing, 4 passing.**

### Test Output

```
test_AT01_valid_credentials_return_authenticated_session_mapping FAILED
test_AT01_invalid_credentials_rejected_without_returning_session FAILED
test_AT01_unauthorized_patient_access_returns_false FAILED
test_AT01_inactive_session_is_rejected FAILED

test_AT02_generate_summary_for_each_supported_detail_level[Brief] FAILED
test_AT02_generate_summary_for_each_supported_detail_level[Standard] FAILED
test_AT02_generate_summary_for_each_supported_detail_level[Detailed] FAILED
test_AT02_unsupported_detail_level_is_rejected FAILED
test_AT02_unauthorized_patient_summary_is_rejected FAILED

test_AT03_search_returns_matching_patient_records FAILED
test_AT03_invalid_search_criteria_are_rejected FAILED
test_AT03_unauthorized_patient_search_is_rejected FAILED

test_AT04_source_resolution_returns_source_mapping FAILED
test_AT04_unauthorized_source_access_is_rejected FAILED
test_AT04_missing_source_item_is_rejected FAILED

test_AT05_organize_available_patient_records_returns_mapping FAILED
test_AT06_traceability_returns_source_descriptor FAILED
test_AT07_record_summary_generation_audit_event FAILED

test_AT01_api_valid_login_returns_201_and_session_data FAILED
test_AT01_api_invalid_login_returns_401_without_session_data FAILED
test_AT03_api_records_rejects_unauthenticated_request FAILED
test_AT02_api_summary_rejects_unauthenticated_request_without_summary FAILED
test_AT04_api_source_rejects_unauthenticated_request_without_disclosure FAILED

test_skeleton_routes_report_documented_501_error_shape [POST sessions] PASSED
test_skeleton_routes_report_documented_501_error_shape [GET records] PASSED
test_skeleton_routes_report_documented_501_error_shape [POST summaries] PASSED
test_skeleton_routes_report_documented_501_error_shape [GET source] PASSED

========================= 23 failed, 4 passed in 0.35s =========================
```

Failing tests grouped by acceptance criterion (by the test's `ATnn` prefix):

| AC | Failing tests | Cause today |
|---|---|---|
| AC-001 (6) | `test_AT01_valid_credentials_return_authenticated_session_mapping`, `test_AT01_invalid_credentials_rejected_without_returning_session`, `test_AT01_unauthorized_patient_access_returns_false`, `test_AT01_inactive_session_is_rejected`, `test_AT01_api_valid_login_returns_201_and_session_data`, `test_AT01_api_invalid_login_returns_401_without_session_data` | `NotImplementedError` / route returns 501 |
| AC-002 (6) | `test_AT02_generate_summary_for_each_supported_detail_level[Brief]`, `[Standard]`, `[Detailed]`, `test_AT02_unsupported_detail_level_is_rejected`, `test_AT02_unauthorized_patient_summary_is_rejected`, `test_AT02_api_summary_rejects_unauthenticated_request_without_summary` | same |
| AC-003 (4) | `test_AT03_search_returns_matching_patient_records`, `test_AT03_invalid_search_criteria_are_rejected`, `test_AT03_unauthorized_patient_search_is_rejected`, `test_AT03_api_records_rejects_unauthenticated_request` | same |
| AC-004 (4) | `test_AT04_source_resolution_returns_source_mapping`, `test_AT04_unauthorized_source_access_is_rejected`, `test_AT04_missing_source_item_is_rejected`, `test_AT04_api_source_rejects_unauthenticated_request_without_disclosure` | same |
| AC-005 (1) | `test_AT05_organize_available_patient_records_returns_mapping` | `NotImplementedError` |
| AC-006 (1) | `test_AT06_traceability_returns_source_descriptor` | `NotImplementedError` |
| AC-007 (1) | `test_AT07_record_summary_generation_audit_event` | `NotImplementedError` |

Passing today (all four are placeholders that assert HTTP 501): `test_skeleton_routes_report_documented_501_error_shape[post-/api/authentication/sessions-payload0]`, `[get-/api/patients/patient-100/records-None]`, `[post-/api/patients/patient-100/summaries-payload2]`, `[get-/api/summaries/summary-100/items/item-100/source-None]`. See Test issue TI-1.

Eight "rejection" tests only assert that the exception is *not* `NotImplementedError`; they are red today only for that reason (see TI-2).

## Code Slices

They are the slices whose listed tests can be made to pass using only the signatures in `contracts.md`, with the fewest unanswered design questions. The deferred work (summary, search, source resolution) is more central to the product, but its tests cannot be satisfied as written until Design question DQ-1 is answered (see "Deferred").

**Order:** authentication (leaf module) → session validity and gating → patient authorization and audit (leaf modules) → organization of records (pure function that later search and summary slices build on).


---


## Slice 1: Login Thin Path

- **Name:** Login thin path
- **Goal:** `POST /api/authentication/sessions` creates a session for valid credentials (201) and rejects invalid ones (401) without leaking credentials or a session.
- **Spec sources:** FR-001; NFR-001 (authentication, no credential disclosure); spec AC-001 scenarios 1-2; architecture §2 Identity and Access, §3 steps 1-2; contracts §1 `authenticate_user`, §2 `POST /api/authentication/sessions`; test_plan AC-001 cases A-B.
- **Criteria:** Advances AC-001 (scenarios 1-2 of 4). AC-001 is completed in Slice 3.
- **Tests that should turn green:**
  - `test_AT01_valid_credentials_return_authenticated_session_mapping`
  - `test_AT01_invalid_credentials_rejected_without_returning_session`
  - `test_AT01_api_valid_login_returns_201_and_session_data`
  - `test_AT01_api_invalid_login_returns_401_without_session_data`
- **Skeleton to fill in:** `identity_and_access.authenticate_user`; route `POST /api/authentication/sessions` (`create_session` in `web_interface.py`).
- **Depends on:** none. Blocked on DQ-1, DQ-3, DQ-4 and DQ-6 for the two API tests; the two module tests are blockable only by DQ-3, DQ-4 and DQ-6.
- **Done when:** the listed tests pass and no previously passing test fails. Expected exception (TI-1): `test_skeleton_routes_report_documented_501_error_shape[post-/api/authentication/sessions-payload0]` will go red by design.
- **Status:** DONE


## Slice 2: Session Validity and Unauthenticated Gating

- **Name:** Session validity and unauthenticated gating
- **Goal:** A missing, unknown or idle-expired session is refused with 401 before any patient data or source is returned, and sessions idle longer than the configured timeout are ended.
- **Spec sources:** NFR-001 (inactive sessions end or lock); spec AC-001 scenario 4; architecture §3 steps 3 and 12, §4 (session locking decision); contracts §1 `validate_session`, §2 the `401` failure rows of the records, summaries and source routes; test_plan AC-001 case D, EX-003, EX-010.
- **Criteria:** Advances AC-001 (scenario 4). The three API tests below are named under AC-003, AC-002 and AC-004, but they only verify the 401 gate; they do not complete those criteria.
- **Tests that should turn green:**
  - `test_AT01_inactive_session_is_rejected`
  - `test_AT03_api_records_rejects_unauthenticated_request`
  - `test_AT02_api_summary_rejects_unauthenticated_request_without_summary`
  - `test_AT04_api_source_rejects_unauthenticated_request_without_disclosure`
- **Skeleton to fill in:** `identity_and_access.validate_session`; the unauthenticated (401) branch only of `GET /api/patients/{patient_id}/records`, `POST /api/patients/{patient_id}/summaries`, `GET /api/summaries/{summary_id}/items/{item_id}/source`. The authenticated branch of each stays 501.
- **Depends on:** Slice 1 (sessions must exist to be validated).
- **Done when:** the listed tests pass and no previously passing test fails. Expected exceptions (TI-1): the skeleton 501 tests for the records, summaries and source routes will go red by design, because an unauthenticated call now returns 401. Rule kept in this slice alone because timeout handling is the easiest place for an off-by-one (EX-003; behavior at exactly `T` is unspecified, so do not assert it).
- **Status:** not started


## Slice 3: Patient Authorization and Audit Primitive

- **Name:** Patient authorization and audit primitive
- **Goal:** Patient access is granted only when the injected policy returns literal `True` (anything else, including errors, is denied), and an audit event can be appended with user, action, patient/record reference and timestamp.
- **Spec sources:** FR-001; NFR-001; NFR-008; spec AC-001 scenario 3, AC-007; architecture §2 Audit Recording, §3 steps 3 and 10; contracts §1 `authorize_patient_access`, `record_audit_event`; test_plan AC-001 case C, AC-007 case A, EX-005.
- **Criteria:** Completes AC-001 (scenario 3, the last open one). Advances AC-007 at function level only: the scenario "when a patient summary is generated" cannot complete until summary generation (deferred) calls `record_audit_event`.
- **Tests that should turn green:**
  - `test_AT01_unauthorized_patient_access_returns_false`
  - `test_AT07_record_summary_generation_audit_event`
- **Skeleton to fill in:** `identity_and_access.authorize_patient_access`; `audit_recording.record_audit_event`. No routes.
- **Depends on:** Slice 2, for ordering only: authentication must precede authorization (EX-010). No code dependency, since both modules are leaves in architecture §2.
- **Done when:** the listed tests pass and no previously passing test fails. Fail-closed handling is why authorization sits in its own slice with the audit primitive that records its failures (NFR-008).
- **Status:** not started

## Slice 4: Organize Records Into the Eleven Categories

- **Name:** Organize records into categories
- **Goal:** Supplied source records are grouped into the eleven predefined categories, and anything uninterpretable is reported rather than silently treated as categorized.
- **Spec sources:** FR-005; NFR-002 and NFR-007 (flag, do not confirm, incomplete/uninterpretable data); spec AC-005; architecture §2 Patient Records, §3 step 6; contracts §1 `organize_patient_records`; test_plan AC-005 cases A-C, EX-012.
- **Criteria:** Completes AC-005.
- **Tests that should turn green:**
  - `test_AT05_organize_available_patient_records_returns_mapping`
- **Skeleton to fill in:** `patient_records.organize_patient_records`.
- **Depends on:** none. This is a pure function, so it is independent of Slices 1-3. Later search and summary slices depend on it.
- **Done when:** the listed test passes and no previously passing test fails. Blocked on DQ-5 (record shape).
- **Status:** not started


---


## Deferred (beyond the four-slice cap)

These 12 failing tests, 4 criteria and 5 skeleton items fit no slice above:

- **Tests (12):** `test_AT02_generate_summary_for_each_supported_detail_level[Brief]`, `[Standard]`, `[Detailed]`, `test_AT02_unsupported_detail_level_is_rejected`, `test_AT02_unauthorized_patient_summary_is_rejected`, `test_AT03_search_returns_matching_patient_records`, `test_AT03_invalid_search_criteria_are_rejected`, `test_AT03_unauthorized_patient_search_is_rejected`, `test_AT04_source_resolution_returns_source_mapping`, `test_AT04_unauthorized_source_access_is_rejected`, `test_AT04_missing_source_item_is_rejected`, `test_AT06_traceability_returns_source_descriptor`.
- **Criteria with no completing slice:** AC-002, AC-003, AC-004, AC-006. AC-007's scenario is also incomplete (function-level only after Slice 3).
- **Functions with no slice:** `ehr_connector.retrieve_patient_records` (no test exercises it at all), `patient_records.search_patient_records`, `summary_generation.generate_patient_summary`, `source_traceability.resolve_summary_item_source`.
- **Routes with no slice:** the authenticated branches of `GET /api/patients/{patient_id}/records`, `POST /api/patients/{patient_id}/summaries`, `GET /api/summaries/{summary_id}/items/{item_id}/source` (still 501 after Slice 2).

Suggested order if more slices are approved: search (AC-003, needs `retrieve_patient_records` + Slice 4), then summary generation (AC-002, AC-007 scenario), then source resolution (AC-004, AC-006). All three are blocked on DQ-1 and TI-5.

---

## Design Questions

Raised instead of adding anything new.

- **DQ-1: Collaborator wiring.** Only some functions take injected dependencies. `generate_patient_summary`, `search_patient_records` and `resolve_summary_item_source` take no policy, EHR client, session store or summary store, and the routes have no place to obtain them. Where do these come from (e.g. `app.state` set in `main.py`)? The API login tests expect `clinician` / `valid-password` to succeed with zero setup, so some default must exist. The contracts say no identity provider or session store is implemented.
- **DQ-2: Session transport.** How does a route receive the session ID (header, cookie)? Not specified in contracts. Affects Slice 2.
- **DQ-3: Rejection signalling.** Contracts say "reject" without naming exception types, and `IdentityProvider.authenticate` has no stated failure signal (raise or return nothing?). May new exception classes be introduced, or should built-ins be used?
- **DQ-4: `clock: Any`.** Tests pass a `datetime`; contracts leave it open. Value or callable?
- **DQ-5: Source-record shape.** The test's record has only `source_id` and `source_value`; no field says which category it belongs to. Which key determines category, and what is the result key for uninterpretable items?
- **DQ-6: Session record shape and activity updates.** `SessionStore` offers only `create`, `get`, `end`. Inactivity measured from last activity needs an update method; is end-then-create acceptable? Key names for session ID and last-activity are also unspecified.
- **DQ-7: Who calls Audit Recording.** Contracts say authentication events and failed authorization are audited, but `authenticate_user` and `authorize_patient_access` take no `audit_store`, and architecture §2 lists no module as depending on Audit Recording. Until answered, authentication-event and failed-authorization auditing (NFR-008) is untestable and unscheduled.


## Test Issues

No test was changed.

- **TI-1: Placeholder 501 tests contradict "no previously passing test fails".** All four are labeled "should pass until the routes are implemented" and will necessarily fail: Slice 1 turns the sessions one red, Slice 2 the other three.
- **TI-2: Eight rejection tests are weak.** Each only asserts the exception is not `NotImplementedError`, so any `TypeError` or `AttributeError` passes. `test_AT01_invalid_credentials_rejected_without_returning_session` is the worst case: its `identity_provider` is a plain `MagicMock` (a success-shaped result, identical to the valid-credentials test) and it never asserts the `CallSpy` store saw no `create`. It cannot prove invalid credentials are rejected.
- **TI-3: `test_AT01_unauthorized_patient_access_returns_false`** configures `policy.is_allowed`, but the `AuthorizationPolicy` protocol defines `can_access_patient`. It passes only if the implementation treats any non-`True` return as denied.
- **TI-4: Idle timeout is untested for real.** `test_AT01_inactive_session_is_rejected` passes via an unknown session (`CallSpy.get` returns `None`). No test checks elapsed time against `T`, either side of it.
- **TI-5: Summary, search and source tests cannot be satisfied legitimately.** They tell authorized from unauthorized from missing only by ID strings (`patient-100` vs `patient-not-authorized`, `summary-100` vs `missing-summary`) with no injected collaborators, so passing them needs hardcoded IDs or hidden defaults. (Deferred slices.)
- **TI-6: `test_AT06_traceability_returns_source_descriptor`** is identical to `test_AT04_source_resolution_returns_source_mapping` and does not check the timestamp or context that AC-006 scenario 2 requires.
- **TI-7: AC-007 is only tested in isolation.** `test_AT07_record_summary_generation_audit_event` calls `record_audit_event` directly; nothing ties summary generation to an audit record.


## Next Action

Slice 1: make `test_AT01_valid_credentials_return_authenticated_session_mapping` pass first (after answering DQ-3, DQ-4 and DQ-6).
