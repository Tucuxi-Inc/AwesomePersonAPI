---
name: warranties-representations
description: Warranties Representations
tags:
  - assurances
  - representations
  - warranties
version: '1.0'
confidence_level: MEDIUM
category: key_provisions
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
pattern_tier: 2
mentoring_priority: 1
validation_type: synthetic
source_type: expert_judgment
---

# Warranties and Representations

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**

## Metadata

```yaml
skill_id: warranties_representations
domain: contract_provisions
sub_domains: [product_warranties, authority, ownership, disclaimers, remedies]
confidence: 0.70
validation_status: synthetic
requires: [keller_patterns, contract_law, ip_law]
complements: [indemnification, liability_limitations, termination_provisions]
skill_tier: foundational
mentoring_priority: 1
```

## Core Principles

### Representations vs. Warranties

**Representation**:
- Statement of **past or present fact** at time of contract execution
- Example: "Company has no pending litigation"
- **Breach**: If untrue at time made → misrepresentation (contract voidable, damages for fraud/negligent misrepresentation)

**Warranty**:
- **Promise** about past, present, or future state
- Example: "Software will conform to Documentation for 90 days"
- **Breach**: If untrue → breach of contract (damages for breach, not fraud)

**Legal Distinction**:
- **Representation**: Induces party to enter contract (reliance-based)
- **Warranty**: Part of the bargain (contractual promise)

**Practical Reality**: Most contracts combine "represents and warrants" (belt-and-suspenders approach)

```
"Party A represents and warrants that..."
```

**Why Both?**: Covers both misrepresentation (inducement) and breach of warranty (contractual) theories of recovery

### Purpose of Warranties and Representations

**Allocate Risk**:
- Party making warranty assumes risk if statement untrue
- Party receiving warranty can rely (no need to independently verify)

**Due Diligence Substitute**:
- Instead of investigating every fact, parties rely on representations
- Example: Buyer relies on Seller's representation "I own this asset" (Buyer doesn't need title search if trusted Seller)

**Disclosure Mechanism**:
- Act as questionnaire (forces party to investigate and disclose)
- Example: "No undisclosed liabilities" forces Seller to review and disclose all liabilities

**Foundation for Indemnification**:
- If representation breached → indemnification triggered
- Example: "Software does not infringe third-party IP" + "Seller indemnifies for IP infringement" → if infringement, Seller indemnifies

## Standard Representations and Warranties

### 1. Authority and Capacity

**Purpose**: Confirm party has legal power to enter contract

**Standard Language**:
```
"Party represents and warrants that:
(a) Organization: Party is duly organized, validly existing, and in good standing
    under the laws of [Jurisdiction];
(b) Authority: Party has full power and authority to execute and deliver this Agreement
    and to perform its obligations hereunder;
(c) Authorization: Execution and performance have been duly authorized by all necessary
    corporate action;
(d) Enforceability: This Agreement constitutes a valid and binding obligation,
    enforceable in accordance with its terms;
(e) No Conflicts: Execution and performance do not violate (i) Party's organizational
    documents, (ii) any agreement to which Party is bound, or (iii) any law or regulation."
```

**Why Important**:
- Prevents "I didn't have authority" defense (if breach occurs)
- Ensures counterparty is legitimate entity (not shell company)
- Confirms no legal barrier to performance (no conflicting obligations)

**Due Diligence**: Request certificates (good standing certificate, board resolutions approving transaction)

### 2. IP Ownership and Non-Infringement

**Purpose**: Confirm party owns or has rights to IP being licensed/transferred

**IP Ownership**:
```
"Licensor represents and warrants that:
(a) Licensor owns all right, title, and interest in the Licensed IP, free and clear
    of liens, encumbrances, or conflicting licenses;
(b) All inventors/authors have executed valid assignments to Licensor;
(c) Licensed IP does not infringe or misappropriate any third-party intellectual
    property rights;
(d) No claims of infringement have been made or threatened against Licensor regarding
    Licensed IP."
```

**Why Important**:
- Licensee needs assurance it can use IP without infringement risk
- If ownership disputed, licensee's license may be void (licensor had no rights to grant)

**Exceptions/Carve-Outs**:
```
"Licensor makes no warranty regarding non-infringement arising from:
(a) Modification of Licensed IP by Licensee;
(b) Combination of Licensed IP with other products, data, or technology;
(c) Use of Licensed IP outside the scope of this Agreement."
```

**See Also**: `ip_ownership_assignment.md`, `indemnification.md`

### 3. Compliance with Laws

**Purpose**: Confirm party is operating legally

**Standard Language**:
```
"Party represents and warrants that:
(a) Compliance: Party is in compliance with all applicable laws, regulations, and
    orders, including (without limitation) export control laws, anti-corruption laws
    (FCPA, UK Bribery Act), and data privacy laws (GDPR, CCPA);
(b) Licenses/Permits: Party holds all licenses, permits, and authorizations necessary
    to conduct its business and perform under this Agreement;
(c) No Violations: Performance under this Agreement will not cause Party to violate
    any applicable law or regulation."
```

**Why Important**:
- Protects against regulatory liability (if counterparty violating law, could create joint liability or reputational risk)
- Particularly critical for regulated industries (healthcare, financial services, government contracting)

**Enhanced for Specific Contexts**:

**GDPR (EU Personal Data)**:
```
"Processor represents and warrants that it will process Personal Data in compliance
with GDPR, including implementing appropriate technical and organizational measures
(Article 32)."
```

**Export Controls (International)**:
```
"Licensee represents that it is not located in, under control of, or a national
or resident of any embargoed country (Cuba, Iran, North Korea, Syria, Crimea), and
is not on any US government restricted party list (Denied Persons List, Entity List,
SDN List)."
```

### 4. Financial Statements (M&A Context)

**Purpose**: Confirm financial condition of target company

**Standard Language**:
```
"Seller represents and warrants that:
(a) Financial Statements: The audited financial statements for years ending [dates]
    and unaudited financials for [recent period] (Exhibit A) are true, complete,
    and accurate in all material respects, and fairly present the financial condition
    and results of operations of the Company;
(b) No Undisclosed Liabilities: Company has no liabilities (absolute, accrued,
    contingent, or otherwise) except as disclosed in Financial Statements or this Agreement;
(c) No Adverse Changes: Since [balance sheet date], there has been no Material Adverse
    Change in Company's business, operations, assets, liabilities, or financial condition."
```

**Material Adverse Change (MAC)**:
- Defined as change that materially and adversely affects business, operations, assets, liabilities, financial condition, or results of operations
- **Buyer's Out**: If MAC occurs between signing and closing, Buyer can refuse to close (deal terminates)

**Why Important**: Buyer relies on financial condition (if materially worse than represented, Buyer overpaid)

### 5. Litigation and Disputes

**Purpose**: Disclose pending or threatened legal claims

**Standard Language**:
```
"Party represents and warrants that:
(a) No Litigation: There is no litigation, arbitration, investigation, or governmental
    proceeding pending or, to Party's knowledge, threatened against Party;
(b) No Violations: Party is not in violation of any order, judgment, or decree of
    any court or governmental authority;
(c) No Default: Party is not in default under any material contract."
```

**"To Party's Knowledge" Qualifier**:
- Limits warranty to facts actually known (not facts party should have known)
- **Buyer Concern**: Too narrow (Seller could claim "we didn't know" even if should have known)
- **Negotiation**: Define "knowledge" (e.g., "knowledge of senior management after reasonable inquiry")

**Why Important**: Undisclosed litigation = contingent liability (could materially affect business value)

### 6. Product Warranties

**Purpose**: Confirm product quality and conformance to specifications

**Standard Software Warranty**:
```
"Vendor warrants that the Software will substantially conform to the Documentation
for [90 days] from the Delivery Date. Vendor's sole obligation and Customer's
exclusive remedy for breach of this warranty shall be, at Vendor's option:
(a) to repair or replace the non-conforming Software; or
(b) to refund the license fee paid and terminate the license."
```

**Standard Hardware Warranty**:
```
"Manufacturer warrants that the Products will be free from defects in materials
and workmanship for [1 year] from delivery. If Product fails to conform, Manufacturer
will, at its option, repair or replace the defective Product or refund the purchase price."
```

**Key Terms**:
- **Standard**: "Substantially conform" (not perfect conformance - allows minor deviations)
- **Duration**: 30-90 days (software), 1-3 years (hardware) - varies by industry
- **Exclusive Remedy**: "Sole obligation and exclusive remedy" limits Customer to repair/replace/refund (no other damages)

**Why Important**: Without warranty, product sold "as is" (Customer assumes all risk)

**See Also**: `software_licensing.md` for comprehensive software warranty treatment

### 7. No Malicious Code

**Purpose**: Ensure software does not contain harmful code

**Standard Language**:
```
"Vendor represents and warrants that the Software does not contain, and Vendor will
not introduce, any viruses, worms, Trojan horses, backdoors, time bombs, or other
malicious code designed to damage, disable, or provide unauthorized access to systems."
```

**Why Important**: Malicious code can cause severe damage (data loss, security breaches, business disruption)

**Carve-Out**:
```
"Vendor is not responsible for malicious code introduced by Customer's modifications
or third-party integrations."
```

## Disclaimer of Warranties

### Purpose of Disclaimers

**Default Rule (Without Disclaimer)**: Uniform Commercial Code (UCC) implies warranties:
- **Merchantability** (§ 2-314): Goods are fit for ordinary purposes (software/products work as expected)
- **Fitness for Particular Purpose** (§ 2-315): If seller knows buyer's specific purpose and buyer relies on seller's expertise, implied warranty that goods are fit for that purpose

**With Disclaimer**: Seller can disclaim implied warranties (shift risk to buyer)

### How to Disclaim Implied Warranties

**UCC Requirements** (§ 2-316):

**To Disclaim Merchantability**:
- Must use word "merchantability"
- Must be **conspicuous** (all caps, bold, separate paragraph)

**To Disclaim Fitness for Particular Purpose**:
- Must be in writing
- Must be conspicuous

**To Disclaim All Implied Warranties**:
- Use "AS IS" or "WITH ALL FAULTS" language

**Standard Disclaimer**:
```
"EXCEPT AS EXPRESSLY PROVIDED IN THIS AGREEMENT, VENDOR DISCLAIMS ALL WARRANTIES,
EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. VENDOR
DOES NOT WARRANT THAT THE SOFTWARE WILL BE ERROR-FREE, UNINTERRUPTED, OR MEET
CUSTOMER'S REQUIREMENTS."
```

**Conspicuous Requirement**: All caps, bold, or separate section header

**Why Vendors Want Disclaimers**: Limit liability (otherwise, implied warranty of merchantability applies = software must be "fit for ordinary purposes" = very broad standard)

**Why Customers Resist**: "AS IS" = no warranties at all (Customer assumes all risk if software defective)

**Negotiation Compromise**:
- **Express Warranty Provided**: Limited warranty (90 days, substantially conform) + disclaimer of implied warranties (merchantability, fitness)
- **Customer Gets**: Some warranty protection (express warranty) but not open-ended (implied warranties disclaimed)

### Non-Waivable Warranties

**Consumer Protection Laws**: Some jurisdictions prohibit waiving warranties in consumer contracts (B2C)

**Examples**:
- **EU Consumer Rights Directive**: 2-year conformity warranty for consumer goods (cannot be waived)
- **Magnuson-Moss Warranty Act (US)**: If written warranty provided to consumers, certain disclosures required (cannot completely disclaim implied warranties if written warranty provided)

**Implication**: "AS IS" disclaimers may be unenforceable in B2C contracts (enterprise B2B contracts are generally enforceable)

## Warranty Remedies and Limitations

### Exclusive Remedies

**Purpose**: Limit buyer's remedies to specific options (prevent open-ended damages)

**Standard Language**:
```
"THE REMEDIES SET FORTH IN THIS SECTION ARE CUSTOMER'S SOLE AND EXCLUSIVE REMEDIES
FOR BREACH OF WARRANTY. VENDOR'S MAXIMUM LIABILITY FOR BREACH OF WARRANTY SHALL
NOT EXCEED THE FEES PAID BY CUSTOMER IN THE 12 MONTHS PRECEDING THE CLAIM."
```

**Typical Remedies**:
- **Repair**: Fix the defect (software patch, hardware repair)
- **Replace**: Provide replacement product
- **Refund**: Return fees and terminate contract

**Customer Negotiation**:
- **Remove "Exclusive Remedy"**: Allow Customer to pursue other remedies (incidental/consequential damages)
- **Specify Timeline**: "Vendor must repair within 30 days; if cannot, must replace or refund" (avoids indefinite repair attempts)

### Failure of Essential Purpose

**Issue**: If exclusive remedy "fails of its essential purpose," court may allow other remedies

**Example**: Software warranty remedy is "repair or replace." Vendor attempts to repair 10 times over 6 months, software still non-functional. Court may find remedy "failed" → Customer can seek consequential damages (even if contract says "exclusive remedy").

**Vendor Protection**:
```
"If repair or replacement is not commercially reasonable, Vendor may refund fees
and terminate license. EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE, VENDOR'S
LIABILITY SHALL NOT EXCEED THE FEES PAID, AND VENDOR SHALL NOT BE LIABLE FOR
CONSEQUENTIAL DAMAGES."
```

**Attempt to Preserve Cap**: Even if exclusive remedy fails, liability cap and consequential damages exclusion survive

**Enforceability**: State-dependent (some courts enforce, others find unconscionable)

### Warranty Disclaimers vs. Liability Limitations

**Warranty Disclaimer**: "We make no warranty that software is error-free" (disclaim obligation)

**Liability Limitation**: "Our maximum liability is $X" (even if warranty breached, cap damages)

**Relationship**:
- **Both Work Together**: Disclaimer reduces likelihood of breach (no warranty = no breach), limitation caps damages (if breach occurs)
- **If Disclaimer Fails**: Implied warranty applies (software must be "merchantable"), but liability limitation may still cap damages

**See Also**: `liability_limitations.md` for comprehensive treatment

## Representation and Warranty Insurance (RWI)

### What is RWI?

**Definition**: Insurance policy that covers losses from breaches of representations and warranties in M&A transactions

**How it Works**:
- **Buyer-Side Policy** (Most Common): If Seller's representations breached, Buyer makes claim against insurance (not Seller)
- **Seller-Side Policy**: If Buyer refuses to close due to Seller's breach, Seller makes claim

**Who Pays Premium**: Negotiated (Buyer, Seller, or split)

### Why Use RWI?

**Seller Benefits**:
- **Clean Exit**: Seller gets cash at closing (no escrow holdback for indemnity claims)
- **No Future Liability**: Buyer claims against insurance, not Seller (Seller moves on)

**Buyer Benefits**:
- **Deeper Coverage**: Insurance proceeds available (not limited to escrow or Seller's assets)
- **Preserve Relationship**: If Seller is management team staying on, avoid suing Seller (claim against insurance instead)

**Typical Structure**:
- **Retention (Deductible)**: $1M-$5M (Buyer bears first $X of losses)
- **Coverage**: $10M-$100M+ (depends on deal size)
- **Premium**: 3-6% of coverage amount (e.g., 4% of $20M = $800K)

### What RWI Covers

**Covered**:
- Breach of fundamental representations (authority, ownership, financial statements, no undisclosed liabilities, compliance, litigation)
- Breaches discovered post-closing (within policy period, typically 3-6 years)

**Excluded**:
- **Known Issues**: Buyer cannot insure against breaches disclosed in disclosure schedules (no insurance for known risks)
- **Forward-Looking Projections**: Forecasts, pro formas (insurance covers historical reps, not future projections)
- **Fraud**: Seller's intentional misrepresentations (insurance covers negligent/innocent breaches, not fraud)

**See Also**: M&A-specific due diligence and deal structuring considerations

## Special Considerations

### GDPR Representations (If Personal Data)

**Data Controller Obligations**:
```
"Data Provider represents and warrants that:
(a) it has collected Personal Data in compliance with GDPR, with lawful basis for processing;
(b) it has obtained necessary consents or has other lawful basis to share Personal
    Data with Data Recipient for the purposes of this Agreement;
(c) Personal Data is accurate and up-to-date (GDPR Article 5(1)(d));
(d) it has provided data subjects with required notices (GDPR Article 13-14)."
```

**Why Important**: If Personal Data collected illegally, Data Recipient may be liable for processing (GDPR applies to both controller and processor)

**Data Processor Obligations**:
```
"Data Processor represents and warrants that it will:
(a) process Personal Data only on documented instructions from Controller;
(b) implement appropriate technical and organizational measures (GDPR Article 32);
(c) notify Controller of data breaches within 24 hours (support Controller's 72-hour notification to authority)."
```

**See Also**: `data_privacy_regulations.md`, `data_agreements.md`

### Open Source Compliance

**Representation (Software Vendors)**:
```
"Vendor represents and warrants that:
(a) Vendor has identified all open source components included in the Software (listed
    in Exhibit A);
(b) Vendor is in compliance with all open source license terms applicable to such components;
(c) No open source components are licensed under GPL, AGPL, or other copyleft licenses
    requiring derivative works to be open sourced [OR: any copyleft components are
    listed in Exhibit A]."
```

**Why Important**: Copyleft licenses (GPL) require derivative works to be open sourced → Customer's proprietary code may need to be released

**Customer Negotiation**: "No GPL" (if Customer concerned about copyleft), OR full disclosure with Customer consent (if Customer accepts risk)

### Financial Covenants (Loan/Investment Context)

**Representations at Closing**:
```
"Borrower represents and warrants as of Closing Date:
(a) Debt-to-EBITDA ratio does not exceed [3.0:1];
(b) Current ratio (current assets / current liabilities) is at least [1.5:1];
(c) Tangible net worth is at least $[X]."
```

**Ongoing Covenants** (Not Just Representations):
```
"Borrower covenants that during the term:
(a) Debt-to-EBITDA shall not exceed [3.0:1] (tested quarterly);
(b) Borrower shall maintain minimum cash balance of $[Y];
(c) Borrower shall not incur additional debt exceeding $[Z] without Lender's consent."
```

**Consequence of Breach**: Event of default → Lender can accelerate loan (demand immediate repayment)

## Risk Assessment Framework

### High-Risk Indicators (Require Immediate Attention)

**Overly Broad Warranties**:
- ⚠️ "Software will be error-free and meet all Customer's requirements" (impossible to satisfy)
- ⚠️ "Data is 100% accurate" (unrealistic for large datasets)
- ⚠️ No qualifier ("to Seller's knowledge," "in all material respects") - absolute warranty

**Inadequate Warranties** (Customer Perspective):
- ⚠️ "AS IS" with no warranties (Customer assumes all risk)
- ⚠️ No IP non-infringement warranty (Customer has no protection if product infringes)
- ⚠️ No compliance representation (Vendor may be violating laws, implicating Customer)

**Exclusive Remedy Too Narrow**:
- ⚠️ Only remedy is "repair" (no replace/refund option if repair fails)
- ⚠️ Warranty period extremely short (7 days) for complex product (insufficient time to discover defects)
- ⚠️ Remedy fails → no fallback (exclusive remedy failed, but no consequential damages allowed = Customer has no recourse)

**Authority/Enforceability Issues**:
- ⚠️ No representation that party has authority to enter contract (if challenged, contract may be void)
- ⚠️ Conflicting agreements not addressed (party may breach other contracts by performing this one)

### Medium-Risk Indicators (Require Clarification)

**Qualifier Ambiguity**:
- ⚠️ "To Party's knowledge" but "knowledge" undefined (whose knowledge? senior management? anyone in company?)
- ⚠️ "Material" not defined (what is "material" breach? $10K? $100K? 5% of revenue?)
- ⚠️ "Substantially conform" vague (how close is "substantial"? 90% conformance? 99%?)

**Warranty Duration Unclear**:
- ⚠️ "Warranty period" not specified (indefinite? or does it end at some point?)
- ⚠️ Start date ambiguous ("from delivery" - is delivery when shipped or when received?)

**Remedy Process Unclear**:
- ⚠️ No process for claiming warranty breach (Customer must notify within X days? Written notice required?)
- ⚠️ No timeline for Vendor to cure (must repair "promptly" - what is "prompt"? 30 days? 90 days?)

### Low-Risk Indicators (Standard Provisions)

- ✅ Authority and capacity representations (organization, authorization, enforceability, no conflicts)
- ✅ IP ownership and non-infringement (with standard exceptions for modifications/combinations)
- ✅ Compliance with laws (including specific regulations relevant to industry - GDPR, export controls)
- ✅ Limited product warranty (substantially conform to docs, 90 days, repair/replace/refund remedy)
- ✅ Disclaimer of implied warranties (merchantability, fitness) - conspicuous (all caps)
- ✅ Exclusive remedy with fail-safe (if repair/replace not possible, refund and terminate)
- ✅ Warranty period clearly defined (start date, duration)
- ✅ Claim process specified (written notice, timeline for cure)
- ✅ Qualifiers appropriately used ("to knowledge," "material," "substantial") with definitions
- ✅ No malicious code representation (if software/data)

## Validation Questions

Before finalizing representations and warranties, validate:

- ✅ **Authority**: Does party represent it has authority to enter contract? Board approval if needed?
- ✅ **Ownership**: If IP involved, does party represent it owns or has rights to IP? Assignments from inventors/authors?
- ✅ **Non-Infringement**: Does party warrant IP does not infringe third-party rights? Exceptions for modifications/combinations?
- ✅ **Compliance**: Does party represent compliance with laws? Specific regulations listed (GDPR, export controls)?
- ✅ **Financial Condition**: If M&A, are financial statements warranted accurate? Material Adverse Change defined?
- ✅ **Litigation**: Does party represent no pending/threatened litigation? "To knowledge" qualifier appropriate?
- ✅ **Product Warranty**: What is standard (substantially conform, error-free, fit for purpose)? Duration?
- ✅ **Warranty Remedy**: Repair, replace, or refund? Exclusive remedy? Timeline for cure?
- ✅ **Disclaimer**: Are implied warranties disclaimed? Conspicuous (all caps)? Enforceable in jurisdiction?
- ✅ **No Malicious Code**: If software/data, is there representation of no viruses/backdoors?
- ✅ **GDPR Compliance**: If personal data, are collection, consent, and data subject rights representations included?
- ✅ **Open Source**: If software, are open source components disclosed? GPL compliance?
- ✅ **Qualifiers**: Are "knowledge," "material," "substantial" defined? Appropriate scope?
- ✅ **Warranty Period**: Start date (delivery, acceptance, effective date)? Duration (30/90/365 days)?
- ✅ **Claim Process**: How does Customer claim warranty breach? Notice requirements? Timeline for Vendor to cure?
- ✅ **Liability Cap**: Is warranty liability capped? Amount (fees paid, $X fixed amount)?
- ✅ **Survival**: Do representations survive closing (M&A) or termination? How long (1-3 years)?
- ✅ **Indemnification**: Are reps/warranties backed by indemnification? Limits (basket, cap)?

## When to Consult Experts

Engage legal counsel with expertise in contract law and specific industry regulations when:

- **M&A Transactions**: Comprehensive representations (financials, liabilities, litigation, compliance, IP)
- **High-Value Contracts**: >$1M (warranties create significant liability exposure)
- **Regulated Industries**: Healthcare (HIPAA), financial services (GLBA, SOX), government (FAR)
- **Complex IP**: Patents, trade secrets, substantial software (ownership and non-infringement critical)
- **Cross-Border**: Multi-jurisdictional (warranty enforceability varies, consumer protection laws)
- **Personal Data**: GDPR, CCPA compliance representations (data collection, consent, data subject rights)
- **Open Source**: Software with open source components (license compliance, copyleft risk)
- **Product Liability**: Hardware, medical devices, consumer products (warranty disclaimers may be unenforceable, product liability insurance needed)
- **Warranty Disputes**: Vendor refusing to honor warranty, Customer claiming defects (interpretation of "substantially conform," "material breach")
- **RWI**: M&A deals with representation and warranty insurance (policy terms, exclusions, underwriting)

Consult warranty counsel BEFORE agreeing to broad warranties (once made, cannot easily disclaim if breached). Representations and warranties are often heavily negotiated (both parties have strong interests).

## References

> ⚠️ **Reminder**: This is a **synthetic skill** created for validation system testing. While based on general legal principles, it has NOT been validated by expert practitioners. Use as a framework for identifying claims requiring validation, not as authoritative legal guidance.

**Cross-Reference Related Skills**:
- `keller_patterns.md` - Cognitive reasoning patterns (S1-S13)
- `contract_law.md` - Contract formation, breach, remedies
- `ip_law.md` - IP ownership and infringement fundamentals
- `ip_ownership_assignment.md` - IP transfer and assignment mechanics
- `software_licensing.md` - Software warranty standards
- `indemnification.md` - Backup for warranty breaches (defense + damages)
- `liability_limitations.md` - Caps and exclusions that limit warranty liability
- `data_privacy_regulations.md` - GDPR/CCPA representations for personal data
- `data_agreements.md` - Data accuracy and compliance warranties

**Contract Intelligence Skills** (from 4,900+ real contracts):
- `warranties-taxonomy.md` - Warranty clause patterns from real contracts
- `representations-taxonomy.md` - Representation clause patterns from real contracts
- `warranty-examples.md` - Real warranty language extracted from contracts
- `representations-examples.md` - Real representation language extracted from contracts
- `warranty-negotiation.md` - Strategic negotiation guidance with S1-S13 patterns
- `representations-negotiation.md` - Strategic negotiation guidance with S1-S13 patterns

**Cognitive Patterns** (apply to warranty/representation analysis):
- `S2` - Information gap identification (what representations to verify?)
- `S3` - Multi-domain synthesis (technical feasibility of warranty)
- `S9` - Hierarchical due diligence (materiality of representations)
- `BI3` - Context-aware risk calibration (warranty scope vs. risk tolerance)

**Key Legal Frameworks** (for validation):
- Uniform Commercial Code (UCC) Article 2 - sales of goods, warranties (§ 2-314 merchantability, § 2-315 fitness, § 2-316 disclaimers)
- Common law misrepresentation - fraudulent, negligent, innocent (varies by jurisdiction)
- Consumer protection laws - Magnuson-Moss Warranty Act (US), Consumer Rights Directive (EU)

**Validation Sources** (when validating claims in analysis):
- Contract text (representations, warranties, disclaimers, exclusive remedies)
- Disclosure schedules (exceptions to representations - "except as disclosed")
- Product documentation (specifications, what is "substantial conformance"?)
- Financial statements (if financial representations made)
- Web search for current case law on warranty disclaimers, exclusive remedy failure, UCC merchantability
