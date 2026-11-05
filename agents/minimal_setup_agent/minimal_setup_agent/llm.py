import time

import httpx

BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "qwen/qwen3.5-plus-20260420"
RETRY_STATUS = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 8


class LLMError(Exception):
    pass


class LLMClient:
    def __init__(self, base_url: str, api_key: str, model: str, max_tokens: int = 8192,
                 timeout: float = 600):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        self.model = model
        self.max_tokens = max_tokens
        self.timeout = timeout

    def config(self) -> dict:
        return {"model": self.model, "max_tokens": self.max_tokens}

    def chat(self, messages: list[dict], tools: list[dict]) -> dict:
        body = {"model": self.model, "messages": messages, "tools": tools,
                "tool_choice": "auto", "max_tokens": self.max_tokens}
        for attempt in range(1, MAX_ATTEMPTS + 1):
            if attempt > 1:
                time.sleep(min(2 ** (attempt - 1), 60))
            try:
                resp = httpx.post(self.url, json=body, headers=self.headers, timeout=self.timeout)
            except httpx.TransportError as e:
                error = f"transport error: {e}"
                continue
            if resp.status_code == 200:
                break
            error = f"HTTP {resp.status_code}: {resp.text[:1000]}"
            if resp.status_code not in RETRY_STATUS:
                raise LLMError(error)
        else:
            raise LLMError(error)
        try:
            data = resp.json()
            data["choices"][0]["message"]
        except (ValueError, KeyError, IndexError, TypeError) as e:
            raise LLMError(f"unparseable response: {resp.text[:1000]}") from e
        return data
