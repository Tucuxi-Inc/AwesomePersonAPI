---
name: maintenance-agreement-expected-clauses
description: >-
  Expected clauses and structure for maintenance, support, and SLA agreements
  including service levels, support tiers, response times, and escalation.
  Use when drafting or reviewing support relationships.
tags:
  - maintenance
  - support
  - sla
  - service-level
  - contract-type
version: '1.0'
confidence_level: HIGH
category: contract_types
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - saas-agreement-expected-clauses
  - warranties-taxonomy
  - termination-taxonomy
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Maintenance & Support Agreement - Expected Clauses

## Overview

Maintenance and support agreements govern ongoing technical support, updates, and service levels for software, hardware, or systems. They may be standalone agreements or incorporated into license/SaaS agreements. This skill documents expected structure and provisions based on analysis of maintenance agreement samples.

## Agreement Types

| Type | Description | Key Features |
|------|-------------|--------------|
| **Software Maintenance** | Updates, patches, bug fixes | Version upgrades, helpdesk |
| **Hardware Maintenance** | Equipment repair/replacement | On-site, depot, parts |
| **SLA** | Service level commitments | Uptime, response times, credits |
| **Managed Services** | Outsourced IT operations | Monitoring, administration |
| **Break/Fix** | Ad-hoc support | Time & materials |

## Standard Structure

### Typical Section Order

1. Definitions
2. Scope of Support Services
3. Service Levels
4. Support Hours and Contacts
5. Issue Classification and Priority
6. Response and Resolution Times
7. Escalation Procedures
8. Exclusions
9. Customer Responsibilities
10. Updates and Upgrades
11. Fees and Payment
12. Term and Renewal
13. Termination
14. General Provisions

## Required Clauses

### 1. Scope of Support

**Must Include**:
- [ ] Covered products/services
- [ ] Types of support provided
- [ ] Support channels
- [ ] What is NOT included

**Example**:
```
Covered Products. This Agreement covers the software products and
versions listed in Exhibit A ("Covered Products").

Support Services. Provider shall provide the following support:
(a) Telephone and email helpdesk support
(b) Remote diagnostic and troubleshooting
(c) Bug fixes and error corrections
(d) Updates, patches, and maintenance releases
(e) Access to online knowledge base and documentation

Exclusions. Support does not include: (a) customizations or
integrations; (b) third-party products; (c) training; (d) on-site
services; (e) issues caused by Customer modifications.
```

### 2. Support Hours and Contacts

**Must Include**:
- [ ] Support hours (business hours vs. 24x7)
- [ ] Time zone
- [ ] Support channels (phone, email, portal)
- [ ] Named contacts (if applicable)

**Example**:
```
Support Hours.
- Standard Support: Monday-Friday, 8:00 AM - 6:00 PM [EST],
  excluding holidays
- Premium Support: 24 hours x 7 days x 365 days

Support Channels.
- Phone: [Number] (Severity 1-2 issues)
- Email: support@vendor.com (all issues)
- Portal: support.vendor.com (all issues, preferred)

Authorized Contacts. Customer shall designate up to [3] authorized
support contacts who may submit support requests.
```

### 3. Issue Classification

**Must Include**:
- [ ] Severity levels
- [ ] Criteria for each level
- [ ] Who determines severity
- [ ] Reclassification process

**Example**:
```
Severity Levels.

Severity 1 (Critical): Production system down; no workaround;
business-critical operations halted.

Severity 2 (High): Major functionality impaired; workaround available
but significantly impacts operations.

Severity 3 (Medium): Moderate functionality impaired; workaround
available; business operations continue with inconvenience.

Severity 4 (Low): Minor issues; cosmetic defects; general questions;
enhancement requests.

Severity Determination. Customer assigns initial severity. Provider
may propose reclassification with justification. Disputes escalate
to management.
```

### 4. Response and Resolution Times

**Must Include**:
- [ ] Response time by severity
- [ ] Resolution/workaround targets
- [ ] Definition of "response"
- [ ] Definition of "resolution"

**Example**:
```
Response Times (during support hours):

| Severity | Initial Response | Status Updates | Resolution Target |
|----------|-----------------|----------------|-------------------|
| Sev 1    | 30 minutes      | Every 2 hours  | 4 hours          |
| Sev 2    | 2 hours         | Daily          | 24 hours         |
| Sev 3    | 8 hours         | Weekly         | 5 business days  |
| Sev 4    | 2 business days | As needed      | Best efforts     |

"Response" means acknowledgment of the issue and assignment of a
support engineer.

"Resolution" means correction of the issue or provision of a
workaround acceptable to Customer.
```

### 5. Escalation Procedures

**Must Include**:
- [ ] Escalation triggers
- [ ] Escalation path
- [ ] Contact information
- [ ] Management escalation

**Example**:
```
Escalation Matrix.

| Level   | Trigger                      | Contact              |
|---------|------------------------------|----------------------|
| Level 1 | Issue opened                 | Support Engineer     |
| Level 2 | Sev 1 > 2 hrs, Sev 2 > 8 hrs | Support Manager      |
| Level 3 | Sev 1 > 4 hrs, Sev 2 > 24 hrs| Director of Support  |
| Level 4 | Sev 1 > 8 hrs                | VP of Engineering    |

Customer may escalate at any time by contacting support@vendor.com
with "ESCALATION" in the subject line.
```

### 6. Service Level Credits

**Must Include**:
- [ ] SLA metrics
- [ ] Measurement methodology
- [ ] Credit calculation
- [ ] Credit cap
- [ ] Claim process

**Example**:
```
Availability SLA. Provider shall maintain [99.9%] availability each
calendar month, calculated as:
(Total Minutes - Unplanned Downtime) / Total Minutes × 100

Service Credits.
| Availability      | Credit (% of monthly fee) |
|-------------------|---------------------------|
| 99.0% - 99.9%     | 10%                       |
| 95.0% - 98.9%     | 25%                       |
| Below 95.0%       | 50%                       |

Maximum Credits. Credits shall not exceed [50%] of monthly fees.

Claim Process. Customer must request credits within [30] days of
the end of the affected month by submitting a support ticket.

Sole Remedy. Service credits are Customer's sole remedy for SLA
failures. Credits may be applied to future invoices; no cash refunds.
```

## Common Clauses

### 7. Updates and Upgrades

```
Updates. Provider shall provide all updates, patches, and maintenance
releases ("Updates") at no additional charge. Updates are mandatory
and shall be installed within [30] days of availability.

Upgrades. Provider may offer major version upgrades ("Upgrades") at
additional cost. Customer is not required to purchase Upgrades;
however, support for older versions may be limited or discontinued.

Version Support. Provider supports the current version and [2] prior
major versions. Support for older versions may be limited to
Severity 1-2 issues only.
```

### 8. Customer Responsibilities

```
Customer shall:
(a) Designate authorized support contacts
(b) Provide accurate and complete information for support requests
(c) Implement Provider-recommended patches and updates
(d) Maintain supported hardware and operating system configurations
(e) Cooperate with Provider's troubleshooting efforts
(f) Provide remote access for diagnostic purposes
(g) Maintain current backups

Failure to meet these responsibilities may affect response times
and Provider's ability to resolve issues.
```

### 9. On-Site Support (if applicable)

```
On-Site Services. If remote support cannot resolve a Severity 1 or 2
issue, Provider shall dispatch a technician to Customer's site within
[24] hours of request.

On-Site Hours. On-site support is available Monday-Friday, 8 AM - 5 PM
local time. After-hours on-site support is available at premium rates.

Customer Access. Customer shall provide Provider's personnel with
reasonable access to facilities, systems, and personnel necessary
to perform on-site services.
```

### 10. Hardware Replacement

```
Replacement Parts. For hardware support, Provider shall provide
replacement parts as follows:
- Same-day replacement for critical components (if requested by 2 PM)
- Next business day for non-critical components

Advance Replacement. For critical components, Provider shall ship
replacement parts before receiving defective parts. Customer shall
return defective parts within [10] days.

Refurbished Parts. Replacement parts may be new or refurbished of
equivalent quality.
```

### 11. Fees and Renewal

```
Fees. Customer shall pay the annual maintenance fee specified in
the Order Form. Fees are due [30] days before the start of each
maintenance term.

Renewal. This Agreement automatically renews for successive [1-year]
terms unless either party provides [60] days notice of non-renewal.

Fee Increases. Upon renewal, fees may increase by up to [X%] per
year. Provider shall notify Customer of fee increases at least
[90] days before renewal.

Reinstatement. If maintenance lapses, Customer may reinstate by
paying: (a) fees for the lapsed period; plus (b) [20%] reinstatement fee.
```

## Optional Clauses

### 12. Dedicated Support

```
Dedicated Resources. Provider shall assign a dedicated Technical
Account Manager (TAM) and priority support queue. TAM shall be
available during business hours and shall coordinate all support
activities.
```

### 13. Preventive Maintenance

```
Provider shall perform preventive maintenance [quarterly], including
system health checks, performance optimization, and security reviews.
Provider shall provide a summary report after each preventive
maintenance session.
```

### 14. Disaster Recovery Support

```
In the event of a disaster affecting Customer's production systems,
Provider shall prioritize Customer's support requests and provide
[24x7] support until systems are restored, regardless of Customer's
support tier.
```

## Red Flags - Missing Elements

| Missing Element | Risk Level | Implication |
|-----------------|------------|-------------|
| No severity definitions | HIGH | Disputes on priority |
| No response times | HIGH | No accountability |
| No escalation path | MEDIUM | Issues stall |
| No SLA credits | MEDIUM | No remedy for failures |
| Vague exclusions | HIGH | Unexpected charges |
| No update policy | MEDIUM | Outdated software |
| No end-of-life policy | HIGH | Surprise discontinuation |
| Missing support hours | MEDIUM | Availability confusion |
| No reinstatement terms | LOW | Cannot resume after lapse |

## Negotiation Priorities

### Customer Priorities
1. **Response times**: Aggressive commitments for Sev 1-2
2. **SLA credits**: Meaningful remedies for failures
3. **Escalation rights**: Direct access to management
4. **Version support**: Long support for current version
5. **Fee predictability**: Caps on annual increases
6. **24x7 for critical**: After-hours support for emergencies
7. **On-site option**: For hardware or critical issues

### Provider Priorities
1. **Exclusions**: Clear scope of what's not covered
2. **Customer obligations**: Required cooperation and access
3. **Severity control**: Input on classification
4. **Credit caps**: Limit exposure for SLA failures
5. **Update requirements**: Customers on current versions
6. **Fee adjustments**: Annual increases permitted
7. **Termination rights**: For payment failures

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[service-levels-taxonomy]] - Availability and response time structures
- [[service-levels-examples]] - Real SLA and support language
- [[service-levels-negotiation]] - SLA negotiation strategies
- [[saas-agreement-expected-clauses]] - SLA in cloud/SaaS context
- [[warranties-taxonomy]] - Maintenance vs. warranty distinction
- [[termination-taxonomy]] - Maintenance renewal and termination
- [[payment-terms-taxonomy]] - Maintenance fee structures
- [[force-majeure-taxonomy]] - SLA exclusions

**Related Key Provisions** (tech_transactions):
- [[service_levels.md]] - Conceptual SLA treatment
- [[warranties_and_disclaimers.md]] - Warranty framework
- [[termination.md]] - Maintenance term management

**Related Transaction Types** (tech_transactions):
- [[software_licensing.md]] - Maintenance with license
- [[saas_licensing_agreements.md]] - Support in SaaS context

**Cognitive Patterns** (apply when reviewing maintenance agreements):
- `S3` - Multi-domain synthesis (technical + service + commercial)
- `S5` - Party dynamics (provider vs. customer expectations)
- `S9` - Due diligence (service quality assessment)
- `S11` - Temporal factors (response times, SLA periods)
- `BI2` - Economic enforceability (SLA credits and remedies)
- `BI3` - Context-aware risk (criticality of supported system)
