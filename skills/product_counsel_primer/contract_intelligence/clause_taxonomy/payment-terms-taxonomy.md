---
name: payment-terms-taxonomy
description: >-
  Comprehensive taxonomy of payment terms including pricing structures,
  invoicing, late fees, taxes, and audit rights. Use when drafting,
  reviewing, or negotiating commercial payment provisions.
tags:
  - payment
  - pricing
  - invoicing
  - fees
  - taxes
version: '1.0'
confidence_level: HIGH
category: clause_taxonomy
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - termination-taxonomy
  - audit-rights-taxonomy
skill_tier: foundational
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 2
validation_type: human_validated
source_type: contract_samples
---

# Payment Terms Taxonomy

## Overview

Payment terms govern pricing, invoicing, and collection of fees in commercial agreements. These provisions are heavily negotiated and significantly impact cash flow and commercial viability. This taxonomy catalogs payment structures observed across commercial technology agreements.

## Pricing Structures

### A. One-Time/Perpetual Fees

```
Customer shall pay the one-time license fee of [AMOUNT] upon
execution of this Agreement.
```

**Use Cases**:
- Perpetual software licenses
- Implementation/setup fees
- Professional services (fixed price)
- Asset purchases

### B. Recurring/Subscription Fees

```
Customer shall pay the subscription fee of [AMOUNT] per [month/year],
payable in advance on the first day of each [billing period].
```

**Billing Frequencies**:
- Monthly (common for SaaS)
- Quarterly (mid-market)
- Annual (enterprise, discounted)
- Multi-year (strategic deals, significant discount)

**Advance vs. Arrears**:
- **In advance**: Payment before service period (vendor-favorable)
- **In arrears**: Payment after service period (customer-favorable)

### C. Usage-Based Pricing

```
Customer shall pay [AMOUNT] per [unit] processed/consumed during
each billing period. Vendor shall provide monthly usage reports.
```

**Usage Metrics**:
- API calls/transactions
- Data volume (GB/TB)
- Active users/seats
- Compute hours
- Messages/emails sent
- Storage consumed

**Variations**:
- Pure usage (pay for what you use)
- Committed minimum + overage
- Tiered pricing (unit cost decreases at volume)
- Hybrid (base subscription + usage)

### D. Tiered/Volume Pricing

```
Per-Unit Pricing:
- Units 1-1,000: [AMOUNT] per unit
- Units 1,001-10,000: [AMOUNT] per unit
- Units 10,001+: [AMOUNT] per unit
```

**Tier Types**:
- **Volume pricing**: All units at tier rate
- **Graduated pricing**: Each tier priced separately
- **Committed volume**: Discount for volume commitment

### E. Per-Seat/User Pricing

```
Customer shall pay [AMOUNT] per named user per month. The minimum
commitment is [X] users. Additional users may be added at any time
at the then-current per-user rate.
```

**User Types**:
- Named users (specific individuals)
- Concurrent users (simultaneous access limit)
- Active users (logged in during period)

### F. Time & Materials

```
Customer shall pay Provider at the following hourly rates:
- Senior Consultant: [AMOUNT]/hour
- Consultant: [AMOUNT]/hour
- Analyst: [AMOUNT]/hour

Provider shall invoice monthly for hours worked.
```

**Rate Protections**:
- Rate lock for term of agreement
- Annual increase cap (CPI, 3-5%)
- Most-favored-customer pricing

### G. Milestone-Based

```
Customer shall pay upon completion and acceptance of each milestone:
- Milestone 1 (Design): [AMOUNT] (Due: [DATE])
- Milestone 2 (Development): [AMOUNT] (Due: [DATE])
- Milestone 3 (Testing): [AMOUNT] (Due: [DATE])
- Milestone 4 (Deployment): [AMOUNT] (Due: [DATE])
```

## Invoicing Terms

### Invoice Requirements

```
All invoices shall include: (a) invoice date and number; (b) purchase
order number (if applicable); (c) description of products/services;
(d) quantity and unit price; (e) total amount due; (f) payment due
date; (g) remittance instructions.
```

### Invoice Timing

| Type | Typical Timing |
|------|----------------|
| Subscription (advance) | First of billing period |
| Subscription (arrears) | End of billing period |
| T&M | Monthly, 15th of following month |
| Milestone | Upon acceptance |
| One-time | Upon execution or delivery |

### Electronic Invoicing

```
Vendor shall submit invoices electronically to [system/email].
Paper invoices will not be processed.
```

## Payment Terms

### Net Payment Terms

```
Payment is due within [thirty (30)] days of the invoice date ("Net 30").
```

**Common Terms**:
- Net 15 (aggressive)
- Net 30 (standard)
- Net 45 (customer-favorable)
- Net 60 (large enterprise)
- Net 90 (government/public sector)

### Early Payment Discount

```
Customer may deduct [2%] from the invoice amount if payment is
received within [10] days of invoice date ("2/10 Net 30").
```

### Payment Methods

```
Customer shall pay by [ACH/wire transfer/credit card/check] to
the account specified on the invoice.
```

**Method Considerations**:
- Wire: Fast, fees may apply
- ACH: Lower fees, 2-3 day processing
- Credit card: Convenience, vendor pays processing fee (2-3%)
- Check: Slow, tracking difficulty

## Late Payment

### Late Payment Interest

```
Overdue amounts shall accrue interest at the rate of [1.5%] per
month (or [18%] per annum), or the maximum rate permitted by
applicable law, whichever is less.
```

**Rate Variations**:
- 1% per month (12% annually)
- 1.5% per month (18% annually)
- Prime + 2-5%
- Maximum legal rate

### Collection Costs

```
Customer shall reimburse Vendor for all costs of collection,
including reasonable attorneys' fees, incurred in collecting
overdue amounts.
```

### Suspension for Non-Payment

```
If any amount is more than [thirty (30)] days overdue, Vendor may,
upon [ten (10)] days written notice, suspend Services until all
overdue amounts are paid in full. Such suspension shall not
constitute a breach by Vendor.
```

### Disputed Invoices

```
If Customer disputes any invoice in good faith, Customer shall:
(a) pay all undisputed amounts when due; (b) provide written notice
of the dispute with reasonable detail within [15] days of invoice;
(c) work with Vendor in good faith to resolve the dispute.
Disputed amounts shall not accrue interest pending resolution.
```

## Taxes

### Tax Exclusion

```
All fees are exclusive of taxes. Customer shall pay all applicable
sales, use, VAT, GST, and other taxes, excluding taxes based on
Vendor's net income.
```

### Tax Exemption

```
If Customer is tax-exempt, Customer shall provide Vendor with a
valid tax exemption certificate. Vendor shall not charge taxes
on invoices issued after receipt of a valid certificate.
```

### Withholding Taxes

```
If Customer is required to withhold taxes from payments to Vendor,
Customer shall: (a) deduct such taxes from the payment; (b) pay
such taxes to the appropriate authority; (c) provide Vendor with
official tax receipts. Customer shall not gross up payments.
```

**Alternative (Gross-Up)**:
```
If withholding is required, Customer shall gross up payments such
that Vendor receives the full amount due after withholding.
```

## Price Adjustments

### Annual Price Increase

```
Upon renewal, Vendor may increase fees by up to [X%] or the
Consumer Price Index (CPI) increase, whichever is greater, upon
[60] days prior written notice.
```

**Cap Variations**:
- Fixed percentage (3-5%)
- CPI or fixed, whichever is greater
- CPI or fixed, whichever is less
- No increase for multi-year commitment

### Most Favored Customer

```
Vendor represents that the fees are no less favorable than those
offered to similarly situated customers for comparable products
and volumes. If Vendor offers more favorable terms, Customer may
elect to adopt such terms.
```

### Price Protection

```
Fees shall not increase during the Initial Term. Upon renewal,
fees shall not increase by more than [5%] per year.
```

## Audit Rights

### Usage Audit

```
Vendor may audit Customer's use of the Software no more than once
per [twelve (12)] month period upon [thirty (30)] days written
notice. Audits shall be conducted during normal business hours
and shall not unreasonably interfere with Customer's operations.
```

### Audit Cost Allocation

```
If an audit reveals underpayment of more than [5%] of amounts
due for the audited period, Customer shall pay: (a) the underpayment
plus applicable interest; and (b) Vendor's reasonable audit costs.
Otherwise, Vendor shall bear all audit costs.
```

### Self-Certification

```
Upon Vendor's request (no more than annually), Customer shall
certify in writing its compliance with the usage limits and
license terms of this Agreement.
```

## Refunds and Credits

### Pro-Rata Refund

```
If this Agreement is terminated by Customer for Vendor's uncured
material breach, Vendor shall refund pre-paid fees for the period
following the effective date of termination on a pro-rata basis.
```

### No Refund

```
All fees are non-refundable, except as expressly set forth herein.
Termination by Vendor for Customer's breach shall not entitle
Customer to any refund.
```

### Service Credits

```
If Vendor fails to meet the Service Level Commitment, Customer
shall receive a credit equal to [X%] of the monthly fee for each
[X%] of downtime below the SLA. Credits are Customer's sole remedy
and shall not exceed [X%] of monthly fees.
```

## Key Decision Points

1. **Pricing Model**: One-time, subscription, usage, or hybrid?
2. **Billing Frequency**: Monthly, quarterly, or annual?
3. **Advance vs. Arrears**: When is payment due relative to service?
4. **Payment Terms**: Net 30, 45, or 60?
5. **Late Payment Penalty**: Interest rate and collection costs?
6. **Tax Treatment**: Exclusive or inclusive? Withholding?
7. **Price Increases**: Annual cap and notice requirement?
8. **Audit Rights**: Frequency, cost allocation, threshold?
9. **Refund Policy**: Pro-rata, credits, or non-refundable?
10. **Dispute Process**: How are billing disputes handled?

## Common Pitfalls

1. **Unclear payment trigger**: When exactly is payment due?
2. **Missing tax provisions**: Disputes over tax responsibility
3. **No dispute process**: Payment held hostage over disputes
4. **Excessive late fees**: May be unenforceable as penalty
5. **No suspension right**: Vendor stuck providing unpaid services
6. **Unlimited audit rights**: Burdensome and disruptive
7. **Automatic price increases**: No cap or notice requirement
8. **No true-up mechanism**: Usage discrepancies unresolved

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[termination-taxonomy]] - Payment on termination
- [[audit-rights-taxonomy]] - Detailed audit provisions
- [[service-levels-taxonomy]] - SLA credits
- [[payment-terms-examples]] - Real payment language from contracts
- [[payment-terms-negotiation]] - Strategic negotiation guidance

**Related Key Provisions** (tech_transactions):
- [[payment_pricing.md]] - Conceptual treatment of payment terms

**Cognitive Patterns** (apply when analyzing payment terms):
- `S5` - Business strategy (pricing as strategic tool)
- `S10` - Systemic impact (pricing precedent for future deals)
- `S11` - Temporal factors (payment timing, escalation)
- `BI4` - Negotiation capital allocation (when to push on pricing)
- `BI5` - Alternative solutions (creative pricing structures)
