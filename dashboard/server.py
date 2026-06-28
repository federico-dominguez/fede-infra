#!/usr/bin/env python3
"""
Dashboard — Panel de monitoreo para Fede
FastAPI server, sirve HTML con datos de sistema y OpenRouter.
Corre en Tailscale (100.109.36.3) para acceso privado.
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

import httpx
import psutil
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

# ── Config ──────────────────────────────────────────────────────────────────

TAILSCALE_IP = "100.109.36.3"
PORT = 8080

# OpenRouter keys
#  - "main" (Ticia)
#  - "main-moltbot" (Claw)
OPENROUTER_KEYS = {
    name: key
    for name, key in [
        ("main", os.environ.get("OPENROUTER_API_KEY", "")),
        ("main-moltbot", os.environ.get("CLAW_OPENROUTER_API_KEY", "")),
    ]
    if key
}

# OpenRouter: account-level credits (shared entre ambas keys)
OPENROUTER_ACCOUNT = list(OPENROUTER_KEYS.values())[0]

# ── Static info ─────────────────────────────────────────────────────────────

AGENT_NAME = os.environ.get("AGENT_NAME", "ticia")
PROVIDER = "openrouter"
MODEL = "deepseek-v4-pro"

# ── App setup ───────────────────────────────────────────────────────────────

app = FastAPI(title="Dashboard Fede", version="1.0.0")
templates = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"))


# ── OpenRouter helpers ──────────────────────────────────────────────────────


async def fetch_account_credits() -> dict:
    """Obtiene créditos de la cuenta (account-wide, compartido entre keys)."""
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(
                "https://openrouter.ai/api/v1/credits",
                headers={"Authorization": f"Bearer {OPENROUTER_ACCOUNT}"},
            )
            resp.raise_for_status()
            data = resp.json().get("data", {})
            total = data.get("total_credits", 0)
            used = data.get("total_usage", 0)
            return {
                "total_credits": total,
                "total_usage": used,
                "credits_left": max(0, total - used),
            }
        except Exception as e:
            return {"error": str(e), "total_credits": 0, "total_usage": 0, "credits_left": 0}


async def fetch_openrouter_key_info(api_key: str, label: str) -> dict:
    """Obtiene info de la key (uso individual)."""
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(
                "https://openrouter.ai/api/v1/auth/key",
                headers={"Authorization": f"Bearer {api_key}"},
            )
            resp.raise_for_status()
            data = resp.json().get("data", {})
            return {
                "label": label,
                "usage": data.get("usage", 0),
                "limit": data.get("limit", 0),
                "is_free_tier": data.get("is_free_tier", False),
            }
        except Exception as e:
            return {"error": str(e), "label": label, "usage": 0, "limit": 0}


async def collect_openrouter_data() -> dict:
    """Recolecta datos de cuenta y keys de OpenRouter."""
    account = await fetch_account_credits()
    keys = []
    for label, api_key in OPENROUTER_KEYS.items():
        info = await fetch_openrouter_key_info(api_key, label)
        keys.append(
            {
                "label": label,
                "usage": info.get("usage", 0),
                "is_free_tier": info.get("is_free_tier", False),
                "error": info.get("error"),
            }
        )
    return {"account": account, "key_list": keys}


# ── System metrics ──────────────────────────────────────────────────────────


def get_system_metrics() -> dict:
    """Obtiene métricas del sistema con psutil."""
    cpu_percent = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    # Obtener hostname
    hostname = subprocess.run(
        ["hostname"], capture_output=True, text=True, timeout=5
    ).stdout.strip()

    # Obtener IPs (pública y Tailscale)
    ips = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2:  # AF_INET
                ips.append({"interface": iface, "ip": addr.address})

    return {
        "hostname": hostname,
        "ips": ips,
        "cpu_percent": round(cpu_percent, 1),
        "ram": {
            "total": round(mem.total / (1024**3), 1),
            "used": round(mem.used / (1024**3), 1),
            "percent": round(mem.percent, 1),
        },
        "disk": {
            "total": round(disk.total / (1024**3), 1),
            "used": round(disk.used / (1024**3), 1),
            "percent": round(disk.percent, 1),
        },
        "uptime": _format_uptime(psutil.boot_time()),
        "backup": _get_backup_status(),
    }


def _get_backup_status() -> dict:
    """Checkea estado del backup OCI vía timestamp del log."""
    log_path = Path("/var/log/oci-backup.log")
    if not log_path.exists():
        return {"status": False, "label": "Sin ejecutar", "last_run": None, "hours_since": None}

    last_modified = log_path.stat().st_mtime
    now = datetime.now().timestamp()
    hours_since = round((now - last_modified) / 3600, 1)
    status = hours_since < 72

    last_run_dt = datetime.fromtimestamp(last_modified)
    label = "Activo" if status else "Inactivo"

    return {
        "status": status,
        "label": label,
        "last_run": last_run_dt.strftime("%Y-%m-%d %H:%M"),
        "hours_since": hours_since,
    }


def _format_uptime(boot_time: float) -> str:
    """Formatea uptime como texto legible."""
    delta = datetime.now() - datetime.fromtimestamp(boot_time)
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


# ── Routes ──────────────────────────────────────────────────────────────────


@app.get("/api/system")
async def api_system():
    return get_system_metrics()


@app.get("/api/openrouter")
async def api_openrouter():
    return await collect_openrouter_data()


@app.get("/", response_class=HTMLResponse)
async def index():
    system = get_system_metrics()
    or_data = await collect_openrouter_data()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    template = templates.get_template("dashboard.html")
    html = template.render(
        system=system,
        openrouter=or_data,
        now=now,
        tailscale_ip=TAILSCALE_IP,
        agent_name=AGENT_NAME,
        provider=PROVIDER,
        model=MODEL,
    )
    return HTMLResponse(content=html)


# ── Entrypoint ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )