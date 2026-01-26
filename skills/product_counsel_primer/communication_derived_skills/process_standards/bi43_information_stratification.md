---
name: bi43-information-stratification
description: >-
  This skill enables strategic layering of information disclosure across different audiences and contexts, managing what information is shared with whom, when, and in what form to optimize outcomes.
tags:
  - information-stratification-disclosure-management-audience-segmentation-need-to-know-information-architecture-selective-transparency-confidentiality-tiers
version: '1.0'
confidence_level: MEDIUM
category: business_intelligence
validated_by: Integration Map Reference
validated_date: '2025-12-17'
skill_tier: strategic
mentoring_priority: 8
validation_type: expert_extracted
source_type: pattern_inference
pattern_tier: 2
orchestrated_by:
  - MC8
  - MC28
  - MC29
---

# BI43 - Information Stratification

**Type:** Business Intelligence - Strategic Relationships
**Focus Area:** Multi-tier information disclosure management
**Complexity:** 8/10
**Uniqueness:** 8/10

## Description

This skill enables experts to strategically layer information across different audiences, contexts, and time periods. Rather than treating information disclosure as binary (share or don't share), experts recognize that information can be stratified - different stakeholders receive different levels of detail, framing, or timing based on their needs, relationship, and the strategic implications of their knowledge.

The skill integrates confidentiality management with stakeholder relations, recognizing that appropriate information stratification serves both protective (limiting sensitive information exposure) and relationship (providing stakeholders what they need) functions.

## Keywords

- information stratification, disclosure management, audience segmentation, need-to-know, information architecture, selective transparency, confidentiality tiers, information layering

## Application Guidance

Apply this skill when:
- Multiple stakeholders need different levels of information about the same matter
- Sensitive information must be shared selectively
- Timing of disclosure differs across audiences
- Legal privilege or confidentiality requires controlled distribution
- Strategic negotiations involve information asymmetry management

---

## 1. Detailed Pattern Description

### Theoretical Foundations

**Information Economics**: Information has value that varies by recipient - stratification optimizes information value while managing leakage costs.

**Principal-Agent Theory**: Information asymmetry between parties must be managed to align incentives while protecting interests.

**Need-to-Know Principle (Security)**: Information access should be limited to those who require it for legitimate purposes.

## 2. Step-by-Step Framework

### Phase 1: Information Classification

**Step 1.1: Categorize Information by Sensitivity**
| Tier | Sensitivity | Example | Default Access |
|------|-------------|---------|----------------|
| Public | Low | Press releases, public filings | Anyone |
| Internal | Medium | Business plans, org changes | Employees |
| Confidential | High | Deal terms, litigation strategy | Need-to-know |
| Restricted | Critical | M&A plans, privileged advice | Named individuals |

**Step 1.2: Assess Leakage Consequences**
- What happens if this information reaches unintended audiences?
- Is damage reputational, competitive, legal, or relational?
- Is leakage reversible or permanent?

**Step 1.3: Map Information Dependencies**
- What must someone know to understand this information?
- What conclusions might they draw from partial information?
- How does this information combine with other knowledge?

### Phase 2: Audience Stratification

**Step 2.1: Identify All Potential Audiences**
- Internal: Board, executives, legal, business teams
- External: Counterparties, regulators, advisors, public

**Step 2.2: Assess Each Audience's Information Needs**
- What do they need to know for their role?
- What would be helpful but not essential?
- What would be harmful for them to know?

**Step 2.3: Define Information Packages by Audience**
| Audience | Information Package | Excluded Information |
|----------|--------------------|--------------------|
| Board | Strategic summary + key risks | Tactical details |
| Legal team | Full detail + privilege | Business strategy |
| Counterparty | Negotiation position | BATNA, reserve price |
| Regulators | Compliance facts | Commercial strategy |

### Phase 3: Disclosure Management

**Step 3.1: Design Disclosure Protocols**
- Who can authorize disclosure at each tier?
- What documentation is required?
- How is access tracked and audited?

**Step 3.2: Manage Information Boundaries**
- Clean team arrangements for sensitive deals
- Privilege logs and maintenance
- Information barrier procedures

**Step 3.3: Handle Tier Transitions**
- When does information move between tiers?
- What triggers broader disclosure?
- How to manage partial leakage?

---

## Cross-References

### Orchestrated By (Tier 3 MC Patterns)
- **MC8 (Information Revelation Strategy)**: Primary orchestrator - strategic disclosure decisions
- **MC28 (Document Lifecycle Intelligence)**: Document-based information management
- **MC29 (Post-Task Reflection)**: Refines information flow from lessons

### Related Patterns (Same Tier)
- **S2 (Information Gap Identification)**: What information exists
- **BI20 (Remote Stakeholder Coordination)**: Information flow design
- **Confidentiality provisions (clause taxonomy)**: Contractual information protection

### Downstream Applications
- M&A information management
- Litigation privilege protocols
- Negotiation information strategy
- Regulatory disclosure management

---

## Metadata

**Pattern ID:** BI43
**Tier:** 2 (Behavioral Intelligence)
**Domain:** Strategic Relationships / Information Management
**Status:** Active - Map Derived
