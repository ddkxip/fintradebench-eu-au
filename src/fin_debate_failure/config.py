"""Read one experiment config. Command-line values override the file."""

import json
import math
from datetime import date
from pathlib import Path

from .protocol import ROLE_INSTRUCTIONS

DEFAULT_CONFIG = Path(__file__).parent / "config.json"


def load_config(path=DEFAULT_CONFIG, overrides=None):
    config = json.loads(Path(path).read_text())
    if isinstance(config, dict):
        config.setdefault("identity_mode", "fake_ticker")
    required = {"data", "rows", "snapshot_date", "agents", "rounds", "self_revision", "seed",
                "output_root", "base_url", "model", "max_tokens", "timeout", "thinking", "sampling",
                "identity_mode"}
    if not isinstance(config, dict) or set(config) != required:
        raise ValueError("Config must have the same settings as the supplied config.json")
    for key in ("data", "output_root", "base_url", "model", "snapshot_date"):
        if not isinstance(config[key], str) or not config[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    # File paths are relative to the config. --data remains relative to the shell.
    for key in ("data", "output_root"):
        config[key] = str((Path(path).resolve().parent / config[key]).resolve())
    config.update(overrides or {})
    if config["identity_mode"] not in ("fake_ticker", "real_name"):
        raise ValueError("identity_mode must be fake_ticker or real_name")
    for key, minimum in (("rows", 1), ("rounds", 0), ("seed", 0), ("max_tokens", 1), ("timeout", 1)):
        if type(config[key]) is not int or config[key] < minimum:
            raise ValueError(f"{key} must be an integer >= {minimum}")
    agents = config["agents"]
    if not isinstance(agents, list) or not agents or any(not isinstance(a, str) or a not in ROLE_INSTRUCTIONS for a in agents):
        raise ValueError(f"agents must list roles from {list(ROLE_INSTRUCTIONS)}")
    if len(set(agents)) != len(agents):
        raise ValueError("Each agent role must appear only once")
    if len(agents) < 2 and config["rounds"] > 0:
        raise ValueError("Debate needs at least two agents; use rounds=0 for one agent")
    for key in ("thinking", "self_revision"):
        if type(config[key]) is not bool:
            raise ValueError(f"{key} must be true or false")
    date.fromisoformat(config["snapshot_date"])
    sampling = config["sampling"]
    allowed = {"temperature", "top_p", "top_k", "min_p", "presence_penalty", "repetition_penalty"}
    if not isinstance(sampling, dict) or set(sampling) != allowed:
        raise ValueError(f"sampling must contain {sorted(allowed)}")
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in sampling.values()):
        raise ValueError("Sampling values must be finite numbers")
    if not (sampling["temperature"] >= 0 and 0 < sampling["top_p"] <= 1
            and 0 <= sampling["min_p"] <= 1 and -2 <= sampling["presence_penalty"] <= 2
            and sampling["repetition_penalty"] > 0 and type(sampling["top_k"]) is int
            and (sampling["top_k"] == -1 or sampling["top_k"] >= 1)):
        raise ValueError("Invalid sampling range")
    return config
