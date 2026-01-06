# reasoning_glyph_mapper.py

from typing import Dict, List, Any, Optional, Set
import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum

class ReasoningStep(Enum):
    SEED_ACTIVATION = "seed_activation"
    PRIOR_APPLICATION = "prior_application"
    PATTERN_MATCHING = "pattern_matching"
    EVIDENCE_EVALUATION = "evidence_evaluation"
    DECISION_SYNTHESIS = "decision_synthesis"
    REFLECTION_INTEGRATION = "reflection_integration"

@dataclass
class ReasoningNode:
    """A node in the reasoning path"""
    node_id: str
    step_type: ReasoningStep
    component: str  # Which vault subsystem contributed
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    confidence: float = 1.0
    predecessors: List[str] = field(default_factory=list)
    successors: List[str] = field(default_factory=list)

@dataclass
class ReasoningPath:
    """Complete reasoning path for auditability"""
    path_id: str
    root_question: str
    nodes: Dict[str, ReasoningNode] = field(default_factory=dict)
    final_verdict: Dict[str, Any] = field(default_factory=dict)
    total_confidence: float = 0.0
    execution_time: float = 0.0
    created_at: float = field(default_factory=time.time)

class ReasoningGlyphMapper:
    """
    Maps complete reasoning paths through glyph traces.
    Makes every verdict auditable and replayable.
    """

    def __init__(self, glyph_generator):
        self.glyph_generator = glyph_generator
        self.reasoning_paths: Dict[str, ReasoningPath] = {}
        self.active_paths: Dict[str, ReasoningPath] = {}

    def start_reasoning_path(self, question: str, context: Dict[str, Any] = None) -> str:
        """Start tracking a new reasoning path"""
        path_id = self._generate_path_id(question, context or {})

        path = ReasoningPath(
            path_id=path_id,
            root_question=question
        )

        self.active_paths[path_id] = path
        return path_id

    def add_reasoning_step(self,
                          path_id: str,
                          step_type: ReasoningStep,
                          component: str,
                          data: Dict[str, Any],
                          confidence: float = 1.0,
                          predecessors: List[str] = None) -> Optional[str]:
        """Add a step to the reasoning path"""

        if path_id not in self.active_paths:
            return None

        path = self.active_paths[path_id]

        # Generate node ID
        node_id = self._generate_node_id(path_id, step_type, component, data)

        # Create node
        node = ReasoningNode(
            node_id=node_id,
            step_type=step_type,
            component=component,
            data=data,
            confidence=confidence,
            predecessors=predecessors or []
        )

        # Add to path
        path.nodes[node_id] = node

        # Update predecessor successors
        for pred_id in predecessors or []:
            if pred_id in path.nodes:
                path.nodes[pred_id].successors.append(node_id)

        return node_id

    def complete_reasoning_path(self,
                               path_id: str,
                               verdict: Dict[str, Any],
                               execution_time: float) -> bool:
        """Complete a reasoning path with final verdict"""

        if path_id not in self.active_paths:
            return False

        path = self.active_paths[path_id]
        path.final_verdict = verdict
        path.execution_time = execution_time
        path.total_confidence = self._calculate_path_confidence(path)

        # Generate glyph trace for the complete path
        glyph = self._generate_path_glyph(path)

        # Store completed path
        self.reasoning_paths[path_id] = path
        del self.active_paths[path_id]

        return True

    def _generate_path_id(self, question: str, context: Dict[str, Any]) -> str:
        """Generate unique path ID"""
        content = f"{question}:{json.dumps(context, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _generate_node_id(self, path_id: str, step_type: ReasoningStep,
                         component: str, data: Dict[str, Any]) -> str:
        """Generate unique node ID"""
        content = f"{path_id}:{step_type.value}:{component}:{json.dumps(data, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def _calculate_path_confidence(self, path: ReasoningPath) -> float:
        """Calculate overall confidence for the reasoning path"""
        if not path.nodes:
            return 0.0

        # Weighted average based on step importance
        step_weights = {
            ReasoningStep.SEED_ACTIVATION: 0.3,
            ReasoningStep.PRIOR_APPLICATION: 0.25,
            ReasoningStep.PATTERN_MATCHING: 0.2,
            ReasoningStep.EVIDENCE_EVALUATION: 0.15,
            ReasoningStep.DECISION_SYNTHESIS: 0.08,
            ReasoningStep.REFLECTION_INTEGRATION: 0.02
        }

        total_weight = 0.0
        weighted_sum = 0.0

        for node in path.nodes.values():
            weight = step_weights.get(node.step_type, 0.1)
            weighted_sum += node.confidence * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _generate_path_glyph(self, path: ReasoningPath) -> Dict[str, Any]:
        """Generate glyph trace for the complete reasoning path"""
        # Create comprehensive data for glyph generation
        glyph_data = {
            'path_id': path.path_id,
            'question': path.root_question,
            'node_count': len(path.nodes),
            'components_used': list(set(node.component for node in path.nodes.values())),
            'step_sequence': [node.step_type.value for node in self._get_topological_order(path)],
            'confidence_scores': {node_id: node.confidence for node_id, node in path.nodes.items()},
            'verdict': path.final_verdict,
            'execution_time': path.execution_time,
            'total_confidence': path.total_confidence
        }

        # Generate glyph using the glyph generator
        return self.glyph_generator.generate_data_glyph(
            data=glyph_data,
            vault_id=f"reasoning_path_{path.path_id}",
            metadata={
                'glyph_type': 'reasoning_trace',
                'created_at': path.created_at,
                'is_complete': True
            }
        )

    def _get_topological_order(self, path: ReasoningPath) -> List[ReasoningNode]:
        """Get nodes in topological order (dependencies first)"""
        # Simple topological sort
        visited = set()
        order = []

        def visit(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)

            node = path.nodes[node_id]
            for pred_id in node.predecessors:
                visit(pred_id)

            order.append(node)

        # Start from nodes with no predecessors
        start_nodes = [node_id for node_id, node in path.nodes.items() if not node.predecessors]

        for node_id in start_nodes:
            visit(node_id)

        return order

    def get_reasoning_path(self, path_id: str) -> Optional[ReasoningPath]:
        """Retrieve a completed reasoning path"""
        return self.reasoning_paths.get(path_id)

    def replay_reasoning_path(self, path_id: str) -> Optional[Dict[str, Any]]:
        """Replay a reasoning path for analysis"""
        path = self.get_reasoning_path(path_id)
        if not path:
            return None

        # Reconstruct the reasoning sequence
        ordered_nodes = self._get_topological_order(path)

        replay_data = {
            'path_id': path.path_id,
            'question': path.root_question,
            'step_by_step': [
                {
                    'step': i + 1,
                    'node_id': node.node_id,
                    'type': node.step_type.value,
                    'component': node.component,
                    'data': node.data,
                    'confidence': node.confidence,
                    'timestamp': node.timestamp
                }
                for i, node in enumerate(ordered_nodes)
            ],
            'final_verdict': path.final_verdict,
            'total_confidence': path.total_confidence,
            'execution_time': path.execution_time
        }

        return replay_data

    def audit_reasoning_paths(self,
                            component_filter: str = None,
                            min_confidence: float = 0.0,
                            time_range: tuple = None) -> List[Dict[str, Any]]:
        """Audit reasoning paths with filters"""

        results = []

        for path in self.reasoning_paths.values():
            # Apply filters
            if component_filter:
                components_used = set(node.component for node in path.nodes.values())
                if component_filter not in components_used:
                    continue

            if path.total_confidence < min_confidence:
                continue

            if time_range:
                start_time, end_time = time_range
                if not (start_time <= path.created_at <= end_time):
                    continue

            # Add to results
            results.append({
                'path_id': path.path_id,
                'question': path.root_question,
                'components_used': list(set(node.component for node in path.nodes.values())),
                'node_count': len(path.nodes),
                'total_confidence': path.total_confidence,
                'execution_time': path.execution_time,
                'created_at': path.created_at,
                'verdict_summary': str(path.final_verdict)[:100] + "..." if len(str(path.final_verdict)) > 100 else str(path.final_verdict)
            })

        return results

    def get_reasoning_statistics(self) -> Dict[str, Any]:
        """Get statistics about reasoning patterns"""
        if not self.reasoning_paths:
            return {}

        total_paths = len(self.reasoning_paths)
        avg_confidence = sum(p.total_confidence for p in self.reasoning_paths.values()) / total_paths
        avg_execution_time = sum(p.execution_time for p in self.reasoning_paths.values()) / total_paths

        # Component usage frequency
        component_usage = {}
        for path in self.reasoning_paths.values():
            for node in path.nodes.values():
                component_usage[node.component] = component_usage.get(node.component, 0) + 1

        # Step type frequency
        step_usage = {}
        for path in self.reasoning_paths.values():
            for node in path.nodes.values():
                step_type = node.step_type.value
                step_usage[step_type] = step_usage.get(step_type, 0) + 1

        return {
            'total_paths': total_paths,
            'average_confidence': avg_confidence,
            'average_execution_time': avg_execution_time,
            'component_usage': component_usage,
            'step_usage': step_usage,
            'most_used_component': max(component_usage.items(), key=lambda x: x[1]) if component_usage else None,
            'most_used_step': max(step_usage.items(), key=lambda x: x[1]) if step_usage else None
        }