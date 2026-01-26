---
name: oem-license-expected-clauses
description: >-
  Expected clauses for OEM and embedded software license agreements including
  bundling rights, branding, support allocation, and royalty structures.
  Use when drafting or reviewing technology embedding arrangements.
tags:
  - oem
  - embedded
  - bundling
  - royalty
  - white-label
  - contract-type
version: '1.0'
confidence_level: HIGH
category: contract_types
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - software-license-expected-clauses
  - ip-ownership-taxonomy
  - warranties-taxonomy
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 3
validation_type: human_validated
source_type: contract_samples
---

# OEM/Embedded License Agreement - Expected Clauses

## Overview

OEM (Original Equipment Manufacturer) license agreements allow a licensee to embed, bundle, or redistribute the licensor's software within the licensee's own products. They differ from end-user licenses in their redistribution rights, branding requirements, and royalty structures. This skill documents expected structure and provisions based on analysis of OEM agreement samples.

## Agreement Models

| Model | Description | Typical Use |
|-------|-------------|-------------|
| **Embedded** | Software integrated into hardware | IoT, appliances, devices |
| **Bundled** | Software packaged with licensee product | Software suites |
| **White Label** | Licensee rebrands as own product | SaaS platforms |
| **Component** | Library/SDK integrated into licensee app | Developer tools |
| **Runtime** | Distributable runtime required by licensee app | Frameworks, engines |

## Standard Structure

### Typical Section Order

1. Definitions
2. License Grant
3. Distribution Rights
4. Branding and Attribution
5. Support Responsibilities
6. Pricing and Royalties
7. Minimum Commitments
8. Intellectual Property
9. Warranties
10. Indemnification
11. Confidentiality
12. Term and Termination
13. General Provisions

## Required Clauses

### 1. Definitions

**Must Include**:
- [ ] Licensed Product definition
- [ ] OEM Product definition
- [ ] End User definition
- [ ] Territory
- [ ] Field of Use

**Example**:
```
DEFINITIONS

"Licensed Software" means [Licensor's] [Product Name] software in
object code form, including Updates provided during the term.

"OEM Product" means Licensee's [product/system/application] into which
the Licensed Software is embedded, integrated, or bundled.

"End User" means a third party who acquires the OEM Product from
Licensee or its authorized distributors for its own use.

"Territory" means [worldwide / specified countries].

"Field of Use" means [specific industry/application type, e.g.,
"industrial automation systems" or "consumer electronics devices"].
```

### 2. License Grant

**Must Include**:
- [ ] Scope of rights
- [ ] Distribution rights
- [ ] Sublicense rights
- [ ] Restrictions

**Example**:
```
LICENSE GRANT

Subject to the terms of this Agreement, Licensor grants Licensee a
non-exclusive [exclusive in Field], non-transferable license to:

(a) Install, copy, and use the Licensed Software internally for
    development and testing of OEM Products;

(b) Reproduce and distribute the Licensed Software solely as embedded
    in or bundled with OEM Products to End Users in the Territory;

(c) Sublicense End Users to use the Licensed Software solely as part
    of and in connection with the OEM Product, subject to license
    terms no less restrictive than this Agreement;

(d) Permit authorized distributors and resellers to distribute
    OEM Products containing the Licensed Software.
```

### 3. Distribution Rights

**Embedding Requirements**:
```
DISTRIBUTION REQUIREMENTS

(a) Integration: The Licensed Software shall be distributed only as
    embedded in or bundled with the OEM Product and shall not be
    distributed separately or as a standalone product.

(b) Value-Add: The OEM Product must provide material functionality
    beyond the Licensed Software such that the Licensed Software
    is not the primary value of the OEM Product.

(c) End User Agreement: Each End User must agree to license terms
    that: (i) restrict use to the OEM Product; (ii) prohibit copying,
    modification, and reverse engineering of the Licensed Software;
    (iii) disclaim warranties and limit liability on behalf of Licensor.

(d) Copy Protection: Licensee shall implement commercially reasonable
    copy protection mechanisms to prevent unauthorized extraction
    or redistribution of the Licensed Software.
```

### 4. Branding and Attribution

**Branding Options**:
```
BRANDING

[Option A - Licensor Branding Required:]
The Licensed Software component shall bear Licensor's trademarks and
branding. OEM Product documentation and packaging shall include:
"Powered by [Licensor Product]" or similar attribution.

[Option B - White Label:]
Licensee may remove Licensor's branding and rebrand the Licensed
Software under Licensee's trademarks. End Users need not be informed
of Licensor's involvement. Licensee shall not use Licensor's
trademarks without prior consent.

[Option C - Co-Branding:]
OEM Product shall display both Licensee's and Licensor's branding.
Trademark usage guidelines are set forth in Exhibit [X].
```

**Attribution Requirements**:
```
ATTRIBUTION
Licensee shall include the following attribution in: (a) OEM Product
documentation; (b) "About" screens; (c) third-party notices file:

"This product includes software developed by [Licensor].
Copyright © [Year] [Licensor]. All rights reserved."
```

### 5. Support Responsibilities

**Tiered Support Model**:
```
SUPPORT

Tier 1 Support (Licensee): Licensee shall provide first-level support
to End Users, including: (a) initial troubleshooting; (b) product
installation assistance; (c) user documentation inquiries;
(d) escalation to Tier 2 when appropriate.

Tier 2 Support (Licensor): Licensor shall provide second-level support
to Licensee (not directly to End Users), including: (a) technical
issue investigation; (b) bug verification and fixes; (c) workarounds
for known issues; (d) escalation to Tier 3.

Tier 3 Support (Licensor): Engineering support for critical defects
and product roadmap issues.

Support Fees: [Included in license fees / $X per year / Per incident].
```

**Training**:
```
TRAINING
Licensor shall provide [X] days of technical training to Licensee's
support personnel at no additional charge. Additional training
available at Licensor's then-current rates.
```

### 6. Pricing and Royalties

**Per-Unit Royalty**:
```
ROYALTIES
Licensee shall pay Licensor a royalty of $[X] per unit of OEM Product
distributed containing the Licensed Software.

Volume Discounts:
- 1-10,000 units: $[X] per unit
- 10,001-50,000 units: $[Y] per unit
- 50,001+ units: $[Z] per unit

Royalties shall be reported and paid [quarterly] within [30] days
after the end of each [quarter]. Reports shall include: units shipped,
by product SKU and territory.
```

**Percentage Royalty**:
```
Licensee shall pay [X%] of Net Revenue from OEM Products.
"Net Revenue" means gross revenue less: (a) returns; (b) taxes;
(c) shipping. Minimum royalty of $[X] per quarter.
```

**Fixed Fee**:
```
Licensee shall pay an annual license fee of $[X], payable in advance.
The fee covers unlimited distribution of OEM Products in the Territory.
```

**Hybrid Model**:
```
Licensee shall pay: (a) an annual platform fee of $[X]; plus
(b) $[Y] per unit for units exceeding [Z] per year.
```

### 7. Minimum Commitments

```
MINIMUM COMMITMENTS
Licensee commits to distribute at least [X] units of OEM Products
containing the Licensed Software during each contract year.

If Licensee fails to meet the minimum, Licensee shall pay Licensor
the royalty that would have been due on the shortfall.

[Exclusive Arrangements:]
If Licensor grants exclusivity, failure to meet minimums for [2]
consecutive years permits Licensor to convert to non-exclusive.
```

### 8. Updates and Maintenance

```
UPDATES
During the term, Licensor shall provide Licensee with Updates
(bug fixes, patches, minor enhancements) at no additional charge.

Upgrades (major new versions) may be licensed separately.

End of Life: Licensor shall provide [24] months notice before
discontinuing support for any version of the Licensed Software.
Licensee may continue distributing existing inventory for [12]
months after discontinuation.
```

### 9. Audit Rights

```
AUDIT
Licensor may audit Licensee's records to verify royalty calculations
upon [30] days notice, no more than annually. Audits shall be
conducted by an independent accountant during business hours.

If audit reveals underpayment exceeding [5%], Licensee shall pay
the underpayment plus Licensor's audit costs. Otherwise, Licensor
bears audit costs.
```

## Common Clauses

### 10. Quality Assurance

```
QUALITY ASSURANCE
Licensee shall: (a) conduct reasonable testing of OEM Products before
distribution; (b) maintain quality standards consistent with industry
practice; (c) promptly notify Licensor of defects in Licensed Software.

Licensor may review OEM Products for compliance with this Agreement
and quality standards. Licensor may require corrections before
distribution if OEM Product materially damages Licensor's reputation.
```

### 11. Warranties

```
LICENSOR WARRANTIES
Licensor warrants that: (a) Licensed Software will substantially
conform to the Documentation for [90] days from delivery; (b) Licensor
has the right to grant the licenses herein; (c) Licensed Software
does not, to Licensor's knowledge, infringe third-party IP rights.

LICENSEE WARRANTIES
Licensee warrants that: (a) OEM Products will comply with applicable
laws; (b) Licensee will not make representations about Licensed
Software inconsistent with Documentation; (c) End User agreements
will include required terms.

DISCLAIMER
EXCEPT AS EXPRESSLY STATED, THE LICENSED SOFTWARE IS PROVIDED "AS IS."
LICENSOR DISCLAIMS ALL IMPLIED WARRANTIES INCLUDING MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.
```

### 12. Indemnification

```
LICENSOR INDEMNIFICATION
Licensor shall defend and indemnify Licensee against claims that
the Licensed Software infringes third-party intellectual property
rights, provided Licensee: (a) notifies Licensor promptly;
(b) grants Licensor control of defense; (c) cooperates as needed.

Licensor may: (a) modify Licensed Software to be non-infringing;
(b) obtain a license; (c) terminate and refund pre-paid royalties.

Licensor is not liable for claims arising from: (a) modifications
by Licensee; (b) combination with non-Licensor products; (c) use
outside licensed scope.

LICENSEE INDEMNIFICATION
Licensee shall indemnify Licensor against claims arising from:
(a) OEM Products (excluding Licensed Software); (b) Licensee's
marketing or distribution; (c) End User use.
```

## Optional Clauses

### 13. Source Code Escrow

```
SOURCE CODE ESCROW
Licensor shall deposit source code for the Licensed Software with
[Escrow Agent]. Source code shall be released to Licensee if:
(a) Licensor discontinues support; (b) Licensor becomes insolvent;
(c) Licensor materially breaches.

Upon release, Licensee may use source code solely to maintain
Licensed Software for existing End Users.
```

### 14. Exclusivity

```
EXCLUSIVITY
During the term, Licensor shall not grant OEM rights to any third
party for [Field of Use] in [Territory], provided Licensee meets
the minimum commitments. Exclusivity terminates if Licensee fails
to meet minimums for [2] consecutive years.
```

### 15. Most Favored Customer

```
MOST FAVORED CUSTOMER
If Licensor offers more favorable terms to another OEM licensee for
substantially similar volume and use, Licensor shall offer such
terms to Licensee upon request.
```

## Red Flags - Missing Elements

| Missing Element | Risk Level | Implication |
|-----------------|------------|-------------|
| No distribution rights | HIGH | Cannot ship product |
| Unclear sublicense rights | HIGH | End User use uncertain |
| No support allocation | MEDIUM | End User complaints |
| Missing EULA requirements | HIGH | Licensor unprotected |
| No audit rights | MEDIUM | Royalty verification impossible |
| Vague branding rules | MEDIUM | Trademark disputes |
| No update commitment | MEDIUM | Stale software |
| Missing indemnification | HIGH | IP claim exposure |

## Key Decision Points

1. **Exclusivity**: Exclusive, co-exclusive, or non-exclusive?
2. **Territory/Field**: Geographic and use restrictions?
3. **Pricing Model**: Per-unit, percentage, or fixed?
4. **Minimum Commitment**: Volume guarantees?
5. **Branding**: Licensor brand, white-label, or co-brand?
6. **Support Model**: Who supports End Users?
7. **Updates**: Included or separate?
8. **Source Code**: Escrow or delivery?
9. **End User Terms**: What must EULA include?
10. **Audit Frequency**: How often and threshold?

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[software-license-expected-clauses]] - Base license terms for OEM context
- [[ip-ownership-taxonomy]] - OEM IP and sublicense structures
- [[ip-ownership-examples]] - Real OEM licensing language
- [[warranties-taxonomy]] - Product and IP warranty provisions
- [[warranty-examples]] - Real warranty and disclaimer language
- [[indemnification-taxonomy]] - OEM IP indemnification
- [[indemnification-examples]] - Real OEM indemnity language
- [[audit-rights-taxonomy]] - Royalty audit provisions
- [[termination-taxonomy]] - OEM relationship termination

**Related Key Provisions** (tech_transactions):
- [[technology_licensing.md]] - Embedded technology licensing
- [[intellectual_property.md]] - OEM IP allocation
- [[indemnification.md]] - OEM IP indemnification

**Related Transaction Types** (tech_transactions):
- [[software_licensing.md]] - Base software license context
- [[embedded_systems.md]] - Embedded software licensing

**Cognitive Patterns** (apply when reviewing OEM licenses):
- `S3` - Multi-domain synthesis (product + legal + commercial)
- `S5` - Party dynamics (licensor vs. OEM leverage)
- `S8` - Scenario planning (volume changes, end of life)
- `S10` - Value creation alignment (royalty structures)
- `BI2` - Economic enforceability (minimum commitments)
- `BI3` - Context-aware risk (end customer exposure)
