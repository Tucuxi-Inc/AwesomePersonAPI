---
name: employment-law
description: Employment Law
tags:
  - employment-law
  - hr
  - labor
version: '1.0'
confidence_level: MEDIUM
category: core_legal_frameworks
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
mentoring_priority: 2
validation_type: synthetic
source_type: statutory
---

# Employment Law Fundamentals

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**

## Metadata

```yaml
skill_id: employment_law
domain: legal_fundamentals
sub_domains: [at_will, non_competes, ip_assignment, wage_hour, discrimination]
jurisdictions: [united_states, california, international]
confidence: 0.70
validation_status: synthetic
requires: [keller_patterns, contract_law]
complements: [ip_ownership_assignment, confidentiality_nda]
skill_tier: foundational
mentoring_priority: 2
```

## Core Principles

### At-Will Employment (US Default)

**Rule**: Either party can terminate employment at any time, for any reason (or no reason), with or without notice

**Exceptions** (Cannot Terminate For):
- **Discrimination**: Protected characteristics (race, sex, age, disability, religion, national origin)
- **Retaliation**: Complaining about illegal conduct (wage violations, safety issues, discrimination)
- **Public Policy**: Violates clear public policy (e.g., firing for jury duty, whistleblowing)
- **Implied Contract**: Employment handbook/statements create contractual promise (rare)

**Montana Exception**: Montana is NOT at-will after probationary period (requires good cause to terminate)

### Employment Agreements vs. Offer Letters

**Offer Letter** (Typical):
- Confirms terms (salary, title, start date, at-will status)
- References employee handbook (incorporated by reference)
- No fixed term (at-will continues)

**Employment Agreement** (Less Common):
- Fixed term (e.g., 2-year contract) or for-cause termination only
- Detailed provisions (duties, compensation, IP assignment, restrictive covenants)
- **When Used**: Executives, specialized roles, international hires

## Key Provisions in Employment Agreements

### 1. IP Assignment (Critical for Tech Companies)

**Standard Language**:
```
"Employee assigns to Company all inventions, discoveries, and works of authorship
conceived or made during employment, whether during business hours or personal time,
using Company resources or not, related to Company's actual or anticipated business."
```

**California Labor Code § 2870** (Limits Employer Assignment):
Employee retains inventions if ALL of:
- Developed **entirely on own time**
- Without using employer's **equipment, supplies, facilities, or trade secrets**
- Does **NOT** relate to employer's business or actual/demonstrably anticipated research

**Washington, Illinois, Minnesota**: Similar § 2870 protections (cannot assign all inventions unconditionally)

**Compliance**: Employment agreement must include § 2870 notice (California requirement)

**See Also**: `ip_ownership_assignment.md` for comprehensive IP assignment treatment

### 2. Confidentiality

**Trade Secrets**: Employee has implied duty not to disclose (even without agreement)

**Confidential Information (Broader)**: Agreement extends beyond trade secrets (customer lists, business strategies, financial data, proprietary processes)

**Survival**: Confidentiality obligations survive termination (trade secrets indefinitely, other confidential information 3-5 years)

**See Also**: `confidentiality_nda.md`

### 3. Non-Compete Agreements

**Purpose**: Prevent employee from competing after termination

**Typical Language**:
```
"For [12] months after termination, Employee shall not, within [50 miles / State of California],
engage in business competing with Company or work for any competitor."
```

**Enforceability - Varies Dramatically by State**:

**California**: **UNENFORCEABLE** (Business & Professions Code § 16600) - except:
- Sale of business (seller can have non-compete)
- Dissolution of partnership
- **Protectable Interests**: Use non-solicitation (customers/employees), confidentiality instead

**States with Strict Limits**: Colorado, North Dakota, Oklahoma (similar to California - broadly unenforceable)

**States Enforcing Non-Competes** (If Reasonable): Most other states (New York, Texas, Massachusetts, etc.) - must be:
- **Reasonable Duration**: 6-12 months typical (>2 years rarely enforced)
- **Reasonable Geographic Scope**: Limited to area where employee worked or Company operates
- **Protectable Interest**: Company has legitimate interest (trade secrets, customer relationships)
- **Consideration**: Employee received something (new job offer sufficient at start, new consideration needed mid-employment)

**Recent Trend**: Many states banning non-competes for low-wage workers (<$100K salary thresholds)

**FTC Proposed Rule (2023)**: Would ban most non-competes nationwide (proposed, not final as of 2024)

### 4. Non-Solicitation (More Enforceable Than Non-Competes)

**Customer Non-Solicitation**:
```
"For [12] months after termination, Employee shall not solicit or service customers
with whom Employee had contact during employment for purpose of providing competing services."
```

**Enforceability**: Generally enforceable (even in California) if:
- Limited to customers Employee personally serviced or had material contact with
- Not overly broad (cannot prohibit all interaction with industry)

**Employee Non-Solicitation**:
```
"For [12] months after termination, Employee shall not solicit Company employees
to leave Company or join Employee's new employer."
```

**Enforceability**:
- **Most States**: Enforceable if reasonable duration/scope
- **California**: Generally unenforceable (§ 16600) - employees have right to work where they choose

### 5. Non-Disparagement

**Mutual Non-Disparagement** (Common in Severance Agreements):
```
"Employee and Company agree not to make negative or disparaging statements about the other."
```

**NLRA Issue**: National Labor Relations Act § 7 protects "concerted activity" (employees discussing working conditions)
- **Risk**: Overly broad non-disparagement may violate NLRA (cannot prohibit employees from discussing wages, working conditions)
- **NLRB Guidance**: Non-disparagement clauses that chill protected activity are unlawful

**Safe Harbor**: Limit to "knowingly false" statements or "in formal legal proceedings"

## Wage and Hour Law

### Fair Labor Standards Act (FLSA)

**Minimum Wage**: Federal $7.25/hour (many states higher - CA $16/hour as of 2024)

**Overtime**: Non-exempt employees must receive 1.5x regular rate for hours >40/week

**Exempt vs. Non-Exempt**:

**Exempt** (No Overtime):
- **Executive**: Primary duty managing enterprise/department, supervises 2+ employees, authority to hire/fire
- **Professional**: Advanced knowledge in science/learning, primarily intellectual work (engineers, lawyers, doctors)
- **Administrative**: Office/non-manual work, discretion on significant matters
- **Computer Employees**: Systems analysis, programming, software engineering (if salary >$115,020/year or $27.63/hour as of 2024)
- **Salary Threshold**: Must earn ≥$684/week ($35,568/year) to be exempt (2024 thresholds)

**Non-Exempt** (Entitled to Overtime):
- Hourly employees, clerical workers, junior employees without discretion
- **Must Track Hours**: Employer must maintain accurate time records

**Misclassification Risk**: Classifying non-exempt as exempt → back pay + penalties (2-3 years of unpaid overtime + liquidated damages)

### California-Specific Rules (Stricter Than Federal)

**Overtime**: Daily OT (>8 hours/day = 1.5x, >12 hours/day = 2x) + weekly OT (>40 hours/week)

**Meal/Rest Breaks**:
- **Meal**: 30 minutes for shifts >5 hours (unpaid if relieved of duties)
- **Rest**: 10 minutes for every 4 hours worked (paid)
- **Penalties**: 1 hour of pay for each missed break

**Exempt Salary Threshold**: Higher than federal ($66,560/year for most exemptions as of 2024)

**Computer Professional Exemption**: Requires $115,763.35/year (higher than federal)

**Final Pay**: Must pay all wages immediately upon termination (CA Labor Code § 201 - "waiting time penalties" if delayed)

## Discrimination and Harassment

### Title VII (Federal)

**Prohibits Discrimination Based On**: Race, color, religion, sex (including sexual orientation, gender identity), national origin

**Applies To**: Employers with ≥15 employees

**Harassment**: Hostile work environment or quid pro quo harassment (based on protected characteristic) = unlawful

**Retaliation**: Cannot retaliate against employee for complaining about discrimination or participating in investigation

### ADA (Americans with Disabilities Act)

**Prohibits**: Disability discrimination (employers with ≥15 employees)

**Reasonable Accommodation**: Must provide reasonable accommodations (modified schedule, assistive technology, remote work) unless undue hardship

**Interactive Process**: Employer must engage in good-faith dialogue to identify accommodations

### State Laws (Often Broader)

**California (FEHA)**: Applies to employers with ≥5 employees, covers additional bases (marital status, sexual orientation, military status)

**NYC Human Rights Law**: One of broadest (covers freelancers, interns, broader definition of disability)

## Immigration and I-9 Compliance

### Form I-9 (Employment Eligibility Verification)

**Requirement**: All US employers must verify employee authorization to work (citizens and non-citizens)

**Timing**: Complete Section 2 within 3 business days of hire (employee completes Section 1 on/before first day)

**Documents**: Employee provides documents proving identity and work authorization (passport, green card, driver's license + Social Security card)

**Retention**: Keep for 3 years after hire or 1 year after termination (whichever later)

**ICE Audits**: Immigration and Customs Enforcement can audit I-9s (fines for violations $252-$2,507 per form)

### H-1B Visa (Specialty Occupations)

**Common for Tech Workers**: Engineers, developers, data scientists (requires bachelor's degree or equivalent)

**Lottery**: Annual cap 85,000 (65K regular + 20K advanced degree) - demand exceeds supply (lottery in March for October start)

**Prevailing Wage**: Must pay at least prevailing wage for position/location (protect US workers from wage depression)

**LCA (Labor Condition Application)**: File with DOL before filing H-1B petition (attest to wage/working conditions)

**Portability**: H-1B holders can change employers (new employer files new petition, can start work once filed if meets criteria)

**Path to Green Card**: H-1B is "dual intent" (can pursue permanent residence while on H-1B)

### Green Card (Permanent Residence)

**PERM Labor Certification**: Employer-sponsored green card requires PERM (test labor market, prove no qualified US workers available) - takes 6-24 months

**I-140 Petition**: After PERM approval, file I-140 (immigrant petition) - proves ability to pay wage, employee qualifications

**Adjustment of Status / Consular Processing**: Final step to obtain green card (I-485 if in US, consular processing if abroad)

**Total Timeline**: 2-5 years (or longer for India/China nationals due to per-country caps)

## Risk Assessment & Compliance

### High-Risk Red Flags

- ⚠️ Misclassifying employees as exempt (back pay + penalties)
- ⚠️ Using non-competes in California (§ 16600 violation - unenforceable, potential employee lawsuit)
- ⚠️ No § 2870 notice in California employment agreement (required)
- ⚠️ Broad non-disparagement clause (may violate NLRA)
- ⚠️ Missed meal/rest breaks in California (1 hour pay penalty per violation)
- ⚠️ I-9 violations (incomplete forms, missing signatures, wrong documents)

### Compliance Best Practices

- ✅ Conduct exempt/non-exempt analysis with employment counsel (especially for border-line roles)
- ✅ Track hours for non-exempt employees (time-tracking software)
- ✅ Include California § 2870 notice in employment agreements (if CA employees)
- ✅ Avoid non-competes (use non-solicitation + confidentiality instead, especially CA)
- ✅ Training on harassment prevention (required in CA, NY, and many states for certain employer sizes)
- ✅ I-9 audit annually (ensure compliance before ICE audit)
- ✅ Establish immigration processes (H-1B lottery timing, green card sponsorship policies)

## When to Consult Experts

- **Executive Hires**: Employment agreements with significant comp, equity, severance (negotiate terms)
- **International Employees**: Cross-border employment, immigration visas (H-1B, L-1, green card sponsorship)
- **Terminations**: High-risk terminations (retaliation claims, discrimination concerns, executive with contract)
- **FLSA Audits**: DOL investigation for wage/hour violations
- **Discrimination Claims**: EEOC charge, state agency complaint, or lawsuit
- **Non-Compete Disputes**: Departing employee going to competitor, or new hire subject to prior non-compete
- **M&A**: Acquiring company (review employment agreements, classification, immigration compliance, liability)

## References

> ⚠️ **Synthetic Skill** - Not expert validated. Employment law is highly state-specific with severe penalties. Consult employment counsel before implementing policies or agreements.

**Key Statutes**: FLSA, Title VII, ADA, NLRA, California Labor Code, CA Business & Professions Code § 16600, § 2870

**Cross-Reference**: `ip_ownership_assignment.md`, `confidentiality_nda.md`
