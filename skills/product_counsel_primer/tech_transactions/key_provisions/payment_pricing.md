---
name: payment-pricing
description: Payment Pricing
tags:
  - commercial-terms
  - payment
  - pricing
version: '1.0'
confidence_level: MEDIUM
category: key_provisions
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
mentoring_priority: 1
validation_type: synthetic
source_type: expert_judgment
---

# Payment and Pricing Provisions

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**

## Metadata

```yaml
skill_id: payment_pricing
domain: contract_provisions
sub_domains: [subscription_pricing, usage_based_pricing, payment_terms, late_fees, price_increases, taxes]
jurisdictions: [united_states, international]
confidence: 0.70
validation_status: synthetic
requires: [keller_patterns, contract_law]
complements: [service_levels, termination_provisions, warranties_representations]
skill_tier: foundational
mentoring_priority: 1
```

## Core Principles

### Payment Structures in Tech Contracts

**Why Pricing Matters**:
- **Revenue Model**: Determines how vendor gets paid (upfront, recurring, usage-based)
- **Customer Budgeting**: Affects customer's ability to plan costs (fixed vs. variable)
- **Risk Allocation**: Who bears risk of usage fluctuations (flat fee vs. consumption-based)

**Common Pricing Models**:
1. **Perpetual License + Maintenance**: One-time license fee + annual maintenance (traditional software)
2. **Subscription**: Recurring fee (monthly/annual) for SaaS/cloud services
3. **Usage-Based**: Pay for consumption (API calls, data storage, compute hours)
4. **Freemium**: Free tier + paid upgrades (common in SaaS)
5. **Transaction-Based**: Fee per transaction (payment processing, marketplace)

## Subscription Pricing

### Fixed Subscription Fees

**Structure**: Customer pays flat fee for access (regardless of usage)

**Example**:
```
"Customer shall pay $10,000 per month for unlimited users and data storage."
```

**Advantages**:
- **Predictable**: Customer knows exact monthly cost
- **Simple**: No usage tracking or reconciliation
- **Sales**: Easier to sell (customer doesn't worry about overages)

**Disadvantages**:
- **Vendor Risk**: Vendor bears cost of heavy usage (if customer uses 10x expected resources)
- **Customer Inefficiency**: Customer pays same price even if low usage

### Tiered Pricing

**Structure**: Different price tiers based on features or usage limits

**Example**:
```
- Starter: $50/month (up to 10 users, 10GB storage)
- Professional: $200/month (up to 50 users, 100GB storage)
- Enterprise: $1,000/month (unlimited users, 1TB storage)
```

**Tier Movement**:
- **Automatic Upgrade**: If customer exceeds tier limit, automatically upgrade (charge higher price)
- **Manual Upgrade**: Customer must manually upgrade (or hit usage cap and lock out)
- **Overage**: Charge overage fees for exceeding tier limit

**Best Practice**: Clearly define upgrade/downgrade process
```
"If Customer exceeds tier usage limit, Customer will be automatically upgraded to next tier and charged applicable
monthly fee on next billing cycle. Customer may downgrade at end of billing period with 30 days notice."
```

### Per-User Pricing

**Structure**: Price based on number of users (seats)

**Example**:
```
"$25 per user per month (minimum 10 users)"
```

**User Definition**:
- **Named User**: Specific individual (cannot share login)
- **Concurrent User**: Number of simultaneous active users (can share login)
- **Active User**: Users who accessed system in billing period

**Common Issues**:
- **Audit Rights**: Vendor right to audit user count (quarterly/annually)
- **True-Up**: Reconcile actual users vs. paid users (charge for excess)
- **Deactivation**: Customer obligation to deactivate users no longer needing access

**Language**:
```
"Customer shall promptly notify Vendor of increases/decreases in user count. Vendor may audit user count
quarterly. If audit reveals >5% underpayment, Customer pays audit costs + underpaid fees + interest."
```

## Usage-Based Pricing

### Consumption-Based Pricing

**Structure**: Pay for actual usage (API calls, data processed, compute hours)

**Example**:
```
"$0.01 per API call + $0.10 per GB data storage + $1.00 per compute hour"
```

**Advantages**:
- **Fair**: Customer pays only for what they use
- **Scalable**: Vendor revenue scales with customer usage
- **Attractive for Startups**: Low entry cost (pay as you grow)

**Disadvantages**:
- **Unpredictable**: Customer doesn't know monthly cost (can spike unexpectedly)
- **Billing Complexity**: Requires usage metering and reconciliation

### Usage Caps and Overage

**Monthly Cap**:
```
"Customer's usage capped at 1M API calls per month. If Customer exceeds cap, Vendor may throttle or
suspend Service until next billing period (or Customer pays overage)."
```

**Overage Fees**:
```
"Included: 1M API calls/month. Overage: $0.02 per additional API call."
```

**Soft vs. Hard Caps**:
- **Soft Cap**: Overage allowed (charged at overage rate)
- **Hard Cap**: Usage cut off at cap (no overage, service throttled/suspended)

**Best Practice**: Notify customer approaching cap
```
"Vendor shall notify Customer when usage reaches 80% and 100% of cap."
```

### Minimum Commitments

**Structure**: Customer commits to minimum spend (regardless of actual usage)

**Example**:
```
"Customer commits to $100,000 minimum annual spend. If actual usage < $100,000, Customer pays shortfall."
```

**Purpose**: Vendor ensures minimum revenue (reduce risk of low usage)

**Negotiation**:
- **Vendor Preference**: High minimum commitment (guaranteed revenue)
- **Customer Preference**: Low/no minimum (pay only for actual usage)
- **Compromise**: Graduated minimums (Year 1: $50K, Year 2: $100K, Year 3: $150K)

**Rollover Credits**:
```
"Unused commitment credits do not roll over to next year."
```

**Or**:
```
"Up to 20% of unused commitment credits may roll over to next year."
```

## Payment Terms

### Invoice and Payment Timing

**Advance Payment** (Common for SaaS):
```
"Fees payable in advance at beginning of each billing period (monthly or annually)."
```

**Arrears Payment** (Common for Usage-Based):
```
"Fees payable within 30 days after end of billing period (based on actual usage)."
```

**Annual Prepayment Discount**:
```
"If Customer pays annually in advance, 10% discount applied (vs. monthly payments)."
```

**Purpose**: Vendor incentivizes upfront payment (better cash flow, reduces churn)

### Payment Methods

**Accepted Methods**:
- **Credit Card**: Automatic recurring billing (common for SMB SaaS)
- **ACH/Wire**: Direct bank transfer (common for enterprise)
- **Purchase Order + Invoice**: Net-30 terms (enterprise customers)

**Automatic Renewal**:
```
"Fees automatically charged to Customer's payment method on file at renewal. Customer may update payment method
or cancel auto-renewal with 30 days notice before renewal date."
```

**Failed Payment**:
```
"If payment fails, Vendor may suspend Service after 10 days notice. Customer responsible for all collection
costs (including attorney's fees)."
```

### Late Payment Fees and Interest

**Late Fee**:
```
"If payment not received within 30 days of invoice date, late fee of $100 or 5% of overdue amount (whichever greater)
shall apply."
```

**Interest**:
```
"Overdue amounts accrue interest at 1.5% per month (18% APR) or maximum rate permitted by law, whichever less."
```

**Suspension for Non-Payment**:
```
"If payment overdue >30 days, Vendor may suspend Service until payment received (without breach of SLA)."
```

**Best Practice**: Grace period + notice before suspension (10-15 days notice)

## Price Increases

### Annual Price Increases

**Fixed Increase**:
```
"Fees may increase up to 5% annually upon 60 days written notice."
```

**CPI-Linked**:
```
"Fees may increase annually by lesser of (a) 5% or (b) percentage increase in Consumer Price Index (CPI)."
```

**Mutual Agreement**:
```
"Fees may increase only upon mutual written agreement (no unilateral increases)."
```

**Negotiation Dynamics**:
- **Vendor Preference**: Right to increase prices annually (inflation, cost increases)
- **Customer Preference**: Price lock for initial term (predictable budgeting)
- **Compromise**: Annual increase capped at CPI or fixed percentage (3-5%)

### Mid-Term Price Changes

**Generally Not Allowed**:
```
"Vendor may not increase Fees during initial term. Upon renewal, fees may increase up to 10% with 90 days notice."
```

**Customer Termination Right**:
```
"If Vendor increases Fees >10%, Customer may terminate Agreement with 30 days notice and receive pro-rata refund
of prepaid fees."
```

**Purpose**: Protect customer from unexpected price shock mid-contract

## Taxes and Fees

### Sales Tax

**Customer Responsibility** (Standard):
```
"Fees exclude all taxes. Customer responsible for all sales, use, VAT, GST, and other taxes (except taxes on
Vendor's income)."
```

**Tax Exemption**:
```
"If Customer tax-exempt, Customer shall provide valid tax exemption certificate. Otherwise, Vendor may collect
applicable taxes."
```

**Nexus Issues**:
- **Sales Tax**: US state sales tax if vendor has nexus (physical presence, economic nexus post-Wayfair)
- **VAT**: EU VAT if vendor exceeds €10K sales in EU (reverse charge for B2B)

### Withholding Tax

**International Payments**:
```
"If applicable law requires Customer withhold taxes on payments to Vendor, Customer shall (a) withhold required
amount, (b) pay to tax authority, (c) provide withholding certificate to Vendor, and (d) gross-up payment so
Vendor receives full fee amount."
```

**Gross-Up**:
- **Customer**: Doesn't want to pay more than agreed fee (withholding comes from vendor's portion)
- **Vendor**: Wants full fee amount (customer gross-up to cover withholding)

**Example**:
- Fee: $100K
- Withholding: 10% ($10K)
- Without Gross-Up: Customer pays $100K, vendor receives $90K
- With Gross-Up: Customer pays $111.11K, vendor receives $100K (after $11.11K withholding)

## Transaction-Based Pricing

### Payment Processing Fees

**Structure**:
```
"2.9% + $0.30 per transaction (credit card processing)"
```

**Who Pays**:
- **Merchant**: Absorbs fee (customer pays $100, merchant receives $97.10)
- **Customer**: Pays fee (customer pays $102.90, merchant receives $100)

**Minimum Transaction Fee**:
```
"Minimum $1.00 fee per transaction (for small transactions <$10)"
```

### Marketplace/Platform Fees

**Revenue Share**:
```
"Platform retains 30% of transaction value (seller receives 70%)"
```

**Listing Fees**:
```
"$0.20 per item listed + 10% of sale price when sold"
```

**Example**: Etsy, eBay, App Store

## Refunds and Credits

### Refund Policies

**No Refunds** (Common for Subscription):
```
"All fees are non-refundable. No refunds for partial months or early termination."
```

**Pro-Rata Refund** (Customer-Favorable):
```
"If Customer terminates for convenience, Vendor shall refund unused portion of prepaid fees (pro-rata)."
```

**Money-Back Guarantee** (Freemium/Low-Risk):
```
"30-day money-back guarantee. If not satisfied, Customer may request full refund within 30 days of purchase."
```

### Service Credits for SLA Breach

**Credit Structure**:
```
"If Uptime < 99.9%, Customer receives service credit:
- 99.0-99.9%: 10% monthly fee credit
- 95.0-99.0%: 25% monthly fee credit
- <95.0%: 50% monthly fee credit"
```

**Credit Limitations**:
```
"Service credits are Customer's sole remedy for SLA breach. Credits do not roll over (must use within 12 months).
Maximum credits per year: 100% of annual fees."
```

**See Also**: `service_levels.md` for SLA details

## Audit Rights

### Usage and Billing Audits

**Vendor Audit of Customer Usage**:
```
"Vendor may audit Customer's usage and user count up to once per quarter, upon 15 days notice, during business hours.
If audit reveals underpayment >5%, Customer pays audit costs + underpaid fees + interest."
```

**Customer Audit of Vendor Billing**:
```
"Customer may audit Vendor's billing and usage metering records up to once per year, upon 30 days notice.
If audit reveals overcharge >5%, Vendor refunds overcharged amount + audit costs."
```

**Third-Party Auditor**:
```
"Audits conducted by independent third-party auditor mutually acceptable to both parties, under NDA."
```

## International Payment Considerations

### Currency

**USD Payments**:
```
"All fees payable in US Dollars (USD). Customer bears currency conversion costs and exchange rate fluctuations."
```

**Local Currency**:
```
"Fees invoiced in Customer's local currency at Vendor's then-current exchange rate."
```

**Fluctuation Protection**:
```
"If exchange rate fluctuates >10% from rate at contract execution, Vendor may adjust fees to reflect new rate."
```

### Cross-Border Payment Fees

**Wire Transfer Fees**:
```
"Customer responsible for all wire transfer, banking, and intermediary fees. Payment must be received by Vendor
in full (net of all fees)."
```

**Payment Timing**:
- International wire transfers: 3-5 business days (vs. 1-2 days domestic)
- Consider advance payment to avoid delays

## Pricing for Different Business Models

### Freemium Model

**Free Tier**:
```
"Free Plan: 10 users, 1GB storage, 1,000 API calls/month. Paid plans available for additional capacity."
```

**Conversion Path**: Free → Starter ($50/month) → Professional ($200/month) → Enterprise (custom)

**Limitations on Free Tier**:
- No SLA (best-efforts only)
- Limited support (email only, 48-hour response)
- Vendor may discontinue free tier with 30 days notice

### Enterprise Custom Pricing

**Volume Discounts**:
```
"For contracts >$100K annually, custom pricing available upon request."
```

**Negotiated Terms**:
- Custom SLA (99.99% uptime)
- Dedicated support (24/7, <1 hour response)
- Committed spend discounts (10-30% off list price)

**Most Favored Customer (MFC)**:
```
"Vendor represents that pricing provided to Customer is equal to or better than pricing provided to other
similarly situated customers."
```

**Risk**: Difficult to enforce (vendor's other customer pricing typically confidential)

## Risk Assessment Framework

### High-Risk Red Flags

**Pricing Structure**:
- ⚠️ Unlimited price increases (vendor can raise prices any time, any amount)
- ⚠️ No cap on usage-based pricing (could result in unexpected $100K bill)
- ⚠️ Automatic tier upgrades without customer approval (customer has no control)
- ⚠️ Minimum commitment with no rollover (customer loses unused credits)

**Payment Terms**:
- ⚠️ Immediate suspension for late payment (no grace period or notice)
- ⚠️ Automatic renewal with no cancellation notice (customer locked in)
- ⚠️ Non-refundable fees even if vendor breaches (customer pays for bad service)

**Taxes**:
- ⚠️ Customer pays all taxes including vendor's income taxes (overly broad)
- ⚠️ No gross-up for withholding taxes (vendor receives less than agreed fee)

### Medium-Risk Areas

**Price Increases**:
- ⚠️ Annual increases >10% (difficult to budget)
- ⚠️ No cap on CPI-linked increases (if inflation spikes)

**Billing**:
- ⚠️ No usage alerts (customer doesn't know when approaching overage)
- ⚠️ Usage-based billing with no cap (unpredictable costs)

**Audits**:
- ⚠️ Frequent audits (quarterly audits disruptive)
- ⚠️ Vendor-selected auditor (not independent)

### Low-Risk (Standard Market Terms)

- ✅ Fixed subscription pricing or capped usage-based pricing
- ✅ Annual price increases capped at 3-5% or CPI
- ✅ 30-day payment terms with 10-15 day grace period before suspension
- ✅ Pro-rata refund for prepaid fees upon termination
- ✅ Customer responsible for taxes (except vendor income taxes)
- ✅ Usage alerts at 80% and 100% of tier limit
- ✅ Automatic renewal with 30-60 days cancellation notice

## Validation Questions

When analyzing payment and pricing provisions:

### Pricing Model
- [ ] What is the pricing model? (Subscription, usage-based, per-user, transaction-based)
- [ ] Are fees fixed or variable? (Predictable vs. consumption-based)
- [ ] Are there tier limits? (What happens if exceeded - overage, upgrade, throttle)
- [ ] Is there a minimum commitment? (Annual spend floor)

### Payment Terms
- [ ] When are fees due? (Advance, arrears, net-30)
- [ ] What payment methods accepted? (Credit card, ACH, wire, PO)
- [ ] Are there late fees or interest? (% per month, flat fee)
- [ ] What happens if payment fails? (Grace period, suspension, termination)

### Price Increases
- [ ] Can vendor increase prices during term? (Fixed pricing or price escalation clause)
- [ ] What is cap on annual increase? (CPI, fixed %, no cap)
- [ ] What notice required for increase? (30, 60, 90 days)
- [ ] Can customer terminate if price increase exceeds threshold? (>10% increase → termination right)

### Taxes
- [ ] Who pays taxes? (Customer pays sales/VAT/GST, vendor pays income tax)
- [ ] Is there withholding tax? (International payments)
- [ ] Who bears currency conversion costs? (Customer or vendor)

### Refunds
- [ ] Are fees refundable? (Non-refundable, pro-rata refund, money-back guarantee)
- [ ] What if vendor breaches SLA? (Service credits, refunds, termination right)
- [ ] Do unused credits roll over? (Annual commitment)

### Audits
- [ ] Can vendor audit usage? (Frequency, notice, customer cost if underpayment)
- [ ] Can customer audit billing? (Accuracy verification)
- [ ] Who conducts audit? (Independent third party or vendor/customer staff)

---

## Business Intelligence Overlay: Incentive-Aligned Pricing Models & Value-Based Pricing

**Integration with BI Skills:**
- **BI1 (Strategic Value Assessment):** Price based on customer value, not vendor cost
- **BI2 (Downside Risk & Incentive Alignment):** Pricing structures that self-enforce performance and align interests
- **BI3 (Resource Constraints):** Cash flow timing and payment structure optimization
- **BI5 (Alternatives Analysis):** Framework for choosing optimal pricing model

---

### Application 1: Incentive-Aligned Pricing - Milestone vs. Fixed vs. Revenue Share

**The Pricing Incentive Problem:**

**Example: Custom Software Development Gone Wrong**

```
Contract: $500K fixed fee for custom CRM system
Payment: $100K upfront, $400K upon delivery
Timeline: 6 months estimated

Vendor's Incentive Structure:
- Collected $100K upfront (sunk cost for customer)
- Remaining $400K paid regardless of quality/timeline
- Vendor's priority: Minimize cost, maximize profit margin
- Customer's priority: High quality, timely delivery, ongoing support

Economic Reality at Month 6:
- System 60% complete, buggy, missing key features
- Vendor spent $300K, has $100K sunk cost in customer
- Customer: "Fix issues before final payment"
- Vendor: "We delivered per spec, pay $400K or we stop work"

Standoff Economics:
- Customer threatens to withhold payment
- Vendor threatens to abandon project
- Mutual hold-up: $400K payment vs. $200K completion work
- Likely outcome: Settlement at $250K, customer gets 75% solution

Total Value Destruction:
- Vendor receives: $350K ($100K + $250K settlement) for $300K cost → +$50K
- Customer gets: 75% solution worth $300K for $350K paid → -$50K
- Expected surplus destroyed: $200K (from $500K full value to $300K partial)
```

**Better Alternative 1 - Milestone-Based Pricing (Self-Enforcing Performance):**

```
Same Project, Different Structure:
$500K total, paid in 5 milestones of $100K each

Milestone 1: Requirements complete + prototype (Month 1) → $100K
Milestone 2: Core module complete + tested (Month 2) → $100K
Milestone 3: Integration complete + user testing (Month 3-4) → $100K
Milestone 4: Full system deployed to staging (Month 5) → $100K
Milestone 5: Production deployment + 30-day stabilization (Month 6) → $100K

Vendor's Incentive Structure:
- Must complete Milestone 1 to get any payment
- Must maintain quality/progress to unlock each $100K
- Cannot collect future payments without delivering prior milestones
- Strong incentive to stay on schedule and meet quality bars

Customer's Incentive Structure:
- Risk limited to $100K per milestone (not $500K upfront)
- Can terminate after any milestone if quality inadequate
- Vendor must earn each payment through demonstrated progress
- Natural checkpoints for course correction

Economic Reality at Month 6:
- All 5 milestones completed successfully
- Vendor earned $500K for $400K cost → +$100K profit
- Customer received $500K value for $500K paid → $0 net, but full solution
- No disputes, no hold-up, no value destruction
- Ongoing relationship established for future work

Key Economic Principle:
Milestone payments create self-enforcing performance incentives
Each party's interests aligned at every stage
Risk distributed across timeline, not concentrated upfront/backend
```

**Better Alternative 2 - Performance-Based Pricing (Pay for Results, Not Effort):**

```
Same Project, Outcome-Based Structure:
$300K base fee + $200K performance bonuses

Base Payment ($300K):
- $100K upon signed requirements (Month 0)
- $200K upon system deployment (Month 6)

Performance Bonuses ($200K):
- +$50K if deployed on time (Month 6 vs. Month 8 deadline)
- +$50K if 90%+ uptime in first 90 days
- +$50K if adoption >80% of target users within 60 days
- +$50K if customer satisfaction score >4.0/5.0

Vendor's Incentive Structure:
- Guaranteed $300K base (cost recovery)
- $200K upside tied to outcomes customer values
- Strong incentive to deliver on time, high quality, user adoption
- Vendor shares risk and reward with customer

Customer's Incentive Structure:
- Pays $300K for delivery (minimal risk)
- Pays $200K bonuses only if real value achieved
- Vendor motivated to optimize for customer success metrics
- Alignment on adoption, quality, and timely delivery

Economic Reality at Month 12:
- System deployed on time (+$50K earned)
- 95% uptime achieved (+$50K earned)
- 85% user adoption (+$50K earned)
- 4.2/5.0 satisfaction score (+$50K earned)

Final Economics:
- Vendor receives: $500K for $400K cost → +$100K profit
- Customer receives: $500K+ value (high adoption, satisfaction) for $500K → Positive ROI
- Perfect incentive alignment: Vendor wins when customer succeeds

Key Economic Principle:
Performance-based pricing ties vendor compensation to customer outcomes
Risk-sharing creates partnership mentality vs. adversarial relationship
Vendor incentivized to maximize customer value, not minimize vendor cost
```

**Better Alternative 3 - Revenue Share (Deep Alignment for Strategic Partnerships):**

```
Same Project, Revenue Share Structure:
$200K fixed fee + 10% of revenue generated by system for 3 years

Fixed Payment ($200K):
- $100K upon requirements + prototype (Month 1)
- $100K upon deployment (Month 6)

Revenue Share (10% for 36 months):
- Customer's target: $5M annual revenue from new CRM
- If achieved: Vendor receives $500K/year × 10% = $50K/year × 3 years = $150K
- Total vendor compensation: $200K + $150K = $350K
- If exceeds target ($7M/year): Vendor receives $200K + $210K = $410K
- If underperforms ($2M/year): Vendor receives $200K + $60K = $260K

Vendor's Incentive Structure:
- Fixed $200K covers cost ($400K total cost, so vendor invests $200K)
- Upside tied to customer's commercial success
- Vendor invested in maximizing system value, adoption, and revenue generation
- Long-term relationship incentive (3-year revenue share)

Customer's Incentive Structure:
- Lower upfront cost ($200K vs. $500K) preserves cash flow
- Vendor shares risk (invested $200K of own capital)
- Vendor incentivized to maximize customer revenue
- Pay for success model: If system doesn't generate revenue, vendor gets only $200K (below cost)

Economic Reality at Year 3:
- System generates $6M/year average revenue
- Vendor receives: $200K + ($6M × 10% × 3 years) = $200K + $180K = $380K
- Customer pays: $380K total for $18M in revenue generated = 2.1% revenue cost
- Customer net: $18M - $380K = $17.6M revenue (vendor generated huge value)

Comparison vs. Fixed Fee:
- Fixed fee: Customer pays $500K regardless of outcome
- Revenue share: Customer pays $380K, only if revenue generated
- Vendor alignment: Revenue share vendor wants customer to succeed (10% of $0 = $0)
- Fixed fee vendor: Already paid, minimal incentive for adoption/success

Key Economic Principle:
Revenue share creates deepest alignment for strategic partnerships
Vendor becomes true partner, not just service provider
Customer gets risk-sharing (pay only if success) and aligned incentives
Best for high-value, uncertain-outcome projects where vendor can influence results
```

**Decision Framework: Choosing the Right Pricing Model**

```
Pricing Model Selection:

IF project outcome is CERTAIN and well-defined:
    → Fixed fee (predictable, simple, works when scope is clear)
    → Example: Routine maintenance, standard integrations, COTS deployment

IF project outcome is UNCERTAIN but milestones are definable:
    → Milestone-based payments (self-enforcing, risk distribution)
    → Example: Custom development, complex integrations, phased rollouts

IF vendor can influence customer success metrics:
    → Performance-based pricing (pay for results, outcome alignment)
    → Example: Consulting, optimization projects, SLA-driven services

IF vendor and customer are strategic partners with shared upside:
    → Revenue share or success fees (deepest alignment, risk-sharing)
    → Example: Joint ventures, platform partnerships, co-innovation

General Rule:
Fixed_Fee → Milestone → Performance_Based → Revenue_Share
(Increasing alignment, increasing vendor risk, increasing potential upside)
```

**Summary Table: Incentive Alignment by Pricing Model**

| Pricing Model | Vendor Incentive | Customer Risk | Alignment Score | Best Use Case |
|---------------|------------------|---------------|-----------------|---------------|
| **Fixed Fee** | Minimize cost, deliver minimum viable | High (all upfront or at end) | Low (3/10) | Certain outcome, clear scope |
| **Time & Materials** | Maximize hours billed | Very High (uncapped) | Very Low (1/10) | Exploratory work, unclear scope |
| **Milestone-Based** | Maintain progress and quality | Medium (distributed) | Medium (6/10) | Phased projects, definable milestones |
| **Performance-Based** | Maximize customer outcomes | Low (pay for results) | High (8/10) | Vendor can influence success metrics |
| **Revenue Share** | Maximize customer revenue/value | Very Low (shared risk) | Very High (10/10) | Strategic partnerships, co-innovation |

**Key Insight:**
The WORST pricing models are those with misaligned incentives:
- Fixed fee with backend-heavy payment → Vendor delays, customer holds payment
- Time & materials with no cap → Vendor maximizes hours, customer wants efficiency
- Fixed fee with all-upfront payment → Vendor has no incentive to complete well/on-time

The BEST pricing models distribute payments across deliverables and tie vendor compensation to customer success.

---

### Application 2: Value-Based Pricing - Price to Customer Value, Not Vendor Cost

**The Cost-Plus Pricing Trap:**

**Example: SaaS Pricing Based on Vendor Cost vs. Customer Value**

```
SaaS Platform: DataFlow Analytics

Vendor's Cost Structure (Per Customer):
- Infrastructure (hosting, storage, compute): $500/month
- Support (customer success, technical support): $300/month
- Sales & marketing (allocated per customer): $200/month
- Total vendor cost per customer: $1,000/month

Cost-Plus Pricing Approach (50% margin):
Vendor calculates: $1,000 cost × 1.5 margin = $1,500/month pricing

Customer A (Small E-commerce, $2M revenue/year):
- DataFlow value: Improves conversion rate by 0.5% → $10K/month additional revenue
- Willingness to pay: Up to $3,000/month (30% of value created)
- Vendor's $1,500/month price: 50% of value created → ACCEPTABLE
- Vendor captures: $1,500/month, Customer keeps $8,500/month → Both win

Customer B (Enterprise Retailer, $500M revenue/year):
- DataFlow value: Improves conversion rate by 0.5% → $2.5M/month additional revenue
- Willingness to pay: Up to $500,000/month (20% of value created)
- Vendor's $1,500/month price: 0.06% of value created → MASSIVE VALUE LEFT ON TABLE
- Vendor captures: $1,500/month, Customer keeps $2,498,500/month → Customer wins huge

Economic Inefficiency:
- Customer B gets 1,667x more value than Customer A
- Both pay same price ($1,500/month)
- Vendor leaves $498,500/month on table with Customer B
- OR vendor prices at $500K/month and loses Customer A entirely
```

**Better Alternative - Tiered Value-Based Pricing:**

```
DataFlow Analytics Tiered Pricing (Value-Aligned):

**Tier 1: Starter ($1,500/month)**
- Up to $5M annual revenue companies
- Captures up to $25K/month value → Customer keeps 94% of value
- Vendor cost: $1,000/month → $500/month profit (33% margin)

**Tier 2: Growth ($5,000/month)**
- $5M-$50M annual revenue companies
- Captures up to $250K/month value → Customer keeps 98% of value
- Vendor cost: $1,200/month (slightly higher support) → $3,800/month profit (76% margin)

**Tier 3: Enterprise ($25,000/month)**
- $50M-$500M annual revenue companies
- Captures up to $2.5M/month value → Customer keeps 99% of value
- Vendor cost: $1,500/month (dedicated support) → $23,500/month profit (94% margin)

**Tier 4: Strategic (Custom pricing, typically $100K-$500K/month)**
- $500M+ annual revenue companies
- Captures up to $25M/month value → Customer keeps 98-99.5% of value
- Vendor cost: $3,000/month (white-glove service) → $97K-$497K/month profit (97-99% margin)

Economic Outcome:
- Customer A (Tier 1): Pays $1,500, gets $10K value → 6.7x ROI ✓
- Customer B (Tier 3): Pays $25K, gets $2.5M value → 100x ROI ✓
- Vendor Revenue: Tier 3 customer pays 16.7x more for same product (different value)
- Vendor Margin: Increases from 33% (Tier 1) to 94% (Tier 3) with minimal cost increase

Key Economic Principle:
Price discrimination based on customer value captured, not vendor cost incurred
Large customers pay significantly more because they derive significantly more value
Small customers pay cost-plus, large customers pay value-based
Vendor captures more total surplus without losing small customers
```

**Value-Based Pricing Decision Framework:**

```
Step 1: Calculate Customer Value (Not Vendor Cost)

Customer_Value = Benefit_Generated - Customer_Cost_to_Achieve

Example - DataFlow Analytics for Customer B (Enterprise Retailer):
Benefit_Generated = 0.5% conversion increase × $500M revenue = $2.5M/month
Customer_Cost_to_Achieve = Alternative solution cost (hire data science team: $100K/month)

Customer_Value = $2.5M - $100K = $2.4M/month (value of using DataFlow vs. next best alternative)

Step 2: Determine Willingness to Pay (Capture Rate)

General Capture Rates:
- Established category (e.g., CRM, ERP): 20-40% of value
- Emerging category (e.g., new analytics): 10-20% of value
- Novel/unproven solution: 5-10% of value

Customer B Willingness to Pay:
DataFlow (established analytics): 20% × $2.4M = $480K/month maximum

Step 3: Design Tiered Pricing Based on Customer Segments

Segment by Proxy Variables (not just revenue):
- Company revenue (small, growth, enterprise, strategic)
- Usage intensity (API calls, data volume, user count)
- Feature access (basic, professional, enterprise features)

Customer B Pricing:
Tier 3 (Enterprise): $25K/month base + $0.01 per API call
- Base: $25K/month for 5M API calls
- Overage: $10/1,000 calls above 5M
- Customer B usage: 30M calls/month
- Total monthly cost: $25K + ($0.01 × 25M) = $25K + $250K = $275K/month

Value Analysis:
- Customer pays: $275K/month
- Customer receives: $2.4M/month value
- Customer ROI: 8.7x return
- Vendor margin: ($275K - $1.5K cost) / $275K = 99.5% margin

Step 4: Validate Against Alternatives

Customer's Alternatives:
A) Build in-house data science team: $100K/month + 12-month build time
B) Hire consulting firm: $200K/month for ongoing analytics
C) Use DataFlow: $275K/month, immediate deployment

Customer Decision:
DataFlow at $275K/month is STILL best alternative (8.7x ROI, immediate value)
Vendor captured 11.5% of customer value ($275K / $2.4M)
Customer kept 88.5% of value → Strong incentive to buy
```

**Common Value-Based Pricing Mistakes:**

**Mistake 1: Pricing Below Value Capture Threshold**
```
Error: Pricing at cost-plus margin, ignoring customer value
DataFlow prices at $1,500/month for all customers (cost-plus)

Result:
- Small customers: Good deal (6.7x ROI) → Happy
- Large customers: Incredible deal (1,667x ROI) → Arbitrage opportunity
- Competitors notice large enterprises paying $1,500/month for $2.5M/month value
- Competitor enters at $50K/month (still 50x ROI for customer)
- Vendor loses all large customers, left with only small customers at low margins

Lesson: Leaving too much value on table invites competition and arbitrage
```

**Mistake 2: Pricing Above Willingness to Pay**
```
Error: Pricing based on vendor's desired margin, not customer value
DataFlow prices at $500K/month for Customer B

Customer B Analysis:
- DataFlow value: $2.4M/month
- DataFlow price: $500K/month (20.8% capture rate)
- Alternative (consulting): $200K/month

Customer Decision:
$500K DataFlow vs. $200K consulting → Choose consulting
Even though DataFlow provides more value, price exceeds next-best alternative

Result:
- Vendor loses deal despite superior product
- Priced above customer's willingness to pay (anchored to alternatives)

Lesson: Price must be below customer's next-best alternative, not just below value created
```

**Mistake 3: Ignoring Price Anchoring and Fairness Perceptions**
```
Error: Charging different prices to similar customers without justification
DataFlow charges Customer C (Enterprise A) $25K/month
DataFlow charges Customer D (Enterprise B, same size/usage) $250K/month (they discovered later)

Customer D Reaction:
- "We're paying 10x more than Customer C for identical service?!"
- Perceived unfairness, even if $250K price was still good ROI
- Demands most-favored customer (MFC) pricing match
- Threatens termination and reputational harm

Result:
- Vendor forced to reduce Customer D pricing to $25K/month (lose $225K/month revenue)
- OR lose Customer D entirely + negative reviews damage sales
- Long-term customer relationship destroyed by price discrimination perception

Lesson: Price differences must be justified by observable differences (features, usage, service level)
Create tiers with clear differentiation to justify price gaps
```

**Summary: Value-Based Pricing Decision Rules**

```
Pricing_Model_Selection:

IF customer value is HOMOGENEOUS across customers:
    → Fixed pricing (all customers get similar value)
    → Example: Small business accounting software (all users ~$500/month value)

IF customer value varies by OBSERVABLE PROXY (revenue, users, usage):
    → Tiered pricing based on proxy variable
    → Example: CRM priced per user (more users → more value)

IF customer value varies SIGNIFICANTLY by customer size/industry:
    → Good-better-best tiers with feature differentiation
    → Example: Basic, Professional, Enterprise plans with distinct features

IF customer value is HIGHLY VARIABLE and customer-specific:
    → Custom/negotiated pricing for large deals
    → Example: Enterprise sales with custom MSAs, bespoke features

General Formula:
Price = min(
    Customer_Value × Capture_Rate,
    Next_Best_Alternative_Cost,
    Fairness_Anchor_Price
)

Where:
    Capture_Rate: 5-40% depending on category maturity, competition, switching costs
    Next_Best_Alternative_Cost: Customer's second-best option cost
    Fairness_Anchor_Price: What similar customers pay (avoid discrimination perception)
```

---

### Application 3: Cash Flow Timing - Fixed vs. Arrears vs. Prepaid Structures

**The Working Capital Trap:**

**Example: SaaS Vendor Cash Flow Crisis**

```
SaaS Vendor: CloudApp (B2B project management software)
Pricing: $10K/month per enterprise customer
Cost Structure:
- Infrastructure: $2K/month per customer (hosting, compute, storage)
- Sales & Marketing: $50K CAC (customer acquisition cost)
- Support: $1K/month per customer
- Total cost per customer: $3K/month + $50K upfront CAC

Payment Terms (Initial Structure - Arrears):
Customer invoiced at end of each month, Net-30 payment terms
Actual payment timing: Typically 45-60 days from service delivery

Customer 1 Timeline:
- Month 0: Sign contract, begin service
- Month 1 (Day 30): Invoice sent for Month 0 service ($10K)
- Month 1 (Day 45-60): Payment received for Month 0 service

Vendor Cash Flow (Customer 1):
Month 0:
    - Revenue: $0 (no payment yet)
    - Costs: $50K CAC + $3K monthly = $53K
    - Cash flow: -$53K

Month 1:
    - Revenue: $0 (still waiting for Month 0 payment)
    - Costs: $3K monthly
    - Cash flow: -$3K

Month 2:
    - Revenue: $10K (Month 0 payment arrives at Day 45-60)
    - Costs: $3K monthly
    - Cash flow: +$7K
    - Cumulative: -$53K - $3K + $7K = -$49K

Breakeven Timeline:
Months 1-7: Cumulative costs $50K CAC + ($3K × 7 months) = $71K
Months 1-7: Revenue $10K × 7 months = $70K (arriving 45-60 days late each month)
Actual breakeven: ~Month 9-10 (accounting for payment delays)

Scaling Problem (10 New Customers in Quarter 1):
CAC cost: 10 × $50K = $500K upfront
Monthly costs: 10 × $3K = $30K/month
Revenue (Month 3): 10 × $10K = $100K/month BUT delayed 45-60 days

Q1 Cash Flow:
    - Costs: $500K CAC + $90K monthly (3 months) = $590K
    - Revenue: $0 (all payments delayed to Q2)
    - Cash burn: -$590K

Q2 Cash Flow:
    - Costs: $90K monthly (3 months) = $90K
    - Revenue: Q1 revenue arrives (~$200K with delays) + Q2 revenue delayed
    - Net: Barely positive, 3-month revenue delay creates crisis

Crisis Point:
Vendor runs out of cash in Q2 despite having profitable customers
Cannot pay infrastructure bills → Service outages → Customer churn
Death spiral: Cash flow crisis → Service degradation → More churn → Worsening cash flow
```

**Solution 1 - Annual Prepayment with Discount:**

```
CloudApp New Payment Structure:
Option A (Monthly): $10K/month, billed monthly in arrears, Net-30
Option B (Annual Prepay): $100K/year upfront (16.7% discount = $120K vs. $100K)

Customer Incentive:
Annual prepay saves $20K/year (16.7% discount)
Customer locks in pricing for 12 months

Vendor Cash Flow (10 Customers, Annual Prepay):
Q1:
    - Costs: $500K CAC + $90K monthly = $590K
    - Revenue: 10 × $100K annual prepay = $1,000K upfront
    - Cash flow: +$410K (vs. -$590K under monthly arrears)
    - Cash position: Strong surplus for growth

Economic Impact:
- Vendor accelerates 12 months of revenue to Day 1
- Eliminates 45-60 day payment delays
- Reduces churn risk (customer locked in for 12 months)
- Frees working capital for new customer acquisition

Cost of Discount:
- Revenue foregone: $20K/customer/year
- Value to vendor: Working capital access ($100K now vs. $120K over 12 months)
- NPV Analysis: $100K today > $120K over 12 months (considering time value + churn risk)
```

**Solution 2 - Milestone Prepayment for Custom Projects:**

```
CloudApp Enterprise Custom Implementation: $500K project

Old Structure (Invoice upon completion):
- Month 0-6: Development work ($500K cost)
- Month 6: Invoice customer $500K
- Month 7-8: Wait for payment (Net-30 + delays)
- Vendor cash flow: -$500K for 7-8 months, then +$500K recovery

New Structure (Milestone Prepayment):
- Milestone 1 (Month 0): Requirements + design complete → $100K prepaid
- Milestone 2 (Month 2): Core development complete → $150K prepaid
- Milestone 3 (Month 4): Integration + testing complete → $150K prepaid
- Milestone 4 (Month 6): Deployment + training complete → $100K prepaid

Vendor Cash Flow:
    - Month 0: +$100K revenue, -$100K cost = $0 cash flow
    - Month 2: +$150K revenue, -$150K cost = $0 cash flow
    - Month 4: +$150K revenue, -$150K cost = $0 cash flow
    - Month 6: +$100K revenue, -$100K cost = $0 cash flow
    - Cumulative: $0 cash burn (vs. -$500K under old structure)

Economic Benefit:
- Zero working capital requirement (revenue matches costs at each milestone)
- Customer shares risk (prepays for work not yet delivered)
- Vendor can scale without external financing
```

**Solution 3 - Usage-Based with Minimum Commitments:**

```
CloudApp Usage Pricing: $0.10 per API call

Problem with Pure Usage-Based:
- Customer usage varies: 50K-200K calls/month (unpredictable)
- Vendor revenue: $5K-$20K/month (volatile)
- Vendor cannot forecast cash flow or plan investments

Solution - Usage with Annual Minimum:
- Customer commits to $100K minimum spend over 12 months
- Prepays $100K upfront OR $25K quarterly
- Usage billed monthly at $0.10/call
- If annual usage < $100K, no refund (use-it-or-lose-it)
- If annual usage > $100K, customer pays overage monthly

Customer Incentive:
- Commitment at $100K provides better pricing vs. pay-as-you-go
- Budgeting certainty (capped at minimum unless usage spikes)

Vendor Cash Flow:
- Guaranteed $100K annual revenue per customer (locked in)
- Prepayment provides working capital
- Upside potential if usage exceeds $100K

Example Customer (Actual usage: $150K/year):
- Prepays $100K upfront (or $25K quarterly)
- Months 1-9: Uses $100K worth of API calls
- Months 10-12: Uses additional $50K worth (overage billed monthly)
- Total paid: $100K prepaid + $50K overage = $150K
- Vendor cash flow: $100K upfront + $50K incremental = Smooth cash flow
```

**Decision Framework: Payment Timing Structures**

```
Cash Flow Optimization Formula:

Vendor_Cash_Flow_Risk = (CAC + Monthly_Cost × Payment_Delay_Months) × New_Customers

Mitigation Strategy Selection:

IF Vendor_Cash_Flow_Risk > Available_Cash_Reserves:
    → REQUIRE prepayment (annual, quarterly, or milestone-based)
    → Offer discount to incentivize prepayment (10-20% for annual prepay)

IF Customer has strong credit AND low churn risk:
    → Accept monthly arrears (Net-30 or Net-60)
    → But monitor DSO (Days Sales Outstanding) closely

IF Project-based work with milestone deliverables:
    → Milestone prepayment (25-50% upfront, remainder at milestones)
    → Eliminates working capital risk entirely

IF Usage-based pricing with volatile revenue:
    → Minimum annual commitment (prepaid or quarterly)
    → Provides revenue floor while retaining usage-based upside

General Rule:
For early-stage/high-growth vendors:
    → Maximize prepayment to fund growth (offer discounts to incentivize)
    → Annual prepay discount: 10-20% (e.g., 12 months for price of 10)

For established vendors with strong cash position:
    → Flexible payment terms (monthly, quarterly, annual options)
    → Premium for monthly flexibility (e.g., month-to-month at +20% premium)
```

**Summary Table: Payment Timing Trade-offs**

| Payment Structure | Vendor Cash Flow | Customer Burden | Churn Risk | Best Use Case |
|-------------------|------------------|-----------------|------------|---------------|
| **Monthly Arrears (Net-30)** | Poor (45-60 day delay) | Low (pay as you go) | High (easy to cancel) | Established vendors, low CAC |
| **Monthly Prepay** | Good (no delay) | Medium (monthly commitment) | Medium (locked 30 days) | Subscription products |
| **Quarterly Prepay** | Very Good (90 days upfront) | Medium-High (quarterly lock-in) | Low (locked 90 days) | Growing SaaS vendors |
| **Annual Prepay** | Excellent (12 months upfront) | High (annual commitment) | Very Low (locked 12 months) | Early-stage SaaS, enterprise |
| **Milestone Prepay** | Excellent (matched to costs) | Low (pay for delivered work) | Low (value demonstrated) | Custom development |
| **Usage + Minimum** | Good (minimum guaranteed) | Medium (minimum commitment) | Low (committed annual spend) | Usage-based with volatility |

**Key Insight:**
Payment timing is a cash flow and risk management tool, not just a revenue collection mechanism.

Vendors with high CAC and long payback periods MUST structure prepayment to avoid cash flow death spiral.

Customers with strong credit and low churn risk can negotiate arrears terms (vendor's cost = working capital financing).

---

### Summary: Pricing Model Decision Framework

**Three-Dimensional Pricing Optimization:**

1. **Incentive Alignment** (How to structure payments to align interests)
   - Fixed fee → Milestone-based → Performance-based → Revenue share
   - Increasing alignment, increasing vendor risk/reward

2. **Value Capture** (How to price based on customer value, not vendor cost)
   - Cost-plus (low margin, leaves value on table)
   - Tiered pricing (segment by value proxy)
   - Custom negotiated (capture maximum value from large customers)

3. **Cash Flow Timing** (When to collect payment relative to cost incurrence)
   - Arrears (worst vendor cash flow, best customer flexibility)
   - Monthly prepay (balanced)
   - Annual prepay (best vendor cash flow, incentivized with discount)
   - Milestone prepay (matched to project costs)

**Integrated Decision Rules:**

```
Optimal Pricing Structure:

IF Customer_Relationship = Strategic Partner:
    Incentive: Revenue share or success fees
    Value: Custom negotiated based on customer-specific value
    Timing: Milestone or quarterly payments (shared risk)

IF Customer_Relationship = Recurring SaaS Subscription:
    Incentive: Service levels (performance-based SLA credits)
    Value: Tiered pricing by usage/seats/revenue proxy
    Timing: Annual prepay with discount (10-20% for cash flow optimization)

IF Customer_Relationship = One-Time Project:
    Incentive: Milestone-based payments (self-enforcing performance)
    Value: Fixed fee (if certain scope) or Time & Materials with cap (if uncertain)
    Timing: Milestone prepayment (25-50% upfront, remainder at milestones)

IF Customer_Relationship = Usage-Based Platform:
    Incentive: Pay-per-use (aligned with customer consumption)
    Value: Tiered pricing with volume discounts
    Timing: Monthly usage with annual minimum commitment (cash flow floor)
```

**Key Economic Principles:**

1. **Incentive Alignment > Pricing Level**
   - A lower price with aligned incentives creates more total value than a higher price with misaligned incentives
   - Example: $300K milestone pricing (self-enforcing) > $500K fixed fee (hold-up risk)

2. **Price to Value, Not Cost**
   - Customer value can vary 100x-1000x across customer segments for same product/service
   - Value-based pricing with tiered structure captures more surplus than cost-plus pricing
   - Example: $1,500/month for small business, $25,000/month for enterprise (same product, different value)

3. **Cash Flow Timing = Hidden Economic Lever**
   - Prepayment provides working capital for growth, reduces churn risk, eliminates payment delays
   - Discount for prepayment (10-20%) is worth cost if vendor has high CAC and working capital constraints
   - Example: $100K annual prepay (16.7% discount) > $120K over 12 months with 45-60 day delays

4. **Avoid Fixed Fee with Uncertain Outcomes**
   - Fixed fee creates adversarial relationship when scope or requirements are uncertain
   - Milestone, performance-based, or time & materials with cap are better for uncertain projects
   - Example: Custom software development → Milestone-based, not fixed fee

---

## When to Consult Experts

### Pricing Negotiation
- **Large Contracts**: >$500K annually (custom pricing, volume discounts, MFC clauses)
- **Usage-Based Pricing**: Uncapped consumption model (negotiate caps, overage rates, minimums)
- **Enterprise Agreements**: Multi-year commitments (price locks, annual increase caps, termination rights)

### Payment Disputes
- **Non-Payment**: Customer disputing charges (audit billing records, resolve dispute)
- **Failed Payments**: Vendor suspending service for late payment (cure period, reinstatement)
- **Overcharges**: Customer believes overbilled (audit, reconciliation, refund)

### Tax Issues
- **International Payments**: Cross-border withholding tax (gross-up analysis, treaty benefits)
- **Sales Tax Nexus**: Multi-state sales tax obligations (Wayfair economic nexus)
- **VAT Compliance**: EU VAT registration, reverse charge mechanism

### Pricing Models
- **New Business Model**: Designing pricing for new SaaS product (market research, competitive analysis)
- **Price Increase Communication**: Announcing price increase to customers (legal review, customer retention strategy)

## Cross-References

**Related Key Provisions** (tech_transactions):
- `service_levels.md` - SLA credits tied to pricing (service credits for downtime)
- `termination_provisions.md` - Refund upon termination (pro-rata refunds, prepaid fees)
- `liability_limitations.md` - Damages caps often tied to fees paid
- `international_tax.md` - Withholding tax, VAT, cross-border payment issues

**Contract Intelligence Skills** (from 4,900+ real contracts):
- `payment-terms-taxonomy.md` - Payment clause patterns from real contracts
- `payment-terms-examples.md` - Real payment language extracted from contracts
- `payment-terms-negotiation.md` - Strategic negotiation guidance with S1-S13 patterns

**Cognitive Patterns** (apply to payment/pricing analysis):
- `S5` - Business strategy implementation (pricing as strategic tool)
- `S10` - Systemic impact (pricing precedent for future deals)
- `S11` - Temporal factor integration (payment timing, escalation triggers)
- `BI4` - Negotiation capital allocation (when to push on pricing)
- `BI5` - Alternative solutions (creative pricing structures)

**Applies to All Transaction Types**:
- Software licensing, SaaS, strategic partnerships, data agreements all include payment and pricing provisions

## References

> ⚠️ **Synthetic Skill** - Not expert validated. Pricing terms are highly negotiated and vary by deal size, customer sophistication, and market segment. This skill provides general commercial principles but specific pricing structures require business, finance, and legal input. Always consult counsel for significant pricing commitments or disputes.

**Key Concepts**:
- Subscription vs. usage-based pricing
- Fixed vs. variable costs
- Annual price increases (CPI-linked, fixed cap)
- Sales tax nexus and VAT compliance
- Withholding tax gross-up
- Service credits for SLA breach

**Market Practices**:
- Annual prepayment discount: 10-20%
- Annual price increase cap: 3-5% or CPI
- Late payment interest: 1.5% per month (18% APR)
- Suspension for non-payment: 30 days past due (after 10-15 day notice)
