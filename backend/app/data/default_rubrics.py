"""Research-based default rubrics for 6 core traits."""

from typing import List, Dict, Any

# Default rubrics for initial 6 core traits
DEFAULT_RUBRICS: List[Dict[str, Any]] = [
    {
        "trait_name": "Curiosity",
        "name": "Curiosity Assessment Rubric",
        "description": "Research-based rubric for assessing intellectual curiosity and drive to learn.",
        "behavioral_anchors": {
            "1": {
                "label": "Low Curiosity",
                "description": "Accepts information at face value without questioning. Learns only when explicitly required. Shows no interest in understanding underlying reasons.",
                "indicators": [
                    "Never asks 'why' questions",
                    "Doesn't seek to understand context",
                    "Avoids learning opportunities",
                    "Sticks rigidly to what they know",
                ],
            },
            "2": {
                "label": "Below Average Curiosity",
                "description": "Occasionally asks questions but doesn't pursue answers. Some interest in learning but only when directly relevant to immediate tasks.",
                "indicators": [
                    "Asks surface-level questions",
                    "Limited follow-through on learning",
                    "Passive recipient of information",
                ],
            },
            "3": {
                "label": "Moderate Curiosity",
                "description": "Shows genuine interest in understanding work-related topics. Asks relevant questions. Engages in learning when opportunities arise.",
                "indicators": [
                    "Asks clarifying questions",
                    "Seeks to understand before acting",
                    "Participates in training willingly",
                    "Shows interest in adjacent topics",
                ],
            },
            "4": {
                "label": "High Curiosity",
                "description": "Proactively seeks to understand beyond requirements. Regularly explores new topics. Questions assumptions and seeks deeper understanding.",
                "indicators": [
                    "Independently researches topics",
                    "Asks 'why' and 'what if' questions",
                    "Connects ideas across domains",
                    "Seeks out learning opportunities",
                ],
            },
            "5": {
                "label": "Exceptional Curiosity",
                "description": "Deep intellectual drive. Continuously questions and explores. Actively challenges assumptions. Pursues learning for its own sake.",
                "indicators": [
                    "Relentless questioning of status quo",
                    "Self-directed learning across domains",
                    "Synthesizes knowledge creatively",
                    "Inspires curiosity in others",
                ],
            },
        },
        "primary_probes": [
            {
                "question": "Tell me about a time when you encountered something you didn't understand at work. What did you do?",
                "purpose": "Assess learning response to gaps",
                "star_focus": "action",
            },
            {
                "question": "Describe a situation where you went beyond what was required to learn something new.",
                "purpose": "Evaluate intrinsic motivation to learn",
                "star_focus": "action",
            },
            {
                "question": "Tell me about a time you questioned an established process or assumption.",
                "purpose": "Assess willingness to challenge status quo",
                "star_focus": "situation",
            },
        ],
        "follow_up_probes": {
            "situation": [
                "What was the context that led to this?",
                "What was happening in the organization at that time?",
            ],
            "task": [
                "What specifically was your responsibility?",
                "What were you trying to achieve?",
            ],
            "action": [
                "Walk me through the specific steps you took.",
                "How did you approach learning about this?",
                "What resources did you seek out?",
            ],
            "result": [
                "What was the outcome of your exploration?",
                "How did this new knowledge impact your work?",
                "What did you learn from this experience?",
            ],
        },
        "star_indicators": {
            "situation": ["context of the knowledge gap", "trigger for curiosity"],
            "task": ["learning goal", "understanding objective"],
            "action": ["research methods", "questions asked", "sources consulted"],
            "result": ["knowledge gained", "application of learning", "impact on work"],
        },
    },
    {
        "trait_name": "Adaptability",
        "name": "Adaptability Assessment Rubric",
        "description": "Research-based rubric for assessing flexibility and response to change.",
        "behavioral_anchors": {
            "1": {
                "label": "Rigid",
                "description": "Strongly resists change. Becomes ineffective when plans change. Unable to adjust approach even when current approach isn't working.",
                "indicators": [
                    "Refuses to deviate from original plan",
                    "Becomes visibly frustrated with change",
                    "Performance drops significantly with change",
                    "Complains about new requirements",
                ],
            },
            "2": {
                "label": "Reluctantly Adapts",
                "description": "Eventually adapts but with difficulty. Needs significant support during transitions. Slow to embrace new approaches.",
                "indicators": [
                    "Requires convincing before adapting",
                    "Takes extended time to adjust",
                    "Needs reassurance during change",
                ],
            },
            "3": {
                "label": "Adequately Adaptable",
                "description": "Adjusts to change when necessary. Maintains performance through moderate changes. Accepts new approaches with reasonable grace.",
                "indicators": [
                    "Adjusts when change is explained",
                    "Maintains baseline performance",
                    "Shows willingness to try new things",
                    "Recovers from setbacks",
                ],
            },
            "4": {
                "label": "Highly Adaptable",
                "description": "Embraces change as opportunity. Quickly adjusts approach based on new information. Helps others navigate change.",
                "indicators": [
                    "Proactively adjusts to signals",
                    "Maintains or improves performance",
                    "Seeks feedback to calibrate",
                    "Supports team through transitions",
                ],
            },
            "5": {
                "label": "Exceptionally Adaptable",
                "description": "Thrives in constant change. Anticipates need to adapt. Leads others through uncertainty. Turns change into competitive advantage.",
                "indicators": [
                    "Anticipates and prepares for change",
                    "Excels in ambiguous environments",
                    "Models adaptability for others",
                    "Creates structures for continuous adaptation",
                ],
            },
        },
        "primary_probes": [
            {
                "question": "Tell me about a time when your project or priorities changed significantly mid-stream. How did you handle it?",
                "purpose": "Assess response to unexpected change",
                "star_focus": "action",
            },
            {
                "question": "Describe a situation where you had to quickly learn a new skill or approach to complete a task.",
                "purpose": "Evaluate learning agility",
                "star_focus": "action",
            },
            {
                "question": "Tell me about a time when your initial approach wasn't working. What did you do?",
                "purpose": "Assess willingness to pivot",
                "star_focus": "action",
            },
        ],
        "follow_up_probes": {
            "situation": [
                "What changed and why?",
                "How much notice did you have?",
            ],
            "task": [
                "What was expected of you in the new situation?",
                "What did you need to accomplish despite the change?",
            ],
            "action": [
                "How did you adjust your approach?",
                "What was your thought process?",
                "What did you do differently?",
            ],
            "result": [
                "What was the outcome?",
                "What did you learn about handling change?",
                "How did this affect future similar situations?",
            ],
        },
        "star_indicators": {
            "situation": ["nature of change", "degree of disruption", "timeline"],
            "task": ["new requirements", "adjusted goals"],
            "action": ["adjustment strategies", "mindset shift", "new behaviors"],
            "result": ["performance outcome", "lessons learned", "improved flexibility"],
        },
    },
    {
        "trait_name": "Collaboration",
        "name": "Collaboration Assessment Rubric",
        "description": "Research-based rubric for assessing teamwork and cooperative working style.",
        "behavioral_anchors": {
            "1": {
                "label": "Non-collaborative",
                "description": "Strongly prefers solo work. Actively avoids team interactions. May undermine team efforts. Takes credit for shared work.",
                "indicators": [
                    "Works in isolation by choice",
                    "Dismisses others' contributions",
                    "Creates friction in teams",
                    "Hoards information",
                ],
            },
            "2": {
                "label": "Minimally Collaborative",
                "description": "Participates in teamwork when required but doesn't contribute beyond minimum. Passive in group settings.",
                "indicators": [
                    "Attends but doesn't engage",
                    "Does only assigned portion",
                    "Rarely offers help to others",
                ],
            },
            "3": {
                "label": "Adequately Collaborative",
                "description": "Works effectively with others when needed. Shares information appropriately. Respects team processes and decisions.",
                "indicators": [
                    "Contributes fair share",
                    "Shares information when asked",
                    "Participates in team discussions",
                    "Supports team decisions",
                ],
            },
            "4": {
                "label": "Strong Collaborator",
                "description": "Actively seeks collaboration. Builds relationships across teams. Shares credit generously. Helps teammates succeed.",
                "indicators": [
                    "Proactively reaches out to others",
                    "Shares information freely",
                    "Recognizes others' contributions",
                    "Offers help without being asked",
                ],
            },
            "5": {
                "label": "Exceptional Collaborator",
                "description": "Elevates team performance. Creates collaborative culture. Bridges divides between groups. Enables others' best work.",
                "indicators": [
                    "Creates cross-functional connections",
                    "Facilitates productive disagreement",
                    "Models collaborative behavior",
                    "Multiplies team effectiveness",
                ],
            },
        },
        "primary_probes": [
            {
                "question": "Tell me about a project where success depended on working closely with others. How did you approach the collaboration?",
                "purpose": "Assess collaborative approach",
                "star_focus": "action",
            },
            {
                "question": "Describe a time when you helped a colleague succeed at something.",
                "purpose": "Evaluate supportive behaviors",
                "star_focus": "action",
            },
            {
                "question": "Tell me about a time when you had to work with someone whose style was very different from yours.",
                "purpose": "Assess flexibility in collaboration",
                "star_focus": "action",
            },
        ],
        "follow_up_probes": {
            "situation": [
                "Who was involved in this collaboration?",
                "What was the team dynamic?",
            ],
            "task": [
                "What was the shared goal?",
                "What was your specific role in the team?",
            ],
            "action": [
                "How did you coordinate with others?",
                "How did you handle differences of opinion?",
                "What did you do to support the team?",
            ],
            "result": [
                "What was the outcome for the team?",
                "What feedback did you receive from teammates?",
                "What did you learn about working with others?",
            ],
        },
        "star_indicators": {
            "situation": ["team composition", "collaboration context"],
            "task": ["shared objective", "individual responsibility"],
            "action": ["communication methods", "coordination strategies", "conflict resolution"],
            "result": ["team outcome", "relationship quality", "lessons learned"],
        },
    },
    {
        "trait_name": "Initiative",
        "name": "Initiative Assessment Rubric",
        "description": "Research-based rubric for assessing proactive behavior and self-starting tendency.",
        "behavioral_anchors": {
            "1": {
                "label": "Passive",
                "description": "Waits to be told what to do. Never acts without explicit direction. Misses obvious opportunities for action.",
                "indicators": [
                    "Only does what's explicitly assigned",
                    "Waits for problems to be assigned",
                    "Never suggests improvements",
                    "Requires constant direction",
                ],
            },
            "2": {
                "label": "Reactive",
                "description": "Responds to problems when they arise but doesn't anticipate. Occasionally takes action beyond requirements when prompted.",
                "indicators": [
                    "Addresses problems after noticing",
                    "Sometimes goes beyond minimum",
                    "Needs hints to take initiative",
                ],
            },
            "3": {
                "label": "Moderately Proactive",
                "description": "Takes action on obvious opportunities. Identifies and solves problems in their area. Occasionally suggests improvements.",
                "indicators": [
                    "Identifies problems in own area",
                    "Acts on clear opportunities",
                    "Suggests improvements when obvious",
                    "Self-manages well",
                ],
            },
            "4": {
                "label": "Highly Proactive",
                "description": "Anticipates problems and acts to prevent them. Regularly identifies opportunities for improvement. Drives projects forward without being asked.",
                "indicators": [
                    "Anticipates and prevents problems",
                    "Creates new opportunities",
                    "Volunteers for challenges",
                    "Drives progress independently",
                ],
            },
            "5": {
                "label": "Entrepreneurial",
                "description": "Exceptional self-starter. Creates value beyond role boundaries. Initiates strategic improvements. Inspires initiative in others.",
                "indicators": [
                    "Creates entirely new initiatives",
                    "Identifies strategic opportunities",
                    "Takes calculated risks",
                    "Mobilizes others to action",
                ],
            },
        },
        "primary_probes": [
            {
                "question": "Tell me about a time when you identified a problem or opportunity that others hadn't noticed. What did you do?",
                "purpose": "Assess proactive problem identification",
                "star_focus": "action",
            },
            {
                "question": "Describe a situation where you took on something beyond your normal responsibilities.",
                "purpose": "Evaluate ownership and drive",
                "star_focus": "action",
            },
            {
                "question": "Tell me about a project or initiative you started on your own.",
                "purpose": "Assess self-starting behavior",
                "star_focus": "action",
            },
        ],
        "follow_up_probes": {
            "situation": [
                "What made you notice this opportunity?",
                "What was the organizational context?",
            ],
            "task": [
                "What did you decide needed to be done?",
                "How did you define the scope?",
            ],
            "action": [
                "How did you get started?",
                "What obstacles did you face and how did you overcome them?",
                "How did you get buy-in from others?",
            ],
            "result": [
                "What was the impact of your initiative?",
                "How was it received by others?",
                "What would you do differently?",
            ],
        },
        "star_indicators": {
            "situation": ["opportunity/problem identified", "context"],
            "task": ["self-defined objective", "scope determination"],
            "action": ["steps taken without direction", "obstacles overcome", "resources marshaled"],
            "result": ["impact achieved", "recognition received", "lessons learned"],
        },
    },
    {
        "trait_name": "Resilience",
        "name": "Resilience Assessment Rubric",
        "description": "Research-based rubric for assessing recovery from setbacks and persistence.",
        "behavioral_anchors": {
            "1": {
                "label": "Fragile",
                "description": "Deeply affected by setbacks. Takes extended time to recover. May give up after failure. Avoids risk due to fear of failure.",
                "indicators": [
                    "Extended recovery from setbacks",
                    "Avoids challenging situations",
                    "Gives up easily when things get hard",
                    "Dwells on failures",
                ],
            },
            "2": {
                "label": "Slow to Recover",
                "description": "Eventually recovers but with difficulty. Setbacks impact performance for extended periods. Needs support to bounce back.",
                "indicators": [
                    "Visible impact from setbacks",
                    "Needs encouragement to continue",
                    "Performance dips after failures",
                ],
            },
            "3": {
                "label": "Adequately Resilient",
                "description": "Recovers from normal setbacks in reasonable time. Maintains baseline performance through difficulties. Learns from failures.",
                "indicators": [
                    "Recovers within expected timeframe",
                    "Maintains performance through challenges",
                    "Reflects on failures productively",
                    "Doesn't take setbacks personally",
                ],
            },
            "4": {
                "label": "Highly Resilient",
                "description": "Quick recovery from setbacks. Uses failures as learning opportunities. Maintains optimism through challenges. Supports others' resilience.",
                "indicators": [
                    "Rapid recovery",
                    "Actively learns from failure",
                    "Maintains positive outlook",
                    "Helps others through setbacks",
                ],
            },
            "5": {
                "label": "Exceptionally Resilient",
                "description": "Thrives through adversity. Transforms setbacks into opportunities. Demonstrates anti-fragility. Models resilience for others.",
                "indicators": [
                    "Grows stronger through challenges",
                    "Transforms failures into opportunities",
                    "Inspires resilience in others",
                    "Maintains effectiveness under sustained pressure",
                ],
            },
        },
        "primary_probes": [
            {
                "question": "Tell me about the biggest professional setback or failure you've experienced. How did you handle it?",
                "purpose": "Assess response to significant failure",
                "star_focus": "action",
            },
            {
                "question": "Describe a time when you had to persist through repeated obstacles to achieve something.",
                "purpose": "Evaluate persistence and determination",
                "star_focus": "action",
            },
            {
                "question": "Tell me about a time when you received critical feedback that was hard to hear. How did you respond?",
                "purpose": "Assess response to criticism",
                "star_focus": "action",
            },
        ],
        "follow_up_probes": {
            "situation": [
                "What was the nature of the setback?",
                "What made it particularly challenging?",
            ],
            "task": [
                "What did you need to accomplish despite the setback?",
                "What were the stakes?",
            ],
            "action": [
                "How did you process the setback?",
                "What did you do to recover?",
                "How did you maintain your effectiveness?",
            ],
            "result": [
                "What was the ultimate outcome?",
                "What did you learn from the experience?",
                "How did it affect how you handle setbacks now?",
            ],
        },
        "star_indicators": {
            "situation": ["nature of setback", "severity", "context"],
            "task": ["recovery goal", "ongoing responsibilities"],
            "action": ["coping strategies", "recovery steps", "mindset management"],
            "result": ["recovery outcome", "lessons learned", "growth achieved"],
        },
    },
    {
        "trait_name": "Communication",
        "name": "Communication Assessment Rubric",
        "description": "Research-based rubric for assessing communication clarity and effectiveness (derived from Collaboration trait).",
        "behavioral_anchors": {
            "1": {
                "label": "Poor Communicator",
                "description": "Unclear and confusing communication. Fails to adapt to audience. Creates misunderstandings regularly.",
                "indicators": [
                    "Messages frequently misunderstood",
                    "Unable to explain complex ideas",
                    "Doesn't listen to others",
                    "Inappropriate communication style",
                ],
            },
            "2": {
                "label": "Developing Communicator",
                "description": "Basic communication skills but inconsistent. Sometimes clear, sometimes confusing. Limited adaptation to audience.",
                "indicators": [
                    "Occasionally unclear",
                    "Limited range of communication styles",
                    "Sometimes misses key information",
                ],
            },
            "3": {
                "label": "Competent Communicator",
                "description": "Generally clear and effective communication. Adapts to most audiences. Listens and responds appropriately.",
                "indicators": [
                    "Clear written and verbal communication",
                    "Adapts to different audiences",
                    "Active listener",
                    "Appropriate level of detail",
                ],
            },
            "4": {
                "label": "Strong Communicator",
                "description": "Highly effective across communication modes. Skilled at adapting to diverse audiences. Excellent at explaining complex topics.",
                "indicators": [
                    "Consistently clear and compelling",
                    "Masterful adaptation to audience",
                    "Explains complex ideas simply",
                    "Skilled at difficult conversations",
                ],
            },
            "5": {
                "label": "Exceptional Communicator",
                "description": "Outstanding communication in all contexts. Inspires and influences through communication. Creates shared understanding effortlessly.",
                "indicators": [
                    "Inspires through communication",
                    "Navigates highly sensitive topics",
                    "Creates alignment across groups",
                    "Coaches others in communication",
                ],
            },
        },
        "primary_probes": [
            {
                "question": "Tell me about a time you had to explain something complex to someone without technical background.",
                "purpose": "Assess adaptation to audience",
                "star_focus": "action",
            },
            {
                "question": "Describe a situation where there was a miscommunication that led to problems. How did you handle it?",
                "purpose": "Evaluate communication problem-solving",
                "star_focus": "action",
            },
            {
                "question": "Tell me about a difficult conversation you had to have with a colleague or stakeholder.",
                "purpose": "Assess handling of challenging communication",
                "star_focus": "action",
            },
        ],
        "follow_up_probes": {
            "situation": [
                "Who was the audience?",
                "What made this communication challenging?",
            ],
            "task": [
                "What did you need to communicate?",
                "What outcome were you trying to achieve?",
            ],
            "action": [
                "How did you prepare your message?",
                "How did you adapt to the audience?",
                "How did you handle questions or confusion?",
            ],
            "result": [
                "Was your message understood?",
                "What was the outcome?",
                "What did you learn about effective communication?",
            ],
        },
        "star_indicators": {
            "situation": ["communication context", "audience", "challenge"],
            "task": ["communication objective", "desired outcome"],
            "action": ["preparation", "delivery approach", "adaptation"],
            "result": ["understanding achieved", "outcome", "lessons learned"],
        },
    },
]
