---
name: ip-ownership-taxonomy
description: >-
  Comprehensive taxonomy of intellectual property ownership clauses including
  work product, pre-existing IP, license grants, and assignment provisions.
  Use when drafting or negotiating IP rights in technology agreements.
tags:
  - intellectual-property
  - ip-ownership
  - work-product
  - license-grant
  - assignment
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - confidentiality-taxonomy
  - indemnification-taxonomy
  - software-license-expected-clauses
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Intellectual Property Ownership Taxonomy

## Overview

IP ownership provisions determine who owns intellectual property created during a business relationship and who has rights to use pre-existing IP. These clauses are critical in software development, services, and licensing agreements. This taxonomy catalogs patterns observed across 4,900+ contract samples.

## Core Concepts

### Categories of Intellectual Property

**Pre-Existing IP (Background IP)**
IP that existed before the agreement or was developed independently outside the agreement.

**Work Product / Deliverables**
Tangible outputs created during the engagement (code, documents, designs).

**Developments / Inventions**
New IP created during the engagement that may not be explicit deliverables.

**Improvements / Enhancements**
Modifications to pre-existing IP made during the engagement.

**Residuals / Know-How**
Intangible knowledge retained in personnel's memory.

## Ownership Models

### A. Customer Owns Work Product (Work-for-Hire)

```
All Work Product created by Vendor under this Agreement shall be
the sole and exclusive property of Customer. Vendor hereby assigns
to Customer all right, title, and interest in and to such Work
Product, including all intellectual property rights therein.
```

**Characteristics**:
- All deliverables assigned to customer
- Vendor retains no rights (except license-back if negotiated)
- Customer pays premium for full ownership
- Common in: Custom development, consulting

**Vendor License-Back**
```
Customer hereby grants Vendor a non-exclusive, royalty-free,
perpetual license to use Work Product for Vendor's internal
purposes and to provide services to other customers, provided
Vendor does not disclose Customer's Confidential Information.
```

### B. Vendor Owns Work Product (Vendor Retains IP)

```
All Work Product, including all intellectual property rights
therein, shall be the sole and exclusive property of Vendor.
Customer shall have no ownership rights in the Work Product.
```

**Characteristics**:
- Vendor retains ownership of all created IP
- Customer receives license to use deliverables
- Standard for: SaaS, product licensing, templated solutions
- Vendor can reuse and resell

**Customer License Grant**
```
Subject to Customer's payment of fees, Vendor grants Customer
a non-exclusive, non-transferable license to use the Work
Product solely for Customer's internal business purposes.
```

### C. Joint Ownership

```
The parties shall jointly own all Work Product created under
this Agreement. Each party may exploit such Work Product without
the consent of the other, subject to the confidentiality
obligations herein.
```

**Considerations**:
- Complex to administer
- May require consent for licensing to third parties
- Difficult to enforce IP rights (both parties needed)
- Avoid unless genuinely collaborative development

### D. Split Ownership (Hybrid)

```
Customer shall own all Custom Deliverables created specifically
for Customer. Vendor shall own all Tools, Frameworks, and
Methodologies used or developed during the engagement, including
any improvements thereto.

Vendor grants Customer a perpetual license to use such Tools,
Frameworks, and Methodologies solely as incorporated into the
Custom Deliverables.
```

**Characteristics**:
- Customer owns custom work
- Vendor owns reusable components
- Balanced approach for custom development
- Common compromise position

## Key Components

### A. Pre-Existing IP Protection

```
"Pre-Existing IP" means any intellectual property that (a) was
owned by a party before the Effective Date, or (b) is developed
by a party independently and without use of the other party's
Confidential Information.

Each party shall retain ownership of its Pre-Existing IP. No
license to Pre-Existing IP is granted except as expressly set
forth herein.
```

**Identification Methods**:
- Schedule listing pre-existing IP (explicit)
- Definition referencing date of development (implicit)
- Burden of proof provisions

### B. Assignment Language

**Present Assignment (Preferred)**
```
Vendor hereby assigns to Customer all right, title, and interest
in and to the Work Product.
```

**Future Assignment**
```
Vendor agrees to assign to Customer...
```
- Less certain; may require future action
- Present tense assignment preferred

**Assignment of Moral Rights**
```
Vendor waives any moral rights in the Work Product, including
rights of attribution and integrity, to the extent permitted
by applicable law.
```

### C. Work-for-Hire Provisions

**US Copyright Context**
```
To the extent any Work Product constitutes a "work made for hire"
as defined in 17 U.S.C. Section 101, such Work Product is a work
made for hire. To the extent any Work Product does not qualify as
a work made for hire, Vendor hereby assigns all copyright therein
to Customer.
```

**Note**: "Work for hire" has specific legal meaning under US law:
- Must be within enumerated categories, OR
- Specifically ordered/commissioned with written agreement

### D. Further Assurances

```
Vendor shall execute all documents and take all actions reasonably
requested by Customer to perfect, register, and enforce Customer's
rights in the Work Product, including patent and copyright
registration applications.
```

**Power of Attorney**
```
Vendor irrevocably appoints Customer as Vendor's attorney-in-fact
to execute such documents on Vendor's behalf if Vendor fails to
do so within [30] days of request.
```

### E. License Grant Structures

**Exclusive License**
```
Licensor grants Licensee an exclusive license to use the Software
in the Territory. Licensor shall not grant any other party rights
to use the Software in the Territory during the term.
```

**Non-Exclusive License**
```
Licensor grants Licensee a non-exclusive, non-transferable license
to use the Software solely for Licensee's internal business purposes.
```

**Perpetual vs. Term License**
- **Perpetual**: Forever; survives agreement termination
- **Term**: Duration of agreement only; expires on termination

**Sublicense Rights**
```
Licensee may sublicense to its Affiliates and contractors solely
for the purpose of providing services to Licensee.
```

## IP Ownership by Contract Type

| Contract Type | Typical Ownership | Key Issues |
|---------------|-------------------|------------|
| **Custom Development** | Customer owns deliverables | Pre-existing IP carve-out; license-back |
| **SaaS/Software License** | Vendor owns platform | Customer data ownership; customization IP |
| **Consulting/Services** | Split or customer owns | Work product definition; residuals |
| **Joint Development** | Joint or split | Contribution tracking; enforcement rights |
| **OEM/Embedding** | Vendor owns; OEM licenses | Integration IP; derivative works |
| **Open Source** | Community/contributor | Contribution back; license compatibility |

## Special Provisions

### A. Inventions and Patents

```
Vendor shall promptly disclose to Customer any inventions,
discoveries, or improvements conceived or reduced to practice
during the engagement that relate to Customer's business or
the Work Product ("Inventions").

Vendor hereby assigns to Customer all right, title, and interest
in such Inventions, including all patent rights.
```

### B. Source Code Ownership

```
Customer shall own all source code comprising the Custom Deliverables.
Vendor shall deliver such source code to Customer upon completion
of each milestone.
```

**Alternative: Escrow**
```
Vendor shall deposit the source code with [Escrow Agent] pursuant
to the Source Code Escrow Agreement. Customer may access the source
code upon the occurrence of a Release Condition.
```

### C. Customer Data

```
As between the parties, Customer shall own all Customer Data.
Nothing in this Agreement shall grant Vendor any ownership rights
in Customer Data.

"Customer Data" means all data and information submitted by
Customer or its users to the Service.
```

### D. Feedback and Suggestions

```
If Customer provides Vendor with any feedback, suggestions, or
ideas regarding the Service ("Feedback"), Vendor may use such
Feedback without restriction or obligation to Customer.
```

**Alternative: Feedback Assignment**
```
Customer hereby assigns to Vendor all Feedback and waives any
rights therein.
```

### E. Residuals Clause

```
Nothing in this Agreement shall restrict either party from using
general ideas, concepts, know-how, or techniques retained in the
unaided memory of its personnel who have worked on the project,
provided such use does not involve disclosure of the other party's
Confidential Information or infringe the other party's patents
or copyrights.
```

## Key Decision Points

1. **Who owns deliverables?** Customer, vendor, or split?
2. **How is pre-existing IP protected?** Listed in schedule or by definition?
3. **What license-back does vendor need?** None, internal use, or reuse?
4. **Are improvements to pre-existing IP covered?** Who owns enhancements?
5. **Is source code delivered or escrowed?** Access rights if vendor fails?
6. **Who owns customer data?** Always customer (non-negotiable for customer)
7. **How is feedback handled?** Free use by vendor or restricted?
8. **Are moral rights addressed?** Waiver where applicable?

## Common Pitfalls

1. **Ambiguous ownership language**: "Shall be owned" vs. "hereby assigns"
2. **Missing pre-existing IP protection**: Vendor's tools inadvertently assigned
3. **No license-back for vendor**: Vendor cannot service other customers
4. **Overlooking improvements**: Unclear who owns enhancements to background IP
5. **No further assurances clause**: Cannot enforce assignment
6. **Residuals clause too broad**: Undermines IP protection
7. **Missing source code delivery/escrow**: Customer stranded if vendor fails
8. **No feedback clause**: Uncertainty over customer suggestions

## Sample Provisions

### Customer Owns (Full Assignment)
```
All Work Product created by Vendor under this Agreement is "work
made for hire" to the extent permitted by law. To the extent any
Work Product is not work made for hire, Vendor hereby irrevocably
assigns to Customer all right, title, and interest in such Work
Product, including all intellectual property rights. Vendor shall
execute all documents and take all actions to perfect Customer's
rights. Vendor retains no rights to the Work Product except as
expressly licensed herein.
```

### Vendor Owns with Customer License
```
Vendor and its licensors own all right, title, and interest in the
Service, Software, and all improvements thereto. Subject to Customer's
compliance with this Agreement, Vendor grants Customer a non-exclusive,
non-transferable, limited license to access and use the Service during
the Subscription Term solely for Customer's internal business purposes.
Customer acquires no ownership rights.
```

### Split Ownership (Custom + Platform)
```
Customer Deliverables: Customer shall own all Custom Deliverables
created specifically for Customer pursuant to a Statement of Work.

Vendor IP: Vendor shall own all Vendor IP, including Vendor's
pre-existing technology, tools, frameworks, and methodologies,
and any improvements thereto.

License Grant: Vendor grants Customer a perpetual, royalty-free,
non-exclusive license to use Vendor IP solely as incorporated into
the Custom Deliverables for Customer's internal business purposes.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[confidentiality-taxonomy]] - Protecting disclosed IP
- [[indemnification-taxonomy]] - IP infringement indemnity
- [[software-license-expected-clauses]] - License agreement structure
- [[ip-ownership-examples]] - Real IP ownership language from contracts
- [[ip-ownership-negotiation]] - Strategic negotiation guidance

**Related Key Provisions** (tech_transactions):
- [[ip_ownership_assignment.md]] - Conceptual treatment of IP ownership

**Cognitive Patterns** (apply when analyzing IP ownership):
- `S3` - Multi-domain synthesis (technical, legal, business implications)
- `S5` - Party dynamics (who contributes more IP?)
- `S10` - Systemic impact (precedent for future IP relationships)
- `BI2` - Economic incentive design (IP ownership as motivator)
