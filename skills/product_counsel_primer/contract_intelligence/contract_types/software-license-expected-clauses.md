---
name: software-license-expected-clauses
description: >-
  Expected clauses and structure for software license agreements including
  perpetual, subscription, and OEM licenses. Use when drafting, reviewing,
  or negotiating software licensing deals.
tags:
  - software-license
  - licensing
  - perpetual-license
  - subscription
  - contract-type
version: '1.0'
confidence_level: HIGH
category: contract_types
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - ip-ownership-taxonomy
  - limitation-of-liability-taxonomy
  - indemnification-taxonomy
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Software License Agreement - Expected Clauses

## Overview

Software License Agreements grant rights to use software without transferring ownership. They may be perpetual (one-time), subscription (recurring), or OEM/embedded. Based on analysis of 500+ license agreement samples, this skill documents expected structure and provisions.

## License Types

### Perpetual License
- One-time fee for indefinite use rights
- May include separate maintenance/support fees
- License survives agreement termination

### Subscription License
- Recurring fees for time-limited use rights
- Typically includes support/updates
- License terminates with subscription

### OEM/Embedded License
- Rights to embed software in licensee's products
- Royalty or per-unit pricing
- Distribution rights included

## Standard Structure

### Typical Section Order

1. Definitions
2. License Grant
3. License Restrictions
4. Delivery and Installation
5. Fees and Payment
6. Support and Maintenance
7. Intellectual Property
8. Confidentiality
9. Warranties and Disclaimers
10. Limitation of Liability
11. Indemnification
12. Term and Termination
13. General Provisions

## Required Clauses

### 1. License Grant

**Must Include**:
- [ ] Scope of license (exclusive/non-exclusive)
- [ ] Permitted users/seats
- [ ] Permitted use cases
- [ ] Territory (if limited)
- [ ] Duration (perpetual/term)

**Example (Perpetual)**:
```
Subject to the terms of this Agreement, Licensor grants Licensee
a non-exclusive, non-transferable, perpetual license to use the
Software in object code form solely for Licensee's internal
business purposes.
```

**Example (Subscription)**:
```
Subject to Licensee's payment of the applicable fees, Licensor
grants Licensee a non-exclusive, non-transferable license to
access and use the Software during the Subscription Term solely
for Licensee's internal business purposes.
```

### 2. License Restrictions

**Must Include**:
- [ ] No reverse engineering/decompilation
- [ ] No modification (or limited modification rights)
- [ ] No sublicensing/transfer
- [ ] No competitive use
- [ ] Usage limits (users, locations, etc.)

**Example**:
```
Licensee shall not: (a) sublicense, sell, lease, or distribute the
Software; (b) modify, translate, or create derivative works of the
Software; (c) reverse engineer, decompile, or disassemble the Software
except as permitted by applicable law; (d) remove any proprietary
notices; (e) use the Software to develop a competing product.
```

### 3. Intellectual Property Ownership

**Must Include**:
- [ ] Licensor retains ownership
- [ ] No transfer of IP rights
- [ ] License-only relationship

**Example**:
```
The Software and all intellectual property rights therein are and
shall remain the exclusive property of Licensor and its licensors.
This Agreement does not transfer any ownership rights to Licensee.
Licensee acquires only the limited license rights expressly granted.
```

### 4. Fees and Payment

**Must Include**:
- [ ] Fee structure (one-time, recurring, usage-based)
- [ ] Payment terms
- [ ] Taxes
- [ ] Late payment consequences

**Example**:
```
Licensee shall pay the license fees set forth in the Order Form.
All fees are due within thirty (30) days of invoice. Fees are
exclusive of taxes. Late payments shall accrue interest at [1.5%]
per month or the maximum legal rate.
```

### 5. Warranty and Disclaimer

**Must Include**:
- [ ] Limited functionality warranty
- [ ] Warranty period
- [ ] Exclusive remedies
- [ ] Disclaimer of implied warranties

**Example**:
```
LIMITED WARRANTY: Licensor warrants that the Software will perform
substantially in accordance with the Documentation for [90] days
from delivery. Licensor's sole obligation is to repair or replace
non-conforming Software.

DISCLAIMER: EXCEPT AS EXPRESSLY SET FORTH ABOVE, THE SOFTWARE IS
PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND. LICENSOR DISCLAIMS
ALL IMPLIED WARRANTIES, INCLUDING MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
```

### 6. Limitation of Liability

**Must Include**:
- [ ] Liability cap (typically license fees)
- [ ] Consequential damages exclusion
- [ ] Carve-outs (indemnification, etc.)

**Example**:
```
EXCEPT FOR INDEMNIFICATION OBLIGATIONS AND BREACHES OF CONFIDENTIALITY,
NEITHER PARTY'S AGGREGATE LIABILITY SHALL EXCEED THE FEES PAID OR
PAYABLE IN THE TWELVE MONTHS PRECEDING THE CLAIM. IN NO EVENT SHALL
EITHER PARTY BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, OR
CONSEQUENTIAL DAMAGES.
```

### 7. IP Indemnification

**Must Include**:
- [ ] Defense obligation
- [ ] Covered IP claims (patents, copyrights)
- [ ] Standard exclusions
- [ ] Mitigation remedies

**Example**:
```
Licensor shall defend Licensee from claims that the Software infringes
any US patent or copyright, and indemnify Licensee for damages awarded.
Licensor may: (a) obtain rights for continued use; (b) modify the
Software; or (c) terminate the license and refund fees paid. This
Section states Licensor's entire liability for IP infringement.
```

## Common Clauses

### 8. Support and Maintenance

**Usually Present**:
```
During the Support Term, Licensor shall provide: (a) telephone and
email support during business hours; (b) error corrections and bug
fixes; (c) updates and new releases at no additional charge.
Support may be renewed annually at Licensor's then-current rates.
```

### 9. Acceptance Testing

**Usually Present** (Especially for custom/enterprise):
```
Licensee shall have [30] days from delivery to test the Software
against the Acceptance Criteria. If the Software fails to meet
the Acceptance Criteria, Licensee shall notify Licensor and
Licensor shall correct the deficiencies within [15] days.
```

### 10. Audit Rights

**Usually Present** (Especially for usage-based):
```
Licensor may audit Licensee's use of the Software no more than
once per year upon reasonable notice. If an audit reveals
underpayment exceeding [5%], Licensee shall pay the underpayment
plus Licensor's reasonable audit costs.
```

### 11. Export Compliance

**Usually Present**:
```
Licensee shall comply with all applicable export laws and shall
not export or re-export the Software to prohibited destinations
or persons without appropriate government authorization.
```

## Optional Clauses

### 12. Source Code Escrow

For mission-critical software:
```
Licensor shall deposit the Source Code with [Escrow Agent] and
maintain current deposits. Licensee may access the Source Code
upon: (a) Licensor's insolvency; (b) Licensor's material breach;
or (c) discontinuation of the Software.
```

### 13. Customization/Professional Services

When customization is included:
```
Licensor shall perform the customization services described in
the Statement of Work. Licensor shall own all Custom Developments.
Licensee shall have a perpetual license to use Custom Developments
as part of the Software.
```

### 14. Third-Party Components

When open source or third-party software is included:
```
The Software may include third-party components subject to separate
license terms. Such components are listed in the Documentation.
Licensee's use of third-party components is subject to their
respective license terms.
```

### 15. Most Favored Customer

For strategic deals:
```
Licensor represents that the fees and terms are no less favorable
than those offered to any other customer for similar products and
volumes. If Licensor offers more favorable terms to another customer,
such terms shall be offered to Licensee.
```

## Red Flags - Missing Elements

| Missing Element | Risk Level | Implication |
|-----------------|------------|-------------|
| No license grant clarity | HIGH | Uncertain usage rights |
| No IP indemnification | HIGH | Licensee bears all IP risk |
| No warranty | MEDIUM | No recourse for defects |
| No limitation of liability | HIGH | Unlimited exposure |
| No support terms | MEDIUM | Uncertainty on updates/fixes |
| No termination rights | HIGH | Cannot exit relationship |
| No source escrow | MEDIUM | Risk if licensor fails |

## Perpetual vs. Subscription Considerations

| Aspect | Perpetual | Subscription |
|--------|-----------|--------------|
| **Fee Structure** | One-time + maintenance | Recurring |
| **License Term** | Indefinite | During subscription |
| **Support** | Separate purchase | Usually included |
| **Updates** | Maintenance-dependent | Usually included |
| **Exit Strategy** | Keep existing version | Lose access at end |
| **Cash Flow** | Front-loaded | Spread over time |
| **Termination** | License survives | License terminates |

## Typical Document Structure

### Simple License (3-5 pages)
1. License Grant
2. Restrictions
3. Fees
4. Warranty/Disclaimer
5. Limitation of Liability
6. Term/Termination
7. General Provisions

### Enterprise License (10-20 pages)
1. Definitions
2. License Grant and Scope
3. Restrictions
4. Delivery and Installation
5. Acceptance Testing
6. Fees and Payment
7. Support and Maintenance
8. Professional Services (if applicable)
9. Intellectual Property
10. Confidentiality
11. Warranties
12. Limitation of Liability
13. Indemnification
14. Term and Termination
15. Audit Rights
16. Export Compliance
17. General Provisions
18. Exhibits (Order Form, SLA, SOW)

## Negotiation Priorities

### Licensor Priorities
1. Clear scope limitations (users, use cases)
2. Strong audit rights
3. Low liability cap (fees paid)
4. Narrow IP indemnification
5. Automatic renewal with price increases

### Licensee Priorities
1. Broad usage rights
2. IP indemnification for all IP types
3. Source code escrow
4. Termination for convenience
5. Strong SLA/support commitments
6. Price protection on renewal

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[ip-ownership-taxonomy]] - IP ownership provisions
- [[limitation-of-liability-taxonomy]] - Liability structures
- [[indemnification-taxonomy]] - IP indemnification patterns
- [[saas-agreement-expected-clauses]] - Cloud software alternative

**Related Transaction Types** (tech_transactions):
- [[software_licensing.md]] - Conceptual software licensing treatment

**Cognitive Patterns** (apply when reviewing software licenses):
- `S3` - Multi-domain synthesis (technical + legal + business)
- `S5` - Party dynamics (licensor vs. licensee leverage)
- `S8` - Scenario planning (usage growth, termination)
- `BI4` - Battle selection (key license terms to focus on)
