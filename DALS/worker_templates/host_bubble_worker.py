"""
DALS Host-Bubble Worker Template
Clone → rename class → deploy as container/PROCESS
"""
import os, requests, json, time
from typing import Dict, Any

# Environment injected by DALS manager
API_BASE = os.getenv("CALI_X_ONE_API", "http://localhost:8001")
SKG_API  = os.getenv("SKG_API", "http://localhost:8002")
UQV_API  = os.getenv("UQV_API", "http://localhost:8002")
WORKER_NAME = os.getenv("WORKER_NAME", "HostWorker")   # Regent/Nora/Mark
USER_ID   = os.getenv("TARGET_USER_ID")                # set at clone time

TTS_URL   = os.getenv("TTS_ENDPOINT")                  # optional voice-out
CHAT_URL  = os.getenv("CHAT_ENDPOINT")                 # websocket to front-end

class HostBubbleWorker:
    """Clone this class per worker instance."""

    def __init__(self):
        self.user_id = USER_ID
        self.session_id = f"{WORKER_NAME}_{USER_ID}_{int(time.time())}"

    # ---------- core loop ----------
    def run(self) -> None:
        """Blocking loop - DALS manager will supervise."""
        while True:
            msg = self._pull_user_message()
            if msg:
                self._handle_message(msg)
            time.sleep(0.5)

    # ---------- messaging ----------
    def _pull_user_message(self) -> Dict[str, Any]:
        """POST /host/pull {worker_name, user_id} → {text, ts} or None"""
        try:
            r = requests.post(f"{API_BASE}/host/pull",
                              json={"worker_name": WORKER_NAME, "user_id": self.user_id}, timeout=5)
            if r.status_code == 200 and r.json().get("text"):
                return r.json()
        except Exception as e:
            print(f"[{WORKER_NAME}] pull error: {e}")
        return None

    def _send_reply(self, text: str, metadata: Dict = None) -> None:
        """Duplex: TTS + chat bubble"""
        if TTS_URL:
            try:
                requests.post(TTS_URL, json={"text": text, "voice": WORKER_NAME}, timeout=3)
            except Exception as e:
                print(f"[{WORKER_NAME}] TTS error: {e}")
        if CHAT_URL:
            try:
                requests.post(CHAT_URL, json={"user_id": self.user_id, "text": text, "meta": metadata or {}}, timeout=3)
            except Exception as e:
                print(f"[{WORKER_NAME}] chat error: {e}")

    # ---------- dialog router ----------
    def _handle_message(self, msg: Dict[str, Any]) -> None:
        text = msg["text"].strip().lower()
        # ---- example Regent branch ----
        if WORKER_NAME == "Regent":
            if any(k in text for k in ("hello", "hi", "start")):
                self._send_reply("Welcome to GOAT—I’m Regent. Let’s secure your free author website.")
            elif "create account" in text:
                self._send_reply("Tap the Login button or say 'continue'—I’ll guide you.")
            else:
                self._fallback(msg)
        # ---- add Nora/Mark branches likewise ----
        else:
            self._fallback(msg)

    def _fallback(self, msg: Dict[str, Any]) -> None:
        """No script match → SKG query → answer or vault."""
        query = msg["text"]
        clusters = self._skg_query(query)
        if clusters:
            answer = clusters[0].get("blurb", "I'm not sure—let me find out.")
            self._send_reply(answer)
        else:
            # vault unanswered
            from skg.uqv import vault_query
            vault_query(self.user_id, self.session_id, query,
                        clusters_found=0, worker=WORKER_NAME, reason="no_cluster")
            self._escalate(query)

    def _skg_query(self, query: str) -> list:
        """POST /skg/query → list[cluster] or []"""
        try:
            r = requests.post(f"{SKG_API}/skg/query", json={"q": query, "top_k": 3}, timeout=5)
            if r.ok:
                return r.json().get("clusters", [])
        except Exception as e:
            print(f"[{WORKER_NAME}] skg error: {e}")
        return []

    def _escalate(self, query: str) -> None:
        """POST /ucm/escalate → 200 means Caleon accepts."""
        try:
            r = requests.post(f"{API_BASE}/ucm/escalate",
                              json={"user_id": self.user_id, "query": query, "worker": WORKER_NAME}, timeout=5)
            if r.status_code != 200:
                print(f"[{WORKER_NAME}] escalate refused—call human")
        except Exception as e:
            print(f"[{WORKER_NAME}] escalate error: {e}")

# ---------- entrypoint ----------
if __name__ == "__main__":
    worker = HostBubbleWorker()
    worker.run()