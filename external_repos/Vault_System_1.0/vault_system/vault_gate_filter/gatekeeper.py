from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import time
import hashlib
from enum import Enum
import numpy as np

class GateAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    QUARANTINE = "quarantine"
    TRANSFORM = "transform"

class SecurityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class GateDecision:
    action: GateAction
    confidence: float
    security_level: SecurityLevel
    reasoning: List[str]
    transformations: List[str]
    timestamp: float

class VaultGatekeeper:
    def __init__(self, default_security_level: SecurityLevel = SecurityLevel.MEDIUM):
        self.default_security_level = default_security_level
        self.access_patterns = {}
        self.threat_signatures = set()
        self.quarantine_queue = []
        self.decision_log = []
        
    def evaluate_input(self, data: Any, source: str, metadata: Dict[str, Any]) -> GateDecision:
        """Evaluate input through security gates"""
        security_checks = []
        
        # Source validation
        source_check = self._validate_source(source, metadata)
        security_checks.append(source_check)
        
        # Data integrity check
        integrity_check = self._check_data_integrity(data, metadata)
        security_checks.append(integrity_check)
        
        # Pattern analysis
        pattern_check = self._analyze_patterns(data, source)
        security_checks.append(pattern_check)
        
        # Threat assessment
        threat_check = self._assess_threats(data, source, metadata)
        security_checks.append(threat_check)
        
        # Make final decision
        decision = self._make_final_decision(security_checks, data, source)
        self.decision_log.append(decision)
        
        return decision
    
    def _validate_source(self, source: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data source"""
        checks = {
            'source_known': source in self.access_patterns,
            'source_reputation': self._get_source_reputation(source),
            'authentication': metadata.get('authenticated', False),
            'encryption': metadata.get('encrypted', False)
        }
        
        score = sum(1 for check in checks.values() if check) / len(checks)
        
        return {
            'check_type': 'source_validation',
            'score': score,
            'details': checks
        }
    
    def _check_data_integrity(self, data: Any, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Check data integrity and structure"""
        try:
            data_str = str(data)
            checks = {
                'size_reasonable': len(data_str) < 1000000,  # 1MB limit
                'structure_valid': self._validate_structure(data),
                'encoding_valid': self._check_encoding(data_str),
                'checksum_match': self._verify_checksum(data, metadata)
            }
            
            score = sum(1 for check in checks.values() if check) / len(checks)
            
        except Exception as e:
            checks = {'error': str(e)}
            score = 0.0
            
        return {
            'check_type': 'data_integrity',
            'score': score,
            'details': checks
        }
    
    def _analyze_patterns(self, data: Any, source: str) -> Dict[str, Any]:
        """Analyze data patterns for anomalies"""
        data_str = str(data)
        
        patterns = {
            'suspicious_keywords': self._detect_suspicious_keywords(data_str),
            'unusual_encoding': self._detect_unusual_encoding(data_str),
            'frequency_analysis': self._frequency_analysis(data_str),
            'entropy_analysis': self._entropy_analysis(data_str)
        }
        
        # Calculate anomaly score
        anomaly_score = (
            patterns['suspicious_keywords'] * 0.4 +
            patterns['unusual_encoding'] * 0.3 +
            patterns['frequency_analysis'] * 0.2 +
            patterns['entropy_analysis'] * 0.1
        )
        
        return {
            'check_type': 'pattern_analysis',
            'score': 1.0 - anomaly_score,  # Convert to trust score
            'details': patterns
        }
    
    def _assess_threats(self, data: Any, source: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Assess potential threats"""
        threat_indicators = {
            'known_threat_signature': self._check_threat_signatures(data),
            'behavioral_anomaly': self._detect_behavioral_anomaly(source, metadata),
            'temporal_anomaly': self._detect_temporal_anomaly(metadata),
            'access_pattern_anomaly': self._detect_access_anomaly(source)
        }
        
        threat_score = sum(1 for indicator in threat_indicators.values() if indicator) / len(threat_indicators)
        
        return {
            'check_type': 'threat_assessment',
            'score': 1.0 - threat_score,  # Convert to trust score
            'details': threat_indicators
        }
    
    def _make_final_decision(self, security_checks: List[Dict[str, Any]], 
                           data: Any, source: str) -> GateDecision:
        """Make final gate decision"""
        # Calculate overall confidence
        overall_confidence = sum(check['score'] for check in security_checks) / len(security_checks)
        
        # Determine action based on confidence thresholds
        if overall_confidence >= 0.8:
            action = GateAction.ALLOW
            security_level = SecurityLevel.LOW
        elif overall_confidence >= 0.6:
            action = GateAction.ALLOW
            security_level = SecurityLevel.MEDIUM
        elif overall_confidence >= 0.4:
            action = GateAction.TRANSFORM
            security_level = SecurityLevel.HIGH
        else:
            action = GateAction.QUARANTINE
            security_level = SecurityLevel.CRITICAL
        
        reasoning = [
            f"Overall confidence: {overall_confidence:.2f}",
            f"Source: {source}",
            f"Data type: {type(data).__name__}"
        ]
        
        # Add specific reasoning from checks
        for check in security_checks:
            if check['score'] < 0.5:
                reasoning.append(f"Low score in {check['check_type']}: {check['score']:.2f}")
        
        transformations = []
        if action == GateAction.TRANSFORM:
            transformations = self._determine_transformations(data, security_checks)
        
        return GateDecision(
            action=action,
            confidence=overall_confidence,
            security_level=security_level,
            reasoning=reasoning,
            transformations=transformations,
            timestamp=time.time()
        )
    
    def _validate_structure(self, data: Any) -> bool:
        """Validate data structure"""
        if isinstance(data, (str, int, float, bool)):
            return True
        elif isinstance(data, (list, dict)):
            return len(str(data)) < 10000  # Size limit for complex structures
        else:
            return False
    
    def _check_encoding(self, data_str: str) -> bool:
        """Check if encoding is valid"""
        try:
            data_str.encode('utf-8')
            return True
        except UnicodeEncodeError:
            return False
    
    def _verify_checksum(self, data: Any, metadata: Dict[str, Any]) -> bool:
        """Verify data checksum if provided"""
        if 'checksum' not in metadata:
            return True
            
        data_str = str(data)
        calculated_checksum = hashlib.md5(data_str.encode()).hexdigest()
        return calculated_checksum == metadata['checksum']
    
    def _detect_suspicious_keywords(self, data_str: str) -> float:
        """Detect suspicious keywords or patterns"""
        suspicious_patterns = [
            'javascript:', 'eval(', 'exec(', 'system(', 'shell_exec',
            'base64_decode', 'document.cookie', '<script>', 'onerror='
        ]
        
        matches = sum(1 for pattern in suspicious_patterns if pattern in data_str.lower())
        return min(1.0, matches / 3)  # Normalize to 0-1
    
    def _detect_unusual_encoding(self, data_str: str) -> float:
        """Detect unusual encoding patterns"""
        # Check for high ratio of non-printable characters
        printable_chars = sum(1 for char in data_str if char.isprintable() or char in ' \t\n\r')
        ratio = printable_chars / len(data_str) if data_str else 1.0
        return 1.0 - ratio  # Higher score for more non-printable
    
    def _frequency_analysis(self, data_str: str) -> float:
        """Perform frequency analysis for anomaly detection"""
        if len(data_str) < 10:
            return 0.0
            
        # Simple frequency analysis
        char_freq = {}
        for char in data_str:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        # Calculate entropy of frequencies
        total_chars = len(data_str)
        entropy = 0.0
        for count in char_freq.values():
            probability = count / total_chars
            entropy -= probability * np.log2(probability)
        
        # Normalize entropy (max ~8 for extended ASCII)
        normalized_entropy = entropy / 8.0
        return 1.0 - normalized_entropy  # Higher score for lower entropy (more predictable)
    
    def _entropy_analysis(self, data_str: str) -> float:
        """Analyze data entropy"""
        if not data_str:
            return 0.0
            
        entropy = 0.0
        for x in range(256):
            p_x = float(data_str.encode('utf-8').count(bytes([x]))) / len(data_str.encode('utf-8'))
            if p_x > 0:
                entropy += -p_x * np.log2(p_x)
        
        # Normalize (max ~8 for random data)
        normalized_entropy = min(1.0, entropy / 8.0)
        return normalized_entropy  # Higher score for higher entropy (more random)
    
    def _check_threat_signatures(self, data: Any) -> bool:
        """Check against known threat signatures"""
        data_str = str(data)
        return any(signature in data_str for signature in self.threat_signatures)
    
    def _detect_behavioral_anomaly(self, source: str, metadata: Dict[str, Any]) -> bool:
        """Detect behavioral anomalies"""
        # Track source access patterns
        if source not in self.access_patterns:
            self.access_patterns[source] = {
                'access_count': 0,
                'last_access': time.time(),
                'data_sizes': []
            }
        
        pattern = self.access_patterns[source]
        pattern['access_count'] += 1
        pattern['last_access'] = time.time()
        
        # Check for rapid access (potential attack)
        if pattern['access_count'] > 100:  # More than 100 accesses
            return True
            
        return False
    
    def _detect_temporal_anomaly(self, metadata: Dict[str, Any]) -> bool:
        """Detect temporal anomalies"""
        current_time = time.time()
        data_timestamp = metadata.get('timestamp', current_time)
        
        # Check for future timestamps or very old timestamps
        time_diff = abs(current_time - data_timestamp)
        if time_diff > 365 * 24 * 3600:  # More than 1 year difference
            return True
            
        return False
    
    def _detect_access_anomaly(self, source: str) -> bool:
        """Detect access pattern anomalies"""
        if source not in self.access_patterns:
            return False
            
        pattern = self.access_patterns[source]
        
        # Check for unusually high access frequency
        if pattern['access_count'] > 1000:  # Very high access count
            return True
            
        return False
    
    def _determine_transformations(self, data: Any, security_checks: List[Dict[str, Any]]) -> List[str]:
        """Determine necessary data transformations"""
        transformations = []
        
        # Add transformations based on security check results
        for check in security_checks:
            if check['score'] < 0.7:
                if check['check_type'] == 'data_integrity':
                    transformations.append('sanitize_input')
                elif check['check_type'] == 'pattern_analysis':
                    transformations.append('normalize_encoding')
                elif check['check_type'] == 'threat_assessment':
                    transformations.append('apply_content_filter')
        
        return transformations
    
    def add_threat_signature(self, signature: str):
        """Add new threat signature to detection database"""
        self.threat_signatures.add(signature)
    
    def get_gate_statistics(self) -> Dict[str, Any]:
        """Get gatekeeper statistics"""
        total_decisions = len(self.decision_log)
        if total_decisions == 0:
            return {}
            
        action_counts = {}
        for decision in self.decision_log:
            action = decision.action.value
            action_counts[action] = action_counts.get(action, 0) + 1
        
        avg_confidence = sum(decision.confidence for decision in self.decision_log) / total_decisions
        
        return {
            'total_decisions': total_decisions,
            'action_distribution': action_counts,
            'avg_confidence': avg_confidence,
            'known_sources': len(self.access_patterns),
            'threat_signatures': len(self.threat_signatures),
            'quarantine_queue_size': len(self.quarantine_queue)
        }