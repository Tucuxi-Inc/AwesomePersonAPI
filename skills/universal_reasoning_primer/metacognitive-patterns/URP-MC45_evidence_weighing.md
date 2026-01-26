---
name: urp-mc45-evidence-weighing
description: Meta-cognitive pattern for evaluating the strength, relevance, and reliability of evidence to determine appropriate weight in reasoning and decisions.
tags:
- meta-cognitive
- epistemic
- evidence-evaluation
- source-reliability
- evidentiary-reasoning
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
- source-evaluation
- relevance-assessment
- strength-calibration
works_with:
- URP-MC6
- URP-MC43
- URP-MC39
co_occurs_with:
- URP-MC42
- URP-MC41
---

# URP-MC45: Evidence Weighing

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Evaluating evidence quality to determine appropriate weight
**Domain Independence:** Universal across all evidence-based reasoning
**Orchestration Role:** Calibrates belief updates and decisions to evidence quality

## Pattern Definition

### Trigger Condition
Situations involving:
- Multiple pieces of evidence of varying quality
- Need to evaluate claims based on supporting evidence
- Conflicting evidence requiring adjudication
- Making decisions based on incomplete information
- Assessing reliability of information sources

### Core Procedure

1. **Source Reliability Assessment**
   - Who/what is the source?
   - What's the track record of this source?
   - What expertise does the source have?
   - What biases might the source have?

2. **Evidence Relevance Evaluation**
   - Does this evidence bear directly on the question?
   - Is it about the specific issue or analogous?
   - What would this evidence prove/disprove?
   - How close is the match to the claim?

3. **Evidence Strength Assessment**
   - How strong is this evidence?
   - Is it conclusive, suggestive, or weak?
   - What's the sample size/replication/methodology?
   - Could this evidence arise even if claim is false?

4. **Aggregate Weighing**
   - How does this evidence combine with other evidence?
   - Do multiple independent sources converge?
   - Is evidence quantity substituting for quality?
   - What's the overall evidential picture?

5. **Weight Assignment**
   - Assign appropriate weight to this evidence
   - Adjust conclusions proportionally
   - Note evidence limitations
   - Identify what evidence would change assessment

### Expert Heuristic

> "Not all evidence is created equal. One well-designed study outweighs a hundred anecdotes. But even the best evidence only shifts probability—it doesn't create certainty. Weigh evidence by its ability to differentiate between truth and falsity."

## Evidence from Literature

### Example 1: Scientific Methodology
**Context:** Philosophy of science
**Evidence:** Evidence quality hierarchies (RCT > observational > anecdote) reflect evidential strength
**Insight:** There are principled grounds for differential weighting

### Example 2: Bayesian Reasoning
**Context:** Probabilistic reasoning research
**Evidence:** Likelihood ratios capture how much evidence should shift beliefs
**Insight:** Evidence weighing has normative foundations

### Example 3: Source Credibility
**Context:** Persuasion and communication research
**Evidence:** Source characteristics systematically affect (and should affect) evidence interpretation
**Insight:** Source evaluation is proper part of evidence weighing

### Example 4: Legal Evidence
**Context:** Rules of evidence
**Evidence:** Legal systems have evolved rules for evidence evaluation
**Insight:** Evidence weighing is socially institutionalized in high-stakes domains

## Decision Criteria

**Criterion 1: Source-Based Weighting**
- IF source is expert and unbiased, THEN high weight
- IF source is non-expert or potentially biased, THEN discount
- IF source track record is poor, THEN heavy discount
- Rationale: Source quality bounds evidence quality

**Criterion 2: Relevance-Based Weighting**
- IF evidence directly addresses claim, THEN high weight
- IF evidence is indirect or analogical, THEN lower weight
- IF evidence addresses different question, THEN very low weight
- Rationale: Relevance determines evidential bearing

**Criterion 3: Methodology-Based Weighting**
- IF methodology is strong, THEN high weight
- IF methodology has flaws, THEN discount for flaws
- IF methodology is unknown, THEN lower default weight
- Rationale: Method quality determines evidence reliability

**Criterion 4: Convergence Bonus**
- IF multiple independent sources converge, THEN increased confidence
- IF sources are not independent, THEN don't double-count
- Rationale: Independent convergence is strong evidence

## Contrast with Naive Approaches

**Naive Approach**: All evidence counts equally; more evidence = stronger case.
**Expert Approach**: Weight evidence by quality; quality can trump quantity.

**Naive Approach**: Evidence that supports belief counts; evidence against is flawed.
**Expert Approach**: Evaluate evidence by quality regardless of direction.

**Naive Approach**: Vivid, concrete evidence is most convincing.
**Expert Approach**: Evaluate evidence by relevance and methodology, not vividness.

**Naive Approach**: Trust or distrust sources wholesale.
**Expert Approach**: Evaluate evidence from source with appropriate source discount.

## Integration with Pattern Tiers

### As Orchestration Operator

URP-MC45 functions as an **evidential weight calculator**:

```
INPUT: Evidence + claims + context
  ↓
URP-MC45: Weigh evidence
  ↓
EVALUATION:
  - Source reliability
  - Relevance
  - Strength/methodology
  - Aggregate pattern
  ↓
OUTPUT: Evidence weights + confidence adjustment + limitations noted
```

### Composition with Other MC Patterns

**Foundation Relationships:**
- **URP-MC45 + URP-MC6**: Source monitoring provides reliability input
- **URP-MC45 → URP-MC43**: Evidence weights determine belief revision magnitude
- **URP-MC45 + URP-MC39**: Evidence quality affects uncertainty levels
- **URP-MC45 + URP-MC42**: Inference quality depends on evidence quality

**Activation Patterns:**
- Evidence receipt triggers URP-MC45
- URP-MC45 outputs feed URP-MC43 (belief revision)
- URP-MC45 informs URP-MC24 (confidence calibration)

## Expertise Level Indicators

| Level | URP-MC45 Application |
|-------|-----------------|
| **Novice** | Equal weighting; influenced by vividness; no source evaluation |
| **Competent** | Some quality awareness; can identify obviously weak evidence |
| **Expert** | Systematic evaluation; appropriate differential weighting |
| **Master** | Intuitive quality assessment; sophisticated methodology evaluation |
| **Sage** | Teaches evidence evaluation; develops evidence standards |

## Theoretical Foundations

- **Bayesian Epistemology**: Evidence as likelihood ratios (Howson & Urbach, 2006)
- **Evidence Hierarchies**: Quality gradations in science and medicine
- **Source Credibility**: Factors affecting source reliability (Pornpitakpan, 2004)
- **Argumentation Theory**: Evidence evaluation in reasoning (Walton, 1996)

---

## Metadata

```yaml
pattern_id: URP-MC45
pattern_name: Evidence Weighing
tier: 3 (Meta-Cognitive)
core_question: "How strong, relevant, and reliable is this evidence?"
domain_independence: Universal
transfer_rate: ">90% (evidence evaluation principles transfer; specific standards vary)"
extraction_confidence: 0.90
orchestration_function: evidential_weight_calculation
related_patterns:
  - URP-MC6: Source Monitoring
  - URP-MC43: Belief Revision
  - URP-MC39: Uncertainty Tracking
```
