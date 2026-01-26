"""Default role templates with associated traits and configurations."""

from typing import List, Dict, Any

# Default role templates - these are global templates organizations can clone and customize
ROLE_TEMPLATES: List[Dict[str, Any]] = [
    # ============= ENGINEERING ROLES =============
    {
        "name": "Software Engineer",
        "description": "Individual contributor focused on designing, developing, and maintaining software systems.",
        "role_category": "Engineering",
        "level": "Mid-Level",
        "department": "Engineering",
        "critical_traits": [
            {"trait_name": "Analytical Thinking", "level": "HIGH", "weight": 1.5, "rationale": "Core problem-solving requirement"},
            {"trait_name": "Detail Orientation", "level": "HIGH", "weight": 1.3, "rationale": "Code quality and bug prevention"},
        ],
        "positive_traits": [
            {"trait_name": "Curiosity", "level": "MODERATE", "weight": 1.0, "rationale": "Learning new technologies"},
            {"trait_name": "Collaboration", "level": "MODERATE", "weight": 1.0, "rationale": "Team development"},
            {"trait_name": "Follow-Through", "level": "MODERATE", "weight": 1.0, "rationale": "Completing projects"},
            {"trait_name": "Adaptability", "level": "MODERATE", "weight": 0.8, "rationale": "Changing requirements"},
        ],
        "counter_indicators": [
            {"trait_name": "Perfectionism", "threshold": "VERY_HIGH", "reason": "Can block shipping and create analysis paralysis"},
        ],
        "valence_notes": {
            "Creativity": "Valuable for architecture decisions but should be balanced with pragmatism",
            "Assertiveness": "Helpful for technical debates but shouldn't override team consensus",
        },
    },
    {
        "name": "Senior Software Engineer",
        "description": "Experienced engineer who leads technical decisions and mentors junior team members.",
        "role_category": "Engineering",
        "level": "Senior",
        "department": "Engineering",
        "critical_traits": [
            {"trait_name": "Analytical Thinking", "level": "HIGH", "weight": 1.5, "rationale": "System design and architecture"},
            {"trait_name": "Strategic Thinking", "level": "HIGH", "weight": 1.3, "rationale": "Long-term technical planning"},
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.2, "rationale": "Cross-team coordination and mentoring"},
        ],
        "positive_traits": [
            {"trait_name": "Influence", "level": "MODERATE", "weight": 1.0, "rationale": "Technical leadership"},
            {"trait_name": "Curiosity", "level": "MODERATE", "weight": 1.0, "rationale": "Staying current with technology"},
            {"trait_name": "Detail Orientation", "level": "MODERATE", "weight": 0.9, "rationale": "Code review and quality"},
            {"trait_name": "Empathy", "level": "MODERATE", "weight": 0.8, "rationale": "Mentoring effectiveness"},
        ],
        "counter_indicators": [
            {"trait_name": "Risk Orientation", "threshold": "VERY_HIGH", "reason": "May take unnecessary technical risks"},
            {"trait_name": "Perfectionism", "threshold": "VERY_HIGH", "reason": "Can slow down team velocity"},
        ],
        "valence_notes": {
            "Assertiveness": "Important for advocating technical decisions",
            "Independence": "Balanced with team collaboration",
        },
    },
    {
        "name": "Engineering Manager",
        "description": "Leads engineering teams, balancing technical oversight with people management.",
        "role_category": "Engineering Management",
        "level": "Manager",
        "department": "Engineering",
        "critical_traits": [
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.5, "rationale": "Team building and coordination"},
            {"trait_name": "Empathy", "level": "HIGH", "weight": 1.3, "rationale": "Understanding team needs and concerns"},
            {"trait_name": "Strategic Thinking", "level": "HIGH", "weight": 1.2, "rationale": "Technical roadmap planning"},
        ],
        "positive_traits": [
            {"trait_name": "Influence", "level": "HIGH", "weight": 1.1, "rationale": "Stakeholder management"},
            {"trait_name": "Analytical Thinking", "level": "MODERATE", "weight": 1.0, "rationale": "Technical decision-making"},
            {"trait_name": "Adaptability", "level": "MODERATE", "weight": 1.0, "rationale": "Handling changing priorities"},
            {"trait_name": "Conflict Tolerance", "level": "MODERATE", "weight": 0.9, "rationale": "Managing team dynamics"},
        ],
        "counter_indicators": [
            {"trait_name": "Detail Orientation", "threshold": "VERY_HIGH", "reason": "May micromanage instead of delegating"},
            {"trait_name": "Independence", "threshold": "VERY_HIGH", "reason": "Must be collaborative, not siloed"},
        ],
        "valence_notes": {
            "Assertiveness": "Needed for advocating for team but must be balanced",
            "Perfectionism": "Some standards important but shouldn't block team",
        },
    },

    # ============= PRODUCT ROLES =============
    {
        "name": "Product Manager",
        "description": "Defines product vision, prioritizes features, and coordinates between stakeholders.",
        "role_category": "Product Management",
        "level": "Mid-Level",
        "department": "Product",
        "critical_traits": [
            {"trait_name": "Strategic Thinking", "level": "HIGH", "weight": 1.5, "rationale": "Product vision and roadmap"},
            {"trait_name": "Influence", "level": "HIGH", "weight": 1.3, "rationale": "Stakeholder alignment without authority"},
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.2, "rationale": "Cross-functional coordination"},
        ],
        "positive_traits": [
            {"trait_name": "Curiosity", "level": "MODERATE", "weight": 1.0, "rationale": "Understanding user needs"},
            {"trait_name": "Analytical Thinking", "level": "MODERATE", "weight": 1.0, "rationale": "Data-driven decisions"},
            {"trait_name": "Empathy", "level": "MODERATE", "weight": 1.0, "rationale": "User-centric thinking"},
            {"trait_name": "Adaptability", "level": "MODERATE", "weight": 0.9, "rationale": "Changing market conditions"},
        ],
        "counter_indicators": [
            {"trait_name": "Detail Orientation", "threshold": "VERY_HIGH", "reason": "May get lost in details vs strategic view"},
            {"trait_name": "Independence", "threshold": "VERY_HIGH", "reason": "Role requires constant collaboration"},
        ],
        "valence_notes": {
            "Assertiveness": "Important for championing product vision",
            "Risk Orientation": "Balanced risk-taking for innovation",
        },
    },
    {
        "name": "Senior Product Manager",
        "description": "Leads product strategy for major product areas and mentors junior PMs.",
        "role_category": "Product Management",
        "level": "Senior",
        "department": "Product",
        "critical_traits": [
            {"trait_name": "Strategic Thinking", "level": "VERY_HIGH", "weight": 1.6, "rationale": "Multi-product/market strategy"},
            {"trait_name": "Influence", "level": "HIGH", "weight": 1.4, "rationale": "Executive stakeholder management"},
            {"trait_name": "Analytical Thinking", "level": "HIGH", "weight": 1.2, "rationale": "Market analysis and metrics"},
        ],
        "positive_traits": [
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.1, "rationale": "Cross-org coordination"},
            {"trait_name": "Empathy", "level": "MODERATE", "weight": 1.0, "rationale": "Mentoring and user understanding"},
            {"trait_name": "Risk Orientation", "level": "MODERATE", "weight": 0.9, "rationale": "Strategic bets"},
        ],
        "counter_indicators": [
            {"trait_name": "Perfectionism", "threshold": "VERY_HIGH", "reason": "Must ship incrementally"},
        ],
        "valence_notes": {},
    },

    # ============= SALES ROLES =============
    {
        "name": "Sales Representative",
        "description": "Builds relationships with prospects and closes deals.",
        "role_category": "Sales",
        "level": "Mid-Level",
        "department": "Sales",
        "critical_traits": [
            {"trait_name": "Influence", "level": "HIGH", "weight": 1.5, "rationale": "Persuading prospects"},
            {"trait_name": "Achievement Orientation", "level": "HIGH", "weight": 1.4, "rationale": "Meeting quotas"},
            {"trait_name": "Resilience", "level": "HIGH", "weight": 1.3, "rationale": "Handling rejection"},
        ],
        "positive_traits": [
            {"trait_name": "Empathy", "level": "MODERATE", "weight": 1.0, "rationale": "Understanding customer needs"},
            {"trait_name": "Urgency", "level": "MODERATE", "weight": 1.0, "rationale": "Driving deals forward"},
            {"trait_name": "Adaptability", "level": "MODERATE", "weight": 0.9, "rationale": "Adjusting pitch to audience"},
        ],
        "counter_indicators": [
            {"trait_name": "Analytical Thinking", "threshold": "VERY_HIGH", "reason": "May over-analyze vs taking action"},
            {"trait_name": "Detail Orientation", "threshold": "VERY_HIGH", "reason": "Can slow deal velocity"},
        ],
        "valence_notes": {
            "Risk Orientation": "Helpful for pursuing large deals",
            "Assertiveness": "Important but must not alienate prospects",
        },
    },
    {
        "name": "Account Executive",
        "description": "Manages complex enterprise sales cycles and key accounts.",
        "role_category": "Sales",
        "level": "Senior",
        "department": "Sales",
        "critical_traits": [
            {"trait_name": "Influence", "level": "VERY_HIGH", "weight": 1.6, "rationale": "C-level engagement"},
            {"trait_name": "Strategic Thinking", "level": "HIGH", "weight": 1.4, "rationale": "Account strategy"},
            {"trait_name": "Achievement Orientation", "level": "HIGH", "weight": 1.3, "rationale": "Large deal targets"},
        ],
        "positive_traits": [
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.1, "rationale": "Internal resource coordination"},
            {"trait_name": "Empathy", "level": "MODERATE", "weight": 1.0, "rationale": "Stakeholder mapping"},
            {"trait_name": "Resilience", "level": "MODERATE", "weight": 1.0, "rationale": "Long sales cycles"},
        ],
        "counter_indicators": [],
        "valence_notes": {},
    },

    # ============= CUSTOMER SUCCESS ROLES =============
    {
        "name": "Customer Success Manager",
        "description": "Ensures customer adoption, satisfaction, and retention.",
        "role_category": "Customer Success",
        "level": "Mid-Level",
        "department": "Customer Success",
        "critical_traits": [
            {"trait_name": "Service Orientation", "level": "HIGH", "weight": 1.5, "rationale": "Customer advocacy"},
            {"trait_name": "Empathy", "level": "HIGH", "weight": 1.4, "rationale": "Understanding customer challenges"},
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.2, "rationale": "Cross-functional problem solving"},
        ],
        "positive_traits": [
            {"trait_name": "Analytical Thinking", "level": "MODERATE", "weight": 1.0, "rationale": "Health metrics and analysis"},
            {"trait_name": "Influence", "level": "MODERATE", "weight": 1.0, "rationale": "Driving adoption"},
            {"trait_name": "Follow-Through", "level": "MODERATE", "weight": 0.9, "rationale": "Customer commitments"},
        ],
        "counter_indicators": [
            {"trait_name": "Assertiveness", "threshold": "VERY_HIGH", "reason": "May damage customer relationships"},
        ],
        "valence_notes": {
            "Achievement Orientation": "Good but shouldn't override customer needs",
        },
    },

    # ============= DATA ROLES =============
    {
        "name": "Data Analyst",
        "description": "Analyzes data to generate insights and inform business decisions.",
        "role_category": "Data/Analytics",
        "level": "Mid-Level",
        "department": "Data",
        "critical_traits": [
            {"trait_name": "Analytical Thinking", "level": "VERY_HIGH", "weight": 1.6, "rationale": "Core job function"},
            {"trait_name": "Detail Orientation", "level": "HIGH", "weight": 1.4, "rationale": "Data accuracy"},
            {"trait_name": "Curiosity", "level": "HIGH", "weight": 1.2, "rationale": "Finding insights"},
        ],
        "positive_traits": [
            {"trait_name": "Follow-Through", "level": "MODERATE", "weight": 1.0, "rationale": "Completing analyses"},
            {"trait_name": "Collaboration", "level": "MODERATE", "weight": 0.9, "rationale": "Stakeholder communication"},
        ],
        "counter_indicators": [],
        "valence_notes": {
            "Creativity": "Useful for visualization but analysis rigor comes first",
        },
    },
    {
        "name": "Data Scientist",
        "description": "Builds predictive models and applies machine learning to business problems.",
        "role_category": "Data/Analytics",
        "level": "Senior",
        "department": "Data",
        "critical_traits": [
            {"trait_name": "Analytical Thinking", "level": "VERY_HIGH", "weight": 1.6, "rationale": "Model development"},
            {"trait_name": "Curiosity", "level": "HIGH", "weight": 1.3, "rationale": "Research and experimentation"},
            {"trait_name": "Strategic Thinking", "level": "HIGH", "weight": 1.2, "rationale": "Business impact focus"},
        ],
        "positive_traits": [
            {"trait_name": "Detail Orientation", "level": "MODERATE", "weight": 1.0, "rationale": "Model accuracy"},
            {"trait_name": "Creativity", "level": "MODERATE", "weight": 1.0, "rationale": "Novel approaches"},
            {"trait_name": "Collaboration", "level": "MODERATE", "weight": 0.9, "rationale": "Cross-functional work"},
        ],
        "counter_indicators": [
            {"trait_name": "Perfectionism", "threshold": "VERY_HIGH", "reason": "May over-optimize vs shipping"},
        ],
        "valence_notes": {},
    },

    # ============= MARKETING ROLES =============
    {
        "name": "Marketing Manager",
        "description": "Plans and executes marketing campaigns to drive brand awareness and leads.",
        "role_category": "Marketing",
        "level": "Mid-Level",
        "department": "Marketing",
        "critical_traits": [
            {"trait_name": "Creativity", "level": "HIGH", "weight": 1.4, "rationale": "Campaign ideation"},
            {"trait_name": "Strategic Thinking", "level": "HIGH", "weight": 1.3, "rationale": "Marketing strategy"},
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.2, "rationale": "Cross-functional execution"},
        ],
        "positive_traits": [
            {"trait_name": "Analytical Thinking", "level": "MODERATE", "weight": 1.0, "rationale": "Performance metrics"},
            {"trait_name": "Adaptability", "level": "MODERATE", "weight": 1.0, "rationale": "Market changes"},
            {"trait_name": "Influence", "level": "MODERATE", "weight": 0.9, "rationale": "Stakeholder buy-in"},
        ],
        "counter_indicators": [],
        "valence_notes": {
            "Detail Orientation": "Important for execution but shouldn't limit creativity",
        },
    },

    # ============= OPERATIONS ROLES =============
    {
        "name": "Operations Manager",
        "description": "Oversees daily operations and process improvement.",
        "role_category": "Operations",
        "level": "Mid-Level",
        "department": "Operations",
        "critical_traits": [
            {"trait_name": "Detail Orientation", "level": "HIGH", "weight": 1.4, "rationale": "Process accuracy"},
            {"trait_name": "Consistency", "level": "HIGH", "weight": 1.3, "rationale": "Reliable execution"},
            {"trait_name": "Follow-Through", "level": "HIGH", "weight": 1.2, "rationale": "Project completion"},
        ],
        "positive_traits": [
            {"trait_name": "Analytical Thinking", "level": "MODERATE", "weight": 1.0, "rationale": "Process optimization"},
            {"trait_name": "Collaboration", "level": "MODERATE", "weight": 1.0, "rationale": "Cross-team coordination"},
            {"trait_name": "Adaptability", "level": "MODERATE", "weight": 0.9, "rationale": "Handling exceptions"},
        ],
        "counter_indicators": [
            {"trait_name": "Risk Orientation", "threshold": "VERY_HIGH", "reason": "Operations requires stability"},
        ],
        "valence_notes": {},
    },

    # ============= HR ROLES =============
    {
        "name": "HR Business Partner",
        "description": "Partners with business leaders on people strategy and employee relations.",
        "role_category": "Human Resources",
        "level": "Mid-Level",
        "department": "Human Resources",
        "critical_traits": [
            {"trait_name": "Empathy", "level": "VERY_HIGH", "weight": 1.5, "rationale": "Employee support"},
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.3, "rationale": "Business partnership"},
            {"trait_name": "Conflict Tolerance", "level": "HIGH", "weight": 1.2, "rationale": "Difficult conversations"},
        ],
        "positive_traits": [
            {"trait_name": "Influence", "level": "MODERATE", "weight": 1.0, "rationale": "Change management"},
            {"trait_name": "Strategic Thinking", "level": "MODERATE", "weight": 1.0, "rationale": "People strategy"},
            {"trait_name": "Detail Orientation", "level": "MODERATE", "weight": 0.9, "rationale": "Policy compliance"},
        ],
        "counter_indicators": [],
        "valence_notes": {
            "Assertiveness": "Needed for advocacy but must maintain trust",
        },
    },

    # ============= DESIGN ROLES =============
    {
        "name": "UX Designer",
        "description": "Designs user experiences through research, prototyping, and testing.",
        "role_category": "Design",
        "level": "Mid-Level",
        "department": "Design",
        "critical_traits": [
            {"trait_name": "Empathy", "level": "HIGH", "weight": 1.5, "rationale": "User-centered design"},
            {"trait_name": "Creativity", "level": "HIGH", "weight": 1.4, "rationale": "Design solutions"},
            {"trait_name": "Curiosity", "level": "HIGH", "weight": 1.2, "rationale": "User research"},
        ],
        "positive_traits": [
            {"trait_name": "Collaboration", "level": "HIGH", "weight": 1.1, "rationale": "Cross-functional work"},
            {"trait_name": "Detail Orientation", "level": "MODERATE", "weight": 1.0, "rationale": "Design polish"},
            {"trait_name": "Analytical Thinking", "level": "MODERATE", "weight": 0.9, "rationale": "Usability metrics"},
        ],
        "counter_indicators": [],
        "valence_notes": {
            "Perfectionism": "Design quality matters but must ship",
        },
    },

    # ============= FINANCE ROLES =============
    {
        "name": "Financial Analyst",
        "description": "Analyzes financial data and creates forecasts to support business decisions.",
        "role_category": "Finance",
        "level": "Mid-Level",
        "department": "Finance",
        "critical_traits": [
            {"trait_name": "Analytical Thinking", "level": "VERY_HIGH", "weight": 1.6, "rationale": "Financial modeling"},
            {"trait_name": "Detail Orientation", "level": "VERY_HIGH", "weight": 1.5, "rationale": "Accuracy critical"},
            {"trait_name": "Consistency", "level": "HIGH", "weight": 1.2, "rationale": "Reliable reporting"},
        ],
        "positive_traits": [
            {"trait_name": "Follow-Through", "level": "MODERATE", "weight": 1.0, "rationale": "Deadline management"},
            {"trait_name": "Collaboration", "level": "MODERATE", "weight": 0.9, "rationale": "Business partnership"},
        ],
        "counter_indicators": [
            {"trait_name": "Risk Orientation", "threshold": "HIGH", "reason": "Finance requires conservative approach"},
            {"trait_name": "Creativity", "threshold": "VERY_HIGH", "reason": "Must follow established standards"},
        ],
        "valence_notes": {},
    },
]
