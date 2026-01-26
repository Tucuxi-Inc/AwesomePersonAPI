---
name: service-levels-taxonomy
description: >-
  Comprehensive taxonomy of service level agreement (SLA) clauses including
  availability, response times, performance metrics, and remedies.
  Use when drafting or negotiating SLAs in cloud and services agreements.
tags:
  - sla
  - service-level
  - availability
  - uptime
  - credits
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - saas-agreement-expected-clauses
  - maintenance-agreement-expected-clauses
  - limitation-of-liability-taxonomy
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Service Level Agreement Taxonomy

## Overview

Service Level Agreements (SLAs) define measurable performance commitments for services. They include metrics, measurement methodology, exclusions, and remedies for failure. This taxonomy catalogs SLA patterns observed across cloud, SaaS, and managed services agreements.

## Core SLA Metrics

### A. Availability/Uptime

**Standard Availability Formula**
```
Availability % = (Total Minutes - Downtime Minutes) / Total Minutes × 100
```

**Common Availability Tiers**
| Tier | Availability | Downtime/Month | Typical Use |
|------|-------------|----------------|-------------|
| Basic | 99.0% | ~7.2 hours | Dev/test |
| Standard | 99.5% | ~3.6 hours | Business apps |
| Premium | 99.9% | ~43 minutes | Critical systems |
| Enterprise | 99.95% | ~22 minutes | Mission-critical |
| Ultra | 99.99% | ~4.4 minutes | Financial/healthcare |

### B. Response Time (Support)

| Severity | Definition | Typical Response |
|----------|------------|------------------|
| Sev 1 | System down | 15 min - 1 hour |
| Sev 2 | Major impairment | 1-4 hours |
| Sev 3 | Minor impact | 4-8 hours |
| Sev 4 | Low priority | 1-2 business days |

### C. Resolution Time

| Severity | Target Resolution |
|----------|-------------------|
| Sev 1 | 4-8 hours |
| Sev 2 | 24 hours |
| Sev 3 | 3-5 business days |
| Sev 4 | Best efforts |

### D. Performance Metrics

**Application Performance**
- Page load time: < X seconds
- API response time: < X milliseconds
- Transaction throughput: X transactions/second

**Infrastructure Performance**
- CPU utilization: < X%
- Memory utilization: < X%
- Network latency: < X ms
- Storage IOPS: X operations/second

## SLA Structure

### 1. Service Level Commitment

```
SERVICE LEVEL COMMITMENT
Vendor commits to maintain [99.9%] availability of the Service
during each calendar month ("Monthly Uptime Percentage").
```

### 2. Measurement Methodology

```
MEASUREMENT
Availability is measured based on Vendor's monitoring systems.
Uptime is calculated by subtracting total Downtime minutes from
total minutes in the month and dividing by total minutes.

"Downtime" means the Service is not available to Customer, as
determined by Vendor's monitoring. A minute is counted as Downtime
if all attempts to establish a connection fail throughout the minute.
```

### 3. Exclusions from SLA

```
EXCLUSIONS
The following are excluded from Downtime calculations:
(a) Scheduled maintenance (with [24] hours notice);
(b) Emergency maintenance (immediate notice);
(c) Force majeure events;
(d) Issues caused by Customer's equipment, software, or actions;
(e) Third-party services not under Vendor's control;
(f) DNS propagation issues;
(g) Customer's failure to follow documentation;
(h) Alpha/beta features;
(i) Issues during Customer's failure to meet obligations.
```

### 4. Service Credits

```
SERVICE CREDITS
If Monthly Uptime Percentage falls below the commitment, Customer
is eligible for credits as follows:

| Monthly Uptime   | Credit (% of monthly fee) |
|------------------|---------------------------|
| 99.0% - 99.9%    | 10%                       |
| 95.0% - 98.9%    | 25%                       |
| 90.0% - 94.9%    | 50%                       |
| Below 90.0%      | 100%                      |
```

### 5. Credit Request Process

```
CREDIT REQUEST
To receive credits, Customer must submit a request via support
ticket within [30] days of the end of the affected month, including:
(a) "SLA Credit Request" in subject line;
(b) dates and times of unavailability;
(c) description of the service impact.

Vendor shall respond within [15] business days. Credits are applied
to future invoices and are not refundable as cash.
```

### 6. Credit Limitations

```
CREDIT LIMITATIONS
(a) Maximum credits per month: [50%] of monthly fees;
(b) Credits are Customer's sole remedy for SLA failures;
(c) Credits may not be carried forward beyond [12] months;
(d) Credits require Customer to be current on payments;
(e) Credits do not apply if Customer is in breach.
```

## SLA Types by Service

### SaaS/Cloud SLA
- Primary metric: Availability percentage
- Secondary: API response time, throughput
- Measurement: Automated monitoring
- Remedy: Service credits

### Support SLA
- Primary metric: Response time by severity
- Secondary: Resolution time, first-call resolution
- Measurement: Ticket timestamps
- Remedy: Credits or extended support

### Managed Services SLA
- Multiple metrics: Availability, performance, security
- Measurement: Monitoring + reporting
- Remedy: Credits, termination rights

### Hosting/Infrastructure SLA
- Metrics: Network uptime, power uptime, hardware replacement
- Measurement: Provider monitoring
- Remedy: Credits

## Advanced SLA Provisions

### Tiered SLAs by Plan

```
| Plan       | Availability | Support Response | Credits |
|------------|-------------|------------------|---------|
| Basic      | 99.0%       | Next bus. day    | No      |
| Pro        | 99.5%       | 8 hours          | 10%     |
| Enterprise | 99.9%       | 1 hour           | 25%     |
```

### Error Budget Model

```
ERROR BUDGET
Customer's "Error Budget" equals [0.1%] of total minutes per month.
If Downtime exceeds the Error Budget, Vendor shall prioritize
reliability improvements over new features until stability is restored.
```

### SLA Reporting

```
REPORTING
Vendor shall provide monthly SLA reports including:
(a) Actual uptime percentage;
(b) Downtime incidents with root cause;
(c) Support ticket statistics;
(d) Credit eligibility (if any).

Reports are available via [dashboard / email / upon request].
```

### Escalation for Chronic Failures

```
CHRONIC SLA FAILURES
If Monthly Uptime falls below [99%] for [3] consecutive months,
Customer may:
(a) terminate the affected services without penalty; and
(b) receive a pro-rata refund of pre-paid fees.
```

## Key Decision Points

1. **Metric Selection**: What's the primary SLA metric?
2. **Target Level**: 99%, 99.9%, or higher?
3. **Measurement**: Who measures? How?
4. **Exclusions**: What doesn't count as downtime?
5. **Credit Tiers**: How much credit for how much failure?
6. **Credit Cap**: Maximum credits per month?
7. **Claim Process**: How to request credits?
8. **Termination Rights**: Can terminate for chronic failures?
9. **Sole Remedy**: Are credits the exclusive remedy?

## Common Pitfalls

1. **No measurement methodology**: Disputes over what counts
2. **Broad exclusions**: Little actual protection
3. **Low credit amounts**: Minimal incentive for provider
4. **Difficult claim process**: Few customers claim
5. **No chronic failure protection**: Locked in despite poor service
6. **Credits as sole remedy**: No termination right
7. **Provider-measured only**: No independent verification
8. **Vague downtime definition**: Interpretation disputes

## Sample SLA Provisions

### Standard SaaS SLA
```
SERVICE LEVEL AGREEMENT

1. Availability Commitment. Vendor commits to [99.9%] Monthly Uptime.

2. Calculation. Monthly Uptime % =
   (Total Minutes - Downtime) / Total Minutes × 100

3. Exclusions. Scheduled maintenance (24hr notice), Customer-caused
   issues, force majeure, third-party services.

4. Credits.
   - 99.0-99.9%: 10% of monthly fee
   - 95.0-98.9%: 25% of monthly fee
   - Below 95%: 50% of monthly fee
   Maximum credits: 50% per month.

5. Process. Submit credit request within 30 days via support ticket.

6. Sole Remedy. Credits are Customer's exclusive remedy for SLA failures.
```

### Enterprise SLA with Termination
```
1. Commitment. [99.95%] availability, measured 24x7x365.

2. Support Response. Sev 1: 15 min; Sev 2: 1 hour; Sev 3: 4 hours.

3. Credits.
   - Each 0.1% below 99.95%: 5% credit
   - Maximum: 100% of monthly fees

4. Chronic Failure. If availability falls below 99% for 3 consecutive
   months, Customer may terminate and receive full refund of fees
   paid for the current term.

5. Root Cause. Vendor shall provide root cause analysis within
   5 business days of any Sev 1 incident.

6. No Sole Remedy. Credits do not limit Customer's other remedies
   under this Agreement or applicable law.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[saas-agreement-expected-clauses]] - SLA in SaaS context
- [[maintenance-agreement-expected-clauses]] - Support SLAs
- [[limitation-of-liability-taxonomy]] - Credits vs. damages
- [[service-levels-examples]] - Real SLA language from contracts
- [[service-levels-negotiation]] - Strategic negotiation guidance

**Related Key Provisions** (tech_transactions):
- [[service_levels.md]] - Conceptual treatment of SLAs

**Cognitive Patterns** (apply when analyzing SLAs):
- `S3` - Multi-domain synthesis (technical feasibility of SLA commitments)
- `S9` - Hierarchical due diligence (prioritize SLAs by business criticality)
- `BI2` - Economic enforceability (are service credits meaningful?)
- `BI3` - Context-aware risk (SLA tier appropriate for use case?)
