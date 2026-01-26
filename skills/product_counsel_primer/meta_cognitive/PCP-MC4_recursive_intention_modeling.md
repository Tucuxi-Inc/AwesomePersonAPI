---
name: pcp-mc4-recursive-intention-modeling
description: Meta-cognitive pattern for multi-level strategic reasoning about what
  others think you think they think, enabling sophisticated strategy in interactions
  with experienced actors.
tags:
- meta-cognitive
- game-theory
- recursive-reasoning
- strategic-interaction
- orchestration-operator
version: '1.1'
confidence_level: HIGH
category: meta_cognitive
validated_by: Email Corpus Analysis
validated_date: '2025-12-11'
skill_tier: strategic
pattern_tier: 3
mentoring_priority: 9
validation_type: expert_extracted
source_type: skill_corpus_analysis
email_evidence_count: 67
source_skills:
- BI4
- BI4_negotiation_capital_allocation
- MS1_multi_domain_relationship_crisis_management
- S7
evidence_strength: strong
synthesis_reason: Originally implicit, now validated by 67 email instances
works_with:
- PCP-MC1
- PCP-MC14
- PCP-MC26
---

# PCP-MC4: Recursive Intention Modeling

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Multi-level reasoning about mutual beliefs and strategies
**Domain Independence:** Universal for strategic interactions with sophisticated actors
**Orchestration Role:** Determines strategy depth based on opponent sophistication

## Pattern Definition

### Trigger Condition
Strategic interaction with sophisticated actors where:
- Both parties are experienced strategists
- Significant stakes create incentive for deep strategic thinking
- Information asymmetry exists on both sides
- Repeated interaction or reputation effects matter

### Core Procedure

Model recursively:

1. **Level 0: Their Objectives**
   - "What do they want?"

2. **Level 1: Their Model of You**
   - "What do they think I want?"
   - "What do they believe I know?"

3. **Level 2: Their Model of Your Model of Them**
   - "What do they think I think they want?"
   - "How do they think I'm modeling them?"

4. **Level 3: Strategy Implications**
   - "How does this recursive understanding affect their strategy?"
   - "What moves do they expect me to make based on their model of me?"

5. **Level 4: Counter-Strategy**
   - "How should my strategy account for their accounting for my accounting?"
   - "Where can I exploit gaps in their model of me?"

### Expert Heuristic

> "In negotiations with experts, go one level deeper than you think necessary - they're probably doing the same. But know when to stop: over-recursion leads to analysis paralysis."

### Application Contexts

- High-stakes negotiations (M&A, labor disputes, settlements)
- Competitive strategy and market positioning
- Diplomacy and political negotiation
- Board dynamics with experienced directors
- Poker and strategic games
- Adversarial legal proceedings

## Abstraction Source Evidence

### From MS1: Multi-Domain Relationship Crisis Management

**Sequential Game Theory with Incomplete Information**:
> "Models multi-move strategic interactions where players have private information about preferences and capabilities. Uses backward induction to plan escalation sequences: at each decision node, calculate optimal response assuming rational counterparty behavior in subsequent moves."

**Bayesian Updating**:
> "Incorporates Bayesian updating of counterparty type probabilities based on observed actions."

### From BI4: Negotiation Capital Allocation

**Game-Theoretic Foundation**:
> "Expert practitioners maintain multiple simultaneous game models... while coordinating moves to optimize outcomes across all games."

## Evidence from Email Corpus

### Example 1: Regulatory Mind Modeling
**Context:** [PERSON] modeling regulatory authority's perspective
**Evidence:** "If [REGULATOR] finds out that we are selling devices for demo before its [APPROVAL] grant, the consequence of lost trust with the [REGULATOR] will be beyond fix..."
**Insight:** Model what the regulator thinks about your company's compliance behavior

### Example 2: Counterparty Condition Anticipation
**Context:** [PERSON] predicting approval conditions
**Evidence:** "I have no objections if the customer is fully aware of what they are buying and the warrantee aspect is covered by the retailor."
**Insight:** Model the conditions under which stakeholders will approve - what they think constitutes acceptable risk

### Example 3: Knowledge State Signaling
**Context:** [PERSON] explicitly revealing their information state
**Evidence:** "please bear with me. This is a new concept to me."
**Insight:** Signal your knowledge state to help others model you accurately, enabling better coordination

### Example 4: Stakeholder Reaction Prediction
**Context:** [PERSON] anticipating stakeholder surprise
**Evidence:** "It sounds like the plan to sell retailers demo devices and the 9W adapter for retail demos has caught people by surprise."
**Insight:** Model what stakeholders expected vs. what they learned, predicting their reaction trajectory

### Example 5: Competitive Strategy Inference
**Context:** [PERSON] modeling competitor's strategic intentions
**Evidence:** "I don't think that we can assume that we will be in a position to advantage ourselves by paying more than our competitors. Better to compete on factors other than that..."
**Insight:** Model what competitors think about competitive dynamics and how they'll respond to strategic moves

## Integration with Pattern Tiers

### As Orchestration Operator

PCP-MC4 functions as a **depth calibration operator** for strategic analysis:

```
INPUT: Strategic interaction + opponent sophistication assessment
  ↓
PCP-MC4: Determine appropriate recursion depth
  ↓
DEPTH DECISION:
  - Naive opponent → Level 1 sufficient
  - Competent opponent → Level 2 needed
  - Expert opponent → Level 3+ required
  - Over-recursive opponent → Exploit by being unpredictable
  ↓
OUTPUT: Strategy calibrated to appropriate depth
```

### Composition with Other MC Patterns (Evidence-Based)

**Foundation Relationships:**
- **PCP-MC1 → PCP-MC4**: Mental models enable recursive modeling
- **PCP-MC4 + PCP-MC2**: Recursive models feed trajectory forecasting
- **PCP-MC4 → PCP-MC8**: Recursive understanding guides information strategy
- **PCP-MC4 → PCP-MC3**: Understanding their model of you informs framing
- **PCP-MC4 + PCP-MC14**: Adversarial perspective taking deepens recursive modeling

**New Pattern Links:**
- **PCP-MC27**: Urgency limits recursion depth; time pressure truncates modeling
- **PCP-MC28**: Documentation reveals intentions useful for recursive modeling; what they write shows what they think

## Decision Criteria

**Criterion 1: Recursion Depth Selection**
- IF opponent is naive or time-constrained, THEN Level 1 recursion sufficient
- IF opponent is sophisticated and stakes are high, THEN Level 3+ required
- Rationale: Match analytical depth to opponent capability

**Criterion 2: Recursion Termination**
- IF additional recursion depth provides diminishing strategic insight, THEN stop and act
- IF recursion is consuming time needed for action, THEN act on current model
- Rationale: Over-recursion causes paralysis; action eventually required

**Criterion 3: Model Exploitation**
- IF opponent's model of you is detectably wrong, THEN exploit the gap
- IF opponent's model is accurate, THEN need genuine strategic advantage
- Rationale: Model gaps create exploitable asymmetries

**Criterion 4: Unpredictability Value**
- IF opponent is over-recursive and modeling deeply, THEN consider strategic unpredictability
- Rationale: Sometimes the best counter to deep modeling is randomization

## Contrast with Naive Approaches

**Naive Approach**: Focus only on what you want and what they want (Level 0-1).
**Expert Approach**: Model what they think you want and how that shapes their strategy (Level 2+).

**Naive Approach**: Assume your strategy is hidden from sophisticated opponents.
**Expert Approach**: Assume they're modeling your strategy and adjust accordingly.

**Naive Approach**: Go infinitely deep in recursive modeling.
**Expert Approach**: Calibrate depth to opponent sophistication; know when to stop.

## Expertise Level Indicators

| Level | PCP-MC4 Application |
|-------|-----------------|
| **Novice** | Focuses on own objectives; ignores opponent modeling |
| **Competent** | Considers what opponent wants; misses deeper levels |
| **Expert** | Intuits opponent's model of them; adjusts implicitly |
| **Master** | Explicitly models multiple levels; calibrates depth |
| **Sage** | Knows when to abandon recursion for unpredictability |

## Theoretical Foundations

- **Game Theory**: Nash equilibrium, extensive form games
- **Theory of Mind**: Recursive mental state attribution
- **Epistemic Logic**: Knowledge about knowledge
- **Cognitive Hierarchy Theory**: Levels of strategic thinking

## Special Considerations

### Extraction Challenges

This pattern is often implicit in expert reasoning:
- Experts apply it unconsciously as "reading the room" or "anticipating moves"
- Rarely articulated explicitly in written communications
- Extraction requires inference from strategic choices rather than direct statements

### Synthesis Notes

Evidence from source skills shows game-theoretic reasoning and backward induction, but explicit recursive intention modeling language is rare. Pattern partially synthesized from:
- Implicit recursive reasoning in negotiation skills
- Game-theoretic frameworks in crisis management skills
- Expert interview patterns from research literature

---

## Metadata

```yaml
pattern_id: PCP-MC4
pattern_name: Recursive Intention Modeling
tier: 3 (Meta-Cognitive)
core_question: "What do they think I think they think, and how should that shape my strategy?"
domain_independence: Universal (for sophisticated actor interactions)
transfer_rate: >75% (requires sophistication calibration per context)
extraction_confidence: 0.85 (validated by 67 email instances)
orchestration_function: strategic_depth_calibration
prerequisite_patterns:
  - PCP-MC1: Stakeholder Mental Model Construction
synthesis_status: now_validated
```
