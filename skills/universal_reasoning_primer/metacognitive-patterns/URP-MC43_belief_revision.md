---
name: urp-mc43-belief-revision
description: Meta-cognitive pattern for updating beliefs appropriately in response to new evidence, including overcoming resistance to change and avoiding both over-reaction and under-reaction.
tags:
- meta-cognitive
- epistemic
- belief-update
- evidence-integration
- bayesian-thinking
version: '1.0'
confidence_level: HIGH
category: meta_cognitive
validated_by: Literature Synthesis
validated_date: '2025-12-30'
skill_tier: strategic
pattern_tier: 3
mentoring_priority: 9
validation_type: literature_synthesis
source_type: academic_research
source_skills:
- evidence-evaluation
- update-magnitude
- prior-management
works_with:
- URP-MC44
- URP-MC45
- URP-MC39
co_occurs_with:
- URP-MC6
- URP-MC41
---

# URP-MC43: Belief Revision

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Updating beliefs appropriately based on new evidence
**Domain Independence:** Universal across all learning and reasoning
**Orchestration Role:** Maintains accurate world model by integrating new information

## Pattern Definition

### Trigger Condition
Situations involving:
- Receiving information that conflicts with current beliefs
- Accumulating evidence that should shift probabilities
- Recognizing that previous beliefs were wrong
- Integrating new data into existing knowledge
- Others challenging your beliefs with evidence

### Core Procedure

1. **Evidence Assessment**
   - What new information have I received?
   - How reliable is the source?
   - How strong is this evidence?
   - Does it directly address my belief?

2. **Prior Examination**
   - What do I currently believe?
   - How confident am I in current belief?
   - What's the basis for current belief?
   - How strongly should I hold prior?

3. **Update Calculation**
   - How much should this evidence shift my belief?
   - What's the likelihood ratio of this evidence?
   - Am I updating too much or too little?
   - What would a calibrated person conclude?

4. **Resistance Recognition**
   - Am I resisting this update for good reasons?
   - Is this motivated reasoning?
   - Am I anchored to my prior excessively?
   - Would I update if the evidence supported my belief?

5. **Update Execution**
   - Revise belief to appropriate level
   - Update all dependent beliefs
   - Note uncertainty in new position
   - Remain open to further revision

### Expert Heuristic

> "Your beliefs should be proportional to evidence, not to how long you've held them or how much you've invested in them. The goal is accuracy, not consistency. If you've never changed your mind about something important, you should be worried."

## Evidence from Literature

### Example 1: Bayesian Reasoning
**Context:** Rational belief update research
**Evidence:** Optimal belief update follows Bayes' theorem; people deviate systematically
**Insight:** There's a normative standard for belief revision

### Example 2: Confirmation Bias
**Context:** Cognitive bias research
**Evidence:** People under-weight evidence against current beliefs
**Insight:** Belief revision is biased toward maintenance

### Example 3: Belief Perseverance
**Context:** Social psychology research
**Evidence:** Beliefs persist even after evidential basis is discredited
**Insight:** Belief revision requires active effort

### Example 4: Superforecasters
**Context:** Tetlock's Good Judgment Project
**Evidence:** Best forecasters update incrementally in response to evidence
**Insight:** Calibrated updating is learnable

## Decision Criteria

**Criterion 1: Update Magnitude**
- IF evidence is strong and direct, THEN large update
- IF evidence is weak or indirect, THEN small update
- IF evidence is ambiguous, THEN minimal update
- Rationale: Update size should match evidence strength

**Criterion 2: Prior Strength Consideration**
- IF prior is well-founded, THEN require stronger evidence to shift
- IF prior is weakly held, THEN update more readily
- Rationale: Strong priors appropriately resist weak evidence

**Criterion 3: Motivated Reasoning Check**
- IF resisting update that would be accepted if direction reversed, THEN override resistance
- IF update threatens identity or investments, THEN be especially vigilant
- Rationale: Motivation biases update; correct for it

**Criterion 4: Cascading Updates**
- IF belief changes, THEN update all dependent beliefs
- IF update has implications, THEN trace them
- Rationale: Beliefs form networks; update should propagate

## Contrast with Naive Approaches

**Naive Approach**: Stick with beliefs; resist change; seek confirming evidence.
**Expert Approach**: Update proportionally to evidence; seek disconfirming evidence.

**Naive Approach**: Wholesale belief flip or complete maintenance.
**Expert Approach**: Incremental proportional update.

**Naive Approach**: Evaluate evidence by whether it supports current belief.
**Expert Approach**: Evaluate evidence by source quality and relevance.

**Naive Approach**: Change is failure; consistency is virtue.
**Expert Approach**: Appropriate change is learning; inappropriate consistency is error.

## Integration with Pattern Tiers

### As Orchestration Operator

URP-MC43 functions as a **belief update engine**:

```
INPUT: Current belief + new evidence + source reliability
  ↓
URP-MC43: Calculate belief revision
  ↓
EVALUATION:
  - Evidence strength
  - Prior strength
  - Update magnitude
  - Resistance check
  ↓
OUTPUT: Revised belief + confidence + change rationale + cascade effects
```

### Composition with Other MC Patterns

**Foundation Relationships:**
- **URP-MC43 + URP-MC44**: Contradictions require revision to resolve
- **URP-MC43 + URP-MC45**: Evidence weighing determines update magnitude
- **URP-MC43 + URP-MC6**: Source monitoring affects evidence reliability
- **URP-MC43 + URP-MC39**: Revision affects uncertainty tracking

**Activation Patterns:**
- New evidence triggers URP-MC43
- URP-MC44 (contradiction detection) triggers URP-MC43
- URP-MC43 outputs update URP-MC39 (uncertainty tracking)

## Expertise Level Indicators

| Level | URP-MC43 Application |
|-------|-----------------|
| **Novice** | Strong resistance; confirmation bias; rarely updates |
| **Competent** | Can update when evidence is overwhelming |
| **Expert** | Proportional updating; recognizes motivated reasoning |
| **Master** | Calibrated Bayesian updating; seeks disconfirmation |
| **Sage** | Teaches belief revision; designs evidence-responsive systems |

## Theoretical Foundations

- **Bayesian Epistemology**: Normative belief update (Jeffrey, 1965)
- **Confirmation Bias**: Systematic under-updating (Nickerson, 1998)
- **Belief Perseverance**: Resistance to revision (Ross et al., 1975)
- **Superforecasting**: Calibrated updating in practice (Tetlock, 2015)

---

## Metadata

```yaml
pattern_id: URP-MC43
pattern_name: Belief Revision
tier: 3 (Meta-Cognitive)
core_question: "How much should this new evidence change what I believe?"
domain_independence: Universal
transfer_rate: ">95% (belief revision applies everywhere)"
extraction_confidence: 0.91
orchestration_function: belief_update_engine
related_patterns:
  - URP-MC44: Contradiction Detection
  - URP-MC45: Evidence Weighing
  - URP-MC6: Source Monitoring
```
