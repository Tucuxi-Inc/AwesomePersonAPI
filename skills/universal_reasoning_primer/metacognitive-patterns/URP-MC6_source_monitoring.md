---
name: urp-mc6-source-monitoring
description: Meta-cognitive pattern for tracking the origin of information—distinguishing between what was perceived, inferred, imagined, told, or read to maintain epistemic accuracy.
tags:
- meta-cognitive
- monitoring
- source-attribution
- epistemic-hygiene
- memory-accuracy
version: '1.0'
confidence_level: HIGH
category: meta_cognitive
validated_by: Literature Synthesis
validated_date: '2025-12-30'
skill_tier: foundational
pattern_tier: 3
mentoring_priority: 8
validation_type: literature_synthesis
source_type: academic_research
source_skills:
- evidence-tracking
- attribution-maintenance
- inference-marking
works_with:
- URP-MC24
- URP-MC39
- URP-MC40
co_occurs_with:
- URP-MC3
- URP-MC41
---

# URP-MC6: Source Monitoring

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Tracking and distinguishing origins of knowledge and beliefs
**Domain Independence:** Universal across all knowledge-dependent contexts
**Orchestration Role:** Maintains epistemic accuracy by preventing source confusion and false confidence

## Pattern Definition

### Trigger Condition
Situations involving:
- Recalling information without clear origin
- Making claims that require evidence attribution
- Integrating information from multiple sources
- Distinguishing what was observed vs. inferred
- Evaluating reliability of recalled information
- Preventing spread of misinformation

### Core Procedure

1. **Source Classification**
   - Did I perceive this directly or hear/read it?
   - Did I reason to this or was it stated?
   - Is this my inference or someone else's claim?
   - Is this from memory or current observation?

2. **Source Quality Assessment**
   - How reliable was the original source?
   - Was the source in position to know?
   - Does the source have relevant expertise?
   - Does the source have potential biases?

3. **Transmission Chain Tracking**
   - How many steps from original source?
   - What transformations might have occurred?
   - Is this primary or secondary/tertiary?
   - What might have been lost or added in transmission?

4. **Reality Monitoring**
   - Did this actually happen or did I imagine it?
   - Am I remembering an event or thinking about an event?
   - Did I actually do this or plan to do it?
   - Is this memory or constructed narrative?

5. **Confidence Adjustment**
   - Adjust confidence by source reliability
   - Flag uncertain sources explicitly
   - Distinguish evidence-based vs. inference-based beliefs
   - Mark tentative conclusions clearly

### Expert Heuristic

> "The question is never just 'what do I believe?' but 'why do I believe it and how did I come to believe it?' Knowledge without traceable source is belief dressed as knowledge."

## Evidence from Literature

### Example 1: Source Monitoring Framework
**Context:** Johnson et al. (1993) source monitoring research
**Evidence:** People frequently misattribute sources—confusing imagined with perceived, or one speaker with another
**Insight:** Source information is stored separately from content and can be lost or confused

### Example 2: Reality Monitoring
**Context:** Johnson & Raye (1981) reality monitoring studies
**Evidence:** Internally generated events (imagined) differ from externally derived events (perceived) but can be confused
**Insight:** Need active discrimination between internal and external sources

### Example 3: Eyewitness Memory
**Context:** Loftus et al. (1978) misinformation effect research
**Evidence:** Post-event information can be misattributed to original event, creating false memories
**Insight:** Sources can be confused across time, making source monitoring crucial

## Decision Criteria

**Criterion 1: Claim Confidence**
- IF source is direct perception, THEN higher confidence in content
- IF source is inference or hearsay, THEN lower confidence and flag
- Rationale: Source reliability bounds content confidence

**Criterion 2: Attribution Requirement**
- IF making external claims, THEN source must be traceable
- IF source is unclear, THEN preface with uncertainty
- Rationale: Claims require support; uncertainty should be transmitted

**Criterion 3: Source Conflict Resolution**
- IF multiple sources disagree, THEN evaluate source quality
- IF cannot evaluate sources, THEN maintain multiple hypotheses
- Rationale: Source quality determines which version to trust

**Criterion 4: Memory vs. Inference**
- IF unsure whether remembered or inferred, THEN treat as inference
- IF feels like memory but details are suspect, THEN verify if possible
- Rationale: Inferences are less reliable than genuine memories

## Contrast with Naive Approaches

**Naive Approach**: Treat all beliefs equally; "I know this" without tracking why.
**Expert Approach**: Maintain source attribution; different sources warrant different confidence.

**Naive Approach**: Assume memories are accurate recordings of events.
**Expert Approach**: Recognize memories are reconstructions subject to source confusion.

**Naive Approach**: Pass along information without noting source.
**Expert Approach**: Preserve and transmit source information with content.

**Naive Approach**: If I believe it strongly, it must be well-sourced.
**Expert Approach**: Belief strength and source quality are independent; check both.

## Integration with Pattern Tiers

### As Orchestration Operator

URP-MC6 functions as an **epistemic provenance tracker**:

```
INPUT: Belief or claim + need for accuracy/attribution
  ↓
URP-MC6: Assess source
  ↓
EVALUATION:
  - Source type (perception/inference/report/imagination)
  - Source reliability
  - Transmission chain
  - Confidence warranted
  ↓
OUTPUT: Confidence level | Attribution | Uncertainty flag | Verification need
```

### Composition with Other MC Patterns

**Foundation Relationships:**
- **URP-MC6 + URP-MC24**: Source quality bounds appropriate confidence
- **URP-MC6 + URP-MC39**: Source monitoring feeds uncertainty tracking
- **URP-MC6 + URP-MC40**: Sources define what we actually know vs. believe
- **URP-MC6 + URP-MC3**: Source confusion is a type of error to detect

**Activation Patterns:**
- URP-MC6 informs URP-MC24 (confidence calibration) about evidence basis
- URP-MC6 triggers URP-MC41 (assumption surfacing) when sources are weak
- URP-MC6 feeds URP-MC40 (knowledge boundaries) about what is truly known

## Expertise Level Indicators

| Level | URP-MC6 Application |
|-------|-----------------|
| **Novice** | No source tracking; presents inference as fact; confident without basis |
| **Competent** | Basic source awareness; distinguishes fact vs. opinion; some attribution |
| **Expert** | Active source monitoring; adjusts confidence by source; flags uncertainty |
| **Master** | Automatic source tracking; transmission chain awareness; epistemic hygiene |
| **Sage** | Teaches epistemic practices; designs systems for source preservation |

## Theoretical Foundations

- **Source Monitoring Framework**: Attributing memories to origins (Johnson et al., 1993)
- **Reality Monitoring**: Distinguishing internal from external sources (Johnson & Raye, 1981)
- **Misinformation Effect**: Post-event information confusion (Loftus, 2005)
- **Epistemic Vigilance**: Evaluating communicated information (Sperber et al., 2010)

---

## Metadata

```yaml
pattern_id: URP-MC6
pattern_name: Source Monitoring
tier: 3 (Meta-Cognitive)
core_question: "Where did this belief come from and how reliable is that source?"
domain_independence: Universal
transfer_rate: ">95% (applies to all knowledge management)"
extraction_confidence: 0.90
orchestration_function: epistemic_provenance_tracking
related_patterns:
  - URP-MC24: Confidence Calibration
  - URP-MC39: Uncertainty Tracking
  - URP-MC40: Knowledge Boundary Awareness
```
