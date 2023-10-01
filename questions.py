questions = [
    {
        "question_type": "multiple choice",
        "question": "What is Caribbean Airlines newest product?",
        "answers": [
            "Caribbean Vacations",
            "Caribbean Cafe",
            "Caribbean Notifications",
            "Caribbean Upgrade",
        ],
        "correct_answer": ["Caribbean Vacations"],
        "parameters": {
            "discrimination": 0.25,  # How well does this question identify skilled candidates
            "difficulty": 0.75,  # How difficult is the question
            "pseudo-guessing": 0.25,  # Probability that an individual with low-proficiency, answers correctly
            "upper-asymptote": 0.75,  # Probability that high proficiency individuals answer incorrectly
            "item-count": 0,
        },
    },
    {
        "question_type": "multiple choice",
        "question": "What is the usual model of aircraft that flies to Tobago?",
        "answers": ["ATR72-600", "Boeing 737-800", "Boeing 737-Max", "ATR-500"],
        "correct_answer": ["ATR72-600"],
        "parameters": {
            "discrimination": 0.20,
            "difficulty": 0.80,
            "pseudo-guessing": 0.20,
            "upper-asymptote": 0.80,
            "item-count": 0,
        },
    },
    {
        "question_type": "multiple choice",
        "question": "What is Caribbean Plus?",
        "answers": [
            "Extra Legroom",
            "Extra Food",
            "Larger Plane",
            "Free first class upgrade",
        ],
        "correct_answer": ["Extra Legroom"],
        "parameters": {
            "discrimination": 0.15,
            "difficulty": 0.80,
            "pseudo-guessing": 0.20,
            "upper-asymptote": 0.65,
            "item-count": 0,
        },
    },
    {
        "question_type": "multiple choice",
        "question": "How much discount do tertiary education students get on Caribbean Airlines?",
        "answers": ["10%", "5%", "15%", "No Discount"],
        "correct_answer": ["10%"],
        "parameters": {
            "discrimination": 0.10,
            "difficulty": 0.50,
            "pseudo-guessing": 0.40,
            "upper-asymptote": 0.25,
            "item-count": 0,
        },
    },
    {
        "question_type": "multiple choice",
        "question": "How many destinations does Caribbean Airlines fly to?",
        "answers": ["20", "12", "25", "17"],
        "correct_answer": ["20"],
        "parameters": {
            "discrimination": 0.10,
            "difficulty": 0.50,
            "pseudo-guessing": 0.40,
            "upper-asymptote": 0.25,
            "item-count": 0,
        },
    },
]
