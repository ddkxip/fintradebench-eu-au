"""Vertex AI chat adapter (gemini via global endpoint, ADC token auth)."""

from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.request

PROJECT = "research-finbot"
ENDPOINT = ("https://aiplatform.googleapis.com/v1/projects/{project}/"
            "locations/global/publishers/google/models/{model}:generateContent")

_token: dict = {"value": None, "expires": 0.0}


def access_token() -> str:
    if _token["value"] and time.time() < _token["expires"]:
        return _token["value"]
    env = dict(os.environ, CLOUDSDK_PYTHON=r"C:\Python314\python.exe")
    out = subprocess.run(["gcloud", "auth", "print-access-token"],
                         capture_output=True, text=True, env=env,
                         timeout=60, shell=True)
    tok = out.stdout.strip()
    if not tok.startswith("ya29"):
        raise RuntimeError(f"gcloud token failed: {out.stderr[:200]}")
    _token.update(value=tok, expires=time.time() + 45 * 60)
    return tok


def chat_vertex(system: str, user: str, model: str,
                temperature: float = 0.7, timeout: int = 120,
                max_retries: int = 4) -> str:
    payload = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {
            "temperature": float(temperature),
            "maxOutputTokens": 2000,
            "responseMimeType": "application/json",
        },
    }
    url = ENDPOINT.format(project=PROJECT, model=model)
    last_err = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode(),
                headers={"Authorization": f"Bearer {access_token()}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                obj = json.loads(r.read().decode())
            return obj["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as exc:  # 429/5xx/network: backoff and retry
            last_err = exc
            time.sleep(2 ** attempt * 3)
    raise RuntimeError(f"vertex chat failed after {max_retries} tries: {last_err}")
