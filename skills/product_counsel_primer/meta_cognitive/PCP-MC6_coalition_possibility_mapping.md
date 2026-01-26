---
name: pcp-mc6-coalition-possibility-mapping
description: Meta-cognitive pattern for identifying which stakeholders can be aligned
  into coalitions, what minimal concessions unlock each coalition, and which coalition
  achieves desired outcomes at lowest cost.
tags:
- meta-cognitive
- coalition-building
- political-strategy
- stakeholder-alignment
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
email_evidence_count: 35
source_skills:
- BI17
- BI17_multi_stakeholder_assessment_validation
- ES1
- ES1_enterprise_governance_design
- MS1_multi_domain_relationship_crisis_management
- S14
- S14_multi_stakeholder_authority_clarification
works_with:
- PCP-MC1
- PCP-MC21
---

# PCP-MC6: Coalition Possibility Mapping

**Type:** Meta-Cognitive Pattern (Tier 3)
**Function:** Identifying and building minimum winning coalitions
**Domain Independence:** Universal for multi-stakeholder decision contexts
**Orchestration Role:** Determines where to focus influence and negotiation efforts

## Pattern Definition

### Trigger Condition
Multi-stakeholder decision requiring support from subset of stakeholders, including:
- Board or committee decisions requiring majority/supermajority
- Organizational changes needing cross-functional buy-in
- Negotiations with multiple parties
- Political or policy decisions requiring coalition
- Project approvals spanning organizational boundaries

### Core Procedure

Given stakeholder mental models (PCP-MC1), map coalition possibilities:

1. **Goal Overlap Analysis**
   - Identify whose goals overlap sufficiently for natural coalition
   - Find shared interests that create alignment basis
   - Recognize conflicting interests that prevent coalition

2. **Minimal Concession Mapping**
   - For each potential coalition member, identify minimum concession that unlocks support
   - Distinguish essential requirements from nice-to-haves
   - Calculate concession costs vs. coalition value

3. **Minimum Winning Coalition Identification**
   - Determine smallest coalition that achieves desired outcome
   - Compare alternative coalitions by total concession cost
   - Select optimal coalition path

4. **Counter-Coalition Assessment**
   - Anticipate what coalitions opponents might form
   - Identify how to block or preempt opposing coalitions
   - Plan for coalition competition dynamics

### Expert Heuristic

> "Don't try to convince everyone - identify the minimum winning coalition and the minimum concessions needed. Over-building coalitions wastes resources and often creates contradictory commitments."

### Application Contexts

- Board and executive decision-making
- Organizational change initiatives
- Multi-party negotiations
- Political and policy strategy
- Cross-functional project approval
- Mergers and organizational integration

## Abstraction Source Evidence

### From BI17: Multi-Stakeholder Assessment Validation

**Phase 2.2 - Multiple Decision Pathway Development**:
> "Create stakeholder-appropriate decision frameworks that maintain consistent underlying evaluation while allowing different criterion weighting. Develop clear protocols for pathway selection and coordination."

**Decision Pathway Management**:
> "The skill distinguishes expert practitioners through their ability to maintain multiple viable decision pathways simultaneously."

### From MS1: Multi-Domain Relationship Crisis Management

**Multi-Stakeholder Coordination**:
> "Coordinate responses across multiple internal stakeholders with different expertise and priorities."

**Strategic Insulation Assessment**:
> "Evaluate feasibility of isolating tactical actions from strategic relationships by analyzing counterparty organizational structure, decision-making processes, and historical compartmentalization patterns."

### From ES1: Enterprise Governance Design

**Multi-Stakeholder Alignment**:
> "Design governance structures that align multiple stakeholder interests through appropriate representation and decision authority allocation."

## Evidence from Email Corpus

### Example 1: Cross-Functional Approval Orchestration
**Context:** [PERSON] routing approvals efficiently during time crunch
**Evidence:** "Can you vett our responses with PR/Legal for appropriateness to communicate to customers... I'll run this by the product team as well..."
**Insight:** Parallel routing to multiple approval stakeholders accelerates process while building necessary coalition

### Example 2: Crisis Coalition Building
**Context:** [PERSON] assembling stakeholders for urgent issue
**Evidence:** "I suggest that some sub/super-set of us meet soon to discuss the implications... I agree we should get together sooner rather than later..."
**Insight:** Rapidly identify and convene minimum winning coalition for strategic decisions

### Example 3: Knowledge State Signaling for Coalition Entry
**Context:** [PERSON] positioning themselves for coalition membership
**Evidence:** "please bear with me. This is a new concept to me."
**Insight:** Acknowledging knowledge gaps appropriately enables coalition participation despite expertise limitations

### Example 4: Stakeholder Validation Choreography
**Context:** [PERSON] sequencing stakeholder approvals
**Evidence:** "We can socialize with [PERSON] after we have [TEAM] feedback, although perhaps we should also give her a head's up that this is coming..."
**Insight:** Sequence coalition building to ensure internal alignment before external engagement

### Example 5: Distributed Risk Validation
**Context:** [PERSON] routing decision across multiple experts
**Evidence:** "[PERSON] and I happened to touch base before it was published. He will bring the other thread into this one for review..."
**Insight:** Integrate parallel workstreams to build broader coalition support and ensure comprehensive validation

## Integration with Pattern Tiers

### As Orchestration Operator

PCP-MC6 functions as a **resource allocation operator** for influence efforts:

```
INPUT: Multi-stakeholder decision + stakeholder models (PCP-MC1)
  ↓
PCP-MC6: Map coalition possibilities
  ↓
ALLOCATION DECISION:
  - Which stakeholders are in minimum winning coalition?
  - What concessions are required for each?
  - Where should influence efforts focus?
  ↓
OUTPUT: Focused coalition-building strategy
```

### Composition with Other MC Patterns (Evidence-Based)

**Foundation Relationships:**
- **PCP-MC1 → PCP-MC6**: Mental models enable coalition mapping
- **PCP-MC6 → PCP-MC3**: Coalition targets inform communication focus
- **PCP-MC6 + PCP-MC2**: Predict how coalitions will evolve
- **PCP-MC6 → PCP-MC8**: Coalition strategy affects information revelation
- **PCP-MC6 + PCP-MC21**: Political intelligence for coalition building (761 co-occurrences)
- **PCP-MC6 + PCP-MC17**: Cross-functional coordination enables coalition execution

**New Pattern Links:**
- **PCP-MC27**: Urgency compresses coalition-building timelines; crisis coalitions form differently
- **PCP-MC28**: Documentation of commitments affects coalition stability and enforcement
- **PCP-MC29**: Post-task reflection reveals which coalition strategies succeeded/failed

## Decision Criteria

**Criterion 1: Minimum Winning Coalition**
- IF smaller coalition can achieve outcome, THEN prefer smaller over larger
- IF marginal members require significant concessions, THEN evaluate whether worth including
- Rationale: Over-building coalitions wastes resources and creates commitments

**Criterion 2: Concession Efficiency**
- IF concession unlocks multiple coalition members, THEN prioritize over single-member concessions
- IF concession conflicts with other coalition member requirements, THEN find alternative path
- Rationale: Efficient concessions maximize coalition value per unit cost

**Criterion 3: Coalition Stability**
- IF coalition members have conflicting interests with each other, THEN assess stability risk
- IF coalition requires ongoing maintenance, THEN factor maintenance cost into evaluation
- Rationale: Unstable coalitions may fail when needed most

**Criterion 4: Counter-Coalition Blocking**
- IF opponents can form blocking coalition, THEN consider preemptive moves
- IF key swing stakeholders could go either way, THEN prioritize securing their commitment
- Rationale: Blocking is often easier than building; secure against it

## Contrast with Naive Approaches

**Naive Approach**: Try to convince everyone; seek unanimous support.
**Expert Approach**: Identify minimum winning coalition; focus resources on essential stakeholders.

**Naive Approach**: Offer same pitch/concessions to all stakeholders.
**Expert Approach**: Tailor approach to each coalition member's specific requirements.

**Naive Approach**: Ignore opponents; focus only on supporters.
**Expert Approach**: Actively block or preempt opposing coalitions.

**Naive Approach**: Lock in coalition early; assume it holds.
**Expert Approach**: Monitor coalition stability; maintain relationships; adapt to shifts.

## Expertise Level Indicators

| Level | PCP-MC6 Application |
|-------|-----------------|
| **Novice** | Seeks unanimous approval; doesn't think in coalitions |
| **Competent** | Identifies supporters vs. opponents; limited strategic mapping |
| **Expert** | Intuits coalition possibilities ("political sense") |
| **Master** | Explicitly maps coalition mathematics; can articulate strategy |
| **Sage** | Knows when coalition-building is wrong approach |

## Theoretical Foundations

- **Coalition Theory (Riker)**: Minimum winning coalition principle
- **Voting Theory**: Decision rules and coalition requirements
- **Game Theory**: Coalition formation games
- **Political Science**: Legislative and organizational politics

---

## Metadata

```yaml
pattern_id: PCP-MC6
pattern_name: Coalition Possibility Mapping
tier: 3 (Meta-Cognitive)
core_question: "What's the smallest coalition that wins, and what does each member need?"
domain_independence: Universal (for multi-stakeholder decisions)
transfer_rate: >80% (applies wherever coalition approval needed)
extraction_confidence: 0.85 (validated by 35 email instances)
orchestration_function: influence_resource_allocation
prerequisite_patterns:
  - PCP-MC1: Stakeholder Mental Model Construction
```
