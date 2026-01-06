// orb/orb-integration-example.ts
/**
 * Example: How to integrate Orb CALI escalation system
 * This shows the complete flow from bubble to Orb
 */

// In your main renderer file (e.g., main.ts or app.ts):

import { BubbleToOrbBridge } from './bubble/bubble-bridge';
import { OrbCaliInterface } from './orb/orb-renderer';

// Initialize when user logs in
let bubbleBridge: BubbleToOrbBridge;
let currentUserId: string;

function initializeOrbSystem(userId: string, goatRootPath: string) {
  currentUserId = userId;
  bubbleBridge = new BubbleToOrbBridge(userId, goatRootPath);
}

// When user sends a message to bubble assistant:
async function handleUserMessageToBubble(userInput: string, workerResponses: any[]) {
  // First, check if this should escalate to Orb
  const { handoffToOrb, orbData } = await bubbleBridge.processUserInput(userInput, workerResponses);

  if (handoffToOrb && orbData) {
    // 3. Initialize Orb CALI
    const orb = new OrbCaliInterface(orbData);

    // 4. Orb takes over - bubble is hidden
    // 5. User now interacts with CALI, not bubble
    console.log('Escalated to Orb CALI');
    return;
  }

  // Continue with normal bubble processing
  console.log('Continue with bubble assistant');
}

// In your Electron main process:

import { OrbMainIntegration } from './orb/orb-main';

function initializeMainProcess(goatRootPath: string) {
  const orbIntegration = new OrbMainIntegration(goatRootPath);

  // Orb integration is now active and listening for IPC events
}

// Example escalation triggers:

// 1. VIP user types "help"
const vipUserInput = "help";
const vipWorkerResponses = []; // Workers couldn't help
// -> Escalates to Orb with high priority

// 2. User has 3+ unanswered questions across workers
const frustratedUserInput = "this isn't working";
const frustratedWorkerResponses = [
  { worker: 'signup', response: 'I don\'t know' },
  { worker: 'onboarding', response: 'unclear' },
  { worker: 'content', response: 'not specified' }
];
// -> Escalates due to temp_vault_fill_rate

// 3. User explicitly asks for human
const explicitRequest = "can I talk to a human?";
const explicitResponses = [];
// -> Escalates due to explicit_user_request

// 4. Enterprise user with any issue
const enterpriseUserInput = "having trouble with the interface";
const enterpriseResponses = [];
// -> Auto-escalates due to enterprise tier

// Orb then provides:
// - Screen sharing capability
// - File access to project directory
// - Direct CALI backend integration
// - Human escalation when needed
// - Cursor-aware positioning
// - Distinct visual identity from bubble

export { initializeOrbSystem, handleUserMessageToBubble, initializeMainProcess };