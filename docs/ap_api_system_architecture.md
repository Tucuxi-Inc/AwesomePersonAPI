# AP API System Architecture

## Complete Technical Design for Awesome Person Assessment Platform

**Version 2.0 | January 2026** **Author: Kevin Keller, Tucuxi Inc.**

---

## 1\. System Overview

### 1.1 Vision

The AP API (Awesome Person API) is a comprehensive talent assessment platform that combines organizational learning with candidate evaluation. The system operates in two complementary modes:

1. **Profile Development Mode**: Extract trait profiles from existing top performers through training-framed engagement sessions  
2. **Candidate Assessment Mode**: Evaluate candidates against organization-specific (or research-based default) rubrics

The platform prioritizes **traceability**, **objectivity**, and **explainability**—every score can be traced to its source evidence, every rubric to its derivation, and every decision to its reasoning.

### 1.2 Core Principles

| Principle | Implementation |
| :---- | :---- |
| **Traceability** | Every score links to source evidence; every rubric links to derivation method |
| **Objectivity** | Behavioral evidence weighted over self-report; consistent scoring algorithms |
| **Explainability** | Human-readable rationale accompanies every score and recommendation |
| **Auditability** | Complete chain of custody from rubric creation through candidate scoring |
| **Adaptability** | Research-based defaults with organization-specific customization |

### 1.3 System Architecture Overview

┌─────────────────────────────────────────────────────────────────────────────────┐

│                              AP API PLATFORM                                     │

├─────────────────────────────────────────────────────────────────────────────────┤

│                                                                                  │

│  ╔═══════════════════════════════════════════════════════════════════════════╗  │

│  ║                    PROFILE DEVELOPMENT SUBSYSTEM                          ║  │

│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      ║  │

│  ║  │  Scenario   │  │  Training   │  │   Profile   │  │   Rubric    │      ║  │

│  ║  │  Generator  │  │   Session   │  │  Extractor  │  │  Synthesizer│      ║  │

│  ║  │             │  │   Engine    │  │             │  │             │      ║  │

│  ║  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      ║  │

│  ║         └─────────────────┴─────────────────┴─────────────────┘           ║  │

│  ╚═══════════════════════════════════════════════════════════════════════════╝  │

│                                      │                                           │

│                                      ▼                                           │

│                        ┌─────────────────────────┐                               │

│                        │     RUBRIC REGISTRY     │                               │

│                        │  ┌─────────┬─────────┐  │                               │

│                        │  │Research │ Org-    │  │                               │

│                        │  │Defaults │ Specific│  │                               │

│                        │  └─────────┴─────────┘  │                               │

│                        └────────────┬────────────┘                               │

│                                     │                                            │

│  ╔═══════════════════════════════════════════════════════════════════════════╗  │

│  ║                   CANDIDATE ASSESSMENT SUBSYSTEM                          ║  │

│  ║  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      ║  │

│  ║  │   Resume    │  │   Stack     │  │  Interview  │  │   Score     │      ║  │

│  ║  │  Analyzer   │  │   Ranker    │  │   Engine    │  │  Calibrator │      ║  │

│  ║  │             │  │  /Clusterer │  │             │  │             │      ║  │

│  ║  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      ║  │

│  ║         └─────────────────┴─────────────────┴─────────────────┘           ║  │

│  ╚═══════════════════════════════════════════════════════════════════════════╝  │

│                                      │                                           │

│                                      ▼                                           │

│                        ┌─────────────────────────┐                               │

│                        │   TRACEABILITY ENGINE   │                               │

│                        │  ┌─────────┬─────────┐  │                               │

│                        │  │Evidence │ Audit   │  │                               │

│                        │  │ Chain   │  Trail  │  │                               │

│                        │  └─────────┴─────────┘  │                               │

│                        └─────────────────────────┘                               │

│                                                                                  │

└─────────────────────────────────────────────────────────────────────────────────┘

---

## 2\. Profile Development Subsystem

### 2.1 Purpose

Extract organization-specific trait profiles and scoring rubrics from top performers through training-framed engagement sessions, creating a defensible, traceable basis for candidate evaluation.

### 2.2 Data Flow

┌──────────────┐     ┌──────────────┐     ┌──────────────┐

│     Job      │     │     Top      │     │  Research    │

│ Description  │     │  Performers  │     │  Defaults    │

└──────┬───────┘     └──────┬───────┘     └──────┬───────┘

       │                    │                    │

       ▼                    │                    │

┌──────────────┐            │                    │

│   Scenario   │            │                    │

│  Generator   │            │                    │

└──────┬───────┘            │                    │

       │                    │                    │

       ▼                    ▼                    │

┌─────────────────────────────┐                  │

│     Training Session        │                  │

│         Engine              │                  │

│  (Expert-Teacher Framing)   │                  │

└──────────────┬──────────────┘                  │

               │                                 │

               ▼                                 │

┌─────────────────────────────┐                  │

│     Profile Extractor       │                  │

│  (Trait Signal Analysis)    │                  │

└──────────────┬──────────────┘                  │

               │                                 │

               ▼                                 │

┌─────────────────────────────┐                  │

│     Rubric Synthesizer      │◄─────────────────┘

│  (Merge Org \+ Defaults)     │

└──────────────┬──────────────┘

               │

               ▼

┌─────────────────────────────┐

│      RUBRIC REGISTRY        │

│   (Versioned, Traceable)    │

└─────────────────────────────┘

### 2.3 Module: Scenario Generator

**Purpose**: Generate role-specific scenarios that surface trait-revealing responses.

**Inputs**:

- Job description  
- Role category  
- Target traits to assess  
- (Optional) Organization context

**Outputs**:

- Set of 12-18 scenarios covering all target traits  
- Extraction question sequences per scenario  
- Trait mapping guides

**Processing Logic**:

class ScenarioGenerator:

    def generate\_scenarios(self, 

                          job\_description: str,

                          role\_category: str,

                          target\_traits: List\[str\]) \-\> ScenarioSet:

        

        \# Extract role-specific elements

        responsibilities \= self.extract\_responsibilities(job\_description)

        stakeholders \= self.extract\_stakeholders(job\_description)

        decision\_points \= self.identify\_decision\_points(responsibilities)

        

        scenarios \= \[\]

        

        \# Generate 2-3 scenarios per trait

        for trait in target\_traits:

            trait\_scenarios \= self.generate\_trait\_scenarios(

                trait=trait,

                responsibilities=responsibilities,

                stakeholders=stakeholders,

                decision\_points=decision\_points,

                role\_category=role\_category

            )

            scenarios.extend(trait\_scenarios)

        

        \# Add extraction questions and trait mapping

        for scenario in scenarios:

            scenario.extraction\_questions \= self.generate\_extraction\_questions(scenario)

            scenario.trait\_mapping \= self.generate\_trait\_mapping(scenario)

        

        return ScenarioSet(

            scenarios=scenarios,

            role\_category=role\_category,

            generation\_metadata=self.capture\_metadata()

        )

**Scenario Data Structure**:

class Scenario:

    id: str

    name: str

    role\_category: str

    

    \# Scenario content

    context: str                    \# Situational setup

    trigger: str                    \# Event requiring response

    decision\_point: str             \# What must be done/decided

    

    \# Assessment structure

    primary\_traits: List\[str\]       \# Traits this scenario surfaces

    difficulty: str                 \# ROUTINE | CHALLENGING | CRISIS

    

    \# Extraction framework

    extraction\_questions: List\[ExtractionQuestion\]

    trait\_mapping: List\[TraitMappingRule\]

    

    \# Traceability

    generation\_source: str          \# JOB\_DESCRIPTION | TEMPLATE | CUSTOM

    generation\_timestamp: datetime

    generation\_rationale: str       \# Why this scenario was created

class ExtractionQuestion:

    question\_text: str

    question\_type: str              \# WALK\_THROUGH | FAILURE\_PROBE | NUANCE\_CHECK | etc.

    follow\_up\_triggers: List\[str\]   \# Conditions that trigger follow-ups

    follow\_up\_questions: List\[str\]

class TraitMappingRule:

    response\_pattern: str           \# What to look for in response

    trait\_id: str                   \# Which trait this indicates

    signal\_strength: str            \# HIGH | MEDIUM | LOW

    signal\_direction: str           \# POSITIVE | NEGATIVE

    evidence\_template: str          \# Template for documenting evidence

### 2.4 Module: Training Session Engine

**Purpose**: Conduct expert-framed sessions with top performers to extract trait insights.

**Session Framing**:

PURPOSE: "Building training materials for new hires"

POSITIONING: Top performer as expert contributor

OUTPUT: Both trait profile data AND actual training content

**Session Flow**:

class TrainingSessionEngine:

    def conduct\_session(self,

                       top\_performer: Employee,

                       scenario\_set: ScenarioSet,

                       session\_config: SessionConfig) \-\> SessionResult:

        

        transcript \= \[\]

        trait\_signals \= \[\]

        training\_content \= \[\]

        

        \# Opening: Establish expert positioning

        opening \= self.deliver\_opening(top\_performer, session\_config.framing\_script)

        transcript.append(opening)

        

        \# Warm-up scenario

        warmup\_result \= self.run\_scenario(

            scenario=scenario\_set.get\_warmup(),

            extraction\_depth="FULL"

        )

        transcript.extend(warmup\_result.exchanges)

        trait\_signals.extend(warmup\_result.signals)

        training\_content.extend(warmup\_result.training\_insights)

        

        \# Core scenarios

        for scenario in scenario\_set.core\_scenarios:

            scenario\_result \= self.run\_scenario(

                scenario=scenario,

                extraction\_depth="FULL"

            )

            transcript.extend(scenario\_result.exchanges)

            trait\_signals.extend(scenario\_result.signals)

            training\_content.extend(scenario\_result.training\_insights)

        

        \# Meta-questions

        meta\_result \= self.run\_meta\_questions(session\_config.meta\_questions)

        transcript.extend(meta\_result.exchanges)

        trait\_signals.extend(meta\_result.signals)

        

        return SessionResult(

            participant\_id=top\_performer.id,

            transcript=transcript,

            trait\_signals=trait\_signals,

            training\_content=training\_content,

            session\_metadata=self.capture\_metadata()

        )

    

    def run\_scenario(self, scenario: Scenario, extraction\_depth: str) \-\> ScenarioResult:

        exchanges \= \[\]

        signals \= \[\]

        training\_insights \= \[\]

        

        \# Present scenario

        response \= self.present\_and\_capture(scenario.context \+ scenario.trigger)

        exchanges.append(response)

        

        \# Run extraction questions

        for question in scenario.extraction\_questions:

            q\_response \= self.ask\_and\_capture(question.question\_text)

            exchanges.append(q\_response)

            

            \# Extract trait signals

            for rule in scenario.trait\_mapping:

                if self.matches\_pattern(q\_response, rule.response\_pattern):

                    signals.append(TraitSignal(

                        trait\_id=rule.trait\_id,

                        strength=rule.signal\_strength,

                        direction=rule.signal\_direction,

                        evidence=self.document\_evidence(q\_response, rule),

                        source\_scenario=scenario.id,

                        source\_question=question.question\_text,

                        source\_response=q\_response.text

                    ))

            

            \# Extract training content

            if self.contains\_training\_insight(q\_response):

                training\_insights.append(self.extract\_training\_content(q\_response))

            

            \# Follow-up if triggered

            for trigger in question.follow\_up\_triggers:

                if self.trigger\_matched(q\_response, trigger):

                    follow\_up\_response \= self.ask\_and\_capture(

                        self.select\_follow\_up(question, trigger)

                    )

                    exchanges.append(follow\_up\_response)

        

        return ScenarioResult(

            exchanges=exchanges,

            signals=signals,

            training\_insights=training\_insights

        )

### 2.5 Module: Profile Extractor

**Purpose**: Analyze session results to extract trait profiles with evidence chains.

**Processing Pipeline**:

Session Transcripts → Signal Aggregation → Pattern Analysis → Profile Draft

class ProfileExtractor:

    def extract\_profile(self, 

                       sessions: List\[SessionResult\],

                       role\_category: str) \-\> ExtractedProfile:

        

        \# Aggregate signals across sessions

        all\_signals \= \[\]

        for session in sessions:

            all\_signals.extend(session.trait\_signals)

        

        \# Group by trait

        trait\_groups \= self.group\_by\_trait(all\_signals)

        

        trait\_profiles \= \[\]

        for trait\_id, signals in trait\_groups.items():

            \# Analyze signal patterns

            analysis \= self.analyze\_trait\_signals(signals)

            

            trait\_profile \= TraitProfile(

                trait\_id=trait\_id,

                

                \# Quantitative measures

                emphasis\_score=analysis.mean\_strength,

                consistency\_score=analysis.cross\_session\_consistency,

                frequency=len(signals) / len(sessions),

                

                \# Qualitative patterns

                behavioral\_patterns=analysis.convergent\_patterns,

                distinguishing\_behaviors=analysis.unique\_patterns,

                counter\_indicators=analysis.negative\_patterns,

                

                \# Evidence chain

                evidence\_summary=self.summarize\_evidence(signals),

                source\_sessions=\[s.participant\_id for s in sessions if self.has\_trait\_signal(s, trait\_id)\],

                

                \# Traceability

                derivation\_method="TOP\_PERFORMER\_EXTRACTION",

                sample\_size=len(sessions),

                confidence\_level=self.calculate\_confidence(analysis)

            )

            trait\_profiles.append(trait\_profile)

        

        return ExtractedProfile(

            role\_category=role\_category,

            trait\_profiles=trait\_profiles,

            hidden\_traits=self.identify\_hidden\_traits(sessions),

            training\_content=self.compile\_training\_content(sessions),

            extraction\_metadata=self.capture\_metadata(sessions)

        )

### 2.6 Module: Rubric Synthesizer

**Purpose**: Combine extracted profiles with research-based defaults to create scoring rubrics.

**Synthesis Logic**:

class RubricSynthesizer:

    def synthesize\_rubric(self,

                         extracted\_profile: Optional\[ExtractedProfile\],

                         research\_defaults: ResearchDefaults,

                         organization\_adjustments: Optional\[Dict\]) \-\> ScoringRubric:

        

        rubric\_items \= \[\]

        

        for trait\_id in self.get\_all\_traits():

            \# Determine base rubric source

            if extracted\_profile and trait\_id in extracted\_profile.traits:

                \# Use organization-specific profile

                base \= self.create\_rubric\_from\_extraction(

                    extracted\_profile.get\_trait(trait\_id)

                )

                source \= RubricSource.ORGANIZATIONAL\_EXTRACTION

            else:

                \# Use research defaults

                base \= research\_defaults.get\_rubric(trait\_id)

                source \= RubricSource.RESEARCH\_DEFAULT

            

            \# Apply organization adjustments if any

            if organization\_adjustments and trait\_id in organization\_adjustments:

                adjusted \= self.apply\_adjustments(base, organization\_adjustments\[trait\_id\])

                source \= RubricSource.ADJUSTED\_DEFAULT if source \== RubricSource.RESEARCH\_DEFAULT else RubricSource.ADJUSTED\_EXTRACTION

            else:

                adjusted \= base

            

            rubric\_item \= RubricItem(

                trait\_id=trait\_id,

                

                \# Scoring criteria

                scoring\_criteria=adjusted.scoring\_criteria,

                behavioral\_anchors=adjusted.behavioral\_anchors,

                evidence\_requirements=adjusted.evidence\_requirements,

                

                \# Weights

                importance\_weight=adjusted.importance\_weight,

                minimum\_threshold=adjusted.minimum\_threshold,

                

                \# Probes

                primary\_probes=adjusted.primary\_probes,

                follow\_up\_probes=adjusted.follow\_up\_probes,

                

                \# Traceability

                source=source,

                derivation\_chain=self.build\_derivation\_chain(base, adjusted, source),

                version=self.generate\_version()

            )

            rubric\_items.append(rubric\_item)

        

        return ScoringRubric(

            rubric\_id=self.generate\_id(),

            role\_category=extracted\_profile.role\_category if extracted\_profile else "GENERIC",

            organization\_id=self.get\_org\_id(),

            items=rubric\_items,

            creation\_timestamp=datetime.utcnow(),

            derivation\_summary=self.summarize\_derivation(rubric\_items)

        )

---

## 3\. Research-Based Default Rubrics

### 3.1 Purpose

Provide scientifically-grounded default rubrics for organizations that haven't yet conducted top performer profiling, or as a baseline for comparison.

### 3.2 Research Foundation

Each default rubric is grounded in established psychological research:

| Trait | Research Foundation | Key Sources |
| :---- | :---- | :---- |
| **Curiosity** | Epistemic curiosity predicts learning & adaptation; Curiosity and Exploration Inventory (CEI-II) | Kashdan et al. (2009); Litman (2008) |
| **Adaptability** | Cognitive flexibility correlates with performance under change; Career Adapt-Abilities Scale | Savickas & Porfeli (2012); Martin et al. (2012) |
| **Communication** | Communication competence theory; encoding/decoding accuracy | Spitzberg & Cupach (1984); McCroskey (1982) |
| **Collaboration** | Team effectiveness research; psychological safety | Edmondson (1999); Salas et al. (2005) |
| **Initiative** | Proactive personality and personal initiative research | Frese & Fay (2001); Bateman & Crant (1993) |
| **Resilience** | Psychological resilience factors; post-traumatic growth | Connor & Davidson (2003); Bonanno (2004) |

### 3.3 Default Rubric Structure

class ResearchDefaultRubric:

    trait\_id: str

    trait\_name: str

    definition: str

    

    \# Research basis

    research\_foundation: ResearchFoundation

    measurement\_instruments: List\[str\]        \# Validated scales this draws from

    key\_citations: List\[Citation\]

    

    \# Scoring criteria (5-point scale)

    scoring\_criteria: Dict\[int, ScoringLevel\]

    

    \# Behavioral anchors

    behavioral\_anchors: Dict\[int, List\[str\]\]  \# Score \-\> Observable behaviors

    

    \# Evidence requirements

    evidence\_requirements: EvidenceRequirements

    

    \# Probes

    primary\_probes: List\[Probe\]

    follow\_up\_probes: Dict\[str, List\[Probe\]\]  \# Trigger \-\> Follow-ups

    

    \# Adjustable parameters

    adjustable\_parameters: List\[AdjustableParameter\]

class ScoringLevel:

    score: int

    label: str

    description: str

    minimum\_evidence: str

    distinguishing\_features: List\[str\]

class AdjustableParameter:

    parameter\_id: str

    parameter\_name: str

    current\_value: Any

    allowed\_range: Tuple\[Any, Any\]

    adjustment\_rationale\_required: bool

### 3.4 Default Rubric: CURIOSITY

CURIOSITY\_DEFAULT\_RUBRIC \= ResearchDefaultRubric(

    trait\_id="CURIOSITY",

    trait\_name="Curiosity",

    definition="The intrinsic drive to explore, understand, and learn beyond immediate requirements",

    

    research\_foundation=ResearchFoundation(

        theoretical\_basis="Epistemic curiosity theory distinguishes between diversive curiosity (seeking novelty) and specific curiosity (seeking to resolve knowledge gaps). Both predict learning outcomes and adaptability.",

        measurement\_instruments=\["Curiosity and Exploration Inventory-II (CEI-II)", "Epistemic Curiosity Scale"\],

        key\_findings=\[

            "Curiosity predicts academic performance beyond IQ (von Stumm et al., 2011)",

            "Curious individuals show greater learning from feedback (Mussel, 2013)",

            "Trait curiosity predicts job performance in complex roles (Reio & Wiswell, 2000)"

        \]

    ),

    

    key\_citations=\[

        Citation(authors="Kashdan, T.B., et al.", year=2009, title="The Curiosity and Exploration Inventory-II", journal="Journal of Research in Personality"),

        Citation(authors="Litman, J.A.", year=2008, title="Interest and deprivation factors of epistemic curiosity", journal="Personality and Individual Differences"),

        Citation(authors="von Stumm, S., et al.", year=2011, title="The hungry mind: Intellectual curiosity is the third pillar of academic performance", journal="Perspectives on Psychological Science")

    \],

    

    scoring\_criteria={

        5: ScoringLevel(

            score=5,

            label="Exceptional",

            description="Demonstrates active, self-directed learning across multiple domains; consistently seeks to understand root causes; questions assumptions; shows evidence of changing views based on new information",

            minimum\_evidence="3+ examples of voluntary learning; demonstrated in-interview curiosity; evidence of perspective change",

            distinguishing\_features=\["Cross-domain exploration", "Proactive knowledge seeking", "Intellectual humility"\]

        ),

        4: ScoringLevel(

            score=4,

            label="Strong",

            description="Shows consistent curiosity within professional domain; asks good clarifying questions; can cite recent learning; seeks to understand 'why' not just 'what'",

            minimum\_evidence="2+ examples of learning; questions asked during interview; recent knowledge acquisition",

            distinguishing\_features=\["Domain-focused exploration", "Question-asking habit", "Learning from feedback"\]

        ),

        3: ScoringLevel(

            score=3,

            label="Adequate",

            description="Average curiosity; learns when prompted or required; asks clarifying questions but not exploratory ones; may not seek information beyond immediate needs",

            minimum\_evidence="1 example of learning; some questions during interview",

            distinguishing\_features=\["Reactive learning", "Task-focused questions"\]

        ),

        2: ScoringLevel(

            score=2,

            label="Limited",

            description="Limited evidence of curiosity; learning is primarily reactive and requirement-driven; few questions asked; accepts information at face value",

            minimum\_evidence="Weak or absent examples of learning; minimal questions",

            distinguishing\_features=\["Passive information consumption", "Minimal inquiry"\]

        ),

        1: ScoringLevel(

            score=1,

            label="Absent",

            description="No evidence of curiosity; purely reactive stance toward information; dismisses unfamiliar topics; no questions for interviewer",

            minimum\_evidence="No examples despite probing; no questions; resistance to new information",

            distinguishing\_features=\["Information avoidance", "Closed mindset"\]

        )

    },

    

    behavioral\_anchors={

        5: \[

            "Provides multiple examples of self-directed learning without prompting",

            "Asks probing questions during interview that reveal genuine interest",

            "Describes changing a strongly-held view based on new evidence",

            "Connects ideas across different domains",

            "Admits knowledge gaps eagerly and describes how they'd fill them"

        \],

        4: \[

            "Provides clear examples of learning within professional domain",

            "Asks clarifying and some exploratory questions",

            "Describes recent learning experience with enthusiasm",

            "Shows interest in understanding underlying mechanisms"

        \],

        3: \[

            "Provides example(s) of learning when directly asked",

            "Asks basic clarifying questions",

            "Learning examples tied primarily to job requirements"

        \],

        2: \[

            "Struggles to provide learning examples",

            "Few or no questions during interview",

            "Learning described only in response to external requirements"

        \],

        1: \[

            "Cannot provide learning examples",

            "No questions for interviewer",

            "Dismissive of topics outside immediate expertise"

        \]

    },

    

    evidence\_requirements=EvidenceRequirements(

        minimum\_behavioral\_examples=1,

        preferred\_behavioral\_examples=2,

        in\_interview\_observation\_weight=0.3,

        self\_report\_discount=0.5,

        recency\_bonus\_months=6

    ),

    

    primary\_probes=\[

        Probe(

            text="What's something you changed your mind about recently?",

            purpose="Assess intellectual flexibility and evidence-responsiveness",

            trait\_signal\_map={

                "multiple\_examples": ("HIGH", "POSITIVE"),

                "describes\_evidence": ("HIGH", "POSITIVE"),

                "struggles\_to\_answer": ("MEDIUM", "NEGATIVE"),

                "external\_pressure\_only": ("LOW", "NEGATIVE")

            }

        ),

        Probe(

            text="Walk me through how you approach something you don't understand.",

            purpose="Assess learning process and information-seeking behavior",

            trait\_signal\_map={

                "systematic\_approach": ("HIGH", "POSITIVE"),

                "multiple\_sources": ("MEDIUM", "POSITIVE"),

                "asks\_experts": ("MEDIUM", "POSITIVE"),

                "avoids\_or\_delays": ("HIGH", "NEGATIVE")

            }

        ),

        Probe(

            text="What have you learned recently that wasn't required for work?",

            purpose="Assess intrinsic vs. extrinsic learning motivation",

            trait\_signal\_map={

                "enthusiastic\_examples": ("HIGH", "POSITIVE"),

                "multiple\_areas": ("HIGH", "POSITIVE"),

                "nothing\_comes\_to\_mind": ("HIGH", "NEGATIVE"),

                "only\_job\_related": ("MEDIUM", "NEGATIVE")

            }

        )

    \],

    

    adjustable\_parameters=\[

        AdjustableParameter(

            parameter\_id="domain\_specificity",

            parameter\_name="Domain Specificity",

            description="Weight given to within-domain vs. cross-domain curiosity",

            current\_value=0.5,

            allowed\_range=(0.0, 1.0),

            adjustment\_rationale\_required=True

        ),

        AdjustableParameter(

            parameter\_id="in\_interview\_weight",

            parameter\_name="In-Interview Observation Weight",

            description="Weight given to curiosity demonstrated during interview vs. reported",

            current\_value=0.3,

            allowed\_range=(0.1, 0.5),

            adjustment\_rationale\_required=False

        ),

        AdjustableParameter(

            parameter\_id="minimum\_threshold",

            parameter\_name="Minimum Acceptable Score",

            description="Minimum score to pass screening for this trait",

            current\_value=3,

            allowed\_range=(1, 5),

            adjustment\_rationale\_required=True

        )

    \]

)

### 3.5 Default Rubric: ADAPTABILITY

ADAPTABILITY\_DEFAULT\_RUBRIC \= ResearchDefaultRubric(

    trait\_id="ADAPTABILITY",

    trait\_name="Adaptability",

    definition="The capacity to adjust approach, behavior, or strategy when circumstances change or initial approaches fail",

    

    research\_foundation=ResearchFoundation(

        theoretical\_basis="Career adaptability comprises four dimensions: concern (planning), control (decision-making), curiosity (exploration), and confidence (self-efficacy). Cognitive flexibility predicts performance in dynamic environments.",

        measurement\_instruments=\["Career Adapt-Abilities Scale (CAAS)", "Cognitive Flexibility Inventory"\],

        key\_findings=\[

            "Adaptability predicts career success beyond personality traits (Savickas & Porfeli, 2012)",

            "Cognitive flexibility correlates with creative problem-solving (Martin & Rubin, 1995)",

            "Adaptive performance is distinct from task performance (Pulakos et al., 2000)"

        \]

    ),

    

    key\_citations=\[

        Citation(authors="Savickas, M.L. & Porfeli, E.J.", year=2012, title="Career Adapt-Abilities Scale", journal="Journal of Vocational Behavior"),

        Citation(authors="Martin, A.J., et al.", year=2012, title="Adaptability: Conceptual and empirical perspectives", journal="Journal of Psychoeducational Assessment"),

        Citation(authors="Pulakos, E.D., et al.", year=2000, title="Adaptability in the workplace", journal="Journal of Applied Psychology")

    \],

    

    scoring\_criteria={

        5: ScoringLevel(

            score=5,

            label="Exceptional",

            description="Multiple clear examples of rapid, effective pivots; treats change as opportunity; demonstrates real-time adaptability in interview; proactively anticipates need for change",

            minimum\_evidence="3+ pivot examples with clear outcomes; demonstrated flexibility in interview",

            distinguishing\_features=\["Proactive adaptation", "Rapid pivot execution", "Change as opportunity framing"\]

        ),

        4: ScoringLevel(

            score=4,

            label="Strong",

            description="Good examples of adaptation; reasonable pivot speed; comfortable with ambiguity; adjusts approach based on feedback",

            minimum\_evidence="2+ adaptation examples; comfort with ambiguity evident",

            distinguishing\_features=\["Responsive adaptation", "Feedback incorporation", "Ambiguity tolerance"\]

        ),

        3: ScoringLevel(

            score=3,

            label="Adequate",

            description="Can adapt when clearly required; prefers stability but manages change; pivots with support or clear necessity",

            minimum\_evidence="1+ adaptation example; eventual adjustment to change",

            distinguishing\_features=\["Reactive adaptation", "Supported change management"\]

        ),

        2: ScoringLevel(

            score=2,

            label="Limited",

            description="Slow to adapt; requires significant evidence or external pressure before changing approach; uncomfortable with ambiguity",

            minimum\_evidence="Weak examples; resistance to hypotheticals",

            distinguishing\_features=\["Resistance to change", "Delayed adaptation"\]

        ),

        1: ScoringLevel(

            score=1,

            label="Rigid",

            description="Rigid approach; resists change even with clear evidence; failures attributed externally; no evidence of adaptation",

            minimum\_evidence="No adaptation examples; external attribution; rigidity in interview",

            distinguishing\_features=\["Change resistance", "External blame", "Fixed approach"\]

        )

    },

    

    behavioral\_anchors={

        5: \[

            "Describes proactively identifying need to change before forced",

            "Multiple examples of rapid course correction with positive outcomes",

            "Demonstrates flexibility in interview (adjusts communication style, explores alternatives)",

            "Frames past changes as learning opportunities",

            "Comfortable with hypothetical scenarios requiring adaptation"

        \],

        4: \[

            "Clear examples of adapting approach based on new information",

            "Describes feedback incorporation process",

            "Shows comfort discussing ambiguous situations",

            "Reasonable speed of recognition and response to change needs"

        \],

        3: \[

            "Provides adaptation example when directly asked",

            "Adapted when change was clearly necessary",

            "May express preference for stability while acknowledging change is sometimes needed"

        \],

        2: \[

            "Struggles to provide adaptation examples",

            "Describes resistance to change or slow adaptation",

            "Uncomfortable with hypothetical change scenarios"

        \],

        1: \[

            "No adaptation examples available",

            "Attributes failures to external factors",

            "Resists engaging with hypothetical change scenarios",

            "Fixed mindset evident"

        \]

    },

    

    evidence\_requirements=EvidenceRequirements(

        minimum\_behavioral\_examples=1,

        preferred\_behavioral\_examples=2,

        in\_interview\_observation\_weight=0.25,

        self\_report\_discount=0.5,

        recency\_bonus\_months=12

    ),

    

    primary\_probes=\[

        Probe(

            text="Tell me about a time your approach wasn't working. What happened?",

            purpose="Assess recognition speed, pivot quality, and outcome",

            trait\_signal\_map={

                "quick\_recognition": ("HIGH", "POSITIVE"),

                "clear\_pivot\_description": ("HIGH", "POSITIVE"),

                "positive\_outcome\_from\_change": ("MEDIUM", "POSITIVE"),

                "external\_attribution": ("HIGH", "NEGATIVE"),

                "no\_example": ("HIGH", "NEGATIVE")

            }

        ),

        Probe(

            text="How do you know when to pivot vs. persist?",

            purpose="Assess metacognitive awareness of adaptation process",

            trait\_signal\_map={

                "clear\_decision\_framework": ("HIGH", "POSITIVE"),

                "balances\_persistence\_and\_flexibility": ("HIGH", "POSITIVE"),

                "always\_persist\_or\_always\_pivot": ("MEDIUM", "NEGATIVE")

            }

        ),

        Probe(

            text="If you joined and discovered everything you assumed was wrong, what would you do?",

            purpose="Assess hypothetical adaptability and comfort with uncertainty",

            trait\_signal\_map={

                "engages\_thoughtfully": ("HIGH", "POSITIVE"),

                "describes\_learning\_process": ("MEDIUM", "POSITIVE"),

                "resists\_hypothetical": ("HIGH", "NEGATIVE"),

                "defensive\_response": ("HIGH", "NEGATIVE")

            }

        )

    \],

    

    adjustable\_parameters=\[

        AdjustableParameter(

            parameter\_id="pivot\_speed\_weight",

            parameter\_name="Pivot Speed Weight",

            description="Importance of rapid adaptation vs. thoughtful adaptation",

            current\_value=0.4,

            allowed\_range=(0.2, 0.8),

            adjustment\_rationale\_required=True

        ),

        AdjustableParameter(

            parameter\_id="proactive\_vs\_reactive",

            parameter\_name="Proactive vs. Reactive Weight",

            description="Weight for anticipatory change vs. responsive change",

            current\_value=0.5,

            allowed\_range=(0.0, 1.0),

            adjustment\_rationale\_required=True

        ),

        AdjustableParameter(

            parameter\_id="minimum\_threshold",

            parameter\_name="Minimum Acceptable Score",

            current\_value=3,

            allowed\_range=(1, 5),

            adjustment\_rationale\_required=True

        )

    \]

)

### 3.6 Additional Default Rubrics (Summary)

\# COMMUNICATION Default Rubric

COMMUNICATION\_DEFAULT\_RUBRIC \= ResearchDefaultRubric(

    trait\_id="COMMUNICATION",

    trait\_name="Communication",

    definition="The ability to convey information clearly, calibrate to audience, and listen effectively",

    research\_foundation=ResearchFoundation(

        theoretical\_basis="Communication competence theory emphasizes both encoding (message creation) and decoding (message reception) skills, along with adaptability across contexts.",

        measurement\_instruments=\["Communicative Adaptability Scale", "Listening Styles Profile"\],

        key\_findings=\[

            "Communication competence predicts job performance across roles (Payne, 2005)",

            "Audience adaptation is central to effective communication (Duran, 1992)",

            "Active listening correlates with relationship quality and problem-solving (Weger et al., 2014)"

        \]

    ),

    \# ... \[full rubric structure as above\]

)

\# COLLABORATION Default Rubric  

COLLABORATION\_DEFAULT\_RUBRIC \= ResearchDefaultRubric(

    trait\_id="COLLABORATION",

    trait\_name="Collaboration",

    definition="The ability to work effectively with others toward shared goals",

    research\_foundation=ResearchFoundation(

        theoretical\_basis="Team effectiveness research identifies key collaboration competencies including coordination, cooperation, and communication. Psychological safety enables productive collaboration.",

        measurement\_instruments=\["Team Diagnostic Survey", "Teamwork Quality Scale"\],

        key\_findings=\[

            "Psychological safety predicts team learning and performance (Edmondson, 1999)",

            "Shared mental models improve coordination (Mathieu et al., 2000)",

            "Conflict management style affects team outcomes (DeChurch & Marks, 2001)"

        \]

    ),

    \# ... \[full rubric structure\]

)

\# INITIATIVE Default Rubric

INITIATIVE\_DEFAULT\_RUBRIC \= ResearchDefaultRubric(

    trait\_id="INITIATIVE",

    trait\_name="Initiative",

    definition="The tendency to act proactively without being directed",

    research\_foundation=ResearchFoundation(

        theoretical\_basis="Personal initiative theory emphasizes self-starting behavior, proactivity, and persistence. Proactive personality predicts career success and job performance.",

        measurement\_instruments=\["Personal Initiative Scale", "Proactive Personality Scale"\],

        key\_findings=\[

            "Proactive personality predicts job performance and career success (Crant, 1995)",

            "Personal initiative is trainable (Frese et al., 1996)",

            "Initiative interacts with organizational support (Morrison & Phelps, 1999)"

        \]

    ),

    \# ... \[full rubric structure\]

)

\# RESILIENCE Default Rubric

RESILIENCE\_DEFAULT\_RUBRIC \= ResearchDefaultRubric(

    trait\_id="RESILIENCE",

    trait\_name="Resilience",

    definition="The capacity to recover from setbacks and maintain effectiveness under pressure",

    research\_foundation=ResearchFoundation(

        theoretical\_basis="Psychological resilience involves adaptive coping, emotion regulation, and meaning-making. It is both a trait and a process that can be developed.",

        measurement\_instruments=\["Connor-Davidson Resilience Scale (CD-RISC)", "Brief Resilience Scale"\],

        key\_findings=\[

            "Resilience predicts post-adversity functioning (Bonanno, 2004)",

            "Resilience is modifiable through intervention (Leppin et al., 2014)",

            "Resilience buffers stress-performance relationship (Robertson et al., 2015)"

        \]

    ),

    \# ... \[full rubric structure\]

)

### 3.7 Default Rubric Registry

class ResearchDefaultRegistry:

    """Registry of all research-based default rubrics."""

    

    rubrics: Dict\[str, ResearchDefaultRubric\] \= {

        "CURIOSITY": CURIOSITY\_DEFAULT\_RUBRIC,

        "ADAPTABILITY": ADAPTABILITY\_DEFAULT\_RUBRIC,

        "COMMUNICATION": COMMUNICATION\_DEFAULT\_RUBRIC,

        "COLLABORATION": COLLABORATION\_DEFAULT\_RUBRIC,

        "INITIATIVE": INITIATIVE\_DEFAULT\_RUBRIC,

        "RESILIENCE": RESILIENCE\_DEFAULT\_RUBRIC

    }

    

    def get\_rubric(self, trait\_id: str) \-\> ResearchDefaultRubric:

        return self.rubrics\[trait\_id\]

    

    def get\_all\_rubrics(self) \-\> List\[ResearchDefaultRubric\]:

        return list(self.rubrics.values())

    

    def get\_adjustable\_parameters(self, trait\_id: str) \-\> List\[AdjustableParameter\]:

        return self.rubrics\[trait\_id\].adjustable\_parameters

    

    def create\_adjusted\_rubric(self, 

                               trait\_id: str, 

                               adjustments: Dict\[str, Any\],

                               adjustment\_rationales: Dict\[str, str\]) \-\> ResearchDefaultRubric:

        """Create a copy of rubric with adjusted parameters."""

        base \= self.rubrics\[trait\_id\]

        adjusted \= copy.deepcopy(base)

        

        for param\_id, new\_value in adjustments.items():

            param \= next(p for p in adjusted.adjustable\_parameters if p.parameter\_id \== param\_id)

            

            \# Validate range

            if not (param.allowed\_range\[0\] \<= new\_value \<= param.allowed\_range\[1\]):

                raise ValueError(f"Adjustment {new\_value} outside allowed range {param.allowed\_range}")

            

            \# Require rationale if specified

            if param.adjustment\_rationale\_required and param\_id not in adjustment\_rationales:

                raise ValueError(f"Rationale required for adjusting {param.parameter\_name}")

            

            param.current\_value \= new\_value

            param.adjustment\_rationale \= adjustment\_rationales.get(param\_id)

        

        return adjusted

---

## 4\. Candidate Assessment Subsystem

### 4.1 Data Flow

┌──────────────┐  ┌──────────────┐  ┌──────────────┐

│     Job      │  │  Candidate   │  │   Scoring    │

│ Description  │  │   Resumes    │  │   Rubric     │

└──────┬───────┘  └──────┬───────┘  └──────┬───────┘

       │                 │                 │

       ▼                 ▼                 │

┌─────────────────────────────┐            │

│       Resume Analyzer       │            │

│  (Requirement Extraction    │            │

│   & Matching)               │            │

└──────────────┬──────────────┘            │

               │                           │

               ▼                           │

┌─────────────────────────────┐            │

│       Stack Ranker /        │            │

│       Clusterer             │            │

│  (Objective Qualification   │            │

│   Ranking)                  │            │

└──────────────┬──────────────┘            │

               │                           │

               ▼                           │

       \[Qualified Candidates\]              │

               │                           │

               └───────────────────────────┼───────┐

                                           │       │

                                           ▼       ▼

                              ┌─────────────────────────────┐

                              │      Interview Engine       │

                              │   (STAR+ Methodology with   │

                              │    Rubric-Based Scoring)    │

                              └──────────────┬──────────────┘

                                             │

                                             ▼

                              ┌─────────────────────────────┐

                              │      Score Calibrator       │

                              │   (Evidence Weighting &     │

                              │    Explanation Generation)  │

                              └──────────────┬──────────────┘

                                             │

                                             ▼

                              ┌─────────────────────────────┐

                              │    Assessment Report        │

                              │  (Scores \+ Evidence \+       │

                              │   Explanations \+ Trace)     │

                              └─────────────────────────────┘

### 4.2 Module: Resume Analyzer

**Purpose**: Extract job requirements and match against candidate resumes objectively.

class ResumeAnalyzer:

    def analyze(self, 

               job\_description: str, 

               resumes: List\[Resume\]) \-\> List\[ResumeAnalysisResult\]:

        

        \# Extract requirements from JD

        requirements \= self.extract\_requirements(job\_description)

        

        results \= \[\]

        for resume in resumes:

            \# Match each requirement

            matches \= \[\]

            for req in requirements:

                match \= RequirementMatch(

                    requirement=req,

                    status=self.evaluate\_match(req, resume),

                    evidence=self.extract\_evidence(req, resume),

                    confidence=self.calculate\_confidence(req, resume)

                )

                matches.append(match)

            

            \# Calculate scores

            result \= ResumeAnalysisResult(

                candidate\_id=resume.candidate\_id,

                hard\_requirement\_score=self.score\_hard\_requirements(matches),

                soft\_requirement\_score=self.score\_soft\_requirements(matches),

                matches=matches,

                pass\_threshold\_met=self.check\_threshold(matches),

                analysis\_trace=self.generate\_trace(matches)

            )

            results.append(result)

        

        return results

class RequirementMatch:

    requirement: Requirement

    status: str                     \# MET | NOT\_MET | PARTIAL | UNCLEAR

    evidence: List\[EvidenceItem\]    \# Specific resume content supporting match

    confidence: float               \# 0.0 \- 1.0

    explanation: str                \# Human-readable explanation

### 4.3 Module: Stack Ranker / Clusterer

**Purpose**: Rank and cluster candidates who meet objective requirements.

class StackRanker:

    def rank\_and\_cluster(self,

                        analysis\_results: List\[ResumeAnalysisResult\],

                        ranking\_config: RankingConfig) \-\> RankedCandidateSet:

        

        \# Filter to passing candidates

        passing \= \[r for r in analysis\_results if r.pass\_threshold\_met\]

        

        \# Calculate composite scores

        scored \= \[\]

        for result in passing:

            composite \= self.calculate\_composite\_score(result, ranking\_config)

            scored.append(ScoredCandidate(

                candidate\_id=result.candidate\_id,

                composite\_score=composite.score,

                score\_components=composite.components,

                score\_explanation=composite.explanation

            ))

        

        \# Rank by composite score

        ranked \= sorted(scored, key=lambda x: x.composite\_score, reverse=True)

        

        \# Cluster into tiers

        clusters \= self.cluster\_into\_tiers(ranked, ranking\_config.tier\_config)

        

        return RankedCandidateSet(

            ranked\_candidates=ranked,

            clusters=clusters,

            ranking\_methodology=self.document\_methodology(ranking\_config),

            trace=self.generate\_trace(ranked, clusters)

        )

    

    def cluster\_into\_tiers(self, 

                          ranked: List\[ScoredCandidate\],

                          tier\_config: TierConfig) \-\> Dict\[str, List\[ScoredCandidate\]\]:

        """

        Cluster candidates into tiers based on score distribution.

        

        Tiers:

        \- TIER\_1: Top candidates (interview first)

        \- TIER\_2: Strong candidates (interview if capacity)

        \- TIER\_3: Qualified candidates (interview if needed)

        """

        if not ranked:

            return {"TIER\_1": \[\], "TIER\_2": \[\], "TIER\_3": \[\]}

        

        \# Use natural breaks in score distribution

        scores \= \[c.composite\_score for c in ranked\]

        breaks \= self.find\_natural\_breaks(scores, n\_clusters=3)

        

        tiers \= {"TIER\_1": \[\], "TIER\_2": \[\], "TIER\_3": \[\]}

        for candidate in ranked:

            if candidate.composite\_score \>= breaks\[0\]:

                tiers\["TIER\_1"\].append(candidate)

            elif candidate.composite\_score \>= breaks\[1\]:

                tiers\["TIER\_2"\].append(candidate)

            else:

                tiers\["TIER\_3"\].append(candidate)

        

        return tiers

### 4.4 Module: Interview Engine

**Purpose**: Conduct structured behavioral interviews using STAR+ methodology with rubric-based scoring.

class InterviewEngine:

    def conduct\_interview(self,

                         candidate: Candidate,

                         rubric: ScoringRubric,

                         interview\_config: InterviewConfig) \-\> InterviewSession:

        

        session \= InterviewSession(

            session\_id=self.generate\_session\_id(),

            candidate\_id=candidate.id,

            rubric\_id=rubric.rubric\_id,

            rubric\_version=rubric.version,

            start\_time=datetime.utcnow()

        )

        

        \# Introduction phase

        session.add\_exchange(self.deliver\_introduction(interview\_config))

        

        \# Trait assessment loop

        trait\_order \= self.prioritize\_traits(rubric)

        

        for trait\_id in trait\_order:

            rubric\_item \= rubric.get\_item(trait\_id)

            

            \# Run STAR+ sequence for this trait

            trait\_assessment \= self.assess\_trait(

                trait\_id=trait\_id,

                rubric\_item=rubric\_item,

                session=session

            )

            session.add\_trait\_assessment(trait\_assessment)

        

        \# Candidate questions (curiosity signal)

        candidate\_q\_result \= self.handle\_candidate\_questions(session)

        session.add\_exchange(candidate\_q\_result)

        

        \# Closing

        session.add\_exchange(self.deliver\_closing())

        session.end\_time \= datetime.utcnow()

        

        return session

    

    def assess\_trait(self,

                    trait\_id: str,

                    rubric\_item: RubricItem,

                    session: InterviewSession) \-\> TraitAssessment:

        

        exchanges \= \[\]

        evidence\_items \= \[\]

        

        \# Primary probe

        primary\_probe \= self.select\_primary\_probe(rubric\_item, session)

        response \= self.ask\_and\_capture(primary\_probe.text)

        exchanges.append(Exchange(

            speaker="SYSTEM",

            content=primary\_probe.text,

            exchange\_type="PROBE",

            probe\_id=primary\_probe.id

        ))

        exchanges.append(Exchange(

            speaker="CANDIDATE",

            content=response.text,

            exchange\_type="RESPONSE"

        ))

        

        \# Extract evidence from response

        evidence \= self.extract\_evidence(response, rubric\_item)

        evidence\_items.extend(evidence)

        

        \# STAR+ follow-ups

        star\_complete \= self.check\_star\_completeness(response)

        if not star\_complete.situation:

            follow\_up \= self.ask\_and\_capture("Can you set the scene? What was the specific situation?")

            exchanges.extend(self.create\_exchange\_pair("SITUATION\_CLARIFICATION", follow\_up))

            evidence\_items.extend(self.extract\_evidence(follow\_up, rubric\_item))

        

        if not star\_complete.action\_specific:

            follow\_up \= self.ask\_and\_capture("What did YOU specifically do? Not the team—you personally.")

            exchanges.extend(self.create\_exchange\_pair("ACTION\_CLARIFICATION", follow\_up))

            evidence\_items.extend(self.extract\_evidence(follow\_up, rubric\_item))

        

        if not star\_complete.result:

            follow\_up \= self.ask\_and\_capture("What was the outcome?")

            exchanges.extend(self.create\_exchange\_pair("RESULT\_CLARIFICATION", follow\_up))

            evidence\_items.extend(self.extract\_evidence(follow\_up, rubric\_item))

        

        \# Reflection (+R)

        reflection \= self.ask\_and\_capture("Looking back, what would you do differently?")

        exchanges.extend(self.create\_exchange\_pair("REFLECTION", reflection))

        evidence\_items.extend(self.extract\_evidence(reflection, rubric\_item))

        

        \# Recursion if needed (+R)

        confidence \= self.assess\_evidence\_confidence(evidence\_items)

        if confidence \< 0.6:

            recursion \= self.ask\_and\_capture(f"Can you tell me about another time you demonstrated {trait\_id.lower()}?")

            exchanges.extend(self.create\_exchange\_pair("RECURSION", recursion))

            evidence\_items.extend(self.extract\_evidence(recursion, rubric\_item))

        

        \# Score with evidence

        score\_result \= self.score\_trait(

            trait\_id=trait\_id,

            rubric\_item=rubric\_item,

            evidence\_items=evidence\_items

        )

        

        return TraitAssessment(

            trait\_id=trait\_id,

            exchanges=exchanges,

            evidence\_items=evidence\_items,

            score=score\_result.score,

            confidence=score\_result.confidence,

            explanation=score\_result.explanation,

            rubric\_item\_version=rubric\_item.version

        )

### 4.5 Module: Score Calibrator

**Purpose**: Generate final scores with full evidence chains and human-readable explanations.

class ScoreCalibrator:

    def calibrate\_and\_explain(self,

                             session: InterviewSession,

                             rubric: ScoringRubric) \-\> CalibratedAssessment:

        

        calibrated\_scores \= \[\]

        

        for trait\_assessment in session.trait\_assessments:

            rubric\_item \= rubric.get\_item(trait\_assessment.trait\_id)

            

            \# Apply evidence weighting

            weighted\_evidence \= self.weight\_evidence(

                evidence\_items=trait\_assessment.evidence\_items,

                evidence\_requirements=rubric\_item.evidence\_requirements

            )

            

            \# Calculate calibrated score

            raw\_score \= trait\_assessment.score

            calibrated\_score \= self.apply\_calibration(

                raw\_score=raw\_score,

                weighted\_evidence=weighted\_evidence,

                rubric\_item=rubric\_item

            )

            

            \# Generate explanation

            explanation \= self.generate\_explanation(

                trait\_id=trait\_assessment.trait\_id,

                score=calibrated\_score,

                evidence=weighted\_evidence,

                rubric\_item=rubric\_item

            )

            

            calibrated\_scores.append(CalibratedTraitScore(

                trait\_id=trait\_assessment.trait\_id,

                raw\_score=raw\_score,

                calibrated\_score=calibrated\_score,

                confidence=self.calculate\_confidence(weighted\_evidence),

                

                \# Evidence chain

                evidence\_summary=self.summarize\_evidence(weighted\_evidence),

                evidence\_items=weighted\_evidence,

                

                \# Explanation

                explanation=explanation,

                score\_rationale=self.generate\_rationale(calibrated\_score, rubric\_item),

                

                \# Traceability

                rubric\_item\_id=rubric\_item.id,

                rubric\_source=rubric\_item.source,

                scoring\_algorithm\_version=self.ALGORITHM\_VERSION

            ))

        

        \# Generate composite assessment

        composite \= self.calculate\_composite(calibrated\_scores, rubric)

        

        \# Generate overall recommendation

        recommendation \= self.generate\_recommendation(composite, rubric)

        

        return CalibratedAssessment(

            session\_id=session.session\_id,

            candidate\_id=session.candidate\_id,

            trait\_scores=calibrated\_scores,

            composite\_score=composite,

            recommendation=recommendation,

            assessment\_trace=self.generate\_full\_trace(session, calibrated\_scores)

        )

    

    def generate\_explanation(self,

                            trait\_id: str,

                            score: int,

                            evidence: List\[WeightedEvidence\],

                            rubric\_item: RubricItem) \-\> str:

        """

        Generate human-readable explanation for a trait score.

        

        Example output:

        "CURIOSITY: Score 4 (Strong)

        

        The candidate demonstrated strong curiosity through two clear behavioral examples.

        

        Supporting Evidence:

        1\. \[BEHAVIORAL, Weight: HIGH\] Described independently learning Kubernetes to solve 

           a deployment problem, spending personal time to gain certification.

        2\. \[BEHAVIORAL, Weight: MEDIUM\] Asked three probing questions during the interview 

           about the team's technical challenges and learning culture.

        

        The candidate meets the behavioral anchor criteria for Score 4: 'Clear examples of 

        learning within professional domain' and 'Shows interest in understanding underlying 

        mechanisms.'

        

        Score could have been higher (5) with evidence of cross-domain learning or 

        perspective change based on new evidence."

        """

        

        \# Get scoring level description

        level \= rubric\_item.scoring\_criteria\[score\]

        

        \# Build evidence summary

        evidence\_lines \= \[\]

        for i, ev in enumerate(evidence, 1):

            evidence\_lines.append(

                f"{i}. \[{ev.evidence\_type}, Weight: {ev.weight}\] {ev.summary}"

            )

        

        \# Identify matched behavioral anchors

        matched\_anchors \= self.identify\_matched\_anchors(evidence, rubric\_item, score)

        

        \# Identify what would raise/lower score

        improvement\_note \= self.generate\_improvement\_note(score, evidence, rubric\_item)

        

        explanation \= f"""{trait\_id}: Score {score} ({level.label})

The candidate demonstrated {level.label.lower()} {trait\_id.lower()} based on {len(evidence)} evidence item(s).

Supporting Evidence:

{chr(10).join(evidence\_lines)}

The candidate meets the behavioral anchor criteria for Score {score}: {', '.join(f'"{a}"' for a in matched\_anchors)}

{improvement\_note}"""

        

        return explanation

---

## 5\. Traceability Engine

### 5.1 Purpose

Maintain complete audit trails for every rubric, score, and decision in the system.

### 5.2 Data Model

class TraceabilityRecord:

    """Base class for all traceable records."""

    record\_id: str

    record\_type: str

    created\_at: datetime

    created\_by: str

    

    \# Chain of custody

    parent\_records: List\[str\]       \# IDs of records this derives from

    child\_records: List\[str\]        \# IDs of records derived from this

    

    \# Versioning

    version: str

    previous\_version: Optional\[str\]

    

    \# Audit

    audit\_log: List\[AuditEntry\]

class RubricTrace(TraceabilityRecord):

    """Trace for how a scoring rubric was created."""

    record\_type \= "RUBRIC"

    

    rubric\_id: str

    organization\_id: str

    role\_category: str

    

    \# Derivation details

    derivation\_method: str          \# RESEARCH\_DEFAULT | ORGANIZATIONAL\_EXTRACTION | ADJUSTED

    

    \# If from research

    research\_sources: Optional\[List\[Citation\]\]

    

    \# If from extraction

    extraction\_session\_ids: Optional\[List\[str\]\]

    top\_performer\_ids: Optional\[List\[str\]\]

    extraction\_methodology: Optional\[str\]

    

    \# If adjusted

    base\_rubric\_id: Optional\[str\]

    adjustments\_made: Optional\[List\[Adjustment\]\]

    adjustment\_rationales: Optional\[Dict\[str, str\]\]

    

    \# Validation

    validation\_status: str          \# VALIDATED | PENDING | NOT\_VALIDATED

    validation\_notes: Optional\[str\]

class AssessmentTrace(TraceabilityRecord):

    """Trace for how a candidate was assessed."""

    record\_type \= "ASSESSMENT"

    

    session\_id: str

    candidate\_id: str

    

    \# Rubric used

    rubric\_id: str

    rubric\_version: str

    rubric\_trace\_id: str            \# Links to RubricTrace

    

    \# Interview details

    interview\_start: datetime

    interview\_end: datetime

    interviewer\_id: Optional\[str\]   \# If human-conducted

    

    \# For each trait

    trait\_traces: List\[TraitAssessmentTrace\]

    

    \# Final assessment

    composite\_score: float

    recommendation: str

    recommendation\_explanation: str

class TraitAssessmentTrace:

    """Detailed trace for a single trait assessment."""

    trait\_id: str

    

    \# Probes used

    probes\_asked: List\[ProbeRecord\]

    

    \# Evidence collected

    evidence\_items: List\[EvidenceRecord\]

    

    \# Scoring

    raw\_score: int

    calibrated\_score: int

    score\_explanation: str

    

    \# Rubric alignment

    rubric\_item\_id: str

    matched\_behavioral\_anchors: List\[str\]

    scoring\_criteria\_applied: str

class EvidenceRecord:

    """Record of a single piece of evidence."""

    evidence\_id: str

    

    \# Source

    source\_type: str                \# BEHAVIORAL | HYPOTHETICAL | SELF\_REPORT | OBSERVED

    source\_exchange\_id: str         \# Links to specific interview exchange

    source\_text: str                \# Verbatim text

    

    \# Classification

    evidence\_classification: str

    weight\_applied: float

    weight\_rationale: str

    

    \# Trait mapping

    trait\_signals: List\[TraitSignal\]

class AuditEntry:

    """Single entry in audit log."""

    timestamp: datetime

    action: str                     \# CREATE | UPDATE | VIEW | EXPORT

    actor\_id: str

    actor\_type: str                 \# SYSTEM | USER | ADMIN

    details: Dict\[str, Any\]

### 5.3 Traceability Queries

class TraceabilityEngine:

    def get\_rubric\_derivation\_chain(self, rubric\_id: str) \-\> DerivationChain:

        """

        Get complete chain showing how a rubric was derived.

        

        Returns:

        \- Research sources (if default-based)

        \- Extraction sessions (if org-specific)

        \- All adjustments made

        \- Validation status

        """

        pass

    

    def get\_score\_justification(self, 

                                session\_id: str, 

                                trait\_id: str) \-\> ScoreJustification:

        """

        Get complete justification for a trait score.

        

        Returns:

        \- All evidence items with sources

        \- How evidence was weighted

        \- Which behavioral anchors were matched

        \- Full explanation text

        \- Link to rubric derivation

        """

        pass

    

    def get\_candidate\_assessment\_audit(self, candidate\_id: str) \-\> AssessmentAudit:

        """

        Get complete audit trail for a candidate's assessment.

        

        Returns:

        \- Resume analysis trace

        \- Stack ranking position and rationale

        \- Interview session details

        \- All scores with justifications

        \- Final recommendation with explanation

        """

        pass

    

    def export\_compliance\_report(self, 

                                organization\_id: str,

                                date\_range: Tuple\[datetime, datetime\]) \-\> ComplianceReport:

        """

        Export report suitable for compliance/audit purposes.

        

        Includes:

        \- All rubrics used and their derivation

        \- All assessments conducted

        \- Score distributions and patterns

        \- Any adjustments or overrides

        """

        pass

---

## 6\. API Specification

### 6.1 Profile Development APIs

\# Scenario Generation

POST /api/v1/scenarios/generate

  Request:

    job\_description: string

    role\_category: string

    target\_traits: string\[\]

    organization\_context?: object

  Response:

    scenario\_set\_id: string

    scenarios: Scenario\[\]

    generation\_trace\_id: string

\# Training Sessions

POST /api/v1/training-sessions/start

  Request:

    organization\_id: string

    top\_performer\_id: string

    scenario\_set\_id: string

    session\_config: SessionConfig

  Response:

    session\_id: string

    first\_prompt: string

POST /api/v1/training-sessions/{session\_id}/respond

  Request:

    response\_text: string

  Response:

    next\_prompt: string

    partial\_extraction?: PartialExtraction

GET /api/v1/training-sessions/{session\_id}/result

  Response:

    session\_result: SessionResult

    trait\_signals: TraitSignal\[\]

    training\_content: TrainingContent\[\]

\# Profile Extraction

POST /api/v1/profiles/extract

  Request:

    organization\_id: string

    role\_category: string

    session\_ids: string\[\]

  Response:

    extracted\_profile\_id: string

    profile: ExtractedProfile

    extraction\_trace\_id: string

\# Rubric Synthesis

POST /api/v1/rubrics/synthesize

  Request:

    organization\_id: string

    role\_category: string

    extracted\_profile\_id?: string  \# If org-specific

    use\_defaults: boolean

    adjustments?: Dict\[string, Adjustment\]

  Response:

    rubric\_id: string

    rubric: ScoringRubric

    rubric\_trace\_id: string

### 6.2 Candidate Assessment APIs

\# Resume Analysis

POST /api/v1/resumes/analyze

  Request:

    job\_description: string

    resumes: Resume\[\]

    analysis\_config?: AnalysisConfig

  Response:

    analysis\_results: ResumeAnalysisResult\[\]

    analysis\_trace\_id: string

\# Stack Ranking

POST /api/v1/candidates/rank

  Request:

    analysis\_results: string\[\]  \# IDs from resume analysis

    ranking\_config: RankingConfig

  Response:

    ranked\_set: RankedCandidateSet

    ranking\_trace\_id: string

\# Interview Sessions

POST /api/v1/interviews/start

  Request:

    candidate\_id: string

    rubric\_id: string

    interview\_config?: InterviewConfig

  Response:

    session\_id: string

    first\_prompt: string

POST /api/v1/interviews/{session\_id}/respond

  Request:

    response\_text: string

  Response:

    next\_prompt: string

    trait\_progress?: TraitProgress\[\]

GET /api/v1/interviews/{session\_id}/result

  Response:

    calibrated\_assessment: CalibratedAssessment

    assessment\_trace\_id: string

\# Assessment Reports

GET /api/v1/assessments/{session\_id}/report

  Response:

    summary: AssessmentSummary

    trait\_details: TraitDetail\[\]

    evidence\_chain: EvidenceChain

    recommendation: Recommendation

    full\_trace: AssessmentTrace

### 6.3 Rubric Management APIs

\# Default Rubrics

GET /api/v1/rubrics/defaults

  Response:

    defaults: ResearchDefaultRubric\[\]

GET /api/v1/rubrics/defaults/{trait\_id}

  Response:

    rubric: ResearchDefaultRubric

    adjustable\_parameters: AdjustableParameter\[\]

\# Organization Rubrics

GET /api/v1/organizations/{org\_id}/rubrics

  Response:

    rubrics: ScoringRubric\[\]

GET /api/v1/rubrics/{rubric\_id}

  Response:

    rubric: ScoringRubric

    derivation\_trace: RubricTrace

POST /api/v1/rubrics/{rubric\_id}/adjust

  Request:

    adjustments: Dict\[string, Any\]

    rationales: Dict\[string, string\]

  Response:

    new\_rubric\_id: string

    new\_rubric: ScoringRubric

    adjustment\_trace\_id: string

### 6.4 Traceability APIs

\# Trace Queries

GET /api/v1/traces/rubric/{rubric\_id}

  Response:

    derivation\_chain: DerivationChain

GET /api/v1/traces/assessment/{session\_id}

  Response:

    assessment\_audit: AssessmentAudit

GET /api/v1/traces/score/{session\_id}/{trait\_id}

  Response:

    score\_justification: ScoreJustification

\# Compliance Export

POST /api/v1/compliance/export

  Request:

    organization\_id: string

    date\_range: DateRange

    export\_format: string  \# PDF | JSON | CSV

  Response:

    report\_url: string

    report\_id: string

---

## 7\. Data Model Summary

### 7.1 Core Entities

┌─────────────────────────────────────────────────────────────────────────┐

│                           ENTITY RELATIONSHIPS                           │

├─────────────────────────────────────────────────────────────────────────┤

│                                                                          │

│  Organization                                                            │

│       │                                                                  │

│       ├──► TopPerformer ──► TrainingSession ──► SessionResult            │

│       │                                              │                   │

│       │                                              ▼                   │

│       │                                       ExtractedProfile           │

│       │                                              │                   │

│       ├──► JobDescription ──► ScenarioSet            │                   │

│       │                                              │                   │

│       │         ┌────────────────────────────────────┘                   │

│       │         │                                                        │

│       │         ▼                                                        │

│       ├──► ScoringRubric ◄─── ResearchDefaults                          │

│       │         │                                                        │

│       │         │                                                        │

│       ├──► Resume ──► ResumeAnalysis ──► RankedCandidateSet             │

│       │                                        │                         │

│       │                                        ▼                         │

│       └──► Candidate ──► InterviewSession ──► CalibratedAssessment      │

│                               │                      │                   │

│                               │                      │                   │

│                               ▼                      ▼                   │

│                         TraitAssessment      AssessmentReport            │

│                               │                                          │

│                               ▼                                          │

│                         EvidenceItem                                     │

│                                                                          │

│  ════════════════════════════════════════════════════════════════════   │

│                                                                          │

│  ALL ENTITIES ──► TraceabilityRecord                                     │

│                                                                          │

└─────────────────────────────────────────────────────────────────────────┘

### 7.2 Key Data Structures

\# Complete data model definitions

@dataclass

class Organization:

    id: str

    name: str

    created\_at: datetime

    settings: OrganizationSettings

@dataclass  

class ScoringRubric:

    rubric\_id: str

    organization\_id: str

    role\_category: str

    version: str

    

    items: List\[RubricItem\]

    

    \# Traceability

    source: RubricSource  \# RESEARCH\_DEFAULT | ORGANIZATIONAL | ADJUSTED

    derivation\_trace\_id: str

    created\_at: datetime

    created\_by: str

@dataclass

class CalibratedAssessment:

    session\_id: str

    candidate\_id: str

    rubric\_id: str

    

    \# Scores

    trait\_scores: List\[CalibratedTraitScore\]

    composite\_score: CompositeScore

    

    \# Recommendation

    recommendation: str  \# STRONG\_HIRE | HIRE | HOLD | NO\_HIRE

    recommendation\_explanation: str

    

    \# Traceability  

    assessment\_trace\_id: str

    created\_at: datetime

@dataclass

class CalibratedTraitScore:

    trait\_id: str

    

    \# Scores

    raw\_score: int

    calibrated\_score: int

    confidence: float

    

    \# Evidence

    evidence\_summary: str

    evidence\_items: List\[EvidenceItem\]

    

    \# Explanation

    explanation: str

    score\_rationale: str

    matched\_anchors: List\[str\]

    

    \# Traceability

    rubric\_item\_id: str

    rubric\_source: RubricSource

---

## 8\. Implementation Roadmap

### Phase 1: Foundation (Months 1-3)

**Deliverables**:

- Research default rubrics for 6 core traits  
- Resume analyzer (basic requirement matching)  
- Basic interview engine (STAR+ methodology)  
- Score calibrator with explanation generation  
- Traceability data model and storage

**Milestone**: End-to-end candidate assessment using research defaults

### Phase 2: Profile Development (Months 4-6)

**Deliverables**:

- Scenario generator  
- Training session engine  
- Profile extractor  
- Rubric synthesizer  
- Organization-specific rubric support

**Milestone**: Complete profile development workflow from top performers

### Phase 3: Advanced Assessment (Months 7-9)

**Deliverables**:

- Stack ranker / clusterer  
- Advanced evidence weighting  
- Rubric adjustment interface  
- Compliance reporting  
- Full traceability queries

**Milestone**: Production-ready assessment platform with full audit capability

### Phase 4: Scale & Intelligence (Months 10-12)

**Deliverables**:

- Multi-modal interview support (voice, video)  
- Outcome tracking and rubric refinement  
- Cross-organization benchmarking (anonymized)  
- Advanced analytics dashboard  
- API for ATS/HRIS integration

**Milestone**: Enterprise-ready platform with continuous learning

---

## 9\. Success Metrics

### 9.1 Objectivity Metrics

| Metric | Target | Measurement |
| :---- | :---- | :---- |
| Inter-rater reliability | κ \> 0.7 | Compare AI vs. human scoring on same interviews |
| Score explanation quality | \>90% rated "clear" | Human review of explanation text |
| Evidence traceability | 100% | Every score has linked evidence |
| Rubric derivation completeness | 100% | Every rubric has complete derivation chain |

### 9.2 Assessment Quality Metrics

| Metric | Target | Measurement |
| :---- | :---- | :---- |
| Predictive validity | r \> 0.3 | Assessment score vs. 6-month performance |
| Adverse impact ratio | \>0.8 | Protected class pass rates vs. majority |
| Candidate experience | \>4.0/5.0 | Post-interview survey |
| Time to assessment | \<60 min | Interview duration |

### 9.3 Profile Development Metrics

| Metric | Target | Measurement |
| :---- | :---- | :---- |
| Top performer engagement | \>80% participation | Invited vs. completed |
| Profile convergence | \>70% trait overlap | Cross-performer analysis |
| Training content utility | \>4.0/5.0 | New hire ratings of extracted content |
| Rubric validation rate | \>90% | Manager agreement with derived rubrics |

---

*Document Version 2.0 | AP API System Architecture* *© 2026 Tucuxi Inc. All rights reserved.*  
