"""Run a configured debate, or preview its baseline prompts with --dry-run."""

import argparse
import csv
import hashlib
import json
from dataclasses import fields
from datetime import datetime, timezone
from pathlib import Path

from .config import DEFAULT_CONFIG, load_config
from .data import load_companies
from .debate import run_question
from .inference import VLLM
from .progress import Progress
from .protocol import QUESTION_TEMPLATES, RESPONSE_COLUMNS, display_name, messages
from .review import agent_behavior, final_answers, identity_mentions, round_answers, summarize


def csv_values(row):
    return {key: json.dumps(value) if isinstance(value, (list, dict)) else value
            for key, value in row.items()}


def save_csv(path, rows, columns):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(csv_values(row) for row in rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, argument_default=argparse.SUPPRESS)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--rows", type=int)
    parser.add_argument("--identity-mode", choices=["fake_ticker", "real_name"])
    parser.add_argument("--agents", nargs="+")
    parser.add_argument("--snapshot-date")
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--rounds", type=int)
    parser.add_argument("--self-revision", action=argparse.BooleanOptionalAction)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    options = vars(parser.parse_args(argv))
    config_path = options.pop("config")
    output = options.pop("output", None)
    dry_run = options.pop("dry_run", False)
    try:
        config = load_config(config_path, options)
        agents = config["agents"]
        companies, identities = load_companies(config["data"], config["rows"],
                                               config["snapshot_date"], config["identity_mode"])
        client = VLLM(**{field.name: config[field.name] for field in fields(VLLM)})
        served_models = None if dry_run else client.check()
        run_name = config["identity_mode"] + datetime.now(timezone.utc).strftime("_%Y%m%dT%H%M%S_%fZ")
        output = output or Path(config["output_root"]) / run_name
        output.mkdir(parents=True, exist_ok=False)
    except (ValueError, TypeError, OSError, RuntimeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    stages = 1 + config["rounds"] * (1 + config["self_revision"])
    planned = config["rows"] * len(QUESTION_TEMPLATES) * len(agents) * stages
    manifest = {"config": config, "config_path": str(config_path),
                "served_models": served_models, "planned_responses": planned,
                "workbook_sha256": hashlib.sha256(Path(config["data"]).read_bytes()).hexdigest(),
                "code_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in Path(__file__).parent.glob("*.py")},
                "companies": companies, "status": "dry_run" if dry_run else "running"}
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str))
    print(f"Identity mode: {config['identity_mode']}", flush=True)
    print(f"Companies: {', '.join(display_name(c['evidence']) for c in companies)}", flush=True)
    print(f"Agents: {', '.join(agents)}; debate rounds: {config['rounds']}", flush=True)
    print(f"Planned responses: {planned}; output: {output}", flush=True)
    if dry_run:
        prompts = [messages(c["evidence"], kind, role) for c in companies
                   for kind in QUESTION_TEMPLATES for role in agents]
        (output / "prompts.json").write_text(json.dumps(prompts, indent=2))
        print(f"Saved {len(prompts)} baseline prompts. No model calls made.")
        return
    rows = []
    progress = Progress(len(companies), len(QUESTION_TEMPLATES), len(agents) * stages)

    def show_call(condition, round_id, role):
        stage = "baseline" if round_id == 0 else f"{condition} {round_id}/{config['rounds']}"
        progress.update(2, detail=f"{stage} | {role}")

    try:
        with (output / "responses.csv").open("w", newline="", encoding="utf-8") as csv_file, \
             (output / "calls.jsonl").open("w", encoding="utf-8") as calls:
            writer = csv.DictWriter(csv_file, fieldnames=RESPONSE_COLUMNS)
            writer.writeheader()
            for row_index, company in enumerate(companies):
                evidence = company["evidence"]
                progress.update(0, row_index, display_name(evidence), reset_children=True)
                for question_index, (kind, template) in enumerate(QUESTION_TEMPLATES.items()):
                    progress.update(1, question_index, kind, reset_children=True)
                    results = run_question(evidence, kind, client.chat, config["rounds"],
                                           config["self_revision"], config["seed"], agents,
                                           on_start=show_call)
                    for answer_index, result in enumerate(results, 1):
                        result.update({"FakeTicker": evidence["FakeTicker"], "QuestionType": kind,
                                       "Question": template.format(ticker=display_name(evidence)),
                                       "IdentityMode": config["identity_mode"],
                                       "CompanyName": evidence.get("CompanyName"),
                                       "Config": "homogeneous", "Seed": config["seed"], "Model": config["model"]})
                        result["IdentityMentions"] = identity_mentions(result["RawResponse"], identities)
                        row = {key: result.get(key) for key in RESPONSE_COLUMNS}
                        writer.writerow(csv_values(row))
                        csv_file.flush()
                        calls.write(json.dumps(result) + "\n")
                        calls.flush()
                        rows.append(row)
                        progress.update(2, answer_index,
                                        f"{result['Condition']} {result['Round']} | "
                                        f"{result['AgentRole']}: {result['ResponseStatus']}")
                    progress.update(1, question_index + 1)
                progress.update(0, row_index + 1)
        manifest["status"] = "complete" if all(r["ResponseStatus"] == "ok" for r in rows) else "complete_with_errors"
    except (RuntimeError, OSError, ValueError, TypeError, KeyError, IndexError, KeyboardInterrupt) as exc:
        manifest.update(status="failed", error=str(exc))
    finally:
        manifest_path.write_text(json.dumps(manifest, indent=2, default=str))
        (output / "summary.json").write_text(json.dumps(
            summarize(rows, agents, config["identity_mode"]), indent=2))
        condition = "debate" if config["rounds"] else "baseline"
        final_rows = [r for r in rows if r["Condition"] == condition and r["Round"] == config["rounds"]]
        save_csv(output / "final_agent_answers.csv", final_rows, RESPONSE_COLUMNS)
        finals = final_answers(rows, agents, config["rounds"])
        if finals:
            save_csv(output / "final_answers.csv", finals, list(finals[0]))
        checkpoints = round_answers(rows, agents, config["rounds"])
        if checkpoints:
            save_csv(output / "round_answers.csv", checkpoints, list(checkpoints[0]))
        behavior = agent_behavior(rows)
        if behavior:
            save_csv(output / "agent_behavior.csv", behavior, list(behavior[0]))
    if manifest["status"] != "complete":
        parser.exit(1, f"Run {manifest['status']}. See {manifest_path}\n")
    print(f"Done. See {output / 'final_answers.csv'}")


if __name__ == "__main__":
    main()
