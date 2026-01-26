---
name: government-sector-requirements
description: Government Sector Requirements
tags:
  - government
  - procurement
  - public-sector
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
  - mc21  # Organizational Political Intelligence - government as stakeholder
  - mc25  # Regulatory Path Optimization - procurement regulations
knowledge_domain: industry_practices
cross_references:
  - s14   # Stakeholder Interest Analysis (government as stakeholder)
  - es1   # Escalation Strategy (government decision processes)
  - regulatory-risk-frameworks  # Government regulatory environment
---

# Government Sector Requirements

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**
>
> This Skill was generated synthetically for testing purposes and has not been reviewed by domain experts. Confidence weighting: 0.6 (vs 0.9 for expert-validated Skills).

---

## Metadata

```yaml
skill_id: government_sector_requirements
domain: government_contracting
sub_domains:
  - federal_acquisition
  - cybersecurity_compliance
  - data_sovereignty
  - clearance_requirements
  - procurement_regulations
jurisdictions:
  - united_states_federal
  - united_states_state_local
  - international
confidence: 0.6
validation_status: synthetic
last_updated: 2024-10-26
skill_tier: applied
mentoring_priority: 5
```

---

## Core Principles

### 1. Government Contracting Overview

**Federal Acquisition Regulation (FAR):**
- Governs federal government procurement
- Applies to all executive agencies
- **Prime Contractors**: Direct contracts with government
- **Subcontractors**: Contracts with primes, many FAR clauses flow down

**Key Characteristics of Government Contracting:**
- **Publicity**: FOIA, public scrutiny
- **Competition**: Preference for competitive bidding
- **Socioeconomic Programs**: Small business set-asides, disadvantaged business programs
- **Buy American**: Preference for domestic products
- **Complex Compliance**: Numerous regulations, certifications, audits

### 2. Contract Types

**GSA Schedules:**
- Pre-negotiated contracts with GSA
- Other agencies can purchase off schedule (fast procurement)
- **Advantage**: Streamlined purchasing for agencies
- **Requirements**: Pricing disclosure, commercial item, Most Favored Customer

**IDIQs (Indefinite Delivery, Indefinite Quantity):**
- Master contract with multiple task orders
- **GWACs** (Government-Wide Acquisition Contracts): Available to all agencies
- **Examples**: Alliant 2, 8(a) STARS III

**BPAs (Blanket Purchase Agreements):**
- Simplified procurement for recurring needs
- Often built off GSA Schedules

**Contract Pricing:**
- **Firm-Fixed-Price (FFP)**: Set price, contractor bears risk
- **Time and Materials (T&M)**: Hourly rate + materials
- **Cost-Plus**: Reimbursement + fee, government bears risk

### 3. Key Compliance Frameworks

**FedRAMP (Federal Risk and Authorization Management Program):**
- **Purpose**: Standardize security assessment for cloud services
- **Levels**: Low, Moderate, High impact (based on FIPS 199)
- **Process**: Sponsoring agency or JAB (Joint Authorization Board) authorizes
- **Timing**: 6-18 months for initial authorization
- **Marketplace**: FedRAMP Marketplace lists authorized services

**NIST 800-171 (Protecting CUI):**
- **CUI**: Controlled Unclassified Information (not classified but sensitive)
- **Applicability**: Defense contractors, federal contractors handling CUI
- **Requirements**: 110 security controls (14 families)
- **CMMC**: Cybersecurity Maturity Model Certification (DoD requirement building on 800-171)

**FISMA (Federal Information Security Management Act):**
- Requires federal agencies to secure information systems
- **Risk Management Framework (RMF)**: NIST SP 800-37
- **ATO (Authority to Operate)**: Agency authorization for systems processing federal data

**Section 508 (Accessibility):**
- **Rehabilitation Act**: Federal IT must be accessible to people with disabilities
- **WCAG 2.0 Level AA**: Web Content Accessibility Guidelines standard
- **VPAT** (Voluntary Product Accessibility Template): Vendor self-assessment

---

## Key Validation Considerations

### Claims to Validate

1. **FedRAMP Authorization Claims**
   - "We're FedRAMP certified"
   - **Validation approach**: Check FedRAMP Marketplace (only place to verify), confirm authorization level (Low/Moderate/High), verify agency sponsorship or JAB

2. **NIST 800-171 Compliance Claims**
   - "We're fully compliant with NIST 800-171"
   - **Validation approach**: Request self-assessment results (SSP - System Security Plan, POA&M - Plan of Action and Milestones), check CMMC certification if DoD, verify independent assessment

3. **Section 508 Compliance Claims**
   - "Our software is Section 508 compliant"
   - **Validation approach**: Request VPAT (Voluntary Product Accessibility Template), verify testing methodology, check for known accessibility issues

4. **Clearance Facility Claims**
   - "We have a cleared facility for classified work"
   - **Validation approach**: Verify FCL (Facility Clearance Level) with DCSA (Defense Counterintelligence and Security Agency), check CAGE code, confirm cleared personnel available

5. **Small Business Status Claims**
   - "We're a certified small business"
   - **Validation approach**: Check SAM.gov registration, verify size standard for NAICS code, confirm SBA certifications (8(a), HUBZone, WOSB, etc.)

---

## Common Pitfalls

### FedRAMP Pitfalls

**"FedRAMP Ready" vs "FedRAMP Authorized":**
- ❌ Problem: "We're FedRAMP Ready so agencies can use us"
- ✅ Reality: FedRAMP Ready ≠ Authorized; agencies still need to issue ATO or accept existing authorization

**Wrong Impact Level:**
- ❌ Problem: "We're FedRAMP Moderate but agency needs High"
- ✅ Better: Verify agency requirements match authorization level; reauthorization at higher level takes months

**Authorization Reciprocity Issues:**
- ❌ Problem: "We have FedRAMP so all agencies will accept it"
- ✅ Reality: Agencies can require additional controls; reciprocity encouraged but not guaranteed

### NIST 800-171 Pitfalls

**Self-Assessment Only:**
- ❌ Problem: "We completed the self-assessment, we're compliant"
- ✅ Better: Self-assessment is minimum; DoD contractors need CMMC certification (third-party assessment)

**Missing POA&M:**
- ❌ Problem: "We're not compliant with all 110 controls but that's okay"
- ✅ Better: Must document deficiencies in POA&M with remediation timeline; some gaps acceptable if documented

**No Independent Assessment:**
- ❌ Problem: "IT department assessed ourselves as compliant"
- ✅ Better: Independent assessment required (CMMC C3POs, or internal audit separate from IT)

### Section 508 Pitfalls

**Outdated VPAT:**
- ❌ Problem: "We have a VPAT from 2018"
- ✅ Better: VPAT should reflect current version; agencies may require current assessment

**Partial Compliance:**
- ❌ Problem: "Most features are accessible, that's good enough"
- ✅ Better: Full compliance required; document any limitations in VPAT, may need workarounds

**No Testing:**
- ❌ Problem: "We self-certified without testing"
- ✅ Better: Use accessibility testing tools (JAWS, NVDA screen readers, automated scanners), user testing with people with disabilities

---

## Detailed Compliance Frameworks

### 1. FedRAMP Deep Dive

**Impact Levels:**

| Level | Description | Example Use Cases | Security Controls |
|-------|-------------|-------------------|-------------------|
| **Low** | Loss has limited adverse effect | Public websites, basic collaboration | 125 baseline controls |
| **Moderate** | Loss has serious adverse effect | Most federal systems | 325 baseline controls |
| **High** | Loss has severe/catastrophic effect | Law enforcement, emergency services, financial systems | 421 baseline controls |

**Authorization Process:**

1. **FedRAMP Ready** (Optional):
   - 3PAO (Third-Party Assessment Organization) conducts readiness assessment
   - Package submitted to FedRAMP PMO for review
   - Listed on marketplace as "FedRAMP Ready"
   - **Not authorized** - cannot process federal data yet

2. **Agency Authorization**:
   - CSP partners with sponsoring agency
   - 3PAO conducts security assessment
   - Agency reviews and issues ATO (Authority to Operate)
   - **Timeline**: 3-6 months (if well-prepared)

3. **JAB Authorization** (P-ATO):
   - Joint Authorization Board (DoD, DHS, GSA representatives)
   - More rigorous review process
   - Results in P-ATO (Provisional ATO) accepted by multiple agencies
   - **Timeline**: 9-18 months

**Continuous Monitoring:**
- Monthly vulnerability scans
- Annual assessments
- Incident reporting within timeframes (1 hour for High impact incidents)

**Common FedRAMP Pain Points:**
- **Documentation**: Hundreds of pages required (SSP, SAP, SAR, POA&M)
- **Cost**: $250K-$1M+ for initial authorization
- **Time**: 6-18 months minimum
- **Ongoing Compliance**: Monthly/annual requirements

### 2. NIST 800-171 and CMMC

**NIST 800-171 Control Families (14 families, 110 controls):**
1. Access Control (22 controls)
2. Awareness and Training (3 controls)
3. Audit and Accountability (9 controls)
4. Configuration Management (9 controls)
5. Identification and Authentication (11 controls)
6. Incident Response (3 controls)
7. Maintenance (6 controls)
8. Media Protection (9 controls)
9. Personnel Security (2 controls)
10. Physical Protection (6 controls)
11. Risk Assessment (3 controls)
12. Security Assessment (4 controls)
13. System and Communications Protection (17 controls)
14. System and Information Integrity (6 controls)

**CMMC 2.0 (DoD's Evolution of 800-171):**

| Level | Requirements | Assessment | Applicable Contracts |
|-------|--------------|------------|---------------------|
| **Level 1** | Basic cyber hygiene (17 practices) | Annual self-assessment | FCI (Federal Contract Information) only |
| **Level 2** | NIST 800-171 (110 controls) | Self-assessment (with affirmation) OR third-party (for critical programs) | CUI (Controlled Unclassified Information) |
| **Level 3** | NIST 800-171 + advanced (24 additional) | Government-led assessment | Critical national security programs |

**CMMC Timeline:**
- Rulemaking in progress (as of 2024)
- Phased implementation expected
- All DoD contracts will eventually require CMMC

**Supplier Performance Risk System (SPRS):**
- DoD contractors must submit 800-171 scores to SPRS
- Score of 110 = full compliance
- Scores <110 must have POA&M

### 3. ITAR and Export Controls

**ITAR (International Traffic in Arms Regulations):**
- **Applicability**: Defense articles, technical data, defense services
- **Registration**: Companies must register with DDTC (Directorate of Defense Trade Controls)
- **License Requirements**: Exports, re-exports, temporary imports require licenses
- **Exemptions**: Canada (limited), NATO allies (limited)

**EAR (Export Administration Regulations):**
- **Applicability**: Dual-use items (commercial items with potential military applications)
- **BIS**: Bureau of Industry and Security administers
- **ECCN** (Export Control Classification Number): Determines if item subject to EAR

**Technology Considerations:**
- **Cloud Storage**: ITAR data cannot be stored on foreign servers or accessed by foreign nationals (including sysadmins)
- **Deemed Exports**: Sharing ITAR/EAR data with foreign nationals in US is an "export"
- **Encryption**: Strong encryption (>56-bit symmetric) is export-controlled under EAR

---

## Procurement and Contracting

### 1. FAR Clauses (Flowdown Requirements)

**Common Clauses That Flow Down to Subcontractors:**
- **52.204-21**: Basic Safeguarding of Covered Contractor Information Systems (NIST 800-171 lite)
- **52.204-25**: Prohibition on Contracting for Certain Telecommunications (Huawei, ZTE ban)
- **52.219-8**: Utilization of Small Business Concerns (subcontracting plan)
- **52.222-26**: Equal Opportunity (affirmative action)
- **52.222-35**: Equal Opportunity for Veterans
- **52.222-36**: Equal Opportunity for Workers with Disabilities
- **52.222-50**: Combating Trafficking in Persons
- **52.223-18**: Encouraging Contractor Policies to Ban Text Messaging While Driving
- **52.225-13**: Restrictions on Certain Foreign Purchases (Buy American Act)

**DFARS Clauses (Defense-Specific):**
- **252.204-7012**: Safeguarding Covered Defense Information (NIST 800-171 full)
- **252.204-7019**: Notice of NIST SP 800-171 DoD Assessment Requirements (CMMC)
- **252.204-7020**: NIST SP 800-171 DoD Assessment Requirements (CMMC certification)

### 2. Small Business Programs

**Types of Small Business Certifications:**
- **Small Business (SB)**: Meets SBA size standard for NAICS code
- **8(a)**: Socially and economically disadvantaged (9-year program)
- **HUBZone**: Historically Underutilized Business Zones
- **SDVOSB**: Service-Disabled Veteran-Owned Small Business
- **WOSB**: Women-Owned Small Business
- **EDWOSB**: Economically Disadvantaged WOSB

**Set-Asides:**
- Contracts reserved for certified small businesses
- Compete only against other small businesses
- **Sole-Source**: Certain programs allow sole-source awards (e.g., 8(a) up to $4.5M)

**Subcontracting Plans:**
- Large businesses must have small business subcontracting plan
- Goals for SB, 8(a), HUBZone, SDVOSB, WOSB utilization
- Reported in eSRS (Electronic Subcontracting Reporting System)

---

## Technology Transactions Specific Issues

### Cloud Services for Government

**FedRAMP vs. DoD IL (Impact Levels):**
- **FedRAMP**: Civilian agencies
- **DoD IL**: Department of Defense cloud environment
  - IL2: Public data
  - IL4: CUI (NIST 800-171 required)
  - IL5: CUI + National Security Systems (NIST 800-53 Moderate)
  - IL6: Classified Secret

**Government Cloud Regions:**
- **AWS GovCloud**: ITAR, FedRAMP High, DoD IL 4-5
- **Azure Government**: FedRAMP High, DoD IL 5-6
- **Google Cloud for Government**: FedRAMP Moderate/High

**Key Considerations:**
- **Data Residency**: Must be in US, personnel must be US persons (for ITAR)
- **Network Isolation**: Government regions isolated from commercial
- **Background Checks**: Personnel may need clearances or suitability determinations

### Software Licensing for Government

**Commercial Off-the-Shelf (COTS):**
- Standard commercial software
- **Advantages**: Faster procurement, proven technology, lower cost
- **FAR 12**: Simplified acquisition procedures for commercial items

**Government Purpose Rights:**
- Government gets broad rights to use software across agencies
- Contractor retains ownership, can license to others
- **Typical Rights**: Install on government systems, allow government contractors to use

**Unlimited Rights:**
- Government can distribute, modify, release publicly
- Rare for commercial software, common for custom development
- **Triggers**: Government funding of development, negotiated in contract

**Open Source in Government:**
- **Generally Allowed**: If consistent with contract terms
- **Security Review**: Same scrutiny as commercial software
- **DFARS 252.227-7014**: Special license rights for open source

### SaaS for Government

**Authority to Operate (ATO):**
- Each agency must issue ATO (even with FedRAMP authorization)
- **Timeline**: 1-6 months (less if FedRAMP authorized)
- **Requirements**: Agency-specific controls, IA (Information Assurance) review

**Terms and Conditions:**
- **Federal Jurisdiction**: Disputes resolved in federal court
- **Indemnification**: Often prohibited or limited (Anti-Deficiency Act)
- **Sovereign Immunity**: Government cannot be sued without consent
- **Assignment**: Government may assign contract to successor agency

**Data Rights:**
- Government retains ownership of its data
- Vendor must return/destroy data upon termination
- **FOIA**: Government data may be subject to Freedom of Information Act requests

---

## Risk Assessment Framework

### High-Risk Government Contracting Scenarios

1. **Classified Work**: Requires FCL, cleared personnel, SCIF (Sensitive Compartmented Information Facility)
2. **ITAR Data**: Export-controlled defense articles, foreign access restrictions
3. **DoD CUI**: NIST 800-171, CMMC certification requirements
4. **FedRAMP High**: Critical systems, extensive controls, high cost
5. **Section 508 Critical Failures**: Inaccessible software for core functions

### Medium-Risk Government Contracting Scenarios

1. **FedRAMP Moderate**: Standard civilian agency cloud services
2. **NIST 800-171**: Non-DoD CUI, self-assessment acceptable
3. **GSA Schedule**: Pricing disclosure, most favored customer, audit risk
4. **Small Business Set-Asides**: Compliance with size standards, affiliation rules

### Low-Risk Government Contracting Scenarios

1. **Public Data**: FedRAMP Low, minimal security requirements
2. **Commercial Products**: COTS software, standard terms
3. **Non-Sensitive Services**: Professional services, no CUI/PII

---

## Validation Questions to Ask

When reviewing government sector technology requirements, ask:

1. ✅ **Which agencies are the end customers?** (Civilian vs. DoD, federal vs. state/local)
2. ✅ **What is the required FedRAMP impact level?** (Low, Moderate, High - or DoD IL)
3. ✅ **Is CUI or classified data involved?** (Determines NIST 800-171, CMMC, clearance needs)
4. ✅ **Is ITAR or EAR applicable?** (Defense articles, export controls, foreign access restrictions)
5. ✅ **What accessibility level is required?** (Section 508, WCAG 2.0 Level AA, VPAT)
6. ✅ **Are there small business requirements?** (Set-asides, subcontracting plan goals)
7. ✅ **What FAR/DFARS clauses flow down?** (NIST 800-171, telecommunications ban, trafficking, etc.)
8. ✅ **What are the data rights?** (Government purpose, unlimited, limited rights)
9. ✅ **Is there a clearance requirement?** (Facility clearance, personnel clearances)
10. ✅ **What is the contract vehicle?** (GSA Schedule, IDIQ, direct contract, subcontract)

---

## Example Validation Scenarios

### Scenario 1: Cloud Platform Seeking FedRAMP Moderate

**Claim:** "We're pursuing FedRAMP Moderate authorization to serve civilian agencies"

**Validation Steps:**
1. Assess readiness:
   - Is system architected for FedRAMP (boundary definition, control inheritance)?
   - Are 325 Moderate baseline controls implemented?
   - Is documentation ready (SSP, 1000+ pages typical)?
2. Check partnership:
   - Is there a sponsoring agency (required for Agency ATO path)?
   - Or pursuing JAB P-ATO (no sponsor needed but longer process)?
3. Verify 3PAO engagement:
   - Is a FedRAMP-recognized 3PAO selected?
   - Cost estimate ($100K-$500K+ for assessment)?
4. Timeline expectations:
   - Understand 6-18 month timeline realistic?
   - Ongoing continuous monitoring requirements (monthly scans, annual assessments)?
5. Commercial viability:
   - What is cost to achieve FedRAMP vs. expected government revenue?
   - Can business sustain ongoing compliance costs?

**Confidence:** MEDIUM (FedRAMP process well-documented but complex)

**Reality Check:** FedRAMP is expensive and time-consuming; ensure strong government market demand before pursuing

### Scenario 2: Defense Contractor Handling CUI

**Claim:** "We're a subcontractor on DoD program and we're NIST 800-171 compliant based on our self-assessment"

**Validation Steps:**
1. Verify CMMC requirements:
   - When will prime contract require CMMC certification? (Check CMMC 2.0 timeline)
   - Is this a critical national security program (CMMC Level 3)?
2. Check self-assessment:
   - Has contractor documented assessment in SSP (System Security Plan)?
   - Are deficiencies documented in POA&M with remediation dates?
   - What is SPRS score (should be submitted to DoD)?
3. Assess actual compliance:
   - Request evidence for key controls (access control, multi-factor authentication, encryption, incident response)
   - Are all 14 control families addressed?
4. Verify subcontract flow-down:
   - Does prime contract include DFARS 252.204-7012?
   - Is contractor required to flow down to sub-subcontractors?
5. Third-party assessment readiness:
   - When CMMC required, can contractor pass C3PAO assessment?
   - Estimated cost: $15K-$150K depending on scope

**Confidence:** MEDIUM-LOW (self-assessments often overstate compliance)

**Common Issue:** Many contractors claim full compliance but have significant gaps; independent assessment reveals deficiencies

### Scenario 3: SaaS Platform for Multiple Agencies

**Claim:** "Our SaaS platform has FedRAMP Moderate authorization so all agencies can use it immediately"

**Validation Steps:**
1. Verify FedRAMP status:
   - Check FedRAMP Marketplace (official source)
   - Is it Agency ATO or JAB P-ATO?
   - When does authorization expire (annual assessment required)?
2. Assess agency-specific requirements:
   - Does target agency accept existing ATO or require additional controls?
   - Reciprocity encouraged but not guaranteed
   - Timeline for agency ATO: 1-6 months even with FedRAMP
3. Review contract terms:
   - Are terms and conditions acceptable to federal agencies?
   - Jurisdiction, indemnification, data rights addressed?
4. Check for agency-specific barriers:
   - DoD: May require DoD IL instead of FedRAMP
   - Intelligence Community: May require ICD 503 instead of FedRAMP
5. Verify continuous monitoring:
   - Are monthly ConMon reports submitted timely?
   - Any outstanding POA&M items that could block agency adoption?

**Confidence:** MEDIUM-HIGH (if FedRAMP verification confirmed on Marketplace)

**Key Point:** FedRAMP accelerates agency adoption but doesn't guarantee immediate use; each agency still issues own ATO

---

## Current Developments (2024)

### CMMC 2.0 Rulemaking
- **Status**: Proposed rule published, final rule expected 2024-2025
- **Phased Implementation**: Critical programs first, then broader DoD contracts
- **Certification Ecosystem**: C3PAOs (CMMC Third-Party Assessment Organizations), training programs

### FedRAMP Modernization
- **FedRAMP Rev. 5**: Updated to NIST SP 800-53 Rev. 5 baseline
- **Automation**: Increased use of OSCAL (Open Security Controls Assessment Language)
- **Timelines**: Efforts to reduce authorization timeline

### Zero Trust Architecture
- **OMB Memo M-22-09**: Requires federal agencies to implement zero trust
- **CISA Guidance**: Zero Trust Maturity Model
- **Vendor Impact**: Solutions must support zero trust principles (identity-centric, least privilege, continuous monitoring)

---

## When to Consult Domain Experts

This synthetic Skill provides foundational knowledge. **Consult government contracting experts for:**

1. **FedRAMP Authorization**: Pursuing initial authorization or annual reassessment
2. **CMMC Certification**: Preparing for DoD assessment, remediation planning
3. **ITAR Compliance**: Defense articles, export control classifications
4. **GSA Schedule**: Application process, pricing strategy, negotiations
5. **Complex Procurements**: Large IDIQs, competitive full-and-opens, protests
6. **Clearance Facility**: Establishing FCL, SCIF requirements, classified work

**Assume:** This Skill covers 50-60% of government technology contracting scenarios. FedRAMP, CMMC, and complex procurement require specialized consulting and legal expertise.

---

## References and Learning Resources

**Primary Regulations:**
- FAR (Federal Acquisition Regulation) - 48 CFR
- DFARS (Defense FAR Supplement) - 48 CFR 200-299
- ITAR (International Traffic in Arms Regulations) - 22 CFR 120-130
- EAR (Export Administration Regulations) - 15 CFR 730-774

**Security Frameworks:**
- NIST SP 800-171 Rev. 2 (Protecting CUI)
- NIST SP 800-53 Rev. 5 (Security and Privacy Controls)
- NIST SP 800-37 Rev. 2 (Risk Management Framework)
- FedRAMP Security Controls Baseline

**Compliance Resources:**
- FedRAMP.gov (official marketplace and guidance)
- CMMC-AB.org (CMMC Accreditation Body)
- SAM.gov (System for Award Management - registrations, contracts)
- Section508.gov (accessibility guidance)

**⚠️ Note:** As a synthetic Skill, these references have not been verified by experts. Government contracting regulations evolve - consult current official sources and legal counsel before making compliance decisions.
