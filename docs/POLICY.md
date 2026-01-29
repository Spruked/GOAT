## The Message (copy/paste)

> **Orb Presence & Naming Directive (Authoritative)**
>
> * **UCM** is the permanent design lineage.
> * Current instantiation is **UCM_4_Core — CALI**.
> * **Cali Caleon** is a presence layer, not a service, not a worker, not a guardian.
>
> **Orb Rendering Rules:**
>
> * In **admin/operator context**, the Cali Caleon Orb is a **global presence layer** within **UCM_4_Core — CALI**.
> * The Orb is **not page-scoped** and must persist across navigation.
> * In **user context**, the Orb is **hidden by default** and appears **only after explicit escalation opt-in**.
> * **Clicking the orb is NOT escalation** and must not open a conversation.
>
> **Behavior Rules:**
>
> * No "Guardian" language anywhere.
> * No implied authority, force, recommendations, or monitoring.
> * No "simulation" language; use "response generation" or "worker-routed responses".
> * GOAT and DALS may expose **status and tools only**, not cognition or persona.
>
> **Mints:**
>
> * Mints may reference **UCM lineage** and **CALI alignment** for provenance and verification.
> * Mints do **not** surface Cali Caleon as an agent, guardian, or decision-maker.
>
> Naming drift is a bug. Presence is intentional. Consent is explicit.

---

## One-line variants (if they want it shorter)

* **GOAT:**

  > Cali Caleon is a global admin presence, not a GOAT feature. GOAT exposes tools; Cali observes by invitation.

* **DALS:**

  > DALS transports and reports status. It does not speak as Cali and does not infer intent.

* **Mints:**

  > Mints certify lineage (UCM) and alignment (CALI). They do not imply agency or guardianship.

---

## That's it

You're not asking them to design.
You're telling them **where the lines are**.

---

## Design Intent vs Implementation Addendum

### Original Design Intent (Conceptual)
- Cali Caleon Orb as universal presence layer across all systems (UCM, GOAT, DALS)
- Global mounting and shared UI components
- Cross-system orb reuse for consistency

### Current Implementation Reality
- Cali Caleon Orb exists **only within UCM_4_Core — CALI**
- GOAT and DALS implement their own native orbs (KayGee, Cali X One)
- No shared UI components; identity-bound implementations
- Presence principles aligned, but not literally reused

### Reconciliation
- **Documentation overstated integration scope** — corrected to reflect reality
- **Code correctly follows identity boundaries** — no changes needed
- **Global mounting would violate current architecture** — correctly avoided
- **Alignment ≠ reuse** — conceptual consistency without component sharing

### Architectural Stance
- Each system maintains its own orb implementation
- Prevents impersonation and confusion
- Preserves ethical boundaries and consent-first design
- Allows for system-specific optimizations

This addendum clarifies that the original intent was aspirational documentation, not implemented code. The current state is correct and intentional.