# ==========================================
# GOAT - Great Orchestrator of Autonomous Teams
# Bubble Code v1.0 - Modular Worker Architecture
# ==========================================

from typing import Dict, List, Any, Optional, Type, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uuid
import json
from enum import Enum

# ==========================================
# CORE INTERFACES & DATA STRUCTURES
# ==========================================

class WorkerState(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    LEARNING = "learning"
    SPECIALIZING = "specializing"
    MAINTENANCE = "maintenance"

@dataclass
class WorkerManifest:
    """Blueprint for worker capabilities and specialization"""
    worker_id: str
    department: str
    feature: str
    specialization_score: float = 0.0
    skills_snapshot: Dict[str, Any] = field(default_factory=dict)
    knowledge_seed: Dict[str, Any] = field(default_factory=dict)
    logic_template: str = "basic_seed_v1"
    deployment_history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "worker_id": self.worker_id,
            "department": self.department,
            "feature": self.feature,
            "specialization_score": self.specialization_score,
            "skills_snapshot": self.skills_snapshot,
            "knowledge_seed": self.knowledge_seed,
            "logic_template": self.logic_template,
            "deployment_history": self.deployment_history
        }

class WorkerPlaceholder(ABC):
    """Abstract base for all worker slots - DALS forge will provide concrete implementations"""

    def __init__(self, manifest: WorkerManifest):
        self.manifest = manifest
        self.state = WorkerState.IDLE
        self.learning_memory: List[Dict[str, Any]] = []

    @abstractmethod
    async def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task with job-specific logic - implemented by DALS forge"""
        pass

    @abstractmethod
    async def learn_from_experience(self, result: Dict[str, Any], feedback: Dict[str, Any]):
        """Update specialization based on performance - implemented by DALS forge"""
        pass

    def get_specialization_path(self) -> str:
        return f"{self.manifest.department}.{self.manifest.feature}.{self.manifest.worker_id}"

    def export_manifest(self) -> Dict[str, Any]:
        return self.manifest.to_dict()

# ==========================================
# DEPARTMENT & FEATURE ARCHITECTURE
# ==========================================

@dataclass
class FeatureSlot:
    """Container for a specific feature with multiple learner workers"""

    feature_name: str
    max_workers: int = 3
    workers: Dict[str, WorkerPlaceholder] = field(default_factory=dict)
    task_queue: List[Dict[str, Any]] = field(default_factory=list)

    def add_worker(self, worker: WorkerPlaceholder) -> bool:
        """Add a worker to this feature slot if capacity allows"""
        if len(self.workers) >= self.max_workers:
            return False

        worker_id = worker.manifest.worker_id
        self.workers[worker_id] = worker
        return True

    def get_optimal_worker(self) -> Optional[WorkerPlaceholder]:
        """Select the most specialized worker for a task"""
        if not self.workers:
            return None

        return max(
            self.workers.values(),
            key=lambda w: w.manifest.specialization_score
        )

    def get_learning_workers(self) -> List[WorkerPlaceholder]:
        """Get workers currently in learning state"""
        return [w for w in self.workers.values() if w.state == WorkerState.LEARNING]

class Department:
    """Functional department containing multiple specialized features"""

    def __init__(self, name: str, description: str = ""):
        self.department_id = f"dept_{name.lower()}"
        self.name = name
        self.description = description
        self.features: Dict[str, FeatureSlot] = {}
        self.department_memory: Dict[str, Any] = {}

    def add_feature(self, feature_name: str, max_workers: int = 3) -> FeatureSlot:
        """Create a new feature slot within this department"""
        feature = FeatureSlot(
            feature_name=feature_name,
            max_workers=max_workers
        )
        self.features[feature_name] = feature
        return feature

    def deploy_worker_to_feature(self, worker: WorkerPlaceholder, feature_name: str) -> bool:
        """Deploy a worker from DALS forge to a specific feature"""
        if feature_name not in self.features:
            raise ValueError(f"Feature '{feature_name}' not found in department '{self.name}'")

        return self.features[feature_name].add_worker(worker)

    async def route_task(self, feature_name: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Route task to the most appropriate worker in a feature"""
        if feature_name not in self.features:
            return {"error": f"Feature '{feature_name}' not available"}

        feature = self.features[feature_name]
        worker = feature.get_optimal_worker()

        if not worker:
            return {"error": f"No workers available for {feature_name}"}

        worker.state = WorkerState.ACTIVE
        try:
            result = await worker.execute(task, self.department_memory)
            worker.state = WorkerState.IDLE
            return result
        except Exception as e:
            worker.state = WorkerState.IDLE
            return {"error": str(e)}

# ==========================================
# GOAT ORCHESTRATOR - MAIN BUBBLE
# ==========================================

class GOATOrchestrator:
    """Central orchestrator that manages all departments and worker deployment"""

    def __init__(self):
        self.orchestrator_id = f"goat_{uuid.uuid4().hex[:8]}"
        self.departments: Dict[str, Department] = {}
        self.worker_registry: Dict[str, WorkerPlaceholder] = {}
        self.dals_forge_connector: Optional[Callable] = None

        # Default department structure - EXTENSIBLE
        self._initialize_default_departments()

    def _initialize_default_departments(self):
        """Setup placeholder departments and features"""

        # ONBOARDING DEPARTMENT
        onboarding_dept = self.create_department("Onboarding", "User onboarding and setup")
        onboarding_dept.add_feature("setup", max_workers=2)
        onboarding_dept.add_feature("guide", max_workers=2)

        # PRICING DEPARTMENT
        pricing_dept = self.create_department("Pricing", "Pricing and subscription management")
        pricing_dept.add_feature("info", max_workers=2)
        pricing_dept.add_feature("advisor", max_workers=2)

        # CREATOR DEPARTMENT
        creator_dept = self.create_department("Creator", "Content creation and building")
        creator_dept.add_feature("tools", max_workers=3)
        creator_dept.add_feature("content", max_workers=3)

        # TECH DEPARTMENT
        tech_dept = self.create_department("Tech", "Technical support and integration")
        tech_dept.add_feature("integration", max_workers=3)
        tech_dept.add_feature("api", max_workers=2)

        # LEGAL DEPARTMENT
        legal_dept = self.create_department("Legal", "Legal and policy information")
        legal_dept.add_feature("policy", max_workers=2)
        legal_dept.add_feature("terms", max_workers=2)

        # CODE DEPARTMENT
        code_dept = self.create_department("Code", "Software development and engineering")
        code_dept.add_feature("python_backend", max_workers=3)
        code_dept.add_feature("frontend_ui", max_workers=2)
        code_dept.add_feature("database_design", max_workers=2)
        code_dept.add_feature("api_integration", max_workers=3)

        # RESEARCH DEPARTMENT
        research_dept = self.create_department("Research", "Information gathering and analysis")
        research_dept.add_feature("web_scraping", max_workers=4)
        research_dept.add_feature("data_analysis", max_workers=3)
        research_dept.add_feature("literature_review", max_workers=2)

        # DESIGN DEPARTMENT
        design_dept = self.create_department("Design", "Visual and UX design")
        design_dept.add_feature("ui_prototyping", max_workers=2)
        design_dept.add_feature("graphic_creation", max_workers=2)

        # QA/DEPLOYMENT DEPARTMENT
        qa_dept = self.create_department("Quality", "Testing and deployment")
        qa_dept.add_feature("unit_testing", max_workers=3)
        qa_dept.add_feature("integration_testing", max_workers=2)
        qa_dept.add_feature("deployment", max_workers=2)

    def register_dals_forge(self, forge_connector: Callable[[str, str, str], WorkerPlaceholder]):
        """Register the DALS worker forge connector function"""
        self.dals_forge_connector = forge_connector

    def create_department(self, name: str, description: str = "") -> Department:
        """Create a new department"""
        dept = Department(name, description)
        self.departments[dept.department_id] = dept
        return dept

    async def forge_and_deploy_worker(
        self,
        department: str,
        feature: str,
        logic_seed: str = "basic_seed_v1",
        custom_skills: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Request worker from DALS forge and deploy it
        This is the main integration point
        """
        if not self.dals_forge_connector:
            raise RuntimeError("DALS forge not registered. Call register_dals_forge first.")

        # Generate unique worker ID
        worker_id = f"worker_{department.lower()}_{feature.lower()}_{uuid.uuid4().hex[:6]}"

        # Request worker from DALS forge
        worker = self.dals_forge_connector(
            worker_id=worker_id,
            department=department,
            feature=feature,
            logic_seed=logic_seed,
            custom_skills=custom_skills or {}
        )

        # Create manifest
        manifest = WorkerManifest(
            worker_id=worker_id,
            department=department,
            feature=feature,
            logic_template=logic_seed,
            skills_snapshot=custom_skills or {},
            knowledge_seed={"initialized": True, "template": logic_seed}
        )
        worker.manifest = manifest

        # Deploy to department/feature
        dept_key = f"dept_{department.lower()}"
        if dept_key not in self.departments:
            raise ValueError(f"Department '{department}' not found")

        success = self.departments[dept_key].deploy_worker_to_feature(worker, feature)
        if not success:
            raise RuntimeError(f"Failed to deploy worker to {department}.{feature} - capacity full")

        # Register in global registry
        self.worker_registry[worker_id] = worker

        return worker_id

    def get_department_overview(self) -> Dict[str, Any]:
        """Get complete system status"""
        overview = {
            "orchestrator_id": self.orchestrator_id,
            "departments": {}
        }

        for dept_id, dept in self.departments.items():
            dept_info = {
                "name": dept.name,
                "features": {}
            }

            for feature_name, feature in dept.features.items():
                feature_info = {
                    "max_capacity": feature.max_workers,
                    "current_workers": len(feature.workers),
                    "workers": [
                        {
                            "id": w.manifest.worker_id,
                            "specialization_score": w.manifest.specialization_score,
                            "state": w.state.value
                        }
                        for w in feature.workers.values()
                    ]
                }
                dept_info["features"][feature_name] = feature_info

            overview["departments"][dept_id] = dept_info

        return overview

    def export_worker_manifests(self, department: Optional[str] = None, feature: Optional[str] = None) -> List[Dict[str, Any]]:
        """Export manifests for all or specific workers"""
        manifests = []

        for worker in self.worker_registry.values():
            if department and worker.manifest.department != department:
                continue
            if feature and worker.manifest.feature != feature:
                continue
            manifests.append(worker.export_manifest())

        return manifests