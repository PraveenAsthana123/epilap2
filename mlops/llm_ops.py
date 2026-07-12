"""
llm_ops.py — LLM / Agent operations layer (the "missing model" capabilities)
============================================================================

Runnable, dependency-free stand-ins for the agentic/LLM-ops capabilities the checklist
lists — so the platform's GenAI parts (onboarding intake, RAG reporting) are governed:

    PromptRegistry     versioned prompt templates (prompt registry)
    SemanticCache      cache responses by normalised query (semantic caching)
    ModelRouter        route task -> model tier by complexity (model routing / cost)
    ResponseEvaluator  hallucination / grounding / PII checks (response evaluation)
    CostTracker        token + cost estimate (token/cost optimization)

These are the interfaces + logic; in production they wrap real providers (Anthropic, etc.).
Run: python mlops/llm_ops.py
"""
from __future__ import annotations
import re, hashlib


class PromptRegistry:
    """Versioned prompt templates with immutable versions."""
    def __init__(self):
        self._store = {}

    def register(self, name, template):
        v = len(self._store.get(name, [])) + 1
        self._store.setdefault(name, []).append(template)
        return v

    def get(self, name, version=None):
        vs = self._store[name]
        return vs[(version or len(vs)) - 1]


class SemanticCache:
    """Cache by normalised query key (lowercase/whitespace); a real impl keys on embeddings."""
    def __init__(self):
        self._c = {}
        self.hits = 0
        self.misses = 0

    @staticmethod
    def _key(q):
        return hashlib.sha1(re.sub(r"\s+", " ", q.strip().lower()).encode()).hexdigest()

    def get(self, q):
        k = self._key(q)
        if k in self._c:
            self.hits += 1
            return self._c[k]
        self.misses += 1
        return None

    def put(self, q, resp):
        self._c[self._key(q)] = resp


class ModelRouter:
    """Route a task to a model tier by estimated complexity (cost/latency optimization)."""
    TIERS = {"small": 1, "medium": 3, "large": 8}  # relative cost units

    def route(self, task_len, needs_reasoning=False):
        if needs_reasoning or task_len > 2000:
            return "large"
        if task_len > 400:
            return "medium"
        return "small"


class ResponseEvaluator:
    """Evaluate a model response: PII leakage, ungrounded claims, refusal markers."""
    PII = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+|\bEP-?\d{3,}\b|\b\d{3}-\d{2}-\d{4}\b")
    HALLUCINATION = re.compile(r"\b(i think|probably|as an ai|i'm not sure|maybe it is)\b", re.I)

    def evaluate(self, response, grounding_sources=None):
        issues = []
        if self.PII.search(response):
            issues.append("pii_leak")
        if self.HALLUCINATION.search(response):
            issues.append("low_confidence_language")
        if grounding_sources is not None and not grounding_sources:
            issues.append("ungrounded (no RAG source)")
        return {"ok": not issues, "issues": issues}


class CostTracker:
    """Estimate tokens + cost (token/cost optimization)."""
    def __init__(self, price_per_1k=0.003):
        self.price = price_per_1k
        self.total_tokens = 0

    def track(self, text):
        toks = max(1, len(text) // 4)          # ~4 chars/token
        self.total_tokens += toks
        return {"tokens": toks, "cost": round(toks / 1000 * self.price, 5)}


def main():
    print("LLM/Agent-Ops demo")
    reg = PromptRegistry()
    reg.register("intake", "You are an epilepsy intake assistant. Ask about {topic}.")
    v2 = reg.register("intake", "You are an epilepsy intake assistant (v2). Elicit {topic} with validation.")
    print(f"  PromptRegistry: 'intake' v{v2} ->", reg.get("intake")[:40], "...")

    cache = SemanticCache()
    cache.put("What is EP001 severity?", "Severe (Level 3)")
    print("  SemanticCache: hit ->", cache.get("what is  EP001 SEVERITY?"), f"(hits={cache.hits})")

    router = ModelRouter()
    print("  ModelRouter: short->", router.route(120), " reasoning->", router.route(120, True))

    ev = ResponseEvaluator()
    print("  ResponseEvaluator clean:", ev.evaluate("Focal seizures, left temporal.", grounding_sources=["ILAE"]))
    print("  ResponseEvaluator bad  :", ev.evaluate("Patient EP-2026-001, I think maybe.", grounding_sources=[]))

    cost = CostTracker()
    print("  CostTracker:", cost.track("Summarise the seizure history for the patient in detail."))


if __name__ == "__main__":
    main()
