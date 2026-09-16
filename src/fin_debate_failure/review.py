"""Small review aids. Identity mentions are flags, not a memory-use verdict."""

import re
from collections import Counter, defaultdict
from itertools import combinations


def identity_mentions(text, identities):
    return sorted({name for name in identities
                   if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text,
                                flags=0 if name.isupper() else re.IGNORECASE)})


def summarize(rows, agents, identity_mode="fake_ticker"):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["FakeTicker"], row["QuestionType"], row["Condition"], row["Round"])].append(row)
    agreement = {}
    for condition, round_id in dict.fromkeys((r["Condition"], r["Round"]) for r in rows):
        complete = [group for key, group in groups.items() if key[2:] == (condition, round_id)
                    and len(group) == len(agents) and {r["AgentRole"] for r in group} == set(agents)
                    and all(r["ResponseStatus"] == "ok" for r in group)]
        committed = [group for group in complete if all(r["Verdict"] != "INSUFFICIENT_DATA" for r in group)]
        pairs = len(agents) * (len(agents) - 1) // 2
        agreement[f"{condition}_round_{round_id}"] = {
            "complete_groups": len(complete),
            "unanimous_groups": sum(len({r["Verdict"] for r in group}) == 1 for group in complete),
            "all_insufficient_data_groups": sum(all(r["Verdict"] == "INSUFFICIENT_DATA" for r in group) for group in complete),
            "committed_groups": len(committed),
            "committed_pairwise_agreement": (
                sum(a["Verdict"] == b["Verdict"] for group in committed for a, b in combinations(group, 2))
                / (pairs * len(committed)) if committed and pairs else None),
        }
    return {
        "responses": len(rows), "status_counts": dict(Counter(r["ResponseStatus"] for r in rows)),
        "agreement": agreement,
        "identity_mode": identity_mode,
        "identity_mention_responses": sum(bool(r["IdentityMentions"]) for r in rows),
        "identity_flagged_responses": (sum(bool(r["IdentityMentions"]) for r in rows)
                                       if identity_mode == "fake_ticker" else None),
        "hypothesis": "If we replace the real ticker with a fake one, the model will not respond from memory.",
        "conclusion": ("Human review needed. No identity mentions does not prove memory was not used."
                       if identity_mode == "fake_ticker" else
                       "Real names were supplied. Identity mentions are expected; compare supporting facts manually."),
    }


def final_answers(rows, agents, final_round):
    """One strict-majority result per question. Never fall back to an earlier round."""
    condition = "debate" if final_round else "baseline"
    groups = defaultdict(list)
    for row in rows:
        groups[(row["FakeTicker"], row["QuestionType"], row["Question"])].append(row)
    results = []
    for (ticker, kind, question), group in groups.items():
        final = [r for r in group if r["Condition"] == condition and r["Round"] == final_round]
        votes = Counter(r["Verdict"] for r in final if r["ResponseStatus"] == "ok")
        complete = (len(final) == len(agents) and {r["AgentRole"] for r in final} == set(agents)
                    and all(r["ResponseStatus"] == "ok" for r in final))
        majority = next((v for v, count in votes.items() if count > len(agents) / 2), None)
        results.append({
            "FakeTicker": ticker, "QuestionType": kind, "Question": question,
            "IdentityMode": group[0].get("IdentityMode", "fake_ticker"),
            "CompanyName": group[0].get("CompanyName"),
            "Config": "homogeneous", "Round": final_round,
            "Verdict": majority if complete else None,
            "FinalStatus": "incomplete" if not complete else "majority" if majority else "no_majority",
            "VoteCounts": dict(votes),
            "AgentAnswers": [{k: r.get(k) for k in (
                "AgentRole", "Verdict", "Reasoning", "Confidence", "MissingInformation",
                "CitedIndicators", "ChallengeTarget", "ResponseStatus")} for r in final],
        })
    return results


def round_answers(rows, agents, rounds):
    """Save the baseline and every debate checkpoint, with outcome changes."""
    results = []
    previous = {}
    for round_id in range(rounds + 1):
        for result in final_answers(rows, agents, round_id):
            key = (result["FakeTicker"], result["QuestionType"])
            prior = previous.get(key)
            comparable = (prior is not None and prior["FinalStatus"] != "incomplete"
                          and result["FinalStatus"] != "incomplete")
            result["PreviousVerdict"] = prior["Verdict"] if prior else None
            result["PreviousFinalStatus"] = prior["FinalStatus"] if prior else None
            result["OutcomeChanged"] = (
                (result["Verdict"], result["FinalStatus"]) !=
                (prior["Verdict"], prior["FinalStatus"]) if comparable else None)
            previous[key] = result
            results.append(result)
    return results


def agent_behavior(rows):
    """Descriptive counts by role, question, and stage. Changes do not imply quality."""
    lookup = {(r["FakeTicker"], r["QuestionType"], r["AgentRole"],
               r["Condition"], r["Round"]): r for r in rows}
    groups = defaultdict(list)
    for row in rows:
        groups[(row["AgentRole"], row["QuestionType"], row["Condition"], row["Round"])].append(row)
    results = []
    for (role, kind, condition, round_id), group in groups.items():
        valid = [r for r in group if r["ResponseStatus"] == "ok"]
        pairs = []
        for row in valid:
            parent = "baseline" if round_id == 1 else condition
            prior = lookup.get((row["FakeTicker"], kind, role, parent, round_id - 1))
            if prior and prior["ResponseStatus"] == "ok":
                pairs.append((prior, row))
        results.append({
            "AgentRole": role, "QuestionType": kind, "Condition": condition, "Round": round_id,
            "Responses": len(group), "ValidResponses": len(valid),
            "FailedResponses": len(group) - len(valid),
            "VerdictCounts": dict(Counter(r["Verdict"] for r in valid)),
            "ComparablePreviousResponses": len(pairs),
            "VerdictChanges": sum(a["Verdict"] != b["Verdict"] for a, b in pairs),
            "ReasoningChanges": sum(a["Reasoning"] != b["Reasoning"] for a, b in pairs),
            "ChallengeResponses": sum(bool(r.get("ChallengeTarget")) for r in valid),
        })
    return results
