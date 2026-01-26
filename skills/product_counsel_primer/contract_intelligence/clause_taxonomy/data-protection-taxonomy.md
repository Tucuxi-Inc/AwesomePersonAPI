---
name: data-protection-taxonomy
description: >-
  Comprehensive taxonomy of data protection clauses including GDPR, CCPA,
  data processing terms, security requirements, and breach notification.
  Critical for cloud, SaaS, and data-intensive agreements.
tags:
  - data-protection
  - privacy
  - gdpr
  - ccpa
  - data-processing
  - security
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - confidentiality-taxonomy
  - indemnification-taxonomy
  - limitation-of-liability-taxonomy
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 1
validation_type: human_validated
source_type: contract_samples
---

# Data Protection Taxonomy

## Overview

Data protection provisions govern the collection, processing, storage, and transfer of personal data. With GDPR, CCPA, and emerging privacy regulations, these clauses have become critical in technology agreements. This taxonomy catalogs data protection patterns observed across commercial agreements.

## Regulatory Framework

### Key Privacy Regulations

| Regulation | Jurisdiction | Key Requirements |
|------------|--------------|------------------|
| **GDPR** | EU/EEA | Controller/processor obligations, DPA required, 72-hour breach notice |
| **CCPA/CPRA** | California | Consumer rights, service provider contracts, opt-out rights |
| **LGPD** | Brazil | Similar to GDPR, local DPO requirement |
| **PIPEDA** | Canada | Consent-based, accountability principle |
| **UK GDPR** | United Kingdom | Post-Brexit GDPR equivalent |
| **HIPAA** | US Healthcare | PHI protections, BAA required |
| **PCI-DSS** | Payment Cards | Security standards for card data |

## Core Definitions

### Personal Data / Personal Information

```
"Personal Data" means any information relating to an identified or
identifiable natural person, including name, identification number,
location data, online identifier, or factors specific to the physical,
physiological, genetic, mental, economic, cultural, or social identity
of that person.
```

### Controller vs. Processor

```
"Controller" means the party that determines the purposes and means
of Processing Personal Data.

"Processor" means the party that Processes Personal Data on behalf
of the Controller.
```

**Typical Roles**:
- SaaS vendor: Processor (processes customer data per instructions)
- Customer: Controller (determines what data and why)
- Joint controllers: Both determine purposes (rare, complex)

### Processing

```
"Processing" means any operation performed on Personal Data, including
collection, recording, organization, structuring, storage, adaptation,
alteration, retrieval, consultation, use, disclosure by transmission,
dissemination, alignment, combination, restriction, erasure, or destruction.
```

## Data Processing Agreement (DPA) Components

### A. Subject Matter and Scope

```
This DPA applies to the Processing of Personal Data by Processor on
behalf of Controller in connection with the Services described in
the Agreement.

Categories of Data Subjects: [employees, customers, end users]
Types of Personal Data: [contact info, usage data, account data]
Processing Activities: [hosting, analytics, support]
Duration: For the term of the Agreement plus data retention period.
```

### B. Processing Instructions

```
Processor shall Process Personal Data only:
(a) in accordance with Controller's documented instructions;
(b) as necessary to perform the Services;
(c) as required by applicable law (with prior notice to Controller
    unless prohibited).

Controller's initial instructions are set forth in the Agreement.
Additional instructions require written agreement and may be subject
to additional fees.
```

### C. Security Measures

```
Processor shall implement appropriate technical and organizational
measures to ensure a level of security appropriate to the risk,
including:
(a) pseudonymization and encryption of Personal Data;
(b) ongoing confidentiality, integrity, availability, and resilience;
(c) ability to restore access following an incident;
(d) regular testing and evaluation of security measures.

Processor shall maintain SOC 2 Type II certification (or equivalent)
and provide audit reports upon request.
```

**Common Security Standards**:
- SOC 2 Type I/II
- ISO 27001
- NIST Cybersecurity Framework
- PCI-DSS (for payment data)
- HIPAA (for health data)

### D. Personnel Obligations

```
Processor shall ensure that personnel authorized to Process Personal
Data:
(a) have committed to confidentiality or are under statutory obligation;
(b) Process Personal Data only on Controller's instructions;
(c) receive appropriate data protection training.
```

### E. Sub-Processors

```
Processor shall not engage any Sub-processor without Controller's
prior [written consent / notification with opportunity to object].

Current Sub-processors are listed at [URL/Exhibit]. Processor shall
provide [30] days notice before engaging new Sub-processors.
Controller may object on reasonable grounds within [15] days.

Processor shall impose data protection obligations on Sub-processors
equivalent to those in this DPA and shall remain liable for
Sub-processor compliance.
```

**Consent Models**:
- Prior written consent (strictest; each sub-processor approved)
- General authorization with notification (standard)
- Pre-approved list with updates (practical)

### F. Data Subject Rights

```
Processor shall assist Controller in responding to Data Subject
requests to exercise their rights under applicable law, including:
(a) access to Personal Data;
(b) rectification of inaccurate data;
(c) erasure ("right to be forgotten");
(d) restriction of Processing;
(e) data portability;
(f) objection to Processing.

Processor shall notify Controller within [5] business days of
receiving any Data Subject request and shall not respond directly
unless instructed.
```

### G. Data Breach Notification

```
Processor shall notify Controller without undue delay (and in no
event later than [72/48/24] hours) after becoming aware of a
Personal Data Breach.

Notification shall include:
(a) description of the nature of the breach;
(b) categories and approximate number of Data Subjects affected;
(c) categories and approximate number of records affected;
(d) name and contact details of Processor's DPO or contact point;
(e) likely consequences of the breach;
(f) measures taken or proposed to address the breach.

Processor shall cooperate with Controller's investigation and
response, including notifications to authorities and Data Subjects.
```

**Notification Timelines**:
- GDPR: 72 hours (Controller to authority)
- HIPAA: 60 days (to individuals)
- CCPA: "Most expedient time possible"
- Contractual: Often 24-72 hours (Processor to Controller)

### H. International Data Transfers

```
Processor shall not transfer Personal Data outside the [EEA/UK/approved
jurisdictions] unless:
(a) the transfer is to a country with an adequacy decision;
(b) appropriate safeguards are in place (Standard Contractual Clauses);
(c) a derogation under Article 49 GDPR applies.

The parties agree to execute the Standard Contractual Clauses
attached as Exhibit [X].
```

**Transfer Mechanisms**:
- Adequacy decisions (limited countries)
- Standard Contractual Clauses (SCCs) - most common
- Binding Corporate Rules (intra-group)
- Specific derogations (consent, contract necessity)

### I. Audit Rights

```
Processor shall make available to Controller all information necessary
to demonstrate compliance with this DPA and applicable law, and shall
allow for and contribute to audits and inspections conducted by
Controller or its auditor.

Audits shall: (a) be conducted upon [30] days notice; (b) occur no
more than [annually]; (c) be subject to confidentiality; (d) be at
Controller's expense unless audit reveals material non-compliance.
```

### J. Data Deletion/Return

```
Upon termination or expiration of the Agreement, Processor shall,
at Controller's election:
(a) return all Personal Data to Controller in a standard format; or
(b) delete all Personal Data and certify such deletion in writing.

Processor may retain Personal Data to the extent required by applicable
law, subject to continued confidentiality and security obligations.
```

### K. Assistance Obligations

```
Processor shall assist Controller with:
(a) Data Protection Impact Assessments (DPIAs);
(b) prior consultations with supervisory authorities;
(c) compliance with Controller's security obligations;
(d) responding to inquiries from supervisory authorities.

Such assistance may be subject to additional fees at Processor's
then-current professional services rates.
```

## Customer Data Provisions (Non-DPA)

### Data Ownership

```
As between the parties, Customer owns all Customer Data. Nothing in
this Agreement transfers ownership of Customer Data to Vendor.

"Customer Data" means all data uploaded by Customer or its users to
the Service, excluding Usage Data and Aggregated Data.
```

### Limited Use

```
Vendor shall use Customer Data solely to: (a) provide the Services;
(b) improve the Services (in aggregated, de-identified form);
(c) comply with applicable law. Vendor shall not sell Customer Data
or use it for advertising purposes.
```

### Aggregated/Anonymous Data

```
Vendor may create Aggregated Data derived from Customer Data, provided
such data is de-identified and cannot reasonably identify Customer
or any individual. Vendor may use Aggregated Data for any purpose,
including product improvement and benchmarking.
```

## Industry-Specific Requirements

### HIPAA (Healthcare)

```
If Vendor will access Protected Health Information (PHI), the parties
shall execute a Business Associate Agreement in the form attached
as Exhibit [X].
```

### PCI-DSS (Payment Cards)

```
Vendor shall maintain PCI-DSS Level [1/2] compliance and provide
evidence of such compliance (AOC/ROC) upon request. Vendor shall
not store CVV/CVC data after authorization.
```

### Financial Services (GLBA/SOX)

```
Vendor shall implement safeguards consistent with the Gramm-Leach-Bliley
Act and shall not share Customer's nonpublic personal information
except as necessary to perform the Services.
```

## Liability and Indemnification

### Data Breach Indemnification

```
Vendor shall indemnify Customer from any claims, fines, penalties,
or damages arising from a Personal Data Breach caused by Vendor's
failure to comply with its obligations under this DPA, including
the security measures in Section [X].
```

### Regulatory Fine Allocation

```
Each party shall be responsible for any regulatory fines or penalties
imposed on such party for its own violation of applicable data
protection law. Vendor shall indemnify Customer for fines imposed
on Customer resulting from Vendor's breach of this DPA.
```

### Limitation on Data Protection Liability

```
Notwithstanding the limitation of liability in the Agreement, the
parties agree that: (a) Personal Data Breach liability shall be
capped at [AMOUNT / 24 months fees]; (b) regulatory fines shall
[be included in / excluded from] the cap.
```

## Key Decision Points

1. **Role Determination**: Controller, processor, or joint?
2. **Sub-Processor Consent**: Prior written, notification, or pre-approved?
3. **Breach Notification Timeline**: 24, 48, or 72 hours?
4. **Audit Rights**: Annual, on-request, or third-party attestation only?
5. **Data Transfer Mechanism**: SCCs, adequacy, or other?
6. **Liability Cap for Data**: Same as general cap or higher?
7. **Regulatory Fine Allocation**: Each party's own or indemnified?
8. **Security Standards**: SOC 2, ISO 27001, or other?

## Common Pitfalls

1. **No DPA in place**: GDPR requires written data processing agreement
2. **Unclear roles**: Controller/processor designation ambiguous
3. **No sub-processor controls**: Unlimited sub-processing
4. **Inadequate breach notice**: Timeline too long or vague
5. **No audit rights**: Cannot verify compliance
6. **Missing transfer mechanism**: International transfers without SCCs
7. **Data ownership unclear**: Disputes over customer data rights
8. **Low liability cap for data**: Inadequate protection for breaches

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[confidentiality-taxonomy]] - Protecting data
- [[indemnification-taxonomy]] - Data breach indemnity
- [[limitation-of-liability-taxonomy]] - Data liability caps
- [[data-processing-expected-clauses]] - Full DPA structure
- [[data-protection-examples]] - Real data protection language
- [[data-protection-negotiation]] - Strategic negotiation guidance

**Related Key Provisions** (tech_transactions):
- [[data_agreements.md]] - Conceptual treatment of data processing

**Cognitive Patterns** (apply when analyzing data protection):
- `S1` - Regulatory landscape (GDPR, CCPA, sector regulations)
- `S3` - Multi-domain synthesis (technical data flows + legal)
- `S4` - Systematic risk (data breach, privacy violation risks)
- `S12` - Cross-jurisdictional complexity (data transfer requirements)
