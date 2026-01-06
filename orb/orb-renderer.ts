// orb/orb-renderer.ts
/**
 * Orb CALI Entry Point - Sophisticated AI Assistant UI
 * Clear distinction from bubble host with:
 * - Dramatic entrance animation
 * - Cursor tracking intelligence
 * - Screen sharing capability
 * - Visual/audio presence that commands attention
 */

import { ipcRenderer } from 'electron';

interface OrbConfig {
  escalationData: {
    userId: string;
    priority: string;
    reason: string;
    userContext: any;
  };
  initialPosition: { x: number; y: number };
}

class OrbCaliInterface {
  private orbElement: HTMLElement | null = null;
  private cursorPosition: { x: number; y: number } = { x: 0, y: 0 };
  private screenAccessGranted: boolean = false;
  private isAttentive: boolean = false;
  private attentionThreshold: number = 150; // pixels

  constructor(private config: OrbConfig) {
    this.initializeOrb();
    this.setupCursorTracking();
    this.setupIPCListeners();
    this.setupScreenAccess();
  }

  private initializeOrb(): void {
    // Remove any existing bubble to make clear distinction
    const bubble = document.getElementById('bubble-host');
    if (bubble) {
      bubble.style.display = 'none';
    }

    // Create Orb container
    this.orbElement = document.createElement('div');
    this.orbElement.id = 'orb-cali-container';
    this.orbElement.className = 'orb-entrance';

    // Orb visual design - distinct from bubble
    this.orbElement.innerHTML = `
      <div class="orb-avatar">
        <div class="orb-pulse-ring"></div>
        <div class="orb-core">
          <div class="orb-eye left"></div>
          <div class="orb-eye right"></div>
        </div>
      </div>

      <div class="orb-dialogue orb-hidden">
        <div class="orb-header">
          <div class="orb-title">CALI Assistant</div>
          <div class="orb-subtitle">Advanced Support • Priority Response</div>
        </div>

        <div class="orb-content">
          <div class="orb-message" id="orb-message"></div>

          <div class="orb-action-bar">
            <button class="orb-btn orb-btn-primary" id="orb-assist-btn">
              Grant Temp Access for Assistance
            </button>
            <button class="orb-btn orb-btn-secondary" id="orb-chat-btn">
              Chat Only
            </button>
            <button class="orb-btn orb-btn-cancel" id="orb-dismiss-btn">
              Dismiss
            </button>
          </div>

          <div class="orb-permissions" id="orb-permissions" style="display: none;">
            <label class="orb-perm-label">
              <input type="checkbox" id="orb-screen-share" /> Screen Sharing
            </label>
            <label class="orb-perm-label">
              <input type="checkbox" id="orb-file-access" /> File Access (Current Project)
            </label>
            <button class="orb-btn orb-btn-confirm" id="orb-confirm-perms">
              Grant Selected Access
            </button>
          </div>
        </div>
      </div>

      <div class="orb-status-indicator orb-hidden" id="orb-status">
        <span class="orb-status-dot"></span>
        <span class="orb-status-text">Analyzing your situation...</span>
      </div>
    `;

    document.body.appendChild(this.orbElement);

    // Position Orb intelligently (not center screen - that's bubble behavior)
    this.positionOrbIntelligently();

    // Trigger entrance animation
    setTimeout(() => this.performEntrance(), 100);
  }

  private positionOrbIntelligently(): void {
    if (!this.orbElement) return;

    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    // For VIP users, appear at productive zone (top-right)
    // For frustrated users, appear in peripheral vision (bottom-right)
    // Never block center screen (bubble behavior)

    const isVip = this.config.escalationData.userContext?.tier === 'vip';
    const isFrustrated = this.config.escalationData.reason.includes('frustration');

    let targetX: number, targetY: number;

    if (isVip) {
      // Top-right, 50px margins
      targetX = screenWidth - 350; // Orb width ~300px
      targetY = 50;
    } else if (isFrustrated) {
      // Bottom-right, less intrusive
      targetX = screenWidth - 350;
      targetY = screenHeight - 200;
    } else {
      // Center-right, attention without blocking
      targetX = screenWidth - 380;
      targetY = screenHeight / 2 - 150;
    }

    this.orbElement.style.position = 'fixed';
    this.orbElement.style.left = `${targetX}px`;
    this.orbElement.style.top = `${targetY}px`;
    this.orbElement.style.zIndex = '9999';
  }

  private performEntrance(): void {
    // Clear distinction from bubble: dramatic, composed, authoritative
    // Not a "pop" but a "materialization"

    const avatar = this.orbElement?.querySelector('.orb-avatar');
    const dialogue = this.orbElement?.querySelector('.orb-dialogue');
    const status = this.orbElement?.querySelector('.orb-status-indicator');

    if (!avatar || !dialogue || !status) return;

    // Phase 1: Avatar materializes with pulse
    avatar.classList.add('orb-materialize');

    // Phase 2: Status indicator shows active processing
    setTimeout(() => {
      status.classList.remove('orb-hidden');
      this.updateStatus('Accessing your account and recent activity...');
    }, 500);

    // Phase 3: CALI introduces herself (distinct from bubble)
    setTimeout(() => {
      status.classList.add('orb-hidden');
      dialogue.classList.remove('orb-hidden');
      this.displayOrbMessage();
    }, 2000);

    // Phase 4: Begin cursor tracking
    setTimeout(() => {
      this.isAttentive = true;
      this.updateStatus('Ready to assist. I can see your screen position and will stay attentive.');
      status.classList.remove('orb-hidden');
    }, 3000);
  }

  private displayOrbMessage(): void {
    const messageEl = document.getElementById('orb-message');
    if (!messageEl) return;

    const { priority, reason, userContext } = this.config.escalationData;
    const name = userContext?.profile?.full_name || 'there';

    // Distinct CALI voice - more composed, direct, capable than bubble
    let message = `Hello ${name}, I'm CALI, your advanced support assistant. `;

    if (priority === 'high') {
      message += `I've been notified due to ${reason.replace(/_/g, ' ')}. `;
      message += `As a ${userContext?.tier || 'valued'} user, you're receiving priority engagement. `;
    } else {
      message += `I can see you're looking for assistance. I'm here to help more directly. `;
    }

    message += `I can guide you through this with full context of your account and current activity.`;

    messageEl.textContent = message;
  }

  private setupCursorTracking(): void {
    document.addEventListener('mousemove', (e) => {
      this.cursorPosition = { x: e.clientX, y: e.clientY };

      if (this.isAttentive && this.orbElement) {
        this.adjustOrbPosition();
      }
    });
  }

  private adjustOrbPosition(): void {
    if (!this.orbElement) return;

    const orbRect = this.orbElement.getBoundingClientRect();
    const distance = this.getDistanceToCursor(orbRect);

    // If cursor is too close, subtly shift Orb away (stay attentive but not blocking)
    if (distance < this.attentionThreshold) {
      const angle = Math.atan2(
        orbRect.top + orbRect.height/2 - this.cursorPosition.y,
        orbRect.left + orbRect.width/2 - this.cursorPosition.x
      );

      const shiftDistance = (this.attentionThreshold - distance) / 2;
      const deltaX = Math.cos(angle) * shiftDistance;
      const deltaY = Math.sin(angle) * shiftDistance;

      const currentLeft = parseFloat(this.orbElement.style.left || '0');
      const currentTop = parseFloat(this.orbElement.style.top || '0');

      this.orbElement.style.left = `${currentLeft + deltaX}px`;
      this.orbElement.style.top = `${currentTop + deltaY}px`;
    }
  }

  private getDistanceToCursor(orbRect: DOMRect): number {
    const orbCenterX = orbRect.left + orbRect.width / 2;
    const orbCenterY = orbRect.top + orbRect.height / 2;

    return Math.sqrt(
      Math.pow(orbCenterX - this.cursorPosition.x, 2) +
      Math.pow(orbCenterY - this.cursorPosition.y, 2)
    );
  }

  private setupScreenAccess(): void {
    const assistBtn = document.getElementById('orb-assist-btn');
    const chatBtn = document.getElementById('orb-chat-btn');
    const dismissBtn = document.getElementById('orb-dismiss-btn');

    assistBtn?.addEventListener('click', () => this.requestScreenAccess());
    chatBtn?.addEventListener('click', () => this.startChatOnly());
    dismissBtn?.addEventListener('click', () => this.dismissOrb());
  }

  private requestScreenAccess(): void {
    const permsDiv = document.getElementById('orb-permissions');
    if (!permsDiv) return;

    permsDiv.style.display = 'block';

    const confirmBtn = document.getElementById('orb-confirm-perms');
    confirmBtn?.addEventListener('click', () => {
      const screenShare = (document.getElementById('orb-screen-share') as HTMLInputElement)?.checked;
      const fileAccess = (document.getElementById('orb-file-access') as HTMLInputElement)?.checked;

      if (!screenShare && !fileAccess) {
        this.updateStatus('Please select at least one access type to proceed.');
        return;
      }

      this.grantTempAccess(screenShare, fileAccess);
    });
  }

  private async grantTempAccess(screenShare: boolean, fileAccess: boolean): Promise<void> {
    this.updateStatus('Requesting temporary access...');

    try {
      if (screenShare) {
        // Request screen capture via main process (safer for Electron)
        ipcRenderer.send('orb:request-screen-capture', {
          userId: this.config.escalationData.userId,
          permissions: { screenShare, fileAccess }
        });

        // Wait for main process response
        ipcRenderer.once('orb:screen-capture-result', (event, result) => {
          if (result.success) {
            this.screenAccessGranted = true;
            this.updateStatus('Screen access granted. CALI can now see your screen.');
          } else {
            this.updateStatus('Screen access denied. You can try again or use chat-only mode.');
          }
        });
      }

      if (fileAccess) {
        // Request access to current project directory
        ipcRenderer.send('orb:file-access-request', {
          userId: this.config.escalationData.userId
        });
      }

      // Close permissions UI, show active assistance
      document.getElementById('orb-permissions')?.style.setProperty('display', 'none');
      this.showActiveAssistanceMode();

    } catch (error) {
      this.updateStatus('Access denied or error occurred. You can try again or use chat-only mode.');
      console.error('Orb access error:', error);
    }
  }

  private showActiveAssistanceMode(): void {
    const messageEl = document.getElementById('orb-message');
    if (!messageEl) return;

    messageEl.textContent = `Temporary access granted. I'm now analyzing your screen and account activity to provide precise assistance. I'll only access what's needed to resolve this issue.`;

    // Add active indicator
    const avatar = this.orbElement?.querySelector('.orb-avatar');
    avatar?.classList.add('orb-active-assistance');
  }

  private startChatOnly(): void {
    this.updateStatus('Chat-only mode. CALI will assist through conversation.');

    const messageEl = document.getElementById('orb-message');
    if (messageEl) {
      messageEl.textContent += ` I'll guide you step-by-step without screen access.`;
    }

    ipcRenderer.send('orb:chat-mode-started', {
      userId: this.config.escalationData.userId,
      escalationData: this.config.escalationData
    });
  }

  private dismissOrb(): void {
    this.updateStatus('CALI dismissed. You can request help anytime from the Help menu.');

    setTimeout(() => {
      this.orbElement?.remove();

      // Restore bubble if it was hidden
      const bubble = document.getElementById('bubble-host');
      if (bubble) {
        bubble.style.display = 'block';
      }

      ipcRenderer.send('orb:dismissed', {
        userId: this.config.escalationData.userId,
        dismissedAt: new Date().toISOString()
      });
    }, 800);

    this.isAttentive = false;
  }

  private updateStatus(message: string): void {
    const statusEl = document.getElementById('orb-status');
    const statusText = statusEl?.querySelector('.orb-status-text');
    if (statusText) {
      statusText.textContent = message;
    }
  }

  private setupIPCListeners(): void {
    // Listen for CALI's analysis updates
    ipcRenderer.on('orb:analysis-update', (event, data) => {
      this.updateStatus(data.message);
    });

    // Listen for resolution
    ipcRenderer.on('orb:issue-resolved', (event, data) => {
      this.showResolutionDialog(data);
    });

    // Listen for human escalation recommendation
    ipcRenderer.on('orb:recommend-human-escalation', (event, data) => {
      this.showHumanEscalationOption(data);
    });
  }

  private showResolutionDialog(data: any): void {
    const messageEl = document.getElementById('orb-message');
    if (messageEl) {
      messageEl.textContent = `✓ Issue resolved: ${data.summary}\n\nIs there anything else I can help you with?`;
    }

    // Update buttons
    const actionBar = document.querySelector('.orb-action-bar');
    if (actionBar) {
      actionBar.innerHTML = `
        <button class="orb-btn orb-btn-primary" id="orb-continue-btn">Continue Working</button>
        <button class="orb-btn orb-btn-secondary" id="orb-new-issue-btn">New Issue</button>
      `;
    }
  }

  private showHumanEscalationOption(data: any): void {
    const messageEl = document.getElementById('orb-message');
    if (messageEl) {
      messageEl.textContent = `I've analyzed your issue and recommend connecting you with a human specialist for the best resolution. They'll have full context from our conversation.\n\nWait time: ~${data.estimatedWaitTime} minutes`;
    }

    const actionBar = document.querySelector('.orb-action-bar');
    if (actionBar) {
      actionBar.innerHTML = `
        <button class="orb-btn orb-btn-primary" id="orb-escalate-human">
          Connect with Specialist
        </button>
        <button class="orb-btn orb-btn-secondary" id="orb-keep-trying">
          Keep Troubleshooting with CALI
        </button>
      `;

      document.getElementById('orb-escalate-human')?.addEventListener('click', () => {
        ipcRenderer.send('orb:request-human-escalation', {
          userId: this.config.escalationData.userId,
          context: this.config.escalationData
        });
      });
    }
  }
}

// Export for use in main renderer
(window as any).OrbCaliInterface = OrbCaliInterface;