---
name: distribution-agreements
description: Distribution Agreements
tags:
  - channel
  - distribution
  - reseller
version: '1.0'
confidence_level: MEDIUM
category: transaction_types
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
mentoring_priority: 2
validation_type: synthetic
source_type: expert_judgment
---

# Distribution and Reseller Agreements

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**

## Metadata

```yaml
skill_id: distribution_agreements
domain: transaction_types
sub_domains: [reseller, var, oem, channel_partner, territory_exclusivity]
confidence: 0.70
validation_status: synthetic
requires: [keller_patterns, contract_law, technology_licensing]
complements: [strategic_partnerships, software_licensing, trademark_licensing]
skill_tier: foundational
mentoring_priority: 2
```

## Core Principles

### Distribution Agreement Fundamentals

**Definition**: Agreement where manufacturer/vendor ("Supplier") appoints intermediary ("Distributor" or "Reseller") to sell Supplier's products to end customers

**Key Characteristic**: Distributor **resells** products (buys from Supplier, resells to customers) - not an agent or employee

**Economic Model**:
- **Supplier**: Sells to Distributor at **wholesale price** (discounted from retail)
- **Distributor**: Resells to customers at **retail price** (or negotiated price)
- **Distributor Margin**: Difference between wholesale and retail (typically 20-40% depending on industry)

**Example**: Software vendor sells licenses to reseller at 60% of list price ($100 list → $60 wholesale). Reseller sells to customer at $90 (10% discount from list). Reseller margin = $30 (33%).

### Distributor vs. Agent vs. Strategic Partner

#### Distributor/Reseller (Most Common)

**Structure**: Distributor buys products from supplier, takes title, resells to customers

**Characteristics**:
- **Takes Title**: Distributor owns inventory (assumes inventory risk)
- **Sets End-Customer Price**: Distributor negotiates with customers (within Supplier's guidelines)
- **Customer Relationship**: Distributor owns customer relationship (customer contracts with Distributor, not Supplier)
- **Margin-Based**: Distributor earns margin (buy-sell spread)

**Risk**: Distributor assumes inventory risk (if cannot sell, stuck with inventory), payment risk (if customer doesn't pay, Distributor still owes Supplier)

#### Agent/Representative

**Structure**: Agent markets/sells Supplier's products but does NOT take title (Supplier sells directly to customer, Agent earns commission)

**Characteristics**:
- **No Title**: Agent never owns products (Supplier ships directly to customer)
- **Supplier Sets Price**: Agent cannot negotiate price (Supplier's list price applies)
- **Supplier's Customer**: Customer contracts with Supplier (Agent just facilitates)
- **Commission-Based**: Agent earns commission (% of sales), not margin

**Advantage**: Agent assumes no inventory/payment risk (easier entry, but lower reward)

**Legal Distinction**: Agency relationships create potential liability for Supplier (agent's actions bind Supplier) - more regulation in some jurisdictions (e.g., EU Commercial Agency Directive)

#### Strategic Partner (Broader Relationship)

**Structure**: Comprehensive collaboration (may include distribution + co-development + technology integration)

**Characteristics**:
- **Beyond Resale**: Joint product development, marketing, support
- **Revenue/Profit Sharing**: Not just margin-based (may share revenue or profit)
- **Long-Term**: Multi-year relationship with strategic alignment

**See Also**: `strategic_partnerships.md` for comprehensive partnership treatment

**This File Focus**: Distributor/Reseller relationships (not agents or broad partnerships)

### Direct vs. Indirect Sales

**Direct Sales** (No Distributor):
- Supplier sells directly to end customers (own sales force, online store)
- **Advantages**: Control (pricing, customer experience), margin capture (no distributor discount)
- **Disadvantages**: Sales cost (must hire sales team), scalability (hard to reach all markets)

**Indirect Sales** (Through Distributors):
- Supplier sells through distributors to end customers
- **Advantages**: Scalability (leverage distributor's reach), capital efficiency (distributor assumes inventory)
- **Disadvantages**: Margin loss (distributor discount 20-40%), less control (distributor owns customer)

**Hybrid Model** (Common):
- **Direct**: Large enterprise customers (Supplier's enterprise sales team)
- **Indirect**: SMB, regional markets (distributors handle)
- **Channel Conflict**: Must manage carefully (distributors unhappy if Supplier "steals" customers)

## Distribution Agreement Types

### 1. Non-Exclusive Distributor

**Grant**:
```
"Supplier appoints Distributor as a non-exclusive distributor of the Products in
the Territory. Supplier reserves the right to appoint other distributors and to
sell directly in the Territory."
```

**Characteristics**:
- **Multiple Distributors**: Supplier can appoint competitors of Distributor (in same territory)
- **Direct Sales Allowed**: Supplier can sell directly (compete with Distributor)
- **No Minimum Commitments** (Typically): Distributor has no guaranteed volume (unless negotiated)

**When Used**:
- Standard for most industries (broad distribution)
- Low-value products (consumer electronics, software, etc.)
- Early-stage relationships (test before exclusivity)

**Distributor Disadvantage**: Must compete with other distributors and Supplier (lower incentive to invest in marketing/sales)

### 2. Exclusive Distributor

**Grant**:
```
"Supplier appoints Distributor as the exclusive distributor of the Products in the
Territory. Supplier shall not appoint other distributors or sell directly in the
Territory, except [reserved customers/channels]."
```

**Characteristics**:
- **Only Distributor**: Supplier cannot appoint others in Territory (Distributor has monopoly)
- **Direct Sales Prohibited**: Supplier cannot sell directly (unless reserved customers excepted)
- **Minimum Commitments**: Distributor typically commits to minimum purchases/sales (Supplier needs guarantee for exclusivity)

**When Used**:
- New market entry (Distributor invests in building market)
- High-investment products (Distributor needs exclusivity to justify investment)
- Strategic relationships (long-term partnership)

**Supplier Disadvantage**: Locked in (if Distributor underperforms, cannot easily add others), minimum guarantees ensure Distributor buys minimum even if demand low

**Reserved Customers/Channels**:
```
"Notwithstanding exclusivity, Supplier reserves the right to sell directly to:
(a) existing strategic customers (listed in Exhibit A);
(b) government customers (requiring direct contracts);
(c) OEM customers (embedding Products in their products)."
```

Purpose: Allows Supplier to maintain key relationships (while giving Distributor exclusivity for remaining market)

### 3. Sole Distributor

**Grant**:
```
"Supplier appoints Distributor as the sole distributor of the Products in the
Territory. Supplier may sell directly in the Territory, but shall not appoint
other distributors."
```

**Characteristics**:
- **Only Distributor**: Supplier cannot appoint other distributors (Distributor has no distributor competition)
- **Direct Sales Allowed**: Supplier can still sell directly (compete with Distributor, but no other distributors)

**Middle Ground**: More commitment than non-exclusive (no distributor competitors), but less than exclusive (Supplier retains direct sales rights)

**When Used**: Distributor wants protection from distributor competition (but Supplier wants to retain large enterprise direct sales)

### 4. Value-Added Reseller (VAR)

**Definition**: Distributor that adds value to products before reselling (customization, integration, support services)

**Grant**:
```
"Supplier appoints VAR as [non-exclusive/exclusive] value-added reseller of the
Products in the Territory. VAR shall provide [implementation, customization, training,
ongoing support] services to end customers."
```

**Key Difference from Standard Distributor**:
- **Services Required**: VAR must provide value-added services (not just resale)
- **Higher Margin**: VAR typically earns higher margin (35-50%) due to services
- **Certification**: VAR often must complete training/certification (demonstrate technical competence)

**When Used**: Complex products requiring implementation (enterprise software, hardware systems, industrial equipment)

**Example**: SAP VAR implements SAP ERP for customers (configures, customizes, trains) - earns margin on license resale + fees for services

### 5. Original Equipment Manufacturer (OEM)

**Definition**: Distributor embeds Supplier's products into its own products (Distributor's brand, not Supplier's)

**Grant**:
```
"Supplier appoints OEM as [non-exclusive/exclusive] OEM partner. OEM may embed the
Products into OEM Products, rebrand, and sell to end customers under OEM's brand."
```

**Key Characteristics**:
- **Rebranding**: OEM removes Supplier's brand, applies own brand (Supplier is invisible to end customer)
- **Bundling**: Products sold as part of OEM's integrated offering (not standalone)
- **Volume-Based Pricing**: Deep discounts (50-80% off list) due to volume and brand sacrifice

**When Used**: Supplier wants volume (sacrifice brand for scale), OEM wants complete solution (white-label component)

**Example**: Dell embeds Intel CPUs in Dell computers (customer sees "Dell computer," Intel is component). Intel gives Dell OEM pricing (deep discount).

**See Also**: `technology_licensing.md` for OEM licensing considerations

## Territory and Geographic Scope

### Territory Definition

**Critical**: Territory must be clearly defined (disputes over geographic scope common)

**Examples**:

**By Country**:
```
"Territory: United States (all 50 states and territories)"
```

**By Region**:
```
"Territory: EMEA (Europe, Middle East, Africa), excluding Russia"
```

**By State/Province**:
```
"Territory: California, Oregon, and Washington"
```

**Worldwide**:
```
"Territory: Worldwide, excluding [Reserved Territories]"
```

### Territory Exclusivity Issues

**Exclusive Territory**: Distributor has exclusive rights in Territory (Supplier cannot appoint others or sell directly, except reserved customers)

**Non-Exclusive Territory**: Supplier can appoint multiple distributors in same Territory (overlap)

**Cross-Territory Sales** (Major Dispute Area):

**Scenario**: Distributor A has exclusive rights in Territory A (US), Distributor B has exclusive rights in Territory B (EU). US customer asks Distributor A to ship to EU subsidiary.

**Question**: Can Distributor A fulfill (sell into Territory B)? Or must refer to Distributor B?

**Typical Restriction**:
```
"Distributor shall sell Products only to customers located in the Territory.
Distributor shall not actively solicit or market to customers outside the Territory.
Passive orders (unsolicited orders from outside Territory) should be referred to
Supplier or authorized distributor for that territory."
```

**Active vs. Passive Sales**:
- **Active Sales** (Prohibited): Distributor actively markets into other distributor's territory (website targeting, advertising, outbound sales calls)
- **Passive Sales** (Allowed): Customer from another territory contacts Distributor unsolicited (Distributor can fulfill or refer)

**EU Competition Law**: Prohibiting passive sales may violate EU competition law (restrict cross-border trade). Consult EU antitrust counsel for EU territories.

### Reserved Customers

**Purpose**: Allow Supplier to maintain direct relationships with strategic customers (even in exclusive territories)

**Structure**:
```
"Notwithstanding Distributor's exclusive rights in Territory, Supplier reserves
the right to sell directly to the following customers:
(a) Named Accounts (listed in Exhibit A): [Fortune 100 companies, government agencies]
(b) OEM Customers: Customers embedding Products into their products
(c) Existing Customers: Customers with direct agreements executed before Effective Date"
```

**Distributor Concern**: Reserved customers reduce addressable market (exclusivity less valuable)

**Negotiation**:
- **Narrow Reserve**: Minimize reserved customers (list specific names, not categories)
- **Revenue Share**: If Supplier sells to reserved customer in Territory, Distributor earns commission (e.g., 10-20%) as "finder's fee"

## Pricing, Discounts, and Margins

### Wholesale Pricing

**Discount from List Price**:
```
"Supplier shall sell Products to Distributor at [40%] discount from Supplier's
then-current list price."
```

**Typical Discounts by Industry**:
- **Software**: 30-50% (high-margin business)
- **Hardware/Electronics**: 20-30% (lower margin, competitive)
- **Industrial Equipment**: 25-40% (varies by product complexity)

**Volume-Based Discounts**:
```
Tier 1: 1-100 units per quarter → 30% discount
Tier 2: 101-500 units per quarter → 35% discount
Tier 3: 500+ units per quarter → 40% discount
```

**Purpose**: Incentivize volume (larger orders → better pricing)

### Price Protection

**Issue**: Supplier lowers prices → Distributor's inventory devalued (bought at old higher price, now worth less)

**Price Protection Clause**:
```
"If Supplier reduces list price on any Product, Distributor shall receive credit
equal to [100%] of the price reduction, applied to Distributor's inventory of such
Product held as of the price reduction date (up to [90 days] of inventory)."
```

**Example**:
- Distributor bought 100 units at $100 each (40% discount from $166 list) = $10K
- Supplier reduces list price to $150 (new wholesale $90)
- Distributor's 100 units now worth $9K (not $10K) → $1K loss
- **Price Protection**: Supplier credits Distributor $1K (refunds price difference)

**Limitation**: "Up to 90 days of inventory" (protects Distributor's reasonable inventory, not excessive stockpiling)

### Minimum Advertised Price (MAP)

**Purpose**: Prevent price wars among distributors (race to bottom hurts brand)

**MAP Policy**:
```
"Distributor shall not advertise Products below the Minimum Advertised Price (MAP)
listed in Supplier's MAP Policy (Exhibit B). Distributor may sell below MAP, but
may not publicly advertise below MAP."
```

**Key Distinction**:
- **Can Sell Below MAP**: Distributor can negotiate with customer (sell at any price), but cannot advertise below MAP
- **Cannot Dictate Resale Price**: Supplier cannot require Distributor to sell at specific price (illegal price-fixing) - can only restrict advertising (antitrust distinction)

**Enforcement**: Violation of MAP → loss of co-op marketing funds, suspension, or termination

**Antitrust Risk**: MAP policies must be unilateral (Supplier announces policy, does not negotiate with distributors). Consult antitrust counsel before implementing.

### Co-Op Marketing Funds (Market Development Funds)

**Purpose**: Supplier provides funds to Distributor for local marketing (joint investment in demand generation)

**Structure**:
```
"Supplier shall provide Market Development Funds (MDF) equal to [3-5%] of
Distributor's net purchases, to be used for Supplier-approved marketing activities
(advertising, events, webinars, training)."
```

**MDF Governance**:
- **Pre-Approval**: Distributor submits marketing plan, Supplier approves before execution (ensures brand compliance)
- **Reimbursement**: Distributor fronts costs, submits receipts, Supplier reimburses (or credits against future purchases)
- **Use-It-or-Lose-It**: MDF expires if not used within [quarter/year] (incentivizes active marketing)

## Purchase Commitments and Forecasting

### Minimum Purchase Commitments

**Exclusive Distribution**: Supplier typically requires minimum commitments (guarantees volume in exchange for exclusivity)

**Structure**:
```
"Distributor commits to purchase minimum quantities:
Year 1: $1M
Year 2: $2M
Year 3: $3M

Measured quarterly: Distributor must meet [75%] of prorated commitment each quarter,
or Supplier may convert to non-exclusive or terminate."
```

**Consequences of Failure**:
- **Shortfall Payment**: Pay shortfall amount (e.g., committed $1M, purchased $800K → pay $200K cash)
- **Conversion to Non-Exclusive**: Lose exclusivity (Supplier can appoint others)
- **Termination**: Supplier may terminate agreement

**Distributor Negotiation**:
- **Ramp-Up**: Lower commitments in Year 1 (market building phase), higher in Years 2-3
- **Cure Period**: 30-60 days to cure shortfall (buy more inventory to meet commitment)
- **Force Majeure Exception**: Excused if failure due to events outside control (pandemic, natural disaster)

### Purchase Forecasting

**Rolling Forecasts**:
```
"Distributor shall provide Supplier with rolling 6-month demand forecast, updated
monthly. Months 1-3 are binding (Distributor commits to purchase), Months 4-6 are
non-binding (forecast only)."
```

**Purpose**:
- **Supplier Production Planning**: Forecasts help Supplier manage inventory, manufacturing capacity
- **Distributor Commitment**: Binding period (months 1-3) ensures Distributor orders what they forecast (reduces forecast gaming)

**Flexibility**:
```
"Distributor may adjust binding forecast by up to [20%] per month with [30] days' notice."
```

**Liability for Inaccurate Forecasts**:
- **Typically No Liability**: Forecasts are good-faith estimates (not guarantees), but binding period creates obligation
- **Exception**: If Distributor materially over-forecasts to secure capacity, then cancels → Supplier may charge cancellation fee or require purchase of [50%] of committed quantity

## Intellectual Property and Branding

### License to Trademarks

**Critical**: Distributor needs license to use Supplier's trademarks (advertise, market products)

**Grant**:
```
"Supplier grants Distributor a non-exclusive, non-transferable license to use
Supplier's Trademarks solely to market and sell the Products in the Territory,
in accordance with Supplier's Brand Guidelines (Exhibit C)."
```

**Brand Guidelines**:
- **Logo Usage**: Size, color, placement restrictions (maintain brand consistency)
- **Approval Rights**: Supplier must approve marketing materials before use (ensure quality control)
- **No Implied Endorsement**: Distributor cannot suggest Supplier endorses Distributor's other products or services

**Quality Control Requirement** (Trademark Law):
- Supplier must control "nature and quality" of goods/services bearing trademark (avoid "naked license" = trademark abandonment)
- **Inspection Rights**: Supplier may inspect Distributor's materials, require changes

**See Also**: `technology_licensing.md` for comprehensive trademark licensing treatment

### IP Infringement Indemnification

**Supplier Indemnity**:
```
"Supplier shall indemnify, defend, and hold harmless Distributor from third-party
claims that the Products infringe any patent, copyright, or trade secret."
```

**Exceptions**:
- Infringement caused by Distributor's modifications or combination with other products
- Infringement from use outside authorized specifications

**Remedies**:
```
"If infringement claim, Supplier may: (a) obtain license for Distributor;
(b) replace Products with non-infringing alternative; (c) modify Products; or
(d) refund Distributor's purchase price and terminate."
```

**See Also**: `indemnification.md` for comprehensive indemnification treatment

## Support, Warranties, and Returns

### Product Warranty Flow-Through

**Supplier's Warranty to Distributor**:
```
"Supplier warrants that Products will conform to Specifications for [90 days]
from delivery to Distributor."
```

**Distributor's Warranty to End Customers**:
```
"Distributor shall pass through Supplier's standard warranty to end customers
(Exhibit D: Supplier End-User Terms). Distributor makes no additional warranties."
```

**Warranty Disclaimer**:
```
"EXCEPT AS EXPRESSLY PROVIDED, SUPPLIER DISCLAIMS ALL WARRANTIES, INCLUDING IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR PARTICULAR PURPOSE."
```

**Purpose**: Supplier limits exposure (Distributor cannot promise more than Supplier provides)

### Support Model

**Model 1: Supplier Provides All Support**
```
"Supplier shall provide technical support directly to end customers. Distributor
shall refer all support requests to Supplier."
```
- **Advantage (Supplier)**: Control (quality, consistency)
- **Disadvantage**: Supplier bears support cost (no revenue from Distributor for support)

**Model 2: Distributor Provides First-Level Support**
```
"Distributor shall provide Level 1 support (installation, basic troubleshooting).
Distributor may escalate to Supplier for Level 2/3 support (complex technical issues)."
```
- **Advantage (Supplier)**: Offload basic support (reduce cost)
- **Advantage (Distributor)**: Deeper customer relationship (control support experience)
- **Requirement**: Distributor must be trained (certification program)

**Support Compensation**:
```
"Supplier shall compensate Distributor [X%] of product price for providing support
services, or Distributor may charge customers separately."
```

### Returns and Inventory

**Return for Refund/Credit**:
```
"Distributor may return Products to Supplier for credit only if:
(a) Products are defective (within warranty period);
(b) Products were shipped in error;
(c) Products are returned by end customer within [30] days (new, unopened).

Return Authorization (RMA) required. Supplier may charge [15%] restocking fee."
```

**Stock Rotation** (Common in Retail/Software):
```
"Distributor may return up to [10%] of quarterly purchases for stock rotation
(exchange for different Products or credit), subject to RMA and restocking fee."
```

**Purpose**: Helps Distributor manage slow-moving inventory (exchange for faster-selling products)

**End-of-Life (EOL) Products**:
```
"If Supplier discontinues Product (EOL), Distributor may return unsold inventory
for [100%] credit (if returned within [90] days of EOL notice)."
```

**Purpose**: Protects Distributor from inventory risk when Supplier changes product line

## Performance Metrics and Termination

### Key Performance Indicators (KPIs)

**Common Metrics**:
```
"Distributor's performance shall be measured by:
(a) Sales Volume: Quarterly revenue or unit sales vs. target
(b) Market Penetration: New customers acquired per quarter
(c) Customer Satisfaction: CSAT or NPS scores from end customers
(d) Inventory Turns: Inventory turnover rate (minimize stale inventory)
(e) Certification: % of sales team certified on Products (technical competence)"
```

**Consequences of Underperformance**:
- **Quarterly Business Review (QBR)**: If below targets, Supplier and Distributor meet to discuss remediation
- **Performance Improvement Plan**: 60-90 days to improve (specific actions, milestones)
- **Conversion to Non-Exclusive**: If exclusive Distributor underperforms, lose exclusivity
- **Termination**: Persistent underperformance (e.g., below 70% of target for 2 consecutive quarters)

### Termination Rights

**Termination for Convenience**:
```
"Either party may terminate this Agreement for convenience upon [90-180] days'
advance written notice."
```

**Termination for Breach**:
```
"Either party may terminate if the other party materially breaches and fails to
cure within [30] days after written notice."
```

**Termination for Insolvency**:
```
"Either party may terminate immediately if the other party files bankruptcy,
becomes insolvent, or makes assignment for benefit of creditors."
```

**Termination for Change of Control** (Supplier-Favorable):
```
"Supplier may terminate upon [30] days' notice if Distributor undergoes change of
control (acquisition by competitor or >50% ownership change)."
```

**Purpose**: Supplier doesn't want products distributed by competitor (if Distributor acquired by competitor)

### Post-Termination Obligations

**Sell-Off Period**:
```
"For [90] days after termination ('Sell-Off Period'), Distributor may continue
to sell remaining inventory, subject to existing terms. After Sell-Off Period,
Distributor shall return unsold inventory for credit."
```

**Purpose**: Allows Distributor to liquidate inventory (avoid total loss)

**Trademark Usage**:
```
"Distributor shall cease use of Supplier's Trademarks immediately upon termination,
except during Sell-Off Period for selling remaining inventory."
```

**Customer Transition**:
```
"Distributor shall cooperate with Supplier to transition end customers to Supplier
or new distributor (provide customer contact lists, introduce Supplier, coordinate
support handover)."
```

**Confidential Information**:
```
"Distributor shall return or destroy all Supplier Confidential Information (price
lists, marketing materials, technical documentation) within 30 days after termination."
```

**Survival**: Confidentiality obligations survive termination for [3-5] years

## Multi-Jurisdictional Considerations

### Export Controls

**US Export Controls** (if distributing US-origin products internationally):

**Distributor Obligations**:
```
"Distributor shall comply with US Export Administration Regulations (EAR) and not
export or re-export Products to:
(a) embargoed countries (Cuba, Iran, North Korea, Syria, Crimea);
(b) restricted parties (Denied Persons List, Entity List, SDN List);
(c) prohibited end-uses (weapons, military, nuclear proliferation)."
```

**Supplier Screening**:
```
"Supplier may screen Distributor and Distributor's customers against restricted
party lists. Distributor shall provide end-customer information upon request."
```

**Liability Allocation**:
```
"Distributor is responsible for export license compliance for re-exports and in-country
transfers. Supplier is responsible for initial export from US to Distributor."
```

**See Also**: `export_controls.md` for comprehensive treatment

### VAT and Sales Tax

**Tax Responsibility**:
```
"Supplier's prices are exclusive of VAT, sales tax, GST, and other indirect taxes.
Distributor is responsible for collecting and remitting applicable taxes to tax authorities."
```

**Reverse Charge** (EU VAT):
```
"For sales within EU, if both parties are VAT-registered, VAT reverse charge applies
(Distributor self-assesses VAT, Supplier does not charge VAT)."
```

**Withholding Tax** (Cross-Border):
```
"If applicable law requires withholding tax on payments to Supplier, Distributor
shall withhold and remit to tax authorities, and provide Supplier with tax certificates."
```

### Data Privacy (Customer Data Sharing)

**If Distributor Shares Customer Data with Supplier**:

**GDPR Compliance** (EU Customers):
```
"To the extent Distributor provides Supplier with personal data of EU customers:
(a) Distributor represents it has lawful basis to share (consent, contract, legitimate interests);
(b) Parties shall execute Data Processing Agreement (DPA) if Supplier processes data
    on behalf of Distributor;
(c) If both parties are controllers, parties shall execute Joint Controller Agreement."
```

**CCPA Compliance** (California Customers):
```
"Distributor certifies that any California consumer personal data provided to Supplier
has been collected in compliance with CCPA, including appropriate opt-out mechanisms."
```

**Data Use Restrictions**:
```
"Supplier may use customer data only to:
(a) fulfill warranty and support obligations;
(b) improve Products (aggregated/anonymized analytics);
(c) comply with legal obligations.

Supplier shall not use customer data for direct marketing without customers' consent."
```

**See Also**: `data_privacy_regulations.md`, `data_agreements.md`

## Risk Assessment Framework

### High-Risk Indicators (Require Immediate Attention)

**Territory/Exclusivity Ambiguity**:
- ⚠️ Territory not clearly defined (disputes over geographic scope)
- ⚠️ "Exclusive" but reserved customers/direct sales not specified (Distributor expected full exclusivity)
- ⚠️ Cross-territory sales restrictions unclear (Can Distributor ship to customer's foreign subsidiary?)

**Pricing/Margin Issues**:
- ⚠️ No price protection (Supplier can lower prices, devalue Distributor's inventory)
- ⚠️ Minimum purchase commitments excessive (Distributor cannot achieve, faces shortfall penalties)
- ⚠️ MAP policy not documented (price wars among distributors, brand damage)

**IP/Branding Risks**:
- ⚠️ No trademark license granted (Distributor using trademarks without permission = infringement)
- ⚠️ No brand guidelines (Distributor could misuse brand, damage reputation)
- ⚠️ No IP indemnity from Supplier (Distributor liable if Products infringe third-party IP)

**Support/Warranty Unclear**:
- ⚠️ Support responsibilities undefined (both parties think other provides support = customer dissatisfaction)
- ⚠️ Distributor cannot pass through Supplier's warranty (Distributor must warrant more than Supplier provides = liability exposure)

**Channel Conflict**:
- ⚠️ Supplier sells directly in Distributor's exclusive territory (violates exclusivity)
- ⚠️ Multiple distributors with overlapping territories (price competition, customer confusion)

### Medium-Risk Indicators (Require Clarification)

**Performance Metrics Vague**:
- ⚠️ "Commercially reasonable efforts" (no specific targets)
- ⚠️ Minimum commitments but no consequences specified (enforcement unclear)
- ⚠️ KPIs not defined (parties have different expectations)

**Returns/Inventory Management**:
- ⚠️ Return policy unclear (when can Distributor return? restocking fees?)
- ⚠️ No EOL protection (Distributor stuck with obsolete inventory)
- ⚠️ No stock rotation rights (Distributor cannot manage slow-movers)

**Termination Consequences**:
- ⚠️ No sell-off period (Distributor loses all inventory value)
- ⚠️ Customer transition not addressed (customers abandoned, or Supplier steals)

### Low-Risk Indicators (Standard Provisions)

- ✅ Territory clearly defined (specific countries/states)
- ✅ Exclusivity clearly stated (exclusive, sole, or non-exclusive) with reserved customers listed
- ✅ Pricing terms defined (discount from list, volume tiers, price protection)
- ✅ Minimum commitments reasonable with ramp-up (if exclusive)
- ✅ Trademark license granted with brand guidelines and approval rights
- ✅ Support model defined (who provides what level)
- ✅ Warranty flow-through (Distributor passes through Supplier's warranty)
- ✅ IP indemnity from Supplier with standard exceptions
- ✅ Returns policy clear (defects, stock rotation, EOL)
- ✅ Performance metrics specified with KPI targets
- ✅ Termination for convenience with reasonable notice (90-180 days)
- ✅ Post-termination sell-off period and customer transition plan

## Validation Questions

Before finalizing a distribution agreement, validate:

- ✅ **Agreement Type**: Distributor, agent, VAR, OEM? Structure clear?
- ✅ **Exclusivity**: Exclusive, sole, or non-exclusive? Territory clearly defined?
- ✅ **Reserved Customers**: Are any customers reserved for Supplier's direct sales? Listed?
- ✅ **Territory**: Geographic scope clear (countries, states, regions)? Cross-border restrictions?
- ✅ **Products**: Which products covered? All current products + future products?
- ✅ **Pricing**: Discount from list price? Volume tiers? Price protection?
- ✅ **Minimum Commitments**: Required (if exclusive)? Amount per year? Consequences if not met?
- ✅ **Forecasting**: Required? Binding vs. non-binding periods?
- ✅ **MAP Policy**: Minimum advertised price specified? Enforcement mechanism?
- ✅ **Co-Op Funds**: Market development funds (MDF) provided? Percentage of purchases?
- ✅ **Trademark License**: Granted? Brand guidelines provided? Approval rights for materials?
- ✅ **IP Indemnity**: Supplier indemnifies for product infringement? Exceptions?
- ✅ **Warranty**: Supplier's warranty to Distributor? Distributor passes through to customers?
- ✅ **Support**: Who provides customer support? Compensation for Distributor if providing?
- ✅ **Returns**: When can Distributor return? Defects, stock rotation, EOL? Restocking fees?
- ✅ **Performance Metrics**: KPIs defined? Targets specified? Review process?
- ✅ **Term & Renewal**: Fixed term or evergreen? Auto-renewal? Opt-out notice?
- ✅ **Termination for Convenience**: Allowed? Notice period (90-180 days)?
- ✅ **Post-Termination**: Sell-off period? Inventory return for credit? Customer transition?
- ✅ **Export Compliance**: If international, export control obligations specified?
- ✅ **Data Privacy**: If customer data shared, GDPR/CCPA compliance addressed? DPA needed?

## When to Consult Experts

Engage legal counsel with expertise in distribution law when:

- **Exclusive Distribution**: High commitment (minimum guarantees, exclusivity)
- **International**: Multi-country distribution (export controls, VAT, data privacy, local laws)
- **EU Distribution**: EU Commercial Agency Directive, EU competition law (passive sales restrictions)
- **Antitrust Concerns**: MAP policies, territorial restrictions, exclusive dealing
- **Channel Conflict**: Disputes between Supplier and Distributor (or among multiple distributors)
- **High-Value Products**: Significant revenue (>$5M annually) or strategic products
- **OEM Agreements**: White-label embedding (complex IP, royalty structures)
- **Regulatory Products**: Products requiring certifications, licenses (medical devices, aerospace, defense)
- **Termination Disputes**: Distributor claims wrongful termination, seeks damages
- **M&A**: Acquiring or being acquired (distribution agreement assignment, change of control provisions)

Consult distribution counsel BEFORE appointing exclusive distributors (exclusivity is hard to unwind if relationship fails).

## References

> ⚠️ **Reminder**: This is a **synthetic skill** created for validation system testing. While based on general legal principles, it has NOT been validated by expert practitioners. Use as a framework for identifying claims requiring validation, not as authoritative legal guidance.

**Cross-Reference Related Skills**:
- `keller_patterns.md` - Cognitive reasoning patterns (S1-S13)
- `contract_law.md` - Contract formation, interpretation, breach
- `strategic_partnerships.md` - Broader partnership structures (beyond pure resale)
- `technology_licensing.md` - OEM licensing, trademark licensing
- `software_licensing.md` - Software-specific distribution terms
- `export_controls.md` - EAR compliance for international distribution
- `data_privacy_regulations.md` - GDPR, CCPA (if customer data shared)
- `indemnification.md` - IP infringement indemnification mechanics

**Contract Intelligence Skills** (from 4,900+ real contracts):
- `distribution-agreement-expected-clauses.md` - Expected clauses for distribution
- `termination-taxonomy.md` - Distributor termination patterns
- `payment-terms-taxonomy.md` - Pricing and payment structures
- `non-compete-taxonomy.md` - Exclusivity and territory restrictions

**Cognitive Patterns** (apply to distribution analysis):
- `S1` - Stakeholder identification (manufacturer, distributor, end customers)
- `S5` - Party dynamics (channel power and leverage)
- `S7` - Multi-perspective (manufacturer vs. distributor interests)
- `BI4` - Battle selection (key distribution terms)

**Key Legal Frameworks** (for validation):
- Uniform Commercial Code (UCC) Article 2 - sales of goods
- Sherman Antitrust Act - MAP policies, territorial restrictions, exclusive dealing
- EU Commercial Agency Directive (if EU agents vs. distributors)
- EU Competition Law - vertical agreements, passive sales restrictions
- Export Administration Regulations (EAR) - US export controls

**Validation Sources** (when validating claims in analysis):
- Distribution agreement text (territory, exclusivity, pricing, commitments)
- Product price lists (MSRP, wholesale pricing, discounts)
- Brand guidelines (trademark usage, quality standards)
- Performance reports (sales vs. targets, KPIs)
- Web search for current distribution law case law, antitrust guidance on MAP/territorial restrictions
