---
name: urp-mc3-error-detection
description: Meta-cognitive pattern for recognizing mistakes, inconsistencies, and anomalies in one's own reasoning, outputs, or processes before they propagate downstream.
tags:
- meta-cognitive
- monitoring
- error-detection
- quality-control
- self-correction
version: '1.0'
confidence_level: HIGH
category: meta_cognitive
validated_by: Literature Synthesis
validated_date: '2025-12-30'
skill_tier: foundational
pattern_tier: 3
mentoring_priority: 9
validation_type: literature_synthesis
source_type: academic_research
source_skills:
- consistency-checking
- output-verification
- anomaly-recognition
works_with:
- URP-MC1
- URP-MC2
- URP-MC9
co_occurs_with:
- URP-MC4
- URP-MC19
---

# URP-MC3: Error Detection

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Recognizing mistakes and inconsistencies in own cognition
**Domain Independence:** Universal across reasoning, production, and decision-making
**Orchestration Role:** Triggers correction, verification, and quality checks before output

## Pattern Definition

### Trigger Condition
Situations involving:
- Any cognitive production (reasoning, calculation, writing)
- Multi-step processes where errors can compound
- High-stakes outputs where errors have significant consequences
- Novel or unfamiliar tasks with higher error likelihood
- Integration of multiple sources where inconsistencies may arise

### Core Procedure

1. **Establish Error Profiles**
   - What types of errors am I prone to in this domain?
   - What are the common failure modes for this task type?
   - Where have I made mistakes before in similar situations?
   - What conditions increase my error rate?

2. **Active Error Scanning**
   - Does this output make sense given the inputs?
   - Are there internal inconsistencies in my reasoning?
   - Does this violate any known constraints or principles?
   - Would I expect this result, or is it surprising?

3. **Anomaly Recognition**
   - Is anything "off" about this result?
   - Does my intuition match my explicit reasoning?
   - Are there warning signs I should attend to?
   - Does this fit patterns I know to be correct?

4. **Verification Procedures**
   - Can I check this through a different method?
   - Does working backward confirm forward work?
   - Do the units/types/formats align properly?
   - Does this pass sanity checks?

5. **Error Classification**
   - Is this a slip (execution error) or mistake (planning error)?
   - Is this systematic (will recur) or random?
   - Is this local (affects one element) or global (affects structure)?
   - What's the likely downstream impact?

### Expert Heuristic

> "The feeling that something is slightly 'off' is often a valid signal—trust it enough to investigate. Experts recognize errors often through pattern violation rather than explicit checking; the result 'feels wrong' before analysis confirms it."

## Evidence from Literature

### Example 1: Expert Error Detection
**Context:** Reason (1990) human error research
**Evidence:** Experts develop strong expectations that make anomalies salient; novices lack the baseline to notice deviations
**Insight:** Error detection depends on having accurate expectations

### Example 2: Slip vs. Mistake Distinction
**Context:** Norman (1981) categorization of human errors
**Evidence:** Slips (execution failures) and mistakes (planning failures) require different detection and correction strategies
**Insight:** Error detection must distinguish error types for effective repair

### Example 3: Metacognitive Error Monitoring
**Context:** Yeung & Summerfield (2012) cognitive control studies
**Evidence:** Error monitoring involves conflict detection systems that trigger increased attention
**Insight:** Error detection is partially automatic but benefits from strategic enhancement

## Decision Criteria

**Criterion 1: Expectation Violation**
- IF result violates prior expectation, THEN investigate
- IF result is exactly as expected but stakes are high, THEN verify anyway
- Rationale: Unexpected results are candidates for errors

**Criterion 2: Internal Consistency**
- IF inconsistency found, THEN at least one element is wrong
- IF perfect consistency but derivation was complex, THEN check derivation
- Rationale: Internal contradictions guarantee error existence

**Criterion 3: Cross-Check Agreement**
- IF different methods give different results, THEN investigate discrepancy
- IF methods agree, THEN increase confidence
- Rationale: Method triangulation reveals errors

**Criterion 4: Intuition Mismatch**
- IF formal result contradicts intuition, THEN check both
- IF intuition and formal agree, THEN higher confidence (but not certainty)
- Rationale: Intuition captures patterns learned from experience

## Contrast with Naive Approaches

**Naive Approach**: Assume outputs are correct once produced; focus only on generation.
**Expert Approach**: Treat every output as potentially erroneous until verified.

**Naive Approach**: Look for errors only when something obviously goes wrong.
**Expert Approach**: Actively scan for errors throughout process, especially at high-risk points.

**Naive Approach**: Check work by repeating the same process.
**Expert Approach**: Check work through independent methods that would reveal different error types.

**Naive Approach**: Trust the process; if procedure was followed, result must be correct.
**Expert Approach**: Recognize that correct procedures can be executed incorrectly; verify outcomes.

## Integration with Pattern Tiers

### As Orchestration Operator

URP-MC3 functions as a **quality assurance operator**:

```
INPUT: Cognitive output + quality criteria
  ↓
URP-MC3: Scan for errors
  ↓
EVALUATION:
  - Consistency check (internal coherence)
  - Expectation check (matches predictions)
  - Constraint check (satisfies requirements)
  - Intuition check (feels right)
  ↓
OUTPUT: Accept | Investigate | Repair | Reject
```

### Composition with Other MC Patterns

**Foundation Relationships:**
- **URP-MC3 + URP-MC2**: Error detection applied to comprehension outputs
- **URP-MC3 → URP-MC9**: Detected errors trigger correction procedures
- **URP-MC3 + URP-MC4**: Prediction errors feed feeling-of-knowing calibration
- **URP-MC3 + URP-MC19**: Error patterns inform future task approach

**Activation Patterns:**
- URP-MC3 activates URP-MC9 (error correction) when errors detected
- URP-MC3 informs URP-MC24 (confidence calibration) about reliability
- URP-MC3 feeds URP-MC20 (post-task reflection) with error data

## Expertise Level Indicators

| Level | URP-MC3 Application |
|-------|-----------------|
| **Novice** | Detects only obvious errors; misses subtle problems; errors propagate |
| **Competent** | Catches common error types; uses basic verification; misses novel errors |
| **Expert** | Strong error intuition; multiple verification methods; catches subtle issues |
| **Master** | Errors feel immediately wrong; automated quality sensing; rarely misses |
| **Sage** | Anticipates error-prone areas; designs error-resistant processes; teaches error detection |

## Theoretical Foundations

- **Human Error Theory**: Classification and detection of human errors (Reason, 1990)
- **Error-Related Negativity**: Neural signatures of error detection (Gehring et al., 1993)
- **Conflict Monitoring**: Role of anterior cingulate in error detection (Botvinick et al., 2001)
- **Signal Detection Theory**: Tradeoffs in error detection sensitivity and specificity (Green & Swets, 1966)

---

## Metadata

```yaml
pattern_id: URP-MC3
pattern_name: Error Detection
tier: 3 (Meta-Cognitive)
core_question: "Is there something wrong here that I should catch before it matters?"
domain_independence: Universal
transfer_rate: ">90% (applies across all cognitive production)"
extraction_confidence: 0.91
orchestration_function: quality_assurance_and_correction_triggering
related_patterns:
  - URP-MC2: Comprehension Monitoring
  - URP-MC9: Error Correction
  - URP-MC24: Confidence Calibration
```
