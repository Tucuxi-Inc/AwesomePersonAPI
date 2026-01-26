---
name: data-protection-examples
description: >-
  Real clause examples for data protection provisions including DPA terms,
  GDPR compliance, security requirements, and breach notification with
  various party position variations.
tags:
  - data-protection
  - gdpr
  - privacy
  - security
  - dpa
  - examples
version: '1.0'
confidence_level: HIGH
category: clause_examples
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - data-protection-taxonomy
  - data-protection-negotiation
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Data Protection Clause Examples

## Processing Terms

### Controller-Favorable (Customer as Controller)

**Example 1 - Strong Controller Rights**
```
DATA PROTECTION

Vendor shall process Customer Data only in accordance with Customer's
documented instructions. Vendor shall not process Customer Data for
any purpose other than performing the Services.

Vendor shall:
(a) implement appropriate technical and organizational measures to
    protect Customer Data against unauthorized access, disclosure,
    alteration, or destruction;
(b) ensure that personnel with access to Customer Data are bound by
    confidentiality obligations;
(c) not engage sub-processors without Customer's prior written consent;
(d) assist Customer in responding to data subject requests;
(e) delete or return Customer Data upon termination;
(f) make available information necessary to demonstrate compliance.

Customer retains all right, title, and interest in Customer Data.
Vendor acquires no rights to Customer Data except as necessary to
perform the Services.
```

---

### GDPR Article 28 Compliance

**Example 2 - Full GDPR DPA Terms**
```
DATA PROCESSING ADDENDUM

1. DEFINITIONS
   "Personal Data" means information relating to an identified or
   identifiable natural person processed by Processor on behalf of
   Controller under this Agreement.

2. PROCESSING INSTRUCTIONS
   Processor shall process Personal Data only on documented instructions
   from Controller, including transfers to third countries. The subject
   matter, duration, nature, and purpose of processing are set forth in
   Annex 1.

3. CONFIDENTIALITY
   Processor shall ensure that persons authorized to process Personal
   Data have committed to confidentiality or are under statutory
   confidentiality obligation.

4. SECURITY
   Processor shall implement appropriate technical and organizational
   measures as set forth in Annex 2, including as appropriate:
   (a) pseudonymization and encryption;
   (b) ability to ensure confidentiality, integrity, availability;
   (c) ability to restore availability in a timely manner;
   (d) regular testing and evaluation of effectiveness.

5. SUB-PROCESSORS
   Processor shall not engage sub-processors without prior specific or
   general written authorization from Controller. Processor shall impose
   equivalent data protection obligations on sub-processors.

6. DATA SUBJECT RIGHTS
   Processor shall assist Controller in responding to requests from data
   subjects to exercise their rights under GDPR.

7. SECURITY INCIDENTS
   Processor shall notify Controller without undue delay (and in any
   event within 48 hours) after becoming aware of a Personal Data breach.

8. AUDITS
   Processor shall make available all information necessary to demonstrate
   compliance and allow for and contribute to audits and inspections.

9. DELETION
   Upon termination, Processor shall, at Controller's choice, delete or
   return all Personal Data and delete existing copies.
```

---

## Security Requirements

**Example 3 - Detailed Security Standards**
```
SECURITY MEASURES

Vendor shall implement and maintain security measures that include:

ADMINISTRATIVE SAFEGUARDS:
(a) Designated security officer responsible for security program
(b) Written information security policies and procedures
(c) Background checks for personnel with data access
(d) Security awareness training for all personnel
(e) Incident response plan tested annually

TECHNICAL SAFEGUARDS:
(a) Encryption of data in transit (TLS 1.2+) and at rest (AES-256)
(b) Multi-factor authentication for administrative access
(c) Network segmentation and firewalls
(d) Intrusion detection and prevention systems
(e) Logging and monitoring of system access
(f) Vulnerability scanning and penetration testing (annual minimum)
(g) Patch management within 30 days (critical), 90 days (other)

PHYSICAL SAFEGUARDS:
(a) Data center access controls and monitoring
(b) Environmental controls (fire, flood, climate)
(c) Secure disposal of media containing Customer Data

CERTIFICATIONS:
Vendor shall maintain SOC 2 Type II certification or equivalent and
provide reports to Customer upon request.
```

---

## Breach Notification

**Example 4 - Comprehensive Breach Response**
```
SECURITY INCIDENT NOTIFICATION

Upon discovery of a Security Incident (unauthorized access to, or
acquisition, use, or disclosure of Customer Data), Vendor shall:

(a) NOTIFICATION: Notify Customer within [24/48/72] hours of discovery.
    Initial notification shall include: nature of the incident, types
    of data affected, estimated number of individuals affected,
    immediate remediation steps taken.

(b) INVESTIGATION: Conduct a thorough investigation and provide Customer
    with a detailed incident report within [5] business days, including
    root cause analysis and steps to prevent recurrence.

(c) COOPERATION: Cooperate with Customer's investigation, including
    providing access to logs, personnel, and systems as reasonably
    requested.

(d) REMEDIATION: Implement appropriate remediation measures and provide
    evidence of completion.

(e) REGULATORY NOTIFICATION: Assist Customer with notifications to
    regulators and affected individuals as required by law.

(f) COSTS: Vendor shall bear costs of: (i) investigation; (ii) required
    notifications; (iii) credit monitoring for affected individuals
    (if breach resulted from Vendor's failure to comply with this
    Agreement); (iv) regulatory fines arising from Vendor's breach.
```

---

## Sub-Processor Management

**Example 5 - Sub-Processor Controls**
```
SUB-PROCESSORS

Vendor may engage the sub-processors listed in Exhibit [X] ("Approved
Sub-Processors") for the processing activities specified.

To engage additional sub-processors, Vendor shall:
(a) Provide Customer with [30] days prior written notice;
(b) Identify the sub-processor, processing activities, and location;
(c) Confirm the sub-processor is bound by equivalent data protection
    obligations.

Customer may object to a new sub-processor on reasonable data protection
grounds within [15] days. If Customer objects and the parties cannot
resolve the objection, Customer may terminate the affected Service
without penalty.

Vendor remains fully liable for the acts and omissions of its
sub-processors.
```

---

## Data Return/Deletion

**Example 6 - Termination Data Handling**
```
DATA RETURN AND DELETION

Upon termination or expiration of this Agreement:

(a) EXPORT PERIOD: Vendor shall make Customer Data available for export
    in a standard, machine-readable format for [30] days following
    termination.

(b) CUSTOMER ELECTION: Customer shall elect in writing to have Customer
    Data returned or deleted.

(c) RETURN: If Customer elects return, Vendor shall provide all Customer
    Data within [30] days in a format reasonably requested by Customer.

(d) DELETION: If Customer elects deletion (or fails to elect), Vendor
    shall delete all Customer Data within [30] days of termination
    (or the export period, if later).

(e) CERTIFICATION: Vendor shall certify in writing that all Customer Data
    has been returned or deleted as requested.

(f) EXCEPTIONS: Vendor may retain copies required by law or embedded in
    backup systems, subject to continuing confidentiality obligations.
    Backups shall be deleted in accordance with normal retention schedules.
```

---

## Cross-Border Transfers

**Example 7 - International Transfer Mechanisms**
```
INTERNATIONAL DATA TRANSFERS

Vendor shall not transfer Personal Data outside the European Economic
Area, United Kingdom, or Switzerland unless:

(a) The transfer is to a jurisdiction deemed adequate by the European
    Commission;

(b) The parties have executed the EU Standard Contractual Clauses
    (Module 2: Controller to Processor) attached as Exhibit [X];

(c) Vendor relies on a valid Binding Corporate Rules mechanism; or

(d) Another lawful transfer mechanism under GDPR applies.

Vendor shall implement supplementary measures as necessary to ensure
adequate protection for transferred data, including encryption and
access controls.
```

---

## Privacy by Design

**Example 8 - Product Privacy Requirements**
```
PRIVACY BY DESIGN

Vendor shall implement data protection by design and default:

(a) MINIMIZATION: Collect and process only the minimum Personal Data
    necessary for the specified purposes;

(b) PURPOSE LIMITATION: Not process Personal Data for purposes beyond
    those specified without consent;

(c) RETENTION: Retain Personal Data only for as long as necessary and
    implement automatic deletion;

(d) ACCESS CONTROLS: Limit access to Personal Data to personnel with
    a legitimate need;

(e) TRANSPARENCY: Provide clear privacy notices and honor data subject
    preferences;

(f) SECURITY: Embed security measures throughout the development lifecycle.
```

---

## Cross-References

- See also: [[data-protection-taxonomy]] - Data protection patterns
- See also: [[data-processing-expected-clauses]] - Full DPA structure
- See also: [[data-protection-negotiation]] - Negotiation strategies
