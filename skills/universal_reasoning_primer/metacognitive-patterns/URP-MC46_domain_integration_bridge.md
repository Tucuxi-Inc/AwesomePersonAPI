---
name: urp-mc46-domain-integration-bridge
description: Meta-cognitive pattern for bridging universal reasoning patterns with domain-specific skill primers, enabling dynamic expertise composition and context-aware skill activation.
tags:
- meta-cognitive
- integration
- domain-bridging
- skill-composition
- expertise-synthesis
version: '1.0'
confidence_level: HIGH
category: meta_cognitive
validated_by: Architecture Design
validated_date: '2026-01-02'
skill_tier: strategic
pattern_tier: 4
mentoring_priority: 5
validation_type: architecture_design
source_type: system_architecture
source_skills:
- domain-expertise-mapping
- skill-orchestration
- context-adaptation
works_with:
- URP-MC1
- URP-MC8
- URP-MC16
- URP-MC37
co_occurs_with:
- URP-SP1
- URP-SP3
- URP-IP1
domain_bridge_config:
  supported_primers:
  - product_counsel_primer
  - employment_counsel_primer
  bridge_mode: additive
  skill_inheritance: true
---

# URP-MC46: Domain Integration Bridge

**Type:** Meta-Cognitive Pattern (Tier 4 - Orchestration)
**Function:** Bridges universal reasoning patterns with domain-specific expertise primers
**Domain Independence:** Universal bridge mechanism, domain-aware activation
**Orchestration Role:** Coordinates URP patterns with domain primers (PCP, ECP, etc.) for context-appropriate expertise synthesis

## Pattern Definition

### Trigger Condition
Situations involving:
- Scenarios requiring domain-specific expertise beyond universal reasoning
- Active domain primer(s) loaded alongside URP foundation
- Cross-domain analysis requiring multi-primer integration
- Expertise gaps identified that domain skills can address
- User/system configuration specifying domain enhancement mode

### Core Procedure

1. **Domain Context Assessment**
   - What domain(s) does this scenario involve?
   - Which domain primer(s) are currently active?
   - What domain-specific skills are relevant to this context?
   - Are there domain regulatory or compliance considerations?

2. **URP-to-Domain Mapping**
   - Which URP patterns are currently active?
   - What domain skills complement each active URP pattern?
   - Are there domain patterns that extend URP capabilities?
   - What domain expertise fills gaps in universal reasoning?

3. **Skill Synthesis**
   - Combine URP pattern guidance with domain skill expertise
   - Layer domain-specific considerations onto universal approaches
   - Ensure domain compliance requirements are addressed
   - Maintain coherent reasoning across pattern layers

4. **Bridge Mode Selection**
   - **Additive Mode:** Domain skills augment URP (default)
   - **Override Mode:** Domain skills replace conflicting URP guidance
   - **Consultation Mode:** Domain skills inform but don't direct
   - **Integration Mode:** Full synthesis of URP + domain reasoning

5. **Output Harmonization**
   - Ensure consistent terminology across pattern sources
   - Resolve any conflicts between URP and domain guidance
   - Present unified recommendations to downstream processes
   - Track which patterns/skills contributed to output

## Bridge Configuration

### Supported Domain Primers

| Primer | Prefix | Domain | Integration Status |
|--------|--------|--------|-------------------|
| Product Counsel Primer | PCP | Technology transactions, IP, contracts | Active |
| Employment Counsel Primer | ECP | Employment law, HR, workplace | Available |
| (Future) Litigation Primer | LCP | Dispute resolution, litigation | Planned |
| (Future) Corporate Primer | CCP | Corporate governance, M&A | Planned |

### Pattern Mapping Examples

| URP Pattern | Domain Enhancement | Primer |
|-------------|-------------------|--------|
| URP-MC1 (Progress Monitoring) | PCP skill tracking, milestone analysis | PCP |
| URP-MC8 (Error Detection) | Contractual risk identification | PCP |
| URP-MC14 (Adversarial Perspective) | Opposing counsel anticipation | PCP/LCP |
| URP-MC24 (Confidence Calibration) | Domain expertise level assessment | All |
| URP-MC37 (Expertise Boundaries) | Domain-specific competency limits | All |

## Operating Modes

### Mode 1: URP-Only
- No domain primers active
- Pure universal reasoning patterns
- Domain-agnostic analysis
- Use case: General reasoning, cross-domain exploration

### Mode 2: URP + Single Domain (Default)
- URP foundation + one domain primer
- Domain skills extend URP capabilities
- Domain-specific terminology and expertise
- Use case: Specialized professional analysis

### Mode 3: URP + Multi-Domain
- URP foundation + multiple domain primers
- Cross-domain synthesis enabled
- Conflict resolution between domains
- Use case: Complex multi-disciplinary scenarios

## Integration Points

### With Pattern Loader
```
MCPatternLoader.set_domain_primer(primer_name)
  → Loads URP patterns (always)
  → Loads domain patterns (if primer specified)
  → Activates URP-MC46 bridge logic
  → Maps domain skills to URP patterns
```

### With Cognitive Router
```
CognitiveRouter.route(scenario)
  → SAGE assessment
  → URP pattern selection
  → IF domain_primer_active:
      → Invoke URP-MC46 bridge
      → Augment with domain patterns/skills
  → Return unified pattern set
```

### With Skills Loader
```
SkillsLoader.load_skills(primer_name)
  → Domain skills available
  → URP-MC46 maps skills to URP patterns
  → Skills accessible via bridge queries
```

## Expert Heuristic

> "Universal reasoning provides the cognitive scaffold; domain expertise fills in the specialized knowledge. The bridge pattern ensures these layers work together coherently, preventing domain knowledge from fragmenting universal reasoning while ensuring specialized expertise is properly applied."

## Application Contexts

- Professional services requiring domain expertise
- Legal, medical, financial analysis scenarios
- Technology and product counseling
- Cross-disciplinary problem solving
- Expertise development and skill progression

## Quality Indicators

**Effective bridging:**
- Domain expertise naturally extends URP reasoning
- No conflicting guidance between layers
- Terminology consistent across sources
- Clear attribution of guidance sources

**Bridging issues:**
- Domain and URP guidance conflict
- Terminology confusion between layers
- Over-reliance on domain at expense of universal reasoning
- Under-utilization of available domain expertise

## Administrative Controls

This pattern is managed through:
- System configuration: `active_primer` setting
- Admin API: `/api/v1/admin/config/primers/*` endpoints
- Pattern loader: `set_domain_primer()` method
- User preferences: Per-session primer selection (future)

## Related Patterns

- **URP-MC37:** Expertise Authority Boundary Recognition (knows when domain expertise needed)
- **URP-MC16:** Approach Selection (chooses between reasoning strategies)
- **URP-SP1:** Strategic Planning (coordinates multi-pattern execution)
- **URP-IP1:** Communication Framing (adapts output to domain context)
