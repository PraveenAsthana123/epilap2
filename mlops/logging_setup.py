"""
logging_setup.py — Structured application / inference / audit logging
====================================================================

Three separate JSON-line log streams (the logging checklist item):
  application  general app events / errors
  inference    every model prediction (model, version, inputs summary, output, confidence)
  audit        governance events (who did what, model/prompt/data version) — accountability

Logs are written to mlops/store/logs/<stream>.log as JSON lines (ship to ELK/Loki in prod).
"""
from __future__ import annotations
import os, json, logging, time

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store", "logs")
os.makedirs(LOG_DIR, exist_ok=True)


class _JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {"ts": record.created, "level": record.levelname, "stream": record.name}
        if isinstance(record.msg, dict):
            base.update(record.msg)
        else:
            base["message"] = record.getMessage()
        return json.dumps(base)


def get_logger(stream: str) -> logging.Logger:
    lg = logging.getLogger(stream)
    if not lg.handlers:
        lg.setLevel(logging.INFO)
        h = logging.FileHandler(os.path.join(LOG_DIR, f"{stream}.log"), encoding="utf-8")
        h.setFormatter(_JsonFormatter())
        lg.addHandler(h)
        lg.propagate = False
    return lg


def log_inference(model: str, version, inputs: dict, output, confidence=None):
    get_logger("inference").info({"event": "prediction", "model": model, "version": version,
                                  "n_inputs": len(inputs), "output": output,
                                  "confidence": confidence, "t": time.time()})


def log_audit(actor: str, action: str, entity: str, detail: dict | None = None):
    get_logger("audit").info({"event": "audit", "actor": actor, "action": action,
                              "entity": entity, "detail": detail or {}, "t": time.time()})


def log_app(message: str, level: str = "INFO"):
    getattr(get_logger("application"), level.lower(), get_logger("application").info)(message)
