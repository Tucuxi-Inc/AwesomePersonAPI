---
name: pcp-mc26-stakeholder-mental-state-inference
description: Inferring stakeholder preferences, concerns, and likely reactions from
  limited signals
tags:
- meta-cognitive
- orchestration-operator
- theory-of-mind
version: '1.0'
confidence_level: MEDIUM
validated_by: Email Corpus Analysis (Anthropic Extraction)
validated_date: '2025-12-15'
email_evidence_count: 52
pattern_tier: 3
category: meta_cognitive
related_patterns:
- PCP-MC1
- PCP-MC4
source_skills:
- BI14
- BI31
- S14
works_with:
- PCP-MC1
- PCP-MC4
- PCP-MC14
---

# PCP-MC26: Stakeholder Mental State Inference

## Pattern Definition

### Trigger Condition
Activate when you need to understand stakeholder preferences, concerns, or likely reactions but have only indirect signals—when you cannot simply ask and must infer from behavior, context, and history.

### Core Procedure
1. **Signal Collection**: Gather available signals about stakeholder mental state
2. **Context Framing**: Understand the situation from the stakeholder's perspective
3. **History Integration**: Factor in past behavior and stated preferences
4. **Preference Modeling**: Build models of what stakeholder actually values (vs. claims)
5. **Reaction Prediction**: Predict likely responses to proposed actions
6. **Validation Testing**: Design low-cost tests to validate inferences

### Expert Heuristic
"What people say they want and what they actually want are often different. The expert watches what stakeholders DO when facing trade-offs—that reveals true preferences better than any stated position."

## Evidence from Email Corpus

### Example 1: Negotiation Signal Interpretation
**Context:** [PERSON] reading negotiation signals
**Evidence:** "Interpreting subtle signals during negotiations to infer counterparty's true positions and constraints"
**Insight:** Negotiators send signals they don't intend; reading them reveals real constraints.

### Example 2: Preference Evolution Modeling
**Context:** [PERSON] tracking preference changes
**Evidence:** "Tracking how stakeholder preferences evolve over time and under different conditions"
**Insight:** Preferences aren't static; understanding evolution improves prediction.

### Example 3: Regulatory Relationship Temperature
**Context:** [PERSON] assessing regulator stance
**Evidence:** "Reading signals about regulatory relationship health and enforcement likelihood"
**Insight:** Regulatory "temperature" signals likely future actions.

### Example 4: Candidate Trajectory Inference
**Context:** [PERSON] assessing candidate intentions
**Evidence:** "Inferring candidate career intentions and mobility from indirect signals"
**Insight:** Candidates signal intentions indirectly; reading signals prevents bad hires.

### Example 5: Supply Chain Mental Model
**Context:** [PERSON] understanding supplier perspective
**Evidence:** "Reverse engineering supplier mental models from their proposals and pushback"
**Insight:** Supplier proposals reveal their constraints and priorities.

## Relationship to PCP-MC1 and PCP-MC4

- **PCP-MC1 (Stakeholder Mental Models)**: Constructs explicit models of stakeholder perspectives
- **PCP-MC4 (Recursive Intention Modeling)**: Models what stakeholders think about what you think
- **PCP-MC26**: Focuses on INFERRING hidden mental states from limited signals

Use PCP-MC26 when you can't directly assess stakeholder state and must infer from behavior.

## Integration with Pattern Tiers

### Orchestrates (Lower-Tier Patterns)
- **PCP-MC1 (Mental Models)**: Provides framework for inference
- **PCP-MC4 (Recursive Intention)**: Deep intention modeling
- **BI3 (Risk Calibration)**: Risk of misreading stakeholders

### Works In Concert With
- **PCP-MC3 (Communication Framing)**: Framing based on inferred state
- **PCP-MC14 (Adversarial Perspective)**: Inferring adversary mental state
- **PCP-MC21 (Political Intelligence)**: Organizational politics inference
- **PCP-MC5 (Emotional Contagion)**: Emotional state inference feeds emotional management

### New Pattern Links
- **PCP-MC27**: Urgency intensifies inference needs; crisis requires rapid mental state assessment
- **PCP-MC28**: Documentation reveals mental states over time; written artifacts as inference source
- **PCP-MC29**: Post-task reflection reveals inference accuracy; learning which signals were predictive

## Sub-Patterns Identified

1. **Negotiation Signal Interpretation**: Reading deal signals
2. **Preference Evolution Modeling**: Tracking preference changes
3. **Regulatory Temperature Reading**: Assessing regulator stance
4. **Trajectory Inference**: Predicting stakeholder moves
5. **Supply Chain Mental Modeling**: Understanding supplier perspective
6. **Sensitivity Context Modeling**: Understanding triggers

## Metadata
- **Source**: Phase B Anthropic Extraction (52 patterns)
- **Related Patterns**: PCP-MC1, PCP-MC3, PCP-MC4, PCP-MC14, PCP-MC21, BI3
- **Domain Applicability**: Negotiations, hiring, regulatory relations, stakeholder management
