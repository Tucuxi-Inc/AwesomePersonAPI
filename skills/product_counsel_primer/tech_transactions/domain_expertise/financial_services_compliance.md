---
name: financial-services-compliance
description: Financial Services Compliance
tags:
  - banking
  - financial-services
  - fintech
version: '1.0'
confidence_level: HIGH
category: domain_expertise
validated_by: Industry Consensus
validated_date: '2024-10-20'
skill_tier: applied
pattern_tier: 2
mentoring_priority: 5
validation_type: industry_practice
source_type: regulatory_guidance

# Relationships
orchestrated_by:
  - mc25  # Regulatory Path Optimization - sector-specific compliance
knowledge_domain: regulatory_knowledge
cross_references:
  - rg1   # Regulatory Guidance Interpretation
  - regulatory-risk-frameworks  # General regulatory risk
  - cross-border-data-transfers  # International financial regulations
---

# Financial Services Compliance

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**
>
> This Skill was generated synthetically for testing purposes and has not been reviewed by domain experts. Confidence weighting: 0.6 (vs 0.9 for expert-validated Skills).

---

## Metadata

```yaml
skill_id: financial_services_compliance
domain: financial_services
sub_domains:
  - banking_regulation
  - securities_regulation
  - consumer_finance
  - fintech_compliance
  - data_security
jurisdictions:
  - united_states
  - european_union
  - international
confidence: 0.6
validation_status: synthetic
last_updated: 2024-10-26
skill_tier: applied
mentoring_priority: 5
```

---

## Core Principles

### 1. Regulatory Landscape Overview

**US Federal Regulators:**
- **Federal Reserve**: Banks, bank holding companies, financial stability
- **OCC** (Office of the Comptroller of the Currency): National banks, federal savings associations
- **FDIC**: Deposit insurance, bank supervision
- **SEC** (Securities and Exchange Commission): Securities, investment advisers, exchanges
- **FINRA** (Financial Industry Regulatory Authority): Broker-dealers, self-regulatory organization
- **CFPB** (Consumer Financial Protection Bureau): Consumer financial products/services
- **CFTC** (Commodity Futures Trading Commission): Derivatives, futures markets

**EU Regulators:**
- **EBA** (European Banking Authority): Banking regulation, harmonization
- **ESMA** (European Securities and Markets Authority): Securities markets
- **ECB** (European Central Bank): Monetary policy, banking supervision (significant institutions)
- **National Regulators**: FCA (UK), BaFin (Germany), AMF (France), etc.

**Key Regulations:**
- **GLBA** (Gramm-Leach-Bliley Act): Financial privacy, safeguards
- **BSA/AML**: Bank Secrecy Act, Anti-Money Laundering
- **FCRA** (Fair Credit Reporting Act): Credit reporting, consumer rights
- **ECOA** (Equal Credit Opportunity Act): Prohibition on credit discrimination
- **TILA** (Truth in Lending Act): Credit disclosures
- **PCI-DSS**: Payment card industry data security standard
- **SOX** (Sarbanes-Oxley): Public company financial reporting, internal controls
- **MiFID II** (EU): Markets in Financial Instruments Directive
- **PSD2** (EU): Payment Services Directive (open banking)

### 2. Core Compliance Areas

**A. Data Security and Privacy**
- **GLBA Safeguards Rule**: Information security program required
- **PCI-DSS**: Cardholder data protection for payment processing
- **State Laws**: NY DFS Cybersecurity Regulation (23 NYCRR 500), CCPA, etc.

**B. Anti-Money Laundering (AML) and Know Your Customer (KYC)**
- **BSA/AML**: Suspicious activity reporting, customer due diligence
- **OFAC**: Sanctions screening, blocked persons list
- **KYC/CDD**: Customer identification program, beneficial ownership

**C. Consumer Protection**
- **UDAAP**: Unfair, deceptive, or abusive acts or practices
- **FCRA**: Accurate credit reporting, dispute resolution, adverse action notices
- **ECOA**: Fair lending, prohibition on discrimination

**D. Vendor Risk Management**
- **OCC Bulletin 2013-29**: Third-party risk management guidance
- **FFIEC IT Examination Handbook**: Technology service provider oversight
- **Concentration Risk**: Over-reliance on single vendors

---

## Key Validation Considerations

### Claims to Validate

1. **PCI-DSS Compliance Claims**
   - "We're PCI-compliant so we can handle credit card data"
   - **Validation approach**: Request Attestation of Compliance (AOC), verify level (1-4), check scope, confirm annual validation

2. **SOC 2 Type II Claims**
   - "We have SOC 2 certification for our financial services platform"
   - **Validation approach**: Request full report (not just certificate), verify audit period (past 12 months?), check scope includes relevant systems

3. **Vendor Due Diligence Claims**
   - "We've completed vendor due diligence as required by our bank regulators"
   - **Validation approach**: Check if risk assessment conducted, verify controls reviewed, confirm ongoing monitoring plan exists

4. **BSA/AML Compliance Claims**
   - "Our platform has built-in AML monitoring"
   - **Validation approach**: Verify transaction monitoring thresholds, check OFAC screening integration, confirm SAR filing capabilities

5. **Fair Lending Claims**
   - "Our credit algorithm complies with ECOA"
   - **Validation approach**: Request fair lending analysis, verify protected class testing, check for disparate impact

---

## Common Pitfalls

### Data Security Pitfalls

**Weak Safeguards Rule Compliance:**
- ❌ Problem: "We have a firewall, that meets GLBA Safeguards Rule"
- ✅ Better: Comprehensive information security program: risk assessment, access controls, encryption, vendor management, incident response, employee training

**PCI-DSS Scope Creep:**
- ❌ Problem: "We're PCI-compliant for one system but now processing cards on new system"
- ✅ Better: Maintain PCI scope inventory, validate compliance for all systems handling cardholder data, segment networks

**Cloud Security Assumptions:**
- ❌ Problem: "AWS is compliant so we don't need to do anything"
- ✅ Better: Shared responsibility model - AWS secures infrastructure, customer secures applications/data

### Vendor Risk Management Pitfalls

**Inadequate Due Diligence:**
- ❌ Problem: "Vendor completed a questionnaire, we're good"
- ✅ Better: Risk-based due diligence: SOC 2 reports, financial statements, BCP testing, security assessments, regulatory compliance verification

**No Ongoing Monitoring:**
- ❌ Problem: "We did due diligence at contract signing, nothing since"
- ✅ Better: Annual reviews minimum, continuous monitoring for critical vendors, alert triggers (breach, regulatory action, financial distress)

**Missing Contractual Protections:**
- ❌ Problem: "Vendor refuses audit rights or SLA commitments"
- ✅ Better: Right to audit, incident notification (24-48 hours), liability provisions, insurance requirements, regulatory compliance representations

### AML/KYC Pitfalls

**Weak Customer Identification:**
- ❌ Problem: "We collect name and email, that's sufficient KYC"
- ✅ Better: CIP requires name, date of birth, address, identification number (SSN or TIN); verify identity through documents or non-documentary methods

**Inadequate Transaction Monitoring:**
- ❌ Problem: "We flag transactions >$10K as required"
- ✅ Better: Risk-based monitoring considering customer profile, transaction patterns, geography, product type; not just threshold-based

**No Sanctions Screening:**
- ❌ Problem: "We're not a bank so we don't need OFAC screening"
- ✅ Better: OFAC compliance required for any US person/entity; screen customers and transactions against SDN list

### Consumer Protection Pitfalls

**UDAAP Violations:**
- ❌ Problem: "Our terms are in the fine print, customers agreed"
- ✅ Better: Material disclosures must be clear and conspicuous; practices must not be unfair, deceptive, or abusive (CFPB standard)

**FCRA Non-Compliance:**
- ❌ Problem: "We use credit data but don't provide adverse action notices"
- ✅ Better: If using consumer reports for credit decisions, must provide adverse action notice with reason codes and credit bureau contact info

**Fair Lending Issues:**
- ❌ Problem: "Our algorithm is neutral, it treats everyone the same"
- ✅ Better: Equal treatment ≠ fair lending; must test for disparate impact across protected classes (race, gender, age, etc.)

---

## Regulatory Deep Dives

### 1. GLBA and Financial Privacy

**Privacy Rule:**
- **Privacy Notice**: Provide at account opening, annually thereafter
- **Opt-Out**: Allow customers to opt out of information sharing with non-affiliates (except permitted disclosures)
- **Content**: Describe categories of information collected, shared, and safeguarding practices

**Safeguards Rule (Updated 2023):**
- **Risk Assessment**: Identify and assess risks to customer information
- **Security Program**: Designate qualified individual to oversee program
- **Access Controls**: Limit access to authorized personnel only
- **Encryption**: Encrypt customer information in transit and at rest (where feasible)
- **Multi-Factor Authentication**: Implement MFA for accessing customer information systems
- **Vendor Management**: Conduct due diligence and oversight of service providers
- **Incident Response**: Plan for responding to security events
- **Testing**: Regular testing and monitoring of safeguards
- **Annual Reporting**: Report to board of directors annually

### 2. BSA/AML and KYC

**Customer Identification Program (CIP):**
- **Minimum Information**: Name, date of birth, address, identification number
- **Verification**: Document-based (driver's license, passport) or non-documentary (credit bureau check, utility bill)
- **Recordkeeping**: Maintain records for 5 years after account closure

**Customer Due Diligence (CDD) and Beneficial Ownership:**
- **Beneficial Ownership Rule (2018)**: Identify individuals who own ≥25% or control legal entity customers
- **Risk-Based Approach**: Enhanced due diligence for higher-risk customers (PEPs, offshore, high-value transactions)

**Suspicious Activity Reporting (SAR):**
- **Threshold**: $5,000+ for consumer accounts, $2,000+ for money laundering involving bank employees
- **Timing**: File within 30 days of detection (60 days if no subject identified)
- **Confidentiality**: Cannot notify subject of SAR filing ("no tipping off")

**OFAC Sanctions Screening:**
- **SDN List**: Specially Designated Nationals and Blocked Persons
- **50% Rule**: Entities owned ≥50% by blocked persons are also blocked
- **Screening Frequency**: At onboarding and ongoing (ideally real-time for transactions)
- **Blocking Requirements**: Block assets of SDN persons, report to OFAC within 10 days

### 3. PCI-DSS

**Four Levels Based on Transaction Volume:**
- **Level 1**: >6M transactions annually - annual onsite assessment by QSA
- **Level 2**: 1-6M transactions - annual Self-Assessment Questionnaire (SAQ)
- **Level 3**: 20K-1M e-commerce transactions - annual SAQ
- **Level 4**: <20K e-commerce or <1M other - annual SAQ

**12 Requirements (6 Categories):**
1. **Build and Maintain Secure Network**: Firewall, secure configurations
2. **Protect Cardholder Data**: Encryption, truncation, masking
3. **Maintain Vulnerability Management**: Anti-virus, secure systems
4. **Implement Strong Access Controls**: Need-to-know basis, unique IDs, physical access restrictions
5. **Regularly Monitor and Test Networks**: Logging, penetration testing
6. **Maintain Information Security Policy**: Security policy, risk assessments

**SAQ Types:**
- **SAQ A**: E-commerce, redirect to third-party processor (easiest)
- **SAQ D**: All others, most comprehensive

### 4. Model Risk Management (SR 11-7)

**Applicability:**
- Federal Reserve guidance for banks using models
- **Model Definition**: Quantitative method/system/approach applying statistical, economic, financial, or mathematical theories

**Three Lines of Defense:**
1. **Model Developers**: Business units creating/using models
2. **Model Validation**: Independent review (not model developers)
3. **Audit**: Internal audit verification of model risk management

**Model Validation Components:**
- **Conceptual Soundness**: Theory, logic, and assumptions reasonable
- **Ongoing Monitoring**: Performance tracking, outcomes analysis, stability testing
- **Outcomes Analysis**: Comparing model predictions to actual results

**Model Inventory:**
- Maintain inventory of all models
- Tier by risk (high/medium/low)
- Validate high-risk models annually, medium every 2-3 years

---

## Sector-Specific Considerations

### Banking

**Core Banking Systems:**
- **Vendor Concentration**: Heavy reliance on few core banking vendors (FIS, Fiserv, Jack Henry)
- **Conversion Risk**: Switching core systems is complex and risky
- **Regulatory Expectations**: OCC Bulletin 2013-29 on third-party risk management

**Open Banking / API Banking:**
- **PSD2 (EU)**: Mandates bank APIs for account information, payment initiation
- **US Approach**: Voluntary, CFPB Section 1033 (consumer data rights) in development
- **Security**: OAuth 2.0, TLS, strong customer authentication

### Securities and Investment Management

**SEC Cybersecurity Rules:**
- **Regulation S-P**: Privacy notices, safeguards, disposal of consumer information
- **Regulation SCI** (Systems Compliance and Integrity): Critical market infrastructure resiliency
- **Proposed Rules (2023)**: Incident disclosure within 4 days, annual cybersecurity reviews

**Investment Adviser Compliance:**
- **Form ADV**: Disclosure of conflicts, services, fees
- **Custody Rule**: Safeguarding client assets
- **Books and Records**: Maintain records for 5-7 years

### Payment Processing

**Card Network Rules:**
- **Visa, Mastercard Rules**: In addition to PCI-DSS, network-specific requirements
- **Chargeback Thresholds**: Excessive chargebacks can result in fines or termination

**ACH Processing:**
- **Nacha Rules**: Originating depository financial institutions (ODFI) responsible for third-party senders
- **Risk Management**: ODFI must conduct due diligence on TPSOs (third-party sender organizations)

### Consumer Lending

**TILA / Regulation Z:**
- **APR Disclosure**: Annual percentage rate calculation and disclosure
- **Ability to Repay**: Must assess borrower's ability to repay (post-CARD Act)

**FCRA:**
- **Permissible Purpose**: Must have permissible purpose to obtain consumer report
- **Adverse Action**: If credit denied or less favorable terms, provide adverse action notice
- **Risk-Based Pricing**: Notify consumers when they receive less favorable terms based on credit report

**ECOA / Regulation B:**
- **Prohibited Bases**: Race, color, religion, national origin, sex, marital status, age, public assistance
- **Adverse Action**: Provide specific reasons for denial (ECOA Notice)
- **HMDA Reporting**: Home Mortgage Disclosure Act data collection for mortgage lenders

---

## Technology Transactions and Financial Services

### Cloud Services

**Regulatory Guidance:**
- **OCC Bulletin 2020-20**: Cloud computing guidance for banks
- **FFIEC Cloud Computing Guidance**: Risk management, due diligence, contracts

**Key Considerations:**
- **Data Location**: Some regulations require domestic data storage (check jurisdiction)
- **Audit Rights**: Regulators expect audit rights over cloud providers
- **Exit Strategy**: Data portability, transition support if leaving cloud provider
- **Shared Responsibility**: Understand division of security/compliance responsibilities

**Cloud Provider SOC 2:**
- **Type II Required**: Not just Type I (point-in-time)
- **Scope**: Verify scope includes services you're using
- **Bridge Letters**: If audit period gap, request bridge letter

### Fintech Partnerships (Bank-Fintech)

**Regulatory Expectations:**
- **Banks Remain Responsible**: Bank cannot outsource regulatory compliance
- **Fintech as "Service Provider"**: Subject to bank vendor risk management requirements
- **FDIC Guidance**: Guidance on third-party lending

**Common Structures:**
- **Bank Partnership**: Fintech partners with bank, bank originates loans
- **Marketplace Lending**: Platform facilitates lending, may not touch funds
- **BaaS (Banking as a Service)**: Bank provides regulated banking services, fintech provides UX

**Key Risks:**
- **Reputational Risk**: Fintech misconduct reflects on bank partner
- **Compliance Risk**: Fintech may not fully understand regulatory obligations
- **Concentration Risk**: Fintech may represent large portion of bank's lending/deposits

### AI/ML in Financial Services

**Model Risk Management:**
- **SR 11-7 Applicability**: ML models used for credit, risk, capital planning subject to model risk management
- **Validation Challenges**: Black-box models harder to validate than traditional statistical models

**Fair Lending:**
- **Disparate Impact**: ML models must be tested for disparate impact (ECOA, HMDA)
- **Explainability**: FCRA adverse action notices require specific reasons - difficult with black-box models

**Regulatory Guidance:**
- **CFPB**: Guidance on AI/ML in credit underwriting
- **OCC**: Responsible AI in banking
- **FINRA**: AI in broker-dealer compliance

---

## Risk Assessment Framework

### High-Risk Financial Services Scenarios

1. **Direct Bank Partnerships**: Fintech partnering with bank to originate loans/deposits
2. **Payment Processing**: Handling cardholder data, high transaction volumes
3. **Credit Decisioning**: Automated underwriting, potential fair lending issues
4. **Cross-Border Services**: Multi-jurisdictional regulatory complexity
5. **Novel Technologies**: Crypto, DeFi, blockchain in regulated financial services

### Medium-Risk Financial Services Scenarios

1. **Financial Data Aggregation**: Account aggregation, personal financial management
2. **Investment Advice**: Robo-advisors, automated recommendations
3. **Business-to-Business Fintech**: Commercial payments, corporate cards
4. **White-Label Services**: Providing technology to regulated financial institutions

### Low-Risk Financial Services Scenarios

1. **Non-Financial Services**: Marketing, HR tools for financial institutions (no regulated data)
2. **Public Data**: Market data, research, publicly available information
3. **Internal Tools**: Development tools, productivity software with no financial data access

---

## Validation Questions to Ask

When reviewing financial services compliance in technology transactions, ask:

1. ✅ **Which regulators have jurisdiction?** (Federal, state, SROs like FINRA)
2. ✅ **Is the vendor subject to PCI-DSS?** (If handling cardholder data, what level?)
3. ✅ **Does vendor have SOC 2 Type II report?** (Request full report, verify scope and audit date)
4. ✅ **What is the vendor risk tier?** (Critical, high, medium, low - determines due diligence depth)
5. ✅ **Are audit rights included in contract?** (Right to audit, regulatory access)
6. ✅ **What are incident notification timelines?** (24-48 hours typical for critical vendors)
7. ✅ **Is there a business continuity plan?** (RTO/RPO, disaster recovery, testing frequency)
8. ✅ **Are there subcontracting restrictions?** (Notice, approval, flow-down of obligations)
9. ✅ **What insurance does vendor carry?** (Cyber, E&O, amounts)
10. ✅ **How is data handled at termination?** (Return, destruction, certification)

---

## Example Validation Scenarios

### Scenario 1: Cloud Banking Platform

**Claim:** "Our cloud-based core banking system is fully compliant with all banking regulations"

**Validation Steps:**
1. Request SOC 2 Type II report:
   - Verify audit date (within last 12 months)
   - Check scope includes production systems
   - Review exceptions/qualifications in auditor opinion
2. Review GLBA Safeguards compliance:
   - Encryption in transit and at rest?
   - MFA implemented?
   - Annual risk assessment conducted?
3. Assess vendor risk management:
   - Financial stability of vendor (audited financials)
   - Concentration risk (what % of customers would this vendor represent?)
   - BCP/DR testing results
4. Check regulatory guidance compliance:
   - OCC Bulletin 2020-20 (cloud computing) requirements met?
   - FFIEC guidance addressed?
5. Review contract terms:
   - Audit rights for bank and regulators?
   - Data location commitments?
   - Incident notification (24-48 hours)?

**Confidence:** MEDIUM (need to review SOC 2 and vendor due diligence materials)

**Red Flag:** "Fully compliant with all regulations" - compliance is shared responsibility; vendor provides controls, bank must implement/configure properly

### Scenario 2: Fintech Lending Platform Partnering with Bank

**Claim:** "We handle all lending operations; the bank just holds the loans on their balance sheet"

**Validation Steps:**
1. Assess true lender determination:
   - Who makes credit decision (bank or fintech)?
   - Whose name is on loan agreement?
   - Who has predominant economic interest?
   - **Risk**: "Rent-a-charter" concerns if fintech is de facto lender
2. Review bank vendor risk management:
   - Has bank conducted due diligence on fintech?
   - Ongoing monitoring plan in place?
   - Board awareness and approval of partnership?
3. Check consumer protection compliance:
   - TILA disclosures provided correctly?
   - FCRA adverse action notices sent timely?
   - Fair lending analysis conducted (ECOA, HMDA)?
4. Assess AML/BSA compliance:
   - KYC/CIP conducted for borrowers?
   - SAR filing procedures if suspicious activity detected?
   - OFAC screening performed?
5. Review concentration risk:
   - What % of bank's loan portfolio is from this fintech?
   - Diversification of funding sources?

**Confidence:** LOW-MEDIUM (fintech-bank partnerships carry significant regulatory scrutiny)

**Key Concern:** Regulators increasingly skeptical of "rent-a-charter" arrangements; bank must retain meaningful control and compliance oversight

### Scenario 3: Payment Processing with PCI-DSS

**Claim:** "We're PCI Level 1 compliant and undergo annual assessments"

**Validation Steps:**
1. Request Attestation of Compliance (AOC):
   - Verify signed by QSA (Qualified Security Assessor)
   - Check compliance date (annual validation required)
   - Confirm scope includes systems in your processing flow
2. Review ASV (Approved Scanning Vendor) reports:
   - Quarterly vulnerability scans required
   - Check for failed scans or outstanding vulnerabilities
3. Verify compensating controls:
   - If any requirements not fully met, are compensating controls adequate?
   - Documented and approved by QSA?
4. Assess card brand compliance:
   - Visa/Mastercard compliant (beyond PCI-DSS)?
   - Registered with card brands as service provider?
5. Check incident response:
   - Does vendor have forensic investigation plan if breach occurs?
   - Forensic investigator on retainer (PFI - PCI Forensic Investigator)?

**Confidence:** MEDIUM-HIGH (if AOC and ASV reports verified)

**Ongoing Monitoring:** PCI compliance is point-in-time; request quarterly ASV scans and annual AOC renewal

---

## Current Developments (2024)

### Open Banking Evolution
- **CFPB Section 1033 Rulemaking**: Consumer data rights, API standards, liability allocation
- **US Lags EU**: PSD2 mandates bank APIs; US still voluntary

### Crypto Regulation
- **SEC Enforcement**: Many crypto tokens treated as securities
- **Banking Agency Guidance**: Crypto activities by banks require notification/approval
- **Stablecoin Regulation**: Proposed legislation for reserve requirements, redemption rights

### AI/ML in Credit
- **CFPB Guidance**: AI explainability in credit decisions, fair lending testing
- **Model Risk Management**: Extending SR 11-7 to ML models
- **NYC AI Law**: Automated employment decision tools (intersects with credit background checks)

---

## When to Consult Domain Experts

This synthetic Skill provides foundational knowledge. **Consult financial services compliance experts for:**

1. **Bank Partnerships**: Fintech-bank partnerships, BaaS arrangements
2. **Complex Vendor Arrangements**: Critical vendor due diligence, contracts
3. **Regulatory Examinations**: OCC, Federal Reserve, CFPB exams or enforcement
4. **Novel Products**: Crypto, embedded finance, BNPL (buy now pay later)
5. **Cross-Border Financial Services**: Multi-jurisdictional licensing and compliance
6. **Fair Lending Analysis**: Testing credit models for disparate impact

**Assume:** This Skill covers 60-70% of standard fintech compliance scenarios. Bank partnerships, regulatory exams, and novel products require specialized legal and compliance expertise.

---

## References and Learning Resources

**Primary Regulations:**
- GLBA (15 USC 6801 et seq.) and Regulations P (privacy) and S-P (SEC privacy)
- BSA/AML (31 USC 5311 et seq. and 31 CFR Chapter X)
- FCRA (15 USC 1681 et seq.) and Regulation V
- ECOA (15 USC 1691 et seq.) and Regulation B
- PCI-DSS v4.0 (March 2022)

**Regulatory Guidance:**
- OCC Bulletin 2013-29 (Third-Party Risk Management)
- OCC Bulletin 2020-20 (Cloud Computing)
- FFIEC IT Examination Handbook
- Federal Reserve SR 11-7 (Model Risk Management)

**Industry Standards:**
- NIST Cybersecurity Framework
- ISO 27001 (Information Security)
- SOC 2 Trust Service Criteria

**⚠️ Note:** As a synthetic Skill, these references have not been verified by experts. Financial services regulation evolves rapidly - consult current legal and regulatory guidance before making compliance decisions.
