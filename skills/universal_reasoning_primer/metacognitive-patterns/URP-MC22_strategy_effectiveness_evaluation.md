---
name: urp-mc22-strategy-effectiveness-evaluation
description: Meta-cognitive pattern for assessing which strategies, methods, and approaches work well in which contexts to build an accurate mental model of method effectiveness.
tags:
- meta-cognitive
- evaluation
- strategy-assessment
- method-calibration
- effectiveness-tracking
version: '1.0'
confidence_level: HIGH
category: meta_cognitive
validated_by: Literature Synthesis
validated_date: '2025-12-30'
skill_tier: strategic
pattern_tier: 3
mentoring_priority: 8
validation_type: literature_synthesis
source_type: academic_research
source_skills:
- outcome-attribution
- method-tracking
- context-sensitivity
works_with:
- URP-MC19
- URP-MC20
- URP-MC34
co_occurs_with:
- URP-MC21
- URP-MC8
---

# URP-MC22: Strategy Effectiveness Evaluation

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Building accurate models of which methods work when
**Domain Independence:** Universal across all strategic behavior
**Orchestration Role:** Calibrates strategy selection by tracking what works in which contexts

## Pattern Definition

### Trigger Condition
Situations involving:
- Completed tasks where strategy effectiveness can be assessed
- Need to choose among strategies for future tasks
- Building expertise in a domain
- Helping others select strategies
- Revising beliefs about method effectiveness

### Core Procedure

1. **Strategy Identification**
   - What strategy did I use?
   - What were its key features?
   - What alternatives existed?
   - Why did I choose this one?

2. **Outcome Attribution**
   - How much did strategy contribute to outcome?
   - What other factors affected outcome?
   - Would a different strategy have done better?
   - Was this a fair test of the strategy?

3. **Context Mapping**
   - What task features were present?
   - What resource conditions existed?
   - What personal factors were relevant?
   - What environmental conditions applied?

4. **Effectiveness Updating**
   - How does this change my view of strategy effectiveness?
   - In what contexts does this strategy excel?
   - In what contexts does it struggle?
   - How confident am I in this assessment?

5. **Strategy-Context Model Building**
   - Which strategies work best in which contexts?
   - What's my current best strategy for each context type?
   - Where do I need more data?
   - What experiments would be informative?

### Expert Heuristic

> "A strategy is not good or bad in the abstract—it's good or bad in context. The expert knows not just many strategies but knows which strategy fits which situation."

## Evidence from Literature

### Example 1: Strategy Selection Research
**Context:** Siegler (1996) adaptive strategy choice
**Evidence:** Effective performers track strategy effectiveness by problem type
**Insight:** Strategy effectiveness is context-dependent

### Example 2: Metacognitive Calibration
**Context:** Dunlosky & Metcalfe (2009) metacognition research
**Evidence:** Accurate calibration of study strategies improves learning efficiency
**Insight:** Strategy effectiveness beliefs must be calibrated against outcomes

### Example 3: Learning Strategy Research
**Context:** Dunlosky et al. (2013) learning strategy effectiveness
**Evidence:** Students often use ineffective strategies due to miscalibrated beliefs
**Insight:** Strategy effectiveness evaluation is often poor and can be improved

## Decision Criteria

**Criterion 1: Attribution Accuracy**
- IF outcome clearly due to strategy, THEN strong update to effectiveness belief
- IF outcome due to multiple factors, THEN proportional attribution
- IF outcome due to luck, THEN minimal update
- Rationale: Updates should reflect actual strategy contribution

**Criterion 2: Context Specificity**
- IF strategy worked in narrow context, THEN update for that context
- IF strategy worked across contexts, THEN update general effectiveness
- Rationale: Effectiveness is often context-specific

**Criterion 3: Sample Size**
- IF many observations, THEN confident estimate
- IF few observations, THEN tentative estimate
- Rationale: Confidence should match evidence

**Criterion 4: Recency**
- IF recent and relevant, THEN weight more heavily
- IF old or context has changed, THEN weight less
- Rationale: Effectiveness may change over time

## Contrast with Naive Approaches

**Naive Approach**: Judge strategy by most recent outcome.
**Expert Approach**: Aggregate across outcomes, weighting by attribution clarity.

**Naive Approach**: Strategy either works or doesn't.
**Expert Approach**: Strategy effectiveness is context-dependent; map context-effectiveness relationship.

**Naive Approach**: Stick with strategies that worked; abandon those that failed.
**Expert Approach**: Understand WHY they worked/failed; apply in appropriate contexts.

**Naive Approach**: Trust intuition about what works.
**Expert Approach**: Track actual outcomes; update beliefs based on evidence.

## Integration with Pattern Tiers

### As Orchestration Operator

URP-MC22 functions as a **strategy calibration system**:

```
INPUT: Strategy used + outcomes + context + attribution
  ↓
URP-MC22: Evaluate strategy effectiveness
  ↓
EVALUATION:
  - Strategy-outcome attribution
  - Context mapping
  - Effectiveness update
  - Context-strategy model refinement
  ↓
OUTPUT: Updated effectiveness beliefs + context-strategy mappings
```

### Composition with Other MC Patterns

**Foundation Relationships:**
- **URP-MC19 → URP-MC22**: Outcome assessment provides data for strategy evaluation
- **URP-MC20 → URP-MC22**: Reflection includes strategy effectiveness analysis
- **URP-MC22 → URP-MC34**: Effectiveness beliefs drive future strategy selection
- **URP-MC22 → URP-MC8**: Effectiveness data drives strategy adjustment

**Activation Patterns:**
- URP-MC19 (outcome assessment) feeds URP-MC22
- URP-MC22 outputs inform URP-MC34 (strategy selection) beliefs
- URP-MC22 updates inform URP-MC16 (approach selection)

## Expertise Level Indicators

| Level | URP-MC22 Application |
|-------|-----------------|
| **Novice** | No tracking; uses preferred strategies regardless; recency bias |
| **Competent** | Some effectiveness awareness; basic context sensitivity |
| **Expert** | Systematic tracking; context-strategy mapping; calibrated beliefs |
| **Master** | Rich mental models; accurate prediction; knows evidence limits |
| **Sage** | Contributes to strategy knowledge; teaches strategy evaluation |

## Theoretical Foundations

- **Adaptive Strategy Choice**: Learning strategy effectiveness by context (Siegler, 1996)
- **Metacognitive Calibration**: Aligning beliefs with performance (Dunlosky & Metcalfe, 2009)
- **Attribution Theory**: Understanding causes of outcomes (Weiner, 1985)
- **Bayesian Updating**: Revising beliefs based on evidence (Griffiths et al., 2008)

---

## Metadata

```yaml
pattern_id: URP-MC22
pattern_name: Strategy Effectiveness Evaluation
tier: 3 (Meta-Cognitive)
core_question: "Which strategies actually work best in which contexts?"
domain_independence: Universal
transfer_rate: ">85% (evaluation process transfers; strategy content varies)"
extraction_confidence: 0.87
orchestration_function: strategy_calibration
related_patterns:
  - URP-MC19: Outcome Assessment
  - URP-MC34: Strategy Selection
  - URP-MC8: Strategy Adjustment
```
