import csv
import json

import pytest

from src.fin_debate_failure.data import load_companies
from src.fin_debate_failure.debate import ROLES, run_question
from src.fin_debate_failure.inference import VLLM
from src.fin_debate_failure.sweep import comparison_rows, main
from src.fin_debate_failure.tests.test_smoke import FakeChat


def test_multiple_samples_share_frozen_history_and_have_distinct_seeds():
    evidence = load_companies(rows=1)[0][0]['evidence']
    chat = FakeChat()
    rows = list(run_question(evidence, 'core_holding', chat, rounds=2, generations=2))
    assert len(rows) == 18
    assert len({r['RequestSeed'] for r in rows}) == 18
    for index, (prompt, _, _) in enumerate(chat.calls):
        if index < 6:
            continue
        previous = json.loads(prompt[1]['content'].splitlines()[-1])
        assert len(previous) == 6
        start = 0 if index < 12 else 6
        assert {p['Answer']['Reasoning'] for p in previous} == {f'marker_{i}' for i in range(start, start + 6)}
    one = list(run_question(evidence, 'core_holding', FakeChat(), rounds=0))
    assert [r['RequestSeed'] for r in one] == [r['RequestSeed'] for r in rows[:6] if r['Generation'] == 1]


def test_round_vote_uses_all_samples_and_requires_strict_majority():
    answers = [{'AgentRole': role, 'Generation': generation, 'Verdict': 'YES' if generation == 1 else 'NO',
                'Reasoning': role, 'ResponseStatus': 'ok'} for role in ROLES for generation in (1, 2)]
    rows = list(comparison_rows(answers, ROLES, 2, {}))
    assert len(rows) == 2 and all(r['DebateDecision'] == 'NO_MAJORITY' for r in rows)
    answers[-1]['Verdict'] = 'YES'
    assert all(r['DebateDecision'] == 'YES' for r in comparison_rows(answers, ROLES, 2, {}))
    answers[-1]['ResponseStatus'] = 'parse_error'
    assert all(r['DebateDecision'] == 'INCOMPLETE' for r in comparison_rows(answers, ROLES, 2, {}))


def test_grid_writes_all_decisions_and_no_evaluation(monkeypatch, tmp_path):
    chat = FakeChat()
    monkeypatch.setattr(VLLM, 'check', lambda self: {'data': [{'id': self.model}]})
    monkeypatch.setattr(VLLM, 'chat', lambda self, *args: chat(*args))
    output = main(['--rows', '1', '--rounds', '1', '2', '--generations', '1', '2',
                   '--output', str(tmp_path / 'grid')])
    assert len(chat.calls) == 270
    with (output / 'decisions.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 90
    assert len({r['RunID'] for r in rows}) == 8
    assert all(r['fundamental_Reasoning'] and r['trading_Reasoning'] and r['challenger_Reasoning'] for r in rows)
    assert all(r['IsFinalRound'] == str(r['Round'] == r['DebateRounds']) for r in rows)
    assert {r['IdentityMode'] for r in rows} == {'fake_ticker', 'real_name'}
    manifest = json.loads((output / 'manifest.json').read_text())
    assert manifest['planned_calls'] == manifest['attempted_calls'] == 270
    assert not (output / 'summary.json').exists()


def test_transport_failure_preserves_partial_round(monkeypatch, tmp_path):
    monkeypatch.setattr(VLLM, 'check', lambda self: {})
    def fail(*args):
        raise RuntimeError('offline')
    monkeypatch.setattr(VLLM, 'chat', fail)
    output = tmp_path / 'failure'
    with pytest.raises(SystemExit):
        main(['--rows', '1', '--output', str(output)])
    with (output / 'decisions.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert rows[0]['DebateDecision'] == 'INCOMPLETE'
    assert rows[0]['fundamental_Status'] == 'transport_error'
    assert rows[0]['trading_Status'] == 'not_generated'
    assert json.loads((output / 'manifest.json').read_text())['status'] == 'failed'


@pytest.mark.parametrize('args', [['--rounds', '-1'], ['--generations', '0'], ['--rounds', '1', '1']])
def test_invalid_grid_is_rejected(args, tmp_path):
    with pytest.raises(SystemExit):
        main([*args, '--dry-run', '--output', str(tmp_path / 'invalid')])
    assert not (tmp_path / 'invalid').exists()
