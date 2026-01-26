---
name: acceptance-testing-negotiation
description: >-
  Strategic negotiation guidance for acceptance testing provisions including
  criteria, procedures, cure rights, and deemed acceptance with cognitive
  pattern and business intelligence integration.
tags:
  - acceptance
  - testing
  - deliverables
  - negotiation
  - strategy
version: '1.0'
confidence_level: HIGH
category: negotiation_guidance
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - acceptance-testing-taxonomy
  - acceptance-change-notice-examples
  - S9-quality-assurance
  - S5-party-dynamics
  - S3-risk-allocation
  - BI2-leverage-analysis
skill_tier: strategic
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: negotiation_practice
---

# Acceptance Testing Negotiation Guide

## Strategic Framework

### Cognitive Patterns Applied

| Pattern | Application |
|---------|-------------|
| **S9-quality-assurance** | Acceptance defines quality standards |
| **S3-risk-allocation** | Risk of defective deliverables |
| **S5-party-dynamics** | Leverage affects testing rigor |
| **S4-temporal-dynamics** | Testing periods and milestones |

### Business Intelligence Applied

| Pattern | Application |
|---------|-------------|
| **BI2-leverage-analysis** | Bargaining power affects procedures |
| **BI3-industry-standards** | Standard testing approaches |
| **BI5-total-cost-analysis** | Cost of testing vs. defect risk |

---

## Acceptance Framework Components

### Key Variables

| Variable | Customer Position | Vendor Position | Balanced |
|----------|------------------|-----------------|----------|
| Test period | 45-60 days | 10-15 days | 30 days |
| Cure attempts | Unlimited | 1-2 | 2-3 |
| Cure period | 30 days | 7-14 days | 15-30 days |
| Criteria | Detailed in SOW | Documentation | Agreed specs |
| Deemed acceptance | Long period/limited | Short/broad | Reasonable |

---

## Acceptance Criteria Negotiations

### Customer-Favorable (Detailed Criteria)

```
ACCEPTANCE CRITERIA

(a) CRITERIA. Deliverables shall be tested against the
    Acceptance Criteria set forth in Exhibit [X], which include:
    - Functional requirements
    - Performance benchmarks
    - Integration requirements
    - Security standards
    - Documentation completeness

(b) MODIFICATION. Acceptance Criteria may be modified only by
    written agreement of both parties.

(c) STANDARD. Deliverables must substantially conform to ALL
    Acceptance Criteria to pass acceptance testing.
```

### Vendor-Favorable (General Standard)

```
ACCEPTANCE

Deliverables shall be deemed to conform to requirements if they
perform substantially in accordance with the Documentation.

Minor variations from specifications that do not materially
affect functionality do not constitute non-conformance.
```

### Best Practice

```
ACCEPTANCE CRITERIA

Acceptance Criteria shall be:
(a) Documented in writing before work begins;
(b) Objective and measurable where possible;
(c) Tied to specific requirements in the SOW;
(d) Achievable with the agreed scope and timeline.

If Acceptance Criteria are not specified, deliverables shall
conform to the Documentation and industry standards for similar
deliverables.
```

---

## Testing Period Negotiations

### Customer-Favorable (Extended Period)

```
TESTING PERIOD

Customer shall have [45] days from delivery to test Deliverables
against the Acceptance Criteria ("Testing Period").

Testing Period shall be extended by:
(a) Any period during which Deliverables are unavailable due
    to Vendor issues;
(b) Any period during which Vendor is correcting deficiencies;
(c) Any period during which Customer reasonably requires
    clarification from Vendor.
```

### Vendor-Favorable (Short Period)

```
ACCEPTANCE PERIOD

Customer shall complete acceptance testing within [10] business
days of delivery. Testing is limited to verifying conformance
to agreed specifications.
```

### Practical Considerations

| Deliverable Type | Reasonable Period |
|------------------|------------------|
| Simple software | 15-30 days |
| Complex system | 30-60 days |
| Integration project | 45-90 days |
| Custom development | 30-45 days |
| SaaS implementation | 15-30 days |

---

## Rejection and Cure Rights

### Customer-Favorable (Multiple Attempts + Remedies)

```
REJECTION AND CURE

(a) REJECTION. If Deliverables fail testing, Customer shall
    provide written rejection notice specifying in reasonable
    detail the non-conformances.

(b) CURE. Vendor shall correct deficiencies within [15] days
    and resubmit. Customer shall have [15] additional days to
    retest.

(c) REPEATED FAILURE. If Deliverables fail after [2] cure
    attempts, Customer may, at its option:
    (i) Accept with equitable price reduction;
    (ii) Require Vendor to engage additional resources at
         Vendor's expense;
    (iii) Terminate the SOW and receive full refund;
    (iv) Engage third party to complete at Vendor's expense.

(d) CRITICAL DEFECTS. For critical defects preventing core
    functionality, Customer may reject without cure opportunity
    and terminate for material breach.
```

### Vendor-Favorable (Limited Cure)

```
CURE

If Deliverables are rejected:
(a) Vendor shall have [30] days to correct;
(b) Vendor may propose alternative solutions;
(c) If cure fails, Vendor's sole liability is re-performance
    or refund of fees for the rejected Deliverable.
```

---

## Deemed Acceptance

### Customer-Favorable (Narrow)

```
DEEMED ACCEPTANCE

Deliverables shall be deemed accepted only upon:
(a) Customer's written acceptance; or
(b) Use in production for [10] consecutive business days
    after successful completion of acceptance testing.

Expiration of the Testing Period without written acceptance
or rejection does NOT constitute deemed acceptance. Customer
shall provide written acceptance or rejection.

Deemed acceptance does not waive warranty rights or rights
to claim for latent defects.
```

### Vendor-Favorable (Broad)

```
DEEMED ACCEPTANCE

Deliverables are deemed accepted upon:
(a) Customer's written acceptance;
(b) Customer's use in production for any purpose; or
(c) Expiration of the Testing Period without written rejection
    specifying the specific non-conformance.

Failure to provide detailed rejection within the Testing Period
constitutes acceptance.
```

### Balanced Approach

```
DEEMED ACCEPTANCE

(a) TRIGGERS. Deliverables are deemed accepted upon:
    - Customer's written acceptance;
    - Use in production for [5] consecutive business days;
    - Expiration of Testing Period without written rejection.

(b) REJECTION REQUIREMENTS. Rejection must be in writing and
    must identify specific Acceptance Criteria not met.

(c) PRESERVATION OF RIGHTS. Deemed acceptance does not waive:
    - Warranty claims for latent defects;
    - Indemnification rights;
    - Rights arising from fraud or misrepresentation.
```

---

## Partial Acceptance

### Customer Protection

```
PARTIAL ACCEPTANCE

(a) Customer may accept conforming components while rejecting
    non-conforming components.

(b) Partial acceptance does not relieve Vendor of obligations
    for non-accepted components.

(c) Customer shall not be obligated to accept Deliverables that
    cannot function without non-conforming components.

(d) Payment for partially accepted Deliverables shall be
    pro-rated based on relative value.
```

### Vendor Protection

```
INTEGRATED DELIVERABLES

For integrated Deliverables, acceptance or rejection applies
to the integrated whole. Customer may not reject individual
components if the integrated Deliverable substantially conforms.
```

---

## Testing Environment

### Customer Responsibilities

```
TESTING ENVIRONMENT

Customer shall:
(a) Provide suitable test environment within [10] days of
    Vendor's request;
(b) Allocate sufficient personnel for testing;
(c) Provide test data and scenarios;
(d) Document test results and defects found;
(e) Cooperate in defect reproduction.

Delays caused by Customer's failure to meet these obligations
shall extend testing and delivery milestones.
```

### Vendor Responsibilities

```
VENDOR TESTING SUPPORT

Vendor shall:
(a) Provide test scripts and scenarios where applicable;
(b) Support Customer's testing activities;
(c) Respond to defect reports within [2] business days;
(d) Participate in testing status meetings;
(e) Provide Documentation sufficient for testing.
```

---

## Leverage-Based Negotiation (BI2)

### High Customer Leverage

**Can Demand:**
- Extended testing periods (45-60 days)
- Multiple cure attempts
- Full refund + third-party completion
- Narrow deemed acceptance triggers
- Detailed acceptance criteria
- Partial acceptance rights

### High Vendor Leverage

**Can Maintain:**
- Short testing periods (10-15 days)
- Limited cure attempts (1-2)
- Re-performance as sole remedy
- Broad deemed acceptance
- General conformance standard
- All-or-nothing acceptance

---

## Payment Linkage

### Milestone-Based Payment

```
PAYMENT FOR DELIVERABLES

(a) [30%] upon execution (design phase);
(b) [30%] upon delivery for testing;
(c) [30%] upon Customer acceptance;
(d) [10%] upon successful production deployment.

No payment milestone is due until prior milestone is achieved.
```

### Holdback

```
ACCEPTANCE HOLDBACK

Customer may withhold [20%] of Deliverable fees until Final
Acceptance. If Final Acceptance is not achieved within [60]
days of delivery, Customer may deduct costs of correction
from the holdback.
```

---

## Dispute Resolution for Acceptance

### Escalation Process

```
ACCEPTANCE DISPUTES

If parties disagree on whether Deliverables meet Acceptance
Criteria:

(a) TECHNICAL REVIEW. Technical representatives shall meet
    within [5] days to review disputed items.

(b) ESCALATION. If unresolved, escalate to project executives
    within [10] days.

(c) EXPERT DETERMINATION. If still unresolved, parties shall
    appoint a mutually acceptable technical expert. Expert's
    determination is final and binding. Costs split equally
    unless expert finds one party clearly correct (then
    incorrect party pays).
```

---

## Negotiation Scripts

### Customer Seeking Rigorous Testing

> "Given the complexity of this implementation and its importance
> to our operations, we need adequate time to test thoroughly.
> A 15-day testing period isn't realistic for testing all
> integration points and user scenarios. We're asking for 45
> days, with the ability to reject and require cure for any
> material non-conformance."

### Vendor Seeking Faster Acceptance

> "Extended testing periods delay project completion and payment.
> If we've met the agreed specifications, we should be able to
> achieve acceptance quickly. We propose 20 days for testing,
> with clear acceptance criteria defined upfront. We'll provide
> support during testing to resolve any issues quickly."

### Resolution Approach

> "Let's agree on 30 days for acceptance testing, with criteria
> defined in the SOW. You'll have two cure attempts, 15 days
> each. If we still can't achieve acceptance after that, we can
> bring in a neutral technical expert to determine conformance.
> We'll make the first 75% payment on delivery, with the final
> 25% on acceptance."

---

## Decision Matrix

| Deliverable | Testing Period | Cure Attempts | Deemed Acceptance |
|-------------|---------------|---------------|-------------------|
| Simple software | 15-30 days | 2 | Expiration or production use |
| Complex system | 30-60 days | 3 | Written only or extended use |
| Integration | 45-90 days | 2-3 | Production use only |
| Services | N/A | Re-perform | N/A |
| SaaS config | 15-30 days | 2 | Production use |

---

## Cross-References

- See also: [[acceptance-testing-taxonomy]] - Clause structure
- See also: [[acceptance-change-notice-examples]] - Real clause language
- See also: [[warranty-negotiation]] - Post-acceptance warranty
- See also: [[payment-terms-negotiation]] - Payment on acceptance
