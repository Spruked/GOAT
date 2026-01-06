from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict, deque
import time
import numpy as np
from itertools import combinations

class RecursiveApriori:
    def __init__(self, min_support: float = 0.1, min_confidence: float = 0.7, 
                 max_recursion_depth: int = 5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.max_recursion_depth = max_recursion_depth
        
        self.frequent_itemsets = defaultdict(list)
        self.association_rules = []
        self.transaction_history = deque(maxlen=5000)
        self.item_frequency = defaultdict(int)
        self.recursion_stack = []
        
    def add_transaction(self, transaction: List[str], context: Dict[str, Any] = None):
        """Add transaction with context for recursive mining"""
        self.transaction_history.append({
            'items': transaction,
            'timestamp': time.time(),
            'context': context or {}
        })
        
        # Update item frequencies
        for item in set(transaction):
            self.item_frequency[item] += 1
            
        # Trigger recursive mining
        self._recursive_mine(transaction, context or {}, depth=0)
        
    def _recursive_mine(self, transaction: List[str], context: Dict[str, Any], depth: int):
        """Recursively mine patterns at different abstraction levels"""
        if depth >= self.max_recursion_depth:
            return
            
        # Mine at current level
        self._mine_frequent_itemsets(transaction, depth)
        self._generate_association_rules(depth)
        
        # Create abstracted transaction for next level
        abstracted_transaction = self._abstract_transaction(transaction, context)
        if abstracted_transaction and len(abstracted_transaction) >= 2:
            self._recursive_mine(abstracted_transaction, context, depth + 1)
            
        self.recursion_stack.append({
            'depth': depth,
            'transaction_size': len(transaction),
            'abstracted_size': len(abstracted_transaction) if abstracted_transaction else 0,
            'timestamp': time.time()
        })
    
    def _abstract_transaction(self, transaction: List[str], context: Dict[str, Any]) -> List[str]:
        """Create abstracted version of transaction"""
        abstracted = set()
        
        for item in transaction:
            # Abstract by category/type
            if ':' in item:
                prefix = item.split(':')[0]
                abstracted.add(f"category:{prefix}")
            elif len(item) > 10:
                # Abstract long items
                abstracted.add(f"type:long_item")
            else:
                abstracted.add(f"type:standard")
                
        # Add context-based abstractions
        for key, value in context.items():
            if isinstance(value, (int, float)):
                abstracted.add(f"ctx_{key}:numeric")
            else:
                abstracted.add(f"ctx_{key}:{type(value).__name__}")
                
        return list(abstracted)
    
    def _mine_frequent_itemsets(self, transaction: List[str], depth: int):
        """Mine frequent itemsets using Apriori algorithm"""
        items = set(transaction)
        k = 1
        
        while True:
            if k == 1:
                # Frequent 1-itemsets
                frequent_k = []
                for item in items:
                    support = self._calculate_support([item])
                    if support >= self.min_support:
                        frequent_k.append([item])
            else:
                # Generate candidate k-itemsets from frequent (k-1)-itemsets
                candidates = self._generate_candidates(self.frequent_itemsets[k-1])
                frequent_k = []
                
                for candidate in candidates:
                    support = self._calculate_support(candidate)
                    if support >= self.min_support:
                        frequent_k.append(candidate)
            
            if not frequent_k:
                break
                
            self.frequent_itemsets[k].extend(frequent_k)
            k += 1
    
    def _generate_candidates(self, frequent_itemsets: List[List[str]]) -> List[List[str]]:
        """Generate candidate itemsets"""
        candidates = []
        n = len(frequent_itemsets)
        
        for i in range(n):
            for j in range(i + 1, n):
                itemset1 = frequent_itemsets[i]
                itemset2 = frequent_itemsets[j]
                
                # Join if first k-1 items are equal
                if itemset1[:-1] == itemset2[:-1] and itemset1[-1] < itemset2[-1]:
                    candidate = itemset1 + [itemset2[-1]]
                    candidates.append(candidate)
                    
        return candidates
    
    def _generate_association_rules(self, depth: int):
        """Generate association rules from frequent itemsets"""
        for k, itemsets in self.frequent_itemsets.items():
            if k < 2:
                continue
                
            for itemset in itemsets:
                support_itemset = self._calculate_support(itemset)
                
                # Generate all possible rules
                for i in range(1, len(itemset)):
                    for antecedent in self._get_subsets(itemset, i):
                        consequent = [item for item in itemset if item not in antecedent]
                        
                        if not consequent:
                            continue
                            
                        support_antecedent = self._calculate_support(antecedent)
                        confidence = support_itemset / support_antecedent if support_antecedent > 0 else 0
                        
                        if confidence >= self.min_confidence:
                            rule = {
                                'antecedent': antecedent,
                                'consequent': consequent,
                                'confidence': confidence,
                                'support': support_itemset,
                                'depth': depth,
                                'lift': self._calculate_lift(antecedent, consequent, support_itemset),
                                'timestamp': time.time()
                            }
                            self.association_rules.append(rule)
    
    def _get_subsets(self, itemset: List[str], size: int) -> List[List[str]]:
        """Get all subsets of given size"""
        return [list(comb) for comb in combinations(itemset, size)]
    
    def _calculate_support(self, itemset: List[str]) -> float:
        """Calculate support for itemset"""
        if not self.transaction_history:
            return 0.0
            
        count = 0
        for transaction_data in self.transaction_history:
            if all(item in transaction_data['items'] for item in itemset):
                count += 1
                
        return count / len(self.transaction_history)
    
    def _calculate_confidence(self, antecedent: List[str], consequent: List[str]) -> float:
        """Calculate confidence for rule"""
        support_antecedent = self._calculate_support(antecedent)
        support_both = self._calculate_support(antecedent + consequent)
        
        return support_both / support_antecedent if support_antecedent > 0 else 0
    
    def _calculate_lift(self, antecedent: List[str], consequent: List[str], support_both: float) -> float:
        """Calculate lift metric for rule interestingness"""
        support_antecedent = self._calculate_support(antecedent)
        support_consequent = self._calculate_support(consequent)
        
        expected_support = support_antecedent * support_consequent
        return support_both / expected_support if expected_support > 0 else 1.0
    
    def get_top_rules(self, n: int = 10, min_confidence: float = None) -> List[Dict[str, Any]]:
        """Get top N association rules by confidence"""
        min_conf = min_confidence or self.min_confidence
        filtered_rules = [rule for rule in self.association_rules if rule['confidence'] >= min_conf]
        sorted_rules = sorted(filtered_rules, key=lambda x: x['confidence'], reverse=True)
        return sorted_rules[:n]
    
    def predict_consequent(self, antecedent: List[str]) -> List[Dict[str, Any]]:
        """Predict possible consequents for given antecedent"""
        predictions = []
        
        for rule in self.association_rules:
            if set(rule['antecedent']).issubset(set(antecedent)):
                predictions.append({
                    'consequent': rule['consequent'],
                    'confidence': rule['confidence'],
                    'support': rule['support'],
                    'lift': rule['lift']
                })
        
        return sorted(predictions, key=lambda x: x['confidence'], reverse=True)
    
    def get_mining_stats(self) -> Dict[str, Any]:
        """Get mining statistics"""
        total_rules = len(self.association_rules)
        avg_confidence = np.mean([rule['confidence'] for rule in self.association_rules]) if total_rules > 0 else 0
        avg_support = np.mean([rule['support'] for rule in self.association_rules]) if total_rules > 0 else 0
        
        return {
            'total_transactions': len(self.transaction_history),
            'total_rules': total_rules,
            'avg_confidence': avg_confidence,
            'avg_support': avg_support,
            'recursion_depth': len(self.recursion_stack),
            'unique_items': len(self.item_frequency)
        }