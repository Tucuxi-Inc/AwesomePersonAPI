---
name: insurance-taxonomy
description: >-
  Comprehensive taxonomy of insurance requirement clauses including coverage
  types, limits, certificates, and additional insured provisions. Use when
  drafting or negotiating risk transfer provisions.
tags:
  - insurance
  - liability
  - coverage
  - certificate
  - additional-insured
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - indemnification-taxonomy
  - limitation-of-liability-taxonomy
  - services-agreement-expected-clauses
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 3
validation_type: human_validated
source_type: contract_samples
---

# Insurance Requirements Taxonomy

## Overview

Insurance provisions require parties to maintain specified coverage to protect against losses arising from the contract. They serve as a risk transfer mechanism, ensuring the party best positioned to prevent harm has resources to cover damages. This taxonomy catalogs insurance patterns observed across commercial agreements.

## Common Coverage Types

### A. Commercial General Liability (CGL)

**Purpose**: Third-party bodily injury, property damage, personal injury.

```
Commercial General Liability insurance with limits of at least
[AMOUNT] per occurrence and [AMOUNT] annual aggregate, covering:
(a) bodily injury and property damage;
(b) personal and advertising injury;
(c) products and completed operations.
```

**Typical Limits**:
- Standard: $1M per occurrence / $2M aggregate
- Higher risk: $2M per occurrence / $4M aggregate

### B. Professional Liability (E&O)

**Purpose**: Errors, omissions, negligent acts in professional services.

```
Professional Liability (Errors & Omissions) insurance with limits
of at least [AMOUNT] per claim and [AMOUNT] annual aggregate,
covering claims arising from negligent acts, errors, or omissions
in the performance of professional services.
```

**Typical Limits**:
- Small engagements: $1M per claim
- Enterprise: $2-5M per claim
- Mission-critical: $5-10M per claim

### C. Cyber/Technology E&O

**Purpose**: Data breaches, cyber incidents, technology failures.

```
Cyber Liability insurance with limits of at least [AMOUNT],
covering: (a) data breach response costs; (b) regulatory fines
and penalties; (c) network security liability; (d) privacy liability;
(e) technology errors and omissions.
```

**Typical Limits**: $2M-$10M depending on data sensitivity.

### D. Workers' Compensation

**Purpose**: Employee injuries/illness; required by law.

```
Workers' Compensation insurance as required by applicable law,
with Employer's Liability coverage of at least [AMOUNT] per
accident, [AMOUNT] disease per employee, and [AMOUNT] disease
policy limit.
```

**Typical Limits**: $1M/$1M/$1M (statutory limits vary by state).

### E. Automobile Liability

**Purpose**: Vehicle-related injuries/damage.

```
Commercial Automobile Liability insurance covering all owned,
non-owned, and hired vehicles with limits of at least [AMOUNT]
combined single limit per accident.
```

**Typical Limits**: $1M combined single limit.

### F. Umbrella/Excess Liability

**Purpose**: Additional coverage above primary policies.

```
Umbrella or Excess Liability insurance with limits of at least
[AMOUNT], providing coverage excess of CGL, Automobile, and
Employer's Liability policies.
```

**Typical Limits**: $5M-$25M depending on contract value and risk.

### G. Property Insurance

**Purpose**: Physical assets, equipment, inventory.

```
Property insurance covering all equipment, materials, and work
in progress at replacement cost, including coverage for [equipment
breakdown / business interruption / flood / earthquake].
```

### H. Crime/Fidelity Insurance

**Purpose**: Employee theft, fraud, dishonesty.

```
Crime insurance with limits of at least [AMOUNT], covering employee
theft, computer fraud, and funds transfer fraud.
```

## Insurance Provisions Structure

### 1. Coverage Requirements

```
INSURANCE REQUIREMENTS
During the term and for [X] years thereafter, [Vendor/Provider]
shall maintain the following insurance coverages:

(a) Commercial General Liability: $[X] per occurrence / $[X] aggregate
(b) Professional Liability: $[X] per claim / $[X] aggregate
(c) Cyber Liability: $[X] per claim
(d) Workers' Compensation: Statutory limits
(e) Automobile Liability: $[X] combined single limit
```

### 2. Additional Insured Requirement

```
[Customer/Client] and its officers, directors, employees, and agents
shall be named as additional insureds on [Vendor's] Commercial General
Liability and Umbrella policies for claims arising out of this Agreement.
```

**Coverage Type**: Primary and non-contributory (Customer's insurance is excess).

### 3. Waiver of Subrogation

```
[Vendor] shall cause its insurers to waive all rights of subrogation
against [Customer] for losses covered by the required insurance policies.
```

**Purpose**: Prevents insurer from seeking recovery from Customer.

### 4. Certificate of Insurance

```
CERTIFICATES
Upon request and upon each renewal, [Vendor] shall provide [Customer]
with certificates of insurance evidencing the required coverages.
Certificates shall: (a) identify policies and limits; (b) confirm
additional insured status; (c) confirm waiver of subrogation;
(d) provide [30] days notice of cancellation or material change.
```

### 5. Notice of Cancellation

```
[Vendor] shall provide [Customer] with [30] days prior written notice
of cancellation, non-renewal, or material reduction in coverage of
any required policy (or [10] days for non-payment of premium).
```

### 6. Insurer Requirements

```
All insurance shall be placed with insurers: (a) licensed to do
business in [State/Country]; (b) rated A- VII or higher by A.M. Best
(or equivalent); (c) acceptable to [Customer].
```

### 7. Deductibles and Self-Insurance

```
Deductibles and self-insured retentions shall not exceed [AMOUNT]
without [Customer's] prior approval. [Vendor] is responsible for
all deductibles.
```

### 8. Claims-Made vs. Occurrence

```
Professional Liability and Cyber Liability policies may be on a
claims-made basis, provided [Vendor] maintains coverage for [X] years
following termination or purchases tail coverage.
```

**Difference**:
- Occurrence: Covers incidents during policy period regardless of when claim is made
- Claims-Made: Covers claims made during policy period regardless of when incident occurred

## Insurance by Contract Type

| Contract Type | Key Coverages | Typical Limits |
|---------------|--------------|----------------|
| Professional Services | CGL, E&O, Cyber | $1-2M each |
| SaaS/Technology | E&O, Cyber | $2-5M each |
| Construction | CGL, Auto, Workers' Comp | $2M+; umbrella $5M+ |
| Manufacturing | CGL, Products, Property | $2M+; product recall |
| Data Processing | Cyber, E&O | $5-10M |
| Events | CGL, Cancellation | Event-specific |

## Key Decision Points

1. **Coverage Types**: Which coverages are necessary?
2. **Limits**: What limits are appropriate for the risk?
3. **Additional Insured**: Should Customer be added?
4. **Primary/Non-Contributory**: Order of coverage?
5. **Waiver of Subrogation**: Required?
6. **Certificate Frequency**: Annual or upon request?
7. **Insurer Rating**: Minimum acceptable rating?
8. **Claims-Made Tail**: Duration after termination?
9. **Deductible Cap**: Maximum acceptable deductible?

## Common Pitfalls

1. **No insurance requirements**: Party has no coverage
2. **Inadequate limits**: Coverage insufficient for potential loss
3. **Missing coverage types**: Key risks not insured
4. **No additional insured**: Customer not protected
5. **No cancellation notice**: Coverage lapses without warning
6. **Low insurer rating**: Insurer may not pay claims
7. **No tail coverage**: Claims-made gaps post-termination
8. **Certificate ≠ Policy**: Certificate doesn't modify coverage

## Sample Provisions

### Standard Services Insurance
```
INSURANCE
Provider shall maintain throughout the term and for [2] years thereafter:
(a) CGL: $1M per occurrence / $2M aggregate
(b) Professional Liability: $2M per claim / $2M aggregate
(c) Workers' Compensation: Statutory limits
(d) Automobile: $1M combined single limit

Customer shall be named as additional insured on CGL policy. Provider
shall provide certificates annually and upon request, with 30 days
notice of cancellation. Insurers rated A- VII or higher by A.M. Best.
```

### Technology/SaaS Insurance
```
Vendor shall maintain: (a) Technology E&O: $5M per claim; (b) Cyber
Liability: $5M per claim, covering data breach response, regulatory
fines, and network security; (c) CGL: $2M aggregate.

Customer shall be additional insured on CGL. All policies shall be
primary and non-contributory. Vendor shall maintain tail coverage
for 3 years following termination.
```

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[indemnification-taxonomy]] - Insurance backing indemnity
- [[limitation-of-liability-taxonomy]] - Insurance as recovery source
- [[services-agreement-expected-clauses]] - Insurance in services context
- [[insurance-examples]] - Real insurance language from contracts
- [[insurance-negotiation]] - Strategic negotiation guidance

**Cognitive Patterns** (apply when analyzing insurance):
- `S3` - Multi-domain synthesis (insurance + liability + indemnification)
- `S4` - Systematic risk assessment (insurance as risk transfer)
- `BI2` - Economic enforceability (insurance backing indemnity)
- `BI3` - Context-aware risk (insurance proportional to deal risk)
- `BI5` - Alternative solutions (insurance as liability cap alternative)
