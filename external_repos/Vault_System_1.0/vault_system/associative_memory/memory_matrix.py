import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import heapq

@dataclass
class MemoryNode:
    coordinates: Tuple[int, int, int]
    activation: float
    associations: List[str]
    last_accessed: float
    access_count: int

class EnhancedMemoryMatrix:
    def __init__(self, dimensions: Tuple[int, int, int] = (20, 20, 10)):
        self.dimensions = dimensions
        self.matrix = np.zeros(dimensions)
        self.associations = {}
        self.activation_history = []
        self.node_metadata = {}
        self.learning_rate = 0.1
        self.activation_threshold = 0.6
        
    def store_pattern(self, pattern: List[float], associations: List[str], 
                     metadata: Dict[str, Any] = None) -> Optional[Tuple[int, int, int]]:
        """Store pattern with metadata and return coordinates"""
        
        # Normalize pattern
        norm_pattern = self._normalize_pattern(pattern)
        if not norm_pattern:
            return None
            
        # Find best storage location
        coords = self._find_optimal_location(norm_pattern)
        if not coords:
            return None
            
        # Store pattern and associations
        self.matrix[coords] = np.mean(norm_pattern)
        self.associations[coords] = associations
        
        # Create memory node
        memory_node = MemoryNode(
            coordinates=coords,
            activation=np.mean(norm_pattern),
            associations=associations,
            last_accessed=float(np.datetime64('now').astype(int)),
            access_count=1
        )
        
        self.node_metadata[coords] = {
            'node': memory_node,
            'metadata': metadata or {},
            'storage_time': float(np.datetime64('now').astype(int))
        }
        
        return coords
    
    def recall_pattern(self, trigger: List[float], similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Recall patterns with similarity scoring"""
        trigger_norm = self._normalize_pattern(trigger)
        if not trigger_norm:
            return []
            
        matches = []
        
        for coords, node_data in self.node_metadata.items():
            stored_value = self.matrix[coords]
            similarity = self._calculate_similarity(trigger_norm, [stored_value])
            
            if similarity >= similarity_threshold:
                node = node_data['node']
                node.access_count += 1
                node.last_accessed = float(np.datetime64('now').astype(int))
                
                matches.append({
                    'associations': node.associations,
                    'similarity': similarity,
                    'coordinates': coords,
                    'metadata': node_data['metadata'],
                    'activation': node.activation
                })
        
        # Sort by similarity
        return sorted(matches, key=lambda x: x['similarity'], reverse=True)
    
    def associative_chaining(self, start_pattern: List[float], depth: int = 3) -> List[List[str]]:
        """Perform associative chaining to find related patterns"""
        chains = []
        visited = set()
        
        def _chain(current_pattern: List[float], current_depth: int, current_chain: List[str]):
            if current_depth >= depth:
                chains.append(current_chain.copy())
                return
                
            matches = self.recall_pattern(current_pattern, 0.5)
            for match in matches:
                chain_key = tuple(match['coordinates'])
                if chain_key in visited:
                    continue
                    
                visited.add(chain_key)
                current_chain.extend(match['associations'])
                
                # Create new trigger from associations
                new_trigger = [len(assoc) for assoc in match['associations']]
                _chain(new_trigger, current_depth + 1, current_chain)
                
                # Backtrack
                for _ in range(len(match['associations'])):
                    current_chain.pop()
        
        _chain(start_pattern, 0, [])
        return chains
    
    def _find_optimal_location(self, pattern: List[float]) -> Optional[Tuple[int, int, int]]:
        """Find optimal location for pattern storage"""
        pattern_value = np.mean(pattern)
        
        # Try to find similar patterns first
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                for k in range(self.dimensions[2]):
                    if self.matrix[i, j, k] == 0:
                        # Found empty slot
                        return (i, j, k)
                    else:
                        # Check if similar pattern exists
                        if abs(self.matrix[i, j, k] - pattern_value) < 0.1:
                            return (i, j, k)
        
        return None
    
    def _normalize_pattern(self, pattern: List[float]) -> List[float]:
        """Enhanced pattern normalization"""
        if not pattern:
            return []
            
        pattern_array = np.array(pattern)
        if np.all(pattern_array == 0):
            return [0.5] * len(pattern)
            
        # Handle outliers
        Q1 = np.percentile(pattern_array, 25)
        Q3 = np.percentile(pattern_array, 75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Clip outliers
        clipped_pattern = np.clip(pattern_array, lower_bound, upper_bound)
        
        # Normalize to [0, 1]
        if np.max(clipped_pattern) == np.min(clipped_pattern):
            return [0.5] * len(pattern)
            
        normalized = (clipped_pattern - np.min(clipped_pattern)) / (np.max(clipped_pattern) - np.min(clipped_pattern))
        return normalized.tolist()
    
    def _calculate_similarity(self, pattern1: List[float], pattern2: List[float]) -> float:
        """Calculate pattern similarity using multiple metrics"""
        if len(pattern1) != len(pattern2):
            # Use the minimum length
            min_len = min(len(pattern1), len(pattern2))
            pattern1 = pattern1[:min_len]
            pattern2 = pattern2[:min_len]
            
        # Cosine similarity
        dot_product = np.dot(pattern1, pattern2)
        norm1 = np.linalg.norm(pattern1)
        norm2 = np.linalg.norm(pattern2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        cosine_sim = dot_product / (norm1 * norm2)
        return max(0.0, min(1.0, cosine_sim))
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory matrix statistics"""
        total_capacity = np.prod(self.dimensions)
        used_capacity = np.count_nonzero(self.matrix)
        
        return {
            'total_capacity': total_capacity,
            'used_capacity': used_capacity,
            'utilization_rate': used_capacity / total_capacity,
            'total_associations': len(self.associations),
            'active_nodes': len(self.node_metadata)
        }