---
name: acceptance-testing-taxonomy
description: >-
  Comprehensive taxonomy of acceptance testing clauses including acceptance
  criteria, testing procedures, rejection rights, and deemed acceptance.
  Use when drafting or negotiating deliverable acceptance provisions.
tags:
  - acceptance
  - testing
  - deliverables
  - milestones
  - rejection
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - warranties-taxonomy
  - payment-terms-taxonomy
  - services-agreement-expected-clauses
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 3
validation_type: human_validated
source_type: contract_samples
---

# Acceptance Testing Taxonomy

## Overview

Acceptance provisions establish the process by which deliverables are reviewed, tested, and formally accepted or rejected. They define acceptance criteria, testing procedures, and consequences of rejection. This taxonomy catalogs acceptance patterns observed across development, services, and supply agreements.

## Acceptance Models

### A. Formal Acceptance Testing

**Description**: Structured testing period with defined criteria.

```
ACCEPTANCE TESTING
Customer shall have [30] days from delivery to test the Deliverable against
the Acceptance Criteria set forth in Exhibit [X] ("Acceptance Period").

Customer shall provide written notice of acceptance or rejection specifying
any deficiencies. If Customer does not provide notice within the Acceptance
Period, the Deliverable shall be deemed accepted.
```

### B. Milestone-Based Acceptance

**Description**: Progressive acceptance at project milestones.

```
MILESTONE ACCEPTANCE
Deliverables shall be accepted on a milestone basis per the Project Plan.
Upon completion of each milestone, Vendor shall notify Customer. Customer
shall have [15] days to test and accept or reject the milestone deliverables.
Final Acceptance occurs upon acceptance of all milestones.
```

### C. Inspection and Acceptance

**Description**: Physical inspection for tangible goods.

```
INSPECTION
Customer may inspect Goods within [10] days of delivery. Customer may
reject Goods that do not conform to the Specifications. Failure to reject
within the inspection period constitutes acceptance, except for latent
defects discovered within [90] days.
```

### D. Deemed Acceptance

**Description**: Automatic acceptance without explicit action.

```
DEEMED ACCEPTANCE
Deliverables shall be deemed accepted upon the earlier of: (a) Customer's
written acceptance; (b) Customer's use of the Deliverable in a production
environment; (c) expiration of the Acceptance Period without rejection.
```

## Acceptance Criteria

### 1. Objective Criteria

```
ACCEPTANCE CRITERIA
The Deliverable shall be deemed to meet the Acceptance Criteria if it:
(a) conforms to the Specifications in Exhibit [X];
(b) passes all test cases in the Test Plan;
(c) contains no Severity 1 or Severity 2 defects;
(d) achieves the performance benchmarks in Exhibit [Y].
```

### 2. Subjective Criteria (Vendor Risk)

```
The Deliverable shall be accepted in Customer's reasonable judgment.
```

**Note**: Avoid purely subjective criteria; creates uncertainty for vendor.

### 3. Documentation Requirements

```
Acceptance requires delivery of:
(a) complete source code and object code;
(b) user documentation and technical documentation;
(c) test results demonstrating conformance;
(d) certificates of completion for training.
```

## Testing Procedures

### 1. Test Environment

```
TESTING ENVIRONMENT
Vendor shall provide a test environment substantially similar to Customer's
production environment. Customer shall provide reasonable access to
Customer systems necessary for integration testing.
```

### 2. Test Plan

```
TEST PLAN
The parties shall mutually agree on a Test Plan within [15] days of
project commencement. The Test Plan shall include: (a) test cases;
(b) test data; (c) expected results; (d) pass/fail criteria.
```

### 3. Customer Responsibilities

```
CUSTOMER OBLIGATIONS
Customer shall: (a) provide timely access to personnel for testing;
(b) provide test data and test scenarios; (c) respond to defect
resolution within [X] business days; (d) conduct acceptance testing
in good faith.
```

## Rejection and Remediation

### 1. Rejection Notice

```
REJECTION
If the Deliverable fails to meet the Acceptance Criteria, Customer shall
provide written notice specifying: (a) the deficiencies in reasonable
detail; (b) the Acceptance Criteria not met; (c) any test results
demonstrating failure.
```

### 2. Cure Period

```
CURE PERIOD
Upon rejection, Vendor shall have [15] days to correct the deficiencies
and resubmit for acceptance testing. Customer shall have an additional
[10] days to retest. The cure and retest process may repeat [twice]
before other remedies apply.
```

### 3. Remedies for Repeated Failure

```
FAILURE TO CURE
If the Deliverable fails acceptance testing after [3] cure attempts,
Customer may: (a) accept the Deliverable with an equitable price
reduction; (b) require Vendor to engage additional resources at
Vendor's expense; (c) terminate the applicable SOW and receive a
refund of fees paid for the rejected Deliverable.
```

## Payment Tied to Acceptance

### 1. Milestone Payments

```
MILESTONE PAYMENTS
Fees shall be paid upon acceptance of each milestone as follows:
- Project Initiation: 20% upon SOW execution
- Design Complete: 20% upon design acceptance
- Development Complete: 30% upon UAT commencement
- Final Acceptance: 30% upon final acceptance
```

### 2. Holdback

```
HOLDBACK
Customer shall withhold [15%] of the total fees until Final Acceptance.
The holdback shall be paid within [30] days of Final Acceptance.
```

### 3. Acceptance as Payment Trigger

```
Payment for Deliverables is contingent upon acceptance. Vendor shall
invoice upon acceptance, and Customer shall pay within [30] days.
```

## Partial Acceptance

```
PARTIAL ACCEPTANCE
Customer may accept portions of a Deliverable that meet Acceptance
Criteria while rejecting non-conforming portions. Payment shall be
prorated based on accepted portions. Rejected portions shall be
subject to the cure process.
```

## Production Acceptance

```
PRODUCTION ACCEPTANCE
Following initial acceptance, there shall be a Production Acceptance
Period of [30] days during which the Deliverable must perform in
Customer's production environment. Production Acceptance requires
no Severity 1 defects and availability of at least [99%].
```

## Acceptance by Contract Type

| Contract Type | Acceptance Model | Typical Period |
|---------------|-----------------|----------------|
| Custom Software | Formal UAT | 30-60 days |
| Professional Services | Milestone | 10-15 days per milestone |
| Manufacturing | Inspection | 10 days |
| Construction | Substantial completion | Punchlist-based |
| SaaS | Implementation acceptance | 15-30 days |
| Hardware | Inspection + burn-in | 30-90 days |

## Key Decision Points

1. **Acceptance Period**: How long for testing?
2. **Acceptance Criteria**: Objective vs. subjective?
3. **Deemed Acceptance**: What triggers automatic acceptance?
4. **Cure Attempts**: How many chances to fix?
5. **Rejection Detail**: How specific must rejection be?
6. **Payment Linkage**: Fees tied to milestones or final?
7. **Partial Acceptance**: Can Customer accept in part?
8. **Production Period**: Post-acceptance warranty period?
9. **Test Environment**: Who provides and maintains?

## Common Pitfalls

1. **Vague acceptance criteria**: Disputes over whether met
2. **Short acceptance period**: Insufficient testing time
3. **No deemed acceptance**: Customer delays indefinitely
4. **Unlimited cure attempts**: Project never completes
5. **Rejection without detail**: Vendor cannot fix
6. **All-or-nothing acceptance**: Cannot progress on partial
7. **No payment holdback**: Customer loses leverage
8. **Subjective standards**: "Customer satisfaction" disputes

## Sample Provisions

### Balanced Acceptance (Software)
```
ACCEPTANCE
Customer shall test the Deliverable against the Specifications for [30]
days. Customer shall accept or reject in writing. Rejection shall specify
non-conforming items with reasonable detail. Vendor shall cure within
[15] days. After [2] failed cure attempts, Customer may terminate and
receive a pro-rata refund. Failure to respond within the testing period
constitutes acceptance. Use in production constitutes acceptance.
```

### Customer-Favorable
```
Customer may reject Deliverables that do not substantially conform to
the Specifications or that contain any material defects. Customer's
determination of conformance shall be conclusive. Upon repeated failure,
Customer may terminate for cause and pursue all available remedies.
```

### Vendor-Favorable
```
Customer shall test Deliverables within [15] days. Failure to provide
detailed written rejection constitutes acceptance. Rejection requires
identification of specific Specification requirements not met. Vendor's
sole obligation for non-conformance is to use reasonable efforts to cure.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[warranties-taxonomy]] - Post-acceptance warranty
- [[payment-terms-taxonomy]] - Payment upon acceptance
- [[services-agreement-expected-clauses]] - Project delivery context
- [[acceptance-change-notice-examples]] - Real acceptance language
- [[acceptance-testing-negotiation]] - Strategic negotiation guidance

**Cognitive Patterns** (apply when analyzing acceptance testing):
- `S9` - Hierarchical due diligence (prioritize acceptance criteria)
- `S3` - Multi-domain synthesis (technical feasibility of criteria)
- `S5` - Party dynamics (vendor vs. customer on criteria)
- `S11` - Temporal factors (testing periods, cure deadlines)
- `BI2` - Economic enforceability (practical acceptance enforcement)
