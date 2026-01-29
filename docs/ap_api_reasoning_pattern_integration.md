# AP API Reasoning Pattern Integration
## Leveraging Universal Reasoning Patterns for Intelligent Probe Generation

**Version 1.0 | January 2026**
**Supplement to: AP API Development Specification**

---

## Purpose

This document specifies how the AP API interview engine and training session engine should leverage Universal Reasoning Patterns (URPs) to generate contextually intelligent questions. Rather than using static question banks, the system dynamically generates probes based on:

1. **Candidate context** (resume, prior responses, role)
2. **Conversation state** (what's been asked, what signals have been detected)
3. **Pattern-based reasoning** (applying specific metacognitive and interpersonal patterns)

---

## Part 1: Core Reasoning Patterns for Assessment

### 1.1 Pattern Reference

These patterns from the URP library are specifically applicable to candidate and employee assessment:

| Pattern ID | Name | Assessment Application |
|------------|------|----------------------|
| **MC1** | Stakeholder Identification & Perspective-Taking | Map candidate as multi-dimensional; understand their goals, constraints, fears |
| **MC24** | Assumption Surfacing | Identify hidden assumptions in responses; probe beneath surface answers |
| **MC29** | Progress Monitoring & Recalibration | Track interview effectiveness; adjust strategy based on signal quality |
| **MC35** | Representation Choice | Select appropriate probe type based on role context and trait |
| **MC38** | Abstraction Level Selection | Calibrate probe depth (surface vs. deep) based on response quality |
| **MC44** | Solution Space Exploration | Consider alternative interpretations; avoid anchoring on first impression |
| **IP3** | Active Listening with Validation | Identify what's NOT said; probe omissions |
| **IP7** | Conflict/Tension Exploration | Probe disagreement, failure, friction—where adaptability reveals itself |
| **IP11** | Trust Calibration | Weight self-report vs. behavioral evidence appropriately |
| **SP8** | Risk Identification | Identify potential failure modes; map warning signals |
| **SP12** | Scenario Projection | Project candidate performance at future time points |

### 1.2 Pattern Categories by Function

```
PROBE GENERATION PATTERNS
├── MC35 (Representation Choice) — Which type of question for this context?
├── MC38 (Abstraction Level) — How deep should this probe go?
└── MC24 (Assumption Surfacing) — What assumptions need challenging?

RESPONSE ANALYSIS PATTERNS
├── IP3 (Active Listening) — What's missing from this response?
├── IP7 (Conflict Exploration) — Where's the tension to explore?
├── IP11 (Trust Calibration) — Is this self-report or behavioral evidence?
└── MC44 (Solution Space) — What alternative interpretations exist?

INTERVIEW MANAGEMENT PATTERNS
├── MC1 (Stakeholder Mapping) — Who is this candidate, really?
├── MC29 (Progress Monitoring) — Is this interview getting good signal?
└── SP8 (Risk Identification) — What failure modes should I probe?
```

---

## Part 2: Implementation Architecture

### 2.1 Pattern-Aware Probe Generator

```python
# backend/app/services/probe_generator.py

from typing import List, Dict, Optional, Any
from enum import Enum
from app.services.llm_client import LLMClient
from app.models.candidate import Candidate
from app.models.interview import InterviewSession
from app.schemas.probe import Probe, ProbeContext

class ReasoningPattern(Enum):
    MC1_STAKEHOLDER = "MC1"
    MC24_ASSUMPTION = "MC24"
    MC29_PROGRESS = "MC29"
    MC35_REPRESENTATION = "MC35"
    MC38_ABSTRACTION = "MC38"
    MC44_SOLUTION_SPACE = "MC44"
    IP3_ACTIVE_LISTENING = "IP3"
    IP7_CONFLICT = "IP7"
    IP11_TRUST = "IP11"
    SP8_RISK = "SP8"
    SP12_PROJECTION = "SP12"


class PatternAwareProbeGenerator:
    """
    Generates contextually intelligent probes by applying URP patterns
    to candidate context and conversation state.
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.pattern_prompts = self._load_pattern_prompts()
    
    async def generate_probe(
        self,
        trait_id: str,
        context: ProbeContext,
        patterns_to_apply: List[ReasoningPattern]
    ) -> Probe:
        """
        Generate a probe by applying specified reasoning patterns.
        
        Args:
            trait_id: The trait being assessed
            context: Full context including resume, prior responses, role
            patterns_to_apply: Which URP patterns to use for generation
        
        Returns:
            A contextually tailored probe
        """
        
        # Build pattern-informed prompt
        prompt = self._build_generation_prompt(
            trait_id=trait_id,
            context=context,
            patterns=patterns_to_apply
        )
        
        # Generate probe
        result = await self.llm.complete(
            prompt=prompt,
            system_prompt=self._get_system_prompt(),
            response_format="json"
        )
        
        return Probe(
            text=result["question"],
            trait_id=trait_id,
            patterns_applied=patterns_to_apply,
            generation_rationale=result["rationale"],
            follow_up_triggers=result.get("follow_up_triggers", []),
            evidence_expectations=result.get("evidence_expectations", [])
        )
    
    async def select_patterns_for_context(
        self,
        trait_id: str,
        context: ProbeContext
    ) -> List[ReasoningPattern]:
        """
        Determine which patterns are most applicable given current context.
        """
        
        patterns = []
        
        # Always apply representation choice for probe type selection
        patterns.append(ReasoningPattern.MC35_REPRESENTATION)
        
        # If this is the first probe for a trait, use assumption surfacing
        if not context.has_prior_probes_for_trait(trait_id):
            patterns.append(ReasoningPattern.MC24_ASSUMPTION)
        
        # If prior response was surface-level, increase abstraction depth
        if context.last_response_depth == "SURFACE":
            patterns.append(ReasoningPattern.MC38_ABSTRACTION)
        
        # If response lacked conflict/failure, probe for tension
        if context.last_response_lacked("conflict", "failure", "tension"):
            patterns.append(ReasoningPattern.IP7_CONFLICT)
        
        # If response was heavy on self-report, seek behavioral evidence
        if context.last_evidence_type == "SELF_REPORT":
            patterns.append(ReasoningPattern.IP11_TRUST)
        
        # If confidence is low, explore alternative interpretations
        if context.current_confidence < 0.5:
            patterns.append(ReasoningPattern.MC44_SOLUTION_SPACE)
        
        # For certain traits, always probe for risk/failure modes
        if trait_id in ["RESILIENCE", "ADAPTABILITY", "INITIATIVE"]:
            patterns.append(ReasoningPattern.SP8_RISK)
        
        return patterns
    
    def _build_generation_prompt(
        self,
        trait_id: str,
        context: ProbeContext,
        patterns: List[ReasoningPattern]
    ) -> str:
        """Build the LLM prompt incorporating pattern instructions."""
        
        pattern_instructions = self._get_pattern_instructions(patterns)
        
        return f"""Generate an interview probe for assessing {trait_id}.

## CANDIDATE CONTEXT
{self._format_candidate_context(context)}

## CONVERSATION HISTORY
{self._format_conversation_history(context)}

## CURRENT ASSESSMENT STATE
- Trait: {trait_id}
- Evidence collected: {len(context.evidence_for_trait(trait_id))} items
- Current confidence: {context.confidence_for_trait(trait_id)}
- Signal gaps: {context.signal_gaps_for_trait(trait_id)}

## REASONING PATTERNS TO APPLY
{pattern_instructions}

## TASK
Generate ONE probe question that:
1. Applies the reasoning patterns above
2. Addresses the signal gaps identified
3. Is tailored to this specific candidate's background
4. Will elicit behavioral (not hypothetical) evidence

Respond in JSON:
{{
    "question": "The probe question text",
    "rationale": "Why this question, how patterns were applied",
    "follow_up_triggers": ["conditions that would trigger follow-up"],
    "evidence_expectations": ["what good answers would include"]
}}
"""
    
    def _get_pattern_instructions(
        self, 
        patterns: List[ReasoningPattern]
    ) -> str:
        """Get specific instructions for each pattern."""
        
        instructions = []
        
        for pattern in patterns:
            if pattern == ReasoningPattern.MC24_ASSUMPTION:
                instructions.append("""
**MC24 - Assumption Surfacing**
Surface and challenge assumptions. Don't accept the candidate's framing at face value.
- What assumptions might the candidate be making about what you want to hear?
- What assumptions are you making about their experience?
- Generate a probe that tests whether stated beliefs match actual behavior.
Example approach: "You mentioned you value X. Tell me about a time that commitment was tested."
""")
            
            elif pattern == ReasoningPattern.MC35_REPRESENTATION:
                instructions.append("""
**MC35 - Representation Choice**
Choose the right type of probe for this role and trait combination.
- For technical roles: probe for systematic thinking
- For leadership roles: probe for people/influence skills
- For creative roles: probe for divergent thinking
- Match the probe style to what success looks like in THIS specific role.
""")
            
            elif pattern == ReasoningPattern.MC38_ABSTRACTION:
                instructions.append("""
**MC38 - Abstraction Level Selection**
The prior response was too surface-level. Go deeper.
- Ask for specific names, dates, numbers, outcomes
- Move from general claims to concrete instances
- Probe the "how" and "why" behind stated actions
Example approach: "You mentioned [general thing]. Walk me through specifically what YOU did—not the team, you personally."
""")
            
            elif pattern == ReasoningPattern.IP3_ACTIVE_LISTENING:
                instructions.append("""
**IP3 - Active Listening (Probe Omissions)**
Something is missing from the candidate's responses. Probe for it.
- What topic did they avoid or gloss over?
- What question did they partially answer?
- What natural follow-up have they not addressed?
Example approach: "You talked about the success, but you didn't mention any challenges. What was the hardest part?"
""")
            
            elif pattern == ReasoningPattern.IP7_CONFLICT:
                instructions.append("""
**IP7 - Conflict/Tension Exploration**
Probe for conflict, failure, disagreement, or tension. This is where real personality reveals itself.
- When did things NOT go well?
- When did they disagree with someone?
- When did their approach fail?
Example approaches:
- "Tell me about a time that approach didn't work."
- "Who pushed back on that, and how did you handle it?"
- "What would your critics say about how you handled that?"
""")
            
            elif pattern == ReasoningPattern.IP11_TRUST:
                instructions.append("""
**IP11 - Trust Calibration**
The candidate is giving self-report ("I'm good at X") rather than behavioral evidence. 
Seek observable, verifiable examples instead of claims.
- Ask for specific instances others could corroborate
- Probe for outcomes and results, not intentions
- Look for what they DID, not what they BELIEVE about themselves
Example approach: "You describe yourself as [trait]. Give me a specific example where someone else would have observed that in action."
""")
            
            elif pattern == ReasoningPattern.MC44_SOLUTION_SPACE:
                instructions.append("""
**MC44 - Solution Space Exploration**
Confidence is low—consider alternative interpretations of what you've heard.
- What if the response means something different than your first read?
- What additional evidence would distinguish between interpretations?
- Generate a probe that tests the alternative hypothesis
Example approach: If they seem collaborative but might be conflict-avoidant, probe: "Tell me about a time you had to push back hard on someone."
""")
            
            elif pattern == ReasoningPattern.SP8_RISK:
                instructions.append("""
**SP8 - Risk Identification**
Probe for failure modes and warning signs.
- What has gone wrong when they applied this trait?
- When has this strength become a weakness?
- What would cause them to fail in this role?
Example approaches:
- "When has your [trait] gotten you into trouble?"
- "What's a time you wish you had done less of [trait]?"
- "What would make you fail in this role?"
""")
            
            elif pattern == ReasoningPattern.SP12_PROJECTION:
                instructions.append("""
**SP12 - Scenario Projection**
Project forward to assess likely future behavior.
- How would they handle a specific situation in this role?
- What would month 3 or month 12 look like?
- Use hypotheticals grounded in role-specific realities
Example approach: "Imagine it's three months in and [realistic scenario]. Walk me through how you'd approach it."
""")
        
        return "\n".join(instructions)
    
    def _format_candidate_context(self, context: ProbeContext) -> str:
        """Format resume and background information."""
        
        sections = []
        
        if context.resume_summary:
            sections.append(f"**Resume Summary:**\n{context.resume_summary}")
        
        if context.role_profile:
            sections.append(f"**Target Role:** {context.role_profile.name}")
            sections.append(f"**Role Category:** {context.role_profile.category}")
            sections.append(f"**Critical Traits:** {', '.join(context.role_profile.critical_traits)}")
        
        if context.candidate_background:
            sections.append(f"**Background Notes:**\n{context.candidate_background}")
        
        return "\n\n".join(sections)
```

### 2.2 Response Analyzer with Pattern-Based Interpretation

```python
# backend/app/services/response_analyzer.py

class PatternAwareResponseAnalyzer:
    """
    Analyzes candidate responses using URP patterns to extract
    evidence and identify gaps.
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    async def analyze_response(
        self,
        response_text: str,
        probe: Probe,
        context: ProbeContext
    ) -> ResponseAnalysis:
        """
        Analyze a response using multiple reasoning patterns.
        """
        
        # Apply IP3: What's missing?
        omission_analysis = await self._analyze_omissions(
            response_text, probe, context
        )
        
        # Apply IP11: Self-report vs. behavioral?
        evidence_classification = await self._classify_evidence_type(
            response_text, probe
        )
        
        # Apply MC44: Alternative interpretations?
        interpretations = await self._generate_alternative_interpretations(
            response_text, probe, context
        )
        
        # Apply MC38: Depth assessment
        depth_assessment = await self._assess_response_depth(
            response_text, probe
        )
        
        # Apply IP7: Tension/conflict present?
        tension_analysis = await self._analyze_tension_presence(
            response_text, probe
        )
        
        return ResponseAnalysis(
            response_text=response_text,
            evidence_items=evidence_classification.evidence_items,
            evidence_type_distribution=evidence_classification.distribution,
            omissions=omission_analysis.omissions,
            response_depth=depth_assessment.depth,
            depth_indicators=depth_assessment.indicators,
            alternative_interpretations=interpretations,
            tension_present=tension_analysis.present,
            tension_details=tension_analysis.details,
            recommended_follow_up_patterns=self._recommend_follow_ups(
                omission_analysis,
                evidence_classification,
                depth_assessment,
                tension_analysis
            )
        )
    
    async def _analyze_omissions(
        self,
        response_text: str,
        probe: Probe,
        context: ProbeContext
    ) -> OmissionAnalysis:
        """Apply IP3: Identify what's NOT in the response."""
        
        prompt = f"""Analyze this interview response for OMISSIONS—what's missing that should be there?

QUESTION ASKED:
{probe.text}

RESPONSE:
{response_text}

EXPECTED ELEMENTS (from probe design):
{probe.evidence_expectations}

TRAIT BEING ASSESSED:
{probe.trait_id}

Identify:
1. Expected elements that are missing
2. Natural follow-up topics they avoided
3. Parts of the question they didn't address
4. Concerning absences (e.g., no mention of results, no specifics, no challenges)

Respond in JSON:
{{
    "omissions": [
        {{
            "expected": "what was expected",
            "assessment": "why its absence matters",
            "follow_up_priority": "HIGH|MEDIUM|LOW"
        }}
    ],
    "overall_completeness": 0.0-1.0
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        return OmissionAnalysis(**result)
    
    async def _classify_evidence_type(
        self,
        response_text: str,
        probe: Probe
    ) -> EvidenceClassification:
        """Apply IP11: Distinguish self-report from behavioral evidence."""
        
        prompt = f"""Classify the evidence in this interview response.

RESPONSE:
{response_text}

For each distinct claim or statement, classify it as:
- BEHAVIORAL: Specific past action with details (names, dates, outcomes)
- OBSERVED: Something demonstrated during this interview
- HYPOTHETICAL: What they would do (not what they did)
- SELF_REPORT: Claim about themselves without behavioral backing
- OPINION: General belief or value statement

BEHAVIORAL evidence is most valuable. SELF_REPORT is least valuable.

Respond in JSON:
{{
    "evidence_items": [
        {{
            "text": "quote or paraphrase",
            "type": "BEHAVIORAL|OBSERVED|HYPOTHETICAL|SELF_REPORT|OPINION",
            "specificity": "HIGH|MEDIUM|LOW",
            "verifiable": true|false
        }}
    ],
    "distribution": {{
        "BEHAVIORAL": 0.0-1.0,
        "SELF_REPORT": 0.0-1.0,
        ...
    }},
    "overall_evidence_quality": "HIGH|MEDIUM|LOW"
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        return EvidenceClassification(**result)
    
    async def _generate_alternative_interpretations(
        self,
        response_text: str,
        probe: Probe,
        context: ProbeContext
    ) -> List[AlternativeInterpretation]:
        """Apply MC44: Generate alternative interpretations of the response."""
        
        prompt = f"""Generate alternative interpretations of this interview response.

CONTEXT:
- Role: {context.role_profile.name}
- Trait being assessed: {probe.trait_id}
- Question asked: {probe.text}

RESPONSE:
{response_text}

The obvious interpretation might not be correct. Generate 2-3 alternative ways to interpret this response:

1. What's the most favorable interpretation?
2. What's the most concerning interpretation?
3. What's a non-obvious interpretation that might be true?

For each, identify what additional evidence would confirm or refute it.

Respond in JSON:
{{
    "interpretations": [
        {{
            "interpretation": "description",
            "valence": "POSITIVE|NEGATIVE|NEUTRAL",
            "probability": 0.0-1.0,
            "confirming_evidence": ["what would confirm this"],
            "refuting_evidence": ["what would refute this"]
        }}
    ]
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        return [AlternativeInterpretation(**i) for i in result["interpretations"]]
    
    async def _assess_response_depth(
        self,
        response_text: str,
        probe: Probe
    ) -> DepthAssessment:
        """Apply MC38: Assess the depth/abstraction level of the response."""
        
        prompt = f"""Assess the depth of this interview response.

QUESTION:
{probe.text}

RESPONSE:
{response_text}

Rate the response depth:
- SURFACE: General statements, no specifics, could apply to anyone
- MODERATE: Some specifics, but missing key details
- DEEP: Rich in specifics—names, dates, numbers, concrete actions, clear outcomes

Identify specific indicators of depth or shallowness.

Respond in JSON:
{{
    "depth": "SURFACE|MODERATE|DEEP",
    "indicators": {{
        "depth_signals": ["specific indicators of depth"],
        "shallowness_signals": ["specific indicators of shallowness"]
    }},
    "missing_specifics": ["what specific details are missing"]
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        return DepthAssessment(**result)
    
    async def _analyze_tension_presence(
        self,
        response_text: str,
        probe: Probe
    ) -> TensionAnalysis:
        """Apply IP7: Check for presence of conflict/tension/failure."""
        
        prompt = f"""Analyze this response for tension, conflict, failure, or challenge.

RESPONSE:
{response_text}

Does the response include:
- Conflict with others (disagreement, pushback, friction)
- Personal failure or mistake
- Challenges or obstacles overcome
- Difficult decisions or tradeoffs
- Negative outcomes or lessons learned

These elements are VALUABLE—they reveal how someone handles difficulty.
Absence of any tension in a behavioral example is a yellow flag.

Respond in JSON:
{{
    "present": true|false,
    "details": {{
        "conflicts": ["any interpersonal conflicts mentioned"],
        "failures": ["any failures or mistakes"],
        "challenges": ["any challenges overcome"],
        "tradeoffs": ["any difficult decisions"],
        "lessons": ["any lessons learned"]
    }},
    "assessment": "How meaningful is the tension present (or how concerning is its absence)?"
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        return TensionAnalysis(**result)
    
    def _recommend_follow_ups(
        self,
        omission_analysis: OmissionAnalysis,
        evidence_classification: EvidenceClassification,
        depth_assessment: DepthAssessment,
        tension_analysis: TensionAnalysis
    ) -> List[ReasoningPattern]:
        """Determine which patterns to apply for follow-up probes."""
        
        recommendations = []
        
        # If significant omissions, probe them
        if omission_analysis.overall_completeness < 0.7:
            recommendations.append(ReasoningPattern.IP3_ACTIVE_LISTENING)
        
        # If too much self-report, seek behavioral evidence
        if evidence_classification.distribution.get("SELF_REPORT", 0) > 0.5:
            recommendations.append(ReasoningPattern.IP11_TRUST)
        
        # If shallow response, go deeper
        if depth_assessment.depth == "SURFACE":
            recommendations.append(ReasoningPattern.MC38_ABSTRACTION)
        
        # If no tension present, probe for it
        if not tension_analysis.present:
            recommendations.append(ReasoningPattern.IP7_CONFLICT)
        
        return recommendations
```

### 2.3 Resume-Informed Probe Customization

```python
# backend/app/services/resume_probe_customizer.py

class ResumeInformedProbeCustomizer:
    """
    Customizes probes based on specific details from the candidate's resume.
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    async def customize_probe_for_resume(
        self,
        base_probe: Probe,
        resume_data: ResumeData,
        trait_id: str
    ) -> Probe:
        """
        Take a generic probe and customize it using resume details.
        
        Example:
        Generic: "Tell me about a time you had to adapt quickly."
        Customized: "At Amazon, you moved from Kindle to Echo teams. 
                    Tell me about a time during that transition when 
                    you had to adapt your approach quickly."
        """
        
        prompt = f"""Customize this interview probe using specific details from the candidate's resume.

GENERIC PROBE:
{base_probe.text}

TRAIT BEING ASSESSED:
{trait_id}

RESUME DETAILS:
- Companies: {resume_data.companies}
- Roles: {resume_data.roles}
- Key projects: {resume_data.key_projects}
- Technologies: {resume_data.technologies}
- Transitions/changes: {resume_data.transitions}
- Achievements: {resume_data.achievements}

CUSTOMIZATION GOALS:
1. Reference specific companies, projects, or transitions from their background
2. Make the probe impossible to answer with a generic, rehearsed response
3. Show the candidate you've read their resume (builds rapport)
4. Anchor the question to their actual experience

Generate a customized version that probes the same trait but uses their specific background.

Respond in JSON:
{{
    "customized_question": "The customized probe text",
    "resume_anchors_used": ["specific resume elements referenced"],
    "customization_rationale": "why these anchors were chosen"
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        
        return Probe(
            text=result["customized_question"],
            trait_id=trait_id,
            patterns_applied=base_probe.patterns_applied,
            generation_rationale=result["customization_rationale"],
            resume_anchors=result["resume_anchors_used"],
            base_probe_id=base_probe.id
        )
    
    async def identify_resume_based_probes(
        self,
        resume_data: ResumeData,
        role_profile: RoleProfile
    ) -> List[ResumeBasedProbeOpportunity]:
        """
        Identify specific resume elements that could anchor trait-revealing probes.
        
        Applies MC1 (Stakeholder Mapping) to understand the candidate's history.
        """
        
        prompt = f"""Analyze this resume to identify probe opportunities for each trait.

RESUME:
{resume_data.full_text}

TARGET ROLE:
{role_profile.name} ({role_profile.category})

TRAITS TO ASSESS:
{[t.trait_id for t in role_profile.trait_config]}

For each trait, identify specific resume elements that could anchor a probe:
- Job transitions (test ADAPTABILITY)
- Leadership mentions (test INITIATIVE, COLLABORATION)
- Project failures or pivots (test RESILIENCE, ADAPTABILITY)
- Skill gaps filled (test CURIOSITY, LEARNING_ORIENTATION)
- Cross-functional work (test COMMUNICATION, COLLABORATION)
- Promotions/growth (test ACHIEVEMENT_ORIENTATION)

Respond in JSON:
{{
    "probe_opportunities": [
        {{
            "trait_id": "ADAPTABILITY",
            "resume_element": "Moved from engineering to product role at Company X",
            "probe_angle": "Probe how they navigated the skill gap and identity shift",
            "suggested_question": "When you moved from engineering to product at X, what was the hardest part of that transition?"
        }}
    ]
}}
"""
        
        result = await self.llm.complete(prompt, response_format="json")
        return [ResumeBasedProbeOpportunity(**p) for p in result["probe_opportunities"]]
```

### 2.4 Adaptive Interview Strategy

```python
# backend/app/services/interview_strategist.py

class AdaptiveInterviewStrategist:
    """
    Applies MC29 (Progress Monitoring) to dynamically adjust
    interview strategy based on signal quality.
    """
    
    def __init__(self):
        self.signal_thresholds = {
            "STRONG": 0.8,
            "ADEQUATE": 0.6,
            "WEAK": 0.4
        }
    
    def assess_interview_progress(
        self,
        session: InterviewSession
    ) -> InterviewProgressAssessment:
        """
        Assess overall interview progress and recommend strategy adjustments.
        """
        
        trait_statuses = []
        
        for trait_id in session.traits_to_assess:
            evidence = session.evidence_for_trait(trait_id)
            
            status = TraitAssessmentStatus(
                trait_id=trait_id,
                evidence_count=len(evidence),
                behavioral_evidence_count=len([e for e in evidence if e.type == "BEHAVIORAL"]),
                confidence=self._calculate_confidence(evidence),
                signal_quality=self._assess_signal_quality(evidence),
                gaps=self._identify_gaps(evidence, trait_id)
            )
            trait_statuses.append(status)
        
        # Overall assessment
        overall_confidence = sum(t.confidence for t in trait_statuses) / len(trait_statuses)
        weak_traits = [t for t in trait_statuses if t.signal_quality == "WEAK"]
        
        return InterviewProgressAssessment(
            trait_statuses=trait_statuses,
            overall_confidence=overall_confidence,
            weak_traits=weak_traits,
            time_elapsed=session.duration_minutes,
            recommended_focus=self._recommend_focus(trait_statuses),
            strategy_adjustments=self._recommend_adjustments(trait_statuses, session)
        )
    
    def _recommend_adjustments(
        self,
        trait_statuses: List[TraitAssessmentStatus],
        session: InterviewSession
    ) -> List[StrategyAdjustment]:
        """
        Recommend specific adjustments based on MC29 progress monitoring.
        """
        
        adjustments = []
        
        # If a trait has only self-report evidence, switch to behavioral probing
        for status in trait_statuses:
            if status.behavioral_evidence_count == 0 and status.evidence_count > 0:
                adjustments.append(StrategyAdjustment(
                    trait_id=status.trait_id,
                    adjustment="SWITCH_TO_BEHAVIORAL",
                    rationale="Only self-report evidence collected; need behavioral examples",
                    pattern_to_apply=ReasoningPattern.IP11_TRUST
                ))
        
        # If responses are consistently shallow, increase depth
        shallow_count = sum(1 for e in session.all_evidence if e.depth == "SURFACE")
        if shallow_count > len(session.all_evidence) * 0.5:
            adjustments.append(StrategyAdjustment(
                adjustment="INCREASE_DEPTH",
                rationale="Too many surface-level responses",
                pattern_to_apply=ReasoningPattern.MC38_ABSTRACTION
            ))
        
        # If no failure/conflict stories yet, probe for tension
        tension_evidence = [e for e in session.all_evidence if e.contains_tension]
        if len(tension_evidence) == 0 and session.duration_minutes > 15:
            adjustments.append(StrategyAdjustment(
                adjustment="PROBE_TENSION",
                rationale="No failure or conflict examples collected",
                pattern_to_apply=ReasoningPattern.IP7_CONFLICT
            ))
        
        # If running low on time, prioritize weak traits
        if session.duration_minutes > 30 and len([t for t in trait_statuses if t.confidence < 0.5]) > 2:
            adjustments.append(StrategyAdjustment(
                adjustment="PRIORITIZE_WEAK_TRAITS",
                rationale="Limited time remaining; focus on traits with insufficient signal",
                focus_traits=[t.trait_id for t in trait_statuses if t.confidence < 0.5]
            ))
        
        return adjustments
```

---

## Part 3: System Prompts for LLM Integration

### 3.1 Master Interview System Prompt

```python
INTERVIEW_SYSTEM_PROMPT = """You are an expert behavioral interviewer conducting a structured assessment. Your goal is to gather high-quality behavioral evidence to assess personality traits.

## YOUR APPROACH

You apply these reasoning patterns:

1. **MC24 (Assumption Surfacing)**: Don't accept surface answers. Probe beneath what candidates say to understand what they actually do.

2. **IP7 (Conflict/Tension Exploration)**: The best evidence comes from difficulty. Always probe for failures, disagreements, and challenges.

3. **IP11 (Trust Calibration)**: Value behavioral evidence ("I did X, and Y happened") over self-report ("I'm good at X"). When you hear self-report, ask for a specific example.

4. **MC38 (Abstraction Level)**: Go deeper. Ask for specific names, dates, numbers, and outcomes. General answers are low-signal.

5. **IP3 (Active Listening)**: Notice what's NOT said. If a candidate doesn't mention challenges, results, or specific actions, probe for those gaps.

## EVIDENCE HIERARCHY

Strongest → Weakest:
1. OBSERVED: Demonstrated in this interview
2. BEHAVIORAL: Specific past action with details
3. HYPOTHETICAL: What they would do
4. SELF-REPORT: Claims about themselves

Your job is to convert self-report and hypothetical into behavioral evidence.

## STAR+ METHODOLOGY

For each example, ensure you get:
- **S**ituation: What was the context?
- **T**ask: What was their specific responsibility?
- **A**ction: What did THEY do (not the team)?
- **R**esult: What happened?
- **+Reflection**: What would they do differently?

If any element is missing, probe for it before moving on.

## CANDIDATE RAPPORT

While probing deeply, maintain warmth and curiosity. You're genuinely interested in understanding them, not interrogating them. Use their specific background (from resume) to personalize questions.
"""
```

### 3.2 Training Session System Prompt

```python
TRAINING_SESSION_SYSTEM_PROMPT = """You are conducting a training content development session with a top performer. Your goal is to extract insights about what makes someone successful in their role.

## YOUR FRAMING

You are NOT evaluating them. You are learning from them to help train others. Position them as the expert.

## YOUR APPROACH

You apply these reasoning patterns:

1. **MC1 (Stakeholder Mapping)**: Understand who this person is—their experience, perspective, and expertise areas.

2. **MC24 (Assumption Surfacing)**: Uncover the non-obvious things. Ask "What would people NOT expect to matter?" and "What looks right but actually fails?"

3. **SP8 (Risk Identification)**: Extract failure patterns. "What type of person struggles in this role?" reveals counter-indicators.

4. **MC35 (Representation Choice)**: Understand how success manifests in THIS specific role context.

## EXTRACTION QUESTIONS

Use questions like:
- "Walk me through how you'd approach this..."
- "What would a new person typically get wrong?"
- "What's the non-obvious thing that makes a difference?"
- "What type of person consistently fails in this role?"
- "What trait looks good on paper but actually hurts?"

## DUAL OUTPUT

You're generating:
1. **Trait signals**: What characteristics matter for this role
2. **Training content**: Actual advice for onboarding new hires

Both are valuable. Capture the expert's wisdom in their own words.
"""
```

---

## Part 4: Integration Points

### 4.1 Interview Engine Integration

Update the `InterviewEngine` class from the main development spec:

```python
# In backend/app/services/interview_engine.py

class InterviewEngine:
    def __init__(
        self,
        llm_client: LLMClient,
        trait_extractor: TraitExtractor,
        probe_generator: PatternAwareProbeGenerator,  # ADD
        response_analyzer: PatternAwareResponseAnalyzer,  # ADD
        resume_customizer: ResumeInformedProbeCustomizer,  # ADD
        strategist: AdaptiveInterviewStrategist  # ADD
    ):
        self.llm = llm_client
        self.extractor = trait_extractor
        self.probe_generator = probe_generator
        self.response_analyzer = response_analyzer
        self.resume_customizer = resume_customizer
        self.strategist = strategist
    
    async def generate_next_probe(
        self,
        session: InterviewSession,
        trait_id: str,
        rubric_item: RubricItem
    ) -> Probe:
        """Generate contextually intelligent next probe."""
        
        # Build context from session state
        context = self._build_probe_context(session)
        
        # Determine which patterns to apply
        patterns = await self.probe_generator.select_patterns_for_context(
            trait_id=trait_id,
            context=context
        )
        
        # Generate pattern-informed probe
        probe = await self.probe_generator.generate_probe(
            trait_id=trait_id,
            context=context,
            patterns_to_apply=patterns
        )
        
        # Customize with resume details if available
        if context.resume_data:
            probe = await self.resume_customizer.customize_probe_for_resume(
                base_probe=probe,
                resume_data=context.resume_data,
                trait_id=trait_id
            )
        
        return probe
    
    async def process_response(
        self,
        db: AsyncSession,
        session: InterviewSession,
        response_text: str
    ) -> InterviewSession:
        """Process response with pattern-based analysis."""
        
        # Get current probe context
        current_probe = session.get_current_probe()
        context = self._build_probe_context(session)
        
        # Analyze response using patterns
        analysis = await self.response_analyzer.analyze_response(
            response_text=response_text,
            probe=current_probe,
            context=context
        )
        
        # Update session with analysis
        session.add_response(response_text, analysis)
        
        # Check interview progress (MC29)
        progress = self.strategist.assess_interview_progress(session)
        
        # Apply any strategy adjustments
        for adjustment in progress.strategy_adjustments:
            session.apply_adjustment(adjustment)
        
        # Determine next action based on analysis and progress
        next_action = self._determine_next_action(
            session=session,
            analysis=analysis,
            progress=progress
        )
        
        # Generate next probe if continuing
        if next_action["type"] in ["FOLLOW_UP", "NEXT_TRAIT"]:
            next_probe = await self.generate_next_probe(
                session=session,
                trait_id=next_action.get("trait_id", current_probe.trait_id),
                rubric_item=session.rubric.get_item(next_action.get("trait_id", current_probe.trait_id))
            )
            session.set_current_probe(next_probe)
        
        await db.commit()
        return session
```

### 4.2 Configuration

Add pattern configuration to organization settings:

```python
# In backend/app/schemas/settings.py

class InterviewPatternSettings(BaseModel):
    """Configure which patterns are enabled and their aggressiveness."""
    
    # Pattern enablement
    enable_assumption_surfacing: bool = True  # MC24
    enable_conflict_probing: bool = True  # IP7
    enable_depth_escalation: bool = True  # MC38
    enable_omission_detection: bool = True  # IP3
    enable_alternative_interpretations: bool = True  # MC44
    
    # Aggressiveness settings
    max_follow_ups_per_trait: int = 3
    minimum_behavioral_evidence: int = 1
    require_tension_example: bool = False
    depth_escalation_threshold: str = "SURFACE"  # When to push deeper
    
    # Resume customization
    enable_resume_customization: bool = True
    max_resume_anchors_per_probe: int = 2
```

---

## Part 5: Testing Pattern Integration

### 5.1 Test Cases

```python
# backend/tests/test_services/test_probe_generator.py

import pytest
from app.services.probe_generator import PatternAwareProbeGenerator, ReasoningPattern

class TestPatternAwareProbeGenerator:
    
    @pytest.mark.asyncio
    async def test_mc24_assumption_surfacing_probe(self, probe_generator, mock_context):
        """Test that MC24 generates assumption-challenging probes."""
        
        probe = await probe_generator.generate_probe(
            trait_id="CURIOSITY",
            context=mock_context,
            patterns_to_apply=[ReasoningPattern.MC24_ASSUMPTION]
        )
        
        # Probe should challenge assumptions
        assert any(word in probe.text.lower() for word in 
                   ["actually", "really", "specific example", "test", "challenged"])
        assert "rationale" in probe.generation_rationale
    
    @pytest.mark.asyncio
    async def test_ip7_conflict_probe_after_smooth_response(
        self, probe_generator, mock_context_smooth_response
    ):
        """Test that IP7 probes for conflict when response lacks tension."""
        
        probe = await probe_generator.generate_probe(
            trait_id="ADAPTABILITY",
            context=mock_context_smooth_response,
            patterns_to_apply=[ReasoningPattern.IP7_CONFLICT]
        )
        
        # Probe should seek tension
        assert any(word in probe.text.lower() for word in 
                   ["fail", "wrong", "difficult", "disagree", "pushback", "challenge"])
    
    @pytest.mark.asyncio
    async def test_ip11_behavioral_probe_after_self_report(
        self, probe_generator, mock_context_self_report
    ):
        """Test that IP11 seeks behavioral evidence after self-report."""
        
        probe = await probe_generator.generate_probe(
            trait_id="INITIATIVE",
            context=mock_context_self_report,
            patterns_to_apply=[ReasoningPattern.IP11_TRUST]
        )
        
        # Probe should request specific example
        assert any(phrase in probe.text.lower() for phrase in 
                   ["specific example", "tell me about a time", "walk me through"])
    
    @pytest.mark.asyncio
    async def test_pattern_selection_for_low_confidence(
        self, probe_generator, mock_context_low_confidence
    ):
        """Test that MC44 is selected when confidence is low."""
        
        patterns = await probe_generator.select_patterns_for_context(
            trait_id="COLLABORATION",
            context=mock_context_low_confidence
        )
        
        assert ReasoningPattern.MC44_SOLUTION_SPACE in patterns
```

---

## Summary

This supplement specifies:

1. **Which URP patterns** to use for probe generation and response analysis
2. **How to implement** pattern-aware services (ProbeGenerator, ResponseAnalyzer)
3. **Resume customization** to make probes specific to each candidate
4. **Adaptive strategy** using MC29 to adjust mid-interview
5. **System prompts** that encode the patterns for LLM use
6. **Integration points** with the main InterviewEngine
7. **Test cases** to verify pattern behavior

The key insight: **Static question banks produce generic, gameable interviews. Pattern-based generation produces contextually intelligent probes that adapt to each candidate's background and responses.**

---

*Document Version 1.0 | AP API Reasoning Pattern Integration*
*Supplement to: AP API Development Specification*
*© 2026 Tucuxi Inc. All rights reserved.*
