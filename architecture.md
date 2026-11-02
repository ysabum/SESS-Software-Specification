# SESS Architecture
## 1. Overview

The Smart EHR Summarization System (SESS) is a healthcare application that assists authorized healthcare professionals in efficiently reviewing patient electronic health records (EHRs). The system organizes fragmented patient information into a structured format, generates appointment-relevant patient summaries, supports searching and filtering patient records, and provides traceability from generated summaries back to the original source records. The system is designed to reduce the time required to review patient information while maintaining security and privacy for protected health information (PHI).

The proposed design is a single deployable web application with a small set of internally separated modules, a relational data store for SESS-managed information and audit records, and an EHR integration boundary. It does not replace the EHR as the system of record.


## 2. Modules

| Module | Responsibility | May depend on |
|---|---|---|
| Web Interface | Presents authentication, patient selection, summary, search/filter, and source-review screens to users | Identity and Access, Patient Records, Summary Generation, Source Traceability |
| Identity and Access | Authenticates users and enforces role-based authorization for SESS functions and patient access | — |
| EHR Connector | Retrieves patient records from the existing EHR through the organization's agreed interface and preserves source identifiers, timestamps, and context | — |
| Patient Records | Organizes retrieved information into the categories used by SESS and performs patient-scoped search and filtering | Identity and Access, EHR Connector |
| Summary Generation | Produces a structured patient summary at the requested detail level from the available organized patient information | Identity and Access, Patient Records, Source Traceability |
| Source Traceability | Associates each displayed summary item with its originating source record and resolves requests to view that source | Identity and Access, EHR Connector |
| Audit Recording | Records authentication events, patient-record access, summary generation, and permission changes with user, applicable patient/record reference, and timestamp | — |

The modules are logical boundaries within one application, not a requirement to deploy separate services. The table is limited to responsibilities needed by FR-001 through FR-006 and NFR-008. Persistent storage is an implementation facility used by the modules that need to retain SESS-managed data. It is not treated as a separate business module.


## 3. Request Flow
### Generate and verify a patient summary

1. The user opens the SESS web interface and submits authentication credentials.
2. Identity and Access validates the credentials. If authentication fails, the interface displays an authentication error. If it succeeds, the authenticated user receives an authenticated session with permissions determined by their assigned role. This is the flow in AC-001.
3. The user selects a patient. Identity and Access checks that the user is authorized to access that patient's information before patient data is returned.
4. The user selects **Generate Summary** and chooses a detail level.
5. Summary Generation requests the patient's available records from Patient Records.
6. Patient Records obtains the required information through EHR Connector, organizes it into the supported categories, and applies any requested patient-scoped search or filtering criteria.
7. EHR Connector preserves the source record identifiers, timestamps, and relevant context supplied by the EHR. If the EHR or network is unavailable, the request fails visibly rather than silently presenting old information as current.
8. Summary Generation creates the structured summary at the selected detail level using an implementation that satisfies the specification's accuracy and traceability requirements. It does not write clinical changes back to the EHR.
9. Source Traceability associates each clinical item in the summary with its originating record and, where the source provides it, the relevant section or data element.
10. Audit Recording records the patient-record access and summary-generation events.
11. The interface displays the summary, its selected detail level, and its available source links.
12. When the user selects a summary item, Source Traceability identifies the originating record. Identity and Access checks access again before the source is shown. The interface opens the source record for verification. This follows AC-004 and AC-006.


## 4. Design Decisions

The requester referred to a list of key design decisions, but no answers to the earlier decision questions were included in the message. The decisions below therefore distinguish constraints directly supplied for this design from provisional preferences made to produce a coherent proposal.

| Decision | Reason |
|---|---|
| **User-specified constraint:** SESS is an aid for reviewing patient information, not a replacement for the EHR; clinical write-back and prescribing are excluded. | The spec defines SESS around retrieval, organization, summarization, and source verification (Overview, FR-002–FR-006, AC-002–AC-006). It does not define clinical order-entry or prescribing workflows. |
| **User-specified constraint:** Healthcare professionals and other authorized healthcare employees may use SESS. An RN or medical scribe may have the same level of access as a healthcare professional where authorized. | The actor model includes Healthcare Professional and Authorized Employee (Domain Model—Actors). NFR-001 requires role-based access control but does not prescribe a fixed role hierarchy. |
| **User-specified constraint:** Prefer Python, Java, JavaScript, HTML, and CSS, and use established libraries where practical. | This is an implementation constraint supplied by the requester, not a requirement in the spec. |
| **User-specified constraint:** Prefer free resources, deploy locally when the EHRs are confined to one organization, otherwise allow cloud deployment. | This is an implementation/deployment constraint supplied by the requester, not a requirement in the spec. |
| Use a browser-based interface backed by one deployable application. **Preference.** | A browser interface is a straightforward way to provide the user workflows in FR-001–FR-004 and AC-001–AC-004. The spec does not mandate a web application or a deployment topology. |
| Keep the modules as internal boundaries of a single application rather than separate network services. **Preference.** | The acceptance criteria describe a small set of sequential user workflows (AC-001–AC-006); they do not require independently deployed services. A single deployment avoids adding operational components not required by the spec. |
| Use an agreed EHR interface, with HL7 FHIR as the preferred interface when supported by the source EHR. **Preference for FHIR. Interface agreement is required.** | NFR-007 requires an agreed, documented interface and preservation of identifiers, timestamps, and context. The spec does not name FHIR, HL7 v2, or a vendor-specific API. |
| Keep the EHR as the authoritative source and retrieve current records when a patient workflow needs them. Do not assume a persistent local replica. **Preference.** | NFR-006 says SESS must identify when current information cannot be retrieved and must not present stale information as current without identifying its age. NFR-007 requires exchange with the existing EHR. The spec does not decide whether records or summaries are cached or retained. |
| Enforce authentication and role-based authorization in Identity and Access, including checks before patient data and source records are disclosed. | FR-001, NFR-001, AC-001, and AC-004. The spec requires authentication and role-based access control but leaves the identity provider and exact role matrix open. |
| Do not assume a fixed list of job titles or that all users have identical permissions. Configure permissions according to the healthcare organization's authorization policy. **Preference.** | NFR-001 requires role-based access control; the Domain Model identifies two broad actor types but does not define role names or a permission matrix. |
| Organize patient information and perform search/filter within the selected patient's records. | FR-003 and FR-005, AC-003 and AC-005. |
| Generate structured summaries using the selected detail level and preserve source associations for each clinical item. | FR-002 and FR-006, NFR-002 and NFR-003, AC-002, AC-004, and AC-006. |
| The specification intentionally does not prescribe a summary-generation algorithm. Implementations may use deterministic methods, artificial intelligence, LLMs, or other techniques that satisfy the specification's accuracy and traceability requirements. **Preference.** | FR-005 requires categorization, while NFR-002 requires preserving source meaning and identifying incomplete or conflicting information. The spec does not prescribe AI, an LLM, or a summarization algorithm. |
| Record audit events in a protected application audit log. | NFR-008 specifies the events and audit fields that must be retained. |
| Preserve source timestamps and display the age of information when current retrieval is unavailable. | NFR-006 and NFR-007. The spec requires timestamps to be preserved and stale information to be clearly identified, but does not define a freshness threshold. |
| Enforce session inactivity locking/termination through the authenticated session handling. Make the timeout configurable by the deploying organization. | NFR-001 requires inactive sessions to end or lock after a configurable period. The spec does not specify the timeout value. |
| Enforce the search and summary response-time targets through implementation and representative workload testing, not through an additional service. | NFR-004 defines the response-time targets and the required validation approach. |
| Treat source access and summary generation as read-only operations against the EHR. **Preference consistent with the stated scope.** | The Overview and FR-002–FR-006 describe reviewing, retrieving, organizing, and summarizing records. No acceptance criterion describes writing to the EHR. |


## 5. Constraints and known limits
### Implementation constraints supplied by the requester

- The implementation may use any language. Python, Java, JavaScript, HTML, and CSS are preferred options.
- Prefer existing libraries commonly used in healthcare EHR integrations.
- Prefer free resources.
- A local deployment is suitable when all connected EHRs belong to one hospital or clinic. A cloud deployment may be needed when the deployment spans organizations or locations.
- The primary users are healthcare professionals, but other authorized healthcare workers, including RNs and medical scribes, may be granted equivalent access.
- SESS is not an EHR replacement and is not intended to prescribe medication or perform clinical write-back.


### Design Limits

- The spec does not identify a target EHR vendor, version, API, or test environment. The EHR Connector cannot be finalized until the actual source interface and its supported data are known (NFR-007).
- The design assumes the EHR can provide patient identity, records, timestamps, and stable source identifiers. If it cannot, source verification and item-level traceability may be incomplete (NFR-003 and NFR-007).
- The design does not define a clinical terminology mapping strategy for differences in coding systems, units, or vendor-specific fields. Such mappings would need to be specified if source systems use incompatible representations (FR-005, NFR-007).
- The design does not select an AI model or guarantee the clinical correctness of generated prose. The system must preserve source meaning, expose source records, and flag unavailable, incomplete, or conflicting information. Clinical users remain responsible for reviewing the source before relying on a summary (NFR-002 and NFR-003).
- The spec does not define summary retention, version history, caching policy, or a freshness threshold. These must be decided before implementing historical summary review or making stronger guarantees about how current a summary is (NFR-006).
- The spec does not define the user identity provider, exact roles, patient-assignment rules, or emergency-access policy. These must be agreed with the healthcare organization to implement a complete authorization policy (FR-001, NFR-001).
- The spec does not define multi-organization tenancy or data-isolation requirements. Serving independent healthcare organizations from one installation would require additional tenant isolation and administration decisions (NFR-001, NFR-007).
- The spec does not define a target workload, number of concurrent users, or record volume. The proposed response-time targets must be validated with a representative dataset and workload as required by NFR-004.
- The spec does not define backup, disaster recovery, or recovery-time objectives. These would need to be added for a production deployment beyond the availability and fault-handling expectations in NFR-006.
- The spec does not define export, printing, EHR embedding, notifications, or break-glass workflows. These are not included in this minimal architecture.


## 6. Out of Scope

- Replacing the existing EHR.
- Prescribing medications or placing clinical orders.
- Creating or modifying diagnoses, medication lists, clinical notes, or other source EHR records.
- Making autonomous clinical decisions or replacing professional review of source information.


## Spec Issues

1. **Authorization scope is underspecified:** Role definitions remain intentionally abstract. The specification now requires configurable role-based access and patient-access rules but does not define a standard set of organizational roles, permission matrices, or care-relationship policies. These are expected to be configured by the deploying healthcare organization.
2.  **Concurrency behavior:** Concurrent updates remain implementation-dependent. The specification requires each summary to represent a single retrieval request and requires regeneration if a consistent summary cannot be produced, but it does not prescribe how concurrent EHR updates are detected or resolved.
3.  **Failure behavior:** Failure handling is partially specified. The specification now requires unavailable categories to be identified during partial retrievals but does not define user-interface behavior for every possible EHR or network failure scenario.
4.  **Audit scope:** Audit scope may require further organizational requirements. The specification now includes authentication, authorization failures, source-record viewing, audit-record access, patient-record access, summary generation, and permission changes, but organizations may choose to audit additional events such as searches or exports.
