// Shared constants for UCM naming and presence rules
// These must not be changed without updating POLICY.md

export const UCM_LINEAGE = "UCM";
export const CURRENT_INSTANTIATION = "UCM_4_Core — CALI";
export const PRESENCE_LAYER = "Cali Caleon";

// Orb rendering rules
export const ORB_ADMIN_CONTEXT = "global presence layer within UCM_4_Core — CALI";
export const ORB_USER_CONTEXT = "hidden by default";
export const CLICK_NOT_ESCALATION = true; // Clicking the orb is NOT escalation

// Behavior rules
export const NO_GUARDIAN_LANGUAGE = true; // Enforce no "Guardian" language
export const NO_AUTHORITY = true; // No implied authority, force, etc.
export const NO_SIMULATION_LANGUAGE = true; // No "simulation"; use "response generation"

// Service-specific messages
export const GOAT_MESSAGE = "Cali Caleon is a global admin presence, not a GOAT feature. GOAT exposes tools; Cali observes by invitation.";
export const DALS_MESSAGE = "DALS transports and reports status. It does not speak as Cali and does not infer intent.";
export const MINTS_MESSAGE = "Mints certify lineage (UCM) and alignment (CALI). They do not imply agency or guardianship.";

// Directive summary
export const DIRECTIVE_SUMMARY = "Naming drift is a bug. Presence is intentional. Consent is explicit.";