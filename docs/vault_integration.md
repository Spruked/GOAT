# Vault System Integration (Vault_System_1.0)

This document explains how to integrate Caleon's Vault System (Vault_System_1.0) into the GOAT workspace.

## Overview
The Vault System is an advanced, plug-and-play cognitive framework developed separately. It can be used in two ways:

1. Run as a separate service (recommended) — build and run the provided Docker image and connect to it via API/dashboard.
2. Import and embed as a Python package inside GOAT (optional) — this will instantiate `AdvancedVaultSystem` inside GOAT's process. Use with caution (resource and dependency impacts).

## Steps to enable embedded integration (optional)

1. Clone the repository inside the GOAT workspace (already done at `external_repos/Vault_System_1.0`):

```pwsh
cd t:\GOAT
git clone https://github.com/Spruked/Vault_System_1.0.git external_repos\Vault_System_1.0
```

2. Install Vault System dependencies into the GOAT virtual environment (this may downgrade/upgrade shared packages):

```pwsh
t:\GOAT\.venv\Scripts\pip.exe install -r t:\GOAT\external_repos\Vault_System_1.0\requirements.txt
```

Note: The Vault System pins certain package versions (FastAPI, Pydantic, etc.). Installing them may conflict with GOAT's own dependencies. Consider running the Vault System in a separate container if you want to avoid dependency conflicts.

3. Enable the integration in GOAT by setting environment variables in `.env` or in your environment:

```
VAULT_SYSTEM_ENABLE=true
VAULT_SYSTEM_MASTER_KEY=your_master_key_here
```

4. The GOAT server (`server/main.py`) will detect the `external_repos/Vault_System_1.0/vault_system` path, add it to `sys.path`, and if `VAULT_SYSTEM_ENABLE` is true it will start `AdvancedVaultSystem` in a background thread. The telemetry dashboard runs on port `8001` by default.

## Recommended (safer) approach — run Vault System as a separate container

1. Build the Docker image provided in the repo:

```pwsh
cd t:\GOAT\external_repos\Vault_System_1.0
docker build -t vault-system .
```

2. Run the container:

```pwsh
docker run -p 8001:8001 vault-system
```

3. Use the dashboard at `http://localhost:8001` and connect programmatically via the Vault System's Python API or build a small adapter service to expose RPC/HTTP endpoints for GOAT.

## Quick tests
- Import test (no start):

```pwsh
python -c "import sys; sys.path.insert(0, r't:\\GOAT\\external_repos\\Vault_System_1.0\\vault_system'); import plug_and_play_integration; print('import OK')"
```

- Start embedded (BE CAREFUL — runs services and dashboard in-process): set `VAULT_SYSTEM_ENABLE=true` and start GOAT server.

## Notes & Caveats
- Dependency changes may affect GOAT. If you see package conflicts, consider containerizing Vault System separately.
- The embedded startup is optional and non-blocking. The server will continue to operate if the Vault System import fails.
- If you want a tighter integration (expose Vault functionality in GOAT endpoints), we can add a thin adapter route module that proxies selected Vault API calls (status, lifecycle control, reasoning start/complete) from GOAT to the Vault System instance.

## Next steps (suggested)
- Create a small adapter `routes/vault_adapter.py` that exposes safe operations (status, start/stop components, start reasoning path) and routes calls to the `VAULT_SYSTEM_INSTANCE` when present.
- Add health checks for the Vault system under `/api/vault/system/status`.
- Add CI or Docker Compose orchestration to bring up both GOAT and Vault System together.
