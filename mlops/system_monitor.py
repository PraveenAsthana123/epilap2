"""
system_monitor.py — System resource monitoring (CPU / memory / GPU / disk / network)
====================================================================================

Samples host resource utilisation for the platform's monitoring dashboard. GPU is read
via nvidia-smi when present (optional). In production this feeds Prometheus/Grafana; here
it returns a snapshot dict + a threshold check for alerting.

Run: python mlops/system_monitor.py
"""
from __future__ import annotations
import shutil, subprocess
import psutil

# Alert thresholds (percent / count) — breaches would raise a monitoring alert.
THRESHOLDS = {"cpu_pct": 85, "memory_pct": 90, "disk_pct": 90}


def gpu_stats():
    """Return GPU utilisation via nvidia-smi if available, else None (no GPU)."""
    if not shutil.which("nvidia-smi"):
        return None
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"], text=True, timeout=5).strip().splitlines()
        gpus = []
        for i, line in enumerate(out):
            u, mu, mt = [x.strip() for x in line.split(",")]
            gpus.append({"gpu": i, "util_pct": float(u), "mem_used_mb": float(mu), "mem_total_mb": float(mt)})
        return gpus
    except Exception:
        return None


def snapshot() -> dict:
    """One resource-utilisation sample across CPU, memory, disk, network (+GPU)."""
    vm = psutil.virtual_memory()
    du = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    return {
        "cpu_pct": psutil.cpu_percent(interval=0.3),
        "cpu_cores": psutil.cpu_count(),
        "memory_pct": vm.percent,
        "memory_used_gb": round(vm.used / 1e9, 2),
        "memory_total_gb": round(vm.total / 1e9, 2),
        "disk_pct": du.percent,
        "disk_free_gb": round(du.free / 1e9, 2),
        "net_sent_mb": round(net.bytes_sent / 1e6, 1),
        "net_recv_mb": round(net.bytes_recv / 1e6, 1),
        "gpu": gpu_stats(),
    }


def check_alerts(snap: dict) -> list[str]:
    """Return threshold breaches for alerting (empty = healthy)."""
    alerts = []
    for k, limit in THRESHOLDS.items():
        if snap.get(k, 0) >= limit:
            alerts.append(f"{k}={snap[k]} >= {limit}")
    return alerts


def main():
    snap = snapshot()
    print("system snapshot:")
    for k, v in snap.items():
        print(f"  {k}: {v}")
    alerts = check_alerts(snap)
    print("alerts:", alerts or "none (healthy)")


if __name__ == "__main__":
    main()
