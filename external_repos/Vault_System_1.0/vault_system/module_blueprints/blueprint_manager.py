from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
import hashlib
import time
from enum import Enum
from collections import defaultdict

class BlueprintStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    EXPERIMENTAL = "experimental"
    MAINTENANCE = "maintenance"

@dataclass
class ModuleBlueprint:
    module_id: str
    module_name: str
    version: str
    dependencies: List[str]
    interfaces: Dict[str, Any]
    configuration: Dict[str, Any]
    status: BlueprintStatus
    created: float
    last_modified: float
    checksum: str

class BlueprintManager:
    def __init__(self):
        self.blueprints = {}
        self.dependency_graph = {}
        self.module_versions = defaultdict(list)
        
    def register_blueprint(self, module_name: str, version: str,
                          dependencies: List[str], interfaces: Dict[str, Any],
                          configuration: Dict[str, Any], 
                          status: BlueprintStatus = BlueprintStatus.ACTIVE) -> str:
        """Register a module blueprint"""
        module_id = f"{module_name}_{version}"
        
        blueprint = ModuleBlueprint(
            module_id=module_id,
            module_name=module_name,
            version=version,
            dependencies=dependencies,
            interfaces=interfaces,
            configuration=configuration,
            status=status,
            created=time.time(),
            last_modified=time.time(),
            checksum=self._calculate_checksum(interfaces, configuration)
        )
        
        self.blueprints[module_id] = blueprint
        self.dependency_graph[module_id] = dependencies
        self.module_versions[module_name].append(version)
        
        print(f"Registered blueprint: {module_id}")
        return module_id
    
    def get_blueprint(self, module_id: str) -> Optional[ModuleBlueprint]:
        """Get module blueprint by ID"""
        return self.blueprints.get(module_id)
    
    def update_blueprint(self, module_id: str, updates: Dict[str, Any]) -> bool:
        """Update existing blueprint"""
        if module_id not in self.blueprints:
            return False
            
        blueprint = self.blueprints[module_id]
        
        # Update allowed fields
        if 'interfaces' in updates:
            blueprint.interfaces = updates['interfaces']
        if 'configuration' in updates:
            blueprint.configuration = updates['configuration']
        if 'status' in updates:
            blueprint.status = updates['status']
        if 'dependencies' in updates:
            blueprint.dependencies = updates['dependencies']
            self.dependency_graph[module_id] = updates['dependencies']
        
        blueprint.last_modified = time.time()
        blueprint.checksum = self._calculate_checksum(
            blueprint.interfaces, blueprint.configuration
        )
        
        return True
    
    def verify_module_integrity(self, module_id: str, current_config: Dict[str, Any]) -> bool:
        """Verify module matches its blueprint"""
        blueprint = self.get_blueprint(module_id)
        if not blueprint:
            return False
            
        current_checksum = self._calculate_checksum(
            current_config.get('interfaces', {}),
            current_config.get('configuration', {})
        )
        
        return current_checksum == blueprint.checksum
    
    def get_dependency_tree(self, module_id: str) -> Dict[str, Any]:
        """Get complete dependency tree for module"""
        if module_id not in self.dependency_graph:
            return {}
            
        tree = {
            'module': module_id,
            'dependencies': []
        }
        
        for dep in self.dependency_graph[module_id]:
            dep_tree = self.get_dependency_tree(dep)
            tree['dependencies'].append(dep_tree)
            
        return tree
    
    def check_circular_dependencies(self) -> List[List[str]]:
        """Check for circular dependencies"""
        visited = set()
        recursion_stack = set()
        circular_paths = []
        
        def _dfs(module_id: str, path: List[str]):
            if module_id in recursion_stack:
                # Found circular dependency
                circular_start = path.index(module_id)
                circular_paths.append(path[circular_start:] + [module_id])
                return
                
            if module_id in visited:
                return
                
            visited.add(module_id)
            recursion_stack.add(module_id)
            path.append(module_id)
            
            for dependency in self.dependency_graph.get(module_id, []):
                _dfs(dependency, path)
                
            path.pop()
            recursion_stack.remove(module_id)
        
        for module_id in self.dependency_graph:
            if module_id not in visited:
                _dfs(module_id, [])
                
        return circular_paths
    
    def get_module_recommendations(self, requirements: Dict[str, Any]) -> List[str]:
        """Get module recommendations based on requirements"""
        recommendations = []
        
        for module_id, blueprint in self.blueprints.items():
            score = self._calculate_compatibility_score(blueprint, requirements)
            if score > 0.7:  # 70% compatibility threshold
                recommendations.append({
                    'module_id': module_id,
                    'score': score,
                    'status': blueprint.status,
                    'dependencies': blueprint.dependencies
                })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)
    
    def _calculate_compatibility_score(self, blueprint: ModuleBlueprint, 
                                     requirements: Dict[str, Any]) -> float:
        """Calculate compatibility score between blueprint and requirements"""
        score = 0.0
        total_weights = 0
        
        # Check interface compatibility
        if 'required_interfaces' in requirements:
            weight = 0.6
            total_weights += weight
            
            required_interfaces = set(requirements['required_interfaces'])
            provided_interfaces = set(blueprint.interfaces.keys())
            interface_match = len(required_interfaces.intersection(provided_interfaces))
            interface_score = interface_match / len(required_interfaces) if required_interfaces else 1.0
            
            score += interface_score * weight
        
        # Check configuration compatibility
        if 'configuration_constraints' in requirements:
            weight = 0.3
            total_weights += weight
            
            constraints = requirements['configuration_constraints']
            config_score = self._check_configuration_constraints(blueprint.configuration, constraints)
            score += config_score * weight
        
        # Consider module status
        weight = 0.1
        total_weights += weight
        status_score = 1.0 if blueprint.status == BlueprintStatus.ACTIVE else 0.5
        score += status_score * weight
        
        return score / total_weights if total_weights > 0 else 0.0
    
    def _check_configuration_constraints(self, configuration: Dict[str, Any],
                                       constraints: Dict[str, Any]) -> float:
        """Check configuration against constraints"""
        matches = 0
        total_constraints = len(constraints)
        
        if total_constraints == 0:
            return 1.0
            
        for key, constraint in constraints.items():
            if key in configuration:
                config_value = configuration[key]
                # Simple type checking
                if 'type' in constraint and isinstance(config_value, eval(constraint['type'])):
                    matches += 1
                elif 'values' in constraint and config_value in constraint['values']:
                    matches += 1
                else:
                    # Check range constraints
                    if 'min' in constraint and 'max' in constraint:
                        if constraint['min'] <= config_value <= constraint['max']:
                            matches += 1
        
        return matches / total_constraints
    
    def _calculate_checksum(self, interfaces: Dict[str, Any], configuration: Dict[str, Any]) -> str:
        """Calculate checksum for blueprint data"""
        data_str = json.dumps({
            'interfaces': interfaces,
            'configuration': configuration
        }, sort_keys=True)
        
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def export_blueprint(self, module_id: str) -> Optional[Dict[str, Any]]:
        """Export blueprint as dictionary"""
        blueprint = self.get_blueprint(module_id)
        if not blueprint:
            return None
            
        return asdict(blueprint)
    
    def import_blueprint(self, blueprint_data: Dict[str, Any]) -> str:
        """Import blueprint from dictionary"""
        return self.register_blueprint(
            module_name=blueprint_data['module_name'],
            version=blueprint_data['version'],
            dependencies=blueprint_data['dependencies'],
            interfaces=blueprint_data['interfaces'],
            configuration=blueprint_data['configuration'],
            status=BlueprintStatus(blueprint_data['status'])
        )
    
    def get_system_blueprint(self) -> Dict[str, Any]:
        """Get complete system blueprint"""
        return {
            'total_modules': len(self.blueprints),
            'modules': {
                module_id: {
                    'name': blueprint.module_name,
                    'version': blueprint.version,
                    'status': blueprint.status.value,
                    'dependencies': blueprint.dependencies
                }
                for module_id, blueprint in self.blueprints.items()
            },
            'dependency_graph': self.dependency_graph,
            'circular_dependencies': self.check_circular_dependencies()
        }