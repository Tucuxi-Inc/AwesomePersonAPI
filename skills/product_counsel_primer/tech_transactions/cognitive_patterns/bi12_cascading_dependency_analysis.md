---
name: bi12-cascading-dependency-analysis
description: >-
  This skill enables systematic identification and management of cascading dependencies across complex systems, recognizing how failures or changes in one component propagate through interconnected business, legal, and technical domains.
tags:
  - dependency-mapping-cascade-analysis-system-thinking-risk-propagation-failure-mode-analysis-interconnection-assessment-domino-effects-critical-path
version: '1.0'
confidence_level: MEDIUM
category: business_intelligence
validated_by: Integration Map Reference
validated_date: '2025-12-17'
skill_tier: strategic
mentoring_priority: 7
validation_type: expert_extracted
source_type: pattern_inference
pattern_tier: 2
orchestrated_by:
  - MC18
  - MC20
---

# BI12 - Cascading Dependency Analysis

**Type:** Business Intelligence - Systems Analysis
**Focus Area:** Multi-system dependency mapping and cascade risk management
**Complexity:** 8/10
**Uniqueness:** 7/10

## Description

This skill enables experts to systematically identify, map, and manage cascading dependencies across complex interconnected systems. When analyzing transactions, crises, or organizational changes, experts recognize that impacts rarely remain isolated - a change or failure in one domain propagates through technical, legal, business, and organizational boundaries in predictable but often overlooked patterns.

The skill applies systems thinking to anticipate "domino effects" before they occur, enabling proactive mitigation rather than reactive crisis management. This includes mapping both direct dependencies (A depends on B) and transitive dependencies (A depends on B which depends on C), as well as identifying feedback loops and amplification mechanisms.

## Keywords

- dependency mapping, cascade analysis, system thinking, risk propagation, failure mode analysis, interconnection assessment, domino effects, critical path, knock-on effects

## Application Guidance

Apply this skill when evaluating any change, decision, or risk that touches multiple interconnected systems. Particularly valuable when:
- Assessing vendor termination impacts across integrated technology stack
- Evaluating regulatory change propagation through compliance systems
- Analyzing contract termination ripple effects on dependent agreements
- Planning system migrations with complex integration dependencies
- Modeling crisis scenario propagation paths

---

## 1. Detailed Pattern Description

### Theoretical Foundations

**Graph Theory and Network Analysis**: Dependencies form directed graphs where nodes represent system components and edges represent dependency relationships. Critical path analysis identifies which dependencies create the longest propagation chains.

**Failure Mode and Effects Analysis (FMEA)**: Systematic evaluation of how component failures cascade, including severity, occurrence probability, and detection capability for each cascade path.

**Systems Dynamics**: Understanding feedback loops where cascades can either dampen (negative feedback) or amplify (positive feedback) through the system.

## 2. Step-by-Step Framework

### Phase 1: Dependency Mapping

**Step 1.1: Identify Direct Dependencies**
- Map all first-order dependencies from the component/decision being analyzed
- Categorize by type: technical, contractual, organizational, regulatory, financial

**Step 1.2: Trace Transitive Dependencies**
- For each direct dependency, identify its dependencies (second-order)
- Continue until reaching stable endpoints or circular references
- Document dependency depth for each path

**Step 1.3: Identify Feedback Loops**
- Look for circular dependencies that could amplify effects
- Assess whether loops are stabilizing or destabilizing

### Phase 2: Cascade Risk Assessment

**Step 2.1: Evaluate Propagation Probability**
- For each dependency link, assess likelihood of cascade given trigger
- Consider timing delays in propagation

**Step 2.2: Assess Impact Magnitude at Each Node**
- Quantify impact if cascade reaches each dependent component
- Identify concentration points where multiple cascades converge

**Step 2.3: Calculate Aggregate Cascade Risk**
- Combine probability and impact across all paths
- Identify highest-risk cascade scenarios

### Phase 3: Mitigation Planning

**Step 3.1: Identify Circuit Breakers**
- Points where cascade can be interrupted or contained
- Contractual provisions, technical isolation, organizational boundaries

**Step 3.2: Design Monitoring Triggers**
- Early warning indicators for cascade initiation
- Escalation thresholds and response protocols

---

## Cross-References

### Orchestrated By (Tier 3 MC Patterns)
- **MC18 (Systems Architecture Reasoning)**: Primary orchestrator - determines when to apply cascade analysis
- **MC20 (Multi-Dimensional Risk Architecture)**: Risk dimension that cascade analysis informs

### Related Patterns (Same Tier)
- **BI3 (Context-Aware Risk Calibration)**: Calibrates risk assessment based on cascade potential
- **BI19 (Crisis Recovery Portfolio Risk)**: Portfolio-level cascade management
- **S10 (Systemic Legal Impact Assessment)**: Legal system cascade effects

### Downstream Applications
- Vendor risk assessment
- Contract termination planning
- System migration risk analysis
- Regulatory change impact assessment

---

## Metadata

**Pattern ID:** BI12
**Tier:** 2 (Behavioral Intelligence)
**Domain:** Systems Analysis / Risk Management
**Status:** Active - Map Derived
