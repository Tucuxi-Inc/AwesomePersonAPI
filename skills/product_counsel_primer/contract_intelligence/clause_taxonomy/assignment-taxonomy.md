---
name: assignment-taxonomy
description: >-
  Comprehensive taxonomy of assignment and change of control clauses including
  consent requirements, successor obligations, and anti-assignment provisions.
  Use when drafting or negotiating transferability terms.
tags:
  - assignment
  - change-of-control
  - successor
  - transfer
  - anti-assignment
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - termination-taxonomy
  - confidentiality-taxonomy
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 3
validation_type: human_validated
source_type: contract_samples
---

# Assignment and Change of Control Taxonomy

## Overview

Assignment provisions govern whether and how contract rights and obligations can be transferred to third parties. Change of control provisions address what happens when a party's ownership changes. These clauses protect parties from dealing with unintended counterparties. This taxonomy catalogs assignment patterns observed across commercial agreements.

## Core Concepts

### Assignment vs. Delegation
- **Assignment**: Transfer of rights (e.g., right to receive payment)
- **Delegation**: Transfer of duties (e.g., obligation to perform)
- Most provisions cover both but may treat them differently

### Change of Control
- Transfer of ownership/voting control
- Merger, acquisition, sale of substantially all assets
- May trigger consent requirements or termination rights

## Assignment Provisions

### A. Mutual Anti-Assignment (Standard)

```
Neither party may assign or transfer this Agreement, in whole or
in part, without the prior written consent of the other party,
which consent shall not be unreasonably withheld. Any purported
assignment without such consent shall be null and void.
```

### B. Asymmetric Assignment

**Vendor-Favorable**
```
Customer may not assign this Agreement without Vendor's prior written
consent. Vendor may assign this Agreement without restriction.
```

**Customer-Favorable**
```
Vendor may not assign this Agreement without Customer's prior written
consent. Customer may assign this Agreement to an Affiliate or in
connection with a merger, acquisition, or sale of substantially all
assets without Vendor's consent.
```

### C. Permitted Assignments

**Corporate Transaction Exception**
```
Either party may assign this Agreement without consent to: (a) an
Affiliate; or (b) a successor in connection with a merger, acquisition,
or sale of all or substantially all of the assigning party's assets
or business to which this Agreement relates, provided the assignee
agrees in writing to be bound by this Agreement.
```

**Additional Permitted Assignments**
- To financing sources (security interest)
- To parent or subsidiary
- Government contractor novation
- Partnership dissolution

### D. Consent Standards

**Unreasonable Withholding Prohibited**
```
...consent shall not be unreasonably withheld, conditioned, or delayed.
```

**Sole Discretion**
```
...consent may be withheld in such party's sole discretion.
```

**Deemed Consent**
```
If the non-assigning party does not respond within [30] days of
receiving a written request for consent, consent shall be deemed granted.
```

### E. Assignee Requirements

```
Any permitted assignee shall: (a) have the financial capability to
perform the assignor's obligations; (b) agree in writing to be bound
by all terms of this Agreement; (c) not be a competitor of the
non-assigning party.
```

## Change of Control Provisions

### A. Definition of Change of Control

**Broad Definition**
```
"Change of Control" means: (a) a sale, transfer, or other disposition
of all or substantially all of a party's assets; (b) a merger,
consolidation, or other reorganization in which such party is not
the surviving entity or in which its equity holders before the
transaction hold less than [50%] of voting power after; (c) a sale,
transfer, or other disposition of more than [50%] of such party's
voting securities; or (d) a change in the composition of such party's
board such that individuals who were directors at the beginning of
any 12-month period no longer constitute a majority.
```

**Narrow Definition**
```
"Change of Control" means the acquisition by any person or group
of more than [50%] of the voting securities of such party.
```

### B. Change of Control Rights

**Notice Requirement**
```
A party undergoing a Change of Control shall provide the other party
with written notice at least [30/60/90] days prior to the Change of
Control (or, if not permitted under applicable law, promptly after
public announcement).
```

**Consent Requirement**
```
Neither party may undergo a Change of Control without the prior
written consent of the other party. Failure to obtain consent
constitutes a material breach.
```

**Termination Right**
```
Either party may terminate this Agreement upon [90] days written
notice following a Change of Control of the other party.
```

**Competitor Restriction**
```
If [Vendor/Customer] undergoes a Change of Control in which the
acquiring entity is a direct competitor of [Customer/Vendor],
[Customer/Vendor] may terminate this Agreement immediately upon notice.
```

### C. Post-Change of Control Protections

**Confidentiality Concerns**
```
Following a Change of Control of Vendor, Customer may: (a) require
Vendor to demonstrate that Confidential Information will not be
accessible to the acquiring entity; (b) require return of all
Confidential Information; (c) terminate the Agreement.
```

**Price Protection**
```
Fees shall not increase as a result of a Change of Control during
the then-current term.
```

**Service Continuity**
```
Following a Change of Control, successor shall maintain service
levels and support commitments for at least [24] months.
```

## Successors and Assigns Clause

```
SUCCESSORS AND ASSIGNS
This Agreement shall be binding upon and inure to the benefit of
the parties and their respective successors and permitted assigns.
```

**Purpose**: Ensures permitted assignees are bound by and benefit from the agreement.

## Assignment by Contract Type

| Contract Type | Typical Approach |
|---------------|-----------------|
| Software License | Consent required; M&A exception |
| SaaS | Consent required; often vendor-favorable |
| Services | Consent required for both |
| Supply | M&A exception common |
| M&A Agreement | Typically non-assignable |
| NDA | Often freely assignable by discloser |
| Lease | Consent with reasonableness standard |

## Special Provisions

### Novation Requirement

```
No assignment shall relieve the assigning party of its obligations
unless the non-assigning party agrees in writing to a novation
releasing the assignor.
```

### Partial Assignment

```
A party may assign its right to receive payment under this Agreement
without consent. Assignment of any other rights or obligations
requires consent.
```

### Assignment to Financing Sources

```
Customer may assign its rights under this Agreement to a financing
source as security without Vendor's consent, provided Vendor's
obligations and rights are not affected.
```

### Government Contracts

```
Vendor acknowledges that Customer is a federal contractor. Upon
Customer's request, Vendor shall execute a novation agreement in
a form required by applicable government regulations.
```

## Key Decision Points

1. **Consent Required?** Mutual, one-way, or free assignment?
2. **Consent Standard**: Reasonableness or sole discretion?
3. **M&A Exception**: Automatic carve-out for corporate transactions?
4. **Affiliate Exception**: Free assignment within corporate family?
5. **Competitor Restriction**: Block assignment to competitors?
6. **Change of Control**: Define and address separately?
7. **Termination Right**: Exit right on counterparty CoC?
8. **Successor Obligations**: What must assignee commit to?
9. **Novation**: Release of assignor required?

## Common Pitfalls

1. **Silent on assignment**: Common law may permit it
2. **No M&A exception**: Consent required for routine transactions
3. **Vague CoC definition**: Disputes over what triggers rights
4. **No competitor protection**: Confidential info exposed to competitor
5. **Consent "not unreasonably withheld" without more**: Still subjective
6. **No deemed consent**: Endless waiting for response
7. **Missing successors clause**: Assignee may not be bound
8. **Assignor not released**: Original party remains liable

## Sample Provisions

### Standard Mutual
```
ASSIGNMENT
Neither party may assign this Agreement without the prior written
consent of the other party, not to be unreasonably withheld; provided
that either party may assign to: (a) an Affiliate, or (b) a successor
by merger or sale of all or substantially all assets, if the successor
agrees in writing to assume all obligations. Any purported assignment
in violation of this Section is void. This Agreement binds and inures
to the benefit of the parties and their successors and permitted assigns.
```

### Customer-Favorable
```
Vendor may not assign this Agreement without Customer's prior written
consent. Customer may assign this Agreement without consent to
an Affiliate or in connection with a merger, acquisition, or
restructuring. Customer may terminate if Vendor undergoes a Change
of Control to a Customer competitor.
```

### Vendor-Favorable (SaaS)
```
Customer may not assign this Agreement or any rights hereunder
without Vendor's prior written consent. Vendor may assign this
Agreement without restriction. Any assignment by Customer in
violation of this Section shall be void.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[termination-taxonomy]] - Termination rights on CoC
- [[confidentiality-taxonomy]] - Post-CoC confidentiality
- [[assignment-examples]] - Real assignment language from contracts
- [[assignment-negotiation]] - Strategic negotiation guidance

**Cognitive Patterns** (apply when analyzing assignment):
- `S5` - Party dynamics (importance of party identity)
- `S6` - Dynamic framework (ongoing relationship structure)
- `S8` - Scenario planning (M&A, restructuring scenarios)
- `BI4` - Battle selection (when assignment rights matter)
