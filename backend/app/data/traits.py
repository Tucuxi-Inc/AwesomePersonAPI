"""24 trait definitions from AP API Trait Taxonomy."""

from typing import List, Dict, Any

# Trait categories
TRAIT_CATEGORIES = [
    "COGNITIVE",
    "INTERPERSONAL",
    "EXECUTION",
    "STABILITY",
    "SELF_MANAGEMENT",
    "ORIENTATION",
]

# All 24 traits with full definitions
TRAITS: List[Dict[str, Any]] = [
    # ============= COGNITIVE TRAITS =============
    {
        "name": "Curiosity",
        "category": "COGNITIVE",
        "definition": "The intrinsic drive to explore, understand, and learn beyond immediate requirements.",
        "spectrum_low_label": "Incurious, accepting",
        "spectrum_high_label": "Questioning, exploring",
        "behavioral_markers_low": [
            "Accepts information at face value",
            "Doesn't ask questions",
            "Learns only when required",
        ],
        "behavioral_markers_high": [
            "Questions assumptions",
            "Seeks to understand 'why'",
            "Pursues learning voluntarily",
        ],
        "counter_indicator_for": [
            "Strict Protocol Adherence",
            "Highly Regulated Compliance",
        ],
        "display_order": 1,
        "valence_mappings": [
            {"role_category": "R&D/Innovation", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Discovery requires questioning"},
            {"role_category": "Product Management", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Understanding user needs"},
            {"role_category": "Assembly Line Work", "valence": "NEUTRAL", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Focus on execution, not exploration"},
            {"role_category": "Entry-level Execution", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Some curiosity good, but need to follow process"},
        ],
    },
    {
        "name": "Analytical Thinking",
        "category": "COGNITIVE",
        "definition": "The tendency to break down complex problems into components and evaluate them systematically.",
        "spectrum_low_label": "Intuitive, holistic",
        "spectrum_high_label": "Systematic, data-driven",
        "behavioral_markers_low": [
            "Relies on gut feel",
            "Makes quick judgments",
            "Comfortable with incomplete information",
        ],
        "behavioral_markers_high": [
            "Breaks down problems",
            "Seeks data",
            "Builds frameworks",
            "Documents reasoning",
        ],
        "counter_indicator_for": [
            "Crisis Response",
            "Fast-paced Intuitive Roles",
        ],
        "display_order": 2,
        "valence_mappings": [
            {"role_category": "Data Science/Finance", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Core job requirement"},
            {"role_category": "Engineering", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Problem-solving foundation"},
            {"role_category": "Sales", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Need balance with relationship intuition"},
            {"role_category": "Creative Roles", "valence": "CONTEXT_DEPENDENT", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Can inhibit creative flow"},
        ],
    },
    {
        "name": "Creativity",
        "category": "COGNITIVE",
        "definition": "The ability to generate novel ideas, approaches, and solutions.",
        "spectrum_low_label": "Conventional, proven methods",
        "spectrum_high_label": "Novel, original approaches",
        "behavioral_markers_low": [
            "Prefers established approaches",
            "Follows templates",
            "Uncomfortable with blank slate",
        ],
        "behavioral_markers_high": [
            "Generates many ideas",
            "Makes unusual connections",
            "Comfortable with ambiguity",
        ],
        "counter_indicator_for": [
            "Accounting/Compliance",
            "Surgery/Aviation",
            "Manufacturing QA",
        ],
        "display_order": 3,
        "valence_mappings": [
            {"role_category": "Design/Marketing", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Core job requirement"},
            {"role_category": "Startup/Entrepreneurship", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Novel solutions needed"},
            {"role_category": "Accounting/Compliance", "valence": "NEGATIVE", "optimal_range_min": 1, "optimal_range_max": 3, "rationale": "Need to follow established rules"},
            {"role_category": "Safety-Critical", "valence": "NEGATIVE", "optimal_range_min": 1, "optimal_range_max": 3, "rationale": "Proven protocols save lives"},
        ],
    },
    {
        "name": "Detail Orientation",
        "category": "COGNITIVE",
        "definition": "The tendency to focus on specifics, notice small discrepancies, and ensure accuracy.",
        "spectrum_low_label": "Big-picture, approximate",
        "spectrum_high_label": "Precise, thorough",
        "behavioral_markers_low": [
            "Comfortable with 'good enough'",
            "Focuses on major issues",
            "May miss small errors",
        ],
        "behavioral_markers_high": [
            "Catches small errors",
            "Thorough review",
            "May struggle to move past details",
        ],
        "counter_indicator_for": [
            "Fast-paced Shipping",
            "Startup MVP Development",
        ],
        "display_order": 4,
        "valence_mappings": [
            {"role_category": "QA/Editing/Auditing", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Core job requirement"},
            {"role_category": "Legal Document Review", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Errors have major consequences"},
            {"role_category": "Executive Leadership", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Need to delegate details"},
            {"role_category": "Startup Founder", "valence": "LOWER", "optimal_range_min": 2, "optimal_range_max": 3, "rationale": "Perfect is enemy of shipped"},
        ],
    },
    {
        "name": "Strategic Thinking",
        "category": "COGNITIVE",
        "definition": "The ability to see long-term implications, patterns, and systemic relationships.",
        "spectrum_low_label": "Tactical, immediate",
        "spectrum_high_label": "Strategic, long-term",
        "behavioral_markers_low": [
            "Focuses on immediate tasks",
            "May miss bigger picture",
            "Strong executor",
        ],
        "behavioral_markers_high": [
            "Considers 2nd/3rd order effects",
            "Identifies patterns",
            "Connects to larger goals",
        ],
        "counter_indicator_for": [
            "Entry-level Execution",
            "Pure Execution Roles",
        ],
        "display_order": 5,
        "valence_mappings": [
            {"role_category": "Executive Leadership", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Core job requirement"},
            {"role_category": "Product Strategy", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Long-term vision needed"},
            {"role_category": "Individual Contributor", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Some helpful, but execution primary"},
            {"role_category": "Entry-level Roles", "valence": "LOWER", "optimal_range_min": 1, "optimal_range_max": 3, "rationale": "May frustrate without scope to apply"},
        ],
    },
    # ============= INTERPERSONAL TRAITS =============
    {
        "name": "Collaboration",
        "category": "INTERPERSONAL",
        "definition": "The ability to work effectively with others toward shared goals.",
        "spectrum_low_label": "Independent, solo",
        "spectrum_high_label": "Team-oriented, cooperative",
        "behavioral_markers_low": [
            "Prefers working alone",
            "May struggle with group dynamics",
            "Strong individual contributor",
        ],
        "behavioral_markers_high": [
            "Seeks input",
            "Shares credit",
            "Coordinates well",
            "May struggle with solo work",
        ],
        "counter_indicator_for": [
            "Solo Security Research",
            "Highly Independent Roles",
        ],
        "display_order": 6,
        "valence_mappings": [
            {"role_category": "Cross-functional PM", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Coordination is the job"},
            {"role_category": "Team-based Engineering", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Code review, pairing, team success"},
            {"role_category": "Solo Research", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Some collaboration good, but independence needed"},
            {"role_category": "Remote Individual Contributor", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Need self-direction"},
        ],
    },
    {
        "name": "Assertiveness",
        "category": "INTERPERSONAL",
        "definition": "The tendency to express opinions, make requests, and stand firm on positions.",
        "spectrum_low_label": "Deferential, accommodating",
        "spectrum_high_label": "Direct, forceful",
        "behavioral_markers_low": [
            "Avoids conflict",
            "Defers to others",
            "May not advocate for self/ideas",
        ],
        "behavioral_markers_high": [
            "States positions clearly",
            "Pushes back when needed",
            "May dominate discussions",
        ],
        "counter_indicator_for": [
            "Counseling/Therapy",
            "Client-centered Roles",
            "Facilitation Roles",
        ],
        "display_order": 7,
        "valence_mappings": [
            {"role_category": "Sales/Negotiation", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Need to advocate and close"},
            {"role_category": "Leadership", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Decision-making requires stance-taking"},
            {"role_category": "Customer Support", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Need balance with empathy"},
            {"role_category": "Junior Roles", "valence": "CONTEXT_DEPENDENT", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "May conflict with hierarchy"},
        ],
    },
    {
        "name": "Empathy",
        "category": "INTERPERSONAL",
        "definition": "The ability to understand and share the feelings of others.",
        "spectrum_low_label": "Detached, objective",
        "spectrum_high_label": "Attuned, feeling-with",
        "behavioral_markers_low": [
            "Task-focused",
            "May miss emotional cues",
            "Efficient but cold",
        ],
        "behavioral_markers_high": [
            "Reads emotional states",
            "Validates feelings",
            "May absorb others' emotions",
        ],
        "counter_indicator_for": [
            "Quantitative Trading",
            "Objective Decision-Making Roles",
        ],
        "display_order": 8,
        "valence_mappings": [
            {"role_category": "Healthcare/Counseling", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Core to patient care"},
            {"role_category": "Customer Success", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Understanding customer needs"},
            {"role_category": "People Management", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Team support and development"},
            {"role_category": "High-stakes Decision Making", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Need to make hard calls"},
        ],
    },
    {
        "name": "Influence",
        "category": "INTERPERSONAL",
        "definition": "The ability to shape others' opinions, decisions, and actions.",
        "spectrum_low_label": "Low-profile, non-persuasive",
        "spectrum_high_label": "Persuasive, politically skilled",
        "behavioral_markers_low": [
            "Lets work speak for itself",
            "Uncomfortable with politics",
            "May be overlooked",
        ],
        "behavioral_markers_high": [
            "Builds coalitions",
            "Shapes narratives",
            "Navigates politics",
            "May seem manipulative",
        ],
        "counter_indicator_for": [
            "Auditing/Compliance",
            "Independent Research",
        ],
        "display_order": 9,
        "valence_mappings": [
            {"role_category": "Executive Leadership", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Alignment requires influence"},
            {"role_category": "Sales/BD", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Persuasion is the job"},
            {"role_category": "Change Management", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Need buy-in for change"},
            {"role_category": "Technical IC", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Some helpful for ideas, but not core"},
        ],
    },
    {
        "name": "Conflict Tolerance",
        "category": "INTERPERSONAL",
        "definition": "Comfort with interpersonal disagreement and tension.",
        "spectrum_low_label": "Harmony-seeking, avoidant",
        "spectrum_high_label": "Conflict-comfortable, confrontational",
        "behavioral_markers_low": [
            "Smooths over disagreements",
            "Avoids hard conversations",
            "May enable dysfunction",
        ],
        "behavioral_markers_high": [
            "Addresses issues directly",
            "Comfortable with tension",
            "May create unnecessary conflict",
        ],
        "counter_indicator_for": [
            "Relationship Preservation Roles",
        ],
        "display_order": 10,
        "valence_mappings": [
            {"role_category": "Management", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Performance conversations require it"},
            {"role_category": "Negotiation", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Tension is inherent"},
            {"role_category": "Legal Litigation", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Adversarial by nature"},
            {"role_category": "Customer-facing Roles", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Need to handle complaints but not escalate"},
        ],
    },
    # ============= EXECUTION TRAITS =============
    {
        "name": "Initiative",
        "category": "EXECUTION",
        "definition": "The tendency to act proactively without being directed.",
        "spectrum_low_label": "Reactive, directed",
        "spectrum_high_label": "Proactive, self-starting",
        "behavioral_markers_low": [
            "Waits for direction",
            "Strong executor of assigned tasks",
            "May miss opportunities",
        ],
        "behavioral_markers_high": [
            "Identifies problems and acts",
            "May overstep",
            "Strong ownership",
        ],
        "counter_indicator_for": [
            "Strict Protocol Roles",
            "Highly Structured Roles",
        ],
        "display_order": 11,
        "valence_mappings": [
            {"role_category": "Entrepreneurship", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "No one else to direct"},
            {"role_category": "Leadership", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Setting direction is the job"},
            {"role_category": "Early-stage Startup", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Ambiguity requires initiative"},
            {"role_category": "Highly Structured Roles", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Process exists for reasons"},
        ],
    },
    {
        "name": "Consistency",
        "category": "EXECUTION",
        "definition": "The tendency to maintain stable, predictable performance and behavior over time.",
        "spectrum_low_label": "Variable, situational",
        "spectrum_high_label": "Steady, predictable",
        "behavioral_markers_low": [
            "Performance varies",
            "Adapts to situation",
            "May seem unreliable",
        ],
        "behavioral_markers_high": [
            "Same approach regardless of context",
            "Reliable but may miss when change needed",
        ],
        "counter_indicator_for": [
            "Startup Environment",
            "Innovation Roles",
        ],
        "display_order": 12,
        "valence_mappings": [
            {"role_category": "Accounting/Finance", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Predictability is essential"},
            {"role_category": "Manufacturing QA", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Variation is the enemy"},
            {"role_category": "Customer Service", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Consistent experience matters"},
            {"role_category": "Startup Environment", "valence": "LOWER", "optimal_range_min": 2, "optimal_range_max": 3, "rationale": "Need to adapt rapidly"},
        ],
    },
    {
        "name": "Urgency",
        "category": "EXECUTION",
        "definition": "The tendency to act quickly and prioritize speed.",
        "spectrum_low_label": "Deliberate, thorough",
        "spectrum_high_label": "Fast, action-oriented",
        "behavioral_markers_low": [
            "Takes time to decide",
            "Thorough analysis",
            "May miss time-sensitive opportunities",
        ],
        "behavioral_markers_high": [
            "Decides quickly",
            "May sacrifice quality for speed",
            "High output",
        ],
        "counter_indicator_for": [
            "Legal Document Review",
            "Quality Control",
        ],
        "display_order": 13,
        "valence_mappings": [
            {"role_category": "Sales (closing)", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Deals have windows"},
            {"role_category": "Emergency Response", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Speed saves lives"},
            {"role_category": "Startup Execution", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Runway is finite"},
            {"role_category": "Long-term Research", "valence": "LOWER", "optimal_range_min": 1, "optimal_range_max": 3, "rationale": "Rushing leads to errors"},
        ],
    },
    {
        "name": "Perfectionism",
        "category": "EXECUTION",
        "definition": "The tendency to seek flawlessness and set extremely high standards.",
        "spectrum_low_label": "Pragmatic, 'good enough'",
        "spectrum_high_label": "Exacting, never satisfied",
        "behavioral_markers_low": [
            "Ships quickly",
            "Comfortable with '80%'",
            "May miss quality issues",
        ],
        "behavioral_markers_high": [
            "High standards",
            "Thorough",
            "May delay delivery",
            "Self-critical",
        ],
        "counter_indicator_for": [
            "Startup MVP Development",
            "Agile Development",
        ],
        "display_order": 14,
        "valence_mappings": [
            {"role_category": "Surgical/Medical", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Errors are catastrophic"},
            {"role_category": "Legal Document Review", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Details matter enormously"},
            {"role_category": "Quality Assurance", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Finding defects is the job"},
            {"role_category": "Startup MVP Development", "valence": "NEGATIVE", "optimal_range_min": 1, "optimal_range_max": 3, "rationale": "Perfect is enemy of shipped"},
        ],
    },
    {
        "name": "Follow-Through",
        "category": "EXECUTION",
        "definition": "The tendency to complete tasks and commitments reliably.",
        "spectrum_low_label": "Starts but doesn't finish",
        "spectrum_high_label": "Completes what's started",
        "behavioral_markers_low": [
            "Many initiatives started; few completed",
            "Excited by new over finishing",
        ],
        "behavioral_markers_high": [
            "Reliable completion",
            "May resist taking on new until current done",
        ],
        "counter_indicator_for": [],  # Generally positive across contexts
        "display_order": 15,
        "valence_mappings": [
            {"role_category": "Project Management", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Completion is the job"},
            {"role_category": "Operations", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Reliability is essential"},
            {"role_category": "Any Role with Commitments", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Trust depends on delivery"},
            {"role_category": "Early Exploration/Ideation", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Sometimes pivoting is right"},
        ],
    },
    # ============= STABILITY TRAITS =============
    {
        "name": "Resilience",
        "category": "STABILITY",
        "definition": "The capacity to recover from setbacks and maintain effectiveness under pressure.",
        "spectrum_low_label": "Fragile, slow recovery",
        "spectrum_high_label": "Bounces back, maintains function",
        "behavioral_markers_low": [
            "Extended impact from setbacks",
            "May avoid risk to prevent failure",
        ],
        "behavioral_markers_high": [
            "Quick recovery",
            "Learns from failure",
            "May underestimate impact of events",
        ],
        "counter_indicator_for": [],  # Positive across most contexts
        "display_order": 16,
        "valence_mappings": [
            {"role_category": "Sales (rejection-heavy)", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Rejection is constant"},
            {"role_category": "Entrepreneurship", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Failure is part of the process"},
            {"role_category": "Emergency Services", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Must function under trauma"},
            {"role_category": "High-stakes Roles", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Setbacks are inevitable"},
        ],
    },
    {
        "name": "Stress Tolerance",
        "category": "STABILITY",
        "definition": "The ability to function effectively under pressure and high-stakes conditions.",
        "spectrum_low_label": "Needs calm conditions",
        "spectrum_high_label": "Thrives under pressure",
        "behavioral_markers_low": [
            "Performance degrades under stress",
            "Needs recovery time",
            "Avoids high-pressure",
        ],
        "behavioral_markers_high": [
            "Maintains or improves under pressure",
            "May seek out stress",
            "May not recognize impact",
        ],
        "counter_indicator_for": [],  # Generally positive
        "display_order": 17,
        "valence_mappings": [
            {"role_category": "Emergency Medicine", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Life-or-death pressure"},
            {"role_category": "Trading Floor", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Constant high stakes"},
            {"role_category": "Startup Leadership", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Pressure is constant"},
            {"role_category": "Research", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Some deadline pressure, but generally calmer"},
        ],
    },
    {
        "name": "Emotional Regulation",
        "category": "STABILITY",
        "definition": "The ability to manage one's emotional responses and expressions.",
        "spectrum_low_label": "Emotionally reactive",
        "spectrum_high_label": "Emotionally controlled",
        "behavioral_markers_low": [
            "Emotions visible",
            "May react in moment",
            "Authentic but unpredictable",
        ],
        "behavioral_markers_high": [
            "Steady demeanor",
            "May seem detached",
            "Professional but potentially suppressed",
        ],
        "counter_indicator_for": [
            "Creative Expression Roles",
        ],
        "display_order": 18,
        "valence_mappings": [
            {"role_category": "Executive Leadership", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Team looks to leader for stability"},
            {"role_category": "Customer-facing Crisis", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Calm reassures customers"},
            {"role_category": "Negotiation", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Emotional tells are costly"},
            {"role_category": "Creative Expression", "valence": "LOWER", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Authenticity may require expression"},
        ],
    },
    {
        "name": "Ambiguity Tolerance",
        "category": "STABILITY",
        "definition": "Comfort with uncertainty, incomplete information, and undefined situations.",
        "spectrum_low_label": "Needs clarity, definition",
        "spectrum_high_label": "Comfortable with undefined",
        "behavioral_markers_low": [
            "Seeks clear direction",
            "Uncomfortable with 'figure it out'",
            "Strong in defined roles",
        ],
        "behavioral_markers_high": [
            "Comfortable without roadmap",
            "May not seek needed clarity",
            "Strong in undefined roles",
        ],
        "counter_indicator_for": [
            "Highly Structured Roles",
            "Manufacturing",
        ],
        "display_order": 19,
        "valence_mappings": [
            {"role_category": "Startup (early stage)", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Everything is undefined"},
            {"role_category": "Consulting", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Each client is different"},
            {"role_category": "R&D/Innovation", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Exploration means uncertainty"},
            {"role_category": "Established Process Roles", "valence": "LOWER", "optimal_range_min": 2, "optimal_range_max": 3, "rationale": "Process provides clarity"},
        ],
    },
    # ============= SELF-MANAGEMENT TRAITS =============
    {
        "name": "Adaptability",
        "category": "SELF_MANAGEMENT",
        "definition": "The capacity to adjust approach when circumstances change.",
        "spectrum_low_label": "Consistent, steady",
        "spectrum_high_label": "Flexible, changeable",
        "behavioral_markers_low": [
            "Prefers routine",
            "May resist change",
            "Strong in stable environments",
        ],
        "behavioral_markers_high": [
            "Adjusts readily",
            "May lack consistency",
            "Strong in changing environments",
        ],
        "counter_indicator_for": [
            "Extreme Consistency Roles",
        ],
        "display_order": 20,
        "valence_mappings": [
            {"role_category": "Startup Environment", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Constant change"},
            {"role_category": "Consulting", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Every engagement different"},
            {"role_category": "Change Management", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Modeling adaptability"},
            {"role_category": "Stable Operations", "valence": "LOWER", "optimal_range_min": 2, "optimal_range_max": 3, "rationale": "Consistency may be more valued"},
        ],
    },
    {
        "name": "Independence",
        "category": "SELF_MANAGEMENT",
        "definition": "The preference and ability to work autonomously without close supervision.",
        "spectrum_low_label": "Prefers guidance, direction",
        "spectrum_high_label": "Self-directed, autonomous",
        "behavioral_markers_low": [
            "Seeks input",
            "May struggle without direction",
            "Strong collaborator",
        ],
        "behavioral_markers_high": [
            "Works alone effectively",
            "May not seek needed input",
            "May resist oversight",
        ],
        "counter_indicator_for": [
            "Highly Collaborative Teams",
            "Junior Learning Roles",
        ],
        "display_order": 21,
        "valence_mappings": [
            {"role_category": "Remote Work", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "No one watching"},
            {"role_category": "Research (solo)", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Extended individual work"},
            {"role_category": "Field Roles", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Operating without direct supervision"},
            {"role_category": "Junior Roles", "valence": "LOWER", "optimal_range_min": 2, "optimal_range_max": 3, "rationale": "Need guidance while learning"},
        ],
    },
    {
        "name": "Self-Awareness",
        "category": "SELF_MANAGEMENT",
        "definition": "Accurate understanding of one's own strengths, weaknesses, and impact.",
        "spectrum_low_label": "Blind spots, inaccurate self-view",
        "spectrum_high_label": "Accurate self-knowledge",
        "behavioral_markers_low": [
            "Overestimates or underestimates self",
            "Surprised by feedback",
            "Misreads impact",
        ],
        "behavioral_markers_high": [
            "Accurate self-assessment",
            "Seeks feedback",
            "Understands impact on others",
        ],
        "counter_indicator_for": [],  # Positive across contexts
        "display_order": 22,
        "valence_mappings": [
            {"role_category": "Leadership", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Leading requires knowing self"},
            {"role_category": "Management", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "People development requires modeling"},
            {"role_category": "Any Growth-oriented Role", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Improvement requires awareness"},
            {"role_category": "Highly Structured Roles", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Less critical but still helpful"},
        ],
    },
    {
        "name": "Accountability",
        "category": "SELF_MANAGEMENT",
        "definition": "The tendency to own outcomes and take responsibility for results.",
        "spectrum_low_label": "Externalizes, blames",
        "spectrum_high_label": "Owns, takes responsibility",
        "behavioral_markers_low": [
            "Attributes failures externally",
            "May not own mistakes",
            "Avoids responsibility",
        ],
        "behavioral_markers_high": [
            "Takes responsibility even when shared",
            "May over-own",
            "Strong ownership",
        ],
        "counter_indicator_for": [],  # Positive across contexts
        "display_order": 23,
        "valence_mappings": [
            {"role_category": "Leadership", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "The buck stops here"},
            {"role_category": "Any Role with Deliverables", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Ownership drives completion"},
            {"role_category": "Team Environments", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Trust requires accountability"},
            {"role_category": "Highly Collaborative", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Need to also distribute appropriately"},
        ],
    },
    # ============= ORIENTATION TRAITS =============
    {
        "name": "Risk Orientation",
        "category": "ORIENTATION",
        "definition": "Comfort with and tendency toward risk-taking vs. risk-avoidance.",
        "spectrum_low_label": "Risk-averse, cautious",
        "spectrum_high_label": "Risk-seeking, bold",
        "behavioral_markers_low": [
            "Prefers proven approaches",
            "Thorough analysis before action",
            "May miss opportunities",
        ],
        "behavioral_markers_high": [
            "Comfortable with uncertainty",
            "Acts on incomplete info",
            "May take unnecessary risks",
        ],
        "counter_indicator_for": [
            "Surgery/Aviation",
            "Compliance/Auditing",
            "Safety-critical Roles",
        ],
        "display_order": 24,
        "valence_mappings": [
            {"role_category": "Entrepreneurship", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Startups are inherently risky"},
            {"role_category": "Venture Capital", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Portfolio approach requires risk"},
            {"role_category": "Surgery/Aviation", "valence": "HIGH_NEGATIVE", "optimal_range_min": 1, "optimal_range_max": 2, "rationale": "Caution saves lives"},
            {"role_category": "Compliance/Auditing", "valence": "NEGATIVE", "optimal_range_min": 1, "optimal_range_max": 2, "rationale": "Risk-seeking is disqualifying"},
        ],
    },
    {
        "name": "Achievement Orientation",
        "category": "ORIENTATION",
        "definition": "The drive to accomplish goals and exceed standards.",
        "spectrum_low_label": "Content, low-drive",
        "spectrum_high_label": "Driven, ambitious",
        "behavioral_markers_low": [
            "Satisfied with adequate",
            "May not push for more",
            "Work-life balance priority",
        ],
        "behavioral_markers_high": [
            "Sets high goals",
            "Competitive",
            "May burn out or push others too hard",
        ],
        "counter_indicator_for": [
            "Sustainability-focused Cultures",
        ],
        "display_order": 25,
        "valence_mappings": [
            {"role_category": "Sales", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Quota attainment requires drive"},
            {"role_category": "Entrepreneurship", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Ambition fuels growth"},
            {"role_category": "Leadership", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Drive inspires teams"},
            {"role_category": "Sustainable Long-term Roles", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Burnout risk if too high"},
        ],
    },
    {
        "name": "Service Orientation",
        "category": "ORIENTATION",
        "definition": "The drive to help, support, and serve others' needs.",
        "spectrum_low_label": "Self-focused",
        "spectrum_high_label": "Other-focused",
        "behavioral_markers_low": [
            "Prioritizes own work",
            "May not go out of way for others",
            "Task over relationship",
        ],
        "behavioral_markers_high": [
            "Goes extra mile for others",
            "May neglect own needs",
            "Relationship over task",
        ],
        "counter_indicator_for": [
            "Individual Output Roles",
        ],
        "display_order": 26,
        "valence_mappings": [
            {"role_category": "Customer Support", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Service is the job"},
            {"role_category": "Healthcare", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Patient focus essential"},
            {"role_category": "Hospitality", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Guest experience is everything"},
            {"role_category": "Sales (hunting)", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Need balance with closing"},
        ],
    },
    {
        "name": "Learning Orientation",
        "category": "ORIENTATION",
        "definition": "The priority placed on continuous development and skill growth.",
        "spectrum_low_label": "Fixed, arrived",
        "spectrum_high_label": "Growth, developing",
        "behavioral_markers_low": [
            "Relies on existing skills",
            "May resist new methods",
            "Strong in stable domains",
        ],
        "behavioral_markers_high": [
            "Always learning",
            "May not apply existing skills",
            "Strong in evolving domains",
        ],
        "counter_indicator_for": [
            "Stable Expertise Roles",
        ],
        "display_order": 27,
        "valence_mappings": [
            {"role_category": "Technology (fast-moving)", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Skills become obsolete"},
            {"role_category": "R&D", "valence": "HIGH_POSITIVE", "optimal_range_min": 4, "optimal_range_max": 5, "rationale": "Learning is the work"},
            {"role_category": "Any Role in Changing Industry", "valence": "POSITIVE", "optimal_range_min": 3, "optimal_range_max": 5, "rationale": "Adaptation requires learning"},
            {"role_category": "Stable Mature Industries", "valence": "MODERATE", "optimal_range_min": 2, "optimal_range_max": 4, "rationale": "Existing expertise may suffice"},
        ],
    },
]
