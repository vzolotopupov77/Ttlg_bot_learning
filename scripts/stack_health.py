"""Проверка полного стека: backend /health, корень frontend, статус контейнеров compose."""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_HEALTH = "http://127.0.0.1:8000/health"
FRONTEND_ROOT = "http://127.0.0.1:3000/"
TIMEOUT_S = 5.0
EXPECTED_SERVICES = ("db", "backend", "bot", "frontend")


def _http_check(url: str, *, ok_statuses: frozenset[int]) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_S) as resp:
            _ = resp.read()
            status = resp.status
        if status not in ok_statuses:
            return False, f"HTTP {status}"
        return True, f"OK (HTTP {status})"
    except urllib.error.HTTPError as e:
        if e.code in ok_statuses:
            return True, f"OK (HTTP {e.code})"
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, str(e.reason if hasattr(e, "reason") and e.reason else e)


def _parse_compose_ps_json(raw: str) -> list[dict]:
    raw = raw.strip()
    if not raw:
        return []
    if raw.startswith("["):
        data = json.loads(raw)
        return data if isinstance(data, list) else [data]
    out: list[dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(json.loads(line))
    return out


def _compose_status() -> tuple[list[dict] | None, str | None]:
    try:
        r = subprocess.run(
            ["docker", "compose", "ps", "-a", "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except FileNotFoundError:
        return None, "docker не найден в PATH"
    except subprocess.TimeoutExpired:
        return None, "timeout docker compose ps"
    except OSError as e:
        return None, str(e)

    if r.returncode != 0:
        err = (r.stderr or r.stdout or "").strip() or f"exit {r.returncode}"
        return None, err

    try:
        return _parse_compose_ps_json(r.stdout), None
    except json.JSONDecodeError as e:
        return None, f"разбор JSON: {e}"


def main() -> int:
    failed = False

    ok_b, msg_b = _http_check(BACKEND_HEALTH, ok_statuses=frozenset({200}))
    print(f"  backend   {BACKEND_HEALTH:32} {msg_b}")
    if not ok_b:
        failed = True

    ok_f, msg_f = _http_check(
        FRONTEND_ROOT,
        ok_statuses=frozenset(range(200, 400)),
    )
    print(f"  frontend  {FRONTEND_ROOT:32} {msg_f}")
    if not ok_f:
        failed = True

    rows, err = _compose_status()
    print("  compose   (docker compose ps)")
    if err:
        print(f"             пропущено: {err}")
    elif not rows:
        print("             нет контейнеров проекта (стек не поднимали?)")
        failed = True
    else:
        by_svc: dict[str, dict] = {}
        for row in rows:
            svc = row.get("Service") or row.get("service")
            if isinstance(svc, str):
                by_svc[svc] = row

        for name in EXPECTED_SERVICES:
            row = by_svc.get(name)
            if not row:
                print(f"             {name:10} отсутствует в compose ps")
                failed = True
                continue
            state = (row.get("State") or row.get("state") or "?").lower()
            health = row.get("Health") or row.get("health") or ""
            status = (row.get("Status") or row.get("status") or "").strip()
            extra = f", health={health}" if health else ""
            line = f"{name:10} {state}{extra}"
            if status:
                line += f" — {status}"
            print(f"             {line}")
            if state != "running":
                failed = True
            if str(health or "").lower() == "unhealthy":
                failed = True

    if failed:
        print("stack-health: есть ошибки", file=sys.stderr)
        return 1
    print("stack-health: все проверки прошли")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
