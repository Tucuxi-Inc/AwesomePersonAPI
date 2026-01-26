---
name: nda-expected-clauses
description: >-
  Expected clauses and structure for non-disclosure agreements (NDAs/MNDAs).
  Use when drafting, reviewing, or negotiating confidentiality agreements
  for due diligence, evaluations, or partnership discussions.
tags:
  - nda
  - non-disclosure
  - confidentiality
  - contract-type
  - agreement-structure
version: '1.0'
confidence_level: HIGH
category: contract_types
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - confidentiality-taxonomy
  - termination-taxonomy
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Non-Disclosure Agreement - Expected Clauses

## Overview

Non-Disclosure Agreements (NDAs) protect confidential information exchanged during business discussions. They may be mutual (both parties exchange information) or unilateral (one party discloses). Based on analysis of 3,300+ NDA samples, this skill documents expected structure and standard provisions.

## Standard NDA Structure

### Typical Section Order

1. Parties and Recitals
2. Definition of Confidential Information
3. Exclusions from Confidential Information
4. Obligations of Receiving Party
5. Permitted Disclosures
6. Compelled Disclosure
7. Ownership / No License
8. Return or Destruction of Materials
9. Term and Termination
10. Remedies (Injunctive Relief)
11. General Provisions

## Required Clauses

### 1. Definition of Confidential Information

**Must Include**:
- [ ] Clear definition of what constitutes Confidential Information
- [ ] Marking/designation requirements (if any)
- [ ] Catch-all provision for information reasonably considered confidential

**Example**:
```
"Confidential Information" means all nonpublic information disclosed
by the Disclosing Party that is designated as confidential or that,
given the nature of the information or the circumstances surrounding
its disclosure, reasonably should be considered confidential.
```

### 2. Standard Exclusions

**Must Include (All Four)**:
- [ ] Public domain (already public or becomes public without breach)
- [ ] Prior knowledge (known before disclosure)
- [ ] Independent development (developed without reference to CI)
- [ ] Third-party receipt (received from unrestricted third party)

**Example**:
```
Confidential Information does not include information that:
(i) is or becomes publicly available without breach of this Agreement;
(ii) was known to Receiving Party prior to disclosure;
(iii) is independently developed without use of Confidential Information;
(iv) is rightfully received from a third party without restriction.
```

### 3. Confidentiality Obligations

**Must Include**:
- [ ] Use restriction (limited to business relationship purpose)
- [ ] Non-disclosure obligation
- [ ] Standard of care (reasonable measures)

**Example**:
```
The Receiving Party shall: (a) use Confidential Information only for
the Purpose; (b) not disclose Confidential Information to any third
party except as permitted herein; (c) protect Confidential Information
using at least the same degree of care it uses for its own confidential
information, but no less than reasonable care.
```

### 4. Permitted Disclosures

**Must Include**:
- [ ] Employees/contractors with need to know
- [ ] Requirement for binding confidentiality obligations
- [ ] Affiliates (if applicable)

**Example**:
```
Receiving Party may disclose Confidential Information to its employees
and contractors who (i) have a need to know for the Purpose, and
(ii) are bound by confidentiality obligations no less protective
than this Agreement.
```

### 5. Term and Survival

**Must Include**:
- [ ] Agreement term
- [ ] Survival period for confidentiality obligations

**Example**:
```
This Agreement shall terminate [three (3)] years from the Effective
Date. The Receiving Party's confidentiality obligations shall survive
for [five (5)] years following termination.
```

## Common Clauses

### 6. Compelled Disclosure

**Usually Present** (Important for litigation/regulatory contexts):
```
Receiving Party may disclose Confidential Information to the extent
required by law or legal process, provided that Receiving Party:
(a) gives Disclosing Party prompt written notice (to the extent
    legally permitted);
(b) cooperates with Disclosing Party's efforts to obtain protective
    treatment; and
(c) discloses only the minimum information required.
```

### 7. No License / Ownership

**Usually Present** (Prevents IP claims):
```
All Confidential Information remains the property of the Disclosing
Party. No license under any intellectual property rights is granted
by this Agreement.
```

### 8. Return/Destruction of Materials

**Usually Present**:
```
Upon termination or request, Receiving Party shall promptly return
or destroy all Confidential Information and provide written
certification of compliance upon request.
```

### 9. Injunctive Relief

**Usually Present** (Protects enforcement rights):
```
Receiving Party acknowledges that breach may cause irreparable harm
for which monetary damages are inadequate. Disclosing Party shall
be entitled to seek injunctive relief without bond.
```

### 10. No Obligation to Proceed

**Usually Present** (Preserves negotiation flexibility):
```
Neither party is obligated to enter into any transaction as a result
of this Agreement or any disclosures hereunder.
```

## Optional Clauses

### 11. Purpose Clause

Limits use to specific business purpose:
```
"Purpose" means the parties' evaluation of a potential business
relationship relating to [description of transaction].
```

### 12. Non-Solicitation

Restricts hiring of disclosed party's employees:
```
During the term and for [12] months thereafter, neither party shall
solicit for employment any employee of the other party who received
or had access to Confidential Information.
```

### 13. Standstill (M&A Context)

Restricts acquisition activity:
```
For [18] months following termination, Company shall not acquire
any securities of Target or seek representation on Target's board
without Target's prior written consent.
```

### 14. Independent Development Acknowledgment

Protects ongoing R&D:
```
Disclosing Party acknowledges that Receiving Party may currently
or in the future be developing information similar to Confidential
Information. Nothing herein restricts such independent development.
```

### 15. Residuals Clause

Permits "head knowledge" retention:
```
Either party may use residuals (information retained in unaided
memory of personnel who had access to Confidential Information)
for any purpose, provided such use does not involve disclosure
of Confidential Information.
```

### 16. Publicity Restrictions

Restricts announcements:
```
Neither party shall disclose the existence of this Agreement or
the discussions contemplated hereby without the other's prior
written consent.
```

## Red Flags - Missing Elements

| Missing Clause | Risk Level | Implication |
|---------------|------------|-------------|
| No exclusions | HIGH | All information is confidential; impractical |
| No standard of care | HIGH | Ambiguous protection level |
| No compelled disclosure | MEDIUM | Trapped between legal obligations |
| No return/destruction | MEDIUM | No mechanism to recover materials |
| No injunctive relief | LOW | May need to post bond for injunction |
| No term/survival | HIGH | Perpetual or uncertain obligations |
| No purpose limitation | MEDIUM | Unlimited use of information |

## Mutual vs. Unilateral

### Mutual NDA (MNDA)

- Both parties disclose and receive
- Reciprocal obligations
- Language: "Each party," "Disclosing Party," "Receiving Party"
- Use for: Technology evaluations, partnerships, M&A

### Unilateral NDA

- One party discloses; one party receives
- One-way obligations
- Language: "Company" (discloser), "Recipient"
- Use for: Vendor evaluation, employment, investor pitch

## NDA by Context

| Context | Key Features |
|---------|--------------|
| **Due Diligence** | Broad definition; standstill; non-solicitation |
| **Technology Evaluation** | Independent development; residuals; no obligation |
| **Partnership Discussion** | Mutual; purpose limitation; publicity restriction |
| **Vendor Evaluation** | Unilateral; vendor as recipient only |
| **Employment** | Unilateral; employee as recipient; often perpetual |
| **Investor Pitch** | Unilateral; startup as discloser; limited exceptions |

## Typical Document Structure

### Simple NDA (1-2 pages)
1. Parties
2. Definition
3. Exclusions
4. Obligations
5. Term
6. Miscellaneous
7. Signatures

### Comprehensive NDA (3-5 pages)
1. Parties and Recitals
2. Definitions (including Affiliates)
3. Confidential Information Definition
4. Exclusions
5. Use and Disclosure Obligations
6. Permitted Recipients
7. Compelled Disclosure
8. Ownership; No License
9. Return/Destruction
10. Term and Survival
11. Injunctive Relief
12. No Obligation to Proceed
13. General Provisions (Governing Law, Entire Agreement, etc.)
14. Signatures

## Negotiation Priorities

### Discloser Priorities
1. Broad definition of Confidential Information
2. Strict marking requirements waived or reduced
3. Long survival period (5-7 years)
4. Robust injunctive relief provision
5. Prohibition on reverse engineering

### Recipient Priorities
1. Clear exclusions (public domain, prior knowledge, etc.)
2. Independent development protection
3. Residuals clause
4. Reasonable survival period (2-3 years)
5. Compelled disclosure protection
6. No non-solicitation or standstill provisions

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[confidentiality-taxonomy]] - Detailed confidentiality clause analysis
- [[termination-taxonomy]] - Term and survival provisions
- [[confidentiality-examples]] - Real NDA language
- [[confidentiality-negotiation]] - Negotiation strategies

**Related Key Provisions** (tech_transactions):
- [[confidentiality_nda.md]] - Conceptual treatment of NDAs

**Cognitive Patterns** (apply when reviewing NDAs):
- `S1` - Stakeholder identification (who needs protection?)
- `S2` - Information gap identification (what's confidential?)
- `S4` - Risk assessment (trade secret vs. general confidential)
- `BI1` - Deal qualification (NDA complexity proportional to deal)
