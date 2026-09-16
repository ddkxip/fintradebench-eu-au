"""All prompts, answer choices, and response parsing."""

import json

# Raw evidence is split by role. Peer answers remain shared during debate.
FUNDAMENTAL_FIELDS = (
    "PE_Ratio", "PB_Ratio", "PS_Ratio", "EV_EBITDA", "Sector_PE",
    "Fundamental_Quarter_Date",
)
TRADING_FIELDS = (
    "RSI_14", "SMA_50", "Price_to_SMA50", "PriceVsSMA50_Percent",
    "Volume_to_AvgVol20", "Close_Price", "Volume",
)
ROLE_FIELDS = {
    "fundamental": FUNDAMENTAL_FIELDS,
    "trading": TRADING_FIELDS,
    "challenger": FUNDAMENTAL_FIELDS + TRADING_FIELDS,
}

QUESTION_TEMPLATES = {
    'valuation_forcing': (
        'Based on the data available to you, does {ticker} look attractively priced, '
        'fairly priced, or expensive right now — and specifically why?'
    ),
    'core_holding': (
        'Is {ticker} a good core holding for a 3–5 year investment thesis, based on '
        'the information available to you?'
    ),
    'confidence_falsifiability': (
        'How confident are you in your BUY/SELL/HOLD call on {ticker} right now, on a '
        'rough scale from low to high, and what specific piece of missing information '
        'would most change your mind?'
    ),
}

ROLE_INSTRUCTIONS = {
    'fundamental': (
        'You are the fundamental analyst. Base your recommendation only on the '
        'fundamental fields in your Data. Do not use trading signals as evidence. '
        'Assess the supplied valuation multiples. Compare P/E with sector P/E only '
        'when both are available. Do not invent benchmarks, growth, or cash flows. '
        'During debate, respond to challenges about fundamentals and stay in your role.'
    ),
    'trading': (
        'You are the trading-signal analyst. Prioritize price, trend, momentum, and '
        'volume. Base your recommendation only on the trading fields in your Data. '
        'Do not use valuation multiples or business facts as evidence. '
        'During debate, respond to challenges about signals and stay in your role. '
        'For the valuation question, explicitly discuss price relative to the '
        '50-day moving average and the volume ratio. Distinguish technical '
        'positioning from intrinsic valuation and short-term signals from evidence '
        'for a 3–5 year thesis. Cite supplied numbers without inventing missing ones.'
    ),
    'challenger': (
        'You are the challenger analyst. You receive both fundamental and trading '
        'data. At baseline, give an independent recommendation and identify its '
        'strongest counterargument. In each debate round, check the previous '
        'answers for calculation errors, claims unsupported by Data, and use of '
        'evidence outside each specialist role. Explain whether a correction '
        'changes your recommendation. Independently assess the strongest '
        'counterargument, unsupported assumptions, conflicting indicators, and '
        'missing evidence. Check numerical comparisons and whether the evidence '
        "matches the question's time horizon. Give your own verdict using the same "
        'choices as the other analysts. When peers are present, identify a specific '
        'claim to challenge, or explain why none needs challenging. Do not disagree '
        'merely to fulfill the role. You are not the final judge and do not see '
        'reference answers.'
    ),
}

COMMON_INSTRUCTION = (
    "Evaluate the supplied evidence for this research task. 'Right now' means the "
    'evidence snapshot date. Use only the '
    'supplied evidence; do not infer identities or introduce outside company facts. '
    'Give your own verdict and a concise evidence-based justification, including '
    'relevant limitations. Treat peer answers as claims to check against the '
    'data available to your role. Peer claims are not verified data. Agreement is '
    'not required. You must select one of the listed recommendations even when '
    'evidence is limited. State uncertainty in your justification; do not abstain '
    'or invent facts to justify your choice. HOLD means maintain the position. '
    'Return only the requested JSON object. Verdict is your specific recommendation. '
    'Reasoning means a concise justification, not a '
    'private reasoning trace.'
)

VERDICT_SPACES = {
    'valuation_forcing': ('ATTRACTIVELY_PRICED', 'FAIRLY_PRICED', 'EXPENSIVE'),
    'core_holding': ('YES', 'NO'),
    'confidence_falsifiability': ('BUY', 'SELL', 'HOLD'),
}

OUTPUT_INSTRUCTION = (
    "Return JSON with Verdict, Reasoning, Confidence, MissingInformation, "
    "CitedIndicators, and ChallengeTarget. Keep Reasoning under 180 words. "
    "CitedIndicators lists only indicator names in your own Data. ChallengeTarget is "
    "a specific peer claim you challenge, or null. For the confidence question, "
    "give Confidence as LOW, MEDIUM, or HIGH, and MissingInformation as a specific "
    "missing fact. For the other questions, set those two fields to null. "
    "If sector P/E or another value is missing, say so; never invent it."
)
REVISION_INSTRUCTION = (
    "Review the previous answers below against the original evidence. "
    "Keep or change your verdict and explain why. Agreement is not required."
)

RESPONSE_COLUMNS = (
    "FakeTicker", "QuestionType", "Question", "AgentRole", "Config", "Verdict",
    "Reasoning", "RawResponse", "Condition", "Round", "Seed", "Model",
    "Confidence", "MissingInformation", "CitedIndicators", "ChallengeTarget",
    "ResponseStatus", "IdentityMentions", "IdentityMode", "CompanyName",
)


def display_name(evidence):
    return evidence.get("CompanyName", evidence["FakeTicker"])


def messages(evidence, question_type, role, previous=None):
    question = QUESTION_TEMPLATES[question_type].format(ticker=display_name(evidence))
    visible = {key: evidence[key] for key in (
        "FakeTicker", "CompanyName", "SnapshotDate", *ROLE_FIELDS[role]) if key in evidence}
    system = COMMON_INSTRUCTION
    if "CompanyName" in visible:
        visible.pop("FakeTicker")  # Retained internally only for pairing and seeds.
    user = f"Question: {question}\nData: {json.dumps(visible)}\n"
    user += f"Verdict choices: {', '.join(VERDICT_SPACES[question_type])}.\n"
    user += OUTPUT_INSTRUCTION
    if previous is not None:
        user += "\n" + REVISION_INSTRUCTION + "\n" + json.dumps(previous)
    return [
        {"role": "system", "content": system + " " + ROLE_INSTRUCTIONS[role]},
        {"role": "user", "content": user},
    ]


def answer_schema(question_type, role=None):
    confidence = question_type == "confidence_falsifiability"
    properties = {
        "Verdict": {"type": "string", "enum": list(VERDICT_SPACES[question_type])},
        "Reasoning": {"type": "string", "minLength": 1},
        "Confidence": {"type": "string" if confidence else "null",
                       "enum": ["LOW", "MEDIUM", "HIGH"] if confidence else [None]},
        "MissingInformation": {"type": "string", "minLength": 1} if confidence else {"type": "null"},
        "CitedIndicators": {"type": "array", "items": {"type": "string"}},
        "ChallengeTarget": {"type": ["string", "null"]},
    }
    if role is not None:
        properties["CitedIndicators"]["items"]["enum"] = list(ROLE_FIELDS[role])
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}


def parse_answer(raw, question_type, role=None):
    answer = json.loads(raw)
    schema = answer_schema(question_type, role)
    if not isinstance(answer, dict) or set(answer) != set(schema["required"]):
        raise ValueError("Wrong answer fields")
    for key, rule in schema["properties"].items():
        value = answer[key]
        if "enum" in rule and value not in rule["enum"]:
            raise ValueError(f"Invalid {key}")
        kind = rule.get("type")
        if kind == "string" and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"Invalid {key}")
        if kind == "null" and value is not None:
            raise ValueError(f"Expected null {key}")
        if kind == "array" and (not isinstance(value, list) or not all(isinstance(v, str) for v in value)):
            raise ValueError(f"Invalid {key}")
        if kind == "array" and "enum" in rule["items"]:
            if any(v not in rule["items"]["enum"] for v in value):
                raise ValueError(f"Invalid {key} for {role}")
        if kind == ["string", "null"] and value is not None and not isinstance(value, str):
            raise ValueError(f"Invalid {key}")
    return answer
