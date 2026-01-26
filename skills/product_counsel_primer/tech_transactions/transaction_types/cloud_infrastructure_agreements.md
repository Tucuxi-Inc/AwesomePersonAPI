---
name: cloud-infrastructure-agreements
description: Cloud Infrastructure Agreements
tags:
  - cloud
  - hosting
  - infrastructure
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

# Cloud & Infrastructure Agreements

```yaml
skill_id: cloud_infrastructure_agreements
domain: transaction_structures
sub_domains: [iaas, paas, cloud_services, multi_tenant, shared_responsibility]
transaction_types: [saas_licensing, data_agreements]
confidence: 0.70
validation_status: synthetic_quick
requires: [service_levels, data_agreements, liability_limitations]
complements: [payment_pricing, force_majeure, termination_provisions]
skill_tier: foundational
mentoring_priority: 3
```

## Overview

Cloud infrastructure agreements govern IaaS (Infrastructure as a Service), PaaS (Platform as a Service), and related cloud computing services. Key issues:
- **Shared responsibility model**: What vendor manages vs. customer manages
- **Multi-tenancy risks**: Isolation, security, noisy neighbor
- **Data location and sovereignty**: Where data is stored/processed
- **Elasticity and scaling**: Auto-scaling, burst capacity, usage limits
- **Lock-in and portability**: Data export, API compatibility, migration

---

## Service Models

### IaaS (Infrastructure as a Service)
```
Examples: AWS EC2, Azure VMs, Google Compute Engine

Customer Manages:
- Operating systems and patches
- Applications and middleware
- Data and security
- Network configuration
- Backup and disaster recovery

Vendor Provides:
- Physical servers and networking
- Hypervisor and virtualization
- Data center facilities
- Power, cooling, physical security
```

### PaaS (Platform as a Service)
```
Examples: Heroku, Google App Engine, Azure App Service

Customer Manages:
- Application code
- Application data
- User access management

Vendor Manages:
- Runtime environment
- Middleware and frameworks
- Operating system patches
- Database management
- Scaling infrastructure
```

### SaaS (Software as a Service)
```
Examples: Salesforce, Workday, Microsoft 365

Customer Manages:
- User data
- Access controls and permissions
- Integration configurations

Vendor Manages:
- Application code and updates
- Infrastructure
- Security patches
- Availability and performance
```

---

## Shared Responsibility Model

**Critical Provision**:
```
"SHARED RESPONSIBILITY

Vendor Responsibilities:
- Security OF the cloud (infrastructure, hardware, facilities)
- Platform availability and performance per SLA
- Physical data center security
- Network infrastructure up to customer VPC boundary

Customer Responsibilities:
- Security IN the cloud (applications, data, access controls)
- Operating system patches (IaaS model)
- Application security and vulnerabilities
- Encryption key management (if customer-managed keys)
- Backup and disaster recovery (customer data)
- User authentication and access management

Vendor is NOT liable for security incidents caused by Customer's
failure to patch systems, configure security groups, or manage credentials."
```

**Why It Matters**: Clarifies who is responsible when security incident occurs. Vendor typically not liable for customer misconfiguration.

---

## Data Location and Sovereignty

**Geographic Data Controls**:
```
"DATA LOCATION

Customer may select primary data region from available options:
- US East (Virginia)
- US West (California)
- EU (Frankfurt)
- Asia Pacific (Singapore)

Data Processing:
- Primary data stored in selected region
- Metadata may be replicated globally for service operation
- Customer Data will not be transferred outside selected region
  except: (a) with Customer's written consent, (b) as required
  by law, (c) for support purposes with Customer approval

Data Residency Exceptions:
- Backup copies may be stored in different region for redundancy
- Disaster recovery may involve cross-region replication
- Certain metadata (account info, logs) processed in US regardless"
```

**GDPR/Privacy Considerations**:
```
For EU customers:
- Data Processing Addendum (DPA) required
- Standard Contractual Clauses if vendor transfers data outside EEA
- Customer typically data controller, vendor is processor
- Right to audit vendor's data processing practices
```

---

## Multi-Tenancy and Isolation

**Multi-Tenant Architecture**:
```
Issue: Multiple customers share same infrastructure

Vendor Obligations:
"Vendor maintains logical separation between Customer's resources
and other tenants through:
- Virtualization and hypervisor isolation
- Network segmentation and VPCs
- Access controls and authentication
- Encryption at rest and in transit

Vendor represents that:
- No customer can access another customer's data
- Resource allocation ensures fair usage (no 'noisy neighbor')
- Security breaches of other tenants do not affect Customer"
```

**Dedicated vs. Shared Infrastructure**:
```
Shared (Standard): Multi-tenant, lower cost
Dedicated Instances: Single-tenant hardware, higher cost, compliance
Private Cloud: Dedicated infrastructure, highest cost, maximum control

Pricing differential: Dedicated may be 2-3x shared pricing
```

---

## Elasticity and Resource Limits

**Auto-Scaling Provisions**:
```
"RESOURCE ALLOCATION

Burstable Capacity:
- Customer may burst up to 2x baseline allocation for up to 4 hours
- Sustained usage above baseline subject to additional charges
- Vendor reserves right to throttle excessive burst usage

Auto-Scaling:
- Customer may configure auto-scaling policies
- Vendor will provision additional resources automatically
- Customer responsible for all usage charges
- No guarantee resources available during extreme demand spikes

Resource Limits:
- Account limits: [X] vCPUs, [Y] TB storage per region
- Rate limits: [Z] API requests per second
- Customer may request limit increases via support ticket"
```

---

## Service Level Agreements

**Cloud Infrastructure SLA**:
```
Compute Availability: 99.99% monthly uptime
Storage Durability: 99.999999999% (11 nines) annual
Network Uptime: 99.9% monthly

Service Credits:
99.0% to <99.99%: 10% monthly bill credit
95.0% to <99.0%: 25% monthly bill credit
<95.0%: 100% monthly bill credit

SLA Exclusions:
- Customer's applications or configurations
- Scheduled maintenance (with 7-day notice)
- Force majeure events
- DDoS attacks targeting customer
- Customer-initiated changes causing downtime
```

**Performance Commitments**:
```
Compute:
- Baseline CPU performance guaranteed
- Burst capacity available on best-effort basis

Storage:
- I/O latency: <10ms (99th percentile) for premium tier
- Throughput: Minimum [X] MB/s per volume

Network:
- Latency within region: <2ms (95th percentile)
- Bandwidth: Minimum [Y] Gbps per instance
```

---

## Data Portability and Lock-In

**Data Export Rights**:
```
"DATA PORTABILITY

Customer may export data at any time via:
- API access (unlimited exports)
- Bulk export tools provided by Vendor
- Database dumps and backups

Upon termination:
- Customer has 30 days to retrieve data
- Vendor provides data in industry-standard formats
  (JSON, CSV, SQL dump, etc.)
- No fees for data export
- Vendor may delete data after 30-day retrieval period

Vendor will not hold data 'hostage' or charge excessive export fees."
```

**Avoiding Vendor Lock-In**:
```
Customer Protections:
- APIs using industry standards (REST, GraphQL)
- Support for standard protocols (HTTPS, TLS, SMTP)
- Open-source compatible tools
- No proprietary data formats
- Container portability (Docker, Kubernetes)

Red Flags:
- Proprietary APIs with no standard alternatives
- Custom database formats requiring vendor tools
- No data export functionality
- Excessive data egress fees (>$0.09/GB)
```

---

## Security and Compliance

**Security Obligations**:
```
Vendor Security:
- SOC 2 Type II audit (annual)
- ISO 27001 certification
- Penetration testing (annual)
- Vulnerability scanning (continuous)
- Security incident notification within 24 hours

Customer Security:
- Implement strong authentication (MFA)
- Configure security groups and firewalls
- Encrypt sensitive data
- Rotate credentials regularly
- Monitor access logs
```

**Compliance Certifications**:
```
Available:
- HIPAA Business Associate Agreement (BAA) for healthcare
- PCI DSS for payment card data
- FedRAMP for US government
- SOC 2 Type II for enterprise customers

Cost: Compliance certifications may require premium tier
```

---

## Pricing Models

**Infrastructure Pricing**:
```
Pay-As-You-Go (On-Demand):
- Compute: $0.10 per hour per vCPU
- Storage: $0.10 per GB-month
- Network egress: $0.09 per GB
- No commitments, pay only for usage

Reserved Instances (1-year or 3-year commitment):
- 30-50% discount vs. on-demand
- Pay upfront or monthly
- Reserved capacity guaranteed

Spot/Preemptible Instances:
- Up to 90% discount vs. on-demand
- Can be interrupted with short notice
- For fault-tolerant workloads
```

---

## Termination and Transition

**Termination Provisions**:
```
Customer Termination: 30 days notice (month-to-month)
Vendor Termination: 90 days notice without cause

Effect of Termination:
- Customer must retrieve data within 30 days
- All customer resources deleted after retrieval period
- Refund of prepaid fees pro-rata
- No penalties for early termination (month-to-month)

Transition Assistance:
- Vendor provides migration tools and documentation
- Professional services available (at additional cost)
- Data export in standard formats
```

---

## Key Negotiation Points

**Customer Priorities**:
- Data sovereignty guarantees (specific regions)
- Committed capacity (no resource unavailability)
- Higher SLA (99.99%+ uptime)
- Longer data retention after termination (60-90 days)
- Migration assistance included
- No lock-in (data portability guarantees)

**Vendor Priorities**:
- Shared responsibility model (customer owns security IN cloud)
- Burst capacity on best-effort basis
- Exclude DDoS and customer-caused outages from SLA
- Limited liability (liability cap, no consequential damages)
- Customer commits to minimum spend or reserved instances

---

## Common Pitfalls

1. **Assuming vendor manages everything**: Understand shared responsibility model
2. **Ignoring data sovereignty**: Data may be processed globally despite region selection
3. **No egress cost planning**: Data transfer out can be expensive ($0.09/GB adds up)
4. **Over-provisioning**: Paying for unused resources (use auto-scaling)
5. **Lock-in risk**: Proprietary APIs make migration difficult
6. **No backup strategy**: Assuming vendor backups = customer backups (often not true)

---

## References and Validation

**CAUTION**: Quick-reference Skills file, not expert-validated.

**Confidence Level**: 0.6 (Synthetic Quick Version)

**For Expert Review**:
- [ ] Shared responsibility model accuracy
- [ ] Typical SLA terms for IaaS/PaaS
- [ ] Data sovereignty standard provisions
- [ ] Multi-tenancy isolation guarantees
- [ ] Pricing model structures
- [ ] Lock-in mitigation strategies

**Recommended Backfill**: AWS/Azure/Google Cloud specific comparisons, detailed compliance requirements, cost optimization strategies, migration case studies.

---

## Cross-References

**Related Transaction Types** (tech_transactions):
- `saas_licensing_agreements.md` - SaaS built on cloud infrastructure
- `data_agreements.md` - Data processing on cloud
- `professional_services_agreements.md` - Cloud implementation services

**Contract Intelligence Skills** (from 4,900+ real contracts):
- `service-levels-taxonomy.md` - Cloud SLA patterns
- `data-protection-taxonomy.md` - Cloud data handling
- `termination-taxonomy.md` - Cloud exit and data portability
- `limitation-of-liability-taxonomy.md` - Cloud liability structures

**Cognitive Patterns** (apply to cloud analysis):
- `S3` - Multi-domain synthesis (cloud architecture + legal + security)
- `S4` - Risk assessment (cloud vendor risk)
- `S6` - Dynamic framework (cloud service evolution)
- `BI3` - Context-aware risk (cloud criticality for business)
