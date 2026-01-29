# goat/core/goat_field_skg.py
"""
GOAT Space-Field SKG: Autobiographical Memory System
4-dimensional knowledge field (3D space + time) for conservative self-improvement.
"""

import asyncio
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    nx = None
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Set, Tuple

logger = logging.getLogger(__name__)

class IntegrityError(Exception):
    """Raised when graph integrity checks fail."""
    pass

@dataclass
class FieldObservation:
    """
    Immutable record of a GOAT operation.
    Append-only. Never mutated. Never deleted.
    """
    timestamp: str
    operation_type: str  # 'distillation', 'worker_session', 'certificate', 'error'
    inputs_hash: str     # SHA256 of input parameters (privacy-preserving)
    outcome: str         # 'success', 'failure', 'degraded'
    metrics: Dict        # Performance data
    context: Dict        # System state at time of operation
    sequence_id: int     # Monotonic counter for temporal ordering

    def verify_integrity(self) -> bool:
        """Self-checking hash chain."""
        content = f"{self.sequence_id}:{self.timestamp}:{self.operation_type}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

class GOATSpaceField:
    """
    Primary SKG for GOAT self-improvement.
    Bounded, conservative, append-only.

    Principles:
    1. OBSERVE, don't mutate
    2. SUGGEST, don't change
    3. WAIT for idle, don't interrupt
    4. HUMAN approves, never auto-deploy
    """

    def __init__(self, field_path: str = "./goat_field/"):
        self.field_path = Path(field_path)
        self.field_path.mkdir(exist_ok=True)

        # The Knowledge Graph (pattern web) - optional
        if HAS_NETWORKX:
            self.graph = nx.DiGraph()
        else:
            self.graph = None
            logger.warning("NetworkX not available - graph functionality disabled")

        # Immutable journal (sequence of observations)
        self.journal_path = self.field_path / "immutable_journal.jsonl"
        self.sequence_counter = self._load_sequence()

        # Reflection state
        self.reflection_active = False
        self.last_reflection = datetime.utcnow()

        # Improvement proposals (pending approval)
        self.proposal_queue = self.field_path / "improvement_queue.json"

        # Clutter control parameters (from ORB, tuned for GOAT)
        self.edge_decay_half_life = 30  # days (edges weaken over time)
        self.clutter_threshold = 0.1    # edge weight below this = clutter
        self.min_node_degree = 2        # isolated nodes = clutter

        # Self-repair metrics
        self.repair_log = self.field_path / "repair_operations.jsonl"
        self.clutter_stats = {
            'edges_pruned': 0,
            'nodes_archived': 0,
            'graphs_restructured': 0
        }

        # Loaded patterns (conservative cache)
        self.learned_patterns = {}
        self._load_patterns()

    async def observe(self, observation: FieldObservation):
        """
        Record an operation to the field.
        Always append. Never overwrite.
        """
        # Atomic append to journal
        with open(self.journal_path, 'a') as f:
            f.write(json.dumps({
                'seq': observation.sequence_id,
                'ts': observation.timestamp,
                'type': observation.operation_type,
                'inputs_hash': observation.inputs_hash,
                'outcome': observation.outcome,
                'metrics': observation.metrics,
                'context': observation.context
            }) + '\n')

        # Add to graph (weak references, not data duplication)
        if self.graph is not None:
            self.graph.add_node(
                observation.sequence_id,
                type=observation.operation_type,
                outcome=observation.outcome,
                timestamp=observation.timestamp
            )

            # Link to recent similar operations (temporal locality)
            recent = self._get_recent_observations(10)
            for prev_id in recent:
                if self._similarity_score(prev_id, observation.sequence_id) > 0.7:
                    self.graph.add_edge(
                        prev_id,
                        observation.sequence_id,
                        weight=self._similarity_score(prev_id, observation.sequence_id),
                        relation='similar_context',
                        created_at=datetime.utcnow().isoformat(),
                        original_weight=self._similarity_score(prev_id, observation.sequence_id)
                    )

    async def reflect(self, idle_threshold_seconds: int = 300):
        """
        Idle-time learning WITH clutter cleaning.
        """
        if self.reflection_active:
            return

        if (datetime.utcnow() - self.last_reflection).seconds < idle_threshold_seconds:
            return

        self.reflection_active = True

        try:
            # Phase 1: Pattern extraction (learning)
            new_patterns = await self._extract_patterns()

            # Phase 2: Clutter detection and self-repair (ORB-style cleaning)
            await self._compaction_pass()  # Includes edge decay, clutter removal, consolidation

            # Phase 3: Queue improvements (conservative)
            for pattern_id, pattern in new_patterns.items():
                confidence = min(0.4, pattern['confidence'])  # Hard cap
                if confidence > 0.25:
                    await self._queue_improvement(pattern)

            # Phase 4: Health check
            health = self.get_graph_health_report()
            if health.get('status') == 'fragmented':
                # Alert admin but don't auto-fix (safety)
                await self._alert_admin("Graph fragmentation detected", health)

        finally:
            self.reflection_active = False
            self.last_reflection = datetime.utcnow()

    async def _alert_admin(self, message: str, details: Dict):
        """
        Alert administrator about field health issues.
        In production, this would send notifications.
        """
        alert_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'alert_type': 'field_health',
            'message': message,
            'details': details,
            'severity': 'warning'
        }

        # Log to alerts file
        alert_log = self.field_path / 'field_alerts.jsonl'
        with open(alert_log, 'a') as f:
            f.write(json.dumps(alert_entry) + '\n')

        logger.warning(f"GOAT Field Alert: {message}")
        # In production: send email, Slack notification, etc.

    async def _extract_patterns(self) -> Dict:
        """
        Discover recurring patterns in observations.
        No mutation of code. Just pattern recognition.
        """
        patterns = {}

        # Pattern 1: Distiller performance by file type
        type_performance = {}
        if self.graph is not None:
            for node, data in self.graph.nodes(data=True):
                if data.get('type') == 'distillation':
                    # Look up metrics from journal (not stored in graph)
                    record = self._get_journal_entry(node)
                    file_type = record['context'].get('file_type', 'unknown')
                    duration = record['metrics'].get('processing_time_ms', 0)

                    if file_type not in type_performance:
                        type_performance[file_type] = []
                    type_performance[file_type].append(duration)
        else:
            # Fallback: scan journal directly
            if self.journal_path.exists():
                with open(self.journal_path) as f:
                    for line in f:
                        record = json.loads(line)
                        if record['type'] == 'distillation':
                            file_type = record['context'].get('file_type', 'unknown')
                            duration = record['metrics'].get('processing_time_ms', 0)
                            if file_type not in type_performance:
                                type_performance[file_type] = []
                            type_performance[file_type].append(duration)

        # Detect inefficient file types
        for file_type, durations in type_performance.items():
            avg_duration = sum(durations) / len(durations)
            if len(durations) > 5 and avg_duration > 60000:  # >60s average
                patterns[f'slow_{file_type}'] = {
                    'type': 'performance_anomaly',
                    'target': f'visidata_distiller:{file_type}',
                    'observation': f'{file_type} files averaging {avg_duration}ms',
                    'suggestion': 'Consider chunking strategy or pre-filtering',
                    'confidence': min(0.35, len(durations) * 0.05),  # Capped
                    'supporting_evidence': durations[-5:]  # Last 5 instances
                }

        # Pattern 2: Worker success rates by task complexity
        worker_outcomes = {}
        if self.graph is not None:
            for node, data in self.graph.nodes(data=True):
                if data.get('type') == 'worker_session':
                    record = self._get_journal_entry(node)
                    worker = record['context'].get('worker_id')
                    outcome = record['outcome']

                    if worker not in worker_outcomes:
                        worker_outcomes[worker] = {'success': 0, 'failure': 0}
                    worker_outcomes[worker][outcome] += 1
        else:
            # Fallback: scan journal directly
            if self.journal_path.exists():
                with open(self.journal_path) as f:
                    for line in f:
                        record = json.loads(line)
                        if record['type'] == 'worker_session':
                            worker = record['context'].get('worker_id')
                            outcome = record['outcome']
                            if worker not in worker_outcomes:
                                worker_outcomes[worker] = {'success': 0, 'failure': 0}
                            worker_outcomes[worker][outcome] += 1

        for worker, counts in worker_outcomes.items():
            total = counts['success'] + counts['failure']
            if total > 10:
                success_rate = counts['success'] / total
                if success_rate < 0.8:
                    patterns[f'low_success_{worker}'] = {
                        'type': 'reliability_concern',
                        'target': worker,
                        'observation': f'Success rate {success_rate:.2%} over {total} runs',
                        'suggestion': 'Review error logs or adjust complexity thresholds',
                        'confidence': min(0.3, total * 0.01),
                        'sample_size': total
                    }

        # Pattern 3: User behavior leading to certificates
        # (What workflows result in completed certificates?)

        return patterns

    async def _queue_improvement(self, pattern: Dict):
        """
        Queue a proposed improvement for HUMAN/SYSTEM approval.
        NEVER auto-implement. Submit to review system.
        """
        try:
            from goat.core.field_review_system import GOATFieldReviewSystem, ImprovementProposal
            review_system = GOATFieldReviewSystem()

            # Convert pattern to ImprovementProposal
            proposal = ImprovementProposal(
                proposal_id=hashlib.sha256(
                    f"{pattern['type']}:{datetime.utcnow().isoformat()}".encode()
                ).hexdigest()[:12],
                pattern_type=pattern['type'],
                target_component=pattern['target'],
                observation=pattern['observation'],
                suggestion=pattern['suggestion'],
                confidence=min(0.4, pattern['confidence']),  # Hard cap
                evidence=pattern.get('supporting_evidence', []),
                proposed_at=datetime.utcnow().isoformat() + "Z"
            )

            review_system.submit_proposal(proposal)

            # Optionally notify admin (could be a Worker notification)
            logger.info(f"GOAT Field: New improvement proposal #{proposal.proposal_id} submitted for review")

        except Exception as e:
            logger.error(f"Failed to submit proposal to review system: {e}")
            # Fallback: log to old queue for manual review
            fallback_proposal = {
                'proposal_id': hashlib.sha256(
                    f"{pattern['type']}:{datetime.utcnow().isoformat()}".encode()
                ).hexdigest()[:12],
                'pattern_type': pattern['type'],
                'target_component': pattern['target'],
                'observation': pattern['observation'],
                'suggestion': pattern['suggestion'],
                'confidence': pattern['confidence'],
                'evidence': pattern.get('supporting_evidence', []),
                'status': 'pending_review',
                'proposed_at': datetime.utcnow().isoformat()
            }

            queue = []
            if self.proposal_queue.exists():
                queue = json.loads(self.proposal_queue.read_text())

            queue.append(fallback_proposal)
            self.proposal_queue.write_text(json.dumps(queue, indent=2))

    def compile_insights(self) -> Dict:
        """
        Generate 'compiled wisdom' for runtime use.
        Safe, read-only optimizations based on APPROVED human-reviewed patterns only.

        Runtime Consumption Rule: Only read from approved proposals.
        Never reads rationale (human-only). Never auto-implements.
        """
        insights = {
            'distiller_optimizations': {},
            'worker_configs': {},
            'resource_hints': {},
            'compiled_at': datetime.utcnow().isoformat()
        }

        # Runtime consumption: Only approved proposals from review system
        try:
            from goat.core.field_review_system import GOATFieldReviewSystem
            review_system = GOATFieldReviewSystem()
            approved_insights = review_system.get_approved_insights()

            for insight in approved_insights:
                target = insight['target_component']
                config = insight['approved_config']
                confidence = insight['confidence']

                # Apply approved optimizations
                if ':' in target and target.startswith('visidata_distiller'):
                    file_type = target.split(':')[-1]
                    insights['distiller_optimizations'][file_type] = {
                        'chunk_size': config.get('chunk_size', 1000),
                        'pre_filter': config.get('pre_filter'),
                        'confidence': confidence,
                        'approved_at': insight.get('approved_at')
                    }
                elif target.startswith('worker:'):
                    worker_id = target.split(':')[-1]
                    insights['worker_configs'][worker_id] = {
                        'max_complexity': config.get('max_complexity', 0.8),
                        'fallback_enabled': config.get('fallback_enabled', True),
                        'confidence': confidence,
                        'approved_at': insight.get('approved_at')
                    }

        except Exception as e:
            # Fallback: use legacy proposal queue if review system unavailable
            logger.warning(f"Review system unavailable, using legacy queue: {e}")
            if self.proposal_queue.exists():
                queue = json.loads(self.proposal_queue.read_text())
                approved = [p for p in queue if p['status'] == 'approved']

                for proposal in approved:
                    if proposal['pattern_type'] == 'performance_anomaly':
                        target = proposal['target_component']
                        file_type = target.split(':')[-1]
                        insights['distiller_optimizations'][file_type] = {
                            'recommended_chunk_size': proposal.get('approved_config', {}).get('chunk_size', 1000),
                            'pre_filter_suggestion': proposal.get('approved_config', {}).get('pre_filter', None)
                        }

                    elif proposal['pattern_type'] == 'reliability_concern':
                        worker = proposal['target_component']
                        insights['worker_configs'][worker] = {
                            'complexity_cap': proposal.get('approved_config', {}).get('max_complexity', 0.8),
                            'fallback_enabled': True
                        }

        return insights

    def _load_sequence(self) -> int:
        """Get next sequence number from journal."""
        if not self.journal_path.exists():
            return 0
        with open(self.journal_path) as f:
            lines = f.readlines()
            if not lines:
                return 0
            last = json.loads(lines[-1])
            return last['seq'] + 1

    def _get_recent_observations(self, n: int) -> List[int]:
        """Get last n observation IDs."""
        if not self.journal_path.exists():
            return []
        with open(self.journal_path) as f:
            lines = f.readlines()
            recent = [json.loads(line) for line in lines[-n:]]
            return [r['seq'] for r in recent]

    def _similarity_score(self, id1: int, id2: int) -> float:
        """Calculate contextual similarity between two observations."""
        # Simplified: same operation type = 0.5 base
        rec1 = self._get_journal_entry(id1)
        rec2 = self._get_journal_entry(id2)

        if rec1['type'] != rec2['type']:
            return 0.0

        score = 0.5

        # Context similarity
        ctx1 = set(rec1.get('context', {}).keys())
        ctx2 = set(rec2.get('context', {}).keys())
        if ctx1 & ctx2:  # Intersection
            score += 0.3 * (len(ctx1 & ctx2) / max(len(ctx1), len(ctx2)))

        return min(score, 1.0)

    def _get_journal_entry(self, seq_id: int) -> Dict:
        """Retrieve specific journal entry by sequence ID."""
        with open(self.journal_path) as f:
            for line in f:
                record = json.loads(line)
                if record['seq'] == seq_id:
                    return record
        return {}

    async def _compaction_pass(self):
        """
        Extended with ORB-style edge detection and clutter repair.
        SAFE: Never deletes journal entries. Only optimizes graph structure.
        """
        if self.graph is None:
            return

        # Phase 1: Edge weight decay (temporal relevance)
        await self._apply_edge_decay()

        # Phase 2: Clutter detection (finding noise)
        clutter_edges, clutter_nodes = self._detect_clutter()

        # Phase 3: Self-repair (structural optimization)
        if clutter_edges or clutter_nodes:
            await self._self_repair(clutter_edges, clutter_nodes)

        # Phase 4: Graph integrity check
        await self._verify_graph_integrity()

        # Save optimized graph (journal preserved)
        try:
            nx.write_graphml(self.graph, self.field_path / 'field_graph.graphml')
            nx.write_graphml(self.graph, self.field_path / f'field_graph_backup_{datetime.utcnow().strftime("%Y%m%d")}.graphml')
        except Exception as e:
            logger.warning(f"Failed to save graph: {e}")

    async def _apply_edge_decay(self):
        """
        Decay edge weights based on age (temporal relevance).
        Recent observations maintain strong connections.
        Old patterns fade unless reinforced.
        """
        if self.graph is None:
            return

        current_time = datetime.utcnow()

        for u, v, data in self.graph.edges(data=True):
            edge_timestamp = data.get('created_at', datetime.utcnow().isoformat())
            edge_time = datetime.fromisoformat(edge_timestamp)

            # Calculate age in days
            age_days = (current_time - edge_time).days

            # Exponential decay: weight * (0.5 ^ (age / half_life))
            decay_factor = 0.5 ** (age_days / self.edge_decay_half_life)

            # Apply decay but keep minimum trace for history
            original_weight = data.get('original_weight', data.get('weight', 1.0))
            data['weight'] = max(0.05, original_weight * decay_factor)
            data['original_weight'] = original_weight  # Preserve original for reference

    def _detect_clutter(self) -> Tuple[Set, Set]:
        """
        Detect graph clutter using edge strength and node connectivity.

        Clutter indicators:
        1. Edge weight below threshold (weak/obsolete pattern)
        2. Node degree < 2 (isolated observation, no pattern value)
        3. Self-loops with no external connections
        4. Duplicate edges (redundant paths between same nodes)
        """
        if self.graph is None:
            return set(), set()

        clutter_edges = set()
        clutter_nodes = set()

        # Detect weak edges (clutter)
        for u, v, data in self.graph.edges(data=True):
            if data.get('weight', 1.0) < self.clutter_threshold:
                clutter_edges.add((u, v))

            # Check for similarity relation decay
            if data.get('relation') == 'similar_context' and data.get('weight', 0) < 0.2:
                clutter_edges.add((u, v))

        # Detect isolated nodes (orphaned observations)
        for node, data in self.graph.nodes(data=True):
            degree = self.graph.degree(node)

            # Keep recent nodes even if isolated (< 7 days)
            node_time = datetime.fromisoformat(data.get('timestamp', datetime.utcnow().isoformat()))
            age_days = (datetime.utcnow() - node_time).days

            if degree < self.min_node_degree and age_days > 7:
                # Check if this node has valuable outcome data
                if data.get('outcome') != 'failure':  # Keep failures for learning
                    clutter_nodes.add(node)

            # Detect self-referential clutter (nodes that only point to themselves)
            if self.graph.has_edge(node, node) and degree == 1:
                clutter_edges.add((node, node))
                clutter_nodes.add(node)

        # Detect duplicate/redundant edges
        seen_pairs = {}
        for u, v, key in self.graph.edges(keys=True):  # MultiDiGraph support
            pair = (min(u, v), max(u, v))
            if pair in seen_pairs:
                # Keep the stronger edge, mark weaker as clutter
                existing_weight = seen_pairs[pair]['weight']
                current_weight = self.graph[u][v][key]['weight']

                if current_weight < existing_weight:
                    clutter_edges.add((u, v, key))
                else:
                    seen_pairs[pair] = self.graph[u][v][key]
            else:
                seen_pairs[pair] = self.graph[u][v][key]

        return clutter_edges, clutter_nodes

    async def _self_repair(self, clutter_edges: Set, clutter_nodes: Set):
        """
        ORB-style self-repair: Remove clutter, preserve knowledge.

        RULES:
        1. Never delete journal entries (immutable history preserved)
        2. Archive clutter nodes (moved to cold storage, not deleted)
        3. Merge duplicate patterns (consolidate similar learnings)
        4. Strengthen high-value connections (reinforce useful patterns)
        """
        if self.graph is None:
            return

        repair_op = {
            'timestamp': datetime.utcnow().isoformat(),
            'edges_pruned': len(clutter_edges),
            'nodes_archived': len(clutter_nodes),
            'details': []
        }

        # Archive clutter nodes (don't delete, move to cold storage)
        archived_nodes = []
        for node in clutter_nodes:
            node_data = dict(self.graph.nodes[node])
            archived_nodes.append({
                'sequence_id': node,
                'data': node_data,
                'archived_reason': 'low_connectivity',
                'original_journal_entry': self._get_journal_entry(node)
            })

            # Remove from active graph (journal stays)
            self.graph.remove_node(node)

        # Save archive
        archive_path = self.field_path / f'node_archive_{datetime.utcnow().strftime("%Y%m%d")}.jsonl'
        with open(archive_path, 'a') as f:
            for item in archived_nodes:
                f.write(json.dumps(item) + '\n')

        # Prune clutter edges (structural only)
        for edge in clutter_edges:
            if len(edge) == 3:  # (u, v, key) format
                u, v, key = edge
                if self.graph.has_edge(u, v, key):
                    self.graph.remove_edge(u, v, key)
            else:
                u, v = edge
                if self.graph.has_edge(u, v):
                    self.graph.remove_edge(u, v)

        # MERGE: Consolidate similar patterns (knowledge compression)
        merged_count = await self._consolidate_patterns()
        repair_op['patterns_merged'] = merged_count

        # REINFORCE: Strengthen edges between high-value observations
        reinforced_count = await self._reinforce_valuable_connections()
        repair_op['connections_reinforced'] = reinforced_count

        # Log repair operation (audit trail)
        with open(self.repair_log, 'a') as f:
            f.write(json.dumps(repair_op) + '\n')

        self.clutter_stats['edges_pruned'] += len(clutter_edges)
        self.clutter_stats['nodes_archived'] += len(clutter_nodes)

    async def _consolidate_patterns(self) -> int:
        """
        Merge redundant pattern observations into meta-patterns.
        Similar to ORB's edge consolidation but for GOAT's operational data.
        """
        if self.graph is None:
            return 0

        merge_count = 0

        # Find clusters of similar successful operations
        success_nodes = [n for n, d in self.graph.nodes(data=True)
                        if d.get('outcome') == 'success']

        # Group by operation type and file type
        pattern_groups = {}
        for node in success_nodes:
            record = self._get_journal_entry(node)
            op_type = record.get('type', 'unknown')
            file_type = record.get('context', {}).get('file_types', ['unknown'])[0]

            key = (op_type, file_type)
            if key not in pattern_groups:
                pattern_groups[key] = []
            pattern_groups[key].append(node)

        # Create meta-nodes for dense clusters (>5 similar operations)
        for (op_type, file_type), nodes in pattern_groups.items():
            if len(nodes) > 5:
                # Create meta-pattern node
                meta_id = f"meta_{op_type}_{file_type}_{datetime.utcnow().strftime('%Y%m%d')}"

                # Calculate aggregate metrics
                total_time = sum(
                    self._get_journal_entry(n).get('metrics', {}).get('processing_time_ms', 0)
                    for n in nodes
                ) / len(nodes)

                self.graph.add_node(
                    meta_id,
                    type='meta_pattern',
                    operation=op_type,
                    file_type=file_type,
                    avg_processing_time=total_time,
                    instance_count=len(nodes),
                    created_at=datetime.utcnow().isoformat(),
                    constituent_nodes=nodes  # Reference to originals
                )

                # Connect meta-node to all instances (with strong weights)
                for node in nodes:
                    self.graph.add_edge(
                        meta_id, node,
                        weight=0.9,
                        relation='consolidates',
                        created_at=datetime.utcnow().isoformat()
                    )

                merge_count += 1

        return merge_count

    async def _reinforce_valuable_connections(self) -> int:
        """
        Strengthen connections that led to successful outcomes.
        Hebbian-style reinforcement (what fires together, wires together).
        """
        if self.graph is None:
            return 0

        reinforced = 0

        for u, v, data in self.graph.edges(data=True):
            u_outcome = self.graph.nodes[u].get('outcome')
            v_outcome = self.graph.nodes[v].get('outcome')

            # If both connected observations were successful, strengthen bond
            if u_outcome == 'success' and v_outcome == 'success':
                current_weight = data.get('weight', 0.5)
                new_weight = min(0.95, current_weight * 1.1)  # Cap at 0.95

                if new_weight > current_weight:
                    data['weight'] = new_weight
                    data['reinforced_at'] = datetime.utcnow().isoformat()
                    reinforced += 1

        return reinforced

    async def _verify_graph_integrity(self):
        """
        Post-repair verification.
        Ensures no critical data loss, graph is navigable.
        """
        if self.graph is None:
            return

        # Check 1: All journal entries have graph nodes OR are archived
        active_nodes = set(self.graph.nodes())

        with open(self.journal_path) as f:
            for line in f:
                record = json.loads(line)
                seq = record['seq']

                # Must be in graph OR archived (not lost)
                if seq not in active_nodes:
                    # Check if recently archived
                    archive_exists = any(
                        f'node_archive_{datetime.utcnow().strftime("%Y%m%d")}' in fname
                        for fname in os.listdir(self.field_path)
                        if fname.startswith('node_archive')
                    )
                    if not archive_exists and (datetime.utcnow() - datetime.fromisoformat(record['ts'])).days > 7:
                        raise IntegrityError(f"Node {seq} missing from graph and archive!")

        # Check 2: Graph weakly connected (no orphaned islands)
        if len(self.graph) > 0:
            try:
                components = list(nx.weakly_connected_components(self.graph))
                if len(components) > 3:  # Allow some fragmentation but not too much
                    # Log warning for manual review
                    logger.warning(f"Graph fragmented into {len(components)} components. Consider manual review.")
            except:
                pass  # NetworkX version compatibility

        # Check 3: No negative weights or NaN values
        for u, v, data in self.graph.edges(data=True):
            weight = data.get('weight', 0)
            if weight < 0 or (isinstance(weight, float) and np.isnan(weight)):
                raise IntegrityError(f"Invalid weight {weight} on edge {u}-{v}")

    def get_graph_health_report(self) -> Dict:
        """
        Diagnostic report for admin review.
        """
        if self.graph is None:
            return {'status': 'networkx_unavailable'}

        try:
            return {
                'total_nodes': self.graph.number_of_nodes(),
                'total_edges': self.graph.number_of_edges(),
                'avg_clustering': nx.average_clustering(self.graph) if len(self.graph) > 0 else 0,
                'graph_density': nx.density(self.graph) if len(self.graph) > 0 else 0,
                'clutter_stats': self.clutter_stats,
                'last_repair': self._get_last_repair_time(),
                'archived_nodes': self._count_archived_nodes(),
                'meta_patterns': len([n for n, d in self.graph.nodes(data=True)
                                    if d.get('type') == 'meta_pattern']),
                'status': 'healthy' if len(self.graph) == 0 or nx.is_weakly_connected(self.graph) else 'fragmented'
            }
        except:
            return {
                'total_nodes': self.graph.number_of_nodes(),
                'total_edges': self.graph.number_of_edges(),
                'status': 'analysis_error'
            }

    def _get_last_repair_time(self):
        if not self.repair_log.exists():
            return None
        try:
            with open(self.repair_log) as f:
                lines = f.readlines()
                if lines:
                    return json.loads(lines[-1])['timestamp']
        except:
            pass
        return None

    def _count_archived_nodes(self):
        count = 0
        try:
            for fname in os.listdir(self.field_path):
                if fname.startswith('node_archive_'):
                    with open(self.field_path / fname) as f:
                        count += sum(1 for _ in f)
        except:
            pass
        return count

    def _load_patterns(self):
        """Load previously learned patterns."""
        pattern_file = self.field_path / 'learned_patterns.json'
        if pattern_file.exists():
            self.learned_patterns = json.loads(pattern_file.read_text())
        else:
            self.learned_patterns = {}