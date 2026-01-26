---
name: export-controls
description: Export Controls
tags:
  - compliance
  - export-controls
  - sanctions
version: '1.0'
confidence_level: MEDIUM
category: core_legal_frameworks
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
mentoring_priority: 2
validation_type: synthetic
source_type: regulatory_guidance
---

# Export Controls and Trade Compliance

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**

## Metadata

```yaml
skill_id: export_controls
domain: legal_fundamentals
sub_domains: [ear, itar, ofac, deemed_exports, encryption, technology_transfers]
jurisdictions: [united_states, international]
confidence: 0.70
validation_status: synthetic
requires: [keller_patterns, contract_law]
complements: [technology_licensing, international_tax, data_agreements]
skill_tier: foundational
mentoring_priority: 2
```

## Core Principles

### What are Export Controls?

**Definition**: Laws restricting export of goods, software, technology, and services from one country to another

**Three Primary US Export Control Regimes**:
1. **EAR** (Export Administration Regulations) - Commerce Department (BIS)
2. **ITAR** (International Traffic in Arms Regulations) - State Department (DDTC)
3. **OFAC** (Office of Foreign Assets Control) - Treasury Department (sanctions)

**Why Export Controls Matter for Tech**:
- **Software**: Source code, encryption, technical data may be controlled
- **Cloud Services**: Foreign access to US servers may trigger export
- **Deemed Exports**: Sharing with foreign nationals in US = export
- **International Customers**: Export licenses may be required for certain countries/end-users

## EAR (Export Administration Regulations)

### Scope and Jurisdiction

**Administered By**: Bureau of Industry and Security (BIS), US Department of Commerce

**What is Controlled**:
- **Dual-Use Items**: Commercial items with potential military application
- **Commercial Software**: Encryption, cybersecurity tools, AI/ML algorithms
- **Technology and Technical Data**: Blueprints, designs, source code, know-how
- **Foreign-Made Items**: Items incorporating >25% US-origin controlled content (de minimis rule)

**Jurisdictional Triggers**:
- **Export**: Shipment from US to foreign country
- **Re-export**: Transfer from one foreign country to another (if item subject to EAR)
- **Transfer**: Release of technology/source code to foreign person (domestically or abroad)
- **Deemed Export**: Release to foreign national in US (even if no physical export)

### ECCN (Export Control Classification Number)

**Structure**: 5-character alphanumeric code (e.g., 5D002)
- **First Character**: Category (0-9)
  - **3**: Electronics
  - **4**: Computers
  - **5**: Telecommunications and Information Security
- **Second Character**: Product group (A-E)
  - **A**: Systems, equipment, assemblies
  - **B**: Test, inspection, production equipment
  - **C**: Materials
  - **D**: Software
  - **E**: Technology (technical data)
- **Third Character**: Type of control (reasons for control)
- **Last Two Characters**: Sequence number

**Example**: **5D002** - "Information security" software (encryption > 56-bit symmetric)

**EAR99**: Items not listed on Commerce Control List (CCL) - generally low-level technology (minimal controls, but still subject to OFAC sanctions)

### License Requirements and Exceptions

**When License Required**:
- **Destination**: Country subject to sanctions or restrictions (China, Russia for certain items)
- **End-User**: Entity on denied parties list, military end-use, nuclear activities
- **End-Use**: WMD (weapons of mass destruction), military, terrorism

**License Exceptions** (No License Needed If Qualify):

**NLR** (No License Required):
- Items designated EAR99 to most destinations (except embargoed countries)

**ENC** (Encryption):
- **Mass Market Software**: Encryption software generally available to public (e.g., HTTPS, SSL, commercial encryption)
- **Self-Classification Report**: File one-time notification with BIS (SNAP-R system)
- **Exception**: Can export/re-export without license to most destinations (except embargoed countries)

**TSU** (Technology and Software - Unrestricted):
- Source code publicly available (open source)
- Educational information (not directly related to design/production)
- Patent information

**Other Common Exceptions**:
- **TMP**: Temporary exports/imports (trade shows, demos)
- **RPL**: Replacement parts
- **BAG**: Personal use items (laptop, phone)

### Deemed Exports

**Definition**: Release of controlled technology or source code to foreign national in US

**Trigger**: Showing source code to foreign national employee, contractor, student (even in US office)

**License May Be Required If**:
- Technology is controlled (high ECCN)
- Foreign national's country requires license (China, Russia, etc.)

**Exemptions**:
- **Fundamental Research**: Publicly available research (university setting, no export-controlled data)
- **Educational Information**: General scientific, mathematical, engineering principles taught in courses

**Practical Impact**:
- Hiring foreign nationals may require export license (or limit access to controlled technology)
- Cloud servers accessible by foreign admin may trigger deemed export

### Technology Control Plans (TCP)

**Purpose**: Internal compliance program to prevent unauthorized technology transfers

**Elements**:
- **Classification**: Identify all ECCN-controlled technology (source code, algorithms, designs)
- **Access Controls**: Restrict access to controlled technology (need-to-know basis)
- **Training**: Export compliance training for employees with access
- **Screening**: Screen foreign nationals for export license requirements
- **Audits**: Periodic audits to ensure compliance

**When Required**: Companies regularly working with controlled technology (encryption, cybersecurity, AI/ML)

## ITAR (International Traffic in Arms Regulations)

### Scope and Jurisdiction

**Administered By**: Directorate of Defense Trade Controls (DDTC), US Department of State

**What is Controlled**:
- **Defense Articles**: Items on US Munitions List (USML) - military equipment, weapons, spacecraft
- **Defense Services**: Assistance related to defense articles (design, manufacture, operation, repair)
- **Technical Data**: Information required for design, development, production, use of defense articles

**USML Categories** (21 categories):
- Category I: Firearms, close assault weapons
- Category IV: Launch vehicles, missiles, rockets
- Category VIII: Aircraft, helicopters (military)
- Category XI: Military electronics
- Category XV: Spacecraft, satellites (limited commercial exceptions)

**Jurisdictional Triggers**:
- **Export**: Any transfer of defense articles or technical data from US
- **Temporary Import**: Foreign defense articles brought into US
- **Brokering**: Arranging sale/transfer of defense articles (even if transaction entirely foreign)

### ITAR vs. EAR

**Key Differences**:

| Aspect | ITAR | EAR |
|--------|------|-----|
| **Scope** | Defense articles (USML) | Dual-use items (CCL) |
| **Agency** | State Dept (DDTC) | Commerce Dept (BIS) |
| **Strictness** | Very strict (minimal exceptions) | More flexible (many license exceptions) |
| **Canada** | Limited exemption (Canadian Exemption) | Broader exceptions |
| **Cloud Storage** | No foreign servers or admin access | More flexibility (depending on ECCN) |
| **Registration** | DDTC registration required ($2,750/year) | No registration required |
| **Penalties** | Criminal (up to $1M/20 years prison) | Criminal (up to $1M/20 years prison) |

**Determining ITAR vs. EAR**:
- **Start with USML**: If item explicitly listed on USML → ITAR
- **Specially Designed**: If item "specially designed" for military application → ITAR
- **600 Series**: Items transitioned from USML to CCL (ECCN starting with "600") → EAR (but still restricted)
- **Catch-All**: If neither ITAR nor CCL → EAR99 (minimal controls)

### ITAR Registration and Licensing

**Registration**:
- **Required**: Any person engaged in business of manufacturing/exporting defense articles or services
- **Process**: Register with DDTC, pay $2,750 annual fee, designate senior officer
- **Exemptions**: Occasional export (<$500K/year), US government agencies, certain foreign governments

**Licenses**:
- **DSP-5**: Permanent export of defense articles
- **DSP-73**: Temporary import of defense articles
- **TAA** (Technical Assistance Agreement): Providing defense services (design, engineering support)
- **MLA** (Manufacturing License Agreement): Foreign manufacture of ITAR items

**Authorization**: Agreement must be approved by DDTC (6-12 months typical processing time)

**Canadian Exemption**:
- Certain items can be exported to Canada without license (if registered with DDTC)
- Exceptions: Items in USML Categories I, II, III, XVII, XVIII, XIX, XX, XXI (still require license)

### ITAR Data Storage Restrictions

**Critical Rule**: ITAR technical data must be stored only in US, accessible only by US persons or authorized foreign nationals

**Prohibited**:
- Storing ITAR data on foreign servers (AWS EU, Azure Asia)
- Foreign nationals accessing ITAR data (even foreign admin access to servers)

**Compliance**:
- **US-Only Servers**: Use US data centers with no foreign admin access
- **Access Controls**: Restrict access to US persons or licensed foreign nationals
- **Encryption in Transit**: Encrypt data transfers (but encryption alone doesn't satisfy ITAR)

**Cloud Services**:
- **AWS GovCloud**: ITAR-compliant (US-only, US persons only admin access)
- **Microsoft Azure Government**: ITAR-compliant region
- **Standard Cloud**: Not ITAR-compliant unless configured for US-only access

## OFAC (Office of Foreign Assets Control)

### Sanctions Programs

**Administered By**: Office of Foreign Assets Control, US Department of Treasury

**Types of Sanctions**:
1. **Comprehensive Sanctions**: Prohibit nearly all transactions (Cuba, Iran, North Korea, Syria, Crimea region)
2. **Selective Sanctions**: Target specific entities, individuals, sectors (Russia, Venezuela, China military-industrial complex)
3. **List-Based Sanctions**: Prohibited from dealing with specific persons/entities (SDN List)

**SDN List** (Specially Designated Nationals):
- **Scope**: ~9,000 individuals and entities prohibited from US transactions
- **50% Rule**: Entity owned 50%+ by SDN = also sanctioned (even if not on list)
- **Blocking**: US persons must block (freeze) assets of SDNs

### Technology Exports to Sanctioned Countries

**Prohibited Exports** (Comprehensive Sanctions):
- Nearly all exports to Iran, North Korea, Cuba, Syria (limited exceptions for humanitarian, information materials)
- No export of technology, software, cloud services (even free/open source in some cases)

**Selective Sanctions** (Russia, China):
- **Russia**: Restricted exports of technology for oil/gas extraction, aviation, dual-use items
- **China**: Military end-use restrictions (no exports to Chinese military, companies supporting military)
- **Entity List**: Huawei, SMIC, other Chinese tech companies (require license for US-origin items)

**Due Diligence**:
- Screen customers against SDN List, Entity List, Denied Persons List (use OFAC screening tools)
- **Red Flags**: Customer refuses to disclose end-use, requests unusual shipping arrangements, located in high-risk country

### Anti-Boycott Regulations

**Prohibition**: US companies cannot participate in unsanctioned foreign boycotts (e.g., Arab League boycott of Israel)

**Reportable Requests**:
- Request to certify goods not of Israeli origin
- Request to not do business with Israel or Israeli companies
- Request for information about business relationships with Israel

**Compliance**: Report boycott requests to Commerce Dept (BIS) within certain timeframes

## Deemed Exports and Foreign National Hiring

### Deemed Export Rules

**EAR Deemed Export**:
- Release of controlled technology to foreign national in US = export to that person's country of nationality
- **License May Be Required**: Depends on foreign national's country and technology ECCN

**ITAR Deemed Export**:
- Release of ITAR technical data to foreign person (in US or abroad) = export
- **Authorization Required**: Foreign national must be specifically authorized (TAA, MLA, or license)

**Exemptions**:
- **Lawful Permanent Residents** (Green Card holders): Not considered foreign nationals for deemed export purposes (both EAR and ITAR)
- **Protected Individuals**: Asylees, refugees (treated as US persons for EAR, but NOT for ITAR)

### Practical Implications for Tech Companies

**Hiring Foreign Nationals**:
- **Assess Export Controls**: Determine if employee will access controlled technology
- **Screen Country**: Check if employee's country requires export license (China, Russia typically require license for advanced tech)
- **File License**: If required, file license before employee accesses controlled technology

**Example**:
- Company develops encryption software (ECCN 5D002)
- Hires Chinese national engineer to work on source code
- **Deemed Export**: Release of 5D002 software to Chinese national = export to China
- **License Requirement**: May need BIS license (unless qualifies for License Exception)

**Best Practices**:
- **Technology Control Plan**: Identify controlled technology, restrict access
- **Hiring Screening**: Screen foreign nationals before extending offer (if working on controlled tech)
- **Export Counsel**: Consult before hiring foreign nationals for sensitive technology roles

## Encryption Controls

### EAR Encryption Controls

**ECCN 5D002**: Encryption software with >56-bit symmetric encryption

**License Exception ENC**:
- **Scope**: Most commercial encryption software qualifies
- **Requirements**:
  - File one-time Self-Classification Report with BIS (SNAP-R)
  - No license needed for most destinations (except embargoed countries)
- **Examples**: HTTPS, SSL/TLS, AES encryption in commercial products

**Open Source Encryption**:
- **TSU Exception**: Publicly available source code (posted on internet, no restrictions on further distribution)
- **Notification**: May need to notify BIS and NSA (email to crypt@bis.doc.gov and crypt_supp@nsa.gov)

**Best Practice**: File Self-Classification Report even if using License Exception ENC (provides compliance record)

### Encryption Registration (Now Self-Classification)

**Former Requirement**: Register encryption products with BIS

**Current Requirement** (Since 2016):
- **Self-Classification Report**: File once per product family (use SNAP-R online system)
- **No Annual Renewal**: One-time filing (update if product significantly changes)

## Cloud Services and SaaS Export Controls

### Cloud Infrastructure Access

**Issue**: Foreign data center or foreign admin access may trigger export

**EAR Analysis**:
- **Technology Release**: If foreign nationals access US-origin controlled source code or technical data → deemed export
- **Example**: US SaaS company uses AWS EU region, EU admin accesses US-developed encryption source code (ECCN 5D002) → potential deemed export to EU

**ITAR Analysis**:
- **Strict Prohibition**: ITAR technical data must be stored in US, no foreign access (even admin)
- **GovCloud**: Use ITAR-compliant regions (AWS GovCloud, Azure Government)

### Software as a Service (SaaS)

**Export Trigger**: Providing SaaS to foreign customers = export of software to customer's country

**EAR Classification**:
- **EAR99**: Most commercial SaaS (minimal controls, but OFAC sanctions apply)
- **ECCN**: If SaaS includes encryption (5D002), cybersecurity tools, AI/ML algorithms → may be controlled

**Licensing**:
- **License Exception**: Many SaaS products qualify for ENC or other exceptions (no license needed)
- **OFAC Compliance**: Cannot provide SaaS to customers in sanctioned countries (Iran, North Korea, Cuba, Syria, Crimea) without license

**Best Practice**:
- Classify SaaS under EAR (determine ECCN or EAR99)
- Screen customers against SDN List, Entity List, sanctions
- Include export control provisions in Terms of Service (customer certifies compliance)

## Open Source Software

### EAR Treatment of Open Source

**TSU Exception**: "Publicly available" software exempt from license requirements

**Publicly Available**:
- Posted on internet, accessible to public
- No restrictions on further distribution (e.g., MIT, Apache, BSD licenses often qualify)
- No license or payment required for access

**Not Publicly Available**:
- Restricted access (login required, NDAs)
- Proprietary licenses with export restrictions
- Internal company source code

**Encryption Notification**:
- If open source includes encryption, notify BIS and NSA (email notification sufficient)

### GPL and Export Controls

**GPL License**: Open source license requiring derivative works to be open source (copyleft)

**Export Control Implications**:
- **Publicly Available**: If GPL software is publicly available → TSU exception applies (no export license)
- **Proprietary Derivative**: If company creates proprietary derivative (violating GPL) → may NOT qualify as publicly available → export controls apply

**Best Practice**: Comply with GPL license terms to maintain "publicly available" status (TSU exception)

## International Export Control Regimes

### Wassenaar Arrangement

**Scope**: 42 countries (including US, EU, Japan, Australia) agree to control exports of dual-use goods and technologies

**Purpose**: Prevent destabilizing accumulation of arms, prevent acquisition by terrorists

**US Implementation**: Wassenaar-controlled items listed on CCL (EAR) - identified by reason for control "NS" (National Security)

**Impact on Tech**: Intrusion software, IP network surveillance tools controlled (ECCN 4A005, 4D004, 5A001, 5D001)

### EU Export Controls

**Dual-Use Regulation** (EU 2021/821):
- **Scope**: Similar to EAR (dual-use items)
- **Member State Implementation**: Each EU country implements controls (Germany BAfA, UK ECJU, France SCCS)

**Differences from US**:
- **Intra-EU**: Generally no license for intra-EU transfers (but still restricted for certain items)
- **Human Rights**: EU has broader human rights grounds for restricting exports (cyber-surveillance tools)

**Practical Impact**: US companies exporting to EU must comply with both US (re-export controls) and EU regulations

### China Export Controls

**Export Control Law** (2020):
- **Scope**: Dual-use items, military items, other items related to national security
- **Extraterritorial**: Can apply to foreign companies re-exporting Chinese-origin items
- **Unreliable Entity List**: Chinese equivalent of Entity List (foreign entities restricted)

**Blocking Statute** (2021):
- **Purpose**: Block compliance with foreign sanctions (e.g., US sanctions on Chinese companies)
- **Prohibition**: Chinese companies cannot comply with unjustified foreign sanctions (must seek Chinese government approval)

## Penalties and Enforcement

### Civil Penalties

**EAR Violations**:
- **Civil Fine**: Up to $330,823 per violation (adjusted annually for inflation)
- **Denial of Export Privileges**: Banned from exporting (temporary or permanent)

**ITAR Violations**:
- **Civil Fine**: Up to $1,062,989 per violation (adjusted annually)
- **Debarment**: Prohibited from participating in defense trade

**OFAC Violations**:
- **Civil Fine**: Up to $368,136 per violation or 2x transaction value (whichever greater)

### Criminal Penalties

**Willful Violations**:
- **Fine**: Up to $1,000,000
- **Prison**: Up to 20 years
- **Examples**: Raytheon engineer smuggling defense technology to China (10 years prison), company exporting to Iran without license

**Strict Liability**: Some violations don't require intent (civil penalties apply even if unintentional)

### Voluntary Self-Disclosure (VSD)

**Benefit**: Reduce penalties by voluntarily disclosing violations to BIS, DDTC, or OFAC before discovered

**Requirements**:
- Promptly report violation (before government awareness)
- Cooperate with investigation
- Implement remedial measures (compliance program improvements)

**Penalty Reduction**: Typically 50% reduction in civil penalties (or no penalty if minor violation)

## Compliance Best Practices

### Export Compliance Program Elements

**Classification**:
- Determine ECCN for all products, software, technology
- Maintain classification records (basis for determination)
- Update as products change or regulations change

**Screening**:
- Screen all customers, partners, end-users against:
  - **SDN List** (OFAC)
  - **Entity List** (BIS)
  - **Denied Persons List** (BIS)
  - **Debarred Parties** (DDTC)
- Use automated screening tools (Visual Compliance, Descartes, OFAC search)

**License Determination**:
- For each export/re-export, determine if license required
- Document license exception relied upon (NLR, ENC, TSU)
- File licenses if required (BIS SNAP-R, DDTC D-Trade)

**Recordkeeping**:
- Maintain records for 5 years (EAR, ITAR, OFAC)
- Include: invoices, licenses, export documentation, correspondence

**Training**:
- Annual export compliance training for employees (identify export transactions, recognize red flags)
- Specialized training for export compliance personnel

**Audits**:
- Periodic internal audits to test compliance (transaction reviews, recordkeeping checks)
- External audits if high-risk or regulatory scrutiny

### Red Flags for Export Transactions

**Customer Red Flags**:
- Customer reluctant to provide end-use information
- Customer requests unusual packaging or shipping (re-routes through third country)
- Customer located in high-risk country (China, Russia, Iran)
- End-user is on watch list or has military connections

**Transaction Red Flags**:
- Product doesn't match customer's business (e.g., semiconductor manufacturer buying large quantities of encryption software)
- Payment from third country (not customer's location)
- Delivery to freight forwarder or P.O. box (not customer's business address)

**Response to Red Flags**:
- Investigate and document (request additional information from customer)
- If cannot resolve, **Do Not Export** (risk of violation)
- Consider Voluntary Self-Disclosure if export already occurred

## Risk Assessment Framework

### High-Risk Red Flags

**Export Controls**:
- ⚠️ No export classification (ECCN determination) for products/software
- ⚠️ Exporting to sanctioned countries (Iran, North Korea, Cuba, Syria, Crimea) without OFAC license
- ⚠️ Foreign nationals accessing controlled technology without deemed export license
- ⚠️ ITAR data stored on foreign servers or accessed by foreign persons

**Sanctions**:
- ⚠️ No SDN/Entity List screening (risk of dealing with prohibited parties)
- ⚠️ Customer on Entity List or SDN List
- ⚠️ 50% owned by SDN (indirect ownership - still sanctioned)

**Deemed Exports**:
- ⚠️ Hiring foreign nationals for controlled technology roles without export review
- ⚠️ Cloud servers with foreign admin access to US-controlled source code

### Medium-Risk Areas

**EAR Classification**:
- ⚠️ Relying on EAR99 classification without analysis (item may be controlled)
- ⚠️ No Self-Classification Report filed for encryption (5D002) - using License Exception ENC without documentation

**Recordkeeping**:
- ⚠️ Inadequate records for exports (no documentation of license exception or classification)
- ⚠️ Records not retained for 5 years (regulatory requirement)

### Low-Risk (Generally Compliant)

- ✅ Comprehensive export classification (all products have ECCN or EAR99 determination)
- ✅ Automated sanctions screening (all customers screened against SDN/Entity List)
- ✅ Technology Control Plan (restricted access to controlled technology, foreign national screening)
- ✅ Encryption Self-Classification Report filed (SNAP-R)
- ✅ Export compliance training (annual training for all employees)

## Validation Questions

When analyzing export compliance and risks:

### Classification
- [ ] What is ECCN classification for product/software? (Or EAR99 if not controlled)
- [ ] Is item subject to ITAR? (On USML or specially designed for military)
- [ ] Does product include encryption? (If yes, likely ECCN 5D002 - need Self-Classification Report)

### Licensing
- [ ] What is destination country? (Determines license requirements)
- [ ] Who is end-user? (Screened against SDN, Entity List, Denied Persons?)
- [ ] What is end-use? (Military, WMD, nuclear - heightened scrutiny)
- [ ] Does license exception apply? (ENC for encryption, TSU for open source, NLR for EAR99)

### Deemed Exports
- [ ] Will foreign nationals access controlled technology? (Deemed export analysis)
- [ ] What is foreign national's country of nationality? (Determines license requirements)
- [ ] Is technology publicly available? (TSU exception for open source)
- [ ] Are foreign nationals lawful permanent residents (Green Card)? (Not deemed export)

### Cloud and SaaS
- [ ] Where are servers located? (US-only for ITAR data)
- [ ] Who has admin access? (Foreign admin access may trigger deemed export)
- [ ] What is export classification of software provided via SaaS? (ECCN or EAR99)

### Sanctions
- [ ] Are customers screened against SDN List, Entity List? (Automated screening)
- [ ] Is destination country subject to sanctions? (Iran, North Korea, Cuba, Syria, Crimea, Russia, China)
- [ ] Are there transaction red flags? (Unusual shipping, reluctant customer, third-country payment)

### Compliance Program
- [ ] Is there export compliance program? (Classification, screening, training, recordkeeping)
- [ ] Are records maintained for 5 years? (EAR, ITAR, OFAC requirement)
- [ ] Is there annual export compliance training? (Employees recognize export transactions, red flags)

## When to Consult Experts

### Initial Classification
- **Product Launch**: Determine ECCN classification for new products (especially encryption, AI/ML, cybersecurity)
- **ITAR Determination**: Assess if product is defense article (USML) or dual-use (CCL)
- **Deemed Export**: Hiring foreign nationals for roles accessing controlled technology

### Licensing
- **License Application**: Applying for BIS export license, DDTC license, TAA, MLA
- **Denied License**: License denied or returned without action (RWA) - explore alternatives
- **Re-Export**: Complex re-export scenario (foreign-made items with US content)

### Enforcement
- **Voluntary Self-Disclosure**: Discovered potential violation (before government aware)
- **Government Investigation**: Received subpoena, search warrant, or investigation notice from BIS, DDTC, OFAC
- **Penalty Mitigation**: Responding to proposed civil penalty (negotiate reduction)

### Transactions
- **M&A Due Diligence**: Acquiring company with export-controlled products (assess compliance, legacy violations)
- **International Expansion**: Setting up foreign subsidiary or operations (export, re-export, foreign national access issues)
- **Joint Ventures**: Collaborating with foreign partners on controlled technology (TAA, technology sharing)

## Cross-References

**Related Skills**:
- `technology_licensing.md` - Technology licensing with export control provisions
- `international_tax.md` - Cross-border transactions and tax implications
- `data_agreements.md` - Data localization requirements (complement to ITAR data storage)
- `confidentiality_nda.md` - Protecting controlled technical data

**Applies to Transaction Types**:
- Software licensing (encryption, cybersecurity tools)
- Technology licensing (source code, technical data)
- Strategic partnerships (joint development with foreign partners)
- Distribution agreements (international distributors, export compliance obligations)

## References

> ⚠️ **Synthetic Skill** - Not expert validated. Export controls are highly complex and fact-specific. Penalties for violations are severe (criminal prosecution, debarment). This skill provides general overview but specific compliance requires specialized export counsel. Always consult export control attorneys before exporting controlled items, hiring foreign nationals for sensitive roles, or structuring international transactions.

**Key Regulations**:
- **EAR**: 15 CFR §§730-774 (Commerce Department, Bureau of Industry and Security)
- **ITAR**: 22 CFR §§120-130 (State Department, Directorate of Defense Trade Controls)
- **OFAC**: 31 CFR Chapter V (Treasury Department, Office of Foreign Assets Control)

**Key Resources**:
- **BIS**: www.bis.doc.gov (ECCN classification, license applications, denied parties screening)
- **DDTC**: www.pmddtc.state.gov (USML, ITAR registration, licensing)
- **OFAC**: www.treasury.gov/ofac (SDN List, sanctions programs, OFAC screening)

**Notable Cases**:
- ZTE (2017): $1.19B penalty for exporting to Iran/North Korea
- Raytheon engineer (2020): 10 years prison for exporting defense technology to China
- Huawei (2019): Entity List - US companies require license to export to Huawei
