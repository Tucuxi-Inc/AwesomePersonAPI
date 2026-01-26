---
name: urp-mc9-error-correction
description: Meta-cognitive pattern for implementing appropriate fixes once errors are detected, selecting correction strategies based on error type, severity, and downstream impact.
tags:
- meta-cognitive
- control
- error-repair
- correction-strategies
- quality-recovery
version: '1.0'
confidence_level: HIGH
category: meta_cognitive
validated_by: Literature Synthesis
validated_date: '2025-12-30'
skill_tier: applied
pattern_tier: 3
mentoring_priority: 8
validation_type: literature_synthesis
source_type: academic_research
source_skills:
- S-error-classification
- S-repair-procedures
works_with:
- URP-MC3
- URP-MC8
- URP-MC19
co_occurs_with:
- URP-MC1
- URP-MC24
---

# URP-MC9: Error Correction

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Implementing appropriate repairs after error detection
**Domain Independence:** Universal across all domains with correctness requirements
**Orchestration Role:** Selects and executes correction strategies matched to error type

## Pattern Definition

### Trigger Condition
Situations involving:
- Error detected by URP-MC3 (error detection)
- Output failing quality check
- Inconsistency identified in reasoning
- Feedback indicating mistake
- Self-test revealing flaw

### Core Procedure

1. **Error Classification**
   - Is this a slip (execution error) or mistake (planning error)?
   - Is the error local (one element) or global (whole structure)?
   - Is this systematic (will recur) or random?
   - What's the root cause?

2. **Impact Assessment**
   - What downstream effects has this error caused?
   - What work depends on the erroneous element?
   - If I fix this, what else must change?
   - Is partial fix acceptable or must correction be complete?

3. **Correction Strategy Selection**
   - Local fix: correct the specific error
   - Backtrack: undo to before error occurred
   - Restart: begin again with corrected approach
   - Patch: work around error without full correction
   - Accept: acknowledge error but proceed (if low impact)

4. **Correction Implementation**
   - Execute chosen correction strategy
   - Verify error is actually fixed
   - Check for introduced errors from correction
   - Update any dependent elements

5. **Recurrence Prevention**
   - What allowed this error to occur?
   - What check would have caught it earlier?
   - Should I modify process to prevent similar errors?

### Expert Heuristic

> "The goal isn't just to fix this error but to fix it in a way that doesn't break something else and ideally prevents the same error from recurring. Sometimes the right fix is a process fix, not a content fix."

## Evidence from Literature

### Example 1: Error Classification and Repair
**Context:** Reason (1990) human error research
**Evidence:** Slips and mistakes require different correction strategies; misclassification leads to ineffective repair
**Insight:** Error classification precedes effective correction

### Example 2: Debugging Expertise
**Context:** Gugerty & Olson (1986) debugging studies
**Evidence:** Expert programmers localize errors more accurately and choose more effective fixes
**Insight:** Correction expertise includes diagnosis, not just repair

### Example 3: Self-Correction in Writing
**Context:** Hayes & Flower (1986) revision studies
**Evidence:** Expert writers distinguish surface errors from meaning errors and prioritize accordingly
**Insight:** Error severity determines correction priority and strategy

## Integration with Pattern Tiers

### As Orchestration Operator

URP-MC9 functions as a **correction strategy selector**:

```
INPUT: Detected error + error classification + impact assessment
  ↓
URP-MC9: Select correction strategy
  ↓
EVALUATION:
  - Error type (slip/mistake, local/global)
  - Correction cost vs. error cost
  - Downstream dependencies
  - Recurrence risk
  ↓
OUTPUT: Local fix | Backtrack | Restart | Patch | Accept
  ↓
VERIFY: Error resolved + no new errors introduced
```

### Composition with Other MC Patterns

**Foundation Relationships:**
- **URP-MC3 → URP-MC9**: Error detection triggers correction
- **URP-MC9 + URP-MC8**: Major errors may require strategy adjustment, not just correction
- **URP-MC9 → URP-MC19**: Corrections inform post-task reflection
- **URP-MC9 + URP-MC24**: Correction success affects confidence calibration

**Activation Patterns:**
- URP-MC3 (error detection) triggers URP-MC9
- URP-MC9 may trigger URP-MC8 (strategy adjustment) if error is systemic
- URP-MC9 feeds URP-MC19 (reflection) with error patterns

## Decision Criteria

**Criterion 1: Error Severity**
- IF error is minor and local, THEN local fix
- IF error propagated widely, THEN consider backtrack or restart
- Rationale: Match correction scope to error scope

**Criterion 2: Correction Cost**
- IF correction is more expensive than impact, THEN consider accept or patch
- IF correction is straightforward, THEN fix even minor errors
- Rationale: Correction has costs too

**Criterion 3: Error Type**
- IF slip (execution error), THEN correct output directly
- IF mistake (planning error), THEN correct plan and re-execute
- Rationale: Fixing symptoms of mistakes leaves root cause

**Criterion 4: Downstream Impact**
- IF many elements depend on error, THEN careful cascade correction
- IF error is isolated, THEN direct correction sufficient
- Rationale: Corrections can break dependencies

## Contrast with Naive Approaches

**Naive Approach**: Fix the symptom without understanding the cause.
**Expert Approach**: Diagnose root cause; fix in a way that prevents recurrence.

**Naive Approach**: Treat all errors equally—same correction effort regardless of impact.
**Expert Approach**: Prioritize corrections by impact; major errors first.

**Naive Approach**: Fix errors in place without checking dependencies.
**Expert Approach**: Trace dependencies; update everything affected by correction.

**Naive Approach**: Correction complete when error is gone.
**Expert Approach**: Verify correction didn't introduce new errors; check broader consistency.

## Expertise Level Indicators

| Level | URP-MC9 Application |
|-------|-----------------|
| **Novice** | Fixes symptoms; breaks other things; same error recurs |
| **Competent** | Can fix common error types; occasionally misdiagnoses; checks obvious dependencies |
| **Expert** | Accurate diagnosis; matched corrections; dependency awareness; prevention thinking |
| **Master** | Efficient minimal fixes; no introduced errors; systematic prevention |
| **Sage** | Designs error-resistant processes; teaches correction strategies |

## Theoretical Foundations

- **Human Error Theory**: Error classification guiding repair (Reason, 1990)
- **Debugging Research**: Expert diagnosis and correction (Gugerty & Olson, 1986)
- **Revision Studies**: Prioritizing and implementing corrections in writing (Hayes, 2004)
- **Error Management**: Distinction between error prevention and error management (Frese & Keith, 2015)

---

## Metadata

```yaml
pattern_id: URP-MC9
pattern_name: Error Correction
tier: 3 (Meta-Cognitive)
core_question: "What's the right way to fix this error without breaking something else?"
domain_independence: Universal
transfer_rate: ">85% (correction strategies vary somewhat by domain)"
extraction_confidence: 0.88
orchestration_function: correction_strategy_selection_and_implementation
related_patterns:
  - URP-MC3: Error Detection
  - URP-MC8: Strategy Adjustment
  - URP-MC19: Post-Task Reflection
```
