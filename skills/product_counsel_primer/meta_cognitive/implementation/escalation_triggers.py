"""
Sage-Mode Escalation Trigger Detection System
==============================================

Monitors task execution and detects conditions requiring cognitive mode shifts.
Handles both escalation (increase depth) and de-escalation (decrease depth) triggers.

Part of the FLO Cognitive Apprentice System.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime, timedelta
import re

from situation_classifier import CognitiveMode, SituationAssessment


# =============================================================================
# TRIGGER TYPES
# =============================================================================

class TriggerType(Enum):
    """Categories of escalation/de-escalation triggers."""

    # Escalation triggers
    COMPLEXITY_DISCOVERY = auto()      # "This is more complex than appeared"
    STAKES_REVELATION = auto()         # "This matters more than I thought"
    OPPONENT_SOPHISTICATION = auto()   # "They're thinking deeper than expected"
    ANOMALY_DETECTION = auto()         # "Something doesn't fit the pattern"
    MODEL_FAILURE = auto()             # "My predictions were wrong"
    NEW_STAKEHOLDER = auto()           # "New party entered the situation"
    PRECEDENT_IMPLICATIONS = auto()    # "This sets precedent I didn't consider"

    # De-escalation triggers
    PROBLEM_SIMPLIFICATION = auto()    # "This is simpler than it appeared"
    TIME_PRESSURE_INCREASE = auto()    # "We need to decide now"
    DIMINISHING_RETURNS = auto()       # "More analysis isn't helping"
    ALIGNMENT_DISCOVERY = auto()       # "Interests are more aligned than expected"
    PATTERN_CLARITY = auto()           # "Standard pattern clearly applies"


class TriggerDirection(Enum):
    """Direction of mode change."""
    ESCALATE = auto()      # Increase cognitive depth
    DE_ESCALATE = auto()   # Decrease cognitive depth


@dataclass
class EscalationTrigger:
    """Represents a detected trigger for mode change."""
    trigger_type: TriggerType
    direction: TriggerDirection
    confidence: float           # 0.0 to 1.0
    evidence: List[str]         # What triggered this
    suggested_mode: CognitiveMode
    rationale: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        arrow = "↑" if self.direction == TriggerDirection.ESCALATE else "↓"
        return f"{arrow} {self.trigger_type.name} ({self.confidence:.0%}) → {self.suggested_mode.name}"


@dataclass
class ExecutionState:
    """Current state of task execution for monitoring."""
    current_mode: CognitiveMode
    task_description: str
    start_time: datetime
    stakeholders_identified: List[str] = field(default_factory=list)
    predictions_made: List[Dict[str, Any]] = field(default_factory=list)
    outcomes_observed: List[Dict[str, Any]] = field(default_factory=list)
    analysis_iterations: int = 0
    anomalies_detected: List[str] = field(default_factory=list)
    context_updates: List[str] = field(default_factory=list)


# =============================================================================
# TRIGGER DETECTION RULES
# =============================================================================

class TriggerRule:
    """Base class for trigger detection rules."""

    def __init__(self, name: str, direction: TriggerDirection, priority: int = 5):
        self.name = name
        self.direction = direction
        self.priority = priority  # 1-10, higher = more important

    def check(self, state: ExecutionState, context: Dict[str, Any]) -> Optional[EscalationTrigger]:
        """Check if trigger condition is met. Override in subclasses."""
        raise NotImplementedError


class ComplexityDiscoveryRule(TriggerRule):
    """Detect when problem is more complex than initially assessed."""

    def __init__(self):
        super().__init__("complexity_discovery", TriggerDirection.ESCALATE, priority=8)

    def check(self, state: ExecutionState, context: Dict[str, Any]) -> Optional[EscalationTrigger]:
        evidence = []
        confidence = 0.0

        # Check 1: New stakeholders discovered
        initial_stakeholders = context.get('initial_stakeholder_count', 1)
        current_stakeholders = len(state.stakeholders_identified)
        if current_stakeholders > initial_stakeholders * 1.5:
            evidence.append(f"Stakeholder count grew from {initial_stakeholders} to {current_stakeholders}")
            confidence += 0.3

        # Check 2: Unexpected interdependencies
        if 'interdependencies' in context:
            if len(context['interdependencies']) > context.get('expected_interdependencies', 2):
                evidence.append("More interdependencies than expected")
                confidence += 0.25

        # Check 3: Initial assumptions invalidated
        invalidated_assumptions = context.get('invalidated_assumptions', [])
        if len(invalidated_assumptions) >= 2:
            evidence.append(f"Key assumptions invalidated: {', '.join(invalidated_assumptions[:3])}")
            confidence += 0.35

        # Check 4: Analysis revealing hidden layers
        if state.analysis_iterations > 3 and context.get('new_factors_emerging', False):
            evidence.append("Repeated analysis revealing new factors")
            confidence += 0.2

        if confidence >= 0.5:
            # Determine suggested mode (escalate by 1-2 levels)
            escalation = 2 if confidence >= 0.7 else 1
            suggested_mode = CognitiveMode(min(5, state.current_mode + escalation))

            return EscalationTrigger(
                trigger_type=TriggerType.COMPLEXITY_DISCOVERY,
                direction=TriggerDirection.ESCALATE,
                confidence=min(1.0, confidence),
                evidence=evidence,
                suggested_mode=suggested_mode,
                rationale="Problem complexity exceeds initial assessment; deeper analysis warranted"
            )

        return None


class StakesRevelationRule(TriggerRule):
    """Detect when stakes are higher than initially assessed."""

    def __init__(self):
        super().__init__("stakes_revelation", TriggerDirection.ESCALATE, priority=9)

    def check(self, state: ExecutionState, context: Dict[str, Any]) -> Optional[EscalationTrigger]:
        evidence = []
        confidence = 0.0

        # Check 1: Hidden consequences discovered
        hidden_consequences = context.get('discovered_consequences', [])
        if hidden_consequences:
            evidence.append(f"Hidden consequences: {', '.join(hidden_consequences[:3])}")
            confidence += 0.3 * min(1.0, len(hidden_consequences) / 3)

        # Check 2: Precedent implications recognized
        if context.get('precedent_setting', False):
            evidence.append("Decision sets significant precedent")
            confidence += 0.3

        # Check 3: Reputation effects identified
        if context.get('reputation_at_risk', False):
            evidence.append("Reputation implications discovered")
            confidence += 0.25

        # Check 4: Financial exposure larger than expected
        initial_exposure = context.get('initial_financial_exposure', 0)
        current_exposure = context.get('current_financial_exposure', 0)
        if current_exposure > initial_exposure * 2:
            evidence.append(f"Financial exposure {current_exposure/initial_exposure:.1f}x initial estimate")
            confidence += 0.35

        # Check 5: Career implications discovered
        if context.get('career_implications', False):
            evidence.append("Career-defining implications identified")
            confidence += 0.4

        if confidence >= 0.5:
            escalation = 2 if confidence >= 0.8 else 1
            suggested_mode = CognitiveMode(min(5, state.current_mode + escalation))

            return EscalationTrigger(
                trigger_type=TriggerType.STAKES_REVELATION,
                direction=TriggerDirection.ESCALATE,
                confidence=min(1.0, confidence),
                evidence=evidence,
                suggested_mode=suggested_mode,
                rationale="Stakes are higher than initially assessed; requires more careful analysis"
            )

        return None


class OpponentSophisticationRule(TriggerRule):
    """Detect when counterparty is more sophisticated than expected."""

    def __init__(self):
        super().__init__("opponent_sophistication", TriggerDirection.ESCALATE, priority=8)

    def check(self, state: ExecutionState, context: Dict[str, Any]) -> Optional[EscalationTrigger]:
        evidence = []
        confidence = 0.0

        # Check 1: Strategic moves that suggest recursive thinking
        strategic_moves = context.get('opponent_strategic_moves', [])
        for move in strategic_moves:
            if move.get('suggests_recursive_modeling', False):
                evidence.append(f"Move suggests they're modeling our thinking: {move.get('description', 'N/A')}")
                confidence += 0.25

        # Check 2: Information asymmetry detected
        if context.get('information_asymmetry_detected', False):
            evidence.append("Opponent appears to have information advantage")
            confidence += 0.2

        # Check 3: Unexpected counter-proposals
        unexpected_counters = context.get('unexpected_counter_proposals', 0)
        if unexpected_counters >= 2:
            evidence.append(f"{unexpected_counters} unexpectedly sophisticated counter-proposals")
            confidence += 0.25

        # Check 4: They're anticipating our moves
        if context.get('opponent_anticipating_moves', False):
            evidence.append("Opponent appears to be anticipating our strategy")
            confidence += 0.3

        # Check 5: Coalition-building behavior observed
        if context.get('opponent_coalition_building', False):
            evidence.append("Opponent engaging in coalition building")
            confidence += 0.2

        if confidence >= 0.5:
            # Sophisticated opponents always warrant at least MASTER mode
            suggested_mode = CognitiveMode(max(4, min(5, state.current_mode + 1)))

            return EscalationTrigger(
                trigger_type=TriggerType.OPPONENT_SOPHISTICATION,
                direction=TriggerDirection.ESCALATE,
                confidence=min(1.0, confidence),
                evidence=evidence,
                suggested_mode=suggested_mode,
                rationale="Counterparty demonstrating sophisticated strategic thinking; need MC4 recursive modeling"
            )

        return None


class AnomalyDetectionRule(TriggerRule):
    """Detect when observations don't match predictions/patterns."""

    def __init__(self):
        super().__init__("anomaly_detection", TriggerDirection.ESCALATE, priority=7)

    def check(self, state: ExecutionState, context: Dict[str, Any]) -> Optional[EscalationTrigger]:
        evidence = []
        confidence = 0.0

        # Check 1: Prediction failures
        prediction_accuracy = self._calculate_prediction_accuracy(state)
        if prediction_accuracy is not None and prediction_accuracy < 0.6:
            evidence.append(f"Prediction accuracy only {prediction_accuracy:.0%}")
            confidence += 0.3 * (1 - prediction_accuracy)

        # Check 2: Behavior doesn't match stakeholder models
        model_mismatches = context.get('stakeholder_model_mismatches', [])
        if model_mismatches:
            evidence.append(f"Stakeholder behavior deviating from model: {', '.join(model_mismatches[:2])}")
            confidence += 0.25

        # Check 3: Explicit anomalies detected during execution
        if state.anomalies_detected:
            evidence.append(f"Anomalies during execution: {', '.join(state.anomalies_detected[:2])}")
            confidence += 0.2 * min(1.0, len(state.anomalies_detected) / 3)

        # Check 4: Intuition signals concern
        if context.get('intuition_concern', False):
            evidence.append("Intuition flags: something doesn't feel right")
            confidence += 0.25

        # Check 5: Outcomes diverging from expectations
        if context.get('outcomes_diverging', False):
            evidence.append("Outcomes significantly diverging from expectations")
            confidence += 0.3

        if confidence >= 0.4:  # Lower threshold for anomalies - they're important signals
            suggested_mode = CognitiveMode(min(5, state.current_mode + 1))

            return EscalationTrigger(
                trigger_type=TriggerType.ANOMALY_DETECTION,
                direction=TriggerDirection.ESCALATE,
                confidence=min(1.0, confidence),
                evidence=evidence,
                suggested_mode=suggested_mode,
                rationale="Observations don't match patterns; need deeper investigation"
            )

        return None

    def _calculate_prediction_accuracy(self, state: ExecutionState) -> Optional[float]:
        """Calculate how well predictions matched outcomes."""
        if not state.predictions_made or not state.outcomes_observed:
            return None

        matches = 0
        for pred in state.predictions_made:
            pred_id = pred.get('id')
            for outcome in state.outcomes_observed:
                if outcome.get('prediction_id') == pred_id:
                    if outcome.get('matched', False):
                        matches += 1
                    break

        return matches / len(state.predictions_made) if state.predictions_made else None


class ProblemSimplificationRule(TriggerRule):
    """Detect when problem is simpler than initially assessed."""

    def __init__(self):
        super().__init__("problem_simplification", TriggerDirection.DE_ESCALATE, priority=6)

    def check(self, state: ExecutionState, context: Dict[str, Any]) -> Optional[EscalationTrigger]:
        evidence = []
        confidence = 0.0

        # Check 1: Stakeholder interests more aligned than expected
        if context.get('interests_aligned', False):
            evidence.append("Stakeholder interests more aligned than expected")
            confidence += 0.35

        # Check 2: Standard pattern clearly applies
        if context.get('standard_pattern_applies', False):
            evidence.append("Recognized: standard pattern applies")
            confidence += 0.3

        # Check 3: Complexity was surface-level only
        if context.get('surface_complexity_resolved', False):
            evidence.append("Initial complexity resolved to simple structure")
            confidence += 0.25

        # Check 4: Single decision-maker identified
        if context.get('single_decision_maker', False):
            evidence.append("Single decision-maker (no coalition dynamics)")
            confidence += 0.2

        # Check 5: No sophisticated opponents
        if not context.get('sophisticated_actors_present', True):
            evidence.append("No sophisticated strategic actors")
            confidence += 0.2

        if confidence >= 0.5:
            de_escalation = 2 if confidence >= 0.8 else 1
            suggested_mode = CognitiveMode(max(1, state.current_mode - de_escalation))

            return EscalationTrigger(
                trigger_type=TriggerType.PROBLEM_SIMPLIFICATION,
                direction=TriggerDirection.DE_ESCALATE,
                confidence=min(1.0, confidence),
                evidence=evidence,
                suggested_mode=suggested_mode,
                rationale="Problem simpler than assessed; reduce cognitive investment"
            )

        return None


class TimePressureIncreaseRule(TriggerRule):
    """Detect when time constraints require faster decision-making."""

    def __init__(self):
        super().__init__("time_pressure_increase", TriggerDirection.DE_ESCALATE, priority=9)

    def check(self, state: ExecutionState, context: Dict[str, Any]) -> Optional[EscalationTrigger]:
        evidence = []
        confidence = 0.0

        # Check 1: External deadline imposed
        deadline = context.get('deadline')
        if deadline:
            time_remaining = deadline - datetime.now()
            if time_remaining < timedelta(hours=1):
                evidence.append(f"Less than 1 hour to deadline")
                confidence += 0.5
            elif time_remaining < timedelta(hours=4):
                evidence.append(f"Less than 4 hours to deadline")
                confidence += 0.3

        # Check 2: Window of opportunity closing
        if context.get('opportunity_window_closing', False):
            evidence.append("Window of opportunity closing")
            confidence += 0.35

        # Check 3: Crisis conditions emerging
        if context.get('crisis_emerging', False):
            evidence.append("Crisis conditions detected")
            confidence += 0.4

        # Check 4: Decision requested immediately
        if context.get('immediate_decision_requested', False):
            evidence.append("Immediate decision requested by stakeholder")
            confidence += 0.35

        if confidence >= 0.4:
            # In crisis, cap at EXPERT mode (can't do deep analysis)
            if confidence >= 0.7:
                suggested_mode = CognitiveMode(min(3, state.current_mode))
            else:
                suggested_mode = CognitiveMode(max(1, state.current_mode - 1))

            return EscalationTrigger(
                trigger_type=TriggerType.TIME_PRESSURE_INCREASE,
                direction=TriggerDirection.DE_ESCALATE,
                confidence=min(1.0, confidence),
                evidence=evidence,
                suggested_mode=suggested_mode,
                rationale="Time pressure requires faster decision-making; reduce analysis depth"
            )

        return None


class DiminishingReturnsRule(TriggerRule):
    """Detect when further analysis isn't yielding new insights."""

    def __init__(self):
        super().__init__("diminishing_returns", TriggerDirection.DE_ESCALATE, priority=6)

    def check(self, state: ExecutionState, context: Dict[str, Any]) -> Optional[EscalationTrigger]:
        evidence = []
        confidence = 0.0

        # Check 1: Analysis yielding same conclusions
        if state.analysis_iterations >= 3:
            conclusions_stable = context.get('conclusions_stable_iterations', 0)
            if conclusions_stable >= 2:
                evidence.append(f"Conclusions unchanged for {conclusions_stable} iterations")
                confidence += 0.35

        # Check 2: Uncertainty not reducible
        if context.get('irreducible_uncertainty', False):
            evidence.append("Remaining uncertainty cannot be reduced with available information")
            confidence += 0.3

        # Check 3: Decision paralysis risk
        time_in_analysis = datetime.now() - state.start_time
        expected_duration = context.get('expected_analysis_duration', timedelta(hours=2))
        if time_in_analysis > expected_duration * 2:
            evidence.append(f"Analysis taking {time_in_analysis.total_seconds()/3600:.1f}x expected time")
            confidence += 0.25

        # Check 4: No new patterns emerging
        if context.get('pattern_saturation', False):
            evidence.append("Pattern analysis saturated - no new patterns emerging")
            confidence += 0.3

        if confidence >= 0.5:
            suggested_mode = CognitiveMode(max(1, state.current_mode - 1))

            return EscalationTrigger(
                trigger_type=TriggerType.DIMINISHING_RETURNS,
                direction=TriggerDirection.DE_ESCALATE,
                confidence=min(1.0, confidence),
                evidence=evidence,
                suggested_mode=suggested_mode,
                rationale="Further analysis showing diminishing returns; time to decide with current information"
            )

        return None


# =============================================================================
# TRIGGER MONITOR
# =============================================================================

class EscalationMonitor:
    """
    Main monitoring system that evaluates triggers during task execution.

    Usage:
        monitor = EscalationMonitor()

        # Initialize for a task
        state = ExecutionState(
            current_mode=CognitiveMode.EXPERT,
            task_description="Negotiate partnership agreement",
            start_time=datetime.now()
        )

        # During execution, update context and check triggers
        context = {
            'opponent_strategic_moves': [{'suggests_recursive_modeling': True, 'description': 'Asked about our BATNA'}],
            'information_asymmetry_detected': True
        }

        triggers = monitor.check_all_triggers(state, context)
        decision = monitor.evaluate_triggers(triggers, state)
    """

    def __init__(self):
        # Initialize all trigger rules
        self.escalation_rules: List[TriggerRule] = [
            ComplexityDiscoveryRule(),
            StakesRevelationRule(),
            OpponentSophisticationRule(),
            AnomalyDetectionRule(),
        ]

        self.de_escalation_rules: List[TriggerRule] = [
            ProblemSimplificationRule(),
            TimePressureIncreaseRule(),
            DiminishingReturnsRule(),
        ]

        # Configuration
        self.escalation_threshold = 0.6    # Confidence needed to escalate
        self.de_escalation_threshold = 0.7  # Higher threshold to de-escalate (be cautious)
        self.min_time_between_shifts = timedelta(minutes=5)
        self.last_mode_shift: Optional[datetime] = None

    def check_all_triggers(
        self,
        state: ExecutionState,
        context: Dict[str, Any]
    ) -> List[EscalationTrigger]:
        """
        Check all trigger rules against current state and context.
        Returns list of triggered conditions, sorted by priority.
        """
        triggers = []

        # Check escalation rules
        for rule in self.escalation_rules:
            trigger = rule.check(state, context)
            if trigger:
                triggers.append(trigger)

        # Check de-escalation rules
        for rule in self.de_escalation_rules:
            trigger = rule.check(state, context)
            if trigger:
                triggers.append(trigger)

        # Sort by priority (higher first) then confidence
        triggers.sort(key=lambda t: (
            -self._get_rule_priority(t.trigger_type),
            -t.confidence
        ))

        return triggers

    def _get_rule_priority(self, trigger_type: TriggerType) -> int:
        """Get priority for a trigger type."""
        priority_map = {
            TriggerType.STAKES_REVELATION: 9,
            TriggerType.TIME_PRESSURE_INCREASE: 9,
            TriggerType.COMPLEXITY_DISCOVERY: 8,
            TriggerType.OPPONENT_SOPHISTICATION: 8,
            TriggerType.ANOMALY_DETECTION: 7,
            TriggerType.MODEL_FAILURE: 7,
            TriggerType.PROBLEM_SIMPLIFICATION: 6,
            TriggerType.DIMINISHING_RETURNS: 6,
            TriggerType.NEW_STAKEHOLDER: 5,
            TriggerType.PRECEDENT_IMPLICATIONS: 5,
            TriggerType.ALIGNMENT_DISCOVERY: 4,
            TriggerType.PATTERN_CLARITY: 4,
        }
        return priority_map.get(trigger_type, 5)

    def evaluate_triggers(
        self,
        triggers: List[EscalationTrigger],
        state: ExecutionState
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate triggered conditions and recommend mode change if warranted.

        Returns:
            None if no mode change recommended
            Dict with mode change recommendation if warranted
        """
        if not triggers:
            return None

        # Check cooldown period
        if self.last_mode_shift:
            time_since_shift = datetime.now() - self.last_mode_shift
            if time_since_shift < self.min_time_between_shifts:
                return {
                    'action': 'WAIT',
                    'reason': f"Cooldown period: {(self.min_time_between_shifts - time_since_shift).seconds}s remaining",
                    'triggers_detected': [str(t) for t in triggers]
                }

        # Separate escalation and de-escalation triggers
        escalation_triggers = [t for t in triggers if t.direction == TriggerDirection.ESCALATE]
        de_escalation_triggers = [t for t in triggers if t.direction == TriggerDirection.DE_ESCALATE]

        # Evaluate escalation (takes priority if both present)
        if escalation_triggers:
            top_trigger = escalation_triggers[0]
            if top_trigger.confidence >= self.escalation_threshold:
                return self._recommend_escalation(top_trigger, state, triggers)

        # Evaluate de-escalation
        if de_escalation_triggers:
            top_trigger = de_escalation_triggers[0]
            if top_trigger.confidence >= self.de_escalation_threshold:
                # Don't de-escalate if there are also escalation signals
                if escalation_triggers and escalation_triggers[0].confidence > 0.4:
                    return {
                        'action': 'HOLD',
                        'reason': "Conflicting signals: escalation and de-escalation triggers both present",
                        'triggers_detected': [str(t) for t in triggers]
                    }
                return self._recommend_de_escalation(top_trigger, state, triggers)

        # No action needed
        return {
            'action': 'CONTINUE',
            'reason': "No triggers met confidence threshold",
            'triggers_detected': [str(t) for t in triggers]
        }

    def _recommend_escalation(
        self,
        trigger: EscalationTrigger,
        state: ExecutionState,
        all_triggers: List[EscalationTrigger]
    ) -> Dict[str, Any]:
        """Generate escalation recommendation."""

        # Validate escalation is actually an increase
        if trigger.suggested_mode <= state.current_mode:
            return {
                'action': 'CONTINUE',
                'reason': f"Already at or above suggested mode ({trigger.suggested_mode.name})"
            }

        return {
            'action': 'ESCALATE',
            'from_mode': state.current_mode.name,
            'to_mode': trigger.suggested_mode.name,
            'primary_trigger': trigger.trigger_type.name,
            'confidence': trigger.confidence,
            'evidence': trigger.evidence,
            'rationale': trigger.rationale,
            'all_triggers': [str(t) for t in all_triggers],
            'mentoring_note': self._generate_escalation_mentoring(trigger, state),
            'patterns_to_activate': self._patterns_to_activate(state.current_mode, trigger.suggested_mode)
        }

    def _recommend_de_escalation(
        self,
        trigger: EscalationTrigger,
        state: ExecutionState,
        all_triggers: List[EscalationTrigger]
    ) -> Dict[str, Any]:
        """Generate de-escalation recommendation."""

        # Validate de-escalation is actually a decrease
        if trigger.suggested_mode >= state.current_mode:
            return {
                'action': 'CONTINUE',
                'reason': f"Already at or below suggested mode ({trigger.suggested_mode.name})"
            }

        return {
            'action': 'DE_ESCALATE',
            'from_mode': state.current_mode.name,
            'to_mode': trigger.suggested_mode.name,
            'primary_trigger': trigger.trigger_type.name,
            'confidence': trigger.confidence,
            'evidence': trigger.evidence,
            'rationale': trigger.rationale,
            'all_triggers': [str(t) for t in all_triggers],
            'mentoring_note': self._generate_de_escalation_mentoring(trigger, state),
            'patterns_to_deactivate': self._patterns_to_deactivate(state.current_mode, trigger.suggested_mode)
        }

    def _generate_escalation_mentoring(
        self,
        trigger: EscalationTrigger,
        state: ExecutionState
    ) -> str:
        """Generate teaching note for escalation."""

        notes = {
            TriggerType.COMPLEXITY_DISCOVERY: (
                "TEACHING: When you discover a situation is more complex than initially assessed, "
                "don't continue with shallow analysis hoping to 'get through it.' "
                "Invest the cognitive resources the situation actually requires. "
                "Key signals: new stakeholders appearing, unexpected interdependencies, "
                "or assumptions being invalidated."
            ),
            TriggerType.STAKES_REVELATION: (
                "TEACHING: Stakes often reveal themselves during analysis, not before. "
                "Watch for hidden consequences, precedent implications, and reputation effects. "
                "When stakes escalate, your cognitive investment should escalate proportionally."
            ),
            TriggerType.OPPONENT_SOPHISTICATION: (
                "TEACHING: When counterparties demonstrate recursive strategic thinking, "
                "you need to match or exceed their depth. Key signals: they seem to be "
                "anticipating your moves, asking probing questions about your constraints, "
                "or making unexpectedly sophisticated counter-proposals."
            ),
            TriggerType.ANOMALY_DETECTION: (
                "TEACHING: Anomalies are important signals. When behavior doesn't match "
                "your models or predictions, don't dismiss it—investigate deeper. "
                "Your intuition detecting 'something off' is often picking up on "
                "patterns your conscious analysis hasn't yet identified."
            ),
        }

        return notes.get(trigger.trigger_type, f"Escalating due to: {trigger.rationale}")

    def _generate_de_escalation_mentoring(
        self,
        trigger: EscalationTrigger,
        state: ExecutionState
    ) -> str:
        """Generate teaching note for de-escalation."""

        notes = {
            TriggerType.PROBLEM_SIMPLIFICATION: (
                "TEACHING: When a problem reveals itself to be simpler than expected, "
                "don't continue with excessive analysis out of habit or fear. "
                "Recognize when standard patterns apply and deploy proportionate resources. "
                "Over-analysis wastes cognitive budget for truly complex situations."
            ),
            TriggerType.TIME_PRESSURE_INCREASE: (
                "TEACHING: When time pressure increases, you must shift from thorough "
                "to 'good enough.' Perfect analysis delivered too late is worthless. "
                "Make the best decision you can with available information and time. "
                "This is a skill—knowing when to stop analyzing and act."
            ),
            TriggerType.DIMINISHING_RETURNS: (
                "TEACHING: Recognize when further analysis isn't adding value. "
                "If conclusions are stable across iterations, and remaining uncertainty "
                "is irreducible, it's time to decide. Analysis paralysis is a failure mode. "
                "The sage knows when to stop analyzing."
            ),
        }

        return notes.get(trigger.trigger_type, f"De-escalating due to: {trigger.rationale}")

    def _patterns_to_activate(
        self,
        from_mode: CognitiveMode,
        to_mode: CognitiveMode
    ) -> List[str]:
        """Determine which patterns to activate when escalating."""

        activations = {
            (CognitiveMode.REFLEX, CognitiveMode.COMPETENT): [
                "Tier 1 Structural Patterns (S1-S5)",
                "Basic stakeholder identification"
            ],
            (CognitiveMode.COMPETENT, CognitiveMode.EXPERT): [
                "Tier 2 Behavioral Patterns (BI1-BI5)",
                "Implicit MC pattern application",
                "Trajectory forecasting"
            ],
            (CognitiveMode.EXPERT, CognitiveMode.MASTER): [
                "Explicit MC1-MC8 patterns",
                "Deep stakeholder mental modeling",
                "Coalition possibility mapping",
                "Information revelation strategy"
            ],
            (CognitiveMode.MASTER, CognitiveMode.SAGE): [
                "Deep recursive modeling (MC4 level 3+)",
                "Meta-pattern awareness",
                "Uncertainty quantification",
                "Wisdom heuristics"
            ],
        }

        # Handle multi-level jumps
        patterns = []
        for start in range(from_mode, to_mode):
            key = (CognitiveMode(start), CognitiveMode(start + 1))
            if key in activations:
                patterns.extend(activations[key])

        return patterns

    def _patterns_to_deactivate(
        self,
        from_mode: CognitiveMode,
        to_mode: CognitiveMode
    ) -> List[str]:
        """Determine which patterns to deactivate when de-escalating."""
        # Reverse of activation
        return self._patterns_to_activate(to_mode, from_mode)

    def apply_mode_shift(
        self,
        state: ExecutionState,
        recommendation: Dict[str, Any]
    ) -> ExecutionState:
        """
        Apply a mode shift and update state.
        """
        if recommendation.get('action') in ('ESCALATE', 'DE_ESCALATE'):
            new_mode = CognitiveMode[recommendation['to_mode']]
            state.current_mode = new_mode
            state.context_updates.append(
                f"Mode shifted to {new_mode.name} due to {recommendation['primary_trigger']}"
            )
            self.last_mode_shift = datetime.now()

        return state


# =============================================================================
# CONTINUOUS MONITORING LOOP
# =============================================================================

class ContinuousMonitor:
    """
    Wrapper for continuous monitoring during task execution.
    Integrates with execution loop to check triggers at appropriate intervals.
    """

    def __init__(self, check_interval: timedelta = timedelta(seconds=30)):
        self.monitor = EscalationMonitor()
        self.check_interval = check_interval
        self.last_check: Optional[datetime] = None

    def should_check(self) -> bool:
        """Determine if it's time for another trigger check."""
        if self.last_check is None:
            return True
        return datetime.now() - self.last_check >= self.check_interval

    def check_and_recommend(
        self,
        state: ExecutionState,
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Check triggers and return recommendation if any.
        Updates last_check timestamp.
        """
        if not self.should_check():
            return None

        self.last_check = datetime.now()
        triggers = self.monitor.check_all_triggers(state, context)
        return self.monitor.evaluate_triggers(triggers, state)


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_usage():
    """Demonstrate escalation trigger detection."""

    print("=" * 70)
    print("ESCALATION TRIGGER DETECTION SYSTEM - Examples")
    print("=" * 70)

    monitor = EscalationMonitor()

    # Example 1: Opponent sophistication escalation
    print("\nEXAMPLE 1: Opponent Sophistication Detected")
    print("-" * 50)

    state = ExecutionState(
        current_mode=CognitiveMode.EXPERT,
        task_description="Negotiate partnership agreement",
        start_time=datetime.now()
    )

    context = {
        'opponent_strategic_moves': [
            {'suggests_recursive_modeling': True, 'description': 'Asked about our BATNA'},
            {'suggests_recursive_modeling': True, 'description': 'Proposed conditional terms based on our perceived constraints'}
        ],
        'information_asymmetry_detected': True,
        'unexpected_counter_proposals': 2
    }

    triggers = monitor.check_all_triggers(state, context)
    recommendation = monitor.evaluate_triggers(triggers, state)

    print(f"Current mode: {state.current_mode.name}")
    print(f"Triggers detected: {len(triggers)}")
    for t in triggers:
        print(f"  • {t}")
    print(f"\nRecommendation: {recommendation.get('action')}")
    if recommendation.get('action') == 'ESCALATE':
        print(f"  → Escalate to: {recommendation.get('to_mode')}")
        print(f"  → Confidence: {recommendation.get('confidence'):.0%}")
        print(f"  → Evidence: {', '.join(recommendation.get('evidence', []))}")
        print(f"\nMentoring Note:\n  {recommendation.get('mentoring_note')}")

    # Example 2: Time pressure de-escalation
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Time Pressure Increase")
    print("-" * 50)

    state = ExecutionState(
        current_mode=CognitiveMode.MASTER,
        task_description="Strategic decision on acquisition structure",
        start_time=datetime.now() - timedelta(hours=3)
    )

    context = {
        'deadline': datetime.now() + timedelta(minutes=30),
        'crisis_emerging': True,
        'immediate_decision_requested': True
    }

    triggers = monitor.check_all_triggers(state, context)
    recommendation = monitor.evaluate_triggers(triggers, state)

    print(f"Current mode: {state.current_mode.name}")
    print(f"Triggers detected: {len(triggers)}")
    for t in triggers:
        print(f"  • {t}")
    print(f"\nRecommendation: {recommendation.get('action')}")
    if recommendation.get('action') == 'DE_ESCALATE':
        print(f"  → De-escalate to: {recommendation.get('to_mode')}")
        print(f"  → Confidence: {recommendation.get('confidence'):.0%}")
        print(f"\nMentoring Note:\n  {recommendation.get('mentoring_note')}")

    # Example 3: Conflicting signals
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Conflicting Escalation/De-escalation Signals")
    print("-" * 50)

    state = ExecutionState(
        current_mode=CognitiveMode.EXPERT,
        task_description="Complex negotiation under time pressure",
        start_time=datetime.now() - timedelta(hours=1)
    )

    context = {
        # Escalation signals
        'opponent_strategic_moves': [
            {'suggests_recursive_modeling': True, 'description': 'Sophisticated counter-proposal'}
        ],
        # De-escalation signals
        'deadline': datetime.now() + timedelta(hours=2),
        'opportunity_window_closing': True
    }

    triggers = monitor.check_all_triggers(state, context)
    recommendation = monitor.evaluate_triggers(triggers, state)

    print(f"Current mode: {state.current_mode.name}")
    print(f"Triggers detected: {len(triggers)}")
    for t in triggers:
        print(f"  • {t}")
    print(f"\nRecommendation: {recommendation.get('action')}")
    print(f"Reason: {recommendation.get('reason')}")


if __name__ == "__main__":
    example_usage()
