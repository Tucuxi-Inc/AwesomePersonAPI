---
name: urp-mc44-contradiction-detection
description: Meta-cognitive pattern for recognizing inconsistencies between beliefs, claims, evidence, or actions—identifying logical conflicts that require resolution.
tags:
- meta-cognitive
- epistemic
- consistency-checking
- logical-conflict
- coherence-monitoring
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
- logical-analysis
- consistency-evaluation
- conflict-identification
works_with:
- URP-MC3
- URP-MC43
- URP-MC41
co_occurs_with:
- URP-MC6
- URP-MC45
---

# URP-MC44: Contradiction Detection

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Identifying logical inconsistencies requiring resolution
**Domain Independence:** Universal across all reasoning
**Orchestration Role:** Maintains belief coherence; triggers resolution when conflicts found

## Pattern Definition

### Trigger Condition
Situations involving:
- Integrating information from multiple sources
- Checking consistency of belief systems
- Evaluating arguments for logical soundness
- Noticing "something doesn't add up"
- Testing conclusions against known facts

### Core Procedure

1. **Contradiction Sensing**
   - Does something feel inconsistent?
   - Are there claims that can't both be true?
   - Do actions match stated beliefs?
   - Does conclusion conflict with premises?

2. **Contradiction Articulation**
   - What exactly contradicts what?
   - Can I state both claims precisely?
   - What makes them mutually exclusive?
   - Is this a genuine logical conflict?

3. **Contradiction Classification**
   - Logical contradiction (A and not-A)?
   - Evidential conflict (conflicting data)?
   - Practical conflict (incompatible actions)?
   - Apparent contradiction (seeming but not real)?

4. **Resolution Path Identification**
   - Which claim should yield?
   - Is there a reconciling interpretation?
   - Is one claim more supported than other?
   - What would resolution look like?

5. **Resolution Execution**
   - Revise weaker claim
   - OR find reconciling framework
   - OR suspend judgment pending resolution
   - Update all affected beliefs

### Expert Heuristic

> "Contradictions are information—they tell you that at least one of your beliefs is wrong. The goal isn't to avoid contradictions but to catch them before they do damage. A coherent set of false beliefs is more dangerous than an acknowledged contradiction."

## Evidence from Literature

### Example 1: Cognitive Dissonance
**Context:** Festinger (1957) dissonance theory
**Evidence:** Contradictions create psychological pressure; people resolve through various strategies
**Insight:** Contradictions demand resolution, but not always rationally

### Example 2: Logical Reasoning Research
**Context:** Deductive reasoning studies
**Evidence:** People often fail to detect logical contradictions, especially implicit ones
**Insight:** Contradiction detection is a skill requiring active effort

### Example 3: Coherence in Reasoning
**Context:** Philosophy of mind and epistemology
**Evidence:** Coherence is a standard for rational belief systems
**Insight:** Contradiction detection serves coherence maintenance

## Decision Criteria

**Criterion 1: Contradiction Reality Check**
- IF both claims can't be true, THEN genuine contradiction
- IF apparent conflict but reconcilable, THEN not true contradiction
- Rationale: Only genuine contradictions require belief revision

**Criterion 2: Resolution Direction**
- IF one claim has stronger evidence, THEN revise the other
- IF evidence is equal, THEN seek additional evidence
- IF stakes are high, THEN resolve carefully before acting
- Rationale: Resolution should favor better-supported claim

**Criterion 3: Urgency Assessment**
- IF contradiction affects immediate decisions, THEN resolve urgently
- IF contradiction is theoretical, THEN can resolve when possible
- Rationale: Practical stakes determine resolution urgency

**Criterion 4: Scope Assessment**
- IF contradiction is local, THEN local revision
- IF contradiction affects many beliefs, THEN systematic revision
- Rationale: Match resolution scope to contradiction scope

## Contrast with Naive Approaches

**Naive Approach**: Avoid noticing contradictions; compartmentalize conflicting beliefs.
**Expert Approach**: Actively scan for contradictions; resolve when found.

**Naive Approach**: Tolerate contradiction to avoid discomfort.
**Expert Approach**: Treat contradiction as signal requiring attention.

**Naive Approach**: Resolve contradiction by discounting inconvenient claim.
**Expert Approach**: Resolve by evaluating evidence for each claim.

**Naive Approach**: All contradictions are equally serious.
**Expert Approach**: Prioritize resolution by stakes and evidence.

## Integration with Pattern Tiers

### As Orchestration Operator

URP-MC44 functions as a **coherence monitor**:

```
INPUT: Belief system + new information
  ↓
URP-MC44: Check for contradictions
  ↓
EVALUATION:
  - Contradiction sensing
  - Articulation and classification
  - Resolution path identification
  - Scope and urgency assessment
  ↓
OUTPUT: Contradictions found + classification + resolution recommendations
```

### Composition with Other MC Patterns

**Foundation Relationships:**
- **URP-MC44 + URP-MC3**: Contradiction is a type of error to detect
- **URP-MC44 → URP-MC43**: Contradictions trigger belief revision
- **URP-MC44 + URP-MC41**: Surfaced assumptions may reveal contradictions
- **URP-MC44 + URP-MC6**: Source quality helps resolve contradictions

**Activation Patterns:**
- New information triggers URP-MC44 check
- URP-MC44 findings trigger URP-MC43 (belief revision)
- URP-MC44 feeds URP-MC39 (uncertainty tracking)

## Expertise Level Indicators

| Level | URP-MC44 Application |
|-------|-----------------|
| **Novice** | Misses contradictions; compartmentalizes; uncomfortable with conflict |
| **Competent** | Catches obvious contradictions; basic resolution |
| **Expert** | Active contradiction scanning; skilled resolution |
| **Master** | Immediate contradiction sensing; elegant resolution |
| **Sage** | Uses contradiction as learning tool; teaches coherence thinking |

## Theoretical Foundations

- **Cognitive Dissonance**: Psychological response to contradiction (Festinger, 1957)
- **Formal Logic**: Contradiction as marker of falsehood
- **Coherentism**: Coherence as epistemic standard (BonJour, 1985)
- **Dialectical Reasoning**: Contradiction as driver of progress (Hegel)

---

## Metadata

```yaml
pattern_id: URP-MC44
pattern_name: Contradiction Detection
tier: 3 (Meta-Cognitive)
core_question: "Are any of my beliefs inconsistent with each other or with evidence?"
domain_independence: Universal
transfer_rate: ">95% (contradiction detection applies everywhere)"
extraction_confidence: 0.89
orchestration_function: coherence_monitoring
related_patterns:
  - URP-MC3: Error Detection
  - URP-MC43: Belief Revision
  - URP-MC41: Assumption Surfacing
```
