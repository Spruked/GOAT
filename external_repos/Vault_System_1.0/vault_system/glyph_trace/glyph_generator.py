import hashlib
import time
import numpy as np
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from enum import Enum

class GlyphType(Enum):
    DATA_GLYPH = "data_glyph"
    ACCESS_GLYPH = "access_glyph"
    SECURITY_GLYPH = "security_glyph"
    TEMPORAL_GLYPH = "temporal_glyph"

@dataclass
class VaultGlyph:
    pattern: str
    complexity: int
    entropy: float
    timestamp: float
    trace_path: List[str]
    glyph_type: GlyphType
    integrity_hash: str
    metadata: Dict[str, Any]

class GlyphGenerator:
    def __init__(self):
        self.glyph_registry = {}
        self.pattern_history = []
        
    def generate_data_glyph(self, data: str, vault_id: str, metadata: Dict[str, Any] = None) -> VaultGlyph:
        """Generate glyph for data storage"""
        data_hash = hashlib.sha3_256(data.encode()).hexdigest()
        pattern = self._create_pattern(data_hash, vault_id)
        integrity_hash = self._calculate_integrity_hash(pattern, vault_id)
        
        glyph = VaultGlyph(
            pattern=pattern,
            complexity=len(data),
            entropy=self._calculate_entropy(data),
            timestamp=time.time(),
            trace_path=[vault_id, f"data_glyph_{int(time.time())}"],
            glyph_type=GlyphType.DATA_GLYPH,
            integrity_hash=integrity_hash,
            metadata=metadata or {}
        )
        
        self.glyph_registry[pattern] = asdict(glyph)
        self.pattern_history.append(pattern)
        
        return glyph
    
    def generate_access_glyph(self, vault_id: str, operation: str) -> VaultGlyph:
        """Generate glyph for access operations"""
        access_hash = hashlib.sha3_256(f"{vault_id}_{operation}_{time.time()}".encode()).hexdigest()
        pattern = self._create_pattern(access_hash, "access")
        
        glyph = VaultGlyph(
            pattern=pattern,
            complexity=len(operation),
            entropy=0.8,  # High entropy for security
            timestamp=time.time(),
            trace_path=[vault_id, f"access_{operation}"],
            glyph_type=GlyphType.ACCESS_GLYPH,
            integrity_hash=self._calculate_integrity_hash(pattern, "access"),
            metadata={"operation": operation, "vault_id": vault_id}
        )
        
        return glyph
    
    def _create_pattern(self, hash_base: str, context: str) -> str:
        """Create a unique pattern from hash and context"""
        combined = f"{hash_base}_{context}_{time.time()}"
        pattern_hash = hashlib.sha3_256(combined.encode()).hexdigest()
        
        # Create visual pattern representation
        pattern_chars = []
        for i in range(0, min(32, len(pattern_hash)), 2):
            hex_pair = pattern_hash[i:i+2]
            decimal_val = int(hex_pair, 16)
            # Map to printable characters
            pattern_chars.append(chr((decimal_val % 26) + 65))  # A-Z
        
        return ''.join(pattern_chars)
    
    def _calculate_entropy(self, data: str) -> float:
        """Calculate Shannon entropy with enhanced metrics"""
        if not data:
            return 0.0
            
        entropy = 0.0
        for x in range(256):
            p_x = float(data.encode('utf-8').count(bytes([x]))) / len(data.encode('utf-8'))
            if p_x > 0:
                entropy += -p_x * np.log2(p_x)
                
        return entropy
    
    def _calculate_integrity_hash(self, pattern: str, context: str) -> str:
        """Calculate integrity verification hash"""
        return hashlib.sha3_512(f"{pattern}_{context}".encode()).hexdigest()
    
    def verify_glyph_integrity(self, glyph: VaultGlyph) -> bool:
        """Verify glyph hasn't been tampered with"""
        expected_hash = self._calculate_integrity_hash(glyph.pattern, glyph.trace_path[0])
        return glyph.integrity_hash == expected_hash
    
    def find_similar_patterns(self, target_pattern: str, threshold: float = 0.7) -> List[str]:
        """Find patterns similar to target (for pattern analysis)"""
        similar = []
        for pattern in self.pattern_history:
            similarity = self._pattern_similarity(target_pattern, pattern)
            if similarity >= threshold:
                similar.append(pattern)
        return similar
    
    def _pattern_similarity(self, pattern1: str, pattern2: str) -> float:
        """Calculate similarity between two patterns"""
        if not pattern1 or not pattern2:
            return 0.0
            
        set1, set2 = set(pattern1), set(pattern2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0