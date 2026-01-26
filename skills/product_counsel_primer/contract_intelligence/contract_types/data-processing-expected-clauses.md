---
name: data-processing-expected-clauses
description: >-
  Expected clauses and structure for Data Processing Agreements (DPAs) and
  Addenda including GDPR compliance, controller-processor terms, security,
  and international transfers. Use when drafting or reviewing privacy terms.
tags:
  - dpa
  - gdpr
  - data-processing
  - privacy
  - controller-processor
  - contract-type
version: '1.0'
confidence_level: HIGH
category: contract_types
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - data-protection-taxonomy
  - confidentiality-taxonomy
  - indemnification-taxonomy
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 1
validation_type: human_validated
source_type: contract_samples
---

# Data Processing Agreement (DPA) - Expected Clauses

## Overview

Data Processing Agreements (DPAs) or Addenda govern the processing of personal data by one party (processor) on behalf of another (controller). GDPR Article 28 requires written agreements between controllers and processors with specific content. This skill documents expected structure and provisions for GDPR-compliant DPAs.

## When DPA is Required

- Vendor processes Personal Data on behalf of Customer
- SaaS, cloud hosting, analytics, marketing services
- Any outsourced data processing involving EU/UK data subjects
- Cross-border data transfers

## Standard Structure

### Typical Section Order

1. Definitions
2. Scope and Processing Details
3. Processor Obligations
4. Controller Obligations
5. Sub-Processing
6. Data Subject Rights
7. Security Measures
8. Data Breach Notification
9. International Transfers
10. Audit Rights
11. Data Return and Deletion
12. Liability
13. Term and Termination
14. Annexes (Processing Details, Security Measures, SCCs)

## Required Clauses (GDPR Article 28)

### 1. Scope and Processing Details

**Must Include** (GDPR Art. 28(3)):
- [ ] Subject matter and duration
- [ ] Nature and purpose of processing
- [ ] Type of personal data
- [ ] Categories of data subjects

**Example**:
```
ANNEX 1: PROCESSING DETAILS

Subject Matter: Processing of Personal Data in connection with
provision of [Service Name] under the Agreement.

Duration: For the term of the Agreement plus any data retention period.

Nature of Processing: [Collection, storage, use, analysis, transmission,
erasure] of Personal Data as necessary to provide the Services.

Purpose: To enable Controller's use of the Services as described in
the Agreement.

Types of Personal Data:
- Contact information (name, email, phone, address)
- Account credentials (username, hashed passwords)
- Usage data (IP address, device info, activity logs)
- [Additional categories specific to service]

Categories of Data Subjects:
- Controller's employees
- Controller's customers/end users
- Controller's business contacts
```

### 2. Processor Obligations

**Must Include** (GDPR Art. 28(3)):
- [ ] Process only on documented instructions
- [ ] Ensure personnel confidentiality
- [ ] Implement security measures
- [ ] Sub-processor requirements
- [ ] Assist with data subject rights
- [ ] Assist with compliance obligations
- [ ] Delete/return data on termination
- [ ] Make information available for audits

**Example**:
```
PROCESSOR OBLIGATIONS

2.1 Instructions. Processor shall process Personal Data only:
    (a) in accordance with Controller's documented instructions;
    (b) as necessary to perform the Services; or
    (c) as required by applicable law (with prior notice to Controller
        unless legally prohibited).

2.2 Controller's initial instructions are set forth in this DPA and
    the Agreement. Additional instructions require written agreement.

2.3 If Processor believes an instruction violates Data Protection Law,
    Processor shall promptly notify Controller before processing.
```

### 3. Personnel and Confidentiality

**Must Include**:
- [ ] Confidentiality obligations
- [ ] Training requirements
- [ ] Access limitations

**Example**:
```
PERSONNEL

3.1 Confidentiality. Processor shall ensure that persons authorized
    to process Personal Data have committed to confidentiality or
    are under an appropriate statutory obligation of confidentiality.

3.2 Training. Processor shall ensure that personnel processing
    Personal Data receive appropriate data protection training.

3.3 Access Limitation. Processor shall limit access to Personal Data
    to personnel who need access to perform the Services.
```

### 4. Security Measures

**Must Include**:
- [ ] Technical and organizational measures
- [ ] Appropriate to the risk
- [ ] Specific measures (encryption, access controls, etc.)

**Example**:
```
SECURITY

4.1 Processor shall implement and maintain technical and organizational
    security measures appropriate to the risk, including:
    (a) pseudonymization and encryption of Personal Data;
    (b) ability to ensure ongoing confidentiality, integrity,
        availability, and resilience of processing systems;
    (c) ability to restore availability and access to Personal Data
        in a timely manner following an incident;
    (d) regular testing and evaluation of effectiveness of measures.

4.2 Specific measures are described in Annex 2 (Security Measures).

4.3 Processor shall maintain [SOC 2 Type II / ISO 27001] certification
    and provide audit reports or certificates upon request.
```

### 5. Sub-Processors

**Must Include**:
- [ ] Authorization requirements
- [ ] Notification process
- [ ] Sub-processor obligations
- [ ] Processor remains liable

**Example**:
```
SUB-PROCESSING

5.1 Authorization. Controller provides general authorization for
    Processor to engage Sub-processors. Current Sub-processors are
    listed at [URL] or in Annex 3.

5.2 Notification. Processor shall notify Controller at least [30] days
    before engaging a new Sub-processor or replacing an existing one.
    Controller may object on reasonable grounds within [15] days.

5.3 If Controller objects and the parties cannot resolve the objection,
    Controller may terminate the affected Services without penalty.

5.4 Sub-processor Agreements. Processor shall impose data protection
    obligations on Sub-processors equivalent to those in this DPA.

5.5 Liability. Processor remains fully liable for Sub-processor
    compliance with this DPA and Data Protection Law.
```

### 6. Data Subject Rights

**Must Include**:
- [ ] Assistance with requests
- [ ] Notification to Controller
- [ ] Response procedures

**Example**:
```
DATA SUBJECT RIGHTS

6.1 Processor shall assist Controller in responding to Data Subject
    requests to exercise rights under Data Protection Law, including:
    (a) access to Personal Data;
    (b) rectification of inaccurate data;
    (c) erasure ("right to be forgotten");
    (d) restriction of processing;
    (e) data portability;
    (f) objection to processing.

6.2 Processor shall notify Controller within [5] business days of
    receiving any Data Subject request and shall not respond directly
    unless instructed by Controller or required by law.

6.3 If Processor receives a request from a Data Subject that it
    cannot identify as relating to Controller, Processor shall
    inform the Data Subject to contact Controller directly.
```

### 7. Data Breach Notification

**Must Include**:
- [ ] Notification timeline
- [ ] Content of notification
- [ ] Cooperation obligations

**Example**:
```
DATA BREACH NOTIFICATION

7.1 Processor shall notify Controller without undue delay, and in
    any event within [24/48/72] hours, after becoming aware of a
    Personal Data Breach.

7.2 Notification shall include, to the extent known:
    (a) description of the nature of the breach, including categories
        and approximate number of Data Subjects and records affected;
    (b) name and contact details of Processor's data protection contact;
    (c) likely consequences of the breach;
    (d) measures taken or proposed to address the breach and mitigate
        possible adverse effects.

7.3 Processor shall cooperate with Controller's investigation and
    response, including communications to authorities and Data Subjects.

7.4 Processor shall document all Personal Data Breaches including
    facts, effects, and remedial actions taken.
```

### 8. International Transfers

**Must Include**:
- [ ] Transfer restrictions
- [ ] Approved transfer mechanisms
- [ ] Standard Contractual Clauses (if applicable)

**Example**:
```
INTERNATIONAL TRANSFERS

8.1 Processor shall not transfer Personal Data outside the EEA/UK
    unless:
    (a) the transfer is to a country with an adequacy decision;
    (b) appropriate safeguards are in place; or
    (c) a derogation under Article 49 GDPR applies.

8.2 The parties agree to the EU Standard Contractual Clauses
    (Controller to Processor) attached as Annex 4 for transfers to
    countries without adequacy decisions.

8.3 If the SCCs or adequacy decision are invalidated or suspended,
    Processor shall: (a) notify Controller; (b) implement alternative
    safeguards; or (c) cease transfers.

8.4 Processor shall not transfer Personal Data to any country that
    Controller has prohibited in writing.
```

### 9. Audit Rights

**Must Include**:
- [ ] Right to audit
- [ ] Audit process
- [ ] Information provision

**Example**:
```
AUDIT RIGHTS

9.1 Processor shall make available to Controller all information
    necessary to demonstrate compliance with this DPA and
    Data Protection Law.

9.2 Processor shall allow for and contribute to audits and inspections
    conducted by Controller or a mandated auditor, subject to:
    (a) [30] days advance notice (except for urgent security concerns);
    (b) reasonable confidentiality protections;
    (c) no more than [one] audit per year (absent cause);
    (d) during normal business hours.

9.3 Controller shall bear audit costs unless the audit reveals
    material non-compliance, in which case Processor shall bear costs.

9.4 Processor may satisfy audit requirements by providing:
    (a) SOC 2 Type II reports or ISO 27001 certificates;
    (b) responses to Controller's security questionnaires;
    (c) summaries of penetration test results.
```

### 10. Data Return and Deletion

**Must Include**:
- [ ] Return or deletion option
- [ ] Certification of deletion
- [ ] Retention exceptions

**Example**:
```
DATA RETURN AND DELETION

10.1 Upon termination or expiration of the Agreement, or upon
     Controller's request, Processor shall, at Controller's election:
     (a) return Personal Data to Controller in a standard,
         machine-readable format; or
     (b) delete all Personal Data and certify deletion in writing.

10.2 Processor shall complete return or deletion within [30] days
     of termination or request.

10.3 Processor may retain Personal Data to the extent required by
     applicable law, subject to continued confidentiality and
     security obligations. Processor shall inform Controller of
     the legal basis and retention period.

10.4 Processor shall ensure Sub-processors comply with this Section.
```

## Common Clauses

### 11. Controller Obligations

```
CONTROLLER OBLIGATIONS

11.1 Controller warrants that: (a) it has a lawful basis for
     processing Personal Data; (b) Data Subjects have been provided
     required notices; (c) it has authority to provide processing
     instructions; (d) its instructions comply with Data Protection Law.

11.2 Controller shall be responsible for the accuracy, quality, and
     legality of Personal Data and the means by which it acquired
     Personal Data.
```

### 12. Assistance with Compliance

```
COMPLIANCE ASSISTANCE

12.1 Processor shall assist Controller with:
     (a) Data Protection Impact Assessments (DPIAs);
     (b) prior consultations with supervisory authorities;
     (c) security obligation compliance (Art. 32);
     (d) breach notification obligations (Arts. 33-34).

12.2 Assistance may be provided at Controller's cost at Processor's
     then-current professional services rates for non-routine requests.
```

### 13. Liability and Indemnification

```
LIABILITY

13.1 Each party shall be liable for damages caused by processing
     that violates Data Protection Law to the extent provided by
     Data Protection Law.

13.2 Processor shall indemnify Controller for fines, penalties, and
     damages arising from Processor's breach of this DPA or Data
     Protection Law, to the extent such breach was within Processor's
     control.

13.3 The limitations of liability in the Agreement shall apply to
     this DPA, except that [Data Breach liability / regulatory fines]
     shall [be subject to a separate cap of [AMOUNT] / be unlimited].
```

## Required Annexes

### Annex 1: Processing Details
- Subject matter and duration
- Nature and purpose
- Personal data types
- Data subject categories

### Annex 2: Security Measures
- Technical measures (encryption, access controls, monitoring)
- Organizational measures (policies, training, incident response)
- Physical measures (facility security)
- Certifications

### Annex 3: Sub-Processors
- List of current sub-processors
- Location and processing activities
- Update mechanism

### Annex 4: Standard Contractual Clauses
- EU SCCs (2021 version)
- UK IDTA (if UK data)
- Module selection and options completed

## Red Flags - Missing Elements

| Missing Element | Risk Level | Implication |
|-----------------|------------|-------------|
| No processing instructions | HIGH | GDPR Art. 28 violation |
| No breach notification | HIGH | Delayed response |
| No sub-processor controls | HIGH | Unknown data exposure |
| No security measures | HIGH | Inadequate protection |
| No transfer mechanism | HIGH | Unlawful transfers |
| No audit rights | MEDIUM | Cannot verify compliance |
| No deletion requirement | MEDIUM | Data retained indefinitely |
| Missing SCCs | HIGH | No transfer basis |
| No liability terms | MEDIUM | Unclear responsibility |

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[data-protection-taxonomy]] - Detailed privacy clause patterns
- [[data-protection-examples]] - Real GDPR/DPA language from contracts
- [[data-protection-negotiation]] - Privacy term negotiation strategies
- [[confidentiality-taxonomy]] - Broader confidentiality obligations
- [[indemnification-taxonomy]] - Data breach and compliance indemnification
- [[limitation-of-liability-taxonomy]] - DPA liability caps and carve-outs
- [[audit-rights-taxonomy]] - Security and compliance audit provisions
- [[termination-taxonomy]] - Data return and deletion upon termination

**Related Key Provisions** (tech_transactions):
- [[privacy_and_data_protection.md]] - Conceptual privacy framework
- [[confidentiality_nda.md]] - Information protection principles
- [[regulatory_compliance.md]] - Privacy regulation compliance

**Related Transaction Types** (tech_transactions):
- [[saas_licensing_agreements.md]] - DPA in SaaS context
- [[cloud_infrastructure_agreements.md]] - DPA for cloud services

**Cognitive Patterns** (apply when reviewing DPAs):
- `S1` - Stakeholder identification (data subjects, controllers, processors)
- `S3` - Multi-domain synthesis (legal + technical + regulatory)
- `S5` - Party dynamics (controller vs. processor obligations)
- `S7` - Future-proofing (regulatory change adaptation)
- `BI3` - Context-aware risk (data sensitivity and volume)
- `BI4` - Battle selection (key DPA terms to negotiate)
