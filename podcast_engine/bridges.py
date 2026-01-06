# bridges.py
"""
UCM and DALS Integration Bridges
"""

import requests
from typing import Dict, Any

class UCMBridge:
    """
    UCM = THINKING
    Use for: topic analysis, script expansion, summaries, segment structure, tone adjustments
    """
    
    def __init__(self, url: str = "http://localhost:8080/ucm"):
        self.url = url
        self.enabled = True
    
    def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send analysis request to UCM"""
        if not self.enabled:
            return {"status": "offline", "result": None}
        
        try:
            r = requests.post(f"{self.url}/analyze", json=payload, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[UCM Bridge] Connection failed: {e}")
            return {"status": "error", "error": str(e)}

class DALSBridge:
    """
    DALS = WORKERS / ROUTING
    Use for: background processing, worker assignment, file routing, logging, status tracking
    """
    
    def __init__(self, url: str = "http://localhost:9002/dals"):
        self.url = url
        self.enabled = True
    
    def dispatch(self, job_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch job to DALS worker system"""
        if not self.enabled:
            return {"status": "offline", "job_id": None}
        
        try:
            r = requests.post(f"{self.url}/dispatch/{job_type}", json=payload, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[DALS Bridge] Connection failed: {e}")
            return {"status": "error", "error": str(e)}
