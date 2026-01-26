---
name: representations-negotiation
description: >-
  Strategic negotiation guidance for representations and warranties provisions
  including scope, qualifiers, survival, and remedies with cognitive pattern
  and business intelligence integration.
tags:
  - representations
  - warranties
  - negotiation
  - strategy
  - risk-allocation
version: '1.0'
confidence_level: HIGH
category: negotiation_guidance
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - representations-taxonomy
  - representations-examples
  - S3-risk-allocation
  - S5-party-dynamics
  - S2-information-asymmetry
  - BI2-leverage-analysis
skill_tier: strategic
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: negotiation_practice
---

# Representations and Warranties Negotiation Guide

## Strategic Framework

### Cognitive Patterns Applied

| Pattern | Application |
|---------|-------------|
| **S2-information-asymmetry** | Reps allocate risk of unknown facts |
| **S3-risk-allocation** | Reps shift risk to party with knowledge |
| **S5-party-dynamics** | Leverage affects rep scope |
| **S11-precedent-awareness** | Market-standard reps |

### Business Intelligence Applied

| Pattern | Application |
|---------|-------------|
| **BI2-leverage-analysis** | Bargaining power affects scope |
| **BI3-industry-standards** | Standard reps by transaction type |

---

## Representation vs. Warranty

### Key Distinctions

| Aspect | Representation | Warranty |
|--------|---------------|----------|
| **Nature** | Statement of fact | Promise about quality |
| **Timing** | At signing/closing | Ongoing obligation |
| **Breach** | Misrepresentation | Breach of warranty |
| **Remedy** | Rescission, fraud | Damages, cure |
| **Reliance** | Required element | Not required |

### Typical Language

**Representation:**
```
Vendor represents that it has full power and authority to
enter into this Agreement and perform its obligations.
```

**Warranty:**
```
Vendor warrants that the Software will perform substantially
in accordance with the Documentation for 12 months.
```

**Combined (R&W):**
```
Vendor represents and warrants that...
```

---

## Standard Mutual Representations

### Core Mutual Reps

```
MUTUAL REPRESENTATIONS

Each party represents and warrants to the other that:

(a) ORGANIZATION. It is duly organized, validly existing, and
    in good standing under the laws of its jurisdiction.

(b) AUTHORITY. It has full power and authority to execute and
    perform this Agreement.

(c) DUE EXECUTION. This Agreement has been duly executed and
    constitutes a valid and binding obligation.

(d) NO CONFLICT. Execution and performance will not violate
    any law, regulation, or agreement to which it is bound.

(e) LITIGATION. There is no pending or threatened litigation
    that would materially affect its ability to perform.

(f) COMPLIANCE. It will comply with all applicable laws in
    performing its obligations.
```

### Expanded Mutual Reps (Customer Request)

```
Additional mutual representations:

(g) ANTI-CORRUPTION. Neither party has made or will make any
    payment in violation of anti-corruption laws (FCPA, UK
    Bribery Act, etc.).

(h) SANCTIONS. Neither party is a Restricted Party under
    applicable sanctions laws.

(i) FINANCIAL CONDITION. No party is insolvent or subject to
    bankruptcy proceedings.
```

---

## Vendor-Specific Representations

### Customer-Favorable (Broad)

```
VENDOR REPRESENTATIONS

Vendor represents and warrants that:

(a) TITLE. Vendor has good title to the Software and has the
    right to grant the licenses herein.

(b) NO INFRINGEMENT. The Software does not infringe any third-
    party intellectual property rights.

(c) NO MALWARE. The Software is free from viruses, malicious
    code, and undisclosed functionality.

(d) EMPLOYEES. All personnel are properly authorized to work
    and have executed confidentiality agreements.

(e) SECURITY. Vendor maintains industry-standard security
    measures and has not experienced material breaches.

(f) OPEN SOURCE. Vendor has disclosed all open source
    components in the Software.

(g) DATA HANDLING. Vendor will process Customer Data only as
    instructed and in compliance with privacy laws.

(h) FINANCIAL STABILITY. Vendor has adequate resources to
    perform its obligations for the term.
```

### Vendor-Favorable (Narrow)

```
VENDOR REPRESENTATIONS

Vendor represents that:
(a) It has the right to license the Software;
(b) The Software will perform substantially as documented.

ALL OTHER WARRANTIES ARE DISCLAIMED.
```

---

## Customer-Specific Representations

### Standard Customer Reps

```
CUSTOMER REPRESENTATIONS

Customer represents and warrants that:

(a) USE. Customer will use the Software only in accordance
    with the license terms and Documentation.

(b) DATA. Customer has all necessary rights to provide
    Customer Data and to authorize Vendor's processing.

(c) COMPLIANCE. Customer will comply with all applicable laws
    in its use of the Software.

(d) EXPORT. Customer will comply with export control laws and
    will not export the Software to restricted destinations.
```

---

## Qualifiers and Limitations

### Knowledge Qualifiers

**Vendor Position (Narrow Qualifier):**
```
To Vendor's knowledge [as of the Effective Date], the Software
does not infringe any third-party intellectual property rights.

"Knowledge" means the actual knowledge of [named individuals]
after reasonable inquiry.
```

**Customer Position (Broader Knowledge):**
```
"Knowledge" means the actual or constructive knowledge of
the party, including knowledge that would be obtained upon
reasonable inquiry by a person in a similar position.
```

### Materiality Qualifiers

**Adding Materiality:**
```
- "No material breach" (vs. "no breach")
- "Material adverse effect" (vs. "adverse effect")
- "In all material respects" (vs. absolute)
```

**Removing/Limiting Materiality:**
```
For purposes of determining breach, materiality qualifiers
shall be disregarded [after having been considered for
determining whether a breach has occurred].
```

---

## Survival Negotiations

### Survival Periods

| Rep Type | Typical Survival | Rationale |
|----------|------------------|-----------|
| Organization/Authority | 12-24 months | Basic capacity |
| IP/Title | 36 months or longer | Latent discovery |
| Tax | Until statute expires | Statutory period |
| Fraud | Unlimited | Cannot contract away |
| Fundamental | 5+ years | Core deal reps |
| General | 12-24 months | Standard discovery |

### Survival Language

**Customer-Favorable:**
```
SURVIVAL

(a) Fundamental Representations (organization, authority, title,
    no infringement) survive for [5] years.

(b) Tax representations survive until [60] days after expiration
    of applicable statute of limitations.

(c) Fraud-related claims survive indefinitely.

(d) All other representations survive for [24] months.
```

**Vendor-Favorable:**
```
SURVIVAL

All representations survive for [12] months following
termination or expiration. No claim may be brought after
the survival period expires.
```

---

## Remedies for Breach

### Indemnification Linkage

```
BREACH OF REPRESENTATIONS

Breach of any representation or warranty entitles the non-
breaching party to:
(a) Indemnification pursuant to Section [X];
(b) Termination if breach is material and uncured;
(c) All other remedies available at law or equity.

Indemnification for breach of representations is subject to
the limitations in Section [Y], except for:
- Fraud
- Willful misconduct
- Breach of fundamental representations
```

### Caps and Baskets

**M&A Context (Seller Protection):**
```
LIMITATIONS

(a) BASKET. Buyer may not claim for breaches until aggregate
    claims exceed $[X] ("Basket"), then Buyer may claim from
    first dollar.

(b) CAP. Seller's liability for breaches shall not exceed $[Y]
    ("Cap"), except for fundamental reps and fraud.

(c) MINI-BASKET. No claim for individual breaches under $[Z].

(d) SOLE REMEDY. Indemnification is the exclusive remedy for
    breach of representations (except fraud).
```

---

## Sandbagging

### Pro-Sandbagging (Buyer-Favorable)

```
The right to indemnification is not affected by any investigation
or knowledge of the indemnified party before or after closing.
```

### Anti-Sandbagging (Seller-Favorable)

```
No indemnification shall be available for matters actually
known to the indemnified party on or before the closing date.
```

### Neutral/Silent

Most commercial agreements are silent on sandbagging, leaving
the issue to applicable law.

---

## Leverage-Based Negotiation (BI2)

### High Customer Leverage

**Can Demand:**
- Broad representations
- Limited qualifiers
- Long survival periods
- Unlimited fraud carve-out
- No caps on fundamental reps
- Bring-down at closing

### High Vendor Leverage

**Can Maintain:**
- Narrow representations
- Knowledge qualifiers
- Short survival (12 months)
- Aggregate caps
- Basket requirements
- Anti-sandbagging

---

## Transaction Type Variations

### SaaS/Technology License

**Standard Reps:**
- Authority and organization
- Non-infringement
- No malware
- Compliance with laws
- Security practices

**Less Common:**
- Financial stability
- Key person availability
- Insurance coverage

### M&A / Asset Purchase

**Comprehensive Reps:**
- Financial statements
- Taxes
- Contracts
- Litigation
- Employees/benefits
- Environmental
- IP ownership
- Customers/suppliers
- Insurance
- Permits/licenses

### Professional Services

**Focused Reps:**
- Authority
- Personnel qualifications
- Compliance
- Insurance
- No conflicts

---

## Disclosure Schedules

### Schedule Mechanics

```
DISCLOSURE SCHEDULES

(a) QUALIFICATION. Representations are qualified by matters
    disclosed in the Disclosure Schedules.

(b) CROSS-REFERENCE. Disclosure on any Schedule qualifies
    all representations where reasonably apparent.

(c) SPECIFICITY. General disclosures do not qualify specific
    representations.

(d) STANDARD. Disclosure must be sufficient to put a
    reasonable person on notice of the matter disclosed.
```

### Updating Schedules

**Buyer-Favorable:**
```
Schedules may not be updated between signing and closing.
Any matter that would require update constitutes breach.
```

**Seller-Favorable:**
```
Seller may update Schedules through closing. Buyer's remedy
for material updates is termination, not breach claim.
```

---

## Negotiation Scripts

### Customer Seeking Broader Reps

> "We need you to stand behind what you're delivering. Your
> representation that the software doesn't infringe should be
> absolute, not qualified to your knowledge. You have access
> to information about your product that we don't. If there's
> an infringement issue, you're in the best position to know
> and to bear that risk."

### Vendor Limiting Exposure

> "We can represent to what we know, but we can't guarantee
> what third parties might claim. The IP landscape is complex
> and changes constantly. We'll provide an indemnity for
> infringement claims, which gives you actual protection, but
> we need to qualify the representation to our knowledge after
> reasonable inquiry."

### Resolution Approach

> "Let's use a knowledge qualifier, but define knowledge to
> include the actual knowledge of your CTO, VP of Engineering,
> and General Counsel after reasonable inquiry. You'll also
> represent that you've conducted a freedom-to-operate search.
> The indemnity will cover infringement claims regardless of
> knowledge, so you have full protection for third-party claims."

---

## Decision Matrix

| Representation | Qualifier? | Survival | Liability |
|----------------|-----------|----------|-----------|
| Authority | No | 24 months | Uncapped |
| Non-infringement | Knowledge + FTO | 36 months | Uncapped |
| No malware | No | 24 months | General cap |
| Compliance | Generally | 24 months | General cap |
| Financial | Material | 24 months | General cap |

---

## Cross-References

- See also: [[representations-taxonomy]] - Clause structure
- See also: [[representations-examples]] - Real clause language
- See also: [[warranty-negotiation]] - Related warranty terms
- See also: [[indemnification-negotiation]] - Breach remedies
