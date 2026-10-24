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
- **Authorized Employee:** Other authenticated user permitted to access patient information.
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

### FR-003: Search and Filter Patient Information

As a healthcare professional, I want to search and filter a patient's health information by criteria such as date, record type, diagnosis, medication, provider, procedure, and laboratory test so that I can quickly locate relevant patient information.

### FR-004: Verify Summary Information

As a healthcare professional, I want to access the underlying source record associated with information in a generated summary so that I can verify the information and review additional details when needed.

### FR-005: Organize Patient Health Information

The system shall organize available PHI into predefined categories, including demographics, medical history, diagnoses, medications, allergies, procedures, laboratory results, imaging, clinical notes, hospitalizations, and recent encounters.

### FR-006: Maintain Summary Traceability

The system shall associate information included in a generated patient summary with the underlying patient record from which the information was obtained.



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
</pre></code>



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
</pre></code>



## AC-003 (FR-003): Search and Filter Patient Information

<pre><code>
<b>Feature:</b> Patient information retrieval

<b>Scenario:</b> Search and filter a patient's health information

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> an authorized patient has been selected

    <b>When</b> a search term is entered

    <b>And</b> one or more filters are applied

    <b>Then</b> matching patient records are displayed
</pre></code>



## AC-004 (FR-004): Verify Summary Information

<pre><code>
<b>Feature:</b> Summary verification and traceability

<b>Scenario:</b> Access the source record for information in a patient summary

    <b>Given</b> the healthcare professional is authenticated

    <b>And</b> a patient summary has already been generated

    <b>When</b> the healthcare professional selects an item within the summary

    <b>Then</b> the system identifies the originating source record

    <b>And</b> allows the source record to be viewed
</pre></code>



## AC-005 (FR-005): Organize Patient Information

<pre><code>
<b>Scenario: Organize PHI

    <b>Given</b> patient records are available

    <b>When</b> the system imports the records

    <b>Then</b> the information is categorized into predefined medical categories
</pre></code>



## AC-006 (FR-006): Maintain Summary Traceability

<pre><code>
<b>Scenario:</b> Link summary to source

    <b>Given</b> a patient summary has been generated

    <b>When</b> any summary item is selected

    <b>Then</b> the corresponding source patient record can be identified
</pre></code>
