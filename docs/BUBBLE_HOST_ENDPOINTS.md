# GOAT Bubble Host – Endpoint Connection Map

## Complete API Architecture Specification

**Last Updated:** 2025-12-16  
**Status:** Authoritative - Locked Design  
**Purpose:** Logical endpoint map for Bubble Host orchestration layer

---

## Overview

This document defines **logical endpoints**, not implementation details.

Names can vary; responsibilities do not.

---

## Mental Model

```
User → Host (guided or manual) 
     → Assistants 
       → Mini-SKG 
         → Pipeline 
           → Host 
             → User
               ↘ Caleon 
                 ↘ Vault
```

---

## 1. Entry & Routing

### Concierge Host

**Endpoint:** `GET /api/products`
- **Purpose:** Fetch available products for user
- **Input:** User token
- **Output:** List of accessible products with metadata
- **Permissions:** Authenticated users only

**Endpoint:** `POST /api/concierge/route`
- **Purpose:** Department routing decision
- **Input:** 
  - user intent (conversational or selected)
  - product choice
  - context from prior session (if any)
- **Output:** 
  - target department host
  - session initialization data
- **Flow:** Concierge → Department Host handoff

---

## 2. Bubble Host Session Control

### All Department Hosts

**Endpoint:** `POST /api/host/session/start`
- **Purpose:** Initialize host session
- **Input:**
  - user_id
  - product_type
  - permissions
  - prior_context (optional)
- **Output:**
  - session_id
  - host_persona_config
  - initial_script
- **Audit:** Logged to vault

**Endpoint:** `POST /api/host/session/message`
- **Purpose:** Process conversational input (optional mode)
- **Input:**
  - session_id
  - user_message
  - timestamp
- **Output:**
  - host_response
  - suggested_next_steps
  - form_prepopulation (if applicable)
- **Flow:** Updates Mini-SKG with conversational patterns

**Endpoint:** `POST /api/host/session/advance`
- **Purpose:** User progression trigger
- **Input:**
  - session_id
  - action ("next" | "continue" | "skip")
  - current_state
- **Output:**
  - next_script
  - form_state
  - validation_results
- **Flow:** Power user fast-forward

**Endpoint:** `POST /api/host/session/end`
- **Purpose:** Clean session termination
- **Input:**
  - session_id
  - completion_status
  - user_feedback (optional)
- **Output:**
  - audit_log_id
  - mini_skg_update_id
- **Audit:** Full trace stored

---

## 3. Manual Input & Overrides (Always Available)

### Product Pages

**Endpoint:** `POST /api/product/{type}/draft`
- **Purpose:** Save partial manual input
- **Input:**
  - session_id
  - form_data (partial)
  - timestamp
- **Output:**
  - draft_id
  - validation_warnings
- **Storage:** Temporary, user-scoped

**Endpoint:** `POST /api/product/{type}/override`
- **Purpose:** Explicit user override of host suggestions
- **Input:**
  - session_id
  - field_name
  - override_value
  - reason (optional)
- **Output:**
  - confirmation
  - mini_skg_note (logged but not enforced)
- **Rule:** Manual intent always wins

**Endpoint:** `POST /api/product/{type}/comment`
- **Purpose:** User clarification notes
- **Input:**
  - session_id
  - comment_text
  - context_field (optional)
- **Output:**
  - comment_id
- **Flow:** Passed to assistants for intent parsing

---

## 4. Assistants (Silent Workers)

### Job-Scoped Assistants

**Endpoint:** `POST /api/assistant/structure`
- **Purpose:** Parse intent into structured config
- **Input:**
  - session_id
  - raw_intent (conversation + form data)
- **Output:**
  - structured_config
  - validation_status
- **Scope:** Structure Assistant only

**Endpoint:** `POST /api/assistant/voice`
- **Purpose:** Prepare voice configuration
- **Input:**
  - structured_config
  - user_preferences
- **Output:**
  - voice_config (for POM)
  - tone_guidance (for Harmonizer)
- **Scope:** Voice Prep Assistant only

**Endpoint:** `POST /api/assistant/consent`
- **Purpose:** Validate consent boundaries
- **Input:**
  - structured_config
  - user_permissions
- **Output:**
  - consent_status
  - blocked_features (if any)
- **Scope:** Consent & Ethics Assistant only

**Endpoint:** `POST /api/assistant/validation`
- **Purpose:** Final validation before production
- **Input:**
  - complete_config
  - product_constraints
- **Output:**
  - validation_result
  - errors (if any)
- **Scope:** All assistants coordinate

**Critical Rule:** Assistants never communicate directly with users.

---

## 5. Mini-SKG (Per Host)

**Endpoint:** `POST /api/miniskg/write`
- **Purpose:** Store structured intent, preferences, patterns
- **Input:**
  - session_id
  - learning_data
  - category (prompt_timing | option_ordering | error_patterns | workflow_efficiency)
- **Output:**
  - write_confirmation
  - learning_version
- **Scope:** Job-specific only

**Endpoint:** `GET /api/miniskg/read`
- **Purpose:** Host recall for session context
- **Input:**
  - session_id
  - user_id
  - product_type
- **Output:**
  - prior_preferences
  - learned_patterns
  - suggested_defaults
- **Scope:** Session-scoped, never cross-product

**Endpoint:** `POST /api/miniskg/close`
- **Purpose:** Finalize learning for audit + Caleon feed-up
- **Input:**
  - session_id
  - final_learning
- **Output:**
  - audit_log_id
  - caleon_feed_id
- **Flow:** Distilled learning → Caleon harmonization

---

## 6. Core Production Pipeline (UNCHANGED)

### Symbolic Generation

**Endpoint:** `POST /api/llm/generate`
- **Purpose:** GPT4All local CPU model symbolic generation
- **Input:**
  - structured_config (from Mini-SKG)
  - product_type
  - context
- **Output:**
  - symbolic_script (text/structure only)
- **Rule:** No audio generation, no tone decisions

### Knowledge Storage

**Endpoint:** `POST /api/skg/store`
- **Purpose:** Persist configuration + structure
- **Input:**
  - symbolic_script
  - product_config
  - session_metadata
- **Output:**
  - skg_id
  - storage_path
- **Format:** JSON (SKG format)

### Tone Arbitration

**Endpoint:** `POST /api/harmonizer/decide`
- **Purpose:** Gyro-Cortical Harmonizer tone decisions
- **Input:**
  - symbolic_script
  - voice_config
  - emotion_guidance
- **Output:**
  - phonatory_parameters (pitch, cadence, formant targets)
- **Rule:** Tone layer only, no content changes

### Voice Output

**Endpoint:** `POST /api/pom/synthesize`
- **Purpose:** Phonatory Output Module (Coqui TTS) synthesis
- **Input:**
  - symbolic_script
  - phonatory_parameters
  - voice_config
- **Output:**
  - audio_file_path (WAV)
- **Rule:** Biological voice synthesis, no content generation

---

## 7. Delivery & Refinement

**Endpoint:** `POST /api/output/present`
- **Purpose:** Host receives completed asset
- **Input:**
  - session_id
  - output_file_path
  - production_metadata
- **Output:**
  - presentation_data (for user display)
  - host_commentary
- **Flow:** Host presents to user conversationally

**Endpoint:** `POST /api/output/refine`
- **Purpose:** User requests changes
- **Input:**
  - session_id
  - output_id
  - refinement_request
- **Output:**
  - new_job_id
  - estimated_time
- **Flow:** Loops back through pipeline

**Endpoint:** `POST /api/output/accept`
- **Purpose:** User confirms completion
- **Input:**
  - session_id
  - output_id
  - user_rating (optional)
- **Output:**
  - final_output_id
  - download_links
- **Audit:** Completion logged

---

## 8. Legacy Assemblies (Restricted)

**Endpoint:** `POST /api/legacy/upload`
- **Purpose:** Upload media files
- **Input:**
  - user_id
  - files (audio/video/photo)
  - metadata (optional)
- **Output:**
  - upload_id
  - storage_confirmation
- **Rule:** No processing without explicit consent

**Endpoint:** `POST /api/legacy/assemble`
- **Purpose:** Assemble archive with consent
- **Input:**
  - upload_ids
  - structure_choice (chronological | thematic)
  - music_opt_in (boolean)
- **Output:**
  - assembly_id
  - preview_link
- **Rule:** User-driven assembly only

**Endpoint:** `GET /api/legacy/archive`
- **Purpose:** Retrieve private archive
- **Input:**
  - user_id
  - archive_id
- **Output:**
  - archive_data
  - access_log (audit)
- **Privacy:** Hard-locked, user-only access

**Endpoint:** `POST /api/legacy/export`
- **Purpose:** Export to external format
- **Input:**
  - archive_id
  - format (mp4 | zip | pdf)
- **Output:**
  - export_file_path
- **Rule:** No cloud upload without consent

**Critical Rules:**
- ❌ No generation endpoints
- ❌ No optimization endpoints
- ❌ No revenue tracking
- ✅ Privacy hard-locked

---

## 9. Caleon Supervision Layer

**Endpoint:** `POST /api/caleon/observe`
- **Purpose:** Receive distilled Mini-SKG learning
- **Input:**
  - mini_skg_feed
  - product_type
  - timestamp
- **Output:**
  - acknowledgment
  - harmonization_status
- **Flow:** Caleon harmonizes cross-product learning

**Endpoint:** `POST /api/caleon/escalate`
- **Purpose:** Trigger floating block appearance
- **Input:**
  - session_id
  - escalation_type (ethical | consent | emotional | boundary)
  - context
- **Output:**
  - caleon_intervention_id
  - intervention_script
- **Flow:** Caleon appears in user interface

**Endpoint:** `POST /api/caleon/harmonize`
- **Purpose:** Cross-product learning merge
- **Input:**
  - learning_feeds (from multiple Mini-SKGs)
  - harmonization_rules
- **Output:**
  - harmonized_knowledge
  - distribution_plan
- **Scope:** Supervisor-level only

---

## 10. Vault & Audit

**Endpoint:** `POST /api/vault/log`
- **Purpose:** Log every host action
- **Input:**
  - session_id
  - action_type
  - actor (host | user | assistant)
  - timestamp
  - context
- **Output:**
  - log_id
- **Storage:** Immutable

**Endpoint:** `POST /api/vault/learning`
- **Purpose:** Mini-SKG → immutable record
- **Input:**
  - mini_skg_snapshot
  - session_id
  - version
- **Output:**
  - vault_id
- **Purpose:** Audit trail for learning

**Endpoint:** `GET /api/vault/audit`
- **Purpose:** Admin-only review
- **Input:**
  - query_params (date_range | user_id | product_type)
  - admin_token
- **Output:**
  - audit_records
- **Permissions:** Master Control Center only

---

## 11. Admin / Master Control Center

**Endpoint:** `GET /api/admin/health`
- **Purpose:** System health check
- **Output:**
  - api_status
  - database_status
  - storage_status
  - cache_status
  - pom_status
  - harmonizer_status

**Endpoint:** `GET /api/admin/hosts`
- **Purpose:** View all Bubble Hosts status
- **Output:**
  - host_list (with active sessions, learning stats)

**Endpoint:** `GET /api/admin/products`
- **Purpose:** Product analytics
- **Output:**
  - product_breakdown (active | in_progress | published per product)

**Endpoint:** `GET /api/admin/escalations`
- **Purpose:** View Caleon interventions
- **Output:**
  - escalation_log
  - resolution_status

**Endpoint:** `GET /api/admin/audit`
- **Purpose:** Full system audit access
- **Input:**
  - query_params
- **Output:**
  - audit_trail

**Permissions:** admin@goat.local only

---

## 12. Deployment (DALS Forge)

**Endpoint:** `POST /api/dals/host/deploy`
- **Purpose:** Deploy new Bubble Host instance
- **Input:**
  - host_definition
  - product_type
  - version
  - plugins
- **Output:**
  - deployment_id
  - host_status

**Endpoint:** `POST /api/dals/host/update`
- **Purpose:** Update existing host configuration
- **Input:**
  - host_id
  - update_package
  - version_bump
- **Output:**
  - update_status

**Endpoint:** `POST /api/dals/plugin/register`
- **Purpose:** Register assistant plugin
- **Input:**
  - plugin_definition
  - capabilities
  - constraints
- **Output:**
  - plugin_id
  - registration_status

**Endpoint:** `GET /api/dals/host/status`
- **Purpose:** Check deployment status
- **Input:**
  - host_id
- **Output:**
  - version
  - health
  - active_sessions
  - learning_stats

---

## Implementation Phases

### Phase 1: MVP (Minimal Viable Product)
- Entry & Routing (Concierge)
- Session Control (start/end only)
- Manual Input (draft/override)
- Core Pipeline (unchanged, existing)
- Vault (basic logging)

### Phase 2: Conversational Layer
- Session messaging
- Assistants (silent workers)
- Mini-SKG (write/read)
- Delivery & Refinement

### Phase 3: Supervision
- Caleon observation
- Caleon escalation
- Caleon harmonization

### Phase 4: Full Deployment
- DALS Forge integration
- Plugin system
- Advanced analytics

---

## Critical Rules

1. **Manual intent always wins** - Override endpoints never blocked
2. **Assistants are silent** - Never talk to users directly
3. **Mini-SKGs are scoped** - Cannot generalize across products
4. **Legacy is hard-locked** - No generation, no optimization
5. **Caleon supervises all** - Receives distilled learning from all hosts
6. **Pipeline unchanged** - GPT4All → SKG → Harmonizer → POM remains intact

---

**Status:** Architecture locked. Ready for backend implementation planning.

**Next:** Backend routing table, API versioning strategy, authentication layer.

---

## 📄 Copyright

Copyright © 2025-2026 PRo Prime Series and GOAT, in association with TrueMark Mint LLC. All rights reserved.
