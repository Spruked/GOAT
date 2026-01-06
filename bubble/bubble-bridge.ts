// bubble/bubble-bridge.ts
/**
 * Bridge between regular bubble assistant and Orb CALI
 * Detects escalation triggers and hands off to Orb
 */

import { ipcRenderer } from 'electron';
import { EscalationProxy } from '../escalation/escalation-proxy';

export class BubbleToOrbBridge {
  private escalationDetector: EscalationProxy;
  private userId: string;
  private conversationHistory: Array<{ input: string; timestamp: Date }> = [];

  constructor(userId: string, goatRootPath: string) {
    this.userId = userId;
    this.escalationDetector = new EscalationProxy(goatRootPath);
  }

  async processUserInput(userInput: string, workerResponses: any[]): Promise<{ handoffToOrb: boolean; orbData?: any }> {
    // Add to history
    this.conversationHistory.push({
      input: userInput,
      timestamp: new Date()
    });

    // Trim old history (> 1 hour)
    this.conversationHistory = this.conversationHistory.filter(
      entry => Date.now() - entry.timestamp.getTime() < 3600000
    );

    // Check for escalation
    const escalationCheck = await this.escalationDetector.shouldEscalateToOrb(
      this.userId,
      userInput,
      {
        workerResponses,
        conversationHistory: this.conversationHistory
      }
    );

    if (escalationCheck.escalate) {
      // Clear distinction: bubble says it's handing off
      this.showBubbleHandoffMessage(escalationCheck);

      // Prepare Orb data
      const orbData = {
        escalationData: escalationCheck,
        initialPosition: this.calculateOrbPosition(),
        timestamp: new Date().toISOString()
      };

      return {
        handoffToOrb: true,
        orbData
      };
    }

    return { handoffToOrb: false };
  }

  private showBubbleHandoffMessage(escalationCheck: any): void {
    // Bubble host clearly states it's escalating
    const bubbleMessage = `
      I'm connecting you with CALI, my advanced counterpart, who has deeper access to your
      account and can see your screen (with permission). She'll resolve this more directly.

      **Escalation reason:** ${escalationCheck.reason}
      **Priority:** ${escalationCheck.priority}
    `;

    // Display in bubble UI
    this.renderBubbleResponse(bubbleMessage);

    // Animate bubble transitioning out
    setTimeout(() => {
      this.animateBubbleHandoff();
    }, 3000);
  }

  private calculateOrbPosition(): { x: number; y: number } {
    // Calculate where Orb should appear based on current UI state
    // This is passed to Orb so it can appear intelligently
    return {
      x: window.innerWidth - 350,
      y: window.innerHeight * 0.3
    };
  }

  private animateBubbleHandoff(): void {
    const bubble = document.getElementById('bubble-host');
    if (bubble) {
      bubble.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      bubble.style.opacity = '0';
      bubble.style.transform = 'scale(0.8)';
    }
  }

  private renderBubbleResponse(message: string): void {
    // Implementation depends on your bubble UI
    console.log('[Bubble] Handoff message:', message);
  }
}