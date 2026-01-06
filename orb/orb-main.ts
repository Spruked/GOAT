// orb/orb-main.ts
/**
 * Orb CALI Main Process Integration
 * Handles screen capture, file access, and CALI backend communication
 */

import { ipcMain, BrowserWindow, desktopCapturer } from 'electron';
import * as fs from 'fs';
import * as path from 'path';

interface OrbSession {
  userId: string;
  escalationData: any;
  screenStream?: Electron.DesktopCapturerSource;
  permissions: {
    screenShare: boolean;
    fileAccess: boolean;
  };
  startTime: Date;
}

export class OrbMainIntegration {
  private activeSessions: Map<string, OrbSession> = new Map();

  constructor(private goatRootPath: string) {
    this.setupIPCHandlers();
  }

  private setupIPCHandlers(): void {
    // Escalation detection
    ipcMain.handle('escalation:check', async (event, data) => {
      return await this.handleEscalationCheck(data);
    });

    // Start Orb session
    ipcMain.handle('orb:start-session', async (event, escalationData) => {
      return await this.startOrbSession(escalationData);
    });

    // Screen access granted
    ipcMain.on('orb:screen-access-granted', (event, data) => {
      this.handleScreenAccessGranted(data.userId, data.streamId, data.permissions);
    });

    // File access request
    ipcMain.handle('orb:file-access-request', async (event, data) => {
      return await this.grantFileAccess(data.userId);
    });

    // Screen capture request (safer than renderer direct access)
    ipcMain.on('orb:request-screen-capture', (event, data) => {
      this.handleScreenCaptureRequest(event.sender, data);
    });

    // Chat mode
    ipcMain.on('orb:chat-mode-started', (event, data) => {
      this.handleChatMode(data.userId, data.escalationData);
    });

    // Dismissed
    ipcMain.on('orb:dismissed', (event, data) => {
      this.endOrbSession(data.userId);
    });

    // Human escalation
    ipcMain.on('orb:request-human-escalation', (event, data) => {
      this.initiateHumanEscalation(data.userId, data.context);
    });
  }

  private async startOrbSession(escalationData: any): Promise<{ success: boolean; sessionId: string }> {
    const sessionId = `orb_${escalationData.userId}_${Date.now()}`;

    const session: OrbSession = {
      userId: escalationData.userId,
      escalationData,
      permissions: { screenShare: false, fileAccess: false },
      startTime: new Date()
    };

    this.activeSessions.set(sessionId, session);

    console.log(`[ORB] Session started for user ${escalationData.userId}, priority: ${escalationData.priority}`);

    // Log to CALI's immutable matrix
    this.logToCALIMatrix(sessionId, 'orb_session_started', escalationData);

    return {
      success: true,
      sessionId
    };
  }

  private async handleScreenAccessGranted(
    userId: string,
    streamId: string,
    permissions: { screenShare: boolean; fileAccess: boolean }
  ): Promise<void> {
    const session = this.findSessionByUserId(userId);
    if (!session) return;

    session.permissions = permissions;

    console.log(`[ORB] Screen access granted for user ${userId}`);

    // In production: send stream to CALI's analysis engine
    // For now, log the permission grant
    this.logToCALIMatrix(userId, 'screen_access_granted', {
      streamId,
      permissions
    });

    // Notify CALI backend to start screen analysis
    this.notifyCALIBackend('screen_analysis_start', {
      userId,
      sessionId: `orb_${userId}`,
      permissions
    });
  }

  private async handleScreenCaptureRequest(sender: Electron.WebContents, data: any): Promise<void> {
    try {
      // Use desktopCapturer for Electron screen access
      const sources = await desktopCapturer.getSources({
        types: ['screen', 'window'],
        thumbnailSize: { width: 150, height: 150 }
      });

      // For now, just grant access and let CALI backend handle analysis
      // In production, you might want to show source selection UI
      const primaryScreen = sources.find(source => source.name === 'Entire Screen' || source.name === 'Screen 1');

      if (primaryScreen) {
        // Store session info
        const session = this.findSessionByUserId(data.userId);
        if (session) {
          session.screenStream = primaryScreen;
          session.permissions.screenShare = true;
        }

        // Notify renderer of success
        sender.send('orb:screen-capture-result', {
          success: true,
          sourceId: primaryScreen.id
        });

        // Notify CALI backend
        this.notifyCALIBackend('screen_capture_granted', {
          userId: data.userId,
          sourceId: primaryScreen.id,
          permissions: data.permissions
        });
      } else {
        sender.send('orb:screen-capture-result', {
          success: false,
          error: 'No screen sources available'
        });
      }

    } catch (error) {
      console.error('Screen capture error:', error);
      sender.send('orb:screen-capture-result', {
        success: false,
        error: error.message
      });
    }
  }

  private async grantFileAccess(userId: string): Promise<{ success: boolean; grantedPath?: string }> {
    const session = this.findSessionByUserId(userId);
    if (!session) return { success: false };

    const userProjectsPath = path.join(this.goatRootPath, 'users', 'active', userId, 'projects');

    // Ensure directory exists
    if (!fs.existsSync(userProjectsPath)) {
      fs.mkdirSync(userProjectsPath, { recursive: true });
    }

    console.log(`[ORB] File access granted for user ${userId} at ${userProjectsPath}`);

    this.logToCALIMatrix(userId, 'file_access_granted', {
      path: userProjectsPath
    });

    return {
      success: true,
      grantedPath: userProjectsPath
    };
  }

  private handleChatMode(userId: string, escalationData: any): void {
    console.log(`[ORB] Chat-only mode for user ${userId}`);

    this.notifyCALIBackend('chat_mode_only', {
      userId,
      escalationData
    });
  }

  private initiateHumanEscalation(userId: string, context: any): void {
    console.log(`[ORB] Human escalation initiated for user ${userId}`);

    // Log to CALI
    this.logToCALIMatrix(userId, 'human_escalation_initiated', {
      context,
      orbSessionDuration: Date.now() - this.findSessionByUserId(userId)?.startTime.getTime()
    });

    // Here you would:
    // 1. Create support ticket
    // 2. Notify human agents
    // 3. Transfer full context
    // 4. Schedule callback if needed

    this.notifyCALIBackend('request_human_handoff', {
      userId,
      context,
      priority: context.escalationData.priority
    });
  }

  private endOrbSession(userId: string): void {
    const session = this.findSessionByUserId(userId);
    if (!session) return;

    const duration = Math.floor((Date.now() - session.startTime.getTime()) / 1000);

    console.log(`[ORB] Session ended for user ${userId}, duration: ${duration}s`);

    this.logToCALIMatrix(userId, 'orb_session_ended', {
      duration,
      permissions_granted: session.permissions,
      resolution_status: 'user_dismissed'
    });

    // Clean up screen stream if exists
    if (session.screenStream) {
      // @ts-ignore
      session.screenStream.thumbnail?.resize({ width: 0, height: 0 });
    }

    // Remove from active sessions
    for (const [sessionId, sess] of this.activeSessions.entries()) {
      if (sess.userId === userId) {
        this.activeSessions.delete(sessionId);
        break;
      }
    }
  }

  private findSessionByUserId(userId: string): OrbSession | undefined {
    for (const session of this.activeSessions.values()) {
      if (session.userId === userId) {
        return session;
      }
    }
    return undefined;
  }

  private logToCALIMatrix(userId: string, eventType: string, data: any): void {
    const logEntry = {
      timestamp: new Date().toISOString(),
      userId,
      eventType,
      data,
      source: 'orb_integration'
    };

    // In production: write to UCM_4_Core/CALI/cali_immutable_matrix/
    const logPath = path.join(this.goatRootPath, 'logs', 'orb_cali');
    if (!fs.existsSync(logPath)) {
      fs.mkdirSync(logPath, { recursive: true });
    }

    const logFile = path.join(logPath, `orb_log_${new Date().toISOString().split('T')[0]}.jsonl`);
    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
  }

  private async handleEscalationCheck(data: any): Promise<any> {
    // Call Python EscalationDetector via subprocess
    const { spawn } = require('child_process');
    const pythonPath = path.join(this.goatRootPath, '.venv', 'Scripts', 'python.exe');

    return new Promise((resolve, reject) => {
      const pythonProcess = spawn(pythonPath, [
        '-c',
        `
import sys
import json
sys.path.insert(0, r"${this.goatRootPath}")

from escalation.escalation_detector import EscalationDetector
from pathlib import Path

detector = EscalationDetector(Path(r"${data.goatRootPath}"))
result = detector.should_escalate_to_orb(
    "${data.userId}",
    "${data.userInput}",
    ${JSON.stringify(data.workerContext)}
)
print(json.dumps(result))
        `
      ], { cwd: this.goatRootPath });

      let output = '';
      let errorOutput = '';

      pythonProcess.stdout.on('data', (data: Buffer) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data: Buffer) => {
        errorOutput += data.toString();
      });

      pythonProcess.on('close', (code: number) => {
        if (code === 0) {
          try {
            resolve(JSON.parse(output.trim()));
          } catch (e) {
            reject(new Error('Failed to parse escalation result'));
          }
        } else {
          reject(new Error(`Escalation check failed: ${errorOutput}`));
        }
      });

      pythonProcess.on('error', (error: Error) => {
        reject(error);
      });
    });
  }

  private notifyCALIBackend(eventType: string, data: any): void {
    // In production: Send to CALI's API endpoint
    // For now, console.log
    console.log(`[CALI Backend] ${eventType}:`, data);
  }
}