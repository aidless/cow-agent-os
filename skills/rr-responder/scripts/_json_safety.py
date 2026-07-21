#!/usr/bin/env python3.11
"""
Shared LLM-call + JSON-parse helpers used by all rr-responder scripts.

Usage from a stage script:

    from _json_safety import call_and_parse

    result = call_and_parse(model, system, user, max_tokens=1200)
    if result is None:
        ...fallback...
    # else `result` is a dict.

`call_and_parse` does:
  - HTTP POST to OPENAI_API_BASE/chat/completions with retries
  - Strips ``` fences
  - First-pass json.loads
  - Fallback: extract the first {...} block (greedy) and try again
  - Final fallback: return None

This module is internal to the rr-responder skill. Other skills should
copy it rather than depend on this path.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from typing import Any

DEFAULT_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1").rstrip("/")
DEFAULT_KEY = os.environ.get("OPENAI_API_KEY", "")
DEFAULT_TIMEOUT = 60


def _strip_fences(text: str) -> str:
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())


def _fix_invalid_escapes(text: str) -> str:
    """Fix common invalid JSON escape sequences.

    Fix 1 (7/11 打磨):Test 2 出现 `Invalid \\escape: line 2 column 31 (char 32)`。
    根因:DeepSeek LLM 偶尔输出 `\\u` `\\d` `\\n` 这种不像标准 JSON 标准的 escape。
    策略:
      1. 把不像 JSON 标准的 escape 替换成字面字符(用反斜杠非 escape 字符)
      2. 把不完整的 `\\u`(没跟 4 位 hex)替换成 `u` 字面

    实现:覆盖了反向验证测试发现的 edge case。
    """
    # 1. 不像 JSON 标准的 escape 替换为字面字符(\b \f \n \r \t \u \")
    #    这些字符之外的 \X 都换成 X 字面
    text = re.sub(r'\\([^"\\/bfnrtu])', r'\1', text)
    # 2. 不完整的 \uXXXX: \u 后面没接 4 个 hex digits,替换为 u 字面
    text = re.sub(r'\\u(?![0-9a-fA-F]{4})', 'u', text)
    return text


def _try_extract_json(text: str) -> str | None:
    """Return the first balanced {...} substring, else None."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == "\\" and in_string:
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def call_llm(model: str, system: str, user: str,
             max_tokens: int = 1200,
             temperature: float = 0.2,
             retries: int = 3,
             timeout: int = DEFAULT_TIMEOUT) -> str | None:
    """POST and return raw assistant content (or None on full failure)."""
    if not DEFAULT_KEY:
        return None

    url = f"{DEFAULT_BASE}/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {DEFAULT_KEY}"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"].get("content", "")
        except (urllib.error.URLError, urllib.error.HTTPError,
                KeyError, json.JSONDecodeError) as e:
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)
    print(f"[call_llm] all retries failed: {last_err}", file=__import__("sys").stderr)
    return None


def call_and_parse(model: str, system: str, user: str,
                   max_tokens: int = 1200,
                   temperature: float = 0.2,
                   retries: int = 3) -> dict[str, Any] | None:
    """POST + parse JSON, with bracket-extraction fallback.

    7/11 打磨:加 `strict=False` 让 json.loads 接受非标准 escape(修复 `\\d` `\\n`)。
    """
    raw = call_llm(model, system, user, max_tokens=max_tokens,
                   temperature=temperature, retries=retries)
    if raw is None:
        return None
    text = _strip_fences(raw)
    # Fix 1: 先尝试 escape 容错
    fixed = _fix_invalid_escapes(text)
    try:
        obj = json.loads(fixed, strict=False)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    # 备选:bracketed-extract
    extracted = _try_extract_json(text)
    if extracted is not None:
        extracted_fixed = _fix_invalid_escapes(extracted)
        try:
            obj = json.loads(extracted_fixed, strict=False)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    return None
