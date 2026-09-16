"""Offline checks for masking, debate isolation, failures, and saved output."""

import csv
import io
import json

import pytest

from src.fin_debate_failure.__main__ import main
from src.fin_debate_failure.config import DEFAULT_CONFIG, load_config
from src.fin_debate_failure.data import load_companies
from src.fin_debate_failure.debate import ROLES, run_question
from src.fin_debate_failure.inference import VLLM
from src.fin_debate_failure.protocol import QUESTION_TEMPLATES, ROLE_FIELDS, answer_schema, messages, parse_answer
from src.fin_debate_failure.review import agent_behavior, final_answers, identity_mentions, round_answers


class FakeChat:
    def __init__(self):
        self.calls = []

    def __call__(self, prompt, schema, seed):
        number = len(self.calls)
        self.calls.append((prompt, schema, seed))
        confidence = schema["properties"]["Confidence"]["enum"][0]
        answer = {"Verdict": schema["properties"]["Verdict"]["enum"][0],
                  "Reasoning": f"marker_{number}", "Confidence": confidence,
                  "MissingInformation": "Sector P/E" if confidence else None,
                  "CitedIndicators": [schema["properties"]["CitedIndicators"]["items"]["enum"][0]],
                  "ChallengeTarget": None}
        return {"choices": [{"finish_reason": "stop", "message": {
            "content": json.dumps(answer), "reasoning": "PRIVATE_TRACE"}}]}


def test_workbook_masking_and_missing_values():
    companies, identities = load_companies(rows=20)
    assert len(companies) == 20
    assert [c["evidence"]["FakeTicker"] for c in companies[:5]] == ["UDAX", "IHHE", "XDVX", "RCSN", "BACG"]
    assert companies[2]["evidence"]["PB_Ratio"] is None
    assert companies[6]["evidence"]["PE_Ratio"] is None
    assert companies[0]["evidence"]["PriceVsSMA50_Percent"] == 2.82
    for company in companies:
        evidence = company["evidence"]
        assert not {"Ticker", "Company_Name", "Bucket"} & evidence.keys()
        for kind in QUESTION_TEMPLATES:
            for role in ROLES:
                prompt = json.dumps(messages(evidence, kind, role))
                assert not identity_mentions(prompt, identities)
                assert "Overvalued" not in prompt and "Undervalued" not in prompt


def test_debate_and_control_only_read_the_correct_baseline():
    company = load_companies(rows=1)[0][0]["evidence"]
    chat = FakeChat()
    rows = list(run_question(company, "valuation_forcing", chat, self_revision=True))
    assert len(rows) == 9
    for index, (prompt, _, _) in enumerate(chat.calls):
        text = json.dumps(prompt)
        assert "PRIVATE_TRACE" not in text
        expected = set() if index < 3 else {0, 1, 2} if index < 6 else {index - 6}
        assert {n for n in range(9) if f"marker_{n}" in text} == expected
    assert [r["RequestSeed"] for r in rows[3:6]] == [r["RequestSeed"] for r in rows[6:9]]


@pytest.mark.parametrize("failure", ["truncated", "parse_error"])
def test_bad_baseline_skips_dependent_rounds(failure):
    company = load_companies(rows=1)[0][0]["evidence"]
    chat = FakeChat()

    def broken(prompt, schema, seed):
        reply = chat(prompt, schema, seed)
        if len(chat.calls) == 1:
            if failure == "truncated":
                reply["choices"][0]["finish_reason"] = "length"
            else:
                reply["choices"][0]["message"]["content"] = "not JSON"
        return reply

    rows = list(run_question(company, "core_holding", broken))
    assert len(chat.calls) == 3
    assert rows[0]["ResponseStatus"] == failure
    assert "Verdict" not in rows[0]
    assert all(r["ResponseStatus"] == "skipped_previous_round_error" for r in rows[3:])


def test_vllm_request_uses_chat_schema_seed_and_final_content(monkeypatch):
    from src.fin_debate_failure import inference

    schema = answer_schema("core_holding")
    prompt = [{"role": "user", "content": "Example"}]

    def respond(request, timeout):
        payload = json.loads(request.data)
        assert request.full_url == "http://localhost:8000/v1/chat/completions"
        assert payload["messages"] == prompt and payload["seed"] == 17
        assert payload["response_format"]["json_schema"]["schema"] == schema
        assert payload["chat_template_kwargs"] == {"enable_thinking": False}
        assert payload["temperature"] == 0.4 and payload["max_tokens"] == 100
        return io.BytesIO(json.dumps({"choices": [{"message": {"content": "final"}}]}).encode())

    monkeypatch.setattr(inference, "urlopen", respond)
    client = VLLM("http://localhost:8000/v1", "test-model", 100, 30, False, {"temperature": 0.4})
    assert client.chat(prompt, schema, 17)["choices"][0]["message"]["content"] == "final"


def test_full_five_row_run_saves_90_grouped_answers(monkeypatch, tmp_path):
    chat = FakeChat()
    monkeypatch.setattr(VLLM, "check", lambda self: {"data": [{"id": self.model}]})
    monkeypatch.setattr(VLLM, "chat", lambda self, *args: chat(*args))
    output = tmp_path / "smoke"
    main(["--rows", "5", "--rounds", "1", "--output", str(output)])
    with (output / "responses.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(chat.calls) == 90
    assert all(row["ResponseStatus"] == "ok" for row in rows)
    for index in range(0, 90, 3):
        group = rows[index:index + 3]
        assert [row["AgentRole"] for row in group] == list(ROLES)
        assert len({(r["FakeTicker"], r["QuestionType"], r["Condition"]) for r in group}) == 1
    assert len((output / "calls.jsonl").read_text().splitlines()) == 90
    summary = json.loads((output / "summary.json").read_text())
    assert summary["identity_flagged_responses"] == 0
    assert summary["agreement"]["baseline_round_0"]["complete_groups"] == 15
    assert json.loads((output / "manifest.json").read_text())["status"] == "complete"


def test_transport_failure_is_saved_and_stops_the_run(monkeypatch, tmp_path):
    monkeypatch.setattr(VLLM, "check", lambda self: {"data": [{"id": self.model}]})

    def unavailable(self, *args):
        raise RuntimeError("Server unavailable")

    monkeypatch.setattr(VLLM, "chat", unavailable)
    output = tmp_path / "failed"
    with pytest.raises(SystemExit) as error:
        main(["--output", str(output)])
    assert error.value.code == 1
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["status"] == "failed"
    with (output / "responses.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1 and rows[0]["ResponseStatus"] == "transport_error"
    assert json.loads((output / "calls.jsonl").read_text())["Messages"]


def test_dry_run_never_calls_inference(monkeypatch, tmp_path):
    def forbidden(self):
        pytest.fail("Dry run contacted the server")

    monkeypatch.setattr(VLLM, "check", forbidden)
    output = tmp_path / "preview"
    main(["--dry-run", "--output", str(output)])
    assert len(json.loads((output / "prompts.json").read_text())) == 45
    assert not (output / "responses.csv").exists()


def test_three_debate_rounds_and_control_keep_separate_histories():
    company = load_companies(rows=1)[0][0]["evidence"]
    chat = FakeChat()
    agents = ["fundamental", "challenger"]
    rows = list(run_question(company, "core_holding", chat, rounds=3,
                             self_revision=True, agents=agents))
    assert len(rows) == len(chat.calls) == 14
    expected = [set(), set(), {0, 1}, {0, 1}, {2, 3}, {2, 3}, {4, 5}, {4, 5},
                {0}, {1}, {8}, {9}, {10}, {11}]
    for index, (prompt, _, _) in enumerate(chat.calls):
        assert "PRIVATE_TRACE" not in json.dumps(prompt)
        if index < 2:
            continue
        previous = json.loads(prompt[1]["content"].splitlines()[-1])
        assert {p["Answer"]["Reasoning"] for p in previous} == {f"marker_{n}" for n in expected[index]}
        assert all(p["AgentRole"] in agents for p in previous)
    assert [r["RequestSeed"] for r in rows[2:8]] == [r["RequestSeed"] for r in rows[8:]]


def test_error_in_debate_does_not_corrupt_the_control_or_create_a_final_verdict():
    company = load_companies(rows=1)[0][0]["evidence"]
    chat = FakeChat()

    def broken(prompt, schema, seed):
        reply = chat(prompt, schema, seed)
        if len(chat.calls) == 4:
            reply["choices"][0]["message"]["content"] = "not JSON"
        return reply

    rows = list(run_question(company, "core_holding", broken, rounds=3, self_revision=True))
    for row in rows:
        row.update(FakeTicker="UDAX", QuestionType="core_holding", Question="Example")
    assert len(rows) == 21 and len(chat.calls) == 15
    assert all(r["ResponseStatus"] == "skipped_previous_round_error" for r in rows[6:12])
    assert all(r["ResponseStatus"] == "ok" for r in rows[12:])
    result = final_answers(rows, ROLES, 3)[0]
    assert result["FinalStatus"] == "incomplete" and result["Verdict"] is None


@pytest.mark.parametrize("verdicts,status,verdict", [
    (["YES", "NO"], "no_majority", None),
    (["YES", "NO", "CONDITIONAL"], "no_majority", None),
    (["YES", "YES", "NO"], "majority", "YES"),
    (["INSUFFICIENT_DATA"] * 3, "majority", "INSUFFICIENT_DATA"),
])
def test_final_vote_preserves_disagreement(verdicts, status, verdict):
    agents = ROLES[:len(verdicts)]
    rows = [{"FakeTicker": "UDAX", "QuestionType": "core_holding", "Question": "Example",
             "AgentRole": role, "Verdict": vote, "Reasoning": role,
             "Condition": "debate", "Round": 3, "ResponseStatus": "ok"}
            for role, vote in zip(agents, verdicts)]
    result = final_answers(rows, agents, 3)[0]
    assert (result["FinalStatus"], result["Verdict"]) == (status, verdict)


def test_default_config_runs_three_rounds_and_exports_final_answers(monkeypatch, tmp_path):
    chat = FakeChat()
    monkeypatch.setattr(VLLM, "check", lambda self: {"data": [{"id": self.model}]})
    monkeypatch.setattr(VLLM, "chat", lambda self, *args: chat(*args))
    output = tmp_path / "three_rounds"
    main(["--output", str(output)])
    assert len(chat.calls) == 180
    with (output / "final_answers.csv").open(newline="") as file:
        finals = list(csv.DictReader(file))
    assert len(finals) == 15 and all(r["Round"] == "3" for r in finals)
    assert all(r["FinalStatus"] == "majority" for r in finals)
    confidence = next(r for r in finals if r["QuestionType"] == "confidence_falsifiability")
    assert all(a["Confidence"] == "LOW" and a["MissingInformation"] == "Sector P/E"
               for a in json.loads(confidence["AgentAnswers"]))
    with (output / "final_agent_answers.csv").open(newline="") as file:
        agents = list(csv.DictReader(file))
    assert len(agents) == 45 and all(r["Round"] == "3" for r in agents)
    summary = json.loads((output / "summary.json").read_text())
    assert len(summary["agreement"]) == 4
    assert all(stage["complete_groups"] == 15 for stage in summary["agreement"].values())
    with (output / "round_answers.csv").open(newline="") as file:
        checkpoints = list(csv.DictReader(file))
    assert len(checkpoints) == 60
    assert {r["Round"] for r in checkpoints} == {"0", "1", "2", "3"}
    assert all(r["OutcomeChanged"] == "False" for r in checkpoints if r["Round"] != "0")
    with (output / "agent_behavior.csv").open(newline="") as file:
        behavior = list(csv.DictReader(file))
    assert len(behavior) == 36
    assert all(r["ValidResponses"] == "5" and r["VerdictChanges"] == "0" for r in behavior)


def test_custom_config_agent_count_and_cli_override(monkeypatch, tmp_path):
    config = load_config()
    config.update(rows=1, agents=["fundamental", "challenger"], rounds=3, thinking=False)
    path = tmp_path / "experiment.json"
    path.write_text(json.dumps(config))
    chat = FakeChat()
    monkeypatch.setattr(VLLM, "check", lambda self: {"data": [{"id": self.model}]})
    monkeypatch.setattr(VLLM, "chat", lambda self, *args: chat(*args))
    output = tmp_path / "two_agents"
    main(["--config", str(path), "--rounds", "2", "--output", str(output)])
    assert len(chat.calls) == 18
    saved = json.loads((output / "manifest.json").read_text())
    assert saved["config"]["rounds"] == 2 and saved["config"]["thinking"] is False
    summary = json.loads((output / "summary.json").read_text())
    assert summary["agreement"]["debate_round_2"]["complete_groups"] == 3
    assert summary["agreement"]["debate_round_2"]["committed_pairwise_agreement"] == 1


@pytest.mark.parametrize("change", [
    {"rounds": -1}, {"rounds": 1.5}, {"agents": []},
    {"agents": ["fundamental", "fundamental"]}, {"agents": ["unknown"]},
    {"agents": ["fundamental"]}, {"thinking": "false"}, {"identity_mode": "unknown"},
])
def test_bad_config_is_rejected(change, tmp_path):
    config = json.loads(DEFAULT_CONFIG.read_text())
    config.update(change)
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError):
        load_config(path)


def test_real_names_change_identity_but_preserve_data_and_question_templates():
    masked, identities = load_companies(rows=5)
    named, _ = load_companies(rows=5, identity_mode="real_name")
    for fake, real in zip(masked, named):
        evidence = real["evidence"]
        name = evidence["CompanyName"]
        assert {k: v for k, v in evidence.items() if k != "CompanyName"} == fake["evidence"]
        for kind, template in QUESTION_TEMPLATES.items():
            for role in ROLES:
                prompt = messages(evidence, kind, role)
                old_prompt = messages(fake["evidence"], kind, role)
                assert prompt[1]["content"].startswith("Question: " + template.format(ticker=name))
                visible = json.loads(prompt[1]["content"].split("Data: ", 1)[1].splitlines()[0])
                assert visible["CompanyName"] == name
                assert not {"FakeTicker", "Ticker", "Bucket"} & visible.keys()
                assert evidence["FakeTicker"] not in json.dumps(prompt)
                assert prompt[0]["content"] == old_prompt[0]["content"].replace(
                    "Company identifiers are pseudonyms. ", "")
                assert not identity_mentions(json.dumps(old_prompt), identities)


def test_identity_modes_use_paired_request_seeds():
    chats = []
    for mode in ("fake_ticker", "real_name"):
        evidence = load_companies(rows=1, identity_mode=mode)[0][0]["evidence"]
        chat = FakeChat()
        list(run_question(evidence, "valuation_forcing", chat, rounds=3))
        chats.append(chat)
    assert [call[2] for call in chats[0].calls] == [call[2] for call in chats[1].calls]


def test_real_name_run_records_mode_and_expected_name_mentions(monkeypatch, tmp_path):
    chat = FakeChat()
    monkeypatch.setattr(VLLM, "check", lambda self: {"data": [{"id": self.model}]})

    def named_reply(self, prompt, schema, seed):
        reply = chat(prompt, schema, seed)
        company = json.loads(prompt[1]["content"].split("Data: ", 1)[1].splitlines()[0])["CompanyName"]
        answer = json.loads(reply["choices"][0]["message"]["content"])
        answer["Reasoning"] = company + ": " + answer["Reasoning"]
        reply["choices"][0]["message"]["content"] = json.dumps(answer)
        return reply

    monkeypatch.setattr(VLLM, "chat", named_reply)
    output = tmp_path / "real_names"
    main(["--identity-mode", "real_name", "--rounds", "1", "--output", str(output)])
    with (output / "responses.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 90
    assert all(r["IdentityMode"] == "real_name" and r["CompanyName"] in r["Question"] for r in rows)
    assert rows[0]["CompanyName"] == "Apple Inc." and rows[0]["FakeTicker"] == "UDAX"
    with (output / "final_answers.csv").open(newline="") as file:
        finals = list(csv.DictReader(file))
    assert len(finals) == 15
    assert all(r["IdentityMode"] == "real_name" and r["CompanyName"] for r in finals)
    summary = json.loads((output / "summary.json").read_text())
    assert summary["identity_mode"] == "real_name"
    assert summary["identity_mention_responses"] == 90
    assert summary["identity_flagged_responses"] is None


def test_older_configs_default_to_fake_tickers(tmp_path):
    config = json.loads(DEFAULT_CONFIG.read_text())
    del config["identity_mode"]
    path = tmp_path / "older.json"
    path.write_text(json.dumps(config))
    assert load_config(path)["identity_mode"] == "fake_ticker"


@pytest.mark.parametrize("role", ROLES)
def test_role_data_is_filtered_in_every_round(role):
    evidence = load_companies(rows=1)[0][0]["evidence"]
    evidence["UnlistedSecret"] = "hidden"
    chat = FakeChat()
    rows = list(run_question(evidence, "valuation_forcing", chat, rounds=3))
    for row in rows:
        if row["AgentRole"] != role:
            continue
        visible = json.loads(row["Messages"][1]["content"].split("Data: ", 1)[1].splitlines()[0])
        assert set(visible) == {"FakeTicker", "SnapshotDate", *ROLE_FIELDS[role]}
        assert row["ResponseStatus"] == "ok"
        assert set(row["CitedIndicators"]) <= set(ROLE_FIELDS[role])
    assert set(evidence) > set(ROLE_FIELDS[role])  # Filtering never mutates shared evidence.


@pytest.mark.parametrize("kind", QUESTION_TEMPLATES)
def test_json_contract_requires_recommendation_and_rejects_abstention(kind):
    schema = answer_schema(kind, "fundamental")
    reply = FakeChat()([], schema, 17)
    answer = json.loads(reply["choices"][0]["message"]["content"])
    assert parse_answer(json.dumps(answer), kind, "fundamental") == answer
    for invalid in ("INSUFFICIENT_DATA", "LIMITED_INFORMATION", "CONDITIONAL", ""):
        with pytest.raises(ValueError):
            parse_answer(json.dumps({**answer, "Verdict": invalid}), kind, "fundamental")
    with pytest.raises(ValueError):
        parse_answer(json.dumps({**answer, "Reasoning": ""}), kind, "fundamental")
    with pytest.raises(ValueError):
        parse_answer(json.dumps({**answer, "CitedIndicators": ["RSI_14"]}), kind, "fundamental")
    with pytest.raises(ValueError):
        parse_answer(json.dumps({k: v for k, v in answer.items() if k != "Verdict"}), kind)


def test_checkpoints_and_agent_changes_handle_disagreement_and_failures():
    rows = []
    votes = [
        ["EXPENSIVE", "EXPENSIVE", "FAIRLY_PRICED"],
        ["EXPENSIVE", "FAIRLY_PRICED", "ATTRACTIVELY_PRICED"],
        ["FAIRLY_PRICED", "FAIRLY_PRICED", "FAIRLY_PRICED"],
        ["FAIRLY_PRICED", "FAIRLY_PRICED", None],
    ]
    for round_id, verdicts in enumerate(votes):
        for role, vote in zip(ROLES, verdicts):
            rows.append({"FakeTicker": "UDAX", "QuestionType": "valuation_forcing",
                         "Question": "Example", "AgentRole": role, "Round": round_id,
                         "Condition": "debate" if round_id else "baseline",
                         "Verdict": vote, "Reasoning": str(round_id),
                         "ResponseStatus": "ok" if vote else "parse_error"})
    checkpoints = round_answers(rows, ROLES, 3)
    assert [r["FinalStatus"] for r in checkpoints] == ["majority", "no_majority", "majority", "incomplete"]
    assert [r["OutcomeChanged"] for r in checkpoints] == [None, True, True, None]
    behavior = agent_behavior(rows)
    trading = next(r for r in behavior if r["AgentRole"] == "trading" and r["Round"] == 1)
    assert trading["VerdictChanges"] == trading["ComparablePreviousResponses"] == 1
    failed = next(r for r in behavior if r["AgentRole"] == "challenger" and r["Round"] == 3)
    assert failed["FailedResponses"] == 1 and failed["ComparablePreviousResponses"] == 0
