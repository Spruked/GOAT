// escalation/escalation-proxy.ts
/**
 * Thin proxy to expose EscalationDetector to frontend via IPC
 * Since EscalationDetector is Python, this proxies calls to main process
 */

import { ipcRenderer } from 'electron';

export class EscalationProxy {
  private goatRootPath: string;

  constructor(goatRootPath: string) {
    this.goatRootPath = goatRootPath;
  }

  async shouldEscalateToOrb(
    userId: string,
    userInput: string,
    workerContext: any = {}
  ): Promise<any> {
    return await ipcRenderer.invoke('escalation:check', {
      userId,
      userInput,
      workerContext,
      goatRootPath: this.goatRootPath
    });
  }
}