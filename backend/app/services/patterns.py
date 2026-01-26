"""Universal Reasoning Patterns (URP) for intelligent probe generation.

These patterns are applied to dynamically generate interview questions based on:
- Candidate context (resume, prior responses, role)
- Conversation state (what's been asked, signals detected)
- Pattern-based reasoning (metacognitive and interpersonal patterns)
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ReasoningPattern(str, Enum):
    """Universal Reasoning Patterns applicable to candidate assessment."""

    # Metacognitive patterns
    MC1_STAKEHOLDER = "MC1"  # Stakeholder Identification & Perspective-Taking
    MC24_ASSUMPTION = "MC24"  # Assumption Surfacing
    MC29_PROGRESS = "MC29"  # Progress Monitoring & Recalibration
    MC35_REPRESENTATION = "MC35"  # Representation Choice
    MC38_ABSTRACTION = "MC38"  # Abstraction Level Selection
    MC44_SOLUTION_SPACE = "MC44"  # Solution Space Exploration

    # Interpersonal patterns
    IP3_ACTIVE_LISTENING = "IP3"  # Active Listening with Validation
    IP7_CONFLICT = "IP7"  # Conflict/Tension Exploration
    IP11_TRUST = "IP11"  # Trust Calibration

    # Strategic patterns
    SP8_RISK = "SP8"  # Risk Identification
    SP12_PROJECTION = "SP12"  # Scenario Projection


# Pattern descriptions for LLM prompts
PATTERN_DESCRIPTIONS: Dict[ReasoningPattern, Dict[str, str]] = {
    ReasoningPattern.MC1_STAKEHOLDER: {
        "name": "Stakeholder Identification & Perspective-Taking",
        "purpose": "Map candidate as multi-dimensional; understand their goals, constraints, fears",
        "application": "Build comprehensive candidate context for personalized probing",
    },
    ReasoningPattern.MC24_ASSUMPTION: {
        "name": "Assumption Surfacing",
        "purpose": "Identify hidden assumptions in responses; probe beneath surface answers",
        "application": "Challenge what candidates say to understand what they actually do",
    },
    ReasoningPattern.MC29_PROGRESS: {
        "name": "Progress Monitoring & Recalibration",
        "purpose": "Track interview effectiveness; adjust strategy based on signal quality",
        "application": "Dynamically adjust interview strategy mid-session",
    },
    ReasoningPattern.MC35_REPRESENTATION: {
        "name": "Representation Choice",
        "purpose": "Select appropriate probe type based on role context and trait",
        "application": "Match probe style to what success looks like in specific role",
    },
    ReasoningPattern.MC38_ABSTRACTION: {
        "name": "Abstraction Level Selection",
        "purpose": "Calibrate probe depth (surface vs. deep) based on response quality",
        "application": "Go deeper when responses lack specific names, dates, numbers",
    },
    ReasoningPattern.MC44_SOLUTION_SPACE: {
        "name": "Solution Space Exploration",
        "purpose": "Consider alternative interpretations; avoid anchoring on first impression",
        "application": "Generate probes that test alternative hypotheses about candidate",
    },
    ReasoningPattern.IP3_ACTIVE_LISTENING: {
        "name": "Active Listening with Validation",
        "purpose": "Identify what's NOT said; probe omissions",
        "application": "Notice and explore gaps in candidate responses",
    },
    ReasoningPattern.IP7_CONFLICT: {
        "name": "Conflict/Tension Exploration",
        "purpose": "Probe disagreement, failure, friction—where adaptability reveals itself",
        "application": "Seek failure and conflict stories for authentic trait signals",
    },
    ReasoningPattern.IP11_TRUST: {
        "name": "Trust Calibration",
        "purpose": "Weight self-report vs. behavioral evidence appropriately",
        "application": "Convert self-report claims into behavioral evidence requests",
    },
    ReasoningPattern.SP8_RISK: {
        "name": "Risk Identification",
        "purpose": "Identify potential failure modes; map warning signals",
        "application": "Probe for when strengths become weaknesses",
    },
    ReasoningPattern.SP12_PROJECTION: {
        "name": "Scenario Projection",
        "purpose": "Project candidate performance at future time points",
        "application": "Use role-specific hypotheticals to assess likely behavior",
    },
}


class EvidenceType(str, Enum):
    """Types of evidence from candidate responses."""

    OBSERVED = "OBSERVED"  # Demonstrated in this interview
    BEHAVIORAL = "BEHAVIORAL"  # Specific past action with details
    HYPOTHETICAL = "HYPOTHETICAL"  # What they would do
    SELF_REPORT = "SELF_REPORT"  # Claims about themselves
    OPINION = "OPINION"  # General belief or value statement


# Evidence weight hierarchy (highest to lowest value)
EVIDENCE_WEIGHTS: Dict[EvidenceType, float] = {
    EvidenceType.OBSERVED: 1.2,
    EvidenceType.BEHAVIORAL: 1.0,
    EvidenceType.HYPOTHETICAL: 0.5,
    EvidenceType.SELF_REPORT: 0.3,
    EvidenceType.OPINION: 0.2,
}


class ResponseDepth(str, Enum):
    """Depth levels for candidate responses."""

    SURFACE = "SURFACE"  # General statements, no specifics
    MODERATE = "MODERATE"  # Some specifics, missing key details
    DEEP = "DEEP"  # Rich in specifics—names, dates, numbers, outcomes


class ProbeContext(BaseModel):
    """Context for generating probes."""

    # Candidate info
    candidate_id: Optional[str] = None
    resume_summary: Optional[str] = None
    resume_data: Optional[Dict[str, Any]] = None
    candidate_background: Optional[str] = None

    # Role info
    role_profile_id: Optional[str] = None
    role_name: Optional[str] = None
    role_category: Optional[str] = None
    critical_traits: List[str] = []

    # Session state
    session_id: Optional[str] = None
    probes_asked: List[Dict[str, Any]] = []
    responses: List[Dict[str, Any]] = []
    evidence_collected: List[Dict[str, Any]] = []

    # Current state
    current_trait_id: Optional[str] = None
    current_confidence: float = 0.0
    last_response_depth: Optional[ResponseDepth] = None
    last_evidence_type: Optional[EvidenceType] = None

    def has_prior_probes_for_trait(self, trait_id: str) -> bool:
        """Check if any probes have been asked for this trait."""
        return any(p.get("trait_id") == trait_id for p in self.probes_asked)

    def evidence_for_trait(self, trait_id: str) -> List[Dict[str, Any]]:
        """Get all evidence collected for a trait."""
        return [e for e in self.evidence_collected if e.get("trait_id") == trait_id]

    def confidence_for_trait(self, trait_id: str) -> float:
        """Get confidence level for a trait assessment."""
        evidence = self.evidence_for_trait(trait_id)
        if not evidence:
            return 0.0
        # Simple confidence based on evidence count and type
        behavioral_count = sum(1 for e in evidence if e.get("type") == "BEHAVIORAL")
        return min(1.0, (len(evidence) * 0.2) + (behavioral_count * 0.3))

    def signal_gaps_for_trait(self, trait_id: str) -> List[str]:
        """Identify signal gaps for a trait."""
        gaps = []
        evidence = self.evidence_for_trait(trait_id)

        if not any(e.get("type") == "BEHAVIORAL" for e in evidence):
            gaps.append("No behavioral evidence")

        if not any(e.get("contains_conflict") for e in evidence):
            gaps.append("No conflict/failure example")

        if all(e.get("depth") == "SURFACE" for e in evidence):
            gaps.append("All responses are surface-level")

        return gaps

    def last_response_lacked(self, *elements: str) -> bool:
        """Check if last response lacked specific elements."""
        if not self.responses:
            return False
        last = self.responses[-1]
        for element in elements:
            if element not in (last.get("contains", []) or []):
                return True
        return False


class PatternSelectionResult(BaseModel):
    """Result of pattern selection for a probe."""

    patterns: List[ReasoningPattern]
    rationale: str
    priority_pattern: Optional[ReasoningPattern] = None


def select_patterns_for_context(
    trait_id: str,
    context: ProbeContext,
) -> PatternSelectionResult:
    """
    Determine which reasoning patterns to apply given current context.

    This is a rule-based selection that can be enhanced with LLM reasoning.
    """
    patterns: List[ReasoningPattern] = []
    rationale_parts: List[str] = []

    # Always apply representation choice for probe type selection
    patterns.append(ReasoningPattern.MC35_REPRESENTATION)
    rationale_parts.append("MC35: Select appropriate probe type for role/trait")

    # If first probe for trait, use assumption surfacing
    if not context.has_prior_probes_for_trait(trait_id):
        patterns.append(ReasoningPattern.MC24_ASSUMPTION)
        rationale_parts.append("MC24: First probe - surface assumptions")

    # If prior response was surface-level, increase depth
    if context.last_response_depth == ResponseDepth.SURFACE:
        patterns.append(ReasoningPattern.MC38_ABSTRACTION)
        rationale_parts.append("MC38: Prior response shallow - go deeper")

    # If response lacked conflict/failure, probe for tension
    if context.last_response_lacked("conflict", "failure", "tension"):
        patterns.append(ReasoningPattern.IP7_CONFLICT)
        rationale_parts.append("IP7: Lacking conflict examples - probe tension")

    # If response was heavy on self-report, seek behavioral evidence
    if context.last_evidence_type == EvidenceType.SELF_REPORT:
        patterns.append(ReasoningPattern.IP11_TRUST)
        rationale_parts.append("IP11: Self-report heavy - seek behavioral evidence")

    # If confidence is low, explore alternative interpretations
    if context.current_confidence < 0.5:
        patterns.append(ReasoningPattern.MC44_SOLUTION_SPACE)
        rationale_parts.append("MC44: Low confidence - explore alternatives")

    # For resilience/adaptability/initiative, always probe for risk
    if trait_id.upper() in ["RESILIENCE", "ADAPTABILITY", "INITIATIVE"]:
        patterns.append(ReasoningPattern.SP8_RISK)
        rationale_parts.append(f"SP8: {trait_id} requires risk/failure probing")

    return PatternSelectionResult(
        patterns=patterns,
        rationale="; ".join(rationale_parts),
        priority_pattern=patterns[0] if patterns else None,
    )


# Interview pattern settings for organization configuration
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
    depth_escalation_threshold: ResponseDepth = ResponseDepth.SURFACE

    # Resume customization
    enable_resume_customization: bool = True
    max_resume_anchors_per_probe: int = 2
