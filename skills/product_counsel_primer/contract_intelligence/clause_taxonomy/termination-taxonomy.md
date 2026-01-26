---
name: termination-taxonomy
description: >-
  Comprehensive taxonomy of termination and expiration provisions including
  for-cause, for-convenience, and automatic renewal clauses. Use when drafting
  or negotiating exit rights and end-of-term provisions.
tags:
  - termination
  - expiration
  - term
  - renewal
  - exit-rights
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - limitation-of-liability-taxonomy
  - confidentiality-taxonomy
  - payment-terms-taxonomy
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 3
validation_type: human_validated
source_type: contract_samples
---

# Termination and Term Taxonomy

## Overview

Termination provisions govern how agreements end, including natural expiration, termination for cause, and termination for convenience. These clauses determine exit rights, notice requirements, and post-termination obligations. This taxonomy catalogs patterns observed across 4,900+ contract samples.

## Term Structures

### A. Fixed Term

```
The initial term of this Agreement shall be [one (1) year]
from the Effective Date (the "Initial Term").
```

**Variations**:
- 1-year terms (most common for subscriptions)
- 3-year terms (enterprise software)
- 5+ year terms (strategic partnerships)
- Project completion (services agreements)

### B. Renewal Provisions

**Auto-Renewal (Standard)**
```
This Agreement shall automatically renew for successive [one (1) year]
periods (each, a "Renewal Term") unless either party provides written
notice of non-renewal at least [thirty (30)] days prior to the end of
the then-current term.
```

**Notice Periods**:
- 30 days (common for SaaS)
- 60 days (enterprise software)
- 90 days (long-term contracts)
- 180 days (major commitments)

**No Auto-Renewal**
```
This Agreement shall expire at the end of the Initial Term unless
the parties agree in writing to renew.
```

**Renewal with Price Adjustment**
```
Upon renewal, fees shall increase by [X%] or the Consumer Price
Index increase, whichever is greater.
```

### C. Evergreen / Perpetual Term

```
This Agreement shall continue until terminated by either party
in accordance with Section [X].
```

## Termination Types

### A. Termination for Cause (Breach)

**Standard Material Breach**
```
Either party may terminate this Agreement if the other party
materially breaches this Agreement and fails to cure such breach
within [thirty (30)] days after receiving written notice thereof.
```

**Cure Period Variations**:
- No cure period (immediate termination for specified breaches)
- 15 days (minor/payment breaches)
- 30 days (standard)
- 60 days (complex obligations)
- Cure if curable (catch-all; some breaches incurable)

**Incurable Breach**
```
If such breach is incapable of cure, termination shall be
effective immediately upon notice.
```

**Specified Material Breaches**
```
The following shall constitute material breaches entitling the
non-breaching party to terminate immediately:
(a) breach of confidentiality obligations;
(b) unauthorized use of intellectual property;
(c) failure to pay undisputed amounts within [60] days;
(d) breach of representations and warranties.
```

### B. Termination for Insolvency

```
Either party may terminate this Agreement immediately upon notice
if the other party:
(a) becomes insolvent or admits inability to pay debts as they mature;
(b) makes an assignment for the benefit of creditors;
(c) files or has filed against it a petition in bankruptcy which is
    not dismissed within [60] days;
(d) has a receiver, trustee, or liquidator appointed for substantially
    all of its assets.
```

### C. Termination for Convenience

**Mutual Convenience Right**
```
Either party may terminate this Agreement for any reason or no
reason upon [ninety (90)] days prior written notice to the other party.
```

**Customer-Only Convenience Right**
```
Customer may terminate this Agreement at any time upon [30] days
prior written notice.
```

**Notice Period Considerations**:
- 30 days: Short, high flexibility
- 60-90 days: Standard for subscriptions
- 180 days: Long-term commitments

**Early Termination Fee**
```
If Customer terminates for convenience prior to the end of the
then-current term, Customer shall pay an early termination fee
equal to [50%] of the remaining fees through the end of such term.
```

### D. Termination for Change of Control

```
Either party may terminate this Agreement upon [90] days notice
following a Change of Control of the other party.

"Change of Control" means a merger, acquisition, sale of
substantially all assets, or transfer of more than [50%] of
voting securities to a third party.
```

**Competitor Clause**
```
Customer may terminate immediately if Vendor undergoes a Change
of Control in which the acquiring party is a direct competitor
of Customer.
```

### E. Termination for Non-Performance

**SLA-Based Termination**
```
Customer may terminate if Vendor fails to meet the Service Level
Commitment for [three (3)] consecutive months or [five (5)] months
in any twelve-month period.
```

**Force Majeure Termination**
```
If a Force Majeure Event continues for more than [90] days,
either party may terminate this Agreement upon [30] days notice.
```

## Effect of Termination

### A. Payment Obligations

**Customer Owes Balance**
```
Upon termination, Customer shall pay all amounts due through the
effective date of termination, including fees for services
rendered prior to termination.
```

**Refund on Early Termination**
```
If Vendor terminates for cause, no refund shall be due.
If Customer terminates for cause, Vendor shall refund pre-paid
fees for the period following termination.
If either party terminates for convenience, [Customer shall pay/
Vendor shall refund pro-rata fees for the remaining term].
```

### B. Data Return and Deletion

```
Upon termination, Vendor shall:
(a) make Customer Data available for export in [standard format]
    for [30] days following termination;
(b) upon request, certify deletion of all Customer Data from
    Vendor's systems within [90] days of termination, except
    as required for legal compliance.
```

### C. Transition Assistance

```
Upon termination or expiration, Vendor shall provide reasonable
transition assistance services at Vendor's then-current professional
services rates for up to [90] days following termination.
```

### D. Wind-Down Period

```
Following termination, Customer may continue to access the Service
for [30] days solely for the purpose of exporting Customer Data.
```

## Survival Provisions

### Standard Survival Clause
```
The following provisions shall survive termination or expiration
of this Agreement: Sections [Definitions], [Confidentiality],
[Intellectual Property], [Limitation of Liability], [Indemnification],
[Governing Law], and [General Provisions].
```

### Survival Periods
```
Confidentiality obligations shall survive for [five (5)] years
following termination. All other surviving provisions shall
survive indefinitely.
```

### Accrued Rights
```
Termination shall not affect any accrued rights or obligations
of either party or any provision which expressly or by
implication is intended to survive termination.
```

## Termination by Contract Type

| Contract Type | For Cause | For Convenience | Key Issues |
|---------------|-----------|-----------------|------------|
| **SaaS** | 30-day cure | 30-60 day notice | Data export; auto-renewal |
| **Software License** | 30-day cure | Often restricted | License survival post-term |
| **Services/MSA** | 30-day cure; project-specific | 30-60 day notice | SOW termination; wind-down |
| **NDA** | Rare | N/A (fixed term) | Survival period |
| **Distribution** | 30-60 day cure | 90+ day notice | Inventory sell-off |
| **Supply** | 30-day cure | 180+ day notice | PO completion |

## Key Decision Points

1. **Term Length**: Fixed term or evergreen?
2. **Auto-Renewal**: Yes/no? Notice period?
3. **Cure Period**: 15, 30, or 60 days? Incurable breaches?
4. **Convenience Termination**: Mutual or customer-only? Notice period?
5. **Termination Fee**: Required for early exit?
6. **Data Return**: Format? Timeline? Certification?
7. **Transition Assistance**: Included? Duration? Cost?
8. **Survival**: Which provisions? For how long?
9. **Refund Policy**: Pro-rata or forfeited on termination?

## Common Pitfalls

1. **Silent on convenience termination**: Customer locked in indefinitely
2. **No cure period**: Immediate termination for minor breaches
3. **Auto-renewal trap**: Short notice period; missed deadline
4. **No data return right**: Customer Data trapped post-termination
5. **Ambiguous survival**: Uncertainty on which provisions survive
6. **Missing transition assistance**: No help during migration
7. **Inconsistent refund treatment**: Different rules for different termination types
8. **No insolvency protection**: Bound to insolvent counterparty

## Sample Provisions

### Standard Term and Termination (SaaS)
```
Term. This Agreement commences on the Effective Date and continues
for an initial term of one (1) year. Thereafter, it automatically
renews for successive one-year terms unless either party provides
written notice of non-renewal at least thirty (30) days before the
end of the then-current term.

Termination for Cause. Either party may terminate this Agreement
if the other party materially breaches any provision and fails to
cure such breach within thirty (30) days after written notice.

Termination for Convenience. Customer may terminate this Agreement
at any time for any reason upon thirty (30) days prior written notice.

Effect of Termination. Upon termination: (a) Customer's access to
the Service shall cease; (b) Customer shall pay all fees accrued
through the termination date; (c) Vendor shall make Customer Data
available for export for thirty (30) days; (d) upon request, Vendor
shall certify deletion of Customer Data within ninety (90) days.

Survival. Sections [Confidentiality], [IP Ownership], [Limitation
of Liability], [Indemnification], and [General] shall survive
termination for any reason.
```

### Customer-Favorable Termination
```
Customer may terminate this Agreement: (a) for any reason upon
thirty (30) days notice; (b) immediately upon notice if Vendor
fails to meet the SLA for three consecutive months; (c) immediately
if Vendor experiences a Change of Control to a Customer competitor.

Upon termination by Customer for cause, Vendor shall refund all
pre-paid fees for the period following termination and provide
ninety (90) days of transition assistance at no additional charge.
```

### Vendor-Favorable Termination
```
Customer may terminate only for Vendor's uncured material breach.
Vendor may terminate: (a) for Customer's uncured breach; (b) for
convenience upon sixty (60) days notice.

Upon termination by Vendor for convenience, Vendor shall refund
pre-paid fees pro-rata. Upon termination for Customer's breach,
all fees for the remaining term shall immediately become due and
payable.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[payment-terms-taxonomy]] - Refund and fee treatment
- [[confidentiality-taxonomy]] - Survival of confidentiality
- [[force-majeure-taxonomy]] - Termination for extended force majeure
- [[termination-examples]] - Real termination language from contracts
- [[termination-negotiation]] - Strategic negotiation guidance

**Related Key Provisions** (tech_transactions):
- [[termination_provisions.md]] - Conceptual treatment of termination

**Cognitive Patterns** (apply when analyzing termination):
- `S4` - Systematic risk assessment (termination as risk mitigation)
- `S8` - Scenario-based planning (what happens in exit scenarios?)
- `S11` - Temporal factor integration (cure periods, notice requirements)
- `BI5` - Alternative solutions (exit strategies)
