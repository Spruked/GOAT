from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import time
import json
from collections import defaultdict, deque
import numpy as np
from enum import Enum

class DecisionType(Enum):
    PRIOR_DECISION = "prior"
    POSTERIORI_DECISION = "posteriori"
    IMMEDIATE_DECISION = "immediate"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class DecisionContext:
    context_hash: str
    parameters: Dict[str, Any]
    environmental_factors: Dict[str, float]
    temporal_factors: Dict[str, Any]

@dataclass
class DecisionRecord:
    decision_id: str
    decision_type: DecisionType
    context: DecisionContext
    confidence: float
    expected_return: float
    risk_level: RiskLevel
    timestamp: float
    reasoning: List[str]
    metadata: Dict[str, Any]

@dataclass 
class ImmediateReturn:
    decision_id: str
    expected: float
    actual: float
    return_ratio: float
    timestamp: float
    risk_adjusted_return: float

class EnhancedDecisionEngine:
    def __init__(self, risk_tolerance: float = 0.3):
        self.risk_tolerance = risk_tolerance
        self.prior_knowledge = {}
        self.decision_history = deque(maxlen=1000)
        self.immediate_returns = deque(maxlen=500)
        self.risk_profiles = defaultdict(lambda: RiskLevel.MEDIUM)
        self.learning_rate = 0.1
        
    def extract_prior_decision(self, context: Dict[str, Any]) -> DecisionRecord:
        """Extract decision based on prior knowledge"""
        context_obj = self._create_context(context)
        context_hash = context_obj.context_hash
        
        # Get prior knowledge or default
        prior = self.prior_knowledge.get(context_hash, {
            'confidence': 0.5,
            'expected_return': 0,
            'risk_level': RiskLevel.MEDIUM,
            'success_rate': 0.5
        })
        
        # Calculate risk-adjusted decision
        risk_adjusted_confidence = self._adjust_for_risk(prior['confidence'], prior['risk_level'])
        
        decision = DecisionRecord(
            decision_id=f"prior_{int(time.time())}_{hash(context_hash) % 10000:04d}",
            decision_type=DecisionType.PRIOR_DECISION,
            context=context_obj,
            confidence=risk_adjusted_confidence,
            expected_return=prior['expected_return'],
            risk_level=prior['risk_level'],
            timestamp=time.time(),
            reasoning=[f"Prior knowledge for context {context_hash[:8]}"],
            metadata={'prior_reference': context_hash}
        )
        
        self.decision_history.append(decision)
        return decision
    
    def extract_posteriori_decision(self, context: Dict[str, Any], 
                                  evidence: Dict[str, Any]) -> DecisionRecord:
        """Extract decision updated with new evidence"""
        prior_decision = self.extract_prior_decision(context)
        
        # Update with Bayesian reasoning
        evidence_confidence = evidence.get('confidence_boost', 0)
        return_adjustment = evidence.get('return_adjustment', 0)
        risk_modifier = evidence.get('risk_modifier', 1.0)
        
        # Calculate posterior confidence
        posterior_confidence = self._combine_confidence(
            prior_decision.confidence, 
            evidence_confidence,
            evidence.get('evidence_strength', 0.5)
        )
        
        # Adjust risk level
        new_risk_level = self._modify_risk_level(prior_decision.risk_level, risk_modifier)
        
        posterior_decision = DecisionRecord(
            decision_id=f"posterior_{int(time.time())}_{hash(prior_decision.decision_id) % 10000:04d}",
            decision_type=DecisionType.POSTERIORI_DECISION,
            context=prior_decision.context,
            confidence=posterior_confidence,
            expected_return=prior_decision.expected_return + return_adjustment,
            risk_level=new_risk_level,
            timestamp=time.time(),
            reasoning=prior_decision.reasoning + [
                f"Evidence-based update: {evidence_confidence} confidence boost",
                f"Return adjustment: {return_adjustment}",
                f"Risk modification: {risk_modifier}x"
            ],
            metadata={
                'prior_decision_id': prior_decision.decision_id,
                'evidence': evidence
            }
        )
        
        # Update prior knowledge
        self._update_prior_knowledge(prior_decision.context.context_hash, posterior_decision)
        
        self.decision_history.append(posterior_decision)
        return posterior_decision
    
    def calculate_immediate_return(self, decision: DecisionRecord, 
                                 actual_outcome: float) -> ImmediateReturn:
        """Calculate immediate return with risk adjustment"""
        expected = decision.expected_return
        actual = actual_outcome
        
        # Calculate basic return ratio
        return_ratio = actual / expected if expected != 0 else 0
        
        # Calculate risk-adjusted return
        risk_factor = self._risk_level_to_factor(decision.risk_level)
        risk_adjusted_return = return_ratio / risk_factor if risk_factor > 0 else return_ratio
        
        immediate_return = ImmediateReturn(
            decision_id=decision.decision_id,
            expected=expected,
            actual=actual,
            return_ratio=return_ratio,
            timestamp=time.time(),
            risk_adjusted_return=risk_adjusted_return
        )
        
        self.immediate_returns.append(immediate_return)
        
        # Update learning
        self._update_decision_quality(decision, immediate_return)
        
        return immediate_return
    
    def _create_context(self, context_dict: Dict[str, Any]) -> DecisionContext:
        """Create decision context from dictionary"""
        context_hash = self._hash_context(context_dict)
        
        return DecisionContext(
            context_hash=context_hash,
            parameters=context_dict,
            environmental_factors=self._extract_environmental_factors(context_dict),
            temporal_factors={
                'timestamp': time.time(),
                'hour_of_day': time.localtime().tm_hour,
                'day_of_week': time.localtime().tm_wday
            }
        )
    
    def _hash_context(self, context: Dict[str, Any]) -> str:
        """Create deterministic hash for context"""
        import hashlib
        return hashlib.sha256(
            json.dumps(context, sort_keys=True).encode()
        ).hexdigest()
    
    def _extract_environmental_factors(self, context: Dict[str, Any]) -> Dict[str, float]:
        """Extract environmental factors from context"""
        factors = {}
        
        # Market volatility estimate
        if 'market' in context:
            factors['volatility'] = 0.3 if context.get('market') == 'volatile' else 0.1
            
        # Complexity factor
        factors['complexity'] = min(1.0, len(str(context)) / 1000)
        
        # Uncertainty factor
        factors['uncertainty'] = context.get('uncertainty', 0.5)
        
        return factors
    
    def _adjust_for_risk(self, confidence: float, risk_level: RiskLevel) -> float:
        """Adjust confidence based on risk level"""
        risk_factor = self._risk_level_to_factor(risk_level)
        return confidence * (1 - (risk_factor * self.risk_tolerance))
    
    def _risk_level_to_factor(self, risk_level: RiskLevel) -> float:
        """Convert risk level to numerical factor"""
        risk_factors = {
            RiskLevel.LOW: 0.1,
            RiskLevel.MEDIUM: 0.3,
            RiskLevel.HIGH: 0.6,
            RiskLevel.CRITICAL: 0.9
        }
        return risk_factors.get(risk_level, 0.3)
    
    def _modify_risk_level(self, current_risk: RiskLevel, modifier: float) -> RiskLevel:
        """Modify risk level based on evidence"""
        risk_order = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
        current_index = risk_order.index(current_risk)
        
        # Apply modifier
        new_index = max(0, min(len(risk_order) - 1, 
                             round(current_index * modifier)))
        
        return risk_order[int(new_index)]
    
    def _combine_confidence(self, prior_confidence: float, 
                          evidence_confidence: float, 
                          evidence_strength: float) -> float:
        """Combine prior and evidence confidence"""
        # Weighted average based on evidence strength
        return (prior_confidence * (1 - evidence_strength) + 
                evidence_confidence * evidence_strength)
    
    def _update_prior_knowledge(self, context_hash: str, decision: DecisionRecord):
        """Update prior knowledge with new decision"""
        self.prior_knowledge[context_hash] = {
            'confidence': decision.confidence,
            'expected_return': decision.expected_return,
            'risk_level': decision.risk_level,
            'last_updated': time.time(),
            'success_rate': self._calculate_success_rate(context_hash)
        }
    
    def _update_decision_quality(self, decision: DecisionRecord, 
                               immediate_return: ImmediateReturn):
        """Update decision quality metrics"""
        context_hash = decision.context.context_hash
        
        if context_hash not in self.prior_knowledge:
            return
            
        # Calculate performance metric
        performance = immediate_return.risk_adjusted_return
        
        # Update confidence based on performance
        current_confidence = self.prior_knowledge[context_hash]['confidence']
        new_confidence = current_confidence * (1 - self.learning_rate) + performance * self.learning_rate
        
        self.prior_knowledge[context_hash]['confidence'] = new_confidence
        self.prior_knowledge[context_hash]['success_rate'] = self._calculate_success_rate(context_hash)
    
    def _calculate_success_rate(self, context_hash: str) -> float:
        """Calculate success rate for context"""
        relevant_returns = [
            ret for ret in self.immediate_returns 
            if any(dec.context.context_hash == context_hash 
                  for dec in self.decision_history 
                  if dec.decision_id == ret.decision_id)
        ]
        
        if not relevant_returns:
            return 0.5
            
        successful_returns = [ret for ret in relevant_returns if ret.return_ratio >= 1.0]
        return len(successful_returns) / len(relevant_returns)
    
    def get_decision_metrics(self) -> Dict[str, Any]:
        """Get overall decision engine metrics"""
        if not self.decision_history:
            return {}
            
        recent_decisions = list(self.decision_history)[-100:]  # Last 100 decisions
        recent_returns = list(self.immediate_returns)[-50:]   # Last 50 returns
        
        avg_confidence = np.mean([dec.confidence for dec in recent_decisions])
        avg_return_ratio = np.mean([ret.return_ratio for ret in recent_returns]) if recent_returns else 0
        success_rate = len([ret for ret in recent_returns if ret.return_ratio >= 1.0]) / len(recent_returns) if recent_returns else 0
        
        return {
            'total_decisions': len(self.decision_history),
            'avg_confidence': avg_confidence,
            'avg_return_ratio': avg_return_ratio,
            'success_rate': success_rate,
            'prior_knowledge_size': len(self.prior_knowledge),
            'risk_tolerance': self.risk_tolerance
        }