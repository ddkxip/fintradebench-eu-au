"""Round order. Each debate round reads only the completed previous round."""

import hashlib
from itertools import product

from .protocol import ROLE_INSTRUCTIONS, answer_schema, messages, parse_answer

ROLES = tuple(ROLE_INSTRUCTIONS)


def run_question(evidence, question_type, chat, rounds=1,
                 self_revision=False, seed=17, agents=ROLES, on_start=None, generations=1):
    if type(rounds) is not int or rounds < 0:
        raise ValueError("rounds must be a nonnegative integer")
    if type(generations) is not int or generations < 1:
        raise ValueError("generations must be a positive integer")
    prior = {}
    histories = {}
    stages = [("baseline", 0)] + [("debate", r) for r in range(1, rounds + 1)]
    if self_revision:
        stages += [("self_revision", r) for r in range(1, rounds + 1)]
    for condition, round_id in stages:
        if round_id:
            parent = "baseline" if round_id == 1 else condition
            prior = histories[(parent, round_id - 1)]
        current = {}
        for role, generation in product(agents, range(1, generations + 1)):
            if on_start is not None:
                on_start(condition, round_id, role)
            if round_id and len(prior) != len(agents) * generations:
                yield {"AgentRole": role, "Condition": condition, "Round": round_id, "Generation": generation,
                       "ResponseStatus": "skipped_previous_round_error", "RawResponse": ""}
                continue
            key = f"{seed}:{evidence['FakeTicker']}:{question_type}:{role}:{round_id}"
            if generation > 1:
                key += f":generation:{generation}"
            request_seed = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16) % (2**31)
            previous = None
            if round_id:
                peers = [p for p in agents if p != role] if condition == "debate" else []
                if request_seed % 2:
                    peers.reverse()
                previous = [{"AgentRole": p, "Generation": g, "Answer": prior[(p, g)]}
                            for p in [role, *peers] for g in range(1, generations + 1)]
            prompt = messages(evidence, question_type, role, previous)
            result = {"AgentRole": role, "Condition": condition, "Round": round_id, "Generation": generation,
                      "RawResponse": "", "ResponseStatus": "ok", "RequestSeed": request_seed,
                      "Messages": prompt}
            try:
                reply = chat(prompt, answer_schema(question_type, role), request_seed)
            except RuntimeError as exc:
                result.update(ResponseStatus="transport_error", Error=str(exc))
                yield result  # Save the failed request before stopping the run.
                raise
            choice = reply["choices"][0]
            raw = choice["message"].get("content") or ""
            result.update(RawResponse=raw, ProviderResponse=reply)
            if choice.get("finish_reason") != "stop":
                result["ResponseStatus"] = "truncated" if choice.get("finish_reason") == "length" else "incomplete"
            else:
                try:
                    answer = parse_answer(raw, question_type, role)
                    result.update(answer)
                    current[(role, generation)] = answer
                except (ValueError, TypeError) as exc:
                    result["ResponseStatus"] = "parse_error"
                    result["Error"] = str(exc)
            yield result
        histories[(condition, round_id)] = current
