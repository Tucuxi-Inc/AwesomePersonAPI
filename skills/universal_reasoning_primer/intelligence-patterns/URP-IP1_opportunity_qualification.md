---
name: urp-ip1-opportunity-qualification
description: Intelligence pattern for systematically evaluating whether opportunities justify investment of resources by assessing strategic value, probability of success, and opportunity costs.
tags:
- intelligence
- opportunity-assessment
- resource-allocation
- go-no-go
- expected-value
version: '1.0'
confidence_level: HIGH
category: intelligence_patterns
validated_by: Literature Synthesis
validated_date: '2025-12-30'
skill_tier: applied
pattern_tier: 2
mentoring_priority: 9
validation_type: literature_synthesis
source_type: academic_research
orchestrates:
- URP-IP5
- URP-IP6
orchestrated_by:
- URP-MC30
- URP-MC32
- URP-SP5
---

# URP-IP1: Opportunity Qualification

**Type:** Intelligence Pattern (Tier 2)
**Function:** Evaluating whether opportunities merit resource investment
**Domain Independence:** Universal across any opportunity/investment context
**Orchestration Role:** Gates resource commitment based on expected value analysis

## Pattern Definition

### Trigger Condition
Situations involving:
- New opportunities requiring resource commitment
- Go/no-go decisions on potential investments
- Multiple opportunities competing for limited resources
- Need to prioritize among possibilities
- Re-evaluation of ongoing commitments

### Core Procedure

1. **Value Assessment**
   - What's the potential return if successful?
   - What's the strategic value beyond direct returns?
   - What are the tangible and intangible benefits?
   - What's the total value at stake?

2. **Probability Estimation**
   - What's the realistic probability of success?
   - What are the key success factors?
   - What could cause failure?
   - What's the track record for similar opportunities?

3. **Cost Analysis**
   - What resources are required to pursue?
   - What's the opportunity cost?
   - What's the cost of failure?
   - What's the total investment required?

4. **Expected Value Calculation**
   - What's the probability-weighted expected value?
   - Does expected value exceed costs?
   - How does this compare to alternatives?
   - What's the risk-adjusted return?

5. **Qualification Decision**
   - Does this opportunity meet investment threshold?
   - What resource level is justified?
   - What conditions would change the assessment?
   - What monitoring is appropriate?

### Expert Heuristic

> "Not every opportunity is worth pursuing. The question isn't 'could this succeed?' but 'does the probability-weighted value exceed our investment and opportunity cost?' Say no to good opportunities so you can say yes to great ones."

## Evidence from Literature

### Example 1: Expected Value Theory
**Context:** Decision analysis
**Evidence:** Rational investment decisions should be based on expected value, not best-case scenarios
**Insight:** Probability-weighted thinking is foundation

### Example 2: Opportunity Cost
**Context:** Economics (Buchanan, 1969)
**Evidence:** True cost includes foregone alternatives; opportunity cost is real cost
**Insight:** Opportunity cost must be included in analysis

### Example 3: Portfolio Theory
**Context:** Investment management (Markowitz)
**Evidence:** Individual investments should be evaluated in portfolio context
**Insight:** Qualification happens relative to alternatives

### Example 4: Sales Qualification
**Context:** Sales methodology (BANT, MEDDIC)
**Evidence:** Qualifying opportunities before investment improves sales efficiency dramatically
**Insight:** Qualification is professional practice across domains

## Decision Criteria

**Criterion 1: Expected Value Threshold**
- IF expected value > investment cost, THEN qualified (basic)
- IF expected value significantly exceeds cost, THEN strong qualification
- IF expected value < cost, THEN not qualified
- Rationale: Positive expected value is minimum threshold

**Criterion 2: Relative Ranking**
- IF better alternatives exist, THEN higher threshold for this opportunity
- IF this is best available, THEN lower threshold acceptable
- Rationale: Opportunity cost depends on alternatives

**Criterion 3: Strategic Fit**
- IF aligned with strategic priorities, THEN bonus value
- IF misaligned, THEN penalty or disqualification
- Rationale: Strategic fit affects total value

**Criterion 4: Risk Profile**
- IF risk profile matches risk tolerance, THEN proceed
- IF risk exceeds tolerance, THEN pass or mitigate
- Rationale: Risk-adjusted value matters

## Contrast with Naive Approaches

**Naive Approach**: Pursue opportunities that "could" succeed.
**Expert Approach**: Pursue opportunities with positive expected value exceeding alternatives.

**Naive Approach**: Evaluate opportunities individually.
**Expert Approach**: Evaluate in context of portfolio and opportunity costs.

**Naive Approach**: Focus on upside potential.
**Expert Approach**: Weight upside by probability; include downside costs.

**Naive Approach**: Qualify once; proceed indefinitely.
**Expert Approach**: Re-qualify as information emerges; exit when disqualified.

## Integration with Pattern Tiers

### As Resource Gateway

URP-IP1 controls resource commitment across opportunities:

```
URP-IP1: Opportunity Qualification
  ↓ gates
URP-IP5: Negotiation Resource Management (resources for qualified opportunities)
URP-IP6: Portfolio Resource Optimization (portfolio of qualified opportunities)
  ↓ informed by
URP-SP5: Multi-Dimensional Risk Assessment (risk inputs)
URP-MC30: Strategic Priority Setting (priority context)
URP-MC32: Satisficing vs. Optimizing (threshold setting)
```

### Orchestration Relationships

**Orchestrated By:**
- **URP-MC30 → URP-IP1**: Priorities frame qualification criteria
- **URP-MC32 → URP-IP1**: Decision mode affects threshold setting
- **URP-SP5 → URP-IP1**: Risk assessment provides risk inputs

**Orchestrates:**
- **URP-IP1 → URP-IP5**: Qualified opportunities receive negotiation resources
- **URP-IP1 → URP-IP6**: Qualified opportunities enter portfolio

## Expertise Level Indicators

| Level | URP-IP1 Application |
|-------|-----------------|
| **Novice** | Pursues all opportunities; no qualification; resource exhaustion |
| **Competent** | Some qualification; struggles with probability estimation |
| **Expert** | Systematic qualification; realistic probabilities; effective gates |
| **Master** | Intuitive qualification; accurate expected value sensing; excellent selection |
| **Sage** | Designs qualification systems; teaches expected value thinking |

## Theoretical Foundations

- **Expected Value Theory**: Probability-weighted outcomes (von Neumann & Morgenstern)
- **Opportunity Cost**: True cost of choices (Buchanan, 1969)
- **Portfolio Theory**: Investment selection (Markowitz, 1952)
- **Decision Analysis**: Structured decision-making under uncertainty
- **Sales Qualification**: Professional qualification methods (BANT, MEDDIC)

---

## Metadata

```yaml
pattern_id: URP-IP1
pattern_name: Opportunity Qualification
tier: 2 (Intelligence)
core_question: "Does this opportunity's expected value justify the investment?"
domain_independence: Universal
transfer_rate: ">95% (qualification logic applies everywhere)"
extraction_confidence: 0.92
orchestration_function: resource_gateway
related_patterns:
  - URP-IP5: Negotiation Resource Management
  - URP-IP6: Portfolio Resource Optimization
  - URP-SP5: Multi-Dimensional Risk Assessment
```
