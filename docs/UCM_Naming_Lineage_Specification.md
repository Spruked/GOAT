# UCM Naming & Lineage Specification

## Purpose

This document defines the **canonical naming, lineage, and evolution rules** for the Unified Cognitive Module (UCM) and its descendants. Its purpose is to prevent naming drift, architectural confusion, and tool‑introduced mislabeling during development, refactoring, and long‑term evolution.

This document is **authoritative**.

---

## 1. UCM — Unified Cognitive Module (Design Name)

**UCM is the permanent design name.**

* UCM represents the **architectural identity**, not a specific implementation
* The name **never changes**, regardless of refactors or internal rewrites
* UCM preserves **origin clarity, intent, and lineage**
* UCM is the stable reference point across all versions

Think of UCM as:

* the keel of a ship
* a platform designation
* a constitutional identifier

> If the system evolves, the name UCM remains.

---

## 2. UCM-Core — Execution & Control Layer

**UCM-Core** is the stabilized execution core inside UCM.

Responsibilities:

* lifecycle control
* orchestration
* invariants and safety boundaries
* coordination of submodules

UCM-Core may evolve internally, but remains:

```
UCM → UCM-Core
```

---

## 3. UCM-Core-ECM — Epistemic Convergence Matrix

**ECM = Epistemic Convergence Matrix**

UCM-Core-ECM is the convergence layer responsible for judgment formation.

Characteristics:

* integrates multiple epistemic frameworks
* deterministic and auditable
* produces signed judgment artifacts
* resolves contradictions through convergence, not heuristics

This is a **qualified descendant**, not a separate system.

```
UCM → UCM-Core → UCM-Core-ECM
```

---

## 4. CALI — Cognitively Aligned Linear Intelligence

**CALI** is the alignment and reasoning model instantiated within UCM.

Properties:

* linear, stepwise reasoning
* cognitively aligned (non-coercive)
* auditable and explainable
* does not imply authority or force

CALI is **not** the UCM itself.
It is a model **hosted by UCM**.

```
UCM-Core → CALI
```

---

## 5. Caleon / Cali Caleon — Presence Layer

* **Caleon** refers to the system identity
* **Cali** is the personable articulation of that identity

Rules:

* Cali is **not** the chat bubble
* Cali appears only where presence is explicitly intended (e.g., orb interface)
* Cali does not act as an authority, guardian, or enforcer

Cali exists **on top of** UCM-CALI, not instead of it.

---

## 6. Other Qualified Descendants (Valid Pattern)

The following naming pattern is valid and encouraged:

* UCM-Core-CALI
* UCM-Core-GOAT
* UCM-Core-Vault
* UCM-Core-DALS

All such components:

* inherit UCM lineage
* must be traceable back to UCM
* do not replace or rename UCM

---

## 7. Naming Rules (Non‑Negotiable)

* **UCM** is never renamed
* No component may claim to replace UCM
* Tooling (IDEs, LLMs, assistants) may not invent names
* Anthropomorphic or authority‑implying titles are prohibited

Allowed usage:

* architectural docs → UCM
* reasoning descriptions → CALI
* UI presence → Cali Caleon
* technical precision → UCM‑CALI

---

## 8. Canonical Composite Reference

When full clarity is required:

**UCM‑CALI**

> Unified Cognitive Module — Cognitively Aligned Linear Intelligence

This denotes:

* the stable architectural identity (UCM)
* the current alignment and reasoning instantiation (CALI)

---

## 9. Final Principle

> UCM is the name that carries truth through time.

Everything else evolves — the lineage does not.

---

**Status:** Final
**Authority:** System Architecture