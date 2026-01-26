---
name: api-agreements
description: Api Agreements
tags:
  - api
  - integration
  - technical
version: '1.0'
confidence_level: MEDIUM
category: transaction_types
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
mentoring_priority: 3
validation_type: synthetic
source_type: expert_judgment
---

# API Agreements

```yaml
skill_id: api_agreements
domain: transaction_structures
sub_domains: [api_licensing, rate_limits, authentication, data_usage, webhooks]
transaction_types: [saas_licensing, data_agreements, strategic_partnerships]
confidence: 0.70
validation_status: synthetic_quick
requires: [software_licensing, data_agreements, service_levels]
complements: [payment_pricing, liability_limitations, ip_ownership_assignment]
skill_tier: foundational
mentoring_priority: 3
```

## Overview

API (Application Programming Interface) agreements govern access to and use of web-based APIs. Key provisions include:
- **Access rights and restrictions**: What can be done with the API?
- **Rate limiting and throttling**: Usage caps and performance limits
- **Authentication and security**: API keys, OAuth, security obligations
- **Data rights**: Ownership and use of data transmitted via API
- **Service levels**: Uptime, latency, support commitments
- **Pricing models**: Free tiers, usage-based, subscription

**Critical for**: SaaS integrations, platform partnerships, data exchanges, third-party developer programs

---

## Common API Agreement Structures

### Public API / Developer Agreement

**Free Tier with Upgrade Options**:
```
Stripe, Twilio, SendGrid model:
- Free tier: Limited calls/month (e.g., 1,000 requests)
- Paid tiers: Usage-based pricing ($0.01 per API call)
- Developer accepts "Terms of Service" (clickwrap)
- No negotiated SLA for free tier
- Enterprise tier: Custom SLA, dedicated support
```

**Key Characteristics**:
- Non-negotiable terms of service
- Automated signup (API key provisioning)
- Tiered pricing based on volume
- Public documentation
- Community support for free tier, paid support for premium

### Enterprise API Agreement

**Negotiated Terms for High-Volume Users**:
```
- Custom contract (not clickwrap TOS)
- Volume commitments and discounts
- Dedicated SLA (99.9%+ uptime)
- Higher rate limits or no rate limits
- Dedicated technical account manager
- Custom features or early access
- Master Services Agreement + API Addendum
```

### Partner API / Integration Agreement

**Strategic Partnership with Special Terms**:
```
Example: Salesforce AppExchange partner, Shopify App partner
- Application review and certification process
- Co-marketing rights and obligations
- Revenue sharing (platform takes 15-30% of app revenue)
- Brand usage guidelines
- Data sharing provisions
- Certification requirements and audits
- Termination for policy violations
```

---

## Core API Provisions

### 1. Grant of Access

**Standard License Grant**:
```
"Provider grants Customer a non-exclusive, non-transferable, revocable
license to access and use the API solely for Customer's internal business
purposes, subject to these Terms and the Documentation."
```

**Key Restrictions**:
```
Customer shall NOT:
(a) Exceed rate limits or attempt to circumvent usage restrictions
(b) Reverse engineer, decompile, or disassemble the API
(c) Use API to build competing service
(d) Resell or sublicense API access (unless authorized reseller)
(e) Use API for illegal purposes or to transmit malware
(f) Scrape, crawl, or harvest data beyond API's intended use
(g) Use API to spam or send unsolicited communications
```

### 2. Rate Limits and Throttling

**Rate Limiting Structure**:
```
Standard Tier:
- 100 requests per minute
- 10,000 requests per day
- 200,000 requests per month

Premium Tier:
- 1,000 requests per minute
- 100,000 requests per day
- 5,000,000 requests per month

Enterprise Tier:
- Custom rate limits or no limits
- Burst allowance for spikes
```

**Throttling Provisions**:
```
"If Customer exceeds rate limits:
(a) Provider may throttle requests (HTTP 429 'Too Many Requests')
(b) Provider may temporarily suspend API access
(c) Customer may purchase additional capacity
(d) Excessive overages may result in termination"
```

**Fair Use Policy**:
```
"Even if below stated rate limits, Provider may throttle requests that:
- Create disproportionate load on Provider's systems
- Exhibit unusual or abusive patterns
- Violate spirit of intended use per Documentation"
```

### 3. Authentication and Security

**API Key Management**:
```
"Customer shall:
(a) Keep API keys confidential and secure
(b) Not share API keys with third parties (except authorized contractors)
(c) Rotate keys regularly (at least annually)
(d) Immediately revoke compromised keys
(e) Use separate keys for development, staging, production
(f) Implement key management best practices (not hardcode in source)"
```

**OAuth 2.0 Provisions**:
```
For APIs using OAuth 2.0 for user authorization:
- Customer must obtain user consent for data access
- Customer shall not request broader scopes than needed
- Customer must respect token expiration and refresh properly
- Customer shall secure client secrets
```

**Security Obligations**:
```
"Customer shall:
(a) Use HTTPS/TLS for all API communications
(b) Validate SSL certificates
(c) Sanitize all inputs and outputs (prevent injection attacks)
(d) Implement industry-standard security practices
(e) Promptly notify Provider of security incidents or vulnerabilities"
```

### 4. Data Rights and Usage

**Data Ownership**:
```
"As between the parties:
(a) Customer retains ownership of Customer Data submitted via API
(b) Provider retains ownership of Provider Data returned by API
(c) Neither party acquires ownership of the other's data
(d) Provider may use aggregated, anonymized data for analytics"
```

**Data Usage Restrictions**:
```
Customer Use of Provider Data:
"Customer may use data returned by API solely for purposes stated in
Documentation. Customer shall NOT:
(a) Resell or redistribute Provider's data (unless authorized)
(b) Publicly display Provider data beyond scope of use case
(c) Combine Provider data with third-party data to re-identify individuals
(d) Cache Provider data beyond permitted retention period (e.g., 24 hours)
(e) Use data for purposes prohibited by Provider's Acceptable Use Policy"
```

**Provider Use of Customer Data**:
```
"Provider may use Customer Data only to:
(a) Provide and maintain the API Service
(b) Generate aggregated, de-identified analytics
(c) Comply with legal obligations
Provider shall NOT:
(a) Sell Customer Data to third parties
(b) Use Customer Data for Provider's own marketing (without consent)
(c) Disclose Customer Data except as required by law or authorized by Customer"
```

### 5. Service Levels

**Standard API SLA**:
```
"API Availability: 99.9% Monthly Uptime
 API Latency: 95th percentile ≤ 200ms
 Error Rate: ≤ 0.1% (5xx errors)

 Service Credits:
 - 99.0% to <99.9% uptime: 10% monthly fee credit
 - <99.0% uptime: 25% monthly fee credit

 Exclusions: Scheduled maintenance, DDoS attacks, Customer's infrastructure"
```

**Response Time SLAs**:
```
GET requests: ≤ 200ms (95th percentile)
POST requests: ≤ 500ms (95th percentile)
Batch operations: ≤ 10 seconds (95th percentile)
```

### 6. Versioning and Deprecation

**API Versioning**:
```
"Provider maintains API versions using semantic versioning (e.g., v1, v2).
- Major versions: Breaking changes (new endpoint path, e.g., /v2/)
- Minor versions: Backward-compatible additions (query parameters, new fields)
- Patches: Bug fixes and non-breaking changes"
```

**Deprecation Policy**:
```
"Provider may deprecate API versions with:
(a) Minimum 12 months notice before sunset
(b) Email notification to registered API users
(c) Changelog and migration guide published
(d) Old version remains functional during deprecation period
(e) After sunset, deprecated version may return errors or be removed"
```

**Backward Compatibility**:
```
"Provider will use commercially reasonable efforts to maintain backward
compatibility within major version. However, Provider may make breaking
changes if required for security or legal compliance with 90 days notice."
```

---

## Pricing Models

### Usage-Based Pricing

```
Per-Request Pricing:
- $0.01 per API call
- Volume discounts: >1M calls/month = $0.008 per call
- Overage charges: Exceeding plan = $0.015 per call

Per-Data Pricing:
- $0.10 per GB transferred
- Ingress (uploads) free, egress (downloads) charged
```

### Tiered Subscription

```
Starter: $50/month - 10,000 calls/month
Professional: $200/month - 100,000 calls/month
Enterprise: Custom - Unlimited calls + SLA
```

### Freemium Model

```
Free Tier:
- 1,000 calls/month
- Community support
- No SLA
- Rate limited to 10 req/min

Paid Tier:
- Unlimited calls (fair use)
- Email/phone support
- 99.9% SLA
- Rate limit 100 req/min
```

---

## Compliance and Acceptable Use

**Acceptable Use Policy**:
```
Customer shall NOT use API to:
(a) Violate laws or regulations
(b) Infringe third-party IP or privacy rights
(c) Transmit malware, spam, or abusive content
(d) Interfere with Provider's systems or other users
(e) Circumvent security or access controls
(f) Engage in fraudulent activity
(g) Violate export controls or sanctions
```

**Regulatory Compliance**:
```
GDPR/Privacy:
- If API processes personal data, DPA required
- Customer is data controller, Provider may be processor
- Provider must have appropriate safeguards (Article 28)

Industry-Specific:
- HIPAA: BAA required if PHI transmitted via API
- PCI DSS: If payment card data, must meet PCI requirements
- SOC 2: Provider may undergo SOC 2 audit for enterprise customers
```

---

## Intellectual Property

**API IP Ownership**:
```
"Provider retains all right, title, and interest in API, including:
(a) API code, architecture, algorithms
(b) Documentation and specifications
(c) Improvements and derivative works
(d) Provider's data and content returned by API

Customer retains ownership of:
(a) Customer's applications that use API
(b) Customer Data submitted to API
(c) Customer's integration code
```

**API Name and Trademark Usage**:
```
"Customer may identify integration with Provider's API, subject to:
(a) Provider's trademark guidelines
(b) Accuracy (e.g., 'Powered by [Provider API]')
(c) No endorsement implied without written consent
(d) Termination of right upon agreement termination"
```

---

## Termination and Suspension

**Termination Rights**:
```
Either Party: Terminate with 30 days notice (or per contract term)

Provider Immediate Termination:
- Customer material breach (exceeds rate limits, violates AUP)
- Customer poses security risk
- Required by law or court order
- End of life for API version (after deprecation period)

Customer Immediate Termination:
- Provider fails to meet SLA for 3 consecutive months
- Provider materially breaches contract
```

**Suspension**:
```
"Provider may immediately suspend API access if:
(a) Customer exceeds usage limits and refuses to upgrade
(b) Customer violates security or AUP provisions
(c) Customer's account in payment default
(d) Suspend required for emergency maintenance or security

Provider shall notify Customer promptly and allow cure within 10 business days."
```

**Effect of Termination**:
```
Upon termination:
(a) Customer's API access immediately revoked
(b) Customer must cease using Provider's data (unless retention permitted)
(c) Customer may retrieve Customer Data within 30 days (data export)
(d) Provider may delete Customer Data after 30 days
(e) Prepaid fees: Pro-rata refund if Provider terminates without cause
```

---

## Key Negotiation Points

**Customer Priorities**:
- Higher rate limits for planned use case
- Guaranteed SLA (99.9%+ uptime)
- Data portability and export rights
- Longer deprecation notice (18-24 months vs. 12 months)
- No automatic rate limit changes (must notify before reducing)
- Custom features or priority in roadmap

**Provider Priorities**:
- Broad termination rights for abuse or non-payment
- No liability for third-party data accessed via API
- Right to change rates/limits with notice
- Customer indemnity for misuse of API
- No exclusivity (customer can use competing APIs)

---

## Due Diligence Checklist

When entering API agreement:

**Technical Due Diligence**:
- [ ] Review API documentation completeness
- [ ] Test API reliability and performance
- [ ] Verify rate limits sufficient for use case
- [ ] Check versioning and deprecation policy
- [ ] Assess security standards (OAuth, TLS, etc.)
- [ ] Review webhook reliability (if applicable)

**Legal Due Diligence**:
- [ ] Data ownership and usage rights clear?
- [ ] SLA meets requirements?
- [ ] Termination provisions acceptable?
- [ ] IP indemnification scope
- [ ] Liability limitations reasonable?
- [ ] Privacy/GDPR compliance (DPA if needed)?

**Commercial Due Diligence**:
- [ ] Pricing model predictable for expected usage?
- [ ] Overage charges reasonable?
- [ ] Volume discounts available?
- [ ] Support tier adequate?
- [ ] Alternative providers available (avoid lock-in)?

---

## References and Validation

**CAUTION**: This is a quick-reference Skills file and has not been validated by legal experts.

**Confidence Level**: 0.6 (Synthetic Quick Version - Not Expert-Validated)

**For Expert Review**:
Kevin Keller should validate:
- [ ] Standard rate limiting structures and enforcement
- [ ] Data rights allocation (especially Provider data restrictions)
- [ ] SLA provisions for APIs vs. SaaS applications
- [ ] Deprecation notice periods (industry standard)
- [ ] OAuth vs. API key security obligations
- [ ] Liability for third-party data breaches via API

**Recommended Backfill**: Add specific examples from major API providers (Stripe, Twilio, Google Maps), webhook provisions, GraphQL-specific considerations, API gateway architectures.

---

## Cross-References

**Related Transaction Types** (tech_transactions):
- `saas_licensing_agreements.md` - SaaS + API combination
- `data_agreements.md` - Data transmitted via API
- `technology_licensing.md` - API as licensed technology

**Contract Intelligence Skills** (from 4,900+ real contracts):
- `api-agreement-expected-clauses.md` - Expected clauses for API agreements
- `service-levels-taxonomy.md` - API availability and performance SLAs
- `data-protection-taxonomy.md` - Data handling in API context
- `termination-taxonomy.md` - API deprecation and termination

**Key Provision Skills** (for specific clauses):
- `service_levels.md` - API SLA structure
- `liability_limitations.md` - API-specific liability caps
- `confidentiality_nda.md` - API key protection

**Cognitive Patterns** (apply to API analysis):
- `S3` - Multi-domain synthesis (technical API architecture + legal)
- `S6` - Dynamic framework (API versioning, deprecation)
- `S11` - Temporal factors (deprecation timelines, migration periods)
- `BI1` - Strategic value assessment (API as revenue channel vs. cost center)
- `BI3` - Resource constraints (API cost economics, rate limiting, overage charges)
- `BI5` - Alternative solutions (build vs. buy API, single provider vs. multi-vendor)
