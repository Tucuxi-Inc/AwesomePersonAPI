---
name: escrow-agreement-expected-clauses
description: >-
  Expected clauses for source code and technology escrow agreements including
  deposit requirements, release conditions, and verification procedures.
  Use when drafting or reviewing escrow arrangements for software assets.
tags:
  - escrow
  - source-code
  - technology
  - release-conditions
  - contract-type
version: '1.0'
confidence_level: HIGH
category: contract_types
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - software-license-expected-clauses
  - termination-taxonomy
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 3
validation_type: human_validated
source_type: contract_samples
---

# Source Code Escrow Agreement - Expected Clauses

## Overview

Source code escrow agreements protect licensees by ensuring access to source code if the licensor fails to support the software. A neutral escrow agent holds the source code and releases it to the beneficiary only upon specified triggering events. This skill documents expected structure and provisions based on analysis of escrow agreement samples.

## Parties

- **Depositor**: Software vendor/licensor who owns the source code
- **Beneficiary**: Customer/licensee who needs protection
- **Escrow Agent**: Neutral third party holding the materials

**Common Escrow Agents**: Iron Mountain, NCC Group (Escrow London), PRISM

## Standard Structure

### Typical Section Order

1. Definitions
2. Deposit Obligations
3. Deposit Materials
4. Verification
5. Release Conditions
6. Release Procedures
7. Dispute Resolution
8. License Upon Release
9. Fees
10. Term and Termination
11. Escrow Agent Limitations
12. General Provisions

## Required Clauses

### 1. Deposit Materials

**Must Include**:
- [ ] Definition of deposit materials
- [ ] Source code and documentation
- [ ] Build instructions
- [ ] Third-party components
- [ ] Update requirements

**Example**:
```
DEPOSIT MATERIALS
Depositor shall deposit and maintain in escrow the following materials
("Deposit Materials"):

(a) Complete source code for the Licensed Software, including all
    modules, libraries, and components necessary to compile and build
    the executable version used by Beneficiary;
(b) Build scripts, makefiles, and compilation instructions;
(c) Technical documentation, including architecture documentation,
    API specifications, and database schemas;
(d) A list of all third-party components, tools, and licenses required;
(e) Installation and configuration instructions;
(f) Test suites and test data sufficient to verify functionality.
```

### 2. Deposit Obligations

**Must Include**:
- [ ] Initial deposit timeline
- [ ] Update frequency
- [ ] Version correspondence
- [ ] Certification requirements

**Example**:
```
DEPOSIT REQUIREMENTS

Initial Deposit. Depositor shall make an initial deposit within [30]
days of the Effective Date.

Updates. Depositor shall update the Deposit Materials within [30] days
of any release of a new version of the Licensed Software provided to
Beneficiary, and in any event at least [quarterly/annually].

Certification. With each deposit, Depositor shall certify that the
Deposit Materials: (a) correspond to the version of the Licensed
Software then in use by Beneficiary; (b) are complete and sufficient
to enable a reasonably skilled programmer to compile, maintain, and
support the Licensed Software.
```

### 3. Verification

**Must Include**:
- [ ] Types of verification
- [ ] Verification frequency
- [ ] Cost allocation
- [ ] Failure remediation

**Example**:
```
VERIFICATION

Level 1 (Inventory): Escrow Agent shall verify that deposit contains
files matching Depositor's description.

Level 2 (Technical): Upon Beneficiary's request (no more than annually),
Escrow Agent shall engage a technical reviewer to verify that Deposit
Materials can be compiled into an executable version of the Licensed
Software substantially equivalent to the version used by Beneficiary.

Level 3 (Full Build): Upon Beneficiary's request, a full build and
functional test shall be performed.

Costs. Beneficiary shall pay for Level 2 and Level 3 verifications
unless verification reveals material deficiencies, in which case
Depositor shall pay and promptly cure deficiencies.
```

### 4. Release Conditions

**Must Include**:
- [ ] Triggering events
- [ ] Evidence requirements
- [ ] Cure period (if applicable)

**Example**:
```
RELEASE CONDITIONS
Escrow Agent shall release the Deposit Materials to Beneficiary upon
the occurrence of any of the following ("Release Conditions"):

(a) Depositor files or has filed against it a petition in bankruptcy,
    makes an assignment for the benefit of creditors, or a receiver
    or trustee is appointed for Depositor's business or assets, and
    such proceeding is not dismissed within [60] days;

(b) Depositor discontinues maintenance and support for the Licensed
    Software and fails to resume within [30] days of written notice;

(c) Depositor ceases to conduct business in the ordinary course;

(d) Depositor materially breaches the License Agreement and fails to
    cure within [60] days of written notice;

(e) Depositor is acquired by or merged with a direct competitor of
    Beneficiary and fails to provide assurance of continued support
    within [30] days.
```

### 5. Release Procedures

**Must Include**:
- [ ] Notice requirements
- [ ] Depositor response period
- [ ] Dispute process
- [ ] Release timeline

**Example**:
```
RELEASE PROCEDURES

(a) Beneficiary shall submit a written release request to Escrow Agent
    with evidence of the Release Condition and a copy to Depositor.

(b) Escrow Agent shall notify Depositor of the request within [5]
    business days.

(c) Depositor may dispute the request within [15] business days by
    providing written objection with supporting evidence.

(d) If Depositor does not object within the response period, Escrow
    Agent shall release the Deposit Materials to Beneficiary.

(e) If Depositor disputes, the matter shall be resolved per the
    dispute resolution procedures. Escrow Agent shall hold materials
    pending resolution.
```

### 6. License Upon Release

**Must Include**:
- [ ] Scope of license
- [ ] Permitted uses
- [ ] Restrictions
- [ ] Sublicense rights

**Example**:
```
LICENSE UPON RELEASE
Upon release of the Deposit Materials, Beneficiary shall have a
non-exclusive, royalty-free, perpetual license to:

(a) Use, compile, and execute the source code solely for Beneficiary's
    internal business purposes;
(b) Modify and create derivative works for Beneficiary's internal
    business purposes;
(c) Engage third-party contractors to support the Licensed Software
    on Beneficiary's behalf, provided such contractors are bound by
    confidentiality obligations.

Restrictions: Beneficiary may not: (a) distribute the source code to
third parties except as provided above; (b) use the source code to
develop competitive products; (c) reverse engineer beyond what is
released.
```

## Common Clauses

### 7. Escrow Agent Duties

```
ESCROW AGENT DUTIES
Escrow Agent shall:
(a) Securely store Deposit Materials with appropriate access controls;
(b) Maintain confidentiality of Deposit Materials;
(c) Accept and catalog deposits from Depositor;
(d) Process release requests per this Agreement;
(e) Provide annual statements of account.

Escrow Agent shall have no duty to: (a) verify accuracy or completeness
of deposits unless requested; (b) investigate Release Conditions;
(c) determine the legal validity of claims.
```

### 8. Fees

```
FEES
Annual escrow maintenance fee: $[X] (paid by [Beneficiary/split])
Verification fees: Per Escrow Agent's standard rates
Release processing fee: $[X]

Fees are due upon invoice and are non-refundable.
```

### 9. Multiple Beneficiaries

```
This Agreement is a multi-beneficiary arrangement. Each beneficiary
has independent release rights. Release to one beneficiary does not
affect the rights of other beneficiaries.
```

### 10. Confidentiality

```
Deposit Materials constitute Confidential Information of Depositor.
Escrow Agent and Beneficiary shall maintain confidentiality and
use Deposit Materials only as permitted herein.

Upon release, Beneficiary may disclose source code only to employees
and contractors with a need to know, bound by confidentiality.
```

## Optional Clauses

### 11. Dual Escrow

```
For critical applications, Depositor shall maintain deposits with
two geographically separated escrow agents. Release from either
agent satisfies the release obligation.
```

### 12. SaaS/Hosted Escrow

```
For hosted/SaaS applications, Deposit Materials shall also include:
(a) Database schemas and data export tools;
(b) Configuration and deployment scripts;
(c) Infrastructure documentation;
(d) APIs for data extraction.

Release Conditions shall include: (a) cessation of hosted service;
(b) failure to meet SLA for [90] days.
```

### 13. Automatic Updates

```
Depositor shall configure automated deposit updates through continuous
integration/deployment pipeline integration with Escrow Agent's systems.
```

## Red Flags - Missing Elements

| Missing Element | Risk Level | Implication |
|-----------------|------------|-------------|
| No verification | HIGH | Unusable deposit |
| Narrow release conditions | HIGH | Cannot trigger release |
| Long cure periods | MEDIUM | Extended vulnerability |
| No update requirement | HIGH | Outdated deposit |
| Missing build instructions | HIGH | Cannot compile |
| No third-party disclosure | HIGH | Missing dependencies |
| No license upon release | HIGH | Right to use unclear |
| Depositor veto on release | HIGH | Defeats escrow purpose |

## Key Decision Points

1. **Verification Level**: Inventory, technical, or full build?
2. **Verification Frequency**: Annual or upon major release?
3. **Release Conditions**: Which events trigger release?
4. **Cure Period**: How long can Depositor cure before release?
5. **Dispute Process**: How are disagreements resolved?
6. **License Scope**: What can Beneficiary do with released code?
7. **Update Frequency**: How often must deposits be updated?
8. **Cost Allocation**: Who pays for escrow and verification?

## Sample Provisions

### Release Conditions (Balanced)
```
RELEASE CONDITIONS
Release shall occur upon:
(a) Depositor bankruptcy not dismissed within 60 days;
(b) Discontinuation of support not cured within 30 days;
(c) Material breach of license agreement not cured within 60 days;
(d) Cessation of Depositor's business.

Depositor may object within 15 days of release request. If disputed,
release shall be stayed pending arbitration. Arbitration shall be
completed within 60 days.
```

### Verification (Customer-Favorable)
```
Annual Technical Verification shall be performed at Beneficiary's
expense. Escrow Agent shall verify that Deposit Materials compile
into an executable substantially equivalent to the production version.
If verification fails, Depositor shall cure within 30 days at
Depositor's expense. Repeated failures constitute grounds for release.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[software-license-expected-clauses]] - License context requiring escrow
- [[termination-taxonomy]] - Termination as release trigger
- [[termination-examples]] - Real termination and trigger language
- [[ip-ownership-taxonomy]] - IP rights upon release
- [[confidentiality-taxonomy]] - Source code confidentiality
- [[dispute-resolution-taxonomy]] - Escrow release disputes

**Related Key Provisions** (tech_transactions):
- [[technology_licensing.md]] - License escrow protection
- [[intellectual_property.md]] - Source code IP rights
- [[termination.md]] - Escrow release triggers

**Related Transaction Types** (tech_transactions):
- [[software_licensing.md]] - Escrow in license context
- [[saas_licensing_agreements.md]] - SaaS escrow considerations

**Cognitive Patterns** (apply when reviewing escrow agreements):
- `S4` - Risk assessment (vendor failure scenarios)
- `S6` - Dynamic framework (escrow update requirements)
- `S8` - Scenario planning (release conditions and disputes)
- `S9` - Due diligence (deposit verification)
- `BI3` - Context-aware risk (software criticality)
- `BI5` - Alternative solutions (escrow alternatives)
