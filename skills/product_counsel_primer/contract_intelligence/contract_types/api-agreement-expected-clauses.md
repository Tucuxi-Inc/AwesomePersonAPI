---
name: api-agreement-expected-clauses
description: >-
  Expected clauses for API and developer agreements including access rights,
  rate limits, usage restrictions, data handling, and developer obligations.
  Use when drafting or reviewing API licensing and integration agreements.
tags:
  - api
  - developer
  - sdk
  - integration
  - platform
  - contract-type
version: '1.0'
confidence_level: HIGH
category: contract_types
validated_by: "Kevin Keller"
validated_date: '2024-12-01'
good_until_date: '2026-12-01'
cross_references:
  - saas-agreement-expected-clauses
  - data-protection-taxonomy
  - service-levels-taxonomy
skill_tier: applied
pattern_tier: 2
knowledge_domain: contract_intelligence
mentoring_priority: 3
validation_type: human_validated
source_type: contract_samples
---

# API/Developer Agreement - Expected Clauses

## Overview

API agreements govern access to and use of application programming interfaces, enabling third-party developers to integrate with platforms and services. They address authentication, usage limits, data handling, and acceptable use. This skill documents expected structure and provisions based on analysis of API and developer agreement samples.

## Agreement Types

| Type | Description | Typical Terms |
|------|-------------|---------------|
| **Free/Public API** | Open access, basic terms | Click-through, limited SLA |
| **Commercial API** | Paid access, enterprise features | Negotiated, SLA included |
| **Partner API** | Strategic integration partners | Custom terms, co-marketing |
| **Internal API** | Inter-company/affiliate use | Simplified, service-oriented |
| **SDK License** | Development toolkit | Distribution rights, attribution |

## Standard Structure

### Typical Section Order

1. Definitions
2. API Access and Credentials
3. License Grant
4. Usage Restrictions
5. Rate Limits and Quotas
6. Fees and Payment
7. Data Handling
8. Privacy and Security
9. Developer Obligations
10. Service Levels (if applicable)
11. Intellectual Property
12. Warranties and Disclaimers
13. Limitation of Liability
14. Term and Termination
15. General Provisions

## Required Clauses

### 1. Definitions

**Must Include**:
- [ ] API definition
- [ ] Developer Application definition
- [ ] End User definition
- [ ] API Data definition

**Example**:
```
DEFINITIONS

"API" means [Company's] application programming interfaces, including
associated tools, documentation, and sample code.

"Developer Application" means any software application developed by
Developer that accesses the API.

"API Data" means any data, content, or information retrieved through
the API.

"End User" means any person who uses the Developer Application.

"API Key" or "Credentials" means the unique authentication keys,
tokens, or credentials issued to Developer to access the API.
```

### 2. API Access and Credentials

**Must Include**:
- [ ] Registration requirements
- [ ] Credential security
- [ ] Authentication methods
- [ ] Access termination

**Example**:
```
API ACCESS

Registration. Developer shall register for API access by providing
accurate information and agreeing to these terms. Developer shall
maintain current registration information.

Credentials. Upon approval, [Company] will issue API Credentials.
Developer shall: (a) keep Credentials confidential and secure;
(b) not share Credentials with third parties; (c) immediately
notify [Company] of any unauthorized access or compromise;
(d) implement industry-standard security practices.

Authentication. Developer shall authenticate all API calls using
the provided Credentials. [Company] may require specific authentication
methods (OAuth 2.0, API keys, JWT) and may change methods with notice.

Credential Revocation. [Company] may revoke Credentials immediately
upon suspected misuse, security breach, or violation of these terms.
```

### 3. License Grant

**Basic License**:
```
LICENSE GRANT
Subject to these terms, [Company] grants Developer a limited,
non-exclusive, non-transferable, revocable license to:

(a) Access and use the API solely to develop, test, and operate
    Developer Applications;

(b) Display API Data within Developer Applications in accordance
    with the Documentation and these terms;

(c) Use the Documentation solely in connection with permitted
    API use.

This license does not include any right to sublicense, except
that Developer may permit End Users to use Developer Applications.
```

**SDK/Library License**:
```
SDK LICENSE
[Company] grants Developer a license to: (a) use the SDK internally
for development; (b) reproduce and distribute the Runtime Components
solely as embedded in Developer Applications; (c) modify Sample Code
for use in Developer Applications.

Developer shall include required notices and attributions per the
Documentation.
```

### 4. Usage Restrictions

```
RESTRICTIONS
Developer shall not:

(a) Access the API except through authorized means and in compliance
    with Documentation;

(b) Reverse engineer, decompile, or derive source code from the API;

(c) Circumvent or disable rate limits, authentication, or security
    features;

(d) Use the API to build a competing service or to replicate core
    [Company] functionality;

(e) Use the API for any unlawful purpose or in violation of any
    third-party rights;

(f) Share, sell, or transfer API access or Credentials to third parties;

(g) Cache, store, or aggregate API Data beyond permitted periods;

(h) Make API calls from a third-party service on Developer's behalf
    without authorization;

(i) Use automated means to access the API beyond approved rate limits;

(j) Remove or modify any proprietary notices in API responses.
```

### 5. Rate Limits and Quotas

```
RATE LIMITS

Limits. Developer's API access is subject to the rate limits and
quotas specified in the Documentation or Developer Dashboard:

[Example Tiers:]
- Free Tier: [1,000] requests per day; [10] requests per second
- Basic: [100,000] requests per day; [50] requests per second
- Professional: [1,000,000] requests per day; [100] requests per second
- Enterprise: Custom limits per agreement

Burst Allowance. Developer may exceed rate limits by up to [20%] for
brief periods, subject to overall daily/monthly quotas.

Overage Handling. Requests exceeding limits will be: [rejected with
HTTP 429 / queued and processed when capacity available / charged at
overage rates of $[X] per [1,000] requests].

Limit Changes. [Company] may adjust rate limits with [30] days notice.
Reductions shall not affect pre-paid commitments.
```

### 6. Fees and Payment

**Tiered Pricing**:
```
FEES

Subscription Fees:
- Free: $0 (subject to Free Tier limits)
- Basic: $[X] per month
- Professional: $[X] per month
- Enterprise: Custom pricing

Usage Fees: [X] cents per [1,000] requests after included quota.

Billing. Fees are billed [monthly in arrears / annually in advance].
Usage-based fees are calculated based on API call logs maintained
by [Company].

Payment Terms. Payment due within [30] days of invoice. Late payments
accrue interest at [1.5%] per month.
```

### 7. Data Handling

```
API DATA

Ownership. [Company] (or its licensors) retains all rights in API Data.
Developer acquires no ownership rights by accessing API Data.

Use Restrictions. Developer may use API Data only:
(a) To operate Developer Applications;
(b) In compliance with these terms and Documentation;
(c) In compliance with applicable laws including privacy laws;
(d) In accordance with [Company's] Privacy Policy.

Caching. Developer may cache API Data for up to [24 hours] unless
Documentation specifies otherwise. Developer shall implement cache
invalidation per Documentation.

Retention. Upon termination, Developer shall delete all API Data
within [30] days and certify deletion upon request.

No Scraping. Developer shall not use the API to harvest, scrape,
or aggregate data for purposes other than operating Developer
Applications.
```

### 8. Privacy and Security

```
PRIVACY

End User Privacy. If Developer collects End User data through
Developer Applications, Developer shall: (a) maintain a privacy
policy compliant with applicable laws; (b) obtain necessary consents;
(c) not use End User data beyond disclosed purposes.

Data Protection. Developer shall implement appropriate technical
and organizational measures to protect API Data and End User data,
including encryption in transit and at rest.

Data Processing. If Developer processes personal data on behalf of
[Company], the Data Processing Addendum (Exhibit [X]) applies.

Security Incidents. Developer shall notify [Company] within [24 hours]
of any security incident affecting API Data or Credentials.
```

### 9. Developer Obligations

```
DEVELOPER OBLIGATIONS

Application Quality. Developer shall ensure Developer Applications:
(a) function properly and do not interfere with the API;
(b) comply with applicable laws and platform policies;
(c) do not contain malware, spyware, or malicious code;
(d) provide clear privacy disclosures to End Users.

Support. Developer is solely responsible for End User support for
Developer Applications. [Company] does not provide support to End Users.

Compliance. Developer shall comply with all applicable laws, including
export controls, privacy laws, and industry regulations.

Branding. Developer shall comply with [Company's] brand guidelines
when referencing [Company] or the API. Developer shall not suggest
endorsement or affiliation beyond the actual relationship.
```

### 10. Service Levels (Commercial APIs)

```
SERVICE LEVELS

Availability. [Company] targets [99.5%] monthly API availability,
excluding scheduled maintenance and force majeure.

Latency. [Company] targets [95th percentile] response time of
[200ms] for standard API endpoints.

Measurement. Availability and latency are measured by [Company's]
monitoring systems. Developer Dashboard displays real-time metrics.

Remedies. If availability falls below [99%] in any month, Developer
may request a service credit of [10%] of that month's fees. Credits
capped at [30%] of monthly fees. Credits are Developer's sole remedy.

Exclusions. SLA excludes: (a) Developer Application issues;
(b) network issues beyond [Company's] control; (c) scheduled
maintenance with [24 hours] notice; (d) force majeure.
```

## Common Clauses

### 11. Documentation and Support

```
DOCUMENTATION
[Company] shall provide and maintain Documentation describing API
functionality, authentication, endpoints, and best practices.
Documentation is available at [URL].

DEVELOPER SUPPORT
Support for the API is provided through:
(a) Documentation and knowledge base (self-service)
(b) Developer forums (community support)
(c) Email support: [response time by tier]
(d) Dedicated support (Enterprise tier only)
```

### 12. Changes to API

```
API CHANGES

Versioning. [Company] shall maintain API versions and provide
[12 months] notice before deprecating any version.

Breaking Changes. [Company] shall provide [90 days] notice before
introducing breaking changes to supported versions.

Non-Breaking Changes. [Company] may introduce non-breaking changes
(new endpoints, additional response fields) without notice.

Migration. [Company] shall provide migration guides and reasonable
support for transitions between API versions.
```

### 13. Intellectual Property

```
INTELLECTUAL PROPERTY

[Company] IP. [Company] retains all rights in the API, Documentation,
and API Data. Nothing grants Developer any rights except the limited
licenses expressly stated.

Developer IP. Developer retains all rights in Developer Applications
(excluding [Company] materials). Developer grants [Company] a license
to use Developer Application names and logos for promotional purposes.

Feedback. Developer grants [Company] a perpetual, royalty-free license
to use any feedback, suggestions, or improvements Developer provides
regarding the API.
```

### 14. Termination

```
TERMINATION

By Developer. Developer may terminate by ceasing API use and deleting
Credentials.

By [Company]. [Company] may terminate or suspend access:
(a) Immediately for violation of these terms or misuse;
(b) Upon [30] days notice for any reason;
(c) Immediately if required by law or to protect security.

Effect. Upon termination: (a) all licenses terminate; (b) Developer
shall cease API use; (c) Developer shall delete API Data and
Credentials; (d) fees remain due for usage prior to termination.

Survival. Sections [X, Y, Z] survive termination.
```

## Optional Clauses

### 15. App Store/Marketplace

```
MARKETPLACE LISTING
Developer may apply to list Developer Application in [Company's]
Marketplace. Listing requires compliance with Marketplace Guidelines
and [Company] approval. [Company] may remove listings at any time.

Revenue Share. For paid listings, [Company] retains [30%] of
transaction fees; Developer receives [70%].
```

### 16. Beta/Preview APIs

```
BETA APIS
Beta or preview APIs are provided "as is" without SLA or support
commitment. [Company] may modify or discontinue beta APIs at any
time. Developer uses beta APIs at own risk.
```

## Red Flags - Missing Elements

| Missing Element | Risk Level | Implication |
|-----------------|------------|-------------|
| No rate limits | HIGH | System abuse possible |
| Unclear data use rights | HIGH | Legal exposure |
| No credential security | HIGH | Breach liability |
| Missing termination rights | MEDIUM | Trapped relationship |
| No API change notice | MEDIUM | Breaking integrations |
| Vague usage restrictions | MEDIUM | Unclear compliance |
| No version deprecation policy | MEDIUM | Sudden breaking changes |
| Missing privacy requirements | HIGH | Regulatory violations |

## Key Decision Points

1. **Access Model**: Free, paid, or hybrid?
2. **Rate Limits**: By tier, by endpoint, or custom?
3. **SLA**: Availability and latency commitments?
4. **Data Rights**: What can developers do with API Data?
5. **Caching**: Permitted duration and rules?
6. **Versioning**: Deprecation notice and support periods?
7. **Support Model**: Self-service, community, or dedicated?
8. **Competitive Use**: Can API build competing products?
9. **Security Requirements**: What must developers implement?
10. **Termination**: What triggers immediate suspension?

## Cross-References

**Related Clause Skills** (contract_intelligence):
- [[saas-agreement-expected-clauses]] - Related cloud/SaaS terms
- [[data-protection-taxonomy]] - API data privacy requirements
- [[data-protection-examples]] - Real data handling language
- [[service-levels-taxonomy]] - API availability and latency SLAs
- [[service-levels-examples]] - Real SLA language from contracts
- [[termination-taxonomy]] - Credential revocation and access termination
- [[limitation-of-liability-taxonomy]] - API liability caps
- [[ip-ownership-taxonomy]] - API and developer application IP

**Related Key Provisions** (tech_transactions):
- [[technology_licensing.md]] - API as licensed technology
- [[privacy_and_data_protection.md]] - API data handling
- [[service_levels.md]] - API availability commitments

**Related Transaction Types** (tech_transactions):
- [[saas_licensing_agreements.md]] - APIs in SaaS context
- [[platform_agreements.md]] - Developer platform relationships

**Cognitive Patterns** (apply when reviewing API agreements):
- `S3` - Multi-domain synthesis (technical + legal + business model)
- `S5` - Party dynamics (platform provider vs. developer)
- `S6` - Dynamic framework (API versioning and changes)
- `S8` - Scenario planning (rate limit changes, deprecation)
- `BI1` - Deal qualification (API tier selection)
- `BI3` - Context-aware risk (data exposure through APIs)
