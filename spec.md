# Description
The Smart EHR Summarization System (SESS) is a healthcare application that assists authorized healthcare professionals in efficiently reviewing patient electronic health records (EHRs). The system organizes fragmented patient information into a structured format, generates appointment-relevant patient summaries, supports searching and filtering patient records, and provides traceability from generated summaries back to the original source records. The system is designed to reduce the time required to review patient information while maintaining security and privacy for protected health information (PHI).



# Goals
1. Enable healthcare professionals to efficiently review patient information.
2. Help healthcare professionals make informed clinical decisions.
3. Quickly communicate a patient's current health status.
4. Organize and retrieve patient health information securely.
5. Maintain traceability between generated summaries and original patient records.




# Domain Model
## Actors
- **Healthcare Professional:** Authorized user who reviews patient records and generates summaries.
- **Authorized Employee:** An authenticated user who is permitted by the healthcare organization to access patient information required for their job responsibilities. Authorized Employees use the same authentication process as Healthcare Professionals, but the patient information and system functions they may access are determined by their assigned role.
- **SESS:** Smart EHR Summarization System responsible for organizing, summarizing, and retrieving patient information.
- **Existing EHR System:** External system that stores patient health records.



## Objects
- Patient
- Patient Record
- Patient Summary
- Source Record
- Protected Health Information (PHI)
- Electronic Health Record (EHR)
- Medical History
- Diagnosis
- Medication
- Allergy
- Procedure
- Laboratory Result
- Clinical Note
- Clinical Event
- Healthcare Professional Account
- Authentication Credentials
- Search Criteria
- Summary Detail Level



# Functional Requirements
### FR-001: Healthcare Professional Authentication
As a healthcare professional, I want to authenticate before accessing patient health information so that I can securely access information that I am authorized to view.

### FR-002: Generate Patient Summary

As a healthcare professional, I want to generate a structured summary of an authorized patient's health information and select the level of detail included in the summary so that I can quickly understand the patient's current status. 

The available summary detail levels shall include Brief, Standard, and Detailed. Each level shall present the same patient information at different levels of completeness while maintaining traceability to the originating source records.

The specification does not require a particular summary-generation algorithm. Implementations may use rule-based methods, artificial intelligence, LLMs, or other techniques provided that the requirements in NFR-002 are satisfied.

### FR-003: Search and Filter Patient Information

As a healthcare professional, I want to search and filter a patient's health information by criteria such as date, record type, diagnosis, medication, provider, procedure, and laboratory test so that I can quickly locate relevant patient information.

### FR-004: Verify Summary Information

As a healthcare professional, I want to access the underlying source record associated with information in a generated summary so that I can verify the information and review additional details when needed.

The originating source record may be displayed within SESS or opened through the connected EHR system, depending on the capabilities of the deployed EHR interface. In either case, authorization shall be verified before access is granted.

### FR-005: Organize Patient Health Information

The system shall organize available PHI into predefined categories, including demographics, medical history, diagnoses, medications, allergies, procedures, laboratory results, imaging, clinical notes, hospitalizations, and recent encounters.

### FR-006: Maintain Summary Traceability

The system shall associate information included in a generated patient summary with the underlying patient record from which the information was obtained.



# Nonfunctional Requirements
### NFR-001: Security and Privacy

SESS shall protect PHI from unauthorized access, disclosure, alteration, and destruction. The system shall enforce role-based access controls for authenticated users, protect PHI during transmission and storage, and end or lock inactive sessions after a configurable period. 

Access to patient information shall be granted only to authenticated users whose assigned role is authorized to access the requested patient according to the healthcare organization's policies. Role permissions and patient-access rules shall be configurable by the deploying organization rather than fixed within SESS.

### NFR-002: Accuracy and Clinical Reliability
SESS shall present patient information in summaries and categorized records without knowingly changing the meaning of the source information. The system shall identify unavailable, conflicting, or incomplete source information rather than presenting it as confirmed fact. Healthcare professionals shall be able to review the source information before relying on a summary for a clinical decision.

### NFR-003: Traceability and Verifiability
For every clinical item included in a generated summary, SESS shall retain a link to its originating source record and make that source accessible to an authorized user. The link shall identify the relevant source record and, when available, the specific section or data element supporting the summary item.

### NFR-004: Performance
Under the expected workload, SESS shall display search results within 3 seconds for at least 95% of searches and generate a patient summary within 10 seconds for at least 95% of summary requests. These targets should be validated using a representative test dataset and workload, then adjusted if actual clinical workflows require different thresholds.

Performance measurements shall begin when the user submits the request and end when the requested results are displayed. Validation shall be performed using a representative workload defined by the deploying healthcare organization, including expected patient record sizes and concurrent users.

### NFR-005: Usability and Workflow Efficiency
A healthcare professional who has received basic system training shall be able to select an authorized patient, generate a summary, locate a relevant record using search or filters, and open its source record without needing technical assistance. The interface shall clearly distinguish summary content from source-record content and make the summary detail level and available categories understandable.

### NFR-006: Availability and Fault Handling
SESS shall be available during the healthcare organization's defined operating hours, with a proposed availability target of at least 99.5% per calendar month, excluding scheduled maintenance. If the EHR source system or a network connection is unavailable, SESS shall communicate that current information cannot be retrieved and shall not present stale information as current without clearly identifying its age.

If only part of the requested patient information can be retrieved, SESS shall clearly identify the unavailable categories while displaying successfully retrieved information. Information shall be considered stale whenever SESS cannot retrieve the current version from the connected EHR and must rely on previously retrieved information. Any stale information shall display the time at which it was originally retrieved.

Generated summaries may be retained according to the healthcare organization's retention policy. Historical summaries shall be clearly identified as historical and shall not be presented as the current patient summary.

Availability shall be measured over each calendar month during the healthcare organization's defined operating hours, excluding scheduled maintenance. Planned maintenance periods shall be communicated to users before maintenance begins.

### NFR-007: Interoperability and Data Compatibility
SESS shall exchange patient information with the Existing EHR System through an agreed, documented interface and shall preserve the meaning, identifiers, timestamps, and relevant context of imported records. The system shall report records or fields that cannot be interpreted or imported.

Imported timestamps shall preserve the values supplied by the source EHR. When displayed to users, timestamps shall use the healthcare organization's configured timezone while retaining the original source timestamp for traceability.

A generated summary shall represent the patient information retrieved during a single summary-generation request. If patient records change during retrieval and a consistent summary cannot be produced, SESS shall notify the user and require the summary to be regenerated.

### NFR-008: Auditability
SESS shall maintain a protected audit record of access to patient information and significant actions, including authentication events, patient-record access, summary generation, and changes to access permissions. Audit records shall include the user, action, patient or record reference where applicable, and timestamp, and shall be accessible only to appropriately authorized personnel.

Audit records shall also include failed authorization attempts, source-record viewing, and access to audit records. Audit records shall not be modified except through authorized system administration functions.



# Acceptance Criteria
## AC-001 (FR-001): Authenticate Healthcare Professional

<pre><code>
<b>Feature: Healthcare professional authentication

<b>Scenario:</b> Successfully authenticate a healthcare professional

    <b>Given</b> the healthcare professional is on the login screen

    <b>When</b> valid authentication credentials are entered

    <b>And</b> the Sign In button is selected

    <b>Then</b> the system authenticates the healthcare professional

    <b>And</b> access to authorized patient information is granted

<b>Scenario:</b> Reject invalid authentication credentials

    <b>Given</b> the healthcare professional is on the login screen

    <b>When</b> invalid credentials are entered

    <b>And</b> the Sign In button is selected

    <b>Then</b> authentication is rejected

    <b>And</b> an authentication error is displayed

<b>Scenario:</b> Reject unauthorized patient access

    <b>Given</b> the healthcare professional is authenticated

    <b>When</b> the healthcare professional attempts to access a patient they are not authorized to view

    <b>Then</b> access is denied

    <b>And</b> an authorization error is displayed

<b>Scenario:</b> Session expires after inactivity

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> the session has been inactive for longer than the configured timeout

    <b>When</b> the healthcare professional attempts another action

    <b>Then</b> the session is ended or locked

    <b>And</b> authentication is required before continuing
</code></pre>


## AC-002 (FR-002): Generate Patient Summary

<pre><code>
<b>Feature:</b> Patient summary generation

<b>Scenario: Generate a patient summary with a selected level of detail

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> an authorized patient has been selected

    <b>When</b> Generate Summary is selected

    <b>And</b> a summary detail level is chosen

    <b>Then</b> the system generates a structured patient summary

    <b>And</b> displays the summary using the selected detail level

<b>Scenario:</b> Generate a partial patient summary

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> an authorized patient has been selected

    <b>And</b> one category of patient information cannot be retrieved

    <b>When</b> Generate Summary is selected

    <b>Then</b> the system generates a structured patient summary using the available information

    <b>And</b> identifies the unavailable category

<b>Scenario:</b> Identify stale information

    <b>Given</b> current patient information cannot be retrieved

    <b>When</b> a previously retrieved patient summary is displayed

    <b>Then</b> the summary is identified as stale

    <b>And</b> the retrieval timestamp is displayed
</code></pre>


## AC-003 (FR-003): Search and Filter Patient Information

<pre><code>
<b>Feature:</b> Patient information retrieval

<b>Scenario:</b> Search and filter a patient's health information

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> an authorized patient has been selected

    <b>When</b> a search term is entered

    <b>And</b> one or more filters are applied

    <b>Then</b> matching patient records are displayed
</code></pre>



## AC-004 (FR-004): Verify Summary Information

<pre><code>
<b>Feature:</b> Summary verification and traceability

<b>Scenario:</b> Access the source record for information in a patient summary

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> a patient summary has already been generated

    <b>When</b> the healthcare professional selects an item within the summary

    <b>Then</b> the system identifies the originating source record

    <b>And</b> allows the source record to be viewed

<b>Scenario:</b> Verify authorization before viewing a source record

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> a patient summary has already been generated

    <b>When</b> the healthcare professional selects an item within the summary

    <b>Then</b> authorization is verified

    <b>And</b> the associated source record is displayed or opened through the connected EHR system
</code></pre>


## AC-005 (FR-005): Organize Patient Information

<pre><code>
<b>Scenario: Organize PHI

    <b>Given</b> patient records are available

    <b>When</b> the system imports the records

    <b>Then</b> the information is categorized into predefined medical categories
</code></pre>



## AC-006 (FR-006): Maintain Summary Traceability

<pre><code>
<b>Scenario:</b> Link summary to source

    <b>Given</b> a patient summary has been generated

    <b>When</b> any summary item is selected

    <b>Then</b> the corresponding source patient record can be identified

<b>Scenario:</b> Preserve source context

    <b>Given</b> a patient summary has been generated

    <b>When</b> any summary item is selected

    <b>Then</b> the corresponding source patient record can be identified

    <b>And</b> the associated timestamp and available source context are displayed
</code></pre>


## AC-007 (NFR-008): Auditability

<pre><code>
<b>Feature:</b> Audit recording

<b>Scenario:</b> Record summary generation

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> an authorized patient has been selected

    <b>When</b> a patient summary is generated

    <b>Then</b> an audit record is created

    <b>And</b> the audit record includes the user, action, patient reference, and timestamp
</code></pre>