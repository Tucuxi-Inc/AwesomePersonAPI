"""
Sage-Mode Situation Classifier
==============================

Implementation pseudocode for classifying situations and allocating cognitive budgets.
This module determines the appropriate cognitive mode (REFLEX through SAGE) based on
four dimensions: Stakes, Complexity, Reversibility, and Time Pressure.

Part of the FLO Cognitive Apprentice System.
"""

from dataclasses import dataclass, field
from enum import IntEnum, Enum
from typing import Optional, List, Dict, Any, Tuple
import re


# =============================================================================
# ENUMERATIONS AND CONSTANTS
# =============================================================================

class CognitiveMode(IntEnum):
    """The five cognitive modes with increasing depth and cost."""
    REFLEX = 1      # Pattern matching, heuristics only (~1x cost)
    COMPETENT = 2   # Tier 1 patterns, basic stakeholder ID (~2x cost)
    EXPERT = 3      # Tier 1+2, implicit MC patterns (~4x cost)
    MASTER = 4      # Full Tier 1-3, explicit MC reasoning (~8x cost)
    SAGE = 5        # Deep recursive analysis + meta-wisdom (~16x cost)


class StakesLevel(IntEnum):
    """What's at risk if we get this wrong?"""
    TRIVIAL = 1     # Easily corrected, low impact
    MINOR = 2       # Some cost to correct, limited impact
    MODERATE = 3    # Significant cost, meaningful impact
    MAJOR = 4       # High cost, substantial impact
    CRITICAL = 5    # Irreversible, transformative impact


class ComplexityLevel(IntEnum):
    """How many interacting factors are involved?"""
    SIMPLE = 1          # Single factor, clear answer
    COMPLICATED = 2     # Multiple factors, but decomposable
    COMPLEX = 3         # Interacting factors, some uncertainty
    HIGHLY_COMPLEX = 4  # Many stakeholders, feedback loops
    WICKED = 5          # Contested framing, no clear solution space


class ReversibilityLevel(IntEnum):
    """Can we course-correct after this decision?"""
    FULLY_REVERSIBLE = 1      # Can undo completely
    MOSTLY_REVERSIBLE = 2     # Some friction to undo
    PARTIALLY_REVERSIBLE = 3  # Significant cost to undo
    DIFFICULT_TO_REVERSE = 4  # Major cost, reputation effects
    IRREVERSIBLE = 5          # Cannot be undone


class TimePressure(IntEnum):
    """How much time is available for deliberation?"""
    ABUNDANT = 1      # Days/weeks available
    COMFORTABLE = 2   # Hours to a day
    CONSTRAINED = 3   # Hours
    PRESSURED = 4     # Minutes to an hour
    CRISIS = 5        # Immediate decision required


# Weight factors for budget calculation
WEIGHTS = {
    'stakes': 0.35,
    'complexity': 0.30,
    'reversibility': 0.25,
    'time_pressure': 0.10
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class SituationAssessment:
    """Complete assessment of a situation's cognitive requirements."""
    stakes: StakesLevel
    complexity: ComplexityLevel
    reversibility: ReversibilityLevel
    time_pressure: TimePressure

    # Optional context for teaching/explanation
    stakes_rationale: str = ""
    complexity_rationale: str = ""
    reversibility_rationale: str = ""
    time_rationale: str = ""

    # Detected indicators
    stakeholders: List[str] = field(default_factory=list)
    sophisticated_actors: List[str] = field(default_factory=list)
    anomalies: List[str] = field(default_factory=list)

    def raw_score(self) -> float:
        """Calculate raw weighted score."""
        return (
            self.stakes * WEIGHTS['stakes'] +
            self.complexity * WEIGHTS['complexity'] +
            self.reversibility * WEIGHTS['reversibility'] +
            self.time_pressure * WEIGHTS['time_pressure']
        )


@dataclass
class ClassificationResult:
    """Result of situation classification with full context."""
    mode: CognitiveMode
    budget_score: float
    assessment: SituationAssessment
    adjustments_applied: List[str]
    reasoning: str
    active_patterns: List[str]
    teaching_note: str = ""


# =============================================================================
# SITUATION INDICATOR DETECTION
# =============================================================================

class SituationIndicatorDetector:
    """
    Detects key indicators in situation descriptions to assist classification.
    Uses pattern matching on natural language descriptions.
    """

    # Stakes indicators
    HIGH_STAKES_PATTERNS = [
        r'\b(bet-the-company|career-defining|existential|catastrophic)\b',
        r'\b(multi-million|significant financial|major liability)\b',
        r'\b(irreversible harm|permanent damage|cannot be undone)\b',
        r'\b(regulatory action|litigation|lawsuit|legal action)\b',
        r'\b(acquisition|merger|ipo|funding round)\b',
        r'\b(termination|firing|restructuring|layoff)\b',
    ]

    LOW_STAKES_PATTERNS = [
        r'\b(routine|standard|typical|normal|usual)\b',
        r'\b(minor|small|trivial|inconsequential)\b',
        r'\b(easily corrected|can be changed|reversible)\b',
        r'\b(internal only|no external impact)\b',
    ]

    # Complexity indicators
    HIGH_COMPLEXITY_PATTERNS = [
        r'\b(multiple stakeholders|many parties|various interests)\b',
        r'\b(cross-functional|cross-border|multi-jurisdictional)\b',
        r'\b(interdependent|feedback loop|cascading effects)\b',
        r'\b(no clear answer|contested|ambiguous|uncertain)\b',
        r'\b(novel|unprecedented|first-of-its-kind)\b',
    ]

    LOW_COMPLEXITY_PATTERNS = [
        r'\b(straightforward|simple|clear-cut|obvious)\b',
        r'\b(template|standard form|boilerplate)\b',
        r'\b(single issue|one factor|isolated)\b',
    ]

    # Sophisticated actor indicators
    SOPHISTICATED_ACTOR_PATTERNS = [
        r'\b(sophisticated|experienced|seasoned|veteran)\b',
        r'\b(strategic|calculating|savvy)\b',
        r'\b(lawyer|attorney|counsel|investment banker)\b',
        r'\b(negotiator|dealmaker)\b',
        r'\b(fortune 500|major corporation|big tech)\b',
        r'\b(private equity|venture capital|hedge fund)\b',
    ]

    # Time pressure indicators
    CRISIS_TIME_PATTERNS = [
        r'\b(immediately|urgent|asap|right now|crisis)\b',
        r'\b(deadline today|due now|must decide)\b',
        r'\b(emergency|time-sensitive|critical)\b',
    ]

    RELAXED_TIME_PATTERNS = [
        r'\b(no rush|take your time|when convenient)\b',
        r'\b(next week|next month|eventually)\b',
        r'\b(planning phase|early stages|preliminary)\b',
    ]

    @classmethod
    def detect_stakes_level(cls, description: str) -> Tuple[StakesLevel, str]:
        """Analyze description for stakes indicators."""
        text = description.lower()
        high_matches = sum(1 for p in cls.HIGH_STAKES_PATTERNS if re.search(p, text, re.I))
        low_matches = sum(1 for p in cls.LOW_STAKES_PATTERNS if re.search(p, text, re.I))

        if high_matches >= 2:
            return StakesLevel.CRITICAL, f"Multiple high-stakes indicators detected ({high_matches})"
        elif high_matches == 1:
            return StakesLevel.MAJOR, "High-stakes indicator present"
        elif low_matches >= 2:
            return StakesLevel.TRIVIAL, f"Multiple low-stakes indicators ({low_matches})"
        elif low_matches == 1:
            return StakesLevel.MINOR, "Low-stakes indicator present"
        else:
            return StakesLevel.MODERATE, "Default: moderate stakes assumed"

    @classmethod
    def detect_complexity_level(cls, description: str) -> Tuple[ComplexityLevel, str]:
        """Analyze description for complexity indicators."""
        text = description.lower()
        high_matches = sum(1 for p in cls.HIGH_COMPLEXITY_PATTERNS if re.search(p, text, re.I))
        low_matches = sum(1 for p in cls.LOW_COMPLEXITY_PATTERNS if re.search(p, text, re.I))

        if high_matches >= 2:
            return ComplexityLevel.WICKED, f"Multiple high-complexity indicators ({high_matches})"
        elif high_matches == 1:
            return ComplexityLevel.HIGHLY_COMPLEX, "High-complexity indicator present"
        elif low_matches >= 2:
            return ComplexityLevel.SIMPLE, f"Multiple simplicity indicators ({low_matches})"
        elif low_matches == 1:
            return ComplexityLevel.COMPLICATED, "Simplicity indicator present"
        else:
            return ComplexityLevel.COMPLEX, "Default: moderate complexity assumed"

    @classmethod
    def detect_sophisticated_actors(cls, description: str) -> List[str]:
        """Identify references to sophisticated actors."""
        text = description.lower()
        actors = []
        for pattern in cls.SOPHISTICATED_ACTOR_PATTERNS:
            matches = re.findall(pattern, text, re.I)
            actors.extend(matches)
        return list(set(actors))

    @classmethod
    def detect_time_pressure(cls, description: str) -> Tuple[TimePressure, str]:
        """Analyze description for time pressure indicators."""
        text = description.lower()
        crisis_matches = sum(1 for p in cls.CRISIS_TIME_PATTERNS if re.search(p, text, re.I))
        relaxed_matches = sum(1 for p in cls.RELAXED_TIME_PATTERNS if re.search(p, text, re.I))

        if crisis_matches >= 1:
            return TimePressure.CRISIS, "Crisis time pressure detected"
        elif relaxed_matches >= 2:
            return TimePressure.ABUNDANT, "Relaxed timeline indicated"
        elif relaxed_matches == 1:
            return TimePressure.COMFORTABLE, "Some timeline flexibility indicated"
        else:
            return TimePressure.CONSTRAINED, "Default: constrained time assumed"

    @classmethod
    def full_analysis(cls, description: str) -> Dict[str, Any]:
        """Run full indicator analysis on description."""
        stakes, stakes_rationale = cls.detect_stakes_level(description)
        complexity, complexity_rationale = cls.detect_complexity_level(description)
        time_pressure, time_rationale = cls.detect_time_pressure(description)
        sophisticated_actors = cls.detect_sophisticated_actors(description)

        return {
            'stakes': stakes,
            'stakes_rationale': stakes_rationale,
            'complexity': complexity,
            'complexity_rationale': complexity_rationale,
            'time_pressure': time_pressure,
            'time_rationale': time_rationale,
            'sophisticated_actors': sophisticated_actors,
        }


# =============================================================================
# MAIN CLASSIFIER
# =============================================================================

class SituationClassifier:
    """
    Main situation classifier that determines appropriate cognitive mode.

    Usage:
        classifier = SituationClassifier()

        # From raw scores
        result = classifier.classify_from_scores(
            stakes=4, complexity=3, reversibility=4, time_pressure=2
        )

        # From natural language description
        result = classifier.classify_from_description(
            "We need to negotiate a partnership agreement with a sophisticated
            private equity firm. This is a multi-million dollar deal that will
            define our growth strategy for the next 5 years."
        )
    """

    def __init__(self):
        self.detector = SituationIndicatorDetector()

    def classify_from_scores(
        self,
        stakes: int,
        complexity: int,
        reversibility: int,
        time_pressure: int,
        stakeholders: Optional[List[str]] = None,
        sophisticated_actors: Optional[List[str]] = None
    ) -> ClassificationResult:
        """
        Classify situation from explicit dimension scores (1-5 each).
        """
        assessment = SituationAssessment(
            stakes=StakesLevel(stakes),
            complexity=ComplexityLevel(complexity),
            reversibility=ReversibilityLevel(reversibility),
            time_pressure=TimePressure(time_pressure),
            stakeholders=stakeholders or [],
            sophisticated_actors=sophisticated_actors or []
        )
        return self._classify(assessment)

    def classify_from_description(self, description: str) -> ClassificationResult:
        """
        Classify situation from natural language description.
        Uses indicator detection to estimate dimension scores.
        """
        # Run indicator analysis
        analysis = self.detector.full_analysis(description)

        # Estimate reversibility based on stakes and description
        # (reversibility is harder to detect from text alone)
        if analysis['stakes'] >= StakesLevel.MAJOR:
            reversibility = ReversibilityLevel.DIFFICULT_TO_REVERSE
            rev_rationale = "High stakes typically correlate with low reversibility"
        elif analysis['stakes'] <= StakesLevel.MINOR:
            reversibility = ReversibilityLevel.MOSTLY_REVERSIBLE
            rev_rationale = "Low stakes typically correlate with high reversibility"
        else:
            reversibility = ReversibilityLevel.PARTIALLY_REVERSIBLE
            rev_rationale = "Default: moderate reversibility assumed"

        assessment = SituationAssessment(
            stakes=analysis['stakes'],
            complexity=analysis['complexity'],
            reversibility=reversibility,
            time_pressure=analysis['time_pressure'],
            stakes_rationale=analysis['stakes_rationale'],
            complexity_rationale=analysis['complexity_rationale'],
            reversibility_rationale=rev_rationale,
            time_rationale=analysis['time_rationale'],
            sophisticated_actors=analysis['sophisticated_actors']
        )

        return self._classify(assessment)

    def _classify(self, assessment: SituationAssessment) -> ClassificationResult:
        """Core classification logic with adjustments."""

        raw_score = assessment.raw_score()
        adjustments = []
        adjusted_score = raw_score

        # Adjustment 1: Time pressure cap
        # If crisis AND raw score > 3, cap at Budget 3 (can't do deep analysis)
        if assessment.time_pressure == TimePressure.CRISIS and raw_score > 3.0:
            adjusted_score = min(adjusted_score, 3.0)
            adjustments.append(
                "CAPPED: Crisis time pressure limits depth to EXPERT mode"
            )

        # Adjustment 2: Stakes minimum floor
        # If stakes = 5 (critical) AND time ≤ 3, minimum Budget 4
        if (assessment.stakes == StakesLevel.CRITICAL and
            assessment.time_pressure <= TimePressure.CONSTRAINED):
            adjusted_score = max(adjusted_score, 4.0)
            adjustments.append(
                "FLOOR: Critical stakes with available time demands MASTER+ mode"
            )

        # Adjustment 3: Simplicity cap
        # If complexity = 1 AND stakes ≤ 2, cap at Budget 2
        if (assessment.complexity == ComplexityLevel.SIMPLE and
            assessment.stakes <= StakesLevel.MINOR):
            adjusted_score = min(adjusted_score, 2.0)
            adjustments.append(
                "CAPPED: Simple low-stakes problems don't need depth"
            )

        # Adjustment 4: Sophisticated actor boost
        # If sophisticated actors present, minimum EXPERT mode
        if assessment.sophisticated_actors:
            adjusted_score = max(adjusted_score, 3.0)
            actors = ", ".join(assessment.sophisticated_actors[:3])
            adjustments.append(
                f"FLOOR: Sophisticated actors ({actors}) require at least EXPERT mode"
            )

        # Adjustment 5: Irreversibility + Critical stakes = SAGE
        if (assessment.reversibility == ReversibilityLevel.IRREVERSIBLE and
            assessment.stakes == StakesLevel.CRITICAL):
            adjusted_score = max(adjusted_score, 5.0)
            adjustments.append(
                "FLOOR: Irreversible + Critical demands SAGE mode"
            )

        # Round to nearest mode
        final_mode = CognitiveMode(max(1, min(5, round(adjusted_score))))

        # Generate reasoning explanation
        reasoning = self._generate_reasoning(assessment, raw_score, adjusted_score, adjustments)

        # Determine active patterns for this mode
        active_patterns = self._get_active_patterns(final_mode)

        # Generate teaching note
        teaching_note = self._generate_teaching_note(assessment, final_mode)

        return ClassificationResult(
            mode=final_mode,
            budget_score=adjusted_score,
            assessment=assessment,
            adjustments_applied=adjustments,
            reasoning=reasoning,
            active_patterns=active_patterns,
            teaching_note=teaching_note
        )

    def _generate_reasoning(
        self,
        assessment: SituationAssessment,
        raw_score: float,
        adjusted_score: float,
        adjustments: List[str]
    ) -> str:
        """Generate human-readable reasoning for the classification."""
        lines = [
            "CLASSIFICATION REASONING:",
            "",
            "Dimension Scores:",
            f"  Stakes:       {assessment.stakes.value}/5 - {assessment.stakes.name}",
            f"  Complexity:   {assessment.complexity.value}/5 - {assessment.complexity.name}",
            f"  Reversibility: {assessment.reversibility.value}/5 - {assessment.reversibility.name}",
            f"  Time Pressure: {assessment.time_pressure.value}/5 - {assessment.time_pressure.name}",
            "",
            f"Raw Weighted Score: {raw_score:.2f}",
        ]

        if adjustments:
            lines.append("")
            lines.append("Adjustments Applied:")
            for adj in adjustments:
                lines.append(f"  • {adj}")

        lines.append("")
        lines.append(f"Final Score: {adjusted_score:.2f} → {CognitiveMode(round(adjusted_score)).name} mode")

        return "\n".join(lines)

    def _get_active_patterns(self, mode: CognitiveMode) -> List[str]:
        """Return list of patterns active for this cognitive mode."""
        patterns = {
            CognitiveMode.REFLEX: [
                "Template matching",
                "Basic heuristics",
            ],
            CognitiveMode.COMPETENT: [
                "Tier 1: Structural patterns (S1-S5)",
                "Basic stakeholder identification",
                "Standard risk assessment",
            ],
            CognitiveMode.EXPERT: [
                "Tier 1: Full structural patterns",
                "Tier 2: Behavioral patterns (BI1-BI5)",
                "MC patterns (implicit application)",
                "Standard trajectory forecasting",
            ],
            CognitiveMode.MASTER: [
                "Tier 1: Full structural patterns",
                "Tier 2: Full behavioral patterns",
                "Tier 3: Explicit MC1-MC8 patterns",
                "MC1: Stakeholder Mental Model Construction",
                "MC2: Behavioral Trajectory Forecasting",
                "MC3: Strategic Communication Framing",
                "MC6: Coalition Possibility Mapping",
                "MC7: Reputation and Credibility Maintenance",
                "MC8: Information Revelation Strategy",
            ],
            CognitiveMode.SAGE: [
                "All MASTER mode patterns, plus:",
                "MC4: Deep Recursive Intention Modeling (level 3+)",
                "MC5: Emotional Contagion Management",
                "Meta-pattern awareness",
                "Explicit uncertainty quantification",
                "Multi-scenario exploration",
                "Wisdom heuristics (analysis termination)",
                "Intuition integration checks",
            ],
        }
        return patterns.get(mode, [])

    def _generate_teaching_note(
        self,
        assessment: SituationAssessment,
        mode: CognitiveMode
    ) -> str:
        """Generate a teaching note explaining the classification choice."""

        mode_names = {
            CognitiveMode.REFLEX: "quick pattern matching",
            CognitiveMode.COMPETENT: "standard professional analysis",
            CognitiveMode.EXPERT: "full professional judgment with stakeholder awareness",
            CognitiveMode.MASTER: "explicit strategic reasoning with full stakeholder modeling",
            CognitiveMode.SAGE: "deep recursive analysis with meta-cognitive wisdom",
        }

        teaching = f"TEACHING NOTE: This situation warrants {mode_names[mode]}.\n\n"

        # Explain why not more
        if mode < CognitiveMode.SAGE:
            if assessment.complexity <= ComplexityLevel.COMPLICATED:
                teaching += "• Deeper analysis unnecessary: The problem is decomposable.\n"
            if assessment.stakes <= StakesLevel.MODERATE:
                teaching += "• Stakes don't justify more investment: Errors are correctable.\n"
            if assessment.time_pressure >= TimePressure.PRESSURED:
                teaching += "• Time constraints prevent deeper analysis.\n"

        # Explain why not less
        if mode > CognitiveMode.REFLEX:
            if assessment.stakeholders or assessment.sophisticated_actors:
                teaching += "• Multiple/sophisticated actors require modeling.\n"
            if assessment.stakes >= StakesLevel.MAJOR:
                teaching += "• High stakes justify careful analysis.\n"
            if assessment.reversibility >= ReversibilityLevel.DIFFICULT_TO_REVERSE:
                teaching += "• Low reversibility demands getting it right the first time.\n"

        # Key insight
        if mode == CognitiveMode.SAGE:
            teaching += "\nSAGE INSIGHT: At this level, also question whether analysis itself is the right approach. Some factors here may be beyond systematic analysis."

        return teaching


# =============================================================================
# QUICK CLASSIFICATION HEURISTICS
# =============================================================================

class QuickClassifier:
    """
    Fast-path classifier for common situation types.
    Bypasses full analysis when situation type is recognized.
    """

    SITUATION_TEMPLATES = {
        # Routine situations → REFLEX or COMPETENT
        "standard_nda_review": CognitiveMode.COMPETENT,
        "routine_contract_amendment": CognitiveMode.COMPETENT,
        "standard_vendor_agreement": CognitiveMode.COMPETENT,
        "internal_policy_question": CognitiveMode.REFLEX,
        "template_request": CognitiveMode.REFLEX,
        "factual_lookup": CognitiveMode.REFLEX,

        # Standard professional work → EXPERT
        "standard_negotiation": CognitiveMode.EXPERT,
        "employee_matter": CognitiveMode.EXPERT,
        "regulatory_filing": CognitiveMode.EXPERT,
        "customer_contract": CognitiveMode.EXPERT,

        # High-stakes situations → MASTER
        "multi_party_deal": CognitiveMode.MASTER,
        "executive_termination": CognitiveMode.MASTER,
        "strategic_partnership": CognitiveMode.MASTER,
        "litigation_strategy": CognitiveMode.MASTER,
        "regulatory_investigation": CognitiveMode.MASTER,

        # Critical situations → SAGE
        "acquisition_negotiation": CognitiveMode.SAGE,
        "bet_the_company": CognitiveMode.SAGE,
        "ceo_succession": CognitiveMode.SAGE,
        "ipo_preparation": CognitiveMode.SAGE,
        "existential_crisis": CognitiveMode.SAGE,
    }

    KEYWORDS_TO_TEMPLATES = {
        # REFLEX triggers
        "what's the standard": "template_request",
        "boilerplate": "template_request",
        "typical term": "factual_lookup",

        # COMPETENT triggers
        "nda": "standard_nda_review",
        "non-disclosure": "standard_nda_review",
        "amendment": "routine_contract_amendment",

        # EXPERT triggers
        "negotiate": "standard_negotiation",
        "employee": "employee_matter",
        "customer agreement": "customer_contract",

        # MASTER triggers
        "multiple parties": "multi_party_deal",
        "terminate executive": "executive_termination",
        "strategic partner": "strategic_partnership",
        "investigation": "regulatory_investigation",

        # SAGE triggers
        "acquisition": "acquisition_negotiation",
        "bet-the-company": "bet_the_company",
        "ceo succession": "ceo_succession",
        "ipo": "ipo_preparation",
    }

    @classmethod
    def quick_classify(cls, description: str) -> Optional[CognitiveMode]:
        """
        Attempt quick classification from known patterns.
        Returns None if no quick match found.
        """
        text = description.lower()

        for keyword, template in cls.KEYWORDS_TO_TEMPLATES.items():
            if keyword in text:
                return cls.SITUATION_TEMPLATES.get(template)

        return None

    @classmethod
    def classify_with_fallback(
        cls,
        description: str,
        classifier: SituationClassifier
    ) -> ClassificationResult:
        """
        Try quick classification first, fall back to full analysis.
        """
        quick_mode = cls.quick_classify(description)

        if quick_mode is not None:
            # Create minimal result for quick classification
            return ClassificationResult(
                mode=quick_mode,
                budget_score=float(quick_mode),
                assessment=SituationAssessment(
                    stakes=StakesLevel.MODERATE,
                    complexity=ComplexityLevel.COMPLEX,
                    reversibility=ReversibilityLevel.PARTIALLY_REVERSIBLE,
                    time_pressure=TimePressure.CONSTRAINED
                ),
                adjustments_applied=["QUICK_CLASSIFICATION: Matched known pattern"],
                reasoning=f"Quick match: Recognized as {quick_mode.name}-level situation",
                active_patterns=classifier._get_active_patterns(quick_mode),
                teaching_note="Recognized pattern - full analysis skipped"
            )

        # Fall back to full classification
        return classifier.classify_from_description(description)


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_usage():
    """Demonstrate classifier usage."""

    classifier = SituationClassifier()

    # Example 1: From explicit scores
    print("=" * 60)
    print("EXAMPLE 1: Explicit Score Classification")
    print("=" * 60)

    result = classifier.classify_from_scores(
        stakes=4,           # Major
        complexity=4,       # Highly complex
        reversibility=4,    # Difficult to reverse
        time_pressure=2,    # Comfortable
        sophisticated_actors=["private equity firm", "experienced lawyer"]
    )

    print(f"Mode: {result.mode.name}")
    print(f"Score: {result.budget_score:.2f}")
    print(result.reasoning)
    print()
    print("Active Patterns:")
    for pattern in result.active_patterns:
        print(f"  • {pattern}")
    print()
    print(result.teaching_note)

    # Example 2: From natural language
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Natural Language Classification")
    print("=" * 60)

    description = """
    We need to negotiate a partnership agreement with a sophisticated
    private equity firm. This is a multi-million dollar deal that will
    define our growth strategy for the next 5 years. Their legal team
    is known for aggressive tactics.
    """

    result = classifier.classify_from_description(description)

    print(f"Mode: {result.mode.name}")
    print(f"Score: {result.budget_score:.2f}")
    print(result.reasoning)
    print()
    print(result.teaching_note)

    # Example 3: Quick classification
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Quick Classification")
    print("=" * 60)

    quick_result = QuickClassifier.classify_with_fallback(
        "What's the standard NDA term for confidentiality period?",
        classifier
    )

    print(f"Mode: {quick_result.mode.name}")
    print(f"Reasoning: {quick_result.reasoning}")


if __name__ == "__main__":
    example_usage()
