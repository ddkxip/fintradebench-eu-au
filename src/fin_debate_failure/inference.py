"""One small vLLM HTTP client. No debate logic here."""

import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

@dataclass
class VLLM:
    base_url: str
    model: str
    max_tokens: int
    timeout: int
    thinking: bool
    sampling: dict

    def request(self, endpoint, payload=None):
        headers = {"Content-Type": "application/json"}
        api_key = os.environ.get("VLLM_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        req = Request(self.base_url.rstrip("/") + endpoint,
                      data=json.dumps(payload).encode() if payload is not None else None,
                      headers=headers)
        try:
            with urlopen(req, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            raise RuntimeError(f"vLLM HTTP {exc.code}: {exc.read().decode()}") from exc
        except (URLError, TimeoutError) as exc:
            raise RuntimeError(f"Cannot reach vLLM at {self.base_url}: {exc}") from exc

    def check(self):
        models = self.request("/models")
        if self.model not in [item["id"] for item in models["data"]]:
            raise ValueError(f"vLLM is not serving {self.model}. Check --model.")
        return models

    def chat(self, messages, schema, seed):
        payload = {"model": self.model, "messages": messages, "seed": seed,
                   "max_tokens": self.max_tokens, **self.sampling,
                   "chat_template_kwargs": {"enable_thinking": self.thinking},
                   "response_format": {"type": "json_schema", "json_schema": {
                       "name": "financial_answer", "strict": True, "schema": schema}}}
        return self.request("/chat/completions", payload)
