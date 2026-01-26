---
name: pcp-mc20-multi-dimensional-risk-architecture
description: Mapping and managing risks across legal, operational, reputational, and
  strategic dimensions
tags:
- meta-cognitive
- orchestration-operator
- risk-reasoning
version: '1.0'
confidence_level: HIGH
validated_by: Email Corpus Analysis (Anthropic Extraction)
validated_date: '2025-12-15'
email_evidence_count: 252
pattern_tier: 3
category: meta_cognitive
source_skills:
- S4
- BI3
- S12
- BI19
- BI12
- CJC1
# Domain knowledge skills
- regulatory-risk-frameworks  # Regulatory risk dimension
- technical-integration-risks  # Technical risk dimension
works_with:
- PCP-MC16
- PCP-MC18
- PCP-MC25
co_occurs_with:
- PCP-MC11
- PCP-MC16
- PCP-MC17
- PCP-MC3
- PCP-MC1
---

# PCP-MC20: Multi-Dimensional Risk Architecture

## Pattern Definition

### Trigger Condition
Activate when risks span multiple dimensions (legal, operational, reputational, financial, strategic) and cannot be adequately addressed by single-dimension risk analysis.

### Core Procedure
1. **Dimension Mapping**: Identify all risk dimensions relevant to the situation
2. **Cross-Dimension Dependencies**: Map how risks in one dimension create or amplify risks in others
3. **Liability Chain Analysis**: Trace how liability flows through entities and decisions
4. **Containment Architecture**: Design boundaries to prevent risk cascade
5. **Distribution Strategy**: Structure arrangements to allocate risks appropriately
6. **Threshold Navigation**: Identify and stay within acceptable risk thresholds per dimension

### Expert Heuristic
"Risk isn't a single number—it's a topology. The expert sees how legal risk amplifies reputational risk, how operational failures create legal exposure, and designs architectures that contain cascades before they become catastrophic."

## Evidence from Email Corpus

### Example 1: Liability Distribution Strategy
**Context:** [PERSON] structuring liability across entities
**Evidence:** "Strategic reasoning about how to distribute legal and operational liability across corporate entities"
**Insight:** Liability is distributable; architecture determines where risk lands when things go wrong.

### Example 2: Compliance Discovery Cascading
**Context:** [PERSON] assessing compliance failure propagation
**Evidence:** "Analyzing how compliance failures in one area trigger discovery and scrutiny in related areas"
**Insight:** Compliance risks cascade—one failure invites investigation of adjacent areas.

### Example 3: Regulatory Enforcement Uncertainty Navigation
**Context:** [PERSON] operating under enforcement ambiguity
**Evidence:** "Strategic decision-making when regulatory enforcement patterns are inconsistent or unpredictable"
**Insight:** Risk includes enforcement uncertainty; architecture must handle variable enforcement.

### Example 4: Diligence-Reliance Calibration
**Context:** [PERSON] balancing due diligence and reliance on others
**Evidence:** "Calibrating the appropriate level of independent verification vs. reliance on counterparty representations"
**Insight:** Diligence has costs; the expert calibrates depth based on risk magnitude and counterparty reliability.

### Example 5: Cross-Jurisdictional Risk Containment
**Context:** [PERSON] managing multi-jurisdiction exposure
**Evidence:** "Designing structures to contain risks within specific jurisdictions rather than allowing cross-border propagation"
**Insight:** Jurisdictional boundaries can be risk containment walls when properly architected.

## Integration with Pattern Tiers

### Orchestrates (Lower-Tier Patterns)
- **S4 (Risk Assessment)**: Single-dimension risk analysis
- **BI3 (Risk Calibration)**: Calibrating acceptable thresholds
- **S12 (Cross-Jurisdictional)**: Jurisdiction-specific risks

### Invoked By (Higher-Level Orchestration)
- **SAGE_MODE**: When risk profile is complex and multi-dimensional
- **PCP-MC16 (Multi-Objective)**: When risk is one of competing objectives

### Works In Concert With (Evidence-Based Co-Occurrence)
**Core Triad (8,000+ co-occurrences each):**
- **PCP-MC11 (Strategic Timing)**: 9,671 co-occurrences - timing decisions require risk assessment
- **PCP-MC16 (Multi-Objective)**: 8,210 co-occurrences - risk is often one competing objective

**Strong Relationships (1,000+ co-occurrences):**
- **PCP-MC17 (Cross-Functional)**: 3,302 co-occurrences - different functions see different risks
- **PCP-MC3 (Communication Framing)**: 1,352 co-occurrences - risk communication requires careful framing
- **PCP-MC1 (Mental Models)**: 1,260 co-occurrences - stakeholder risk tolerance varies

**Additional Relationships:**
- **PCP-MC18 (Systems Reasoning)**: Risk propagates through systems
- **PCP-MC25 (Regulatory Path)**: Regulatory risks need special handling
- **PCP-MC28 (Document Lifecycle)**: Risk documentation and version control
- **PCP-MC27 (Urgency Coordination)**: Risk under time pressure

## Sub-Patterns Identified

1. **Liability Distribution Strategy**: Allocating liability across entities
2. **Compliance Discovery Cascading**: Understanding cascade triggers
3. **Regulatory Enforcement Uncertainty**: Operating under variable enforcement
4. **Diligence-Reliance Calibration**: Balancing verification and trust
5. **Cross-Jurisdictional Containment**: Using boundaries as walls
6. **Risk-Magnitude Decoupling**: Separating likelihood from impact

## Metadata
```yaml
pattern_id: PCP-MC20
pattern_name: Multi-Dimensional Risk Architecture
tier: 3 (Meta-Cognitive)
extraction_confidence: 0.85 (corpus-validated with 18,984 known instances)
corpus_validation: Full Corpus (44,728 emails)
core_triad_member: true
primary_co_occurrences:
  - PCP-MC11: 9,671 (Strategic Timing) - HIGHEST co-occurrence in corpus
  - PCP-MC16: 8,210 (Multi-Objective Optimization)
  - PCP-MC17: 3,302 (Cross-Functional Synthesis)
  - PCP-MC3: 1,352 (Communication Framing)
related_patterns: [PCP-MC1, PCP-MC3, PCP-MC11, PCP-MC16, PCP-MC17, PCP-MC18, PCP-MC25, PCP-MC27, PCP-MC28, S4, S12, BI3]
domain_applicability: Legal structuring, compliance, corporate transactions
```
