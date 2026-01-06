# Orb CALI Escalation System

## Overview

The Orb CALI system provides advanced AI assistance when regular GOAT workers cannot resolve user issues. It creates a clear distinction from the bubble host with sophisticated UI, screen access capabilities, and direct human escalation paths.

## Architecture

### Components

1. **EscalationDetector** (`workers/escalation_detector.py`)
   - Monitors user interactions for escalation triggers
   - Checks user tier, frustration keywords, temp vault fill rates
   - Determines priority and escalation reason

2. **OrbCaliInterface** (`orb/orb-renderer.ts`)
   - Sophisticated UI component with cursor tracking
   - Screen sharing and file access permissions
   - Distinct visual identity from bubble host

3. **OrbMainIntegration** (`orb/orb-main.ts`)
   - Electron main process integration
   - Handles screen capture and file access
   - Logs to CALI's immutable matrix

4. **BubbleToOrbBridge** (`bubble/bubble-bridge.ts`)
   - Seamless handoff from bubble to Orb
   - Maintains conversation context
   - Animates transition between assistants

## Escalation Triggers

### Automatic Escalation
- **VIP/Enterprise users**: Immediate high-priority escalation
- **Temp vault saturation**: 3+ unanswered questions across workers
- **Repeated questions**: Same question asked 3+ times
- **Frustration detection**: Sentiment analysis (placeholder)

### User-Requested Escalation
- Explicit keywords: "help", "support", "agent", "human", "someone"
- Direct requests for assistance beyond worker capabilities

## Visual Distinctions

| Feature | Bubble Host | Orb CALI |
|---------|-------------|----------|
| **Identity** | "I'm your assistant" | "I am CALI, advanced support" |
| **Appearance** | Chat bubble, bottom-right | Materializing orb, intelligent positioning |
| **Access** | Worker knowledge only | Full UCM + screen/file access |
| **Voice** | Friendly, general | Authoritative, precise, capable |
| **Entry** | Simple slide-in | Dramatic materialization with pulse |
| **Cursor** | None | Active avoidance, attentive positioning |

## Usage Flow

```typescript
// 1. Initialize bridge when user logs in
const bubbleBridge = new BubbleToOrbBridge(userId, goatRootPath);

// 2. Check every user message for escalation
const { handoffToOrb, orbData } = await bubbleBridge.processUserInput(
  userInput, workerResponses
);

if (handoffToOrb) {
  // 3. Launch Orb CALI
  const orb = new OrbCaliInterface(orbData);
  // Bubble hides, Orb takes over
}
```

## Permissions & Security

### Screen Access
- User must explicitly grant permission
- Temporary access only during session
- Stream sent to CALI backend for analysis

### File Access
- Limited to user's project directory
- Read-only by default (configurable)
- Logged for audit purposes

### Human Escalation
- When CALI cannot resolve issue
- Full context transfer to human agents
- Priority-based routing

## Integration Points

### UCM Integration
- Logs all Orb interactions to immutable matrix
- Submits for continuous learning approval
- Maintains restricted learning principle

### Worker System
- Monitors temp vaults across all workers
- Escalates when workers collectively cannot help
- Provides worker context to CALI

### User Profiles
- Access to complete user context
- Spending history and tier information
- Activity tracking and preferences

## Development Notes

### File Structure
```
orb/
├── orb-renderer.ts      # UI component
├── orb-main.ts          # Electron integration
├── orb-styles.css       # Visual design
└── orb-integration-example.ts

bubble/
└── bubble-bridge.ts     # Handoff bridge

workers/
└── escalation_detector.py # Escalation logic
```

### Key Principles
1. **Clear Distinction**: Orb is visually and functionally distinct from bubble
2. **User Consent**: All permissions require explicit user approval
3. **Context Preservation**: Full conversation history transferred
4. **Graceful Degradation**: Falls back to chat-only if permissions denied
5. **Audit Trail**: All actions logged to CALI matrix

### Future Enhancements
- Sentiment analysis integration
- Advanced screen analysis with AI vision
- Voice interaction capabilities
- Multi-user session support
- Integration with external support systems