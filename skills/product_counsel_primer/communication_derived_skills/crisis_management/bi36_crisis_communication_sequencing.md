---
name: bi36-crisis-communication-sequencing
description: >-
  This skill enables strategic sequencing of crisis communications across multiple stakeholder groups, ensuring message consistency while respecting information hierarchy and timing requirements.
tags:
  - crisis-communication-stakeholder-sequencing-message-timing-information-hierarchy-audience-prioritization-narrative-control-damage-containment
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
  - MC5
  - MC22
---

# BI36 - Crisis Communication Sequencing

**Type:** Business Intelligence - Crisis Management
**Focus Area:** Strategic ordering and timing of crisis communications
**Complexity:** 8/10
**Uniqueness:** 7/10

## Description

This skill enables experts to strategically sequence crisis communications across multiple stakeholder groups. In crisis situations, the order in which different audiences learn information significantly impacts both the crisis trajectory and stakeholder relationships. Experts must balance competing pressures: legal notification requirements, relationship preservation, information leakage risks, and narrative control.

The skill integrates communication strategy with stakeholder analysis, recognizing that each audience has different information needs, relationship dynamics, and potential to amplify or dampen crisis impact based on how they learn about developments.

## Keywords

- crisis communication, stakeholder sequencing, message timing, information hierarchy, audience prioritization, narrative control, damage containment, communication cadence

## Application Guidance

Apply this skill when:
- A significant negative event requires disclosure to multiple audiences
- Regulatory notifications have specific timing requirements
- Information leakage could preempt planned communications
- Different stakeholders have conflicting information timing preferences
- Crisis involves both internal and external communication requirements

---

## 1. Detailed Pattern Description

### Theoretical Foundations

**Stakeholder Theory (Freeman)**: Different stakeholders have different salience based on power, legitimacy, and urgency - crisis communication order should reflect this hierarchy.

**Information Asymmetry**: Controlling the sequence of disclosure can reduce adverse selection and moral hazard problems in ongoing relationships.

**Signaling Theory**: The order and manner of disclosure signals organizational priorities and competence to stakeholders.

## 2. Step-by-Step Framework

### Phase 1: Stakeholder Mapping for Crisis

**Step 1.1: Identify All Affected Audiences**
- Primary: Board, executives, employees, regulators
- Secondary: Customers, partners, investors, media
- Tertiary: Industry analysts, competitors, general public

**Step 1.2: Assess Notification Requirements**
| Stakeholder | Legal Requirement | Relationship Requirement | Timing Constraint |
|-------------|------------------|-------------------------|-------------------|
| Regulators | Often mandatory | Maintain credibility | Usually specified |
| Board | Fiduciary duty | Trust maintenance | Immediate |
| Employees | Depends on nature | Morale/retention | Before external |
| Customers | Contractual | Relationship | Before media |

**Step 1.3: Map Information Leakage Paths**
- Which audiences might leak to others?
- What is the realistic hold time for each group?
- Which leaks would be most damaging?

### Phase 2: Sequence Design

**Step 2.1: Establish Communication Waves**
- Wave 1: Mandatory/immediate (regulators if required, board)
- Wave 2: Internal (executives, then broader employee base)
- Wave 3: Key external (major customers, critical partners)
- Wave 4: Public (press release, website, social media)

**Step 2.2: Design Hold Periods**
- Minimum time between waves to prepare next audience
- Maximum time before leakage risk becomes unacceptable
- Buffer for unexpected questions requiring escalation

**Step 2.3: Prepare Escalation Protocol**
- If leak occurs during sequencing, accelerate remaining waves
- Pre-position statements for accelerated release
- Identify decision-maker for compression authorization

### Phase 3: Execution Management

**Step 3.1: Synchronized Deployment**
- Clear trigger for each wave initiation
- Confirmation protocol that wave completed
- Real-time monitoring for leakage indicators

**Step 3.2: Message Consistency Control**
- Core facts consistent across all audiences
- Tailored framing appropriate to each audience
- Q&A guidance for each communication team

---

## Cross-References

### Orchestrated By (Tier 3 MC Patterns)
- **MC5 (Emotional Contagion Management)**: Manages emotional dynamics during crisis
- **MC22 (Strategic Communication Architecture)**: Designs multi-channel communication

### Related Patterns (Same Tier)
- **BI34 (Crisis Intelligence Synthesis)**: Crisis assessment informing communication
- **BI35 (Crisis Stakeholder Coordination)**: Stakeholder management during crisis
- **BI38 (Cross-Functional Crisis Authority)**: Decision authority for communications

### Downstream Applications
- Crisis communication planning
- Regulatory notification compliance
- Investor relations management
- Internal communications strategy

---

## Metadata

**Pattern ID:** BI36
**Tier:** 2 (Behavioral Intelligence)
**Domain:** Crisis Management / Communications
**Status:** Active - Map Derived
