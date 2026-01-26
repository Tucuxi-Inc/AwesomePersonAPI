---
name: antitrust-competition
description: Antitrust Competition
tags:
  - antitrust
  - competition-law
  - regulatory
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

# Antitrust and Competition Law

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**

## Metadata

```yaml
skill_id: antitrust_competition
domain: legal_fundamentals
sub_domains: [sherman_act, clayton_act, price_fixing, market_allocation, mergers]
jurisdictions: [united_states, european_union, international]
confidence: 0.70
validation_status: synthetic
requires: [keller_patterns, contract_law]
complements: [technology_licensing, strategic_partnerships, distribution_agreements]
skill_tier: foundational
mentoring_priority: 2
```

## Core Principles

### Purpose of Antitrust Law

**Goal**: Promote competition, prevent monopolies, protect consumers from anti-competitive practices

**Key US Statutes**:
- **Sherman Act (1890)**: Prohibits monopolization and restraints of trade (§1 and §2)
- **Clayton Act (1914)**: Prohibits anti-competitive mergers, exclusive dealing, tying arrangements
- **FTC Act (1914)**: Prohibits unfair methods of competition (FTC enforcement)

**Key EU Law**:
- **TFEU Article 101**: Prohibits anti-competitive agreements (cartels, price-fixing, market allocation)
- **TFEU Article 102**: Prohibits abuse of dominant position (monopolization equivalent)
- **EU Merger Regulation**: Requires notification and approval of large mergers

### Sherman Act Section 1 - Restraints of Trade

**Per Se Violations** (Always Illegal):
- **Price Fixing**: Competitors agree on prices (horizontal price-fixing)
- **Bid Rigging**: Competitors coordinate bids to fix outcomes
- **Market Allocation**: Competitors divide markets (geographic, customers, products)
- **Group Boycotts**: Competitors agree to refuse to deal with certain parties

**Rule of Reason** (Analyze Competitive Effects):
- **Vertical Restraints**: Supplier-distributor agreements (minimum advertised pricing, territorial restrictions)
- **Exclusive Dealing**: Agreements requiring buyer to purchase exclusively from one supplier
- **Tying Arrangements**: Conditioning sale of one product on purchase of another

### Sherman Act Section 2 - Monopolization

**Elements**:
1. **Monopoly Power**: Ability to control prices or exclude competition (>60-70% market share often sufficient)
2. **Willful Acquisition/Maintenance**: Anti-competitive conduct (not just superior product/business acumen)

**Lawful Monopoly**: Achieving monopoly through innovation, efficiency, or business skill is legal (e.g., Google became dominant through superior search algorithm)

**Unlawful Monopolization**: Using exclusionary practices to maintain monopoly (e.g., Microsoft tying Internet Explorer to Windows to exclude Netscape)

## Common Antitrust Issues in Tech Transactions

### 1. Horizontal Agreements (Competitor Collaborations)

**Price-Fixing** (Per Se Illegal):
```
❌ "Company A and Company B (competitors) agree to charge customers minimum $100/unit"
```
**Risk**: Criminal prosecution (jail time) + treble damages + DOJ investigation

**Information Exchange** (Risky):
- **Problem**: Competitors sharing pricing, costs, capacity, customer lists → facilitates collusion
- **Safe Harbor**: Share through independent third party (trade association), aggregated data (no individual company data visible), historical data (>3 months old)

**Joint Ventures** (Analyze Under Rule of Reason):
- **Lawful**: Competitors collaborate on R&D, new product development (procompetitive benefits)
- **Requires**: Legitimate business justification, no price-fixing, no market allocation as primary goal
- **Example**: Tech companies jointly develop industry standard (5G, Wi-Fi) - legal if open to all licensees on FRAND terms

**See Also**: `strategic_partnerships.md` for partnership structures

### 2. Vertical Agreements (Supplier-Distributor)

**Resale Price Maintenance (RPM)**:
- **Minimum RPM**: Supplier sets minimum resale price (e.g., "Distributor must sell at ≥$100") - analyzed under rule of reason (can be lawful if procompetitive justification)
- **Maximum RPM**: Supplier sets maximum resale price - generally lawful (protects consumers from overcharging)

**Minimum Advertised Price (MAP)**:
- **Structure**: Supplier prohibits advertising below MAP (but distributor can sell below MAP if doesn't advertise)
- **Legality**: Generally lawful if unilateral policy (Supplier announces policy, does not negotiate with distributors)
- **Enforcement**: Violation → loss of co-op funds, suspension (not price-fixing if unilateral)

**Exclusive Dealing**:
- **Structure**: Buyer agrees to purchase exclusively from Supplier (or vice versa)
- **Legality**: Lawful unless forecloses substantial market (typically >30-40% of market) and harms competition

**Territorial Restrictions**:
- **Exclusive Territory**: "Distributor has exclusive rights in State A, no other distributors appointed"
- **Legality**: Generally lawful (promotes interbrand competition), but cannot prohibit passive sales (unsolicited orders)
- **EU Restriction**: Cannot prohibit online sales or passive cross-border sales (violates Article 101)

**See Also**: `distribution_agreements.md` for distribution terms

### 3. Tying and Bundling

**Tying**:
- **Structure**: "To buy Product A, you must also buy Product B"
- **Illegality**: If seller has market power in tying product (A) and forecloses substantial market for tied product (B)
- **Example**: Microsoft tying Internet Explorer to Windows (found to be anticompetitive)

**Bundling**:
- **Structure**: Seller offers discount for purchasing products together (but allows separate purchases)
- **Legality**: Generally lawful (procompetitive - efficiency, cost savings)

### 4. Standard-Essential Patents (SEPs) and FRAND

**Issue**: Patent holder declares patents essential to industry standard (e.g., 5G), commits to license on FRAND terms

**FRAND Obligation**:
- **Fair and Reasonable**: Royalty rates must be reasonable (not monopoly pricing)
- **Non-Discriminatory**: Similarly situated licensees get similar terms (cannot discriminate)

**Antitrust Risk**: Refusing to license SEPs, charging excessive royalties, or discriminating violates antitrust (abuse of dominant position)

**Enforcement**: FTC, DOJ, EU Commission investigate SEP holders for FRAND violations

**See Also**: `technology_licensing.md` for FRAND licensing

### 5. Mergers and Acquisitions

**Clayton Act Section 7**: Prohibits mergers that "substantially lessen competition"

**HSR Act**: Requires pre-merger notification to FTC/DOJ if transaction exceeds thresholds ($111.4M in 2024, adjusted annually)

**Horizontal Merger**: Competitors merge (most scrutinized - directly reduces competition)
- **Market Concentration**: Herfindahl-Hirschman Index (HHI) - if post-merger HHI >2500 and increase >200, presumptively anticompetitive
- **Example**: Facebook acquiring Instagram (2012 - approved, but controversial in hindsight)

**Vertical Merger**: Supplier-customer merge (less scrutinized, but increasing scrutiny)
- **Foreclosure Theory**: Merged entity could foreclose rivals from inputs or customers
- **Example**: AT&T acquiring Time Warner (2018 - approved after litigation)

**FTC/DOJ Review**:
- **Phase I**: 30-day review (most transactions approved or second request issued)
- **Phase II**: Extended review (6-12 months), parties produce documents, depositions
- **Outcome**: Approve, approve with conditions (divestitures), or challenge (block via litigation)

## EU Competition Law Distinctions

**Article 101 (Agreements)**:
- Similar to Sherman Act §1 (prohibits anti-competitive agreements)
- **Stricter on Vertical Restraints**: Territorial restrictions, online sales bans more heavily scrutinized

**Article 102 (Abuse of Dominance)**:
- Similar to Sherman Act §2 (monopolization), but lower threshold
- **Dominance**: >40% market share may be sufficient (vs. 60-70% in US)
- **Abuse**: Excessive pricing, refusal to deal, exclusive dealing, tying (broader than US)

**EU Merger Control**:
- **Thresholds**: Worldwide turnover >€5B and EU turnover >€250M (both parties)
- **One-Stop Shop**: EU Commission reviews (no separate member state reviews if thresholds met)
- **Remedies**: Divestitures, behavioral commitments (similar to US)

## Risk Assessment Framework

### High-Risk Red Flags

**Horizontal Agreements**:
- ⚠️ Competitors discussing prices, capacity, bids, customer allocation (per se illegal)
- ⚠️ Trade association meetings where competitors share current pricing/cost data
- ⚠️ Joint venture with no legitimate business justification (cover for price-fixing)

**Vertical Agreements**:
- ⚠️ Minimum resale price maintenance with enforcement (closely scrutinized)
- ⚠️ Exclusive dealing that forecloses >40% of market
- ⚠️ Tying arrangement where seller has market power in tying product

**SEP/FRAND**:
- ⚠️ Refusing to license SEPs to willing licensee (antitrust violation)
- ⚠️ Charging discriminatory royalties (favoring some licensees over others)
- ⚠️ Seeking injunction for FRAND-committed SEPs before good-faith negotiation

**Mergers**:
- ⚠️ Horizontal merger increasing HHI >200 points with post-merger HHI >2500
- ⚠️ Acquiring direct competitor with significant market overlap
- ⚠️ "Gun jumping" (integrating before clearance) - DOJ violation

### Medium-Risk Areas

**MAP Policies**:
- ⚠️ MAP policy negotiated with distributors (should be unilateral)
- ⚠️ Resale price monitoring without clear policy (suggests RPM agreement)

**Information Sharing**:
- ⚠️ Sharing competitively sensitive information with competitors (even if indirect)
- ⚠️ No safeguards (aggregation, time lag, third-party intermediary)

**Exclusive Dealing**:
- ⚠️ Foreclosing 30-40% of market (gray zone)
- ⚠️ No procompetitive justification (efficiency, quality control)

### Low-Risk (Generally Lawful)

- ✅ Unilateral MAP policy (no agreement with distributors)
- ✅ Vertical non-price restraints with procompetitive justification
- ✅ Joint ventures with legitimate R&D/efficiency purpose (not market allocation)
- ✅ Mergers with minimal market overlap (<10% combined share)

## Compliance Best Practices

**Antitrust Training**: Educate employees (especially sales, business development) on per se violations

**Document Retention**: Be cautious with emails/communications (avoid language like "let's coordinate pricing")

**Trade Association Participation**: Have antitrust counsel review agendas, avoid discussions of pricing/capacity/customers

**Merger Integration**: Do NOT integrate operations before clearance (gun-jumping violations = significant fines)

**FRAND Licensing**: If holding SEPs, have transparent licensing program with published rates

## When to Consult Experts

- **Horizontal Agreements**: Any collaboration with competitors (joint ventures, standard-setting, R&D partnerships)
- **Vertical Restraints**: MAP policies, exclusive dealing, territorial restrictions (especially EU)
- **SEP Licensing**: Declaring patents as standard-essential, negotiating FRAND licenses
- **Mergers >$100M**: Likely HSR filing required (antitrust counsel for pre-merger review)
- **FTC/DOJ Investigation**: Received civil investigative demand (CID) or subpoena
- **Private Antitrust Litigation**: Sued for alleged antitrust violation (treble damages risk)

## References

> ⚠️ **Synthetic Skill** - Not expert validated. Antitrust law is complex and fact-specific. Violations carry severe penalties (criminal prosecution, treble damages). Always consult antitrust counsel before implementing potentially anti-competitive practices.

**Key Statutes**: Sherman Act (15 U.S.C. §§1-2), Clayton Act (15 U.S.C. §12 et seq.), FTC Act (15 U.S.C. §45), TFEU Articles 101-102

**Cross-Reference**: `technology_licensing.md` (SEPs, FRAND), `distribution_agreements.md` (MAP, exclusive territories), `strategic_partnerships.md` (joint ventures)
