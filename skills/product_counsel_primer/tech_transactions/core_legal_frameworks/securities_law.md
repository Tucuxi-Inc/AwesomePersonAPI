---
name: securities-law
description: Securities Law
tags:
  - disclosure
  - equity
  - securities-law
version: '1.0'
confidence_level: MEDIUM
category: core_legal_frameworks
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
pattern_tier: 2
mentoring_priority: 2
validation_type: synthetic
source_type: statutory
---

# Securities Law Fundamentals

> **⚠️ SYNTHETIC SKILL - NOT EXPERT VALIDATED**

## Metadata

```yaml
skill_id: securities_law
domain: legal_fundamentals
sub_domains: [securities_act_1933, exchange_act_1934, regulation_d, sar simple, public_offerings]
jurisdictions: [united_states]
confidence: 0.70
validation_status: synthetic
requires: [keller_patterns, contract_law]
complements: [strategic_partnerships, warranties_representations]
skill_tier: foundational
mentoring_priority: 2
```

## Core Principles

### What is a Security?

**Securities Act §2(a)(1) + Howey Test**:
A security includes any:
- Stock, bond, note, debenture
- Investment contract (Howey test - see below)
- Evidence of indebtedness

**Howey Test** (*SEC v. W.J. Howey Co.*, 1946):
An "investment contract" is a security if:
1. **Investment of Money**: Person invests money/value
2. **Common Enterprise**: Pooled funds or horizontal commonality
3. **Expectation of Profits**: Investor expects returns
4. **Solely from Efforts of Others**: Profits depend on promoter/third party, not investor's own efforts

**Why It Matters**: If instrument is a "security," must comply with securities laws (register offering or qualify for exemption, anti-fraud rules apply)

### Tech Transaction Implications

**Tokens/Cryptocurrency**: If token represents investment in enterprise (expectation of profit from developers' efforts) → likely security (SEC position)

**SAFEs/Convertible Notes**: Promissory notes converting to equity → securities (must comply with Regulation D or other exemption)

**Revenue Sharing Agreements**: If investor funds business expecting share of profits from others' efforts → may be security (fact-specific)

**Equity Compensation**: Stock options, RSUs to employees → securities (but exempt under Rule 701 if private company)

## Key Securities Laws

### 1. Securities Act of 1933 (Registration)

**Core Requirement**: Cannot offer/sell securities unless:
- **Registered with SEC** (IPO, public offering - expensive, burdensome), OR
- **Exempt from Registration** (Regulation D, Regulation CF, Regulation A, etc.)

**Typical Private Company**: Uses exemptions (not registered offerings)

**Key Exemptions**:

#### Regulation D (Private Placements)

**Rule 506(b)** (Most Common):
- **No $ Limit**: Can raise unlimited amount
- **Accredited Investors Only**: Primarily accredited investors (unlimited number)
- **Up to 35 Non-Accredited**: Can have up to 35 non-accredited sophisticated investors (rare in practice)
- **No General Solicitation**: Cannot advertise or publicly promote offering
- **Requirements**: File Form D with SEC within 15 days after first sale

**Rule 506(c)** (General Solicitation Allowed):
- **No $ Limit**: Unlimited
- **Accredited Investors Only**: Only accredited investors (must verify - cannot rely on self-certification)
- **General Solicitation OK**: Can advertise publicly (websites, conferences, social media)
- **Requirements**: File Form D, take reasonable steps to verify accredited status

**Accredited Investor Definition** (Reg D Rule 501):
- **Income**: Individual with income >$200K (or $300K joint) in each of last 2 years
- **Net Worth**: Individual/joint net worth >$1M (excluding primary residence)
- **Entity**: Entity with >$5M assets (or all equity owners are accredited)
- **Sophisticated**: Directors, executives, general partners of issuer
- **Licenses**: Individuals with Series 7, 65, or 82 licenses (added 2020)

**Rule 506(b) vs. 506(c) Choice**:
- **506(b)**: Standard for most startups (existing investors, referrals - no general solicitation)
- **506(c)**: Use if need to advertise (demo days, AngelList, etc.) - must verify accredited status (harder)

#### Regulation CF (Crowdfunding)

- **Limit**: Can raise up to $5M per 12-month period
- **Open to Everyone**: Non-accredited investors can participate (subject to investment limits)
- **Must Use Platform**: Offering through SEC-registered crowdfunding portal (e.g., Wefunder, Republic, StartEngine)
- **Disclosure**: Provide financial statements (reviewed or audited depending on amount raised)
- **Investment Limits for Non-Accredited**: Lesser of $2,500 or 5% of annual income/net worth (if income/net worth <$124K), or 10% of annual income/net worth (if ≥$124K), up to $124K max

**When Used**: Startups raising small amounts ($50K-$5M) from many small investors (community round, product pre-sales)

#### Regulation A (Mini-IPO)

**Tier 1**: Up to $20M per 12 months
- Requires SEC qualification, state blue sky compliance

**Tier 2**: Up to $75M per 12 months
- **Pre-empts State Review**: No state blue sky filing (federal only)
- **Ongoing Reporting**: Must file semi-annual and annual reports (similar to public company)
- **Investment Limits**: Non-accredited investors limited to 10% of income/net worth

**When Used**: Companies raising $20M-$75M without going fully public (expensive but less than IPO)

### 2. Securities Exchange Act of 1934 (Public Companies)

**Applicability**: If company has:
- **Registered Securities**: Completed IPO (listed on exchange), OR
- **>2,000 Shareholders + >$10M Assets**: Private company triggers registration (must file as public company)

**Requirements**:
- **Form 10-K**: Annual report (audited financials)
- **Form 10-Q**: Quarterly reports
- **Form 8-K**: Current reports (material events - M&A, executive changes, etc.)
- **Proxy Statements**: For shareholder votes
- **SOX Compliance**: Sarbanes-Oxley Act (internal controls, CEO/CFO certification, auditor independence)

**When Startups Must Consider**: If approaching 2,000 shareholders (stock option holders count) + $10M assets → may need to go public or reduce shareholders (buy back shares)

### 3. Rule 144 (Resale of Restricted Securities)

**Problem**: Securities acquired in private placement (Reg D) are "restricted securities" (cannot freely resell)

**Rule 144 Safe Harbor**: Can resell restricted securities if:
- **Holding Period**: Hold for 6 months (reporting company) or 1 year (non-reporting company)
- **Current Information**: Issuer is current in SEC reporting (if reporting company)
- **Volume Limits**: If affiliate (insider), resale limited to 1% of outstanding shares or average weekly trading volume (whichever greater) per 3-month period
- **Ordinary Brokerage**: Sale through normal brokerage (no solicitation)
- **File Form 144**: If selling >5,000 shares or >$50K

**Non-Affiliates**: After 1-year holding period (if non-reporting) or 6 months (if reporting), non-affiliates can resell freely (no volume limits, no Form 144)

## Anti-Fraud Provisions

### Rule 10b-5 (General Anti-Fraud)

**Prohibits**:
- Fraudulent statements or omissions of material facts in connection with purchase/sale of securities
- Applies to ALL securities transactions (registered or exempt, public or private)

**Elements**:
1. **Material Misrepresentation or Omission**: Statement is false or omits material fact
2. **In Connection with Purchase/Sale**: Related to securities transaction
3. **Scienter**: Intentional or reckless disregard for truth

**Private Right of Action**: Injured investors can sue for damages

**Example**: Startup CEO tells investors "We have $1M in revenue" (actually $100K) to induce investment → Rule 10b-5 violation (fraud)

### Section 12(a)(1) (Unregistered Offerings)

**Strict Liability**: If sell securities without registration or exemption, buyer can rescind (get money back) + interest

**No Scienter Required**: Even if unintentional failure to register → liability

**Remedy**: Rescission (buyer returns security, seller returns purchase price + interest)

**Example**: Company raises money under Reg D but fails to file Form D or exceeds limits → buyers can rescind

## Common Pitfalls in Tech Transactions

### 1. Accidentally Creating Securities

**SAFE/Convertible Note Offerings**:
- **Mistake**: Raising money from 50+ investors without Reg D compliance (no Form D filed, general solicitation without 506(c))
- **Risk**: Unregistered offering → rescission rights for all investors

**Token Sales (ICOs)**:
- **Mistake**: Selling utility tokens but marketing as investment ("buy now, price will increase as platform grows")
- **Howey Test**: If profits expected from others' efforts → security → unregistered offering
- **SEC Enforcement**: SEC brought 100+ ICO enforcement actions (2017-2020)

**Revenue Share Agreements**:
- **Mistake**: Investor funds business, gets % of future revenue (passive investment)
- **Risk**: May be investment contract (security) if investor not materially involved in business

### 2. General Solicitation Violations (Rule 506(b))

**Prohibition**: Cannot "offer" securities through advertising, public announcements, mass emails to strangers

**Common Violations**:
- Posting on company website "We're raising $2M Series A"
- Tweeting "Join our investor round"
- Demo day presenting to >100 unknown attendees (may be general solicitation depending on context)

**Safe Harbor**: Pre-existing relationship (know investors before offering) or limit to accredited investors you already know

**If Need to Advertise**: Use Rule 506(c) (verify accredited status)

### 3. Exceeding 2,000 Shareholders (Section 12(g))

**Trigger**: Private company with:
- >2,000 shareholders of record (or >500 non-accredited shareholders), AND
- >$10M assets

**Consequence**: Must register as public company (file 10-K, 10-Q, SOX compliance)

**Planning**: If approaching limit, consider:
- **Tender Offers**: Buy back shares from employees to reduce count
- **Hold Shares in Nominee**: Use single nominee entity to hold employee shares (counts as 1 shareholder, not 500)
- **Go Public**: If ready, IPO or direct listing

**Reform**: JOBS Act (2012) increased threshold from 500 to 2,000 (relief for late-stage startups)

### 4. Insider Trading (Rule 10b5-1)

**Prohibition**: Corporate insiders cannot trade on material non-public information (MNPI)

**Insider**: Officer, director, employee, or anyone with MNPI (includes lawyers, accountants, investors who receive info)

**MNPI**: Information that would affect stock price if public (e.g., upcoming acquisition, major customer win/loss, financial results before announcement)

**Safe Harbor (Rule 10b5-1 Plan)**:
- Establish pre-arranged trading plan (specify dates, amounts) when NOT in possession of MNPI
- Plan must be committed to (cannot cancel trades based on later MNPI)
- **Cooling-Off**: 90-day delay before first trade under plan

**Penalties**: SEC enforcement (disgorgement, civil penalties), criminal prosecution (DOJ)

## International Securities Law

**US Extraterritorial Reach**:
- US securities laws apply if:
  - Conduct occurred in US (even if foreign issuer), OR
  - Domestic effect (US investors harmed, transactions on US exchanges)

**Foreign Private Issuers (FPIs)**:
- Foreign companies with <50% US shareholders or <US business operations
- **Advantages**: Exempt from some US rules (proxy rules, SOX 404(b), Section 16), can use home country GAAP

**Regulation S**:
- **Exemption**: Offshore offerings to non-US persons (no registration if no directed selling efforts in US)
- **Restrictions**: Cannot offer to US persons, cannot use US jurisdictional means (US wires, US mails)

## Risk Assessment & Compliance

### High-Risk Red Flags

- ⚠️ Raising capital without securities counsel review (may be unregistered offering)
- ⚠️ General solicitation (website, social media) for Reg D 506(b) offering
- ⚠️ Marketing tokens as investments without securities compliance
- ⚠️ Approaching 2,000 shareholders without public company readiness
- ⚠️ Insiders trading on MNPI (no 10b5-1 plan)

### Compliance Best Practices

- ✅ Engage securities counsel for all capital raises (even small amounts)
- ✅ File Form D within 15 days of first sale (Reg D)
- ✅ Maintain accredited investor verification records (for 506(c) or audit)
- ✅ Implement insider trading policy (lockup periods, 10b5-1 plans)
- ✅ Track shareholder count (avoid Section 12(g) surprise registration)

## When to Consult Experts

- **Any Capital Raise**: Even "simple" SAFE or convertible note (must ensure exemption applies)
- **Token/Cryptocurrency**: Before launching (SEC scrutiny intense, many enforcement actions)
- **Going Public**: IPO, direct listing, SPAC (requires specialized counsel)
- **SEC Investigation**: Received subpoena or Wells notice (immediate securities litigation counsel)
- **M&A**: Acquiring company with securities law issues (due diligence critical)

## References

> ⚠️ **Synthetic Skill** - Not expert validated. Securities law is highly technical with severe penalties for violations (rescission rights, SEC enforcement, criminal prosecution). Always consult securities counsel before offering securities.

**Key Statutes**: Securities Act of 1933, Securities Exchange Act of 1934, JOBS Act (2012), Regulation D, Regulation CF, Regulation A

**Cross-Reference**: `contract_law.md` (investment agreements), `warranties_representations.md` (disclosure obligations)
