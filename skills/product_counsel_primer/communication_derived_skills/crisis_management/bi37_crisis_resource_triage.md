---
name: bi37-crisis-resource-triage
description: >-
  This skill enables rapid prioritization and allocation of limited resources during crisis situations, applying triage principles to ensure critical functions receive support while accepting controlled degradation elsewhere.
tags:
  - crisis-triage-resource-allocation-priority-assessment-critical-function-identification-controlled-degradation-emergency-response-capacity-management
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
  - MC23
  - MC27
---

# BI37 - Crisis Resource Triage

**Type:** Business Intelligence - Crisis Management
**Focus Area:** Emergency resource prioritization and allocation
**Complexity:** 8/10
**Uniqueness:** 7/10

## Description

This skill enables experts to rapidly prioritize and allocate limited resources during crisis situations. When demand for attention, personnel, budget, and time exceeds supply, experts must make explicit trade-offs about what receives full support, what receives partial support, and what must wait or be abandoned.

The skill applies medical triage principles to business crisis response: focusing resources where they can have maximum impact, accepting that some lower-priority matters will experience degraded service, and recognizing that attempting to address everything equally results in addressing nothing adequately.

## Keywords

- crisis triage, resource allocation, priority assessment, critical function identification, controlled degradation, emergency response, capacity management, trade-off decisions

## Application Guidance

Apply this skill when:
- Crisis demands exceed available response capacity
- Multiple urgent matters compete for limited expert attention
- Normal resource allocation processes are too slow for crisis tempo
- Trade-offs between business functions must be made explicitly
- Recovery prioritization decisions are required

---

## 1. Detailed Pattern Description

### Theoretical Foundations

**Triage Theory (Medical)**: Allocate resources to maximize lives saved, not to save any individual life - adapted to maximize business survival/value.

**Queuing Theory**: When arrival rate exceeds service rate, queues build infinitely - must either increase capacity or reduce arrivals through prioritization.

**Opportunity Cost Economics**: Every resource deployed to one area is unavailable to another - crisis amplifies these trade-offs.

## 2. Step-by-Step Framework

### Phase 1: Demand Assessment

**Step 1.1: Inventory Active Crisis Demands**
- List all matters requiring attention
- Estimate resource requirement for each (time, expertise, budget)
- Assess deadline urgency for each

**Step 1.2: Assess Available Capacity**
- Current personnel bandwidth
- Budget flexibility
- External resource availability (counsel, consultants)
- Timeline until reinforcement possible

**Step 1.3: Calculate Demand-Capacity Gap**
- Total demand vs. total capacity
- Bottleneck identification (which resource is most constrained?)
- Timeline for gap (when does crisis tempo normalize?)

### Phase 2: Triage Classification

**Step 2.1: Apply Triage Categories**
| Category | Criteria | Action |
|----------|----------|--------|
| Critical | Existential threat, immediate action required | Full resources immediately |
| Urgent | Significant damage if delayed, recoverable | Resources within 24h |
| Important | Material impact, can tolerate delay | Scheduled attention |
| Deferrable | Lower impact, fully recoverable | Pause until crisis passes |
| Abandon | Irrecoverable or not worth saving | Explicit write-off |

**Step 2.2: Assign Each Matter to Category**
- Resist pressure to classify everything as critical
- Enforce maximum percentage in each category
- Document rationale for borderline decisions

**Step 2.3: Communicate Triage Decisions**
- Stakeholders for deferred matters must understand and accept
- Set expectations for resumed attention
- Identify escalation triggers that would re-prioritize

### Phase 3: Dynamic Reallocation

**Step 3.1: Monitor Crisis Evolution**
- Categories may shift as crisis develops
- New matters enter the queue
- Some matters resolve or escalate

**Step 3.2: Periodic Re-triage**
- Daily reassessment during acute crisis
- Explicit protocol for emergency re-prioritization
- Authority clarity for triage decisions

---

## Cross-References

### Orchestrated By (Tier 3 MC Patterns)
- **MC23 (Resource Allocation Under Uncertainty)**: Strategic resource decisions
- **MC27 (Urgency-Driven Coordination)**: Coordination under time pressure

### Related Patterns (Same Tier)
- **BI1 (Strategic Deal Qualification)**: Normal-state resource allocation
- **BI7 (Crisis Financial Engineering)**: Financial resource triage
- **BI38 (Cross-Functional Crisis Authority)**: Authority for triage decisions

### Downstream Applications
- Crisis response planning
- Business continuity prioritization
- Legal matter portfolio management
- Resource mobilization protocols

---

## Metadata

**Pattern ID:** BI37
**Tier:** 2 (Behavioral Intelligence)
**Domain:** Crisis Management / Resource Allocation
**Status:** Active - Map Derived
