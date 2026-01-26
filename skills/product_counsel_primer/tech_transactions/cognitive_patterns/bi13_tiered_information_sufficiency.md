---
name: bi13-tiered-information-sufficiency
description: >-
  This skill enables systematic assessment of whether available information is sufficient for decisions at different stakes levels, calibrating due diligence depth to decision importance and reversibility.
tags:
  - information-sufficiency-decision-quality-due-diligence-calibration-epistemic-assessment-knowledge-gaps-evidence-thresholds-decision-readiness
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
  - MC19
  - MC15
---

# BI13 - Tiered Information Sufficiency

**Type:** Business Intelligence - Decision Support
**Focus Area:** Information adequacy assessment calibrated to decision stakes
**Complexity:** 7/10
**Uniqueness:** 8/10

## Description

This skill enables experts to systematically assess whether available information is sufficient to support decisions at various stakes levels. Rather than applying uniform due diligence standards to all decisions, experts calibrate information requirements based on decision magnitude, reversibility, and downstream consequences.

The skill recognizes that both over-investigation (analysis paralysis) and under-investigation (premature decisions) carry costs. Optimal decision-making requires matching information depth to decision importance - routine matters warrant quick assessment while transformative decisions require comprehensive validation.

## Keywords

- information sufficiency, decision quality, due diligence calibration, epistemic assessment, knowledge gaps, evidence thresholds, decision readiness, information adequacy

## Application Guidance

Apply this skill when:
- Determining how much due diligence is appropriate for a transaction
- Deciding whether to proceed with available information or gather more
- Prioritizing information-gathering efforts across multiple workstreams
- Communicating confidence levels to stakeholders
- Balancing speed and thoroughness in time-sensitive situations

---

## 1. Detailed Pattern Description

### Theoretical Foundations

**Decision Theory**: Expected value of information (EVOI) calculations - additional information is worth gathering only if expected decision improvement exceeds gathering costs.

**Epistemology**: Knowledge justification standards vary by context - scientific certainty differs from practical business certainty differs from legal certainty.

**Satisficing vs. Maximizing**: Herbert Simon's bounded rationality - decisions should be "good enough" given constraints rather than theoretically optimal.

## 2. Step-by-Step Framework

### Phase 1: Decision Classification

**Step 1.1: Assess Decision Stakes**
| Tier | Stakes Level | Examples |
|------|-------------|----------|
| 1 | Low (< $50K, easily reversible) | Routine vendor selection, standard NDA |
| 2 | Medium ($50K-$500K, partially reversible) | Significant vendor contract, key hire |
| 3 | High ($500K-$5M, difficult to reverse) | Strategic partnership, acquisition |
| 4 | Critical (> $5M or existential) | Merger, major litigation, IPO |

**Step 1.2: Assess Reversibility**
- Can decision be undone? At what cost?
- What is the correction timeline if wrong?
- Are there interim checkpoints before full commitment?

**Step 1.3: Assess Time Constraints**
- What is the decision deadline?
- What is the cost of delay?
- Are there diminishing returns to additional information?

### Phase 2: Information Requirement Setting

**Step 2.1: Define Sufficiency Thresholds by Tier**
| Tier | Confidence Required | Validation Standard |
|------|--------------------|--------------------|
| 1 | 60% | Single source, face validity |
| 2 | 75% | Multiple sources, basic verification |
| 3 | 85% | Expert validation, documentary evidence |
| 4 | 95% | Independent verification, stress testing |

**Step 2.2: Map Current Information State**
- What do we know with high confidence?
- What do we believe but haven't verified?
- What are explicit knowledge gaps?

**Step 2.3: Calculate Gap to Threshold**
- Current confidence vs. required confidence
- Estimated effort to close gap
- Expected confidence improvement per unit effort

### Phase 3: Gather/Decide Assessment

**Step 3.1: Expected Value of Additional Information**
- If gap is small and closing cost is high → proceed
- If gap is large and closing cost is low → gather more
- If time constraint is binding → proceed with risk acknowledgment

**Step 3.2: Document Decision Basis**
- Explicit statement of information sufficiency assessment
- Acknowledged gaps and associated risks
- Contingency plans for gap-related surprises

---

## Cross-References

### Orchestrated By (Tier 3 MC Patterns)
- **MC19 (Epistemic Validation & Reconciliation)**: Primary orchestrator - determines validation depth
- **MC15 (Confidence Calibration)**: Calibrates confidence thresholds

### Related Patterns (Same Tier)
- **S2 (Information Gap Identification)**: Identifies what's unknown
- **S9 (Hierarchical Due Diligence)**: Prioritizes diligence efforts
- **BI3 (Context-Aware Risk Calibration)**: Risk tolerance informs sufficiency

### Downstream Applications
- Due diligence scope definition
- Decision documentation
- Stakeholder communication
- Post-decision review

---

## Metadata

**Pattern ID:** BI13
**Tier:** 2 (Behavioral Intelligence)
**Domain:** Decision Support / Epistemics
**Status:** Active - Map Derived
