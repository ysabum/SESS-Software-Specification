# SESS Implementation Plan
## Baseline

`tests/test_sess_contracts.py`: **27 tests, 23 failing, 4 passing** (original skeleton).


### Test Output (from the original skeleton baseline)

```
=============================================== short test summary info ================================================
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


### Test Output (after Slice 1)

```
=============================================== short test summary info ================================================
FAILED tests/test_sess_contracts.py::test_AT01_invalid_credentials_rejected_without_returning_session - Failed: DID NOT RAISE Exception
FAILED tests/test_sess_contracts.py::test_AT01_unauthorized_patient_access_returns_false - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT01_inactive_session_is_rejected - assert not True
FAILED tests/test_sess_contracts.py::test_AT02_generate_summary_for_each_supported_detail_level[Brief] - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT02_generate_summary_for_each_supported_detail_level[Standard] - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT02_generate_summary_for_each_supported_detail_level[Detailed] - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT02_unsupported_detail_level_is_rejected - assert not True
FAILED tests/test_sess_contracts.py::test_AT02_unauthorized_patient_summary_is_rejected - assert not True
FAILED tests/test_sess_contracts.py::test_AT03_search_returns_matching_patient_records - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT03_invalid_search_criteria_are_rejected - assert not True
FAILED tests/test_sess_contracts.py::test_AT03_unauthorized_patient_search_is_rejected - assert not True
FAILED tests/test_sess_contracts.py::test_AT04_source_resolution_returns_source_mapping - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT04_unauthorized_source_access_is_rejected - assert not True
FAILED tests/test_sess_contracts.py::test_AT04_missing_source_item_is_rejected - assert not True
FAILED tests/test_sess_contracts.py::test_AT05_organize_available_patient_records_returns_mapping - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT06_traceability_returns_source_descriptor - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT07_record_summary_generation_audit_event - NotImplementedError
FAILED tests/test_sess_contracts.py::test_AT03_api_records_rejects_unauthenticated_request - assert 501 == 401
FAILED tests/test_sess_contracts.py::test_AT02_api_summary_rejects_unauthenticated_request_without_summary - assert 501 == 401
FAILED tests/test_sess_contracts.py::test_AT04_api_source_rejects_unauthenticated_request_without_disclosure - assert 501 == 401
FAILED tests/test_sess_contracts.py::test_skeleton_routes_report_documented_501_error_shape[post-/api/authentication/sessions-payload0] - assert 201 == 501
============================================= 21 failed, 6 passed in 1.92s =============================================
```

### Current State (after implementing Slice 1 + 2)

```
=============================================== short test summary info ================================================
FAILED test_sess_contracts.py::test_AT01_unauthorized_patient_access_returns_false - NotImplementedError
FAILED test_sess_contracts.py::test_AT02_generate_summary_for_each_supported_detail_level[Brief] - NotImplementedError
FAILED test_sess_contracts.py::test_AT02_generate_summary_for_each_supported_detail_level[Standard] - NotImplementedError
FAILED test_sess_contracts.py::test_AT02_generate_summary_for_each_supported_detail_level[Detailed] - NotImplementedError
FAILED test_sess_contracts.py::test_AT02_unsupported_detail_level_is_rejected - assert not True
FAILED test_sess_contracts.py::test_AT02_unauthorized_patient_summary_is_rejected - assert not True
FAILED test_sess_contracts.py::test_AT03_search_returns_matching_patient_records - NotImplementedError
FAILED test_sess_contracts.py::test_AT03_invalid_search_criteria_are_rejected - assert not True
FAILED test_sess_contracts.py::test_AT03_unauthorized_patient_search_is_rejected - assert not True
FAILED test_sess_contracts.py::test_AT04_source_resolution_returns_source_mapping - NotImplementedError
FAILED test_sess_contracts.py::test_AT04_unauthorized_source_access_is_rejected - assert not True
FAILED test_sess_contracts.py::test_AT04_missing_source_item_is_rejected - assert not True
FAILED test_sess_contracts.py::test_AT05_organize_available_patient_records_returns_mapping - NotImplementedError
FAILED test_sess_contracts.py::test_AT06_traceability_returns_source_descriptor - NotImplementedError
FAILED test_sess_contracts.py::test_AT07_record_summary_generation_audit_event - NotImplementedError
FAILED test_sess_contracts.py::test_skeleton_routes_report_documented_501_error_shape[post-/api/authentication/sessions-payload0] - assert 201 == 501
FAILED test_sess_contracts.py::test_skeleton_routes_report_documented_501_error_shape[get-/api/patients/patient-100/records-None] - assert 401 == 501
FAILED test_sess_contracts.py::test_skeleton_routes_report_documented_501_error_shape[post-/api/patients/patient-100/summaries-payload2] - assert 401 == 501
FAILED test_sess_contracts.py::test_skeleton_routes_report_documented_501_error_shape[get-/api/summaries/summary-100/items/item-100/source-None] - assert 401 == 501
============================================= 19 failed, 8 passed in 1.86s =============================================
```

| Group | Count | State |
|---|---|---|
| Slice 1 tests (2 module, 2 API) | 4 | green |
| Slice 2 tests (1 module, 3 API) | 4 | green |
| Remaining AC tests (Slices 3, 4, 8, 9, 13) | 15 | red (`NotImplementedError` / 501) |
| Placeholder `test_skeleton_routes_report_documented_501_error_shape` (4) | 4 | red **by design** (TI-1): sessions now returns 201; records, summaries and source now return 401 when unauthenticated |

Failing tests grouped by acceptance criterion (by the test's `ATnn` prefix), as of the original baseline. Items marked **(now green)** were completed by Slices 1-2:

| AC | Tests | Cause today |
|---|---|---|
| AC-001 (6) | `test_AT01_valid_credentials_return_authenticated_session_mapping` **(now green)**, `test_AT01_invalid_credentials_rejected_without_returning_session` **(now green)**, `test_AT01_unauthorized_patient_access_returns_false`, `test_AT01_inactive_session_is_rejected` **(now green)**, `test_AT01_api_valid_login_returns_201_and_session_data` **(now green)**, `test_AT01_api_invalid_login_returns_401_without_session_data` **(now green)** | Only the unauthorized-patient test remains red: `NotImplementedError` |
| AC-002 (6) | `test_AT02_generate_summary_for_each_supported_detail_level[Brief]`, `[Standard]`, `[Detailed]`, `test_AT02_unsupported_detail_level_is_rejected`, `test_AT02_unauthorized_patient_summary_is_rejected`, `test_AT02_api_summary_rejects_unauthenticated_request_without_summary` **(now green)** | `NotImplementedError` |
| AC-003 (4) | `test_AT03_search_returns_matching_patient_records`, `test_AT03_invalid_search_criteria_are_rejected`, `test_AT03_unauthorized_patient_search_is_rejected`, `test_AT03_api_records_rejects_unauthenticated_request` **(now green)** | `NotImplementedError` |
| AC-004 (4) | `test_AT04_source_resolution_returns_source_mapping`, `test_AT04_unauthorized_source_access_is_rejected`, `test_AT04_missing_source_item_is_rejected`, `test_AT04_api_source_rejects_unauthenticated_request_without_disclosure` **(now green)** | `NotImplementedError` |
| AC-005 (1) | `test_AT05_organize_available_patient_records_returns_mapping` | `NotImplementedError` |
| AC-006 (1) | `test_AT06_traceability_returns_source_descriptor` | `NotImplementedError` |
| AC-007 (1) | `test_AT07_record_summary_generation_audit_event` | `NotImplementedError` |

Eight "rejection" tests only assert that the exception is *not* `NotImplementedError` (see TI-2).

---


## Slice Scope

The plan has **21 slices**. Slices 1-2 are **implemented**. Slices 3-4 are the next candidates. **Slices 5-21 are planning-only: they exist to show that the whole of `spec.md`, `architecture.md`, `contracts.md` and `test_plan.md` is covered, and they will not be built for this project**. Their status is therefore "not started (planned only)".

**Order:** authentication (leaf) → session validity and gating → patient authorization and audit primitive (leaves) → record organization → EHR retrieval → timestamps → records endpoint → search/filter → summary generation → audit wiring → data-quality flags → retrieval consistency → source resolution → remaining audit work → historical summaries → browser UI → performance, availability and PHI-protection verification.

Where the existing suite has no test for a slice, the "Tests" line says so and lists **proposed** test names (marked *proposed*, not in the suite). Proposed names are suggestions; no test in `tests/` was changed.

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
- **Skeleton to fill in (as implemented):** `identity_and_access.authenticate_user`; route `POST /api/authentication/sessions` (`create_session` in `web_interface.py`); development collaborators `InMemoryIdentityProvider` and `InMemorySessionStore`, wired onto `app.state` in `main.py`.
- **Depends on:** none. (DQ-1 [auth collaborators], DQ-3, DQ-4 and DQ-6 are now answered; see Deviations.)
- **Done when:** the listed tests pass and no previously passing test fails. Expected exception (TI-1): `test_skeleton_routes_report_documented_501_error_shape[post-/api/authentication/sessions-payload0]` goes red by design.
- **Status:** DONE (with deviations D1-D8, D10-D12 below)


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
- **Skeleton to fill in (as implemented):** `identity_and_access.validate_session`; the `_require_session` helper in `web_interface.py`, called first in each of `GET /api/patients/{patient_id}/records`, `POST /api/patients/{patient_id}/summaries` and `GET /api/summaries/{summary_id}/items/{item_id}/source`. The authenticated branch of each still returns 501.
- **Depends on:** Slice 1 (sessions must exist to be validated).
- **Done when:** the listed tests pass and no previously passing test fails. Expected exceptions (TI-1): the skeleton 501 tests for the records, summaries and source routes go red by design. Exactly-`T` behavior is now fixed by the implementation (see D6) but remains unasserted by any test (EX-003).
- **Status:** DONE (with deviations D2, D4, D5, D6, D9, D12, D13 below)


## Slice 3: Patient Authorization and Audit Primitive

- **Name:** Patient authorization and audit primitive
- **Goal:** Patient access is granted only when the injected policy returns literal `True` (anything else, including errors, is denied), and an audit event can be appended with user, action, patient/record reference and timestamp.
- **Spec sources:** FR-001; NFR-001; NFR-008; spec AC-001 scenario 3, AC-007; architecture §2 Audit Recording, §3 steps 3 and 10; contracts §1 `authorize_patient_access`, `record_audit_event`; test_plan AC-001 case C, AC-007 case A, EX-005.
- **Criteria:** Completes AC-001 (scenario 3, the last open one). Advances AC-007 at function level only: the scenario "when a patient summary is generated" cannot complete until summary generation calls `record_audit_event` (Slice 10).
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
- **Criteria:** Completes AC-005 at function level (end to end in Slice 7).
- **Tests that should turn green:**
  - `test_AT05_organize_available_patient_records_returns_mapping`
- **Skeleton to fill in:** `patient_records.organize_patient_records`.
- **Depends on:** none. This is a pure function, so it is independent of Slices 1-3. Later search and summary slices depend on it.
- **Done when:** the listed test passes and no previously passing test fails. Blocked on DQ-5 (record shape).
- **Status:** not started

---

## Slices 5-21 (planned only, not to be built)
## Slice 5: EHR Connector Retrieval

- **Name:** EHR retrieval with source preservation
- **Goal:** `retrieve_patient_records` returns a record batch that keeps source identifiers, original timestamps and context, stamps the retrieval time, reports per-category availability and uninterpretable records, and surfaces EHR/network errors instead of returning old data as current.
- **Spec sources:** FR-002, FR-005; NFR-006, NFR-007; spec AC-002 scenario 2; architecture §2 EHR Connector, §3 steps 6-7, §4 (EHR is authoritative, read-only); contracts §1 `retrieve_patient_records`; test_plan AC-005 case C, AC-006 cases C-D, EX-011, EX-012.
- **Criteria:** Advances AC-002 (scenario 2, retrieval half), AC-005 (case C), AC-006 (cases C-D).
- **Tests that should turn green:** none in the current suite (TI-8). *Proposed:* `test_EHR_retrieval_preserves_source_ids_and_timestamps`, `test_EHR_retrieval_reports_unavailable_category`, `test_EHR_retrieval_surfaces_ehr_error`, `test_EHR_retrieval_reports_uninterpretable_record`.
- **Skeleton to fill in:** `ehr_connector.retrieve_patient_records`; a fake `EHRClient` for tests and the demo (no real EHR is selected, contracts §4).
- **Depends on:** none (leaf module).
- **Done when:** the proposed tests pass and no previously passing test fails. Read-only: no call writes to the EHR.
- **Status:** not started (planned only)


## Slice 6: Timestamp Preservation and Configured-Timezone Display

- **Name:** Source timestamps and display timezone
- **Goal:** Every imported timestamp keeps its original source value and also carries a display value in the organization's configured timezone, with no fabricated or overwritten timestamps.
- **Spec sources:** NFR-007 (timestamps); spec AC-006 scenario 2; architecture §4 (preserve source timestamps); test_plan AC-006 case C, EX-004.
- **Criteria:** Advances AC-006 (case C).
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_timestamp_retains_original_and_displays_in_configured_timezone`, `test_timestamp_across_date_boundary_and_dst`, `test_ordinary_timestamp_control_is_unchanged`.
- **Skeleton to fill in:** a timestamp-conversion helper used by `patient_records.organize_patient_records` and `source_traceability.resolve_summary_item_source`. No contract function owns this (DQ-8).
- **Depends on:** Slice 5.
- **Done when:** the proposed tests pass and no previously passing test fails. Do not assert timestamp format or DST handling the spec does not define.
- **Status:** not started (planned only)


## Slice 7: Categorized Records Endpoint

- **Name:** Categorized records endpoint
- **Goal:** The authenticated branch of `GET /api/patients/{patient_id}/records` returns the patient's records in the eleven categories with source identifiers, timestamps and per-category availability, and denies unauthorized patients with 403.
- **Spec sources:** FR-001 (authorization), FR-005; NFR-001, NFR-002, NFR-006, NFR-007; spec AC-001 scenario 3, AC-005; architecture §3 steps 3, 6-7; contracts §2 `GET /api/patients/{patient_id}/records`; test_plan AC-005 cases A-B, EX-005, EX-011, EX-012.
- **Criteria:** Completes AC-005 end to end; advances AC-001 (scenario 3) at route level.
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_AT05_api_records_returns_eleven_categories`, `test_AT01_api_records_unauthorized_patient_returns_403`, `test_AT05_api_records_identifies_unavailable_category`, `test_EX011_api_records_ehr_unavailable_returns_503`.
- **Skeleton to fill in:** the authenticated branch of `get_patient_records`; `_require_session` must be changed to return the validated session so the route knows `user_id` (it currently returns only an error or `None`, see D13); collaborator wiring for the EHR client, authorization policy and clock on `app.state` (DQ-1).
- **Depends on:** Slices 3, 4, 5.
- **Done when:** the proposed tests pass, and the 401 tests from Slice 2 stay green.
- **Status:** not started (planned only)


## Slice 8: Patient-Scoped Search and Filter

- **Name:** Search and filter
- **Goal:** A search term plus date, record type, diagnosis, medication, provider, procedure and laboratory-test filters return matching records for the selected patient only; invalid criteria are rejected (422) and unauthorized patients are denied.
- **Spec sources:** FR-003; NFR-001, NFR-004, NFR-005; spec AC-003; architecture §2 Patient Records, §3 step 6; contracts §1 `search_patient_records`, §2 `GET /api/patients/{patient_id}/records` (query parameters); test_plan AC-003 cases A-C, EX-009, EX-012.
- **Criteria:** Completes AC-003.
- **Tests that should turn green:**
  - `test_AT03_search_returns_matching_patient_records`
  - `test_AT03_invalid_search_criteria_are_rejected`
  - `test_AT03_unauthorized_patient_search_is_rejected`
- **Skeleton to fill in:** `patient_records.search_patient_records`; the query-parameter handling of `get_patient_records` (`q`, `date_from`, `date_to`, `record_type`, `diagnosis`, `medication`, `provider`, `procedure`, `laboratory_test`).
- **Depends on:** Slice 7. Blocked on DQ-1 and TI-5 (the tests tell authorized from unauthorized patients only by ID strings).
- **Done when:** the listed tests pass and no previously passing test fails. A rejected search creates no result object (EX-009).
- **Status:** not started (planned only)


## Slice 9: Summary Generation With Source Associations

- **Name:** Summary generation (Brief / Standard / Detailed)
- **Goal:** `POST /api/patients/{patient_id}/summaries` returns a structured summary at the chosen level in which every clinical item carries a source association; unsupported levels (422) and unauthorized patients (403) are rejected.
- **Spec sources:** FR-002, FR-006; NFR-002, NFR-003, NFR-004; spec AC-002 scenario 1; architecture §2 Summary Generation, §3 steps 4-5, 8-9, 11; contracts §1 `generate_patient_summary`, §2 `POST /api/patients/{patient_id}/summaries`; test_plan AC-002 case A, AC-006 case A, EX-009.
- **Criteria:** Completes AC-002 scenario 1; advances AC-006 (the association half of case A).
- **Tests that should turn green:**
  - `test_AT02_generate_summary_for_each_supported_detail_level[Brief]`
  - `test_AT02_generate_summary_for_each_supported_detail_level[Standard]`
  - `test_AT02_generate_summary_for_each_supported_detail_level[Detailed]`
  - `test_AT02_unsupported_detail_level_is_rejected`
  - `test_AT02_unauthorized_patient_summary_is_rejected`
- **Skeleton to fill in:** `summary_generation.generate_patient_summary` (any algorithm that satisfies NFR-002; a rule-based one is enough); a source-association helper owned by Source Traceability; a summary store; the authenticated branch of `create_patient_summary`.
- **Depends on:** Slices 3, 4, 5, 7. Blocked on DQ-1, DQ-9 and TI-5.
- **Done when:** the listed tests pass and no previously passing test fails. The three levels present the same information at different completeness.
- **Status:** not started (planned only)


## Slice 10: Audit Wiring for Record Access and Summary Generation

- **Name:** Audit patient-record access and summary generation
- **Goal:** Patient-record access and summary generation append audit events (user, action, patient reference, timestamp), and an audit-store failure fails the calling workflow.
- **Spec sources:** NFR-008; spec AC-007; architecture §2 Audit Recording, §3 step 10; contracts §1 `record_audit_event`, §3 (NFR-008 row); test_plan AC-007 cases A-B.
- **Criteria:** Completes the spec AC-007 scenario (summary generation). Advances AC-007 case B (patient-record access).
- **Tests that should turn green:** none new. `test_AT07_record_summary_generation_audit_event` (Slice 3) is function-level only (TI-7). *Proposed:* `test_AT07_summary_generation_creates_audit_event`, `test_AT07_record_access_creates_audit_event`, `test_AT07_audit_store_failure_fails_the_request`.
- **Skeleton to fill in:** calls to `record_audit_event` from `get_patient_records` and `create_patient_summary` (or the module functions they call); an audit store on `app.state` (DQ-1, DQ-7).
- **Depends on:** Slices 3, 7, 9.
- **Done when:** the proposed tests pass and no previously passing test fails.
- **Status:** not started (planned only)


## Slice 11: Data-Quality Flags: Partial, Conflicting, Incomplete, Stale

- **Name:** Summary data-quality flags
- **Goal:** Summaries and records identify unavailable categories, incomplete or conflicting items and stale information (with its original retrieval timestamp) instead of presenting them as confirmed current fact.
- **Spec sources:** FR-002; NFR-002, NFR-006, NFR-007; spec AC-002 scenarios 2-3; architecture §3 step 7, §5 (freshness threshold undefined); contracts §1 `generate_patient_summary` (failure/success text), §2 summaries route; test_plan AC-002 cases B-D, EX-011, EX-013.
- **Criteria:** Completes AC-002 (scenarios 2-3).
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_AT02_partial_summary_identifies_unavailable_category`, `test_AT02_stale_summary_shows_retrieval_timestamp`, `test_AT02_fresh_retrieval_is_not_marked_stale`, `test_EX013_conflicting_source_item_is_flagged_and_linked`.
- **Skeleton to fill in:** flagging logic in `summary_generation.generate_patient_summary` and `patient_records.organize_patient_records`; a place to keep previously retrieved data (DQ-10).
- **Depends on:** Slices 5, 9. Blocked on DQ-10: contracts §4 says there is no cache or retention.
- **Done when:** the proposed tests pass and no previously passing test fails. Stale data is never labeled current.
- **Status:** not started (planned only)


## Slice 12: Single-Request Retrieval Consistency

- **Name:** Retrieval consistency and regeneration
- **Goal:** If records change during a summary request so that no consistent summary can be produced, the user is told (503) to regenerate and no inconsistent summary is stored or shown as current.
- **Spec sources:** NFR-007 (single retrieval); spec Spec Issue 2; architecture §3 step 7, Spec Issues 2; contracts §1 `generate_patient_summary` (failure), §2 summaries route (`503` inconsistent retrieval); test_plan AC-002 case E, EX-008.
- **Criteria:** Completes AC-002 case E (test_plan only; no spec scenario).
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_AT02_inconsistent_retrieval_requires_regeneration`, `test_AT02_consistent_retrieval_generates_summary`.
- **Skeleton to fill in:** consistency check across the retrieval in `ehr_connector.retrieve_patient_records` and its use in `generate_patient_summary`.
- **Depends on:** Slices 5, 9. Blocked on DQ-11 (detection method is unspecified).
- **Done when:** the proposed tests pass and no previously passing test fails.
- **Status:** not started (planned only)


## Slice 13: Source Resolution and Traceability

- **Name:** Source resolution
- **Goal:** `GET /api/summaries/{summary_id}/items/{item_id}/source` re-checks authorization, then returns the originating source record (or EHR launch reference), its original timestamp and available section/data-element context, and records the source view; unauthorized access (403) and missing items (404) disclose nothing.
- **Spec sources:** FR-004, FR-006; NFR-001, NFR-003, NFR-007; spec AC-004, AC-006; architecture §2 Source Traceability, §3 step 12; contracts §1 `resolve_summary_item_source`, §2 source route; test_plan AC-004 cases A-B, AC-006 cases A-D.
- **Criteria:** Completes AC-004 and AC-006.
- **Tests that should turn green:**
  - `test_AT04_source_resolution_returns_source_mapping`
  - `test_AT04_unauthorized_source_access_is_rejected`
  - `test_AT04_missing_source_item_is_rejected`
  - `test_AT06_traceability_returns_source_descriptor`
- **Skeleton to fill in:** `source_traceability.resolve_summary_item_source`; the authenticated branch of `get_summary_item_source`; an audit event for source viewing.
- **Depends on:** Slices 3, 6, 9, 10. Blocked on DQ-1, DQ-9 and TI-5. TI-6: `test_AT06_traceability_returns_source_descriptor` does not check the timestamp or context; add assertions when this slice is built.
- **Done when:** the listed tests pass and no previously passing test fails. A failed or missing link never produces a fabricated source, timestamp or context.
- **Status:** not started (planned only)


## Slice 14: Authentication-Event and Authorization-Failure Auditing

- **Name:** Audit authentication and authorization failures
- **Goal:** Successful and failed logins, failed patient authorization and failed source-access attempts are each audited with user, action, patient/record reference and timestamp.
- **Spec sources:** NFR-008; spec AC-007; architecture §2 Audit Recording; contracts §3 (NFR-008 row); test_plan AC-001 cases A-C ("record authentication event"), AC-004 case B, AC-007 case B, EX-005, EX-010.
- **Criteria:** Advances AC-007 (case B).
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_AT07_login_success_is_audited`, `test_AT07_login_failure_is_audited`, `test_AT07_failed_patient_authorization_is_audited`, `test_AT07_failed_source_authorization_is_audited`.
- **Skeleton to fill in:** audit calls from `create_session` and the 403 branches in the routes (the Identity and Access functions take no `audit_store`; DQ-7).
- **Depends on:** Slices 3, 10, 13.
- **Done when:** the proposed tests pass and no previously passing test fails. A rejected request discloses no protected data; the audit event is the permitted side effect.
- **Status:** not started (planned only)


## Slice 15: Audit Access Control and Integrity

- **Name:** Audit access control and immutability
- **Goal:** Audit records can be read only by appropriately authorized personnel, every audit access (allowed or denied) is itself audited, and no ordinary application operation can modify or delete an existing audit record.
- **Spec sources:** NFR-008; spec AC-007; architecture §2 Audit Recording; contracts §1 `record_audit_event` ("cannot be altered"), §3 (no audit-browsing route); test_plan AC-007 cases B-D, EX-015.
- **Criteria:** Completes AC-007 (cases C-D).
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_AT07_unauthorized_audit_access_denied_and_audited`, `test_AT07_authorized_audit_access_allowed_and_audited`, `test_AT07_audit_record_cannot_be_modified`.
- **Skeleton to fill in:** an audit-read operation and append-only store. Neither exists in contracts (contracts §3 deliberately adds no audit route), so this needs a contract amendment first (DQ-12).
- **Depends on:** Slices 3, 10.
- **Done when:** the proposed tests pass and no previously passing test fails.
- **Status:** not started (planned only)


## Slice 16: Permission-Change Auditing

- **Name:** Audit permission changes
- **Goal:** A change to a user's role or patient-access permissions is audited, and later patient/source access follows the configured policy without asserting a revocation latency.
- **Spec sources:** NFR-001, NFR-008; spec AC-007; architecture §4 (configurable roles), §5 (no permission-administration function); contracts §3, §4; test_plan AC-007 case B, EX-005, EX-006.
- **Criteria:** Advances AC-007 (case B, permission changes).
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_AT07_permission_change_is_audited`, `test_EX006_unchanged_user_is_unaffected`, `test_EX005_authorized_employee_uses_same_login_flow`.
- **Skeleton to fill in:** an audit call at whichever configuration path changes permissions. No such function exists (DQ-12).
- **Depends on:** Slices 3, 10, 14.
- **Done when:** the proposed tests pass and no previously passing test fails.
- **Status:** not started (planned only)


## Slice 17: Historical Summary Labeling

- **Name:** Historical summaries
- **Goal:** A retained earlier summary is clearly labeled historical and is never presented as the current summary; viewing it creates no new current summary.
- **Spec sources:** NFR-006 (retention); architecture §5 (retention, version history and caching undefined); contracts §4 (no historical-summary API); test_plan EX-007.
- **Criteria:** none of AC-001 to AC-007 (covers a test_plan extra case).
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_EX007_historical_summary_is_labeled_historical`, `test_EX007_viewing_history_creates_no_current_summary`.
- **Skeleton to fill in:** a `status: historical` marker in the summary store and display path. **Conditional:** needs an organization retention decision and a contract amendment first (contracts §4 excludes it).
- **Depends on:** Slices 9, 11.
- **Done when:** the proposed tests pass and no previously passing test fails.
- **Status:** not started (planned only, conditional)


## Slice 18: Browser User Interface

- **Name:** Browser UI screens
- **Goal:** HTML/CSS/JS screens served by the same FastAPI application let a trained user sign in, pick an authorized patient, generate a summary at a chosen level, search/filter records and open a summary item's source, with authentication and authorization errors shown and summary content visibly separate from source content.
- **Spec sources:** FR-001 to FR-004; NFR-005; spec AC-001 ("Sign In button", error displayed), AC-002 to AC-004; architecture §2 Web Interface, §3 steps 1-4 and 11-12, §4 (browser-based interface); test_plan AC-003 NFR-005 note, EX-009.
- **Criteria:** Presents AC-001 to AC-004 to the user; no new criterion.
- **Tests that should turn green:** none in the current suite (the suite tests only the JSON API). *Proposed:* browser-level checks such as `test_UI_login_screen_shows_authentication_error`, `test_UI_summary_distinguishes_summary_from_source_content`, `test_UI_expired_session_returns_to_login`.
- **Skeleton to fill in:** static pages or templates and their serving route. Today `GET /` returns only `{"application":"SESS","status":"skeleton"}` and the only page is the FastAPI-generated `/docs`; the health check would move to `/health`.
- **Depends on:** Slices 8, 9, 13.
- **Done when:** the proposed checks pass and no previously passing test fails.
- **Status:** not started (planned only)


## Slice 19: Performance Validation

- **Name:** Performance validation
- **Goal:** A repeatable workload run shows searches finishing within 3 seconds and summaries within 10 seconds for at least 95% of requests, measured from request submission to results displayed.
- **Spec sources:** NFR-004; architecture §4 (response-time targets via testing); test_plan AC-003 performance boundary, EX-001.
- **Criteria:** none of AC-001 to AC-007 (NFR-004 has no acceptance criterion; test_plan §4.1).
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_NFR004_search_p95_within_3_seconds`, `test_NFR004_summary_p95_within_10_seconds`, `test_NFR004_retry_creates_no_duplicate_summary`.
- **Skeleton to fill in:** a benchmark script and representative dataset; no module function. The organization must supply the dataset and workload.
- **Depends on:** Slices 8, 9.
- **Done when:** the proposed tests pass and no previously passing test fails.
- **Status:** not started (planned only)


## Slice 20: Availability and Maintenance Notices

- **Name:** Availability reporting and maintenance notice
- **Goal:** SESS can report availability over a calendar month against the 99.5% target (excluding scheduled maintenance), and shows planned-maintenance notices before maintenance begins.
- **Spec sources:** NFR-006; architecture §4; test_plan EX-002, EX-016, EX-011 (outage messaging).
- **Criteria:** none of AC-001 to AC-007.
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_NFR006_availability_calculation_excludes_scheduled_maintenance`, `test_NFR006_maintenance_notice_precedes_maintenance`, `test_NFR006_no_notice_when_no_maintenance`.
- **Skeleton to fill in:** an uptime log, a maintenance-window setting and a notice shown by the Web Interface. Notice period and channel are unspecified (test_plan §4.3).
- **Depends on:** Slice 18.
- **Done when:** the proposed tests pass and no previously passing test fails.
- **Status:** not started (planned only)


## Slice 21: PHI Protection in Transit and Storage

- **Name:** PHI protection
- **Goal:** PHI is protected during transmission and storage, no credentials or PHI appear in logs or error bodies, and unauthorized copies of PHI are not created.
- **Spec sources:** NFR-001; architecture §4 (security decision), §5 (backup, DR, tenancy undefined); test_plan EX-014.
- **Criteria:** none of AC-001 to AC-007.
- **Tests that should turn green:** none in the current suite. *Proposed:* `test_NFR001_credentials_never_appear_in_responses_or_logs`, `test_NFR001_phi_not_written_to_logs`. Transport and storage encryption need a deployment-level check, since the spec names no protocols.
- **Skeleton to fill in:** deployment configuration (TLS termination, encrypted summary and audit storage) and log filtering; no module function.
- **Depends on:** none in code; best checked after Slices 9 and 15.
- **Done when:** the proposed checks pass and no previously passing test fails.
- **Status:** not started (planned only)

---


## Coverage Map

Every functional requirement, nonfunctional requirement, acceptance criterion and extra test case is assigned to at least one slice.

| Item | Slices |
|---|---|
| FR-001 | 1, 2, 3, 7 |
| FR-002 | 5, 9, 11 |
| FR-003 | 8 |
| FR-004 | 13 |
| FR-005 | 4, 5, 7 |
| FR-006 | 9, 13 |
| NFR-001 | 1, 2, 3, 7, 16, 21 |
| NFR-002 | 4, 7, 9, 11 |
| NFR-003 | 9, 13 |
| NFR-004 | 8, 9, 19 |
| NFR-005 | 8, 18 |
| NFR-006 | 5, 11, 17, 20 |
| NFR-007 | 4, 5, 6, 12, 13 |
| NFR-008 | 3, 10, 13, 14, 15, 16 |
| AC-001 | 1, 2, 3 |
| AC-002 | 9, 11, 12 (retrieval half in 5) |
| AC-003 | 8 |
| AC-004 | 13 |
| AC-005 | 4, 7 |
| AC-006 | 5, 6, 9, 13 |
| AC-007 | 3, 10, 14, 15, 16 |
| EX-001 | 19 |
| EX-002 | 20 |
| EX-003 | 2 |
| EX-004 | 6 |
| EX-005 | 3, 7, 16 |
| EX-006 | 16 |
| EX-007 | 17 |
| EX-008 | 12 |
| EX-009 | 8, 9, 18 |
| EX-010 | 2, 14 |
| EX-011 | 5, 7, 11, 20 |
| EX-012 | 4, 5, 7, 8 |
| EX-013 | 11 |
| EX-014 | 21 |
| EX-015 | 15 |
| EX-016 | 20 |

All 15 still-failing tests in the suite are assigned: Slice 3 (2), Slice 4 (1), Slice 8 (3), Slice 9 (5), Slice 13 (4). The four placeholder 501 tests are retired by design (TI-1).

---


## Deviations From the Original Plan (as implemented in Slices 1-2)

These differences are visible in `app/main.py`, `app/web_interface.py` and `app/identity_and_access.py`. The slices above were updated to match.

| # | Original plan or contract | Implemented | Where |
|---|---|---|---|
| D1 | `SessionStore` offered `create`, `get`, `end` (DQ-6) | An `update` method was added to the protocol, so last-activity is refreshed in place rather than end-then-create | `identity_and_access.py`, `InMemorySessionStore.update` in `main.py` |
| D2 | Rejection signal unspecified (DQ-3) | Rejected credentials and unknown/expired sessions raise built-in `PermissionError`; any other exception is a provider/service failure and is surfaced unchanged | `authenticate_user`, `validate_session`, `InMemoryIdentityProvider` |
| D3 | `clock: Any` left open (DQ-4) | `clock` is a `datetime` value, taken fresh per request with `datetime.now(timezone.utc)` | route code in `web_interface.py` |
| D4 | Session transport unspecified (DQ-2) | `Authorization: Bearer <session_id>` header; a missing, non-Bearer or empty token gives 401 with `WWW-Authenticate: Bearer` | `_require_session` |
| D5 | Collaborator wiring unspecified (DQ-1) | The identity provider, session store and `inactivity_timeout_seconds` (default 900) are set on `app.state` in `main.py`. This answers DQ-1 for authentication only; the EHR client, authorization policy, summary store and audit store are still unwired | `main.py` |
| D6 | Behavior at exactly `T` "unspecified, do not assert" | Implemented as **valid**: a session is rejected only when idle time is strictly greater than the timeout. Documented in the docstring, but no test covers it | `validate_session` |
| D7 | Session record keys unspecified (DQ-6) | Keys are `session_id`, `user_id`, `permissions`, `created_at`, `last_activity_at` (datetimes) | `authenticate_user` |
| D8 | Contracts §1 says `authenticate_user` creates a session | It also raises `RuntimeError` if `session_store.create` returns `None`, which the route reports as 503 | `authenticate_user` |
| D9 | Contracts §2 lists 401 and 503 (provider) only | Session-service failures during validation return 503 `session_service_unavailable` | `_require_session` |
| D10 | Contracts §2: invalid credentials give 401; malformed input unspecified | A body that is not JSON, not an object, or lacks string `username`/`password` returns 401 `authentication_failed`, not 422 | `create_session` |
| D11 | Contracts §2 201 body: session ID, identity, role/permissions, "expiry/activity metadata" | 201 returns `session_id`, `user_id`, `permissions`, `created_at`, `last_activity_at`; there is no `role` and no expiry timestamp. Any non-`PermissionError` failure is reported as 503 `identity_provider_unavailable`, including a session-store failure | `create_session` |
| D12 | The development identity provider was not specified | In-memory PBKDF2 stand-in (200,000 iterations, constant-cost check for unknown users). The only account is `clinician` / `valid-password` with an empty permission list because the role matrix is undefined | `main.py` |
| D13 | Slice 2 gated the three routes | `_require_session` returns only an error response or `None`; it discards the validated session. Slices 3-13 need the session's `user_id`, so it must change to return the session | `web_interface.py` |

Other observations, not deviations: the README still says every route returns 501, which is no longer true for `POST /api/authentication/sessions` and for unauthenticated calls to the other three routes. `GET /` still returns `{"application":"SESS","status":"skeleton"}`.

---


## Design Questions

- **DQ-1: Collaborator wiring.** *Partly answered (D5).* Authentication collaborators live on `app.state`, set in `main.py`. Still open: where do the EHR client, authorization policy, summary store and audit store come from, and how do `generate_patient_summary`, `search_patient_records` and `resolve_summary_item_source` (which take no collaborators) reach them?
- **DQ-2: Session transport.** *Answered (D4):* `Authorization: Bearer <session_id>`.
- **DQ-3: Rejection signalling.** *Answered (D2):* built-in `PermissionError` for rejection; other exceptions are provider failures.
- **DQ-4: `clock: Any`.** *Answered (D3):* a `datetime` value.
- **DQ-5: Source-record shape.** *Open.* The test's record has only `source_id` and `source_value`; no field says which category it belongs to. Which key determines category, and what is the result key for uninterpretable items?
- **DQ-6: Session record shape and activity updates.** *Answered (D1, D7).*
- **DQ-7: Who calls Audit Recording.** *Open.* `authenticate_user` and `authorize_patient_access` take no `audit_store`, and architecture §2 lists no module as depending on Audit Recording. The login route currently records no authentication event. Slices 10 and 14 assume the routes or workflow modules make the calls.
- **DQ-8: Configured timezone.** *New, open.* Where does the organization's display timezone come from, and which function converts timestamps (Slice 6)?
- **DQ-9: Summary store and source association.** *New, open.* `resolve_summary_item_source` takes only IDs, so the summary and its item-to-source links must be stored somewhere. Which module owns that store, and who creates the association (Slices 9, 13)?
- **DQ-10: Source of "previously retrieved" data.** *New, open.* Stale-summary display needs retained earlier data, but contracts §4 says there is no cache, replica or retention policy (Slice 11, 17).
- **DQ-11: Consistency detection.** *New, open.* How does SESS tell that records changed during retrieval (Spec Issue 2) (Slice 12)?
- **DQ-12: Audit-read and permission-admin entry points.** *New, open.* Contracts §3 adds no audit-browsing or permission-administration function, yet NFR-008 requires audited audit access and permission changes (Slices 15, 16).


## Test Issues

No test was changed.

- **TI-1: Placeholder 501 tests contradict "no previously passing test fails".** All four are labeled "should pass until the routes are implemented." Slice 1 turned the sessions one red; Slice 2 turned the other three red. This is expected and is not a regression.
- **TI-2: Eight rejection tests are weak.** Each only asserts the exception is not `NotImplementedError`, so any `TypeError` or `AttributeError` passes. `test_AT01_invalid_credentials_rejected_without_returning_session` is the worst case: its `identity_provider` is a plain `MagicMock` (a success-shaped result, identical to the valid-credentials test) and it never asserts the `CallSpy` store saw no `create`. **Observed after Slice 1:** it is green only because `CallSpy.create` returns `None`, which makes `authenticate_user` raise `RuntimeError`, not because invalid credentials were rejected.
- **TI-3: `test_AT01_unauthorized_patient_access_returns_false`** configures `policy.is_allowed`, but the `AuthorizationPolicy` protocol defines `can_access_patient`. It passes only if the implementation treats any non-`True` return as denied.
- **TI-4: Idle timeout is untested for real.** `test_AT01_inactive_session_is_rejected` passes via an unknown session (`CallSpy.get` returns `None`). No test checks elapsed time against `T`, either side of it. The real check in `validate_session` has no test.
- **TI-5: Summary, search and source tests cannot be satisfied legitimately.** They tell authorized from unauthorized from missing only by ID strings (`patient-100` vs `patient-not-authorized`, `summary-100` vs `missing-summary`) with no injected collaborators, so passing them needs hardcoded IDs or hidden defaults (Slices 8, 9, 13).
- **TI-6: `test_AT06_traceability_returns_source_descriptor`** is identical to `test_AT04_source_resolution_returns_source_mapping` and does not check the timestamp or context that AC-006 scenario 2 requires.
- **TI-7: AC-007 is only tested in isolation.** `test_AT07_record_summary_generation_audit_event` calls `record_audit_event` directly; nothing ties summary generation to an audit record.
- **TI-8: `retrieve_patient_records` has no test at all.** *New.* Slices 5, 6, 11 and 12 depend on it and need new tests.