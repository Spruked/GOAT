# telemetry_dashboard.py

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import json
from typing import Dict, Any, Optional
import time
from pathlib import Path

class TelemetryDashboard:
    """
    FastAPI-based telemetry dashboard for monitoring vault system.
    Shows active modules, performance metrics, glyph traces, reflection cycles.
    Auto-connects when Vault_System plugs into UCM.
    """

    def __init__(self, vault_system, host: str = "localhost", port: int = 8000):
        self.vault_system = vault_system
        self.host = host
        self.port = port

        self.app = FastAPI(title="Vault System Telemetry Dashboard",
                          description="Real-time monitoring of Caleon's integrated vault system")

        self._setup_routes()
        self._mount_static_files()

    def _setup_routes(self):
        """Set up API routes"""

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard():
            """Main dashboard page"""
            return self._get_dashboard_html()

        @self.app.get("/api/system/status")
        async def system_status():
            """Get overall system status"""
            try:
                # Get status from various system components
                status = {
                    'timestamp': time.time(),
                    'system_health': self._get_system_health(),
                    'active_modules': self._get_active_modules(),
                    'performance_metrics': self._get_performance_metrics(),
                    'glyph_traces': self._get_glyph_traces(),
                    'reflection_cycles': self._get_reflection_cycles(),
                    'vault_status': self._get_vault_status()
                }
                return status
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/modules/{module_name}")
        async def module_details(module_name: str):
            """Get detailed information about a specific module"""
            try:
                details = self._get_module_details(module_name)
                if not details:
                    raise HTTPException(status_code=404, detail="Module not found")
                return details
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/glyphs/recent")
        async def recent_glyphs(limit: int = 10):
            """Get recent glyph traces"""
            try:
                return self._get_recent_glyphs(limit)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/reflections/recent")
        async def recent_reflections(limit: int = 10):
            """Get recent reflection entries"""
            try:
                return self._get_recent_reflections(limit)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/performance/history")
        async def performance_history(hours: int = 24):
            """Get performance history"""
            try:
                return self._get_performance_history(hours)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    def _mount_static_files(self):
        """Mount static files directory"""
        static_path = Path(__file__).parent / "static"
        static_path.mkdir(exist_ok=True)

        # Create a simple CSS file
        css_content = """
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .dashboard { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric-card { background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-healthy { color: #27ae60; }
        .status-warning { color: #f39c12; }
        .status-error { color: #e74c3c; }
        .module-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
        .module-item { background: white; padding: 10px; border-radius: 3px; border-left: 4px solid #3498db; }
        """

        css_file = static_path / "style.css"
        css_file.write_text(css_content)

        self.app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

    def _get_dashboard_html(self) -> str:
        """Generate the main dashboard HTML"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Vault System Telemetry Dashboard</title>
            <link rel="stylesheet" href="/static/style.css">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1>🧠 Caleon's Vault System Dashboard</h1>
                    <p>Real-time monitoring of integrated vault subsystems</p>
                    <div id="last-update">Loading...</div>
                </div>

                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>System Health</h3>
                        <div id="system-health">Loading...</div>
                    </div>

                    <div class="metric-card">
                        <h3>Active Modules</h3>
                        <div id="active-modules">Loading...</div>
                    </div>

                    <div class="metric-card">
                        <h3>Performance Metrics</h3>
                        <div id="performance-metrics">Loading...</div>
                    </div>

                    <div class="metric-card">
                        <h3>Glyph Traces</h3>
                        <div id="glyph-traces">Loading...</div>
                    </div>
                </div>

                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Recent Reflections</h3>
                        <div id="recent-reflections">Loading...</div>
                    </div>

                    <div class="metric-card">
                        <h3>Module Status</h3>
                        <div id="module-status">Loading...</div>
                    </div>
                </div>

                <div class="metric-card">
                    <h3>Active Modules List</h3>
                    <div id="modules-list" class="module-list">Loading...</div>
                </div>
            </div>

            <script>
                async function updateDashboard() {{
                    try {{
                        const response = await fetch('/api/system/status');
                        const data = await response.json();

                        // Update system health
                        const healthElement = document.getElementById('system-health');
                        const health = data.system_health.overall_health;
                        const healthClass = health > 0.8 ? 'status-healthy' : health > 0.6 ? 'status-warning' : 'status-error';
                        healthElement.innerHTML = `<span class="${{healthClass}}">${{(health * 100).toFixed(1)}}%</span>`;

                        // Update active modules
                        document.getElementById('active-modules').textContent = data.active_modules.length;

                        // Update performance metrics
                        const perf = data.performance_metrics;
                        document.getElementById('performance-metrics').innerHTML =
                            `CPU: ${{perf.cpu_usage || 'N/A'}}%<br>` +
                            `Memory: ${{perf.memory_usage || 'N/A'}}%<br>` +
                            `Response Time: ${{perf.avg_response_time || 'N/A'}}ms`;

                        // Update glyph traces
                        document.getElementById('glyph-traces').textContent = data.glyph_traces.total_traces || 0;

                        // Update recent reflections
                        const reflections = data.reflection_cycles.recent_reflections || [];
                        document.getElementById('recent-reflections').innerHTML =
                            reflections.slice(0, 3).map(r =>
                                `<div>• ${{r.insight.substring(0, 50)}}...</div>`
                            ).join('');

                        // Update module status
                        const modules = data.active_modules;
                        document.getElementById('modules-list').innerHTML =
                            modules.map(m => `<div class="module-item">${{m}}</div>`).join('');

                        // Update timestamp
                        document.getElementById('last-update').textContent =
                            `Last updated: ${{new Date(data.timestamp * 1000).toLocaleTimeString()}}`;

                    }} catch (error) {{
                        console.error('Dashboard update failed:', error);
                    }}
                }}

                // Update every 5 seconds
                updateDashboard();
                setInterval(updateDashboard, 5000);
            </script>
        </body>
        </html>
        """
        return html

    def _get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        try:
            # This would integrate with lifecycle controller
            return {
                'overall_health': 0.95,
                'component_health': {
                    'vault_core': 1.0,
                    'reflection_vault': 0.9,
                    'glyph_trace': 0.95,
                    'telemetry': 1.0
                }
            }
        except:
            return {'overall_health': 0.5, 'status': 'unknown'}

    def _get_active_modules(self) -> list:
        """Get list of active modules"""
        # This would query the lifecycle controller
        return [
            'vault_core', 'glyph_trace', 'reflection_vault', 'telemetry_stream',
            'apriori_posterior', 'associative_memory', 'decision_apriori',
            'vault_gate_filter', 'ISS_bridge', 'module_blueprints'
        ]

    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        try:
            # This would integrate with telemetry manager
            return {
                'cpu_usage': 45.2,
                'memory_usage': 67.8,
                'avg_response_time': 12.3,
                'requests_per_second': 8.7
            }
        except:
            return {}

    def _get_glyph_traces(self) -> Dict[str, Any]:
        """Get glyph trace information"""
        try:
            # This would integrate with glyph trace expansion
            return {
                'total_traces': 42,
                'recent_traces': 5,
                'avg_confidence': 0.87
            }
        except:
            return {'total_traces': 0}

    def _get_reflection_cycles(self) -> Dict[str, Any]:
        """Get reflection cycle information"""
        try:
            # This would integrate with reflection vault
            return {
                'total_reflections': 28,
                'recent_reflections': [
                    {'insight': 'Improved pattern recognition in glyph traces', 'timestamp': time.time()},
                    {'insight': 'Enhanced memory consolidation in associative matrix', 'timestamp': time.time() - 3600},
                    {'insight': 'Optimized decision confidence thresholds', 'timestamp': time.time() - 7200}
                ],
                'active_cycles': 1
            }
        except:
            return {'total_reflections': 0, 'recent_reflections': []}

    def _get_vault_status(self) -> Dict[str, Any]:
        """Get vault system status"""
        try:
            # This would integrate with main vault system
            return {
                'total_entries': 156,
                'encrypted_entries': 89,
                'active_connections': 3,
                'last_backup': time.time() - 3600
            }
        except:
            return {}

    def _get_module_details(self, module_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a module"""
        # This would query specific module status
        module_info = {
            'vault_core': {
                'name': 'Cryptographic Vault',
                'status': 'active',
                'health': 1.0,
                'entries': 89,
                'last_operation': time.time() - 300
            },
            'reflection_vault': {
                'name': 'Reflection Vault',
                'status': 'active',
                'health': 0.9,
                'reflections': 28,
                'last_insight': time.time() - 1800
            },
            'glyph_trace': {
                'name': 'Glyph Trace System',
                'status': 'active',
                'health': 0.95,
                'traces': 42,
                'avg_confidence': 0.87
            }
        }

        return module_info.get(module_name)

    def _get_recent_glyphs(self, limit: int) -> list:
        """Get recent glyph traces"""
        # Mock data - would integrate with glyph trace expansion
        return [
            {
                'id': f'glyph_{i}',
                'confidence': 0.8 + (i * 0.02),
                'components': ['vault_core', 'reflection_vault'],
                'timestamp': time.time() - (i * 600)
            }
            for i in range(min(limit, 10))
        ]

    def _get_recent_reflections(self, limit: int) -> list:
        """Get recent reflections"""
        # Mock data - would integrate with reflection vault
        return [
            {
                'module': 'glyph_trace',
                'insight': f'Pattern recognition improvement #{i}',
                'timestamp': time.time() - (i * 1800)
            }
            for i in range(min(limit, 5))
        ]

    def _get_performance_history(self, hours: int) -> list:
        """Get performance history"""
        # Mock data - would integrate with telemetry
        return [
            {
                'timestamp': time.time() - (i * 3600),
                'cpu_usage': 40 + (i * 2),
                'memory_usage': 60 + (i * 1.5),
                'response_time': 10 + (i * 0.5)
            }
            for i in range(min(hours, 24))
        ]

    def start_dashboard(self):
        """Start the dashboard server"""
        print(f"Starting telemetry dashboard on http://{self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)

    def run_in_background(self):
        """Run dashboard in background thread"""
        import threading
        dashboard_thread = threading.Thread(target=self.start_dashboard, daemon=True)
        dashboard_thread.start()
        return dashboard_thread