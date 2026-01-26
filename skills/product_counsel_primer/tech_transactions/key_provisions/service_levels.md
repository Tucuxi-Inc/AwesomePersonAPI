---
name: service-levels
description: Service Levels
tags:
  - performance
  - service-levels
  - sla
version: '1.0'
confidence_level: MEDIUM
category: key_provisions
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
mentoring_priority: 2
validation_type: synthetic
source_type: expert_judgment
---

# Service Levels (SLA Provisions)

```yaml
skill_id: service_levels
domain: contract_provisions
sub_domains: [sla, uptime, performance_metrics, service_credits, support_levels]
transaction_types: [saas_licensing, cloud_services, managed_services, hosting_agreements]
confidence: 0.70
validation_status: synthetic
requires: [contract_law, liability_limitations, termination_provisions]
complements: [warranties_representations, payment_pricing, force_majeure]
skill_tier: foundational
mentoring_priority: 2
```

## Overview

Service Level Agreements (SLAs) define measurable performance commitments in technology services contracts. They establish:
- **Quantified service standards** (uptime, latency, response times)
- **Measurement methodologies** (monitoring, calculation periods)
- **Consequences for failure** (service credits, termination rights)
- **Exclusions from SLA** (force majeure, customer-caused issues)

**Critical for**: SaaS, cloud infrastructure, managed services, hosting, API services

**Why It Matters**: SLAs allocate performance risk between vendor and customer. Strong SLAs provide meaningful remedies for service failures; weak SLAs offer only token credits with numerous exclusions.

---

## Core SLA Components

### 1. Uptime Commitments

**Standard Uptime Tiers:**

```
99.0% Uptime ("Two Nines"):
- Downtime: 7.2 hours/month, 3.65 days/year
- Use: Basic web hosting, non-critical applications

99.9% Uptime ("Three Nines"):
- Downtime: 43.2 minutes/month, 8.76 hours/year
- Use: Standard SaaS, business applications
- Industry norm for most commercial SaaS

99.95% Uptime ("Three and a Half Nines"):
- Downtime: 21.6 minutes/month, 4.38 hours/year
- Use: Mission-critical business systems

99.99% Uptime ("Four Nines"):
- Downtime: 4.32 minutes/month, 52.56 minutes/year
- Use: High-availability systems, financial services

99.999% Uptime ("Five Nines"):
- Downtime: 26 seconds/month, 5.26 minutes/year
- Use: Critical infrastructure, telecom, payment processing
```

**Sample Provision:**

```
"Vendor commits to 99.9% Monthly Uptime for the Service, measured as:

Uptime % = (Total Minutes in Month - Downtime Minutes) / Total Minutes in Month

'Downtime' means Service is unavailable and returns error to properly
configured requests, excluding Scheduled Maintenance and Excused Downtime."
```

**Key Variables:**
- **Measurement Period**: Monthly (most common), quarterly, annual
- **Scheduled Maintenance**: Typically excluded if during maintenance window (e.g., Sunday 2-6am PT)
- **Partial Outages**: Some SLAs count partial degradation proportionally

### 2. Performance Metrics

**Common Performance SLAs:**

#### Response Time / Latency
```
"95th Percentile Response Time ≤ 200ms:
- 95% of API requests return response within 200 milliseconds
- Measured over monthly period
- Excludes network latency outside Vendor's infrastructure"
```

**Percentile Approach** (industry best practice):
- 50th percentile (median): Half of requests faster
- 95th percentile: 95% of requests faster (excludes outliers)
- 99th percentile: Very strict, 99% of requests faster

**Why Percentiles Matter**: Average response time masks outliers. A service with 100ms average might have 10% of requests taking 5+ seconds.

#### Throughput / Capacity
```
"Platform shall process minimum 10,000 transactions per second (TPS)
with ≤1% error rate during peak hours."
```

#### Error Rates
```
"Error Rate ≤ 0.1% monthly:
- Errors = HTTP 500/502/503/504 responses
- Calculated as: (Error Responses / Total Requests) × 100
- Excludes errors caused by Customer code or invalid requests"
```

#### Data Processing SLAs
```
"Batch Processing: 95% of batch jobs complete within 4 hours of submission.
Real-Time Processing: 99% of events processed within 30 seconds of receipt."
```

### 3. Support Response Times

**Tiered Support SLA Structure:**

```
Severity 1 (Critical - Service Down):
- Initial Response: 1 hour
- Status Updates: Every 2 hours
- Restoration Target: 4 hours

Severity 2 (Major - Significant Impact):
- Initial Response: 4 business hours
- Status Updates: Daily
- Resolution Target: 24 hours

Severity 3 (Minor - Limited Impact):
- Initial Response: 1 business day
- Resolution Target: 5 business days

Severity 4 (General Inquiry):
- Initial Response: 2 business days
- Resolution: Reasonable efforts
```

**Key Definitions:**
- **Initial Response**: Vendor acknowledges ticket (not resolution)
- **Business Hours**: Often 9am-5pm PT, Monday-Friday (excluding holidays)
- **24/7 Support**: Premium tier, typically for Severity 1 only
- **Resolution vs. Workaround**: Some SLAs distinguish between full resolution and temporary workaround

**Sample Provision:**

```
"Support Response Times (measured from Customer's support ticket submission):

| Severity | Definition | Response Time | Availability |
|----------|-----------|---------------|--------------|
| Critical | Production down | 1 hour | 24/7 |
| High | Major feature unavailable | 4 hours | Business Hours |
| Medium | Minor feature issue | 8 hours | Business Hours |
| Low | General question | 2 business days | Business Hours |

'Response Time' means Vendor's initial acknowledgment and assignment to support engineer.
'Business Hours' means 6am-6pm Pacific Time, Monday-Friday excluding US holidays."
```

### 4. Service Credits

**Standard Service Credit Structure:**

```
"Monthly Uptime Service Credits:

| Monthly Uptime % | Service Credit |
|-----------------|----------------|
| < 99.9% to ≥ 99.0% | 10% of monthly fees |
| < 99.0% to ≥ 95.0% | 25% of monthly fees |
| < 95.0% | 50% of monthly fees |

Maximum Service Credits: 50% of fees paid for affected month.

Claiming Process:
- Customer must submit claim within 30 days of month end
- Vendor verifies claim within 15 days
- Credit applied to next month's invoice (no cash refunds)"
```

**Key Credit Provisions:**

#### Credit Calculation Methods
```
1. Tiered (Most Common):
   - Discrete tiers based on performance level
   - Example: 99.5% uptime → 10% credit, 98% uptime → 25% credit

2. Sliding Scale:
   - Proportional credit based on exact performance
   - Example: Credit = (Committed % - Actual %) × 10 × Monthly Fee
   - 99.9% commitment, 99.5% actual → 0.4% × 10 = 4% credit

3. Per-Incident:
   - Fixed credit per SLA breach
   - Example: $500 credit per Severity 1 incident exceeding 4-hour target
```

#### Credit Caps
```
"Aggregate service credits shall not exceed 100% of fees paid in
the 12-month period preceding the claim."

OR

"Service credits are Customer's sole and exclusive remedy for
SLA failures (except termination rights)."
```

**Negotiation Points:**
- **Higher caps**: Customer wants credits >50% monthly fees
- **Cash refunds**: Customer wants cash option, not just future credits
- **Cumulative credits**: Allow credits to accumulate month-over-month
- **Automatic credits**: Apply without requiring customer claim

### 5. Measurement and Monitoring

**Monitoring Provisions:**

```
"SLA Measurement:
1. Vendor monitors Service availability using distributed monitoring from
   5+ geographic locations
2. Downtime recorded if ≥3 monitoring locations report unavailability
3. Customer may request monitoring data within 30 days
4. Monthly SLA reports provided by 10th day of following month"
```

**Third-Party Monitoring:**

```
"Customer may use third-party monitoring service (e.g., Pingdom, New Relic)
to verify Vendor's SLA reporting. If discrepancy >0.5% uptime, parties will
meet and confer to reconcile measurement methodologies."
```

**Reporting Requirements:**
- **Real-time status page**: Public dashboard showing current service status
- **Monthly SLA reports**: Automated delivery of performance metrics
- **Incident post-mortems**: Detailed analysis of major outages
- **Trend reporting**: Quarterly performance trends

### 6. Exclusions from SLA

**Standard SLA Exclusions:**

```
"Uptime Commitment excludes downtime caused by:

A. Scheduled Maintenance:
   - Performed during Maintenance Window (Sunday 2am-6am Pacific)
   - Emergency maintenance with 24-hour notice (max 4 hours/month)

B. Force Majeure Events:
   - See Force Majeure clause

C. Customer-Caused Issues:
   - Customer's applications, content, or configurations
   - Customer's network, internet connectivity, or infrastructure
   - Exceeding allocated usage limits or rate limits
   - Denial-of-service attacks targeting Customer

D. Third-Party Services:
   - Failures of third-party APIs, services, or infrastructure
   - Internet backbone or DNS infrastructure failures

E. Alpha/Beta Features:
   - Features designated as alpha, beta, preview, or experimental

F. Suspension for Non-Payment:
   - Service suspension due to Customer payment default"
```

**Key Negotiation Points:**

#### Scheduled Maintenance Windows
```
Vendor-Friendly: "Vendor may perform maintenance at any time with 48-hour notice."
Balanced: "Maintenance during designated window (Sunday 2-6am PT) with 7-day notice."
Customer-Friendly: "Max 4 hours/month scheduled maintenance, min 14-day notice,
                    Customer may reschedule once per quarter."
```

#### Emergency Maintenance
```
Vendor-Friendly: "Unlimited emergency maintenance with reasonable notice."
Balanced: "Max 4 hours/month emergency maintenance with 4-hour notice."
Customer-Friendly: "Emergency maintenance counts toward uptime SLA unless
                    genuine security emergency."
```

#### Third-Party Dependencies
```
Issue: Vendor's service depends on AWS, but AWS outage causes downtime.

Vendor Position: "We don't control AWS, should be excluded from SLA."
Customer Position: "You chose AWS, architectural decisions are your risk."

Common Resolution: Tiered SLA
  - "Platform Uptime: 99.9% (includes infrastructure dependencies)"
  - "Application Uptime: 99.95% (excludes third-party infrastructure failures)"
```

---

## SLA Structures by Service Type

### SaaS Application SLA

```
"SERVICE LEVEL AGREEMENT

1. Availability Commitment: 99.9% Monthly Uptime

2. Performance Commitments:
   - Page Load Time: ≤2 seconds (95th percentile)
   - API Response Time: ≤200ms (95th percentile)

3. Support Response Times:
   - Critical (Service Down): 1 hour, 24/7
   - High (Major Feature): 4 hours, Business Hours
   - Medium (Minor Issue): 1 business day
   - Low (Question): 2 business days

4. Service Credits:
   - 99.0% to <99.9%: 10% monthly fee credit
   - 95.0% to <99.0%: 25% monthly fee credit
   - <95.0%: 50% monthly fee credit
   - Maximum: 50% of monthly fees

5. Measurement:
   - Monthly measurement period
   - Excludes Scheduled Maintenance (Sunday 2-6am PT, max 4 hours/month)
   - Customer must claim credits within 30 days of month end

6. Termination Right:
   - If Uptime <99.0% for 3 consecutive months, Customer may terminate
     for cause with full refund of prepaid fees"
```

### Infrastructure/Cloud SLA

```
"INFRASTRUCTURE SLA

1. Compute Availability: 99.99% Monthly Uptime
   - Measured per virtual machine instance
   - Customer must deploy instances across multiple availability zones for SLA

2. Storage Durability: 99.999999999% (11 nines) annual durability
   - Data loss <0.000000001% per year

3. Network Connectivity: 99.9% Monthly Uptime
   - Measured at network edge, excludes customer's internet connection

4. Service Credits (per affected service):
   | Uptime % | Credit |
   |----------|--------|
   | <99.99% to ≥99.0% | 10% |
   | <99.0% to ≥95.0% | 25% |
   | <95.0% | 100% |

5. Claim Process: Submit support ticket within 30 days with:
   - Dates/times of unavailability
   - Affected resources (instance IDs, regions)
   - Customer's monitoring logs (if applicable)"
```

### API Service SLA

```
"API SERVICE LEVEL AGREEMENT

1. Availability: 99.95% Monthly Uptime (per API endpoint)

2. Performance:
   - Latency: ≤100ms (99th percentile) for requests <1KB
   - Throughput: Minimum 1,000 requests/second per customer

3. Rate Limits:
   - Standard Tier: 100 requests/minute
   - Premium Tier: 1,000 requests/minute
   - Enterprise Tier: Custom (no hard limit)
   - Rate limit errors (429) do not count toward availability SLA

4. Error Rate: ≤0.1% (5xx errors / total requests)

5. Service Credits:
   - Availability <99.95%: 5% credit per 0.1% below commitment
   - Latency >150ms (99th percentile): 10% credit
   - Error Rate >0.1%: 10% credit
   - Credits cumulative (max 50% monthly fee)

6. Monitoring: Real-time status page at status.vendor.com
   - Current system status
   - 90-day uptime history
   - Scheduled maintenance calendar"
```

### Managed Services SLA

```
"MANAGED SERVICES AGREEMENT

1. Infrastructure Monitoring: 24/7/365
   - Alert response: ≤15 minutes
   - Issue triage: ≤30 minutes

2. Incident Response:
   - Critical (P1): 30-minute response, 4-hour restoration target
   - High (P2): 2-hour response, 24-hour restoration target
   - Medium (P3): 8-hour response, 5-day resolution target

3. Change Management:
   - Standard changes: Implemented within 5 business days
   - Emergency changes: Implemented within 4 hours (if approved)

4. Patch Management:
   - Security patches: Within 72 hours of vendor release
   - Critical security patches: Within 24 hours

5. Backup/Recovery:
   - Daily backups with 30-day retention
   - Recovery Time Objective (RTO): 4 hours
   - Recovery Point Objective (RPO): 24 hours
   - Quarterly backup restoration tests

6. Reporting:
   - Monthly service reports by 10th of month
   - Quarterly business reviews"
```

---

## Advanced SLA Concepts

### Multi-Tier SLAs

**Tiered Service Levels by Plan:**

```
| Metric | Basic | Professional | Enterprise |
|--------|-------|--------------|------------|
| Uptime | 99.5% | 99.9% | 99.95% |
| Support Response | 8 hrs | 2 hrs | 30 min |
| Support Hours | Bus. Hrs | Extended | 24/7 |
| Service Credits | 10% max | 25% max | 50% max |
| Dedicated Support | No | No | Yes |
| Custom SLA | No | No | Available |
```

### Composite SLAs

**Calculating Overall SLA When Service Depends on Multiple Components:**

```
Example: SaaS application depends on:
- Application servers (99.95% SLA)
- Database (99.99% SLA)
- CDN (99.9% SLA)

Composite SLA (if serial dependencies):
= 0.9995 × 0.9999 × 0.999
= 0.9984
= 99.84% overall SLA

Note: Actual calculation depends on redundancy architecture.
With proper redundancy, composite can exceed individual component SLAs.
```

### Regional SLAs

```
"Service availability measured per geographic region:

- US East: 99.95% monthly uptime
- US West: 99.95% monthly uptime
- EU (Frankfurt): 99.95% monthly uptime
- Asia Pacific (Singapore): 99.9% monthly uptime

Customer must deploy across multiple regions for global availability.
SLA applies per region; multi-region deployments are Customer's responsibility."
```

### Degraded Performance SLAs

```
"Partial Service Availability:

Full Downtime: Service completely unavailable (0% availability)
Degraded Performance: Service available but below performance SLA

If performance degrades below SLA thresholds:
- Latency >500ms (vs. 200ms commitment): Counts as 50% downtime
- Error rate >1% (vs. 0.1% commitment): Counts as proportional downtime
- Throughput <50% of commitment: Counts as 50% downtime

Example: If service available all month but 95th percentile latency
         600ms for 10 hours:
         Effective downtime = 10 hours × 50% = 5 hours"
```

---

## SLA Remedies Beyond Credits

### Termination Rights

```
"Material SLA Breach Termination:

If any of the following occurs, Customer may terminate Agreement
for cause with 30 days' notice and receive pro-rata refund:

A. Monthly Uptime <99.0% for 3 consecutive months
B. Monthly Uptime <95.0% in any single month
C. Critical (P1) support response >4 hours on 3+ occasions in 6-month period
D. Vendor fails to pay earned service credits within 60 days of claim

Vendor has 30-day cure period to remediate and prevent future breaches."
```

### Enhanced Support

```
"If Monthly Uptime <99.0% for 2 consecutive months, Customer
entitled to:
- Dedicated technical account manager
- Weekly service review meetings
- Root cause analysis of all outages
- Remediation plan with milestones
- Priority feature requests related to stability improvements"
```

### SLA Review and Adjustment

```
"Annual SLA Review:

If Vendor achieves >99.99% uptime for 12 consecutive months:
- Parties will negotiate uptime commitment increase
- Enhanced SLA tier may be offered

If Vendor fails to meet SLA >6 months in any 12-month period:
- Parties will meet to discuss architectural improvements
- Customer may request independent technical audit
- Vendor shall implement remediation plan"
```

---

## Risk Assessment Framework

### High-Risk SLA Issues (Require Negotiation)

1. **No Meaningful Uptime Commitment**
   - "Best efforts" or "commercially reasonable" uptime
   - Uptime commitment <99.0% for critical business applications
   - No measurement methodology specified

2. **Service Credits Sole Remedy**
   - "Service credits are Customer's sole and exclusive remedy"
   - No termination right for material SLA breaches
   - Prevents consequential damages AND prevents termination

3. **Excessive Exclusions**
   - Unlimited scheduled maintenance
   - Third-party dependencies broadly excluded
   - Customer-caused issues not clearly defined
   - Alpha/beta features undefined (could exclude core functionality)

4. **Unilateral SLA Changes**
   - "Vendor may modify SLA at any time with notice"
   - No requirement that changes be materially beneficial or neutral

5. **Difficult Credit Claim Process**
   - Must claim within 7-14 days (too short for monthly calculation)
   - Requires extensive documentation burden
   - Credits expire if not used within 90 days

6. **Measurement Disputes**
   - Vendor's monitoring is "sole evidence" of uptime
   - No third-party monitoring allowed
   - No audit rights for SLA calculations

### Medium-Risk Issues (Assess Based on Use Case)

1. **Monthly vs. Annual Measurement**
   - Monthly: More granular, better for customer (1 bad month = credits)
   - Annual: Vendor-friendly (bad months averaged out)
   - Quarterly: Middle ground

2. **Support Response vs. Resolution**
   - Response time only (vendor acknowledges ticket) vs.
   - Resolution time (vendor actually fixes issue)
   - Most SLAs use response time (easier to measure)

3. **Business Hours Support for Critical Systems**
   - If customer needs 24/7 support, business hours SLA inadequate
   - Verify support hours match operational requirements

4. **Percentage-Based Credits (Lower Tiers)**
   - 10% credit for 99.0-99.9% uptime may be inadequate
   - Customer impact may far exceed credit value

5. **Scheduled Maintenance Windows**
   - Assess whether window aligns with customer's low-traffic periods
   - Verify maximum monthly maintenance hours

### Lower-Risk Issues (Standard Commercial Terms)

1. **99.9% Uptime for Standard SaaS**
   - Industry standard for non-critical business applications
   - 43 minutes/month downtime acceptable for most use cases

2. **Service Credits as Primary Remedy**
   - Standard for SaaS/cloud services
   - With termination right for material breaches

3. **Force Majeure Exclusions**
   - Standard to exclude force majeure events
   - See force_majeure.md for details

4. **Alpha/Beta Feature Exclusions**
   - Reasonable to exclude pre-release features
   - Ensure clearly labeled and optional

---

## Validation Questions

When reviewing SLA provisions, verify:

### Uptime and Performance

- [ ] What is the uptime commitment percentage? (99.9% is standard)
- [ ] How is uptime measured (monthly, quarterly, annually)?
- [ ] Are there performance SLAs beyond availability (latency, throughput)?
- [ ] What monitoring methodology is used?
- [ ] Is customer allowed third-party monitoring for verification?

### Service Credits

- [ ] What service credits are provided for SLA failures?
- [ ] Is there a cap on monthly/annual service credits?
- [ ] How are credits calculated (tiered, sliding scale)?
- [ ] What is the claim process and deadline?
- [ ] Are credits actual credits or just future service (important if planning to churn)?
- [ ] Are service credits the "sole remedy" (blocking other remedies)?

### Exclusions

- [ ] What scheduled maintenance is permitted?
- [ ] What is the maximum scheduled maintenance per month?
- [ ] What notice is required for scheduled maintenance?
- [ ] Are third-party service failures excluded?
- [ ] Are customer-caused issues clearly defined?
- [ ] Are force majeure events excluded?
- [ ] Are alpha/beta features excluded (and how are they designated)?

### Support Levels

- [ ] What are support response time commitments?
- [ ] What hours is support available (business hours vs. 24/7)?
- [ ] How are severity levels defined?
- [ ] Who determines severity classification?
- [ ] Are response times or resolution times committed?
- [ ] What support channels are available (email, phone, chat, portal)?

### Remedies and Termination

- [ ] Does customer have termination right for material SLA breaches?
- [ ] What constitutes a "material" SLA breach?
- [ ] Is there a cure period before termination?
- [ ] What refunds are provided upon SLA-based termination?
- [ ] Are there enhanced remedies beyond credits (e.g., dedicated support)?

### Reporting and Auditing

- [ ] Are monthly SLA reports provided automatically?
- [ ] Is there a public status page?
- [ ] Can customer audit SLA calculations?
- [ ] Are incident post-mortems provided?
- [ ] What data retention period for SLA records?

---

## Negotiation Strategies

### Customer Negotiation Priorities

**Mission-Critical Systems:**
1. **Higher uptime commitment**: Negotiate 99.95%+ for critical systems
2. **Termination rights**: Material breach termination (e.g., <99% for 3 months)
3. **Higher credit caps**: 100% monthly credits or actual damages
4. **24/7 support**: Critical issue response within 1 hour, any time
5. **Limited exclusions**: Minimize third-party and maintenance exclusions

**Standard Business Applications:**
1. **Industry-standard uptime**: 99.9% acceptable
2. **Reasonable credit tiers**: 10-25% for minor breaches, 50%+ for major
3. **Business hours support**: Adequate for non-critical systems
4. **Monthly measurement**: More granular than quarterly/annual
5. **Third-party monitoring**: Right to verify vendor's measurements

**Cost-Sensitive Deployments:**
1. **Lower tier SLA**: Accept 99.5% for reduced cost
2. **Credit-based remedies**: Acceptable if credits are meaningful
3. **Business hours support**: Avoid premium 24/7 support costs
4. **Self-service options**: Reduce support costs with documentation/forums

### Vendor Negotiation Priorities

1. **Credit caps**: Limit to 50% monthly fees or 100% annual fees
2. **Exclusions**: Exclude third-party dependencies, force majeure, customer-caused
3. **Measurement methodology**: Vendor monitoring as authoritative source
4. **Sole remedy**: Service credits as exclusive remedy (limit liability)
5. **Claim requirements**: Require timely claims with documentation

### Balanced Middle Ground

```
"SERVICE LEVEL AGREEMENT - BALANCED TERMS

1. Uptime Commitment: 99.9% Monthly Uptime
   - Measured from Vendor's distributed monitoring (5+ global locations)
   - Customer may use third-party monitoring; if discrepancy >0.5%,
     parties meet and confer

2. Exclusions:
   - Scheduled Maintenance: Max 4 hours/month, Sunday 2-6am PT, 7-day notice
   - Emergency Maintenance: Max 2 hours/month, 4-hour notice (security only)
   - Force Majeure: See Section [X]
   - Customer-Caused: Customer's apps, content, or exceeding usage limits
   - Third-Party Infrastructure: AWS/Azure infrastructure failures

3. Service Credits (per month):
   | Uptime % | Credit | Cap |
   |----------|--------|-----|
   | 99.0-99.9% | 10% | None |
   | 95.0-99.0% | 25% | None |
   | <95.0% | 50% | None |
   - Maximum aggregate credits: 100% of fees paid in prior 12 months

4. Termination for Material Breach:
   If Monthly Uptime <99.0% for 3 consecutive months, Customer may:
   - Terminate Agreement with 30-day notice
   - Receive pro-rata refund of prepaid fees
   - Vendor has 30-day cure period upon first breach notice

5. Support Response Times:
   | Severity | Definition | Response | Hours |
   |----------|-----------|----------|-------|
   | Critical | Service Down | 1 hour | 24/7 |
   | High | Major Feature | 4 hours | Bus. Hrs |
   | Medium | Minor Issue | 8 hours | Bus. Hrs |
   | Low | Question | 2 days | Bus. Hrs |

6. Reporting:
   - Monthly SLA report by 10th of following month
   - Public status page with real-time status and 90-day history
   - Post-mortem for outages >1 hour within 5 business days

7. Credit Claims:
   - Submit within 30 days of month end
   - Include dates/times of unavailability and impact description
   - Vendor verifies and applies to next month's invoice within 15 days"
```

---

## Integration with Other Provisions

### Cross-References to Other Skills

**Liability Limitations** (`liability_limitations.md`):
- SLA credits often carved out from liability cap
- Example: "Notwithstanding liability cap, service credits always available"
- Conversely: "Service credits are Customer's sole remedy (limits liability)"

**Termination Provisions** (`termination_provisions.md`):
- SLA failures may trigger termination for cause
- Material breach definitions often reference SLA thresholds

**Force Majeure** (`force_majeure.md`):
- Force majeure events typically excluded from SLA
- Interplay between force majeure and third-party dependency exclusions

**Warranties and Representations** (`warranties_representations.md`):
- SLA is a performance warranty
- Disclaimer of implied warranties except as specified in SLA

**Payment and Pricing** (`payment_pricing.md`):
- Service credits applied against future invoices
- Usage-based pricing may have separate SLA for metering accuracy

**Dispute Resolution** (`dispute_resolution.md`):
- SLA disputes may have expedited resolution procedures
- Technical disputes about measurement methodology

---

## Common Pitfalls

### Customer Pitfalls

1. **Accepting "Best Efforts" Uptime**
   - No measurable commitment
   - No remedies for failures
   - Fix: Require quantified uptime percentage

2. **No Termination Rights**
   - Stuck with underperforming vendor
   - Service credits meaningless if planning to leave
   - Fix: Material breach termination for repeated SLA failures

3. **Excessive Exclusions**
   - Vendor excludes so many issues that SLA is meaningless
   - Third-party exclusions swallow entire SLA
   - Fix: Limit exclusions to force majeure and customer-caused issues

4. **Credits as Sole Remedy**
   - Prevents consequential damages
   - Prevents termination
   - Fix: Service credits as primary remedy, with termination for material breach

5. **Short Claim Periods**
   - 7-14 day claim window too short for monthly calculations
   - Fix: 30-day claim period from month end

### Vendor Pitfalls

1. **Overly Aggressive Uptime Commitments**
   - Committing to 99.99% when infrastructure supports 99.9%
   - Setting up for consistent SLA failures
   - Fix: Commit to achievable SLA with buffer

2. **Unlimited Service Credits**
   - Could exceed revenue from customer
   - Fix: Cap at 50-100% of fees

3. **Vague Measurement Methodology**
   - Disputes about whether SLA was met
   - Fix: Specify monitoring approach, calculation formula

4. **No Exclusions for Dependencies**
   - Vendor liable for AWS outages beyond their control
   - Fix: Exclude third-party infrastructure failures (but clearly define)

---

## Industry-Specific Considerations

### Financial Services

```
- Higher uptime requirements (99.95%+ for trading platforms)
- Specific regulatory SLAs (e.g., SEC Rule 15c3-5 risk management)
- Disaster recovery SLAs (RTO/RPO commitments)
- Audit rights for SLA compliance
```

### Healthcare (HIPAA)

```
- Availability requirements for patient care systems
- Breach notification SLAs (report within 24-48 hours)
- Backup and recovery SLAs to prevent data loss
- Business Associate Agreement alignment
```

### Government

```
- May require 99.99%+ for critical infrastructure
- FedRAMP or other certification requirements
- US-based support personnel (24/7)
- Specific incident response SLAs
```

### E-Commerce

```
- Peak period SLAs (Black Friday, Cyber Monday)
- Transaction processing SLAs (payment gateway uptime)
- Scalability commitments (auto-scaling SLAs)
- CDN performance SLAs (global latency)
```

---

## When to Consult Experts

Consult legal counsel when:

1. **Critical system SLAs**: Mission-critical systems where downtime = significant revenue loss
2. **Complex composite SLAs**: Multi-component services with interdependencies
3. **Regulatory requirements**: Industry-specific SLA requirements (financial, healthcare)
4. **Custom SLA structures**: Negotiating non-standard SLA terms
5. **SLA disputes**: Vendor claims SLA met, customer disagrees
6. **Damages exceed credits**: Considering consequential damages claim despite SLA cap

Consult technical experts when:

1. **SLA feasibility**: Assessing whether vendor's SLA is realistic given architecture
2. **Monitoring setup**: Designing third-party monitoring to verify vendor claims
3. **Performance baselines**: Establishing realistic performance SLA targets
4. **Composite SLA calculation**: Calculating overall SLA from component SLAs
5. **Disaster recovery**: Defining RTO/RPO requirements

---

## References and Validation

**CAUTION**: This Skills file is synthetically generated and has not been validated by legal experts. The content is based on:
- General commercial contracting principles
- Common SaaS/cloud service SLA structures
- Industry-standard uptime tiers and service credit frameworks
- Technology transaction patterns

**Confidence Level**: 0.6 (Synthetic - Not Expert-Validated)

**Known Limitations**:
- Specific SLA terms vary widely by vendor and industry
- Industry-specific SLA requirements (financial services, healthcare, government) require specialized expertise
- Complex technical SLA calculations (composite SLAs, degraded performance) need validation
- Regulatory SLA requirements (uptime, breach notification) jurisdiction-specific

**Recommended Validation**:
Before relying on this information:
1. Review actual vendor SLA agreements for specific terms
2. Consult legal counsel for mission-critical systems or high-value contracts
3. Consult technical experts for SLA feasibility and monitoring approaches
4. Cross-reference industry-specific SLA standards (e.g., AWS, Azure, Google Cloud)

**For Expert Review**:
Kevin Keller should validate:
- [ ] SLA tier structures (uptime percentages and corresponding credits)
- [ ] Typical exclusion clauses and customer negotiation strategies
- [ ] Support response time standards by severity level
- [ ] Termination rights thresholds for material SLA breaches
- [ ] Industry-specific SLA requirements and variations
- [ ] Practical enforcement challenges with service credits

---

## Cross-References

**Related Key Provisions** (tech_transactions):
- `payment_pricing.md` - Service credits as exclusive remedy tied to pricing
- `termination_provisions.md` - Material SLA breach as termination trigger
- `liability_limitations.md` - SLA credits as cap on performance liability
- `force_majeure.md` - Force majeure exclusions from uptime calculations

**Contract Intelligence Skills** (from 4,900+ real contracts):
- `service-levels-taxonomy.md` - SLA clause patterns from real contracts
- `service-levels-examples.md` - Real SLA language extracted from contracts
- `service-levels-negotiation.md` - Strategic negotiation guidance with S1-S13 patterns
- `maintenance-agreement-expected-clauses.md` - Maintenance/support SLA context

**Cognitive Patterns** (apply to SLA analysis):
- `S3` - Multi-domain synthesis (technical feasibility of SLA commitments)
- `S9` - Hierarchical due diligence (prioritize SLAs by business criticality)
- `BI2` - Economic enforceability (are service credits meaningful remedies?)
- `BI3` - Context-aware risk (SLA tier appropriate for use case?)
