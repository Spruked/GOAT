# routes/vault_adapter.py
"""
Thin adapter to control and monitor the embedded Vault System when present.
This is intentionally lightweight and uses runtime imports to avoid circular imports.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import os
import threading

router = APIRouter(tags=["vault-adapter"])

def _get_server_module():
    # Import server.main at call time to avoid circular import during module load
    import importlib
    server_main = importlib.import_module('server.main')
    return server_main

@router.get("/api/vaultsystem/status")
async def vaultsystem_status() -> Dict[str, Any]:
    server_main = _get_server_module()
    present = getattr(server_main, 'VAULT_SYSTEM_DIR', None) is not None and getattr(server_main, 'VAULT_SYSTEM_DIR').exists()
    enabled_env = os.getenv('VAULT_SYSTEM_ENABLE', 'false').lower() in ('1', 'true', 'yes')
    started = getattr(server_main, 'VAULT_SYSTEM_INSTANCE', None) is not None

    status = {
        'present': bool(present),
        'enabled_env': bool(enabled_env),
        'started': bool(started),
    }

    if started:
        try:
            status['dashboard_url'] = server_main.VAULT_SYSTEM_INSTANCE.get_system_status().get('dashboard_url')
        except Exception:
            status['dashboard_url'] = None

    return status

@router.post("/api/vaultsystem/start")
async def vaultsystem_start() -> Dict[str, Any]:
    server_main = _get_server_module()
    if not getattr(server_main, 'VAULT_SYSTEM_DIR', None) or not server_main.VAULT_SYSTEM_DIR.exists():
        raise HTTPException(status_code=404, detail="Vault System code not found")

    if getattr(server_main, 'VAULT_SYSTEM_INSTANCE', None) is not None:
        return {"started": True, "message": "Vault System already started"}

    # Start in background
    def _start():
        master_key = os.getenv('VAULT_SYSTEM_MASTER_KEY', 'master_key_2024')
        try:
            server_main.VAULT_SYSTEM_INSTANCE = server_main.AdvancedVaultSystem(master_key)
        except Exception as e:
            # propagate error via logging; but return will be immediate
            print(f"Vault system start failed: {e}")

    threading.Thread(target=_start, daemon=True).start()

    return {"started": True, "message": "Starting Vault System in background"}

@router.post("/api/vaultsystem/stop")
async def vaultsystem_stop() -> Dict[str, Any]:
    server_main = _get_server_module()
    if getattr(server_main, 'VAULT_SYSTEM_INSTANCE', None) is None:
        return {"stopped": True, "message": "Vault System not running"}

    try:
        server_main.VAULT_SYSTEM_INSTANCE.graceful_shutdown()
        server_main.VAULT_SYSTEM_INSTANCE = None
        return {"stopped": True, "message": "Vault System shutdown initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
