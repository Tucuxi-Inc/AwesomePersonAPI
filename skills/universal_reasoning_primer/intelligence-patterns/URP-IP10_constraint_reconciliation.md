---
name: urp-ip10-constraint-reconciliation
description: Intelligence pattern for reconciling conflicting constraints from different domains, stakeholders, or requirements to find solutions that satisfy all necessary constraints.
tags:
- intelligence
- solution-design
- constraint-satisfaction
- reconciliation
- multi-requirement
version: '1.0'
confidence_level: HIGH
category: intelligence_patterns
validated_by: Literature Synthesis
validated_date: '2025-12-30'
skill_tier: applied
pattern_tier: 2
mentoring_priority: 8
validation_type: literature_synthesis
source_type: academic_research
orchestrates: []
orchestrated_by:
- URP-SP3
- URP-SP8
---

# URP-IP10: Constraint Reconciliation

**Type:** Intelligence Pattern (Tier 2)
**Function:** Finding solutions that satisfy multiple conflicting constraints
**Domain Independence:** Universal across any multi-constraint context
**Orchestration Role:** Enables solutions in over-constrained problem spaces

## Pattern Definition

### Core Procedure

1. **Constraint Inventory**: What constraints apply from all relevant sources?
2. **Conflict Identification**: Which constraints conflict?
3. **Constraint Classification**: Which are hard (must satisfy) vs. soft (prefer)?
4. **Reconciliation Search**: How can conflicting constraints be satisfied simultaneously?
5. **Tradeoff Optimization**: Where reconciliation is impossible, what's the optimal tradeoff?

### Expert Heuristic

> "Conflicting constraints aren't necessarily incompatible—they may just look incompatible from a limited perspective. Before accepting tradeoffs, search for solutions that satisfy all constraints."

## Evidence from Literature

- **Constraint Satisfaction**: Computer science frameworks for constraint problems
- **Multi-Criteria Decision Making**: Reconciling multiple objectives
- **Paradox Management**: Working with competing demands
- **Systems Design**: Meeting multi-domain requirements

---

## Metadata

```yaml
pattern_id: URP-IP10
pattern_name: Constraint Reconciliation
tier: 2 (Intelligence)
core_question: "How can I satisfy all these conflicting constraints?"
domain_independence: Universal
transfer_rate: ">85%"
extraction_confidence: 0.87
```
