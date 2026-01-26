---
name: ip-law
description: Ip Law
tags:
  - intellectual-property
  - ip-law
  - patents-trademarks
version: '1.0'
confidence_level: MEDIUM
category: core_legal_frameworks
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
mentoring_priority: 1
validation_type: synthetic
source_type: statutory
---

# Intellectual Property Law Fundamentals

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**

## Metadata

```yaml
skill_id: ip_law
domain: legal_fundamentals
sub_domains: [copyright, patents, trademarks, trade_secrets, ip_ownership]
jurisdictions: [united_states, international]
confidence: 0.70
validation_status: synthetic
requires: [keller_patterns, contract_law]
complements: [technology_licensing, ip_ownership_assignment, confidentiality_nda]
skill_tier: foundational
mentoring_priority: 1
```

## Core Principles

### What is Intellectual Property?

**Definition**: Legal rights in creations of the mind (inventions, artistic works, symbols, names, designs)

**Four Primary Types**:
1. **Copyright**: Original works of authorship (software, books, music, art)
2. **Patents**: Inventions and discoveries (utility, design, plant patents)
3. **Trademarks**: Source identifiers (brand names, logos, slogans)
4. **Trade Secrets**: Confidential business information (formulas, algorithms, customer lists)

**Why IP Matters for Tech**:
- Core asset of many tech companies (software, algorithms, brands)
- Enables licensing revenue and partnerships
- Competitive moat (patents, trade secrets)
- M&A value driver (IP ownership, freedom-to-operate)

## Copyright Law

### Copyright Basics

**Constitutional Basis**: US Constitution Article I, Section 8 ("promote progress of science and useful arts")

**Statute**: Copyright Act of 1976 (17 USC)

**What is Protected**:
- **Original Works of Authorship**: Literary works, musical works, dramatic works, pictorial/graphic/sculptural works, motion pictures, sound recordings, architectural works
- **Software**: Source code and object code are "literary works" (Apple v. Franklin, 1983)
- **Databases**: Compilations if selection/arrangement is original (Feist v. Rural Telephone, 1991)

**Requirements for Copyright Protection**:
1. **Originality**: Work must be independently created (not copied) with minimal creativity
2. **Fixation**: Fixed in tangible medium of expression (written, recorded, saved to disk)

**Not Required**:
- Registration (but required to sue)
- Copyright notice (but helpful for damages)
- Novelty or non-obviousness (unlike patents)

### Rights of Copyright Owner

**Exclusive Rights** (17 USC §106):
1. **Reproduction**: Right to copy the work
2. **Derivative Works**: Right to create adaptations, translations, sequels
3. **Distribution**: Right to sell, lend, give away copies
4. **Public Performance**: Right to perform work publicly (music, movies, software demos)
5. **Public Display**: Right to display work publicly (artwork, photos)
6. **Digital Transmission** (sound recordings): Right to perform via digital audio transmission

**Technology Implications**:
- **Copying Software**: Installing software = reproduction (requires license)
- **Modifying Code**: Creating derivative work (requires permission unless fair use/license allows)
- **SaaS**: Public performance and display rights implicated (hosting on server accessed by users)

### Copyright Ownership

**Initial Ownership**: Author owns copyright from moment of fixation

**Work Made for Hire** (17 USC §101):
Two categories where employer/commissioning party owns copyright:

**1. Employee Works** (within scope of employment):
- **Test**: Was work created by employee within scope of employment?
- **Factors**: Employer's right to control, work done at employer's location, using employer's resources
- **Result**: Employer owns copyright (no assignment needed)

**2. Commissioned Works** (if both conditions met):
- **Must be one of 9 categories**: Contribution to collective work, part of audiovisual work, translation, supplementary work, compilation, instructional text, test, answer material for test, atlas
- **Must have written agreement**: "This shall be a work made for hire"
- **Software Development**: Custom software generally NOT work-for-hire unless employee (need assignment)

**Assignments**:
- **Must be in writing**: 17 USC §204 (oral transfer invalid)
- **Recordation**: Can record with Copyright Office (notice to world, priority)
- **Reversion**: Authors can terminate assignment after 35 years (statutory right)

**Joint Works**:
- **Definition**: Work prepared by two+ authors with intent that contributions be merged into inseparable/interdependent whole
- **Ownership**: Each co-author owns undivided interest (can license non-exclusively without other's consent)
- **Intent Requirement**: Must intend joint authorship at time of creation (not later combination)

### Copyright Infringement

**Elements**:
1. **Ownership**: Plaintiff owns valid copyright
2. **Copying**: Defendant copied the work (access + substantial similarity)
3. **Improper Appropriation**: Copying of protected expression (not just ideas)

**Defenses**:
- **Independent Creation**: Defendant created work independently (no copying)
- **Fair Use**: Transformative use, criticism, parody (see below)
- **First Sale Doctrine**: Owner of lawful copy can resell (but not reproduce or distribute copies)
- **Merger Doctrine**: Idea and expression merged (only one way to express idea) - no protection
- **Scènes à Faire**: Stock elements common to genre (no protection)

**Remedies**:
- **Injunction**: Stop infringing activity
- **Actual Damages**: Copyright owner's losses + infringer's profits
- **Statutory Damages**: $750-$30,000 per work ($150,000 if willful) - requires registration before infringement
- **Attorney's Fees**: If registered within 3 months of publication or before infringement

### Fair Use (17 USC §107)

**Four Factors**:
1. **Purpose and Character**: Transformative use, commercial vs. nonprofit/educational
2. **Nature of Work**: Creative vs. factual (less protection for factual)
3. **Amount Used**: Proportion and substantiality of portion used
4. **Market Effect**: Does use substitute for original or harm market?

**All Factors Considered Together** (no single factor dispositive)

**Technology Examples**:
- **Reverse Engineering**: May be fair use if necessary to achieve interoperability (Sega v. Accolade)
- **API Copying**: Google copied Java API structure to create Android - fair use because transformative (Google v. Oracle, 2021)
- **Search Engine Caching**: Thumbnails and caching likely fair use (transformative, minimal amount)
- **Parody/Commentary**: Transformative use, favors fair use

**Not Fair Use**:
- **Wholesale Copying**: Copying entire work (factor 3 weighs against)
- **Commercial Substitute**: Use replaces market for original (factor 4 weighs heavily against)

### Copyright Registration

**Benefits of Registration**:
- **Prerequisite to Sue**: US authors must register before filing infringement suit
- **Statutory Damages**: Only available if registered within 3 months of publication or before infringement
- **Attorney's Fees**: Only available if registered timely
- **Prima Facie Evidence**: If registered within 5 years, presumption of validity

**Process**:
- File application with Copyright Office (online or paper)
- $45-$65 fee (depending on application type)
- Deposit copy of work
- 6-8 months processing (expedited available for $800 fee)

**Best Practice**: Register software before major product launch, before licensing, or upon discovery of infringement

### DMCA (Digital Millennium Copyright Act)

**DMCA §512 Safe Harbor**:
**Purpose**: ISPs, platforms, hosting providers not liable for user infringement if comply with notice-and-takedown

**Requirements**:
1. **Registered Agent**: Designate DMCA agent with Copyright Office
2. **Notice-and-Takedown**: Expeditiously remove infringing content upon notice
3. **Counter-Notice**: Restore content if user files counter-notice (absent lawsuit in 10-14 days)
4. **Repeat Infringer Policy**: Terminate accounts of repeat infringers

**Technology Platforms**: YouTube, GitHub, Facebook rely on DMCA safe harbor to avoid liability for user uploads

**DMCA §1201 Anti-Circumvention**:
**Prohibition**: Circumventing technological measures that control access to copyrighted work (DRM, encryption)
**Penalties**: Civil damages, criminal prosecution (up to 5 years prison for willful violation)
**Exemptions**: Reverse engineering for interoperability, security research, jailbreaking phones (some exemptions)

## Patent Law

### Patent Basics

**Constitutional Basis**: Same as copyright (promote progress of science and useful arts)

**Statute**: Patent Act (35 USC)

**Types of Patents**:
1. **Utility Patent**: Inventions and discoveries (new and useful process, machine, manufacture, composition of matter) - 20 years from filing
2. **Design Patent**: Ornamental design for article of manufacture - 15 years from grant
3. **Plant Patent**: Distinct and new variety of plant - 20 years from filing

**Requirements for Patentability** (utility patent):
1. **Patentable Subject Matter** (35 USC §101): Process, machine, manufacture, composition of matter
2. **Utility**: Useful (minimal requirement - almost always met)
3. **Novelty** (35 USC §102): Not anticipated by single prior art reference (new)
4. **Non-Obviousness** (35 USC §103): Not obvious to person of ordinary skill in the art (POSITA)
5. **Enablement** (35 USC §112): Specification must teach how to make and use invention
6. **Written Description**: Specification must describe invention (show inventor had possession)

### Software Patents (Post-Alice)

**Alice Corp. v. CLS Bank (2014)**: Two-step test for patentable subject matter

**Step 1**: Is claim directed to abstract idea, law of nature, or natural phenomenon?
- **Abstract Ideas**: Mathematical algorithms, fundamental economic practices, methods of organizing human activity
- **Example**: Hedging risk, mitigating settlement risk, intermediated settlement = abstract ideas

**Step 2**: If yes, does claim contain "inventive concept" sufficient to transform abstract idea into patent-eligible application?
- **Inventive Concept**: More than "apply it on a computer" or "use generic computer components"
- **Example**: Improved computer functionality, specific technical improvement, non-conventional arrangement

**Practical Impact**:
- **Business Method Patents**: Harder to get/enforce (often abstract)
- **AI/ML Patents**: Focus on specific technical improvement (not just "apply AI to problem X")
- **Software Patents**: More likely valid if tied to specific hardware, technical problem, or measurable improvement

**Post-Alice Strategies**:
- Claim specific technical solution (not general problem)
- Describe improvement to computer functionality
- Avoid claim language like "on a computer" or "using a processor" (generic)

### Patent Prosecution

**Process**:
1. **File Application**: Provisional (1-year placeholder) or non-provisional (examination begins)
2. **Examination**: USPTO examiner reviews for patentability (102, 103, 112 rejections)
3. **Office Actions**: Examiner issues rejection/objection (applicant responds, amends claims)
4. **Allowance**: If examiner satisfied, issues notice of allowance (pay issue fee → patent grants)

**Timeline**: 1-3 years (average 24 months from non-provisional filing to grant)

**Costs**: $10K-$20K for simple software patent, $50K+ for complex inventions (includes filing, prosecution, attorney fees)

**Publication**: Application published 18 months after filing (or earlier if request)

### Patent Infringement

**Literal Infringement**: Accused product/process meets every limitation of patent claim

**Doctrine of Equivalents**: Accused product performs substantially same function, in substantially same way, to achieve substantially same result (even if not literal infringement)

**Types**:
- **Direct Infringement**: Making, using, selling, offering to sell, importing patented invention without authorization
- **Indirect Infringement**: Inducing infringement (knowingly encouraging others to infringe) or contributory infringement (selling component with no substantial non-infringing use)

**Defenses**:
- **Invalidity**: Patent invalid (anticipated, obvious, lack enablement, indefiniteness)
- **Non-Infringement**: Accused product doesn't meet claim limitations
- **Experimental Use**: Limited exemption for research (very narrow)
- **Prior User Rights**: Commercially used invention at least 1 year before patent filing (35 USC §273 - trade secret defense)

**Remedies**:
- **Injunction**: Permanent injunction if ongoing infringement causes irreparable harm (eBay v. MercExchange - must show 4 factors)
- **Damages**: Lost profits or reasonable royalty (not less than reasonable royalty)
- **Enhanced Damages**: Up to 3x for willful infringement
- **Attorney's Fees**: Exceptional cases (willfulness, bad faith)

### Patent Licensing

**Exclusive License**: Licensee has exclusive rights (even patent owner cannot practice)
- **Treated as Assignment**: Must be in writing, recorded with USPTO
- **Standing to Sue**: Exclusive licensee can sue for infringement

**Non-Exclusive License**: Licensee can practice, but so can others (including patent owner)
- **No Writing Required**: But best practice to have written agreement
- **No Standing**: Cannot sue for infringement (only patent owner)

**Royalty Structures**:
- **Lump Sum**: One-time payment
- **Running Royalty**: Per-unit fee (e.g., $1 per device sold)
- **Paid-Up License**: Upfront payment for unlimited use
- **Minimum Guarantees**: Minimum annual royalty (protects licensor)

**Field-of-Use Restrictions**: Limit license to specific field (e.g., medical devices, not consumer electronics)

**Grant-Back Clauses**: Licensee grants back improvements to licensor (may be antitrust issue if exclusive)

### Prior Art Searches and Freedom-to-Operate

**Prior Art Search**:
- **Purpose**: Assess patentability before filing application
- **Scope**: Search issued patents, published applications, publications, products, trade shows
- **Cost**: $2K-$10K for professional search

**Freedom-to-Operate (FTO) Opinion**:
- **Purpose**: Assess infringement risk before launching product
- **Scope**: Search issued patents in relevant jurisdiction (US, EU, etc.)
- **Analysis**: Do any claim limitations read on our product?
- **Cost**: $15K-$50K for opinion (depends on complexity, number of patents)
- **Benefit**: Evidence of good faith (may avoid willfulness finding, enhanced damages)

**Best Practice**: Conduct FTO before major product launch, before accepting investment, before M&A

## Trademark Law

### Trademark Basics

**Purpose**: Identify source of goods/services, prevent consumer confusion

**Protectable Marks**:
- **Word Marks**: Brand names (Apple, Google, Microsoft)
- **Design Marks**: Logos, stylized text
- **Slogans**: Taglines ("Just Do It", "Think Different")
- **Trade Dress**: Product packaging, design (Coca-Cola bottle shape)
- **Sound Marks**: Distinctive sounds (NBC chimes, Intel jingle)
- **Color**: Single color if acquired secondary meaning (Tiffany blue, UPS brown)

**Not Protectable**:
- **Generic Terms**: Common name for goods/services ("Computer" for computers)
- **Functional Features**: Feature essential to use/purpose (Qualitex v. Jacobson - color functional if affects cost/quality)

### Distinctiveness Spectrum

**Strong → Weak** (more protection → less protection):

**1. Fanciful**: Made-up words with no meaning (Kodak, Xerox, Exxon) - **strongest protection**

**2. Arbitrary**: Common words used in unrelated context (Apple for computers, Camel for cigarettes) - **strong protection**

**3. Suggestive**: Suggests quality/characteristic but requires imagination (Greyhound for fast bus service, Netflix for streaming) - **protectable**

**4. Descriptive**: Describes quality, characteristic, function, or use - **NOT protectable unless secondary meaning acquired**
- **Examples**: "Cold and Creamy" for ice cream, "Vision Center" for eyeglasses
- **Secondary Meaning**: Consumers associate mark with single source (acquired through long use, advertising, sales)

**5. Generic**: Common name for goods/services - **NEVER protectable**
- **Examples**: "Computer" for computers, "Escalator" (formerly trademark, became generic)
- **Genericide**: Trademark becomes generic through common usage (Aspirin, Zipper, Thermos)

### Trademark Registration

**Why Register**:
- **Federal Rights**: Nationwide priority (vs. common law rights in geographic area only)
- **Prima Facie Evidence**: Presumption of validity, ownership, exclusive right to use
- **Statutory Damages**: Enhanced remedies for counterfeiting (not just dilution)
- **Customs Enforcement**: Can record with Customs to stop infringing imports
- **® Symbol**: Can use ® (federal registration) vs. ™ (common law)

**Registration Process**:
1. **Search**: Trademark search to identify confusingly similar marks ($500-$2K professional search)
2. **File Application**: USPTO TEAS application (specify goods/services, class)
3. **Examination**: USPTO examining attorney reviews (6-9 months)
4. **Publication**: If approved, published for opposition (30 days for third parties to oppose)
5. **Registration**: If no opposition, register (or file Statement of Use if intent-to-use application)

**Costs**: $250-$350 per class (government fees) + $1K-$3K attorney fees

**Timeline**: 8-12 months if no issues, 1-2 years if office actions

**Use Requirement**:
- **Trademark**: Must use in commerce to register (or file intent-to-use and use within 3 years)
- **Maintenance**: Must file Declaration of Continued Use (§8 declaration) at 5-6 years, 9-10 years, and every 10 years thereafter

### Trademark Infringement

**Likelihood of Confusion Test**:
**Factors** (varies by circuit, typically 8-13 factors):
1. **Similarity of Marks**: Sight, sound, meaning, commercial impression
2. **Similarity of Goods/Services**: Related or unrelated?
3. **Strength of Mark**: Fanciful/arbitrary (strong) vs. descriptive/weak
4. **Evidence of Actual Confusion**: Consumer surveys, misdirected communications
5. **Intent**: Did defendant intend to confuse? (bad faith weighs heavily)
6. **Marketing Channels**: Overlapping distribution, advertising
7. **Sophistication of Consumers**: Sophisticated buyers less likely confused
8. **Expansion**: Likelihood plaintiff will expand into defendant's market

**No Fixed Threshold**: Balancing test (some factors weigh more heavily depending on facts)

**Defenses**:
- **Fair Use**: Descriptive fair use (using descriptive term in descriptive sense, not as mark)
- **Nominative Fair Use**: Using competitor's trademark to refer to their product ("Compatible with iPhone")
- **Parody**: Mocking trademark (strong First Amendment protection if clear parody)
- **Laches**: Unreasonable delay in bringing suit (defendant detrimentally relied on delay)
- **Genericide**: Mark became generic (no longer protectable)

**Remedies**:
- **Injunction**: Stop using infringing mark
- **Profits**: Defendant's profits from infringing sales
- **Actual Damages**: Plaintiff's lost sales, corrective advertising
- **Enhanced Damages**: Up to 3x for willful infringement
- **Counterfeiting**: Statutory damages $1K-$200K per mark per type of goods (intentional counterfeiting $2K-$2M)

### Trademark Dilution

**Purpose**: Protect famous marks from uses that blur or tarnish (even absent likelihood of confusion)

**Requirements** (15 USC §1125(c)):
1. **Famous Mark**: Widely recognized by general consuming public (not just niche)
2. **Use in Commerce**: Defendant uses mark in commerce
3. **Likelihood of Dilution**: Blurring (weakens distinctiveness) or tarnishment (harms reputation)

**Blurring**: Use of famous mark on unrelated goods dilutes distinctiveness (Tiffany for motorcycles - even if no confusion, dilutes Tiffany brand)

**Tarnishment**: Use of famous mark in unwholesome context (Disney characters in adult films)

**Defenses**:
- **Fair Use**: Comparative advertising, parody, news reporting, commentary
- **Functional Use**: Using mark to describe product (not as trademark)

**Remedies**: Injunction (but not damages unless willfulness proven)

### Domain Names and Cybersquatting

**Anticybersquatting Consumer Protection Act (ACPA)** (15 USC §1125(d)):
**Prohibits**: Registering, trafficking in, or using domain name that is identical/confusingly similar to trademark with bad faith intent to profit

**Bad Faith Factors**:
- Registrant has no IP rights in domain
- Domain is identical to trademark
- Registrant has pattern of cybersquatting
- Registrant offered to sell domain to trademark owner
- Registrant provided false contact information
- Registrant registered multiple domains identical to trademarks

**Remedies**: Statutory damages $1K-$100K per domain (or actual damages)

**UDRP** (Uniform Domain-Name Dispute-Resolution Policy):
- **Faster, Cheaper**: Alternative to ACPA litigation (ICANN arbitration)
- **Requirements**: (1) Domain identical/confusingly similar, (2) Registrant has no rights/legitimate interests, (3) Registered and used in bad faith
- **Remedy**: Transfer domain (not damages)
- **Timeline**: 45-60 days (vs. 1-2 years for litigation)
- **Cost**: $1K-$5K (vs. $100K+ for litigation)

## Trade Secrets

### Trade Secret Basics

**Definition**: Information that (1) derives economic value from being secret, and (2) is subject to reasonable efforts to maintain secrecy

**Laws**:
- **Federal**: Defend Trade Secrets Act (DTSA) - 18 USC §1836 (civil remedy)
- **State**: Uniform Trade Secrets Act (UTSA) - adopted by 48 states (not NY, NC)
- **Common Law**: Common law trade secret protection (NY)

**What Qualifies**:
- **Technical Information**: Algorithms, source code, formulas, processes, designs
- **Business Information**: Customer lists, pricing information, business strategies, financial data
- **Negative Know-How**: What doesn't work (failed experiments, abandoned approaches)

**What Does NOT Qualify**:
- **Publicly Known Information**: Once publicly disclosed, no longer secret
- **Independently Discovered**: If third party independently discovers, no violation
- **Reverse Engineered**: Lawfully reverse engineering product to discover trade secret (if no license restriction)
- **General Skills and Knowledge**: Employee's general skills/knowledge not protectable (only specific trade secrets)

### Reasonable Efforts to Maintain Secrecy

**Required Measures** (fact-specific, but typically):
- **NDAs**: Non-disclosure agreements with employees, contractors, partners
- **Physical Security**: Locked facilities, badge access, clean desk policy
- **Digital Security**: Password protection, encryption, access controls, DRM
- **Marking**: Label documents "Confidential" or "Trade Secret"
- **Exit Interviews**: Remind departing employees of confidentiality obligations, return all materials
- **Limited Disclosure**: Only disclose to those with need to know

**NOT Required**:
- **Extreme Measures**: Fort Knox-level security not required (reasonableness standard)
- **Absolute Secrecy**: Can disclose to employees, contractors, advisors (with NDAs)

### Trade Secret Misappropriation

**DTSA/UTSA Definition**:
**Acquisition**: Acquiring trade secret by improper means (theft, bribery, espionage, breach of duty)
**Disclosure/Use**: Disclosing or using trade secret knowing/having reason to know it was acquired by improper means or under duty of confidentiality

**Examples**:
- **Employee Departure**: Employee takes customer list, source code to new employer (breach of duty)
- **Hacking**: Hacker accesses company servers, steals proprietary algorithm (improper means)
- **Reverse Engineering**: Generally lawful UNLESS software license prohibits reverse engineering

**Defenses**:
- **Independent Development**: Defendant developed information independently (no misappropriation)
- **Reverse Engineering**: Lawfully reverse engineered product (unless prohibited by license)
- **Public Domain**: Information publicly available (no longer secret)
- **Lack of Reasonable Efforts**: Plaintiff didn't maintain secrecy (no trade secret protection)

**Remedies**:
- **Injunction**: Prohibit use/disclosure (typically for period trade secret would have remained secret)
- **Damages**: Actual loss or unjust enrichment (defendant's profits)
- **Exemplary Damages**: Up to 2x for willful/malicious misappropriation (DTSA/UTSA)
- **Attorney's Fees**: If bad faith (DTSA/UTSA)

### Whistleblower Protections (DTSA §1833(b))

**Protection**: Individuals cannot be held liable for disclosing trade secret to government official or attorney for purpose of reporting/investigating suspected violation of law

**Notice Requirement**: Employers must include notice of whistleblower immunity in agreements (or lose exemplary damages/attorney's fees)

**Standard Language**: "You will not be held criminally or civilly liable under any federal or state trade secret law for disclosing a trade secret to a government official or to an attorney for the purpose of reporting or investigating a suspected violation of law..."

## IP Ownership Issues

### Work-for-Hire

**Copyright**: See Copyright Ownership section above (employees vs. commissioned works)

**Patents**: Invention belongs to inventor (employee), but employer may have "shop right" (non-exclusive, non-transferable right to use)
- **Assignment Required**: Employer must obtain assignment to own patent (not automatic like copyright)
- **Hired to Invent**: If employee hired specifically to invent, courts may find implied assignment

**Trademarks**: Work-for-hire concept doesn't apply (ownership follows use in commerce)

**Best Practice**: All employment agreements should include IP assignment clause covering inventions, works of authorship, trademarks

### Pre-Invention Assignment Agreements

**Common Provision**:
"Employee assigns to Company all inventions, works of authorship, and discoveries conceived or reduced to practice during employment, whether during business hours or not, using Company resources or not, related to Company's actual or anticipated business."

**State Law Limits**:

**California Labor Code §2870**:
Cannot assign employee inventions if ALL of:
- Developed **entirely on own time**
- Without using employer's **equipment, supplies, facilities, or trade secrets**
- Does **NOT** relate to employer's business or actual/demonstrably anticipated research

**Other States**: Washington, Illinois, Minnesota, Kansas, North Carolina, Nevada, Utah (similar limitations)

**Compliance**: Employment agreement must include §2870 notice (California requirement) - see `employment_law.md`

### Joint Ownership

**Patents**: Each co-inventor owns undivided interest (can license, sell entire interest without other's consent - no duty to account)

**Copyright**: Each co-author owns undivided interest (can license non-exclusively, but not exclusively without other's consent - no duty to account)

**Trade Secrets**: No concept of joint ownership (either party's disclosure destroys secrecy)

**Trademarks**: No joint ownership (ownership follows use - only one source)

**Best Practice**: Avoid joint ownership (use assignments, licensing, work-for-hire) - joint ownership creates uncertainty

## International IP Protection

### Copyright

**Berne Convention**: 179 countries recognize copyrights from member countries (no registration required)
- **Automatic Protection**: US work automatically protected in Berne countries
- **Moral Rights**: Some countries recognize moral rights (right to attribution, integrity) - limited in US

**Digital Issues**: DMCA-equivalent laws vary (EU has Copyright Directive, but implementations differ)

### Patents

**Patent Cooperation Treaty (PCT)**: File single international application, designate countries (preserves filing date)
- **Not a Grant**: PCT doesn't grant patent (must enter national phase in each country)
- **Benefits**: 30-month delay before national phase (time to assess commercial viability, 12+ month priority window)
- **Costs**: $4K filing fee + $2K-$10K per country for national phase

**Key Markets**: US, EU, China, Japan, South Korea, India (90%+ of tech patent value)

**Differences**:
- **Grace Period**: US allows 1-year grace period after public disclosure (most countries: absolute novelty requirement - any disclosure before filing = unpatentable)
- **First-to-File**: US switched to first-to-file (2013 AIA) - file early, file often
- **Software Patents**: US more permissive than EU (EU requires "technical character")

### Trademarks

**Madrid Protocol**: File single application through home country, designate countries (100+ countries)
- **Benefits**: Centralized filing, reduced costs ($653 base fee + $100-$300 per country)
- **Drawbacks**: Dependent on base registration for 5 years (if base registration cancelled, international registration cancelled)

**Use Requirement**: US requires actual use to register (most countries: no use required, can register based on intent)

**Enforcement**: Varies significantly (China: first-to-file system, trademark squatting common; EU: opposition rate ~10%, longer examination)

### Trade Secrets

**No International Treaty**: Trade secrets protected by national laws (varies widely)

**EU Trade Secrets Directive** (2016): Harmonized EU trade secret protection (similar to DTSA)

**China**: Anti-Unfair Competition Law (trade secret protection, but enforcement weaker than US)

**Best Practice**: Use NDAs with choice of law/forum selection (US or EU law/forum)

## Technology-Specific IP Issues

### APIs and Interoperability

**Oracle v. Google** (US Supreme Court, 2021):
- **Holding**: Google's copying of Java API structure for Android was **fair use**
- **Reasoning**: (1) Transformative (different platform, purpose), (2) APIs are functional (more flexible fair use), (3) Google copied only what necessary for interoperability, (4) No harm to Oracle's market (smartphones, not desktops)

**Impact**: API copying may be fair use if necessary for interoperability and transformative purpose

**Caution**: Fair use is fact-specific (not blanket license to copy APIs)

### Open Source Software

**GPL (General Public License)**:
- **Copyleft**: Derivative works must also be GPL (source code must be released)
- **Trigger**: Distribution (not internal use)
- **Risk**: Incorporating GPL code into proprietary software may require releasing proprietary code as GPL

**LGPL (Lesser GPL)**:
- **Dynamic Linking**: Can link proprietary software to LGPL library (no copyleft if dynamically linked)
- **Static Linking**: If statically linked, derivative work (must be GPL/LGPL)

**MIT/BSD/Apache** (Permissive):
- **No Copyleft**: Can incorporate into proprietary software (no source code release requirement)
- **Attribution**: Typically require copyright notice and license text in documentation

**Patent Grant**: Apache 2.0 includes express patent license (GPL v3 also includes patent provisions)

**Compliance**:
- **Inventory**: Track all open source components (use tools like FOSSA, Black Duck, Snyk)
- **License Review**: Review license obligations (especially GPL/LGPL)
- **Attribution**: Include required notices in documentation

### AI-Generated Content

**Copyright**:
- **Authorship**: US Copyright Office requires human authorship (no copyright for AI-generated works - *Thaler v. Perlmutter*, 2023)
- **AI-Assisted**: If human provides creative input (not just prompts), may be copyrightable
- **Training Data**: Scraping copyrighted works for AI training may be fair use (transformative, factual extraction) - ongoing litigation

**Patents**:
- **Inventorship**: US law requires human inventor (AI cannot be inventor - *Thaler v. Vidal*, Fed. Cir. 2022)
- **AI-Assisted**: If human conceived invention using AI as tool, human is inventor

**Practical Issues**:
- **Ownership Uncertainty**: If AI generates work, who owns it? (user, AI company, public domain?)
- **Indemnification**: AI vendors may not indemnify for IP infringement (generated content may infringe third-party IP)

## Risk Assessment Framework

### High-Risk Red Flags

**Copyright**:
- ⚠️ No written assignment from contractors/consultants (no work-for-hire presumption)
- ⚠️ Copying third-party code without license (infringement risk)
- ⚠️ GPL code incorporated into proprietary software (copyleft risk)
- ⚠️ No DMCA agent registered (no safe harbor protection for platforms)

**Patents**:
- ⚠️ No FTO analysis before product launch (willful infringement risk, enhanced damages)
- ⚠️ Copying patented technology (clear infringement)
- ⚠️ No patent strategy for core technology (competitors can patent, block use)
- ⚠️ Filing patent application >1 year after public disclosure (barred in most countries, potentially in US post-AIA)

**Trademarks**:
- ⚠️ Using descriptive mark without secondary meaning (weak/unenforceable)
- ⚠️ No trademark search before launch (confusingly similar mark exists)
- ⚠️ Using famous mark on unrelated goods (dilution risk)
- ⚠️ Trademark becoming generic (Genericide - use "Google search", not "Google it")

**Trade Secrets**:
- ⚠️ No NDAs with employees/contractors (no duty of confidentiality)
- ⚠️ No access controls or security measures (fails "reasonable efforts" requirement)
- ⚠️ Departing employee taking customer lists/code (misappropriation risk)
- ⚠️ No whistleblower notice in agreements (DTSA - lose exemplary damages/fees)

### Medium-Risk Areas

**Copyright**:
- ⚠️ Using copyrighted images/content without license (infringement, but may be small damages)
- ⚠️ No copyright registration (limits remedies to actual damages, no statutory damages/attorney's fees)

**Patents**:
- ⚠️ Provisional patent filed but no non-provisional within 12 months (lose priority date)
- ⚠️ No patent portfolio for defensive purposes (cross-licensing opportunities limited)

**Trademarks**:
- ⚠️ No federal registration (only common law rights in geographic area)
- ⚠️ Using ™ instead of ® (lost benefits of registration notice)

**Trade Secrets**:
- ⚠️ Inadequate exit interview process (departing employees may not understand obligations)
- ⚠️ No monitoring of competitor hiring (former employees may disclose trade secrets)

### Low-Risk (Generally Compliant)

- ✅ Written IP assignment from all employees/contractors
- ✅ IP provisions in all vendor/customer contracts (reps, warranties, indemnification)
- ✅ FTO analysis before major product launch (patent clearance)
- ✅ Registered trademarks for core brands (federal registration)
- ✅ Open source compliance program (inventory, license review, attribution)
- ✅ Trade secret protection measures (NDAs, access controls, marking)

## Validation Questions

When analyzing IP ownership, infringement risk, and protection:

### Ownership
- [ ] Who created the work/invention? (Employee, contractor, founder)
- [ ] Is there written assignment? (Copyright assignment, patent assignment)
- [ ] Was it work-for-hire? (Employee within scope, or commissioned work in 9 categories + written agreement)
- [ ] Are there joint owners? (Joint authorship, co-inventors)
- [ ] Does company own all IP needed? (Background IP from founders, contractors)

### Copyright
- [ ] Is work original and fixed in tangible medium?
- [ ] Is it registered with Copyright Office? (Required to sue, statutory damages)
- [ ] Are there third-party copyrighted materials incorporated? (Images, code, text)
- [ ] Is use fair use? (Four factors - transformative, amount, market effect)
- [ ] Is there DMCA compliance? (Registered agent, notice-and-takedown for platforms)

### Patents
- [ ] Is invention patentable subject matter? (Alice test for software - abstract idea + inventive concept)
- [ ] Is it novel and non-obvious? (Prior art search, FTO analysis)
- [ ] Was FTO analysis conducted? (Before product launch)
- [ ] Are there blocking patents? (Third-party patents covering our technology)
- [ ] Is patent licensed or owned? (Freedom-to-operate)

### Trademarks
- [ ] Is mark distinctive? (Fanciful/arbitrary/suggestive vs. descriptive/generic)
- [ ] Was trademark search conducted? (Confusingly similar marks exist?)
- [ ] Is mark registered? (Federal registration, state registration, common law)
- [ ] Is there likelihood of confusion with third-party mark? (8+ factors)
- [ ] Is mark being used properly? (As adjective, not verb/noun - prevent genericide)

### Trade Secrets
- [ ] Does information qualify as trade secret? (Economic value from secrecy, reasonable efforts to maintain secrecy)
- [ ] Are reasonable security measures in place? (NDAs, access controls, marking)
- [ ] Are employees/contractors bound by confidentiality? (NDAs, employment agreements)
- [ ] Is whistleblower notice included? (DTSA requirement)
- [ ] What happens when employees leave? (Exit interview, return materials, reminder of obligations)

## When to Consult Experts

### Copyright
- **Software Development**: Using third-party code, open source integration (license compliance)
- **DMCA Compliance**: Platform hosting user-generated content (safe harbor requirements)
- **Infringement Claims**: Received DMCA takedown notice or cease-and-desist (response strategy)
- **Fair Use Defense**: Relying on fair use for copyrighted content (fact-specific analysis)

### Patents
- **Patent Prosecution**: Filing patent application (claims drafting, prosecution strategy)
- **FTO Analysis**: Launching product in crowded patent landscape (clearance opinion)
- **Infringement Claims**: Received patent demand letter or notice (invalidity analysis, design-around)
- **Licensing**: Negotiating patent license (royalty rates, grant-back clauses)

### Trademarks
- **Trademark Clearance**: Selecting brand name, logo (comprehensive search, risk analysis)
- **Registration**: Filing trademark application (classification, specimen, description)
- **Infringement**: Competitor using confusingly similar mark (cease-and-desist, litigation)
- **Opposition/Cancellation**: Third party opposes your application or seeks to cancel your registration (response strategy)

### Trade Secrets
- **Employee Departure**: Key employee leaving to competitor (risk of misappropriation)
- **Misappropriation Claims**: Suspect competitor stole trade secrets (forensics, litigation)
- **M&A Due Diligence**: Acquiring company with trade secret-dependent business (validation of protection measures)

### Transactions
- **Licensing**: Technology licensing, software licensing (IP provisions, reps/warranties, indemnification)
- **M&A**: IP due diligence, representations, post-closing IP assignments
- **Strategic Partnerships**: Joint development agreements, co-ownership issues

## Cross-References

**Related Skills**:
- `technology_licensing.md` - Patent and copyright licensing structures
- `ip_ownership_assignment.md` - Detailed IP assignment provisions in contracts
- `confidentiality_nda.md` - Trade secret protection through NDAs
- `employment_law.md` - Employee IP ownership, California § 2870

**Applies to All Transaction Types**:
- Software licensing, technology licensing, strategic partnerships, data agreements all involve IP ownership, licensing, and risk allocation

## References

> ⚠️ **Synthetic Skill** - Not expert validated. IP law is highly technical and jurisdiction-specific. This skill provides general US principles but specific enforceability may vary. Patent prosecution, FTO analysis, and IP litigation require specialized counsel. Always consult IP counsel for significant transactions or disputes.

**Key Statutes**:
- **Copyright**: 17 USC (Copyright Act of 1976), DMCA (17 USC §512, §1201)
- **Patents**: 35 USC (Patent Act), America Invents Act (AIA, 2011)
- **Trademarks**: 15 USC §1051 et seq. (Lanham Act), ACPA (15 USC §1125(d))
- **Trade Secrets**: 18 USC §1836 (DTSA), Uniform Trade Secrets Act (UTSA)

**Key Cases**:
- **Copyright**: Google v. Oracle (API fair use), Feist v. Rural Telephone (originality), ProCD v. Zeidenberg (shrinkwrap)
- **Patents**: Alice Corp. v. CLS Bank (software patentability), eBay v. MercExchange (injunctions)
- **Trademarks**: Qualitex v. Jacobson (color marks), Polaroid v. Polarad (likelihood of confusion)
