"""
Sage-Mode Teaching and Calibration Dialogue Templates
======================================================

Templates for the mentoring module to:
1. Explain cognitive budget choices
2. Calibrate with users on appropriate analysis depth
3. Teach cognitive efficiency principles
4. Provide progressive disclosure of reasoning levels

Part of the FLO Cognitive Apprentice System.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Dict, Any
from string import Template

from situation_classifier import CognitiveMode, SituationAssessment, ClassificationResult


# =============================================================================
# DIALOGUE TYPES
# =============================================================================

class DialogueType(Enum):
    """Types of teaching/calibration dialogues."""
    EXPLAIN_CHOICE = auto()        # Explain why a mode was chosen
    CALIBRATION_PROMPT = auto()    # Ask user to calibrate depth preference
    PROGRESSIVE_DISCLOSURE = auto() # Show reasoning at each level
    ESCALATION_NOTICE = auto()     # Explain mode shift during execution
    EFFICIENCY_TEACHING = auto()   # Teach cognitive budgeting principles
    BUDGET_SUMMARY = auto()        # Summarize cognitive budget usage
    PATTERN_HIGHLIGHT = auto()     # Highlight specific patterns being used


class TeachingTone(Enum):
    """Tone for teaching dialogues."""
    CONCISE = auto()       # Minimal explanation
    STANDARD = auto()      # Normal teaching
    DETAILED = auto()       # Comprehensive explanation
    SOCRATIC = auto()      # Question-based teaching


# =============================================================================
# TEMPLATE STRUCTURES
# =============================================================================

@dataclass
class DialogueTemplate:
    """A teaching dialogue template with placeholders."""
    dialogue_type: DialogueType
    template: str
    variables: List[str]
    tone: TeachingTone = TeachingTone.STANDARD
    follow_up_options: List[str] = field(default_factory=list)

    def render(self, **kwargs) -> str:
        """Render template with provided variables."""
        t = Template(self.template)
        return t.safe_substitute(**kwargs)


# =============================================================================
# EXPLAIN CHOICE TEMPLATES
# =============================================================================

EXPLAIN_CHOICE_TEMPLATES = {
    CognitiveMode.REFLEX: DialogueTemplate(
        dialogue_type=DialogueType.EXPLAIN_CHOICE,
        template="""
**Cognitive Mode: REFLEX** (Budget 1/5)

I'm using pattern matching for this because:
- $primary_reason
- $secondary_reason

**Why not deeper analysis?**
$why_not_deeper

**Key Pattern Applied:** $pattern_applied

$teaching_point
""",
        variables=['primary_reason', 'secondary_reason', 'why_not_deeper', 'pattern_applied', 'teaching_point'],
        follow_up_options=[
            "Want me to go deeper anyway?",
            "What would make this warrant more analysis?",
            "Show me similar situations that needed more depth"
        ]
    ),

    CognitiveMode.COMPETENT: DialogueTemplate(
        dialogue_type=DialogueType.EXPLAIN_CHOICE,
        template="""
**Cognitive Mode: COMPETENT** (Budget 2/5)

I'm applying standard professional analysis:
- $structural_patterns
- $risk_assessment

**Assessment Scores:**
- Stakes: $stakes_score/5 ($stakes_rationale)
- Complexity: $complexity_score/5 ($complexity_rationale)
- Reversibility: $reversibility_score/5
- Time: $time_score/5

**Why this depth is appropriate:**
$depth_rationale

$teaching_point
""",
        variables=['structural_patterns', 'risk_assessment', 'stakes_score', 'stakes_rationale',
                   'complexity_score', 'complexity_rationale', 'reversibility_score', 'time_score',
                   'depth_rationale', 'teaching_point'],
        follow_up_options=[
            "Should I consider additional stakeholders?",
            "What would escalate this to EXPERT mode?"
        ]
    ),

    CognitiveMode.EXPERT: DialogueTemplate(
        dialogue_type=DialogueType.EXPLAIN_CHOICE,
        template="""
**Cognitive Mode: EXPERT** (Budget 3/5)

Full professional judgment with stakeholder awareness:

**Stakeholders Identified:**
$stakeholder_list

**Patterns Applied:**
- Tier 1 (Structural): $tier1_patterns
- Tier 2 (Behavioral): $tier2_patterns
- Meta-Cognitive (implicit): $mc_patterns

**Assessment:** $assessment_summary

**Why not MASTER mode?**
$why_not_master

$teaching_point
""",
        variables=['stakeholder_list', 'tier1_patterns', 'tier2_patterns', 'mc_patterns',
                   'assessment_summary', 'why_not_master', 'teaching_point'],
        follow_up_options=[
            "Should I model stakeholder mental states explicitly?",
            "Are there sophisticated actors I should model more deeply?"
        ]
    ),

    CognitiveMode.MASTER: DialogueTemplate(
        dialogue_type=DialogueType.EXPLAIN_CHOICE,
        template="""
**Cognitive Mode: MASTER** (Budget 4/5)

Explicit strategic reasoning with full stakeholder modeling:

**Stakeholder Mental Models (MC1):**
$mental_models

**Trajectory Forecasting (MC2):**
$trajectories

**Strategic Framing (MC3):**
$framing_strategy

**Coalition Analysis (MC6):**
$coalition_analysis

**Reputation Considerations (MC7):**
$reputation_check

**Information Strategy (MC8):**
$information_strategy

**Why MASTER and not SAGE?**
$why_not_sage

$teaching_point
""",
        variables=['mental_models', 'trajectories', 'framing_strategy', 'coalition_analysis',
                   'reputation_check', 'information_strategy', 'why_not_sage', 'teaching_point'],
        follow_up_options=[
            "Should I apply deeper recursive modeling?",
            "What would this situation look like with SAGE-level analysis?"
        ]
    ),

    CognitiveMode.SAGE: DialogueTemplate(
        dialogue_type=DialogueType.EXPLAIN_CHOICE,
        template="""
**Cognitive Mode: SAGE** (Budget 5/5)

Deep recursive analysis with meta-cognitive wisdom:

**Recursive Intention Modeling (MC4 - Level $recursion_level):**
$recursive_analysis

**Uncertainty Quantification:**
$uncertainty_analysis

**What Analysis Cannot Capture:**
$analysis_limits

**Meta-Wisdom Check:**
- Am I over-analyzing? $overanalysis_check
- What might I be missing? $blind_spots
- Should I trust intuition here? $intuition_check

**Scenario Exploration:**
$scenarios

**Final Recommendation with Humility:**
$recommendation

$teaching_point
""",
        variables=['recursion_level', 'recursive_analysis', 'uncertainty_analysis',
                   'analysis_limits', 'overanalysis_check', 'blind_spots', 'intuition_check',
                   'scenarios', 'recommendation', 'teaching_point'],
        follow_up_options=[
            "What's your confidence in this analysis?",
            "What would change your recommendation?"
        ]
    ),
}


# =============================================================================
# CALIBRATION PROMPT TEMPLATES
# =============================================================================

CALIBRATION_PROMPTS = {
    'mode_mismatch': DialogueTemplate(
        dialogue_type=DialogueType.CALIBRATION_PROMPT,
        template="""
**Calibration Check**

You've requested: "$user_request"

My initial assessment suggests **$suggested_mode** mode:
$assessment_summary

However, I want to calibrate with you:

$calibration_question

**Options:**
A) $option_a
B) $option_b
C) $option_c

Which approach would you prefer?
""",
        variables=['user_request', 'suggested_mode', 'assessment_summary',
                   'calibration_question', 'option_a', 'option_b', 'option_c']
    ),

    'stakes_clarification': DialogueTemplate(
        dialogue_type=DialogueType.CALIBRATION_PROMPT,
        template="""
**Stakes Clarification Needed**

I'm assessing this as **$assessed_stakes** stakes, but I want to verify:

$context_description

**Questions that affect analysis depth:**
1. $question_1
2. $question_2
3. $question_3

Your answers will help me calibrate the appropriate cognitive investment.
""",
        variables=['assessed_stakes', 'context_description', 'question_1', 'question_2', 'question_3']
    ),

    'time_preference': DialogueTemplate(
        dialogue_type=DialogueType.CALIBRATION_PROMPT,
        template="""
**Analysis Depth vs. Time Trade-off**

This situation could warrant **$full_analysis_mode** mode analysis, which would:
- Take approximately $estimated_time
- Cover: $full_coverage

Alternatively, I can provide **$quick_mode** mode analysis:
- Available immediately
- Trade-offs: $quick_tradeoffs

**What's your preference given your constraints?**
""",
        variables=['full_analysis_mode', 'estimated_time', 'full_coverage',
                   'quick_mode', 'quick_tradeoffs']
    ),

    'sophistication_check': DialogueTemplate(
        dialogue_type=DialogueType.CALIBRATION_PROMPT,
        template="""
**Counterparty Sophistication Check**

How sophisticated is $counterparty in strategic thinking?

A) **Standard** - Will react to proposals at face value
B) **Experienced** - Will think one step ahead, model your basic interests
C) **Sophisticated** - Will model what you think they want, play multi-level games
D) **Expert** - Top-tier negotiator, multiple levels of recursive modeling

This determines whether I need to activate deep recursive modeling (MC4).
""",
        variables=['counterparty']
    ),
}


# =============================================================================
# PROGRESSIVE DISCLOSURE TEMPLATES
# =============================================================================

PROGRESSIVE_DISCLOSURE_TEMPLATE = DialogueTemplate(
    dialogue_type=DialogueType.PROGRESSIVE_DISCLOSURE,
    template="""
**Progressive Analysis: $situation_summary**

---

**LEVEL 1 - REFLEX Response:**
> $level1_response

---

**LEVEL 2 - COMPETENT Analysis:**
$level2_analysis

---

**LEVEL 3 - EXPERT Judgment:**
$level3_analysis

---

**LEVEL 4 - MASTER Strategy:**
$level4_analysis

---

**LEVEL 5 - SAGE Wisdom:**
$level5_analysis

---

**Teaching Summary:**
$teaching_summary
""",
    variables=['situation_summary', 'level1_response', 'level2_analysis',
               'level3_analysis', 'level4_analysis', 'level5_analysis', 'teaching_summary']
)


# =============================================================================
# ESCALATION NOTICE TEMPLATES
# =============================================================================

ESCALATION_NOTICE_TEMPLATES = {
    'escalation': DialogueTemplate(
        dialogue_type=DialogueType.ESCALATION_NOTICE,
        template="""
**Mode Shift: $from_mode → $to_mode**

I'm increasing analysis depth because:
- **Trigger:** $trigger_type
- **Evidence:** $evidence

**What this means:**
$what_changes

**Patterns now active:**
$new_patterns

**Teaching Point:**
$teaching_point
""",
        variables=['from_mode', 'to_mode', 'trigger_type', 'evidence',
                   'what_changes', 'new_patterns', 'teaching_point']
    ),

    'de_escalation': DialogueTemplate(
        dialogue_type=DialogueType.ESCALATION_NOTICE,
        template="""
**Mode Shift: $from_mode → $to_mode**

I'm reducing analysis depth because:
- **Trigger:** $trigger_type
- **Evidence:** $evidence

**Why this is appropriate:**
$rationale

**Teaching Point:**
$teaching_point
""",
        variables=['from_mode', 'to_mode', 'trigger_type', 'evidence',
                   'rationale', 'teaching_point']
    ),
}


# =============================================================================
# EFFICIENCY TEACHING TEMPLATES
# =============================================================================

EFFICIENCY_TEACHING_TEMPLATES = {
    'over_investment': DialogueTemplate(
        dialogue_type=DialogueType.EFFICIENCY_TEACHING,
        template="""
**Cognitive Efficiency Note**

I notice you've been using $high_mode mode for tasks that typically warrant $appropriate_mode:

$examples

**The Cost:**
- Each $high_mode analysis uses ~$cost_multiplier cognitive resources
- Over $time_period, this accumulated to $total_cost

**The Insight:**
$insight

**Suggestion:**
Learn to recognize $recognition_signals as indicators that $appropriate_mode is sufficient.
""",
        variables=['high_mode', 'appropriate_mode', 'examples', 'cost_multiplier',
                   'time_period', 'total_cost', 'insight', 'recognition_signals']
    ),

    'under_investment': DialogueTemplate(
        dialogue_type=DialogueType.EFFICIENCY_TEACHING,
        template="""
**Risk Alert: Under-Investment Detected**

This situation has characteristics that typically warrant deeper analysis:
$warning_signals

However, current analysis is at **$current_mode** level.

**Potential Risks:**
$risks

**Recommendation:**
Consider escalating to **$recommended_mode** because:
$recommendation_rationale
""",
        variables=['warning_signals', 'current_mode', 'risks', 'recommended_mode',
                   'recommendation_rationale']
    ),

    'optimal_investment': DialogueTemplate(
        dialogue_type=DialogueType.EFFICIENCY_TEACHING,
        template="""
**Efficiency Recognition**

This was an excellent example of cognitive budget optimization:

**Situation:** $situation
**Mode Used:** $mode_used
**Why Optimal:** $why_optimal

**Pattern to Remember:**
When you see $recognition_pattern, this level of analysis is appropriate.
""",
        variables=['situation', 'mode_used', 'why_optimal', 'recognition_pattern']
    ),
}


# =============================================================================
# BUDGET SUMMARY TEMPLATES
# =============================================================================

BUDGET_SUMMARY_TEMPLATE = DialogueTemplate(
    dialogue_type=DialogueType.BUDGET_SUMMARY,
    template="""
**Cognitive Budget Summary: $session_name**

**Duration:** $duration
**Tasks Completed:** $task_count

---

**Budget Allocation:**
```
$budget_table
```

**Efficiency Metrics:**
- Total Budget Used: $total_budget
- High-Investment Tasks: $high_investment_count ($high_investment_percent)
- Budget Efficiency Score: $efficiency_score

**Analysis:**
$efficiency_analysis

**Patterns Observed:**
$patterns_observed

**Recommendations:**
$recommendations
""",
    variables=['session_name', 'duration', 'task_count', 'budget_table',
               'total_budget', 'high_investment_count', 'high_investment_percent',
               'efficiency_score', 'efficiency_analysis', 'patterns_observed', 'recommendations']
)


# =============================================================================
# DIALOGUE GENERATOR
# =============================================================================

class TeachingDialogueGenerator:
    """
    Generates teaching dialogues based on context and classification results.
    """

    def __init__(self, tone: TeachingTone = TeachingTone.STANDARD):
        self.tone = tone

    def generate_explain_choice(
        self,
        result: ClassificationResult
    ) -> str:
        """Generate explanation of mode choice."""

        template = EXPLAIN_CHOICE_TEMPLATES.get(result.mode)
        if not template:
            return f"Using {result.mode.name} mode for this situation."

        # Build variables based on mode
        variables = self._build_explain_variables(result)
        return template.render(**variables)

    def _build_explain_variables(self, result: ClassificationResult) -> Dict[str, str]:
        """Build template variables for explain choice dialogue."""

        assessment = result.assessment

        # Common variables
        base_vars = {
            'stakes_score': str(assessment.stakes.value),
            'stakes_rationale': assessment.stakes.name.replace('_', ' ').lower(),
            'complexity_score': str(assessment.complexity.value),
            'complexity_rationale': assessment.complexity.name.replace('_', ' ').lower(),
            'reversibility_score': str(assessment.reversibility.value),
            'time_score': str(assessment.time_pressure.value),
        }

        # Mode-specific variables
        mode_vars = {
            CognitiveMode.REFLEX: {
                'primary_reason': 'This is a routine question with established patterns',
                'secondary_reason': 'Stakes are low and reversible',
                'why_not_deeper': 'The cost of deeper analysis exceeds potential benefit',
                'pattern_applied': 'Template matching / direct retrieval',
                'teaching_point': '**Teaching:** Recognize when problems are "solved problems" - apply the pattern and move on.'
            },
            CognitiveMode.COMPETENT: {
                'structural_patterns': 'Standard risk identification and provision review',
                'risk_assessment': 'Checking key provisions against known patterns',
                'depth_rationale': 'Stakes and complexity don\'t justify deeper stakeholder modeling',
                'teaching_point': '**Teaching:** Most routine professional work falls here. Master pattern recognition to handle these efficiently.'
            },
            CognitiveMode.EXPERT: {
                'stakeholder_list': '\n'.join([f'- {s}' for s in (assessment.stakeholders or ['Primary parties identified'])]),
                'tier1_patterns': 'Full structural analysis',
                'tier2_patterns': 'Behavioral pattern consideration',
                'mc_patterns': 'Implicit stakeholder awareness',
                'assessment_summary': 'Moderate complexity with identifiable stakeholder dynamics',
                'why_not_master': 'Stakeholder sophistication doesn\'t require recursive modeling',
                'teaching_point': '**Teaching:** Expert mode adds stakeholder awareness without full strategic depth.'
            },
            CognitiveMode.MASTER: {
                'mental_models': 'Building explicit models of each stakeholder\'s goals, constraints, and beliefs',
                'trajectories': 'Predicting how stakeholders will respond to proposed actions',
                'framing_strategy': 'Designing communication for maximum effectiveness',
                'coalition_analysis': 'Mapping who can be aligned and at what cost',
                'reputation_check': 'Ensuring actions protect long-term credibility',
                'information_strategy': 'Planning what to reveal when',
                'why_not_sage': 'Depth of recursive modeling is sufficient; no need for level 3+ recursion',
                'teaching_point': '**Teaching:** Master mode is for high-stakes situations with sophisticated actors.'
            },
            CognitiveMode.SAGE: {
                'recursion_level': '3+',
                'recursive_analysis': 'Modeling what they think we think they want...',
                'uncertainty_analysis': 'Explicit identification of irreducible uncertainties',
                'analysis_limits': 'Personal chemistry, random events, factors beyond systematic analysis',
                'overanalysis_check': 'No - stakes justify this depth',
                'blind_spots': 'Actively considering what might be missed',
                'intuition_check': 'Balancing analytical conclusions with intuitive signals',
                'scenarios': 'Multiple future scenarios with probability estimates',
                'recommendation': 'Recommendation with appropriate confidence bounds',
                'teaching_point': '**Teaching:** Sage mode includes knowing when to stop analyzing. The highest wisdom is recognizing limits.'
            }
        }

        return {**base_vars, **mode_vars.get(result.mode, {})}

    def generate_calibration_prompt(
        self,
        prompt_type: str,
        context: Dict[str, Any]
    ) -> str:
        """Generate a calibration prompt dialogue."""

        template = CALIBRATION_PROMPTS.get(prompt_type)
        if not template:
            return f"Please clarify your preferences for analysis depth."

        return template.render(**context)

    def generate_progressive_disclosure(
        self,
        situation: str,
        analyses: Dict[CognitiveMode, str]
    ) -> str:
        """Generate progressive disclosure of reasoning levels."""

        variables = {
            'situation_summary': situation,
            'level1_response': analyses.get(CognitiveMode.REFLEX, 'N/A'),
            'level2_analysis': analyses.get(CognitiveMode.COMPETENT, 'N/A'),
            'level3_analysis': analyses.get(CognitiveMode.EXPERT, 'N/A'),
            'level4_analysis': analyses.get(CognitiveMode.MASTER, 'N/A'),
            'level5_analysis': analyses.get(CognitiveMode.SAGE, 'N/A'),
            'teaching_summary': self._generate_progressive_teaching_summary(analyses)
        }

        return PROGRESSIVE_DISCLOSURE_TEMPLATE.render(**variables)

    def _generate_progressive_teaching_summary(
        self,
        analyses: Dict[CognitiveMode, str]
    ) -> str:
        """Generate teaching summary for progressive disclosure."""

        return """Notice how each level adds genuine insight, but also notice where diminishing
returns set in. A sage recognizes when the current level is sufficient. Learning to
identify this "sufficiency point" is the key skill in cognitive efficiency."""

    def generate_escalation_notice(
        self,
        direction: str,
        from_mode: CognitiveMode,
        to_mode: CognitiveMode,
        trigger_type: str,
        evidence: List[str],
        teaching_point: str
    ) -> str:
        """Generate escalation/de-escalation notice."""

        template_key = 'escalation' if direction == 'ESCALATE' else 'de_escalation'
        template = ESCALATION_NOTICE_TEMPLATES.get(template_key)

        if not template:
            return f"Mode shifting from {from_mode.name} to {to_mode.name}"

        variables = {
            'from_mode': from_mode.name,
            'to_mode': to_mode.name,
            'trigger_type': trigger_type.replace('_', ' ').title(),
            'evidence': ', '.join(evidence) if evidence else 'Analysis of current context',
            'what_changes': self._describe_mode_change(from_mode, to_mode),
            'new_patterns': self._list_new_patterns(from_mode, to_mode),
            'rationale': 'Current analysis depth exceeds what the situation requires',
            'teaching_point': teaching_point
        }

        return template.render(**variables)

    def _describe_mode_change(
        self,
        from_mode: CognitiveMode,
        to_mode: CognitiveMode
    ) -> str:
        """Describe what changes between modes."""

        if to_mode > from_mode:
            return "I'm now applying deeper stakeholder modeling and more explicit strategic reasoning."
        else:
            return "I'm simplifying analysis to match the actual complexity of the situation."

    def _list_new_patterns(
        self,
        from_mode: CognitiveMode,
        to_mode: CognitiveMode
    ) -> str:
        """List patterns being activated or deactivated."""

        if to_mode <= from_mode:
            return "N/A (de-escalating)"

        patterns = {
            CognitiveMode.COMPETENT: "- Tier 1 Structural Patterns",
            CognitiveMode.EXPERT: "- Tier 2 Behavioral Patterns\n- Implicit MC patterns",
            CognitiveMode.MASTER: "- Explicit MC1-MC8\n- Coalition mapping\n- Information strategy",
            CognitiveMode.SAGE: "- Deep recursive modeling (MC4)\n- Meta-wisdom checks\n- Uncertainty quantification"
        }

        active = []
        for mode in range(from_mode + 1, to_mode + 1):
            if CognitiveMode(mode) in patterns:
                active.append(patterns[CognitiveMode(mode)])

        return '\n'.join(active) if active else "Standard patterns for this mode"

    def generate_budget_summary(
        self,
        session_data: Dict[str, Any]
    ) -> str:
        """Generate cognitive budget summary."""

        # Build budget table
        tasks = session_data.get('tasks', [])
        table_lines = ["Task                              Mode      Budget"]
        table_lines.append("-" * 50)
        for task in tasks[:10]:  # Limit to 10 for display
            task_name = task['name'][:30].ljust(30)
            mode = task['mode'].ljust(10)
            budget = f"{task['budget']}x"
            table_lines.append(f"{task_name} {mode} {budget}")

        total_budget = sum(t['budget'] for t in tasks)
        high_investment = [t for t in tasks if t['budget'] >= 8]
        efficiency = self._calculate_efficiency_score(tasks)

        variables = {
            'session_name': session_data.get('name', 'Analysis Session'),
            'duration': session_data.get('duration', 'Unknown'),
            'task_count': str(len(tasks)),
            'budget_table': '\n'.join(table_lines),
            'total_budget': f"{total_budget}x",
            'high_investment_count': str(len(high_investment)),
            'high_investment_percent': f"{len(high_investment)/len(tasks)*100:.0f}%" if tasks else "0%",
            'efficiency_score': f"{efficiency:.0f}%",
            'efficiency_analysis': self._analyze_efficiency(tasks, efficiency),
            'patterns_observed': self._identify_patterns(tasks),
            'recommendations': self._generate_recommendations(tasks, efficiency)
        }

        return BUDGET_SUMMARY_TEMPLATE.render(**variables)

    def _calculate_efficiency_score(self, tasks: List[Dict]) -> float:
        """Calculate efficiency score (0-100)."""
        if not tasks:
            return 100.0

        # Simple heuristic: are high-budget tasks justified?
        appropriate = 0
        for task in tasks:
            if task['budget'] <= 2 and task.get('stakes', 3) <= 2:
                appropriate += 1
            elif task['budget'] >= 4 and task.get('stakes', 3) >= 4:
                appropriate += 1
            elif 2 < task['budget'] < 4 and 2 < task.get('stakes', 3) < 4:
                appropriate += 1

        return (appropriate / len(tasks)) * 100

    def _analyze_efficiency(self, tasks: List[Dict], score: float) -> str:
        """Generate efficiency analysis text."""
        if score >= 80:
            return "Excellent budget allocation. Analysis depth matched situation requirements."
        elif score >= 60:
            return "Good budget allocation with some room for optimization."
        else:
            return "Budget allocation could be improved. Consider calibrating depth to stakes."

    def _identify_patterns(self, tasks: List[Dict]) -> str:
        """Identify patterns in task handling."""
        if not tasks:
            return "Insufficient data for pattern analysis."

        high_budget = [t for t in tasks if t['budget'] >= 8]
        low_budget = [t for t in tasks if t['budget'] <= 2]

        patterns = []
        if len(high_budget) > len(tasks) * 0.3:
            patterns.append("- Tendency toward deep analysis even for moderate situations")
        if len(low_budget) > len(tasks) * 0.7:
            patterns.append("- Efficient handling of routine matters")

        return '\n'.join(patterns) if patterns else "- Balanced approach across task types"

    def _generate_recommendations(self, tasks: List[Dict], score: float) -> str:
        """Generate recommendations for improvement."""
        if score >= 80:
            return "- Continue current approach\n- Consider documenting decision patterns for future reference"
        elif score >= 60:
            return "- Review high-budget decisions for necessity\n- Develop pattern recognition for routine situations"
        else:
            return "- Calibrate analysis depth to actual stakes\n- Use quick classification for routine matters\n- Reserve deep analysis for genuinely complex situations"


# =============================================================================
# SPECIALIZED DIALOGUE GENERATORS
# =============================================================================

class SocraticDialogueGenerator:
    """Generate Socratic-style teaching dialogues that guide through questions."""

    def generate_discovery_dialogue(
        self,
        situation: str,
        target_insight: str,
        current_mode: CognitiveMode
    ) -> str:
        """Generate a dialogue that leads user to discover appropriate mode."""

        return f"""
**Let's Think Through This Together**

Situation: {situation}

**Question 1:** What's at stake here if we get this wrong?
- What are the consequences of an error?
- Is this easily correctable, or would damage be lasting?

**Question 2:** How many parties are affected?
- Who has a stake in this outcome?
- Do their interests align or conflict?

**Question 3:** How much time do we have?
- Is there urgency, or can we take time for thorough analysis?
- What's the cost of delay vs. the cost of rushing?

**Question 4:** How sophisticated are the other actors?
- Are they likely to be thinking about what we're thinking?
- Do we need to model their mental models?

Based on your answers, what level of analysis does this situation warrant?
- Routine pattern matching (REFLEX)
- Standard professional review (COMPETENT)
- Full stakeholder-aware analysis (EXPERT)
- Explicit strategic reasoning (MASTER)
- Deep recursive wisdom (SAGE)

*My assessment: This appears to warrant **{current_mode.name}** mode. Do you agree?*
"""


class ConflictResolutionDialogue:
    """Handle dialogues when user preference conflicts with recommended mode."""

    def generate_conflict_dialogue(
        self,
        user_preference: CognitiveMode,
        recommended_mode: CognitiveMode,
        reasoning: str
    ) -> str:
        """Generate dialogue for mode preference conflict."""

        if user_preference < recommended_mode:
            return f"""
**Depth Preference Conflict**

You've requested **{user_preference.name}** mode, but my assessment suggests **{recommended_mode.name}**.

**Why I recommend deeper analysis:**
{reasoning}

**Risks of lower depth:**
- May miss stakeholder dynamics that affect outcome
- Could overlook strategic implications
- Predictions may be less accurate

**Options:**
A) Proceed with {user_preference.name} (faster, but with noted risks)
B) Use {recommended_mode.name} (my recommendation)
C) Let me show you both levels so you can compare

Which would you prefer?
"""
        else:
            return f"""
**Efficiency Opportunity**

You've requested **{user_preference.name}** mode, but this situation may not require that depth.

**Why {recommended_mode.name} may suffice:**
{reasoning}

**Considerations:**
- Additional depth may not improve decision quality
- Time could be better invested elsewhere
- Over-analysis can sometimes cloud judgment

**Options:**
A) Proceed with {recommended_mode.name} (my recommendation)
B) Use {user_preference.name} anyway
C) Start with {recommended_mode.name}, escalate if needed

Which would you prefer?
"""


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example_usage():
    """Demonstrate teaching dialogue generation."""

    print("=" * 70)
    print("TEACHING DIALOGUE TEMPLATES - Examples")
    print("=" * 70)

    generator = TeachingDialogueGenerator()

    # Example 1: Explain choice for EXPERT mode
    print("\nEXAMPLE 1: Explain Choice Dialogue")
    print("-" * 50)

    from situation_classifier import SituationClassifier
    classifier = SituationClassifier()

    result = classifier.classify_from_scores(
        stakes=3,
        complexity=3,
        reversibility=3,
        time_pressure=2,
        stakeholders=["Client", "Vendor", "Internal team"]
    )

    dialogue = generator.generate_explain_choice(result)
    print(dialogue)

    # Example 2: Calibration prompt
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Calibration Prompt")
    print("-" * 50)

    calibration = generator.generate_calibration_prompt(
        'mode_mismatch',
        {
            'user_request': 'Just give me a quick answer on this acquisition',
            'suggested_mode': 'MASTER',
            'assessment_summary': 'Multi-party deal with sophisticated counterparty',
            'calibration_question': 'Given the complexity, would you prefer deeper analysis?',
            'option_a': 'Quick heuristic (may miss important considerations)',
            'option_b': 'Full strategic analysis (comprehensive but time-intensive)',
            'option_c': 'Tell me about your time constraints'
        }
    )
    print(calibration)

    # Example 3: Progressive disclosure
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Progressive Disclosure")
    print("-" * 50)

    progressive = generator.generate_progressive_disclosure(
        situation="Partnership negotiation with tech startup",
        analyses={
            CognitiveMode.REFLEX: '"Use standard partnership template."',
            CognitiveMode.COMPETENT: 'Review their financials, check IP ownership, standard terms.',
            CognitiveMode.EXPERT: '''Partner is smaller company with different risk tolerance.
They need IP protection; we need indemnification.
Frame our needs in terms of their concerns.''',
            CognitiveMode.MASTER: '''Their CEO is ex-BigCo, sophisticated negotiator.
They\'re probably modeling our walkaway point.
Coalition consideration: their board may override CEO.
Design information revelation strategy.''',
            CognitiveMode.SAGE: '''Full analysis has diminishing returns.
Key uncertainty: relationship quality post-signing.
Perhaps invest energy in governance mechanisms
rather than trying to anticipate all scenarios.'''
        }
    )
    print(progressive)

    # Example 4: Escalation notice
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Escalation Notice")
    print("-" * 50)

    escalation = generator.generate_escalation_notice(
        direction='ESCALATE',
        from_mode=CognitiveMode.EXPERT,
        to_mode=CognitiveMode.MASTER,
        trigger_type='OPPONENT_SOPHISTICATION',
        evidence=['Counterparty asked about our BATNA', 'Sophisticated counter-proposal received'],
        teaching_point='When counterparties demonstrate recursive thinking, match their depth.'
    )
    print(escalation)

    # Example 5: Socratic dialogue
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Socratic Discovery Dialogue")
    print("-" * 50)

    socratic = SocraticDialogueGenerator()
    discovery = socratic.generate_discovery_dialogue(
        situation="Reviewing standard vendor agreement",
        target_insight="This is a routine matter warranting COMPETENT mode",
        current_mode=CognitiveMode.COMPETENT
    )
    print(discovery)


if __name__ == "__main__":
    example_usage()
