"""
Services package for AP API.

This package contains the core business logic services:
- LLMClient: Wrapper for Anthropic Claude API
- PatternAwareProbeGenerator: Intelligent interview probe generation
- PatternAwareResponseAnalyzer: Response analysis and evidence extraction
- ResumeInformedProbeCustomizer: Resume-anchored probe customization
- InterviewEngine: Core interview orchestrator (STAR+ methodology)
- ScoreCalibrator: Evidence-weighted scoring with explanations
"""

from app.services.llm_client import LLMClient, get_llm_client
from app.services.patterns import (
    ReasoningPattern,
    EvidenceType,
    ResponseDepth,
    ProbeContext,
    PatternSelectionResult,
    select_patterns_for_context,
    EVIDENCE_WEIGHTS,
    PATTERN_DESCRIPTIONS,
)
from app.services.probe_generator import (
    PatternAwareProbeGenerator,
    GeneratedProbe,
    ProbeGenerationContext,
    get_probe_generator,
)
from app.services.response_analyzer import (
    PatternAwareResponseAnalyzer,
    ResponseAnalysis,
    ExtractedEvidence,
    OmissionAnalysis,
    ResponseQuality,
    get_response_analyzer,
)
from app.services.resume_customizer import (
    ResumeInformedProbeCustomizer,
    ResumeElement,
    ProbeCustomization,
    ResumeProbeOpportunity,
    get_resume_customizer,
)
from app.services.interview_engine import (
    InterviewEngine,
    InterviewState,
    InterviewResponse,
    InterviewConfig,
    TraitProgress,
    InterviewPhase,
    ProbePhase,
    get_interview_engine,
)
from app.services.score_calibrator import (
    ScoreCalibrator,
    CalibratedTraitScore,
    CompositeScore,
    AssessmentResult,
    EvidenceForScoring,
    Recommendation,
    get_score_calibrator,
)
from app.services.job_analyzer import JobDescriptionAnalyzer, get_job_analyzer
from app.services.resume_parser import (
    ResumeParser,
    ResumeParserError,
    get_resume_parser,
)
from app.services.resume_analyzer import (
    ResumeAnalyzer,
    get_resume_analyzer,
)
from app.services.qualification_screener import (
    QualificationScreener,
    get_qualification_screener,
)
from app.services.email_service import (
    EmailService,
    get_email_service,
)

__all__ = [
    # LLM Client
    "LLMClient",
    "get_llm_client",
    # Patterns
    "ReasoningPattern",
    "EvidenceType",
    "ResponseDepth",
    "ProbeContext",
    "PatternSelectionResult",
    "select_patterns_for_context",
    "EVIDENCE_WEIGHTS",
    "PATTERN_DESCRIPTIONS",
    # Probe Generator
    "PatternAwareProbeGenerator",
    "GeneratedProbe",
    "ProbeGenerationContext",
    "get_probe_generator",
    # Response Analyzer
    "PatternAwareResponseAnalyzer",
    "ResponseAnalysis",
    "ExtractedEvidence",
    "OmissionAnalysis",
    "ResponseQuality",
    "get_response_analyzer",
    # Resume Customizer
    "ResumeInformedProbeCustomizer",
    "ResumeElement",
    "ProbeCustomization",
    "ResumeProbeOpportunity",
    "get_resume_customizer",
    # Interview Engine
    "InterviewEngine",
    "InterviewState",
    "InterviewResponse",
    "InterviewConfig",
    "TraitProgress",
    "InterviewPhase",
    "ProbePhase",
    "get_interview_engine",
    # Score Calibrator
    "ScoreCalibrator",
    "CalibratedTraitScore",
    "CompositeScore",
    "AssessmentResult",
    "EvidenceForScoring",
    "Recommendation",
    "get_score_calibrator",
    # Job Analyzer
    "JobDescriptionAnalyzer",
    "get_job_analyzer",
    # Resume Parser
    "ResumeParser",
    "ResumeParserError",
    "get_resume_parser",
    # Resume Analyzer
    "ResumeAnalyzer",
    "get_resume_analyzer",
    # Qualification Screener
    "QualificationScreener",
    "get_qualification_screener",
    # Email Service
    "EmailService",
    "get_email_service",
]
