---
name: representations-taxonomy
description: >-
  Comprehensive taxonomy of representations and warranties including structure,
  common reps, qualifiers, and remedies for breach. Use when drafting or
  negotiating rep & warranty sections in commercial agreements.
tags:
  - representations
  - warranties
  - reps-and-warranties
  - disclosure
  - bring-down
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - warranties-taxonomy
  - indemnification-taxonomy
  - limitation-of-liability-taxonomy
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 3
validation_type: human_validated
source_type: contract_samples
---

# Representations and Warranties Taxonomy

## Overview

Representations and warranties (R&W) are statements of fact that allocate risk between parties. Representations are assertions about past or present facts; warranties are promises about current or future conditions. Breach may give rise to indemnification claims or termination rights. This taxonomy catalogs R&W patterns observed across commercial agreements.

## Representations vs. Warranties

### Legal Distinction

| Aspect | Representation | Warranty |
|--------|----------------|----------|
| **Nature** | Statement of fact | Promise/guarantee |
| **Timing** | Past or present | Present or continuing |
| **Remedy for Breach** | Rescission, damages | Damages |
| **Knowledge Requirement** | May be qualified | Typically unqualified |
| **Survival** | May expire | Often survive closing |

**Practice Note**: In commercial contracts, "represents and warrants" is typically used together, blending the concepts. The distinction matters more in M&A.

## Standard Representations

### A. Authority and Capacity

```
Each party represents and warrants that:
(a) it is duly organized, validly existing, and in good standing
    under the laws of its jurisdiction of organization;
(b) it has full power and authority to enter into this Agreement
    and perform its obligations hereunder;
(c) the execution and performance of this Agreement has been duly
    authorized by all necessary corporate action;
(d) this Agreement constitutes a legal, valid, and binding obligation
    enforceable in accordance with its terms.
```

### B. No Conflicts

```
Each party represents and warrants that the execution and performance
of this Agreement will not:
(a) violate any law, regulation, or order applicable to such party;
(b) breach any agreement to which such party is bound;
(c) require any consent, approval, or authorization not already obtained.
```

### C. Compliance with Laws

```
Each party represents and warrants that it is in compliance with all
applicable laws, rules, and regulations, and shall maintain such
compliance throughout the term of this Agreement.
```

**Specific Compliance Representations**:
- Anti-bribery/FCPA
- Export controls
- Data protection/privacy
- Industry-specific regulations
- Sanctions/OFAC

### D. Non-Infringement (IP)

```
Vendor represents and warrants that:
(a) the Software does not infringe any patent, copyright, trademark,
    trade secret, or other intellectual property right of any third party;
(b) Vendor has the right to grant the licenses granted hereunder;
(c) Vendor has not received any claim of infringement regarding the Software.
```

### E. No Litigation

```
Each party represents that there is no pending or, to its knowledge,
threatened litigation, arbitration, or administrative proceeding
that would materially affect its ability to perform this Agreement.
```

### F. Financial Condition

```
Vendor represents that: (a) it is not insolvent and is able to pay
its debts as they mature; (b) no bankruptcy or similar proceeding
has been filed or is contemplated.
```

### G. No Debarment

```
Vendor represents that neither it nor any of its principals has been
debarred, suspended, or proposed for debarment by any governmental
authority.
```

## Vendor-Specific Representations

### Software/Technology

```
Vendor represents and warrants that:
(a) the Software will perform substantially in accordance with
    the Documentation;
(b) the Software does not contain any virus, malware, or malicious code;
(c) the Software does not contain any open source code except as
    disclosed in Exhibit [X];
(d) Vendor has implemented industry-standard security measures.
```

### Services

```
Provider represents and warrants that:
(a) Services will be performed by qualified personnel with appropriate
    skills and experience;
(b) Services will be performed in a professional, workmanlike manner;
(c) Provider holds all licenses and certifications required to
    perform the Services.
```

### Data/Privacy

```
Vendor represents and warrants that:
(a) Vendor has implemented appropriate technical and organizational
    measures to protect Personal Data;
(b) Vendor has conducted necessary data protection impact assessments;
(c) Vendor has lawful bases for all Processing of Personal Data;
(d) Vendor will notify Customer of any Data Breach within [72] hours.
```

## Customer-Specific Representations

### Lawful Use

```
Customer represents and warrants that:
(a) Customer's use of the Software will comply with applicable laws;
(b) Customer has obtained all necessary consents from data subjects;
(c) Customer Data does not contain unlawful content.
```

### Authority to Provide Data

```
Customer represents that it has all necessary rights and authority
to provide Customer Data to Vendor and to permit Vendor's use of
such data as contemplated by this Agreement.
```

## Qualifiers and Limitations

### A. Knowledge Qualifiers

**Types of Knowledge Standards**:

| Standard | Definition | Protection Level |
|----------|------------|------------------|
| **Actual knowledge** | What the person actually knows | Lowest for representing party |
| **Knowledge after inquiry** | After reasonable investigation | Moderate |
| **Constructive knowledge** | What person should know | Highest for representing party |

```
"Knowledge" means the actual knowledge of [Name/Title] after
reasonable inquiry of [relevant personnel/direct reports].
```

### B. Materiality Qualifiers

```
Vendor represents that there are no material defects in the Software.

"Material" means a defect that substantially impairs the Software's
functionality for its intended purpose.
```

**Double Materiality Scrub**: Watch for materiality in both rep and indemnification—may over-limit claims.

### C. Disclosure Schedule Exceptions

```
Except as set forth in the Disclosure Schedule, Vendor represents
and warrants that [representation].
```

**Use**: Allows party to disclose known issues while still making general representation.

### D. "To the Best of Knowledge"

```
To Vendor's knowledge, the Software does not infringe any third-party
intellectual property rights.
```

**Effect**: Limits representation to what is actually known; no duty to investigate unless specified.

### E. "As of" Qualifications

```
The representations and warranties in this Section are made as of
the Effective Date and shall be deemed repeated as of each renewal.
```

## Survival and Bring-Down

### Survival Periods

```
The representations and warranties in this Agreement shall survive
[closing/the Effective Date] for a period of [X] months/years.
```

| Rep Type | Typical Survival |
|----------|------------------|
| General reps | 12-24 months |
| Fundamental reps (authority, title) | Indefinite or statute of limitations |
| IP reps | 24-36 months |
| Tax reps | Statute of limitations + 60 days |
| Environmental | 3-6 years |

### Bring-Down Certificate

```
At Closing, Seller shall deliver a certificate confirming that all
representations and warranties are true and correct in all material
respects as of the Closing Date.
```

**Bring-Down Standards**:
- True in all respects (strictest)
- True in all material respects (standard)
- No material adverse change (loosest)

## Remedies for Breach

### Indemnification

```
Vendor shall indemnify Customer for any losses arising from a breach
of Vendor's representations and warranties in Section [X].
```

### Termination Right

```
If any representation or warranty is materially inaccurate, the
non-breaching party may terminate this Agreement upon written notice.
```

### Rescission

```
If any representation was materially false when made, the other party
may rescind this Agreement and recover all amounts paid.
```

## Representations by Contract Type

| Contract Type | Key Representations |
|---------------|-------------------|
| **Software License** | Non-infringement, conformance, no malware |
| **SaaS** | Security, compliance, availability |
| **Services** | Qualified personnel, workmanship, licenses |
| **M&A** | Extensive (financial, legal, operational) |
| **Supply** | Quality, conformance, no defects |
| **Data Processing** | Privacy compliance, security measures |

## Key Decision Points

1. **Scope of Reps**: Comprehensive or limited?
2. **Knowledge Qualifiers**: Actual, constructive, or after inquiry?
3. **Materiality Standards**: Material, material adverse, or unqualified?
4. **Survival Period**: How long do reps survive?
5. **Disclosure Schedules**: Exceptions permitted?
6. **Bring-Down**: Required at renewal or milestones?
7. **Remedy**: Indemnification, termination, or both?
8. **Caps on Rep Breach Claims**: Subject to liability cap?

## Common Pitfalls

1. **Overbroad qualifiers**: Every rep qualified by knowledge/materiality
2. **Missing fundamental reps**: No authority or capacity representation
3. **No survival provision**: Reps expire immediately after signing
4. **Inconsistent remedies**: Rep breach vs. indemnity conflicts
5. **Double materiality**: Materiality in rep AND indemnity threshold
6. **Vague knowledge standard**: Whose knowledge? After what inquiry?
7. **No bring-down**: Reps not confirmed at closing/renewal
8. **Missing IP rep**: No non-infringement representation

## Sample Provisions

### Mutual Representations
```
REPRESENTATIONS AND WARRANTIES
Each party represents and warrants that:
(a) Organization. It is duly organized and validly existing under
    the laws of its jurisdiction of organization.
(b) Authority. It has full power and authority to enter into this
    Agreement and perform its obligations.
(c) No Conflicts. Execution of this Agreement will not breach any
    other agreement or violate any applicable law.
(d) Binding Obligation. This Agreement is a legal, valid, and binding
    obligation enforceable in accordance with its terms.
```

### Vendor Technology Representations
```
Vendor represents and warrants that:
(a) Non-Infringement. The Software does not infringe any third-party
    intellectual property rights.
(b) No Malware. The Software does not contain any virus, trojan,
    worm, or other malicious code.
(c) Conformance. The Software will perform substantially in accordance
    with the Documentation for the Warranty Period.
(d) Open Source. The Software does not contain any open source code
    except as disclosed in Exhibit A.
(e) Security. Vendor maintains industry-standard security measures
    to protect the Software and Customer Data.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[warranties-taxonomy]] - Product/service warranties
- [[indemnification-taxonomy]] - Remedy for rep breach
- [[limitation-of-liability-taxonomy]] - Caps on rep breach claims
- [[representations-examples]] - Real representation language
- [[representations-negotiation]] - Strategic negotiation guidance

**Related Key Provisions** (tech_transactions):
- [[warranties_representations.md]] - Conceptual treatment of representations

**Cognitive Patterns** (apply when analyzing representations):
- `S2` - Information gap identification (what reps to verify?)
- `S3` - Multi-domain synthesis (technical/legal/business reps)
- `S9` - Hierarchical due diligence (materiality of representations)
- `BI3` - Context-aware risk (rep scope vs. risk tolerance)
