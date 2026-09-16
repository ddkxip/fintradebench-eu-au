"""Run a parameter grid and save side-by-side decisions without evaluation."""

import argparse
import csv
import hashlib
import json
from collections import Counter
from dataclasses import fields
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

from .config import DEFAULT_CONFIG, load_config
from .data import load_companies
from .debate import run_question
from .inference import VLLM
from .progress import Progress
from .protocol import QUESTION_TEMPLATES, display_name

DEFAULT_SWEEP = Path(__file__).with_name("sweep.json")


def comparison_rows(answers, agents, generations, metadata):
    """One row per generation; the round vote includes every agent sample."""
    lookup = {(a["AgentRole"], a["Generation"]): a for a in answers}
    complete = (len(lookup) == len(agents) * generations
                and all(a["ResponseStatus"] == "ok" for a in lookup.values()))
    votes = Counter(a["Verdict"] for a in lookup.values() if a["ResponseStatus"] == "ok")
    majority = next((v for v, count in votes.items() if count > len(agents) * generations / 2), None)
    status = "incomplete" if not complete else "majority" if majority else "no_majority"
    for generation in range(1, generations + 1):
        row = {**metadata, "Generation": generation,
               "DebateDecision": majority if complete and majority else status.upper(),
               "DebateStatus": status, "VoteCounts": json.dumps(dict(votes))}
        for role in agents:
            answer = lookup.get((role, generation), {})
            row[f"{role}_Decision"] = answer.get("Verdict", "")
            row[f"{role}_Reasoning"] = answer.get("Reasoning", "")
            row[f"{role}_Status"] = answer.get("ResponseStatus", "not_generated")
        yield row


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--sweep-config", type=Path, default=DEFAULT_SWEEP)
    parser.add_argument("--rounds", nargs="+", type=int)
    parser.add_argument("--identity-modes", nargs="+", choices=["fake_ticker", "real_name"])
    parser.add_argument("--generations", nargs="+", type=int)
    parser.add_argument("--rows", type=int)
    parser.add_argument("--model")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        grid = json.loads(args.sweep_config.read_text())
        if set(grid) != {"rounds", "identity_modes", "generations"}:
            raise ValueError("Sweep config requires rounds, identity_modes, generations")
        for key in grid:
            override = getattr(args, key)
            if override is not None:
                grid[key] = override
            values = grid[key]
            if not isinstance(values, list) or not values:
                raise ValueError(f"{key} must be a nonempty list")
            if key == "identity_modes":
                valid = all(v in ("fake_ticker", "real_name") for v in values)
            else:
                valid = all(type(v) is int and v >= (1 if key == "generations" else 0) for v in values)
            if not valid or len(set(values)) != len(values):
                raise ValueError(f"Invalid or duplicate {key}")
        overrides = {k: getattr(args, k) for k in ("rows", "model") if getattr(args, k) is not None}
        overrides.update(rounds=max(grid["rounds"]), self_revision=False)
        config = load_config(args.config, overrides)
        companies = {mode: load_companies(config["data"], config["rows"],
                     config["snapshot_date"], mode)[0] for mode in grid["identity_modes"]}
        combinations = list(product(grid["rounds"], grid["identity_modes"], grid["generations"]))
        agents = config["agents"]
        planned = sum(config["rows"] * len(QUESTION_TEMPLATES) * len(agents) * (r + 1) * g
                      for r, _, g in combinations)
        client = VLLM(**{f.name: config[f.name] for f in fields(VLLM)})
        served = None if args.dry_run else client.check()
        output = args.output or Path(config["output_root"]) / datetime.now(timezone.utc).strftime("sweep_%Y%m%dT%H%M%S_%fZ")
        output.mkdir(parents=True, exist_ok=False)
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    manifest = {"config": config, "grid": grid, "planned_calls": planned, "served_models": served,
                "status": "dry_run" if args.dry_run else "running",
                "workbook_sha256": hashlib.sha256(Path(config["data"]).read_bytes()).hexdigest(),
                "code_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in Path(__file__).parent.glob("*.py")},
                "sampling_rule": "All samples read the frozen previous round; all samples vote equally."}
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"{len(combinations)} configurations; {planned} calls; output: {output}", flush=True)
    if args.dry_run:
        return output
    calls_done = 0
    response_errors = 0
    writer = None
    try:
        with (output / "decisions.csv").open("w", newline="", encoding="utf-8-sig") as table, \
             (output / "calls.jsonl").open("w", encoding="utf-8") as log:
            for index, (rounds, mode, generations) in enumerate(combinations, 1):
                run_id = f"rounds_{rounds}_{mode}_generations_{generations}"
                print(f"Configuration {index}/{len(combinations)}: {run_id}", flush=True)
                progress = Progress(config["rows"], len(QUESTION_TEMPLATES), len(agents) * generations * (rounds + 1))
                for company_index, company in enumerate(companies[mode]):
                    evidence = company["evidence"]
                    progress.update(0, company_index, display_name(evidence), reset_children=True)
                    for question_index, (kind, template) in enumerate(QUESTION_TEMPLATES.items()):
                        progress.update(1, question_index, kind, reset_children=True)
                        pending = []

                        def save_round():
                            nonlocal writer
                            if not pending:
                                return
                            round_id = pending[0]["Round"]
                            metadata = {"RunID": run_id, "Model": config["model"], "Seed": config["seed"],
                                        "DebateRounds": rounds, "IdentityMode": mode,
                                        "GenerationsPerAgent": generations, "FakeTicker": evidence["FakeTicker"],
                                        "DisplayName": display_name(evidence), "QuestionType": kind,
                                        "Question": template.format(ticker=display_name(evidence)),
                                        "Round": round_id, "Stage": "baseline" if round_id == 0 else "debate",
                                        "IsFinalRound": round_id == rounds}
                            for row in comparison_rows(pending, agents, generations, metadata):
                                if writer is None:
                                    writer = csv.DictWriter(table, fieldnames=list(row))
                                    writer.writeheader()
                                writer.writerow(row)
                            table.flush()
                            pending.clear()

                        def show_call(condition, round_id, role):
                            progress.update(2, detail=f"{condition} {round_id}/{rounds} | {role}")

                        try:
                            results = run_question(evidence, kind, client.chat, rounds=rounds,
                                                   seed=config["seed"], agents=agents,
                                                   generations=generations, on_start=show_call)
                            for answer_index, answer in enumerate(results, 1):
                                if pending and answer["Round"] != pending[0]["Round"]:
                                    save_round()
                                log.write(json.dumps({"RunID": run_id, "FakeTicker": evidence["FakeTicker"],
                                                      "QuestionType": kind, **answer}) + "\n")
                                log.flush()
                                pending.append(answer)
                                calls_done += "RequestSeed" in answer
                                response_errors += answer["ResponseStatus"] != "ok"
                                progress.update(2, answer_index, f"round {answer['Round']} | {answer['AgentRole']} | sample {answer['Generation']}: {answer['ResponseStatus']}")
                                if len(pending) == len(agents) * generations:
                                    save_round()
                        finally:
                            save_round()
                        progress.update(1, question_index + 1)
                    progress.update(0, company_index + 1)
            manifest["status"] = "complete_with_errors" if response_errors else "complete"
    except (RuntimeError, OSError, ValueError, TypeError, KeyError, IndexError, KeyboardInterrupt) as exc:
        manifest.update(status="failed", error=str(exc))
    finally:
        manifest["attempted_calls"] = calls_done
        manifest["response_errors"] = response_errors
        manifest_path.write_text(json.dumps(manifest, indent=2))
    if manifest["status"] != "complete":
        parser.exit(1, f"Run {manifest['status']}; results saved in {output}\n")
    print(f"Done: {output / 'decisions.csv'}")
    return output


if __name__ == "__main__":
    main()
