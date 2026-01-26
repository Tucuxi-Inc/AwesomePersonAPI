---
name: service-levels-examples
description: >-
  Real clause examples for service level provisions including availability
  targets, response times, measurement, credits, and exclusions with
  various party position variations.
tags:
  - sla
  - service-levels
  - availability
  - uptime
  - credits
  - examples
version: '1.0'
confidence_level: HIGH
category: clause_examples
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - service-levels-taxonomy
  - service-levels-negotiation
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Service Level Clause Examples

## Availability SLAs

### Vendor-Favorable (Limited Commitment)

**Example 1 - Target with Exclusions**
```
SERVICE AVAILABILITY

Vendor targets [99.5%] monthly availability for the Service, measured
as the percentage of minutes in a calendar month during which the
Service is operational.

"Downtime" excludes: (a) scheduled maintenance with [24] hours notice;
(b) emergency maintenance; (c) Customer-caused issues; (d) third-party
service failures; (e) Internet connectivity issues; (f) force majeure;
(g) beta or preview features.

Availability is measured by Vendor's monitoring systems. Vendor shall
make reasonable efforts to meet the availability target but makes no
guarantee of uninterrupted service.
```

---

### Customer-Favorable (Strong SLA with Credits)

**Example 2 - Guaranteed Availability with Credits**
```
SERVICE LEVEL AGREEMENT

1. AVAILABILITY COMMITMENT
   Vendor guarantees [99.9%] monthly availability ("Availability SLA").
   "Availability" means the Service is accessible and operational.

2. MEASUREMENT
   Availability = (Total Minutes - Downtime Minutes) / Total Minutes × 100%
   Measured monthly using Vendor's monitoring and Customer-reported incidents.

3. SERVICE CREDITS
   If Vendor fails to meet the Availability SLA:
   - 99.0% - 99.9%: 10% credit of monthly fees
   - 95.0% - 98.9%: 25% credit of monthly fees
   - Below 95.0%:   50% credit of monthly fees

4. CREDIT PROCESS
   Customer shall request credits within [30] days of the end of the
   affected month. Vendor shall apply credits to the next invoice.
   Credits are cumulative but capped at [100%] of monthly fees.

5. CHRONIC FAILURES
   If availability falls below [99%] for [3] consecutive months, Customer
   may terminate without penalty and receive a pro-rata refund.
```

---

## Support Response Times

**Example 3 - Tiered Support SLA**
```
SUPPORT SERVICE LEVELS

| Severity | Description | Response Time | Resolution Target |
|----------|-------------|---------------|-------------------|
| Critical | Service down, no workaround | 1 hour | 4 hours |
| High | Major feature impaired | 4 hours | 1 business day |
| Medium | Feature impaired, workaround exists | 8 hours | 3 business days |
| Low | Minor issue, enhancement request | 2 business days | Best efforts |

"Response Time" means acknowledgment of the issue and assignment to
qualified support personnel.

"Resolution Target" means restoration of service or provision of
workaround. Resolution targets are goals, not guarantees.

Support is available 24x7 for Critical issues; business hours
(8am-6pm ET, Mon-Fri) for other severities.
```

---

## Performance SLAs

**Example 4 - Performance Metrics**
```
PERFORMANCE SERVICE LEVELS

Vendor commits to the following performance metrics:

(a) PAGE LOAD TIME: 95th percentile page load time of [3] seconds
    or less for standard pages.

(b) API RESPONSE TIME: 95th percentile API response time of [500ms]
    or less for standard endpoints.

(c) TRANSACTION THROUGHPUT: Capacity to process [X] transactions
    per second without degradation.

(d) ERROR RATE: Less than [0.1%] error rate for properly formed requests.

Performance is measured from Vendor's data center to the Internet
backbone and excludes network latency outside Vendor's control.
```

---

## Maintenance Windows

**Example 5 - Scheduled Maintenance Terms**
```
MAINTENANCE

(a) SCHEDULED MAINTENANCE: Vendor shall perform scheduled maintenance
    during the maintenance window ([Saturday 2am-6am ET] or as otherwise
    agreed). Vendor shall provide [72] hours advance notice.

(b) EMERGENCY MAINTENANCE: Vendor may perform emergency maintenance
    outside the window if necessary for security or stability.
    Vendor shall provide as much notice as practicable.

(c) MAINTENANCE EXCLUSION: Scheduled maintenance with proper notice
    is excluded from availability calculations. Emergency maintenance
    counts toward downtime unless caused by Customer.

(d) MAINTENANCE FREQUENCY: Scheduled maintenance shall not exceed
    [8] hours per month. Maintenance exceeding this limit counts
    as downtime.
```

---

## Exclusions from SLA

**Example 6 - Comprehensive Exclusions**
```
SLA EXCLUSIONS

The Availability SLA does not apply to downtime caused by:

(a) Scheduled maintenance performed during the maintenance window
    with proper notice;

(b) Customer's equipment, software, or network connectivity;

(c) Customer's failure to follow Vendor's documentation or recommendations;

(d) Customer's unauthorized modification of the Service;

(e) Third-party services, APIs, or integrations not provided by Vendor;

(f) Denial of service attacks or other malicious activity;

(g) Force majeure events;

(h) Suspension of Customer's account for breach or non-payment;

(i) Beta, trial, or proof-of-concept deployments;

(j) Customer exceeding usage limits specified in the Order Form.
```

---

## Credit Mechanics

**Example 7 - Credit Request Process**
```
SERVICE CREDITS

(a) ELIGIBILITY: Service credits are available only if Customer is
    current on all payments and not in breach of the Agreement.

(b) REQUEST: Customer must request credits in writing within [30] days
    of the end of the affected month, specifying the dates and duration
    of downtime.

(c) CALCULATION: Credits are calculated as a percentage of the monthly
    fees for the affected Service.

(d) APPLICATION: Credits will be applied to the next invoice. Credits
    may not be redeemed for cash or transferred.

(e) CAP: Total credits in any month shall not exceed [100%] of that
    month's fees for the affected Service.

(f) SOLE REMEDY: Service credits are Customer's sole and exclusive
    remedy for failure to meet the Service Levels. Credits do not
    apply to fees for professional services or one-time charges.
```

---

## Reporting

**Example 8 - SLA Reporting Requirements**
```
SERVICE LEVEL REPORTING

Vendor shall provide Customer with monthly service level reports
including:

(a) Actual availability percentage and calculation methodology;

(b) Summary of incidents affecting availability, including root cause
    and resolution;

(c) Scheduled and emergency maintenance performed;

(d) Response and resolution times for support requests by severity;

(e) Trend analysis comparing current period to prior periods;

(f) Planned improvements or changes that may affect service levels.

Reports shall be delivered within [10] business days after month end.
Customer may request a quarterly service review meeting to discuss
performance and improvement plans.
```

---

## SLA Review and Updates

**Example 9 - Periodic SLA Review**
```
SLA REVIEW

The parties shall review the Service Levels annually or upon request.

(a) IMPROVEMENT: Vendor shall use reasonable efforts to improve Service
    Levels over time based on technology advancements and feedback.

(b) NO DEGRADATION: Vendor shall not reduce Service Level commitments
    during the Subscription Term without Customer's consent.

(c) CHANGES: Material changes to Service Levels require [90] days
    notice and shall not apply to existing subscription terms unless
    Customer consents.
```

---

## Termination Trigger

**Example 10 - Chronic Failure Rights**
```
TERMINATION FOR SERVICE LEVEL FAILURES

If Vendor fails to meet the Availability SLA:

(a) for [2] consecutive months, Customer may require a remediation
    plan within [15] days;

(b) for [3] consecutive months, Customer may terminate the affected
    Service upon [30] days notice and receive a pro-rata refund of
    pre-paid fees;

(c) for [4] or more months in any [12] month period, Customer may
    terminate the entire Agreement upon [30] days notice and receive
    a pro-rata refund.

Customer's termination right is in addition to, not in lieu of,
any service credits earned.
```

---

## Cross-References

- See also: [[service-levels-taxonomy]] - SLA patterns
- See also: [[saas-agreement-expected-clauses]] - SaaS context
- See also: [[service-levels-negotiation]] - SLA negotiation strategies
