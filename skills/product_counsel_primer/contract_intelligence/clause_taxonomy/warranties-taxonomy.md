---
name: warranties-taxonomy
description: >-
  Comprehensive taxonomy of warranty clauses including express warranties,
  implied warranty disclaimers, and warranty remedies. Use when drafting,
  reviewing, or negotiating warranty provisions in commercial agreements.
tags:
  - warranties
  - disclaimer
  - merchantability
  - fitness
  - remedy
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - limitation-of-liability-taxonomy
  - indemnification-taxonomy
  - representations-taxonomy
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Warranties Taxonomy

## Overview

Warranty provisions allocate risk for product/service quality between parties. They include express warranties (affirmative promises), implied warranty disclaimers, and remedies for breach. This taxonomy catalogs warranty patterns observed across commercial technology agreements.

## Warranty Categories

### A. Express Warranties

Affirmative promises about product/service quality or performance.

#### 1. Conformance Warranty

```
Vendor warrants that the Software will perform substantially in
accordance with the Documentation for [ninety (90)] days from
delivery (the "Warranty Period").
```

**Key Elements**:
- "Substantially" qualifier (not perfect conformance)
- Reference to documentation/specifications
- Limited warranty period

#### 2. Performance Warranty (Services)

```
Provider warrants that Services will be performed in a professional,
workmanlike manner consistent with generally accepted industry
standards by qualified personnel.
```

**Variations**:
- "Workmanlike manner" (baseline professional standard)
- "Industry standards" (ties to external benchmark)
- "Reasonable skill and care" (UK formulation)

#### 3. Non-Infringement Warranty

```
Vendor represents and warrants that the Software does not infringe
any patent, copyright, trademark, or trade secret of any third party.
```

**Note**: Often paired with IP indemnification; warranty creates direct claim while indemnity covers third-party claims.

#### 4. Authority/Capacity Warranty

```
Each party represents and warrants that it has full power and
authority to enter into this Agreement and perform its obligations
hereunder.
```

#### 5. Compliance Warranty

```
Vendor warrants that it will comply with all applicable laws,
rules, and regulations in performing the Services.
```

**Specific Compliance Warranties**:
- Export control compliance
- Anti-bribery/FCPA compliance
- Data protection/privacy compliance
- Industry-specific regulations (HIPAA, PCI-DSS)

#### 6. Virus/Malware Warranty

```
Vendor warrants that the Software, at the time of delivery, does
not contain any virus, trojan horse, worm, or other malicious code
designed to damage or disrupt systems.
```

#### 7. Title Warranty

```
Vendor warrants that it has good and marketable title to the
Deliverables, free and clear of all liens and encumbrances.
```

### B. Implied Warranty Disclaimers

Negation of warranties implied by law (UCC, common law).

#### Standard Implied Warranties

| Warranty | Source | Meaning |
|----------|--------|---------|
| **Merchantability** | UCC 2-314 | Goods fit for ordinary purpose |
| **Fitness for Particular Purpose** | UCC 2-315 | Goods fit for buyer's specific use |
| **Non-Infringement** | UCC 2-312 | Title free of IP claims |
| **Quiet Enjoyment** | Common law | Undisturbed use of license |

#### Standard Disclaimer Language

```
EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, VENDOR MAKES NO
WARRANTIES OF ANY KIND, WHETHER EXPRESS, IMPLIED, STATUTORY, OR
OTHERWISE. VENDOR SPECIFICALLY DISCLAIMS ALL IMPLIED WARRANTIES,
INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE, TITLE, AND NON-INFRINGEMENT, TO THE MAXIMUM EXTENT
PERMITTED BY APPLICABLE LAW.
```

**Required Elements**:
- Conspicuous presentation (ALL CAPS or bold)
- Reference to implied warranties by name
- "To the extent permitted by law" qualifier

#### "As Is" Disclaimer

```
THE SOFTWARE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT
WARRANTY OF ANY KIND.
```

**Note**: "As Is" alone may not disclaim all implied warranties; explicit disclaimer language preferred.

### C. Warranty Periods

| Product/Service Type | Typical Period |
|---------------------|----------------|
| Software (perpetual) | 90 days from delivery |
| Software (subscription) | Duration of subscription |
| Professional services | 30-90 days from completion |
| Hardware | 1-3 years from delivery |
| Custom development | 90 days from acceptance |
| SaaS | During subscription term |

### D. Warranty Remedies

#### Exclusive Remedy Clause

```
CUSTOMER'S SOLE AND EXCLUSIVE REMEDY FOR BREACH OF THE FOREGOING
WARRANTY SHALL BE, AT VENDOR'S OPTION: (A) REPAIR OR REPLACEMENT
OF THE NON-CONFORMING SOFTWARE; OR (B) REFUND OF FEES PAID FOR
THE NON-CONFORMING SOFTWARE.
```

**Remedy Options**:
- Repair/correction
- Replacement
- Re-performance (services)
- Refund (partial or full)
- Credit toward future purchases

#### Remedy Hierarchy

```
Vendor shall first attempt to repair non-conforming Software. If
repair is not commercially practicable, Vendor shall replace the
Software. If replacement is not commercially practicable, Vendor
shall refund fees paid.
```

#### Time to Claim

```
Customer must notify Vendor of any warranty claim within [thirty
(30)] days of discovering the non-conformance. Failure to provide
timely notice shall waive the warranty claim.
```

## Warranty Structures by Contract Type

### Software License

**Express Warranties**:
- Conformance to documentation (90 days)
- No material defects
- Media free from defects (if applicable)

**Disclaimers**:
- Full implied warranty disclaimer
- "As Is" for trial/beta versions

**Remedies**:
- Repair, replace, or refund

### SaaS Agreement

**Express Warranties**:
- Service availability (often in SLA)
- Conformance to documentation
- Security/compliance (SOC 2, ISO 27001)

**Disclaimers**:
- Standard implied warranty disclaimer
- No warranty of uninterrupted service

**Remedies**:
- SLA credits
- Repair/correction
- Termination right for material breach

### Professional Services

**Express Warranties**:
- Workmanlike manner
- Industry standards
- Qualified personnel

**Disclaimers**:
- Limited disclaimers (harder to disclaim service quality)

**Remedies**:
- Re-performance
- Fee reduction
- Termination

### Hardware/Equipment

**Express Warranties**:
- Free from defects in materials and workmanship
- Conformance to specifications
- New (not refurbished) unless disclosed

**Disclaimers**:
- Standard implied warranty disclaimer

**Remedies**:
- Repair or replace
- Return/refund

### OEM/Supply Agreements

**Express Warranties**:
- Conformance to specifications
- Free from defects
- Compliance with applicable standards
- No counterfeit parts

**Disclaimers**:
- Often more limited (customer needs protection)

**Remedies**:
- Repair, replace, or refund
- Extended warranty for replacements

## Special Warranty Provisions

### Pass-Through Warranty

```
Vendor shall pass through to Customer all warranties received from
Vendor's suppliers and licensors, to the extent such warranties
are transferable.
```

### Extended Warranty

```
Customer may purchase extended warranty coverage for additional
[one (1) year] periods at Vendor's then-current extended warranty
rates.
```

### Warranty of Quiet Enjoyment

```
Vendor warrants that Customer's use of the Software in accordance
with this Agreement will not be disturbed by any claim of
infringement or other adverse claim.
```

### Epidemic Failure Warranty

```
If defects in the Products affect more than [X%] of units delivered
in any [90-day] period ("Epidemic Failure"), Vendor shall, at its
expense: (a) replace all affected units; (b) conduct root cause
analysis; and (c) implement corrective actions.
```

## Warranty Limitations

### Exclusions from Warranty

```
The warranty does not apply to defects or non-conformance caused by:
(a) modification by anyone other than Vendor;
(b) use outside the scope of the Documentation;
(c) combination with non-Vendor products;
(d) accident, abuse, or misuse;
(e) failure to install updates or patches;
(f) use of other than the current release.
```

### Refurbished/Used Products

```
Refurbished products are warranted for [90] days from delivery.
ALL OTHER WARRANTIES ARE DISCLAIMED FOR REFURBISHED PRODUCTS.
```

### Beta/Trial Products

```
BETA SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
CUSTOMER USES BETA SOFTWARE AT ITS OWN RISK.
```

## Key Decision Points

1. **Express Warranty Scope**: What specific promises are being made?
2. **Warranty Period**: How long does coverage last?
3. **Disclaimer Scope**: Which implied warranties are disclaimed?
4. **Remedy Hierarchy**: Repair first, then replace, then refund?
5. **Exclusive Remedy**: Is the remedy exclusive or cumulative?
6. **Notice Requirements**: How quickly must claims be made?
7. **Exclusions**: What conduct voids the warranty?
8. **Pass-Through**: Are supplier warranties available to customer?

## Common Pitfalls

1. **Inadequate disclaimer language**: Missing "merchantability" or "fitness"
2. **Non-conspicuous disclaimer**: Not in caps or bold; may be unenforceable
3. **Unlimited warranty period**: No time limit on claims
4. **No exclusive remedy**: Customer can pursue full damages
5. **Overbroad exclusions**: Warranty voided for minor issues
6. **Missing repair/replace option**: Immediate refund obligation
7. **No notice requirement**: Stale warranty claims
8. **Conflicting provisions**: Warranty vs. SLA vs. indemnity conflicts

## Sample Provisions

### Balanced Software Warranty
```
LIMITED WARRANTY. Vendor warrants that for [ninety (90)] days from
delivery, the Software will perform substantially in accordance with
the Documentation. Vendor does not warrant that the Software will be
error-free or uninterrupted.

EXCLUSIVE REMEDY. Customer's exclusive remedy for breach of the
foregoing warranty is, at Vendor's option: (a) repair or replacement
of non-conforming Software; or (b) refund of fees paid for such
Software. Customer must report defects within [30] days of discovery.

DISCLAIMER. EXCEPT AS EXPRESSLY SET FORTH ABOVE, THE SOFTWARE IS
PROVIDED "AS IS." VENDOR DISCLAIMS ALL IMPLIED WARRANTIES, INCLUDING
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT,
TO THE MAXIMUM EXTENT PERMITTED BY LAW.
```

### Services Warranty
```
Provider warrants that Services will be performed in a professional,
workmanlike manner consistent with industry standards. If Services
fail to meet this warranty, Customer must notify Provider within
[30] days of performance. Provider's sole obligation is to re-perform
the non-conforming Services at no additional charge. If re-performance
fails to cure the deficiency, Customer may terminate the affected
Statement of Work and receive a refund of fees paid for the deficient
Services.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[limitation-of-liability-taxonomy]] - Warranty remedy limitations
- [[representations-taxonomy]] - Reps vs. warranties distinction
- [[indemnification-taxonomy]] - Third-party claims vs. direct warranty
- [[service-levels-taxonomy]] - SLA as performance warranty
- [[warranty-examples]] - Real warranty language from contracts
- [[warranty-negotiation]] - Strategic negotiation guidance

**Related Key Provisions** (tech_transactions):
- [[warranties_representations.md]] - Conceptual treatment of warranties

**Cognitive Patterns** (apply when analyzing warranties):
- `S3` - Multi-domain synthesis (technical feasibility of warranty)
- `S9` - Hierarchical due diligence (materiality of warranty claims)
- `BI2` - Economic enforceability (warranty remedies vs. damages)
- `BI3` - Context-aware risk (warranty scope vs. risk tolerance)
