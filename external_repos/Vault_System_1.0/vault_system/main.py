#!/usr/bin/env python3
"""
Integrated Vault System - Main Entry Point
"""

import time
import json
from typing import Dict, Any

from vault_core import CryptographicVault, VaultCategory
from glyph_trace import GlyphGenerator, GlyphType
from associative_memory import EnhancedMemoryMatrix
from apriori_posterior import RecursiveApriori, BayesianEngine
from decision_apriori import EnhancedDecisionEngine, DecisionType, RiskLevel
from vault_gate_filter import VaultGatekeeper, GateAction
from telemetry_stream import TelemetryManager, TelemetryEventType
from ISS_bridge import ISSConnector, ISSMessageType
from module_blueprints import BlueprintManager, BlueprintStatus

class IntegratedVaultSystem:
    def __init__(self, master_key: str, node_id: str = "vault_main"):
        # Initialize all components
        self.telemetry = TelemetryManager()
        self.vault = CryptographicVault(master_key)
        self.glyph_generator = GlyphGenerator()
        self.memory_matrix = EnhancedMemoryMatrix()
        self.apriori_engine = RecursiveApriori()
        self.bayesian_engine = BayesianEngine()
        self.decision_engine = EnhancedDecisionEngine()
        self.gatekeeper = VaultGatekeeper()
        self.iss_connector = ISSConnector(node_id, "secret_key_2024")
        self.blueprint_manager = BlueprintManager()
        
        # Register blueprints
        self._register_component_blueprints()
        
        # Set up ISS message handlers
        self._setup_iss_handlers()
        
        # Record system startup
        self.telemetry.record_event(
            TelemetryEventType.SYSTEM_HEALTH,
            "IntegratedVaultSystem",
            "initialization",
            0.0,
            True,
            {'components_initialized': 8}
        )
    
    def _register_component_blueprints(self):
        """Register blueprints for all system components"""
        
        # Vault Core Blueprint
        self.blueprint_manager.register_blueprint(
            module_name="cryptographic_vault",
            version="2.0.0",
            dependencies=["python-cryptography"],
            interfaces={
                'store': {'parameters': ['vault_id', 'category', 'data', 'source']},
                'retrieve': {'parameters': ['vault_id', 'category']},
                'encrypt_data': {'parameters': ['data']},
                'decrypt_data': {'parameters': ['encrypted_data']}
            },
            configuration={
                'encryption_algorithm': 'AES-256',
                'key_derivation_iterations': 100000,
                'default_retention_days': 30
            },
            status=BlueprintStatus.ACTIVE
        )
        
        # Glyph System Blueprint
        self.blueprint_manager.register_blueprint(
            module_name="glyph_generator", 
            version="1.5.0",
            dependencies=[],
            interfaces={
                'generate_data_glyph': {'parameters': ['data', 'vault_id', 'metadata']},
                'generate_access_glyph': {'parameters': ['vault_id', 'operation']},
                'verify_glyph_integrity': {'parameters': ['glyph']}
            },
            configuration={
                'hash_algorithm': 'SHA3-256',
                'pattern_complexity': 'medium',
                'entropy_calculation': 'shannon'
            },
            status=BlueprintStatus.ACTIVE
        )
        
        # Add more blueprints for other components...
    
    def _setup_iss_handlers(self):
        """Set up ISS message handlers"""
        
        def handle_data_input(message):
            """Handle data input from ISS network"""
            payload = message.payload
            data = payload['data']
            source = payload['source']
            metadata = payload['metadata']
            
            # Process through gatekeeper
            gate_decision = self.gatekeeper.evaluate_input(data, source, metadata)
            
            if gate_decision.action == GateAction.ALLOW:
                # Store in appropriate vault
                category = VaultCategory(metadata.get('category', 'OPERATIONAL'))
                vault_id = metadata.get('vault_id', f"iss_{int(time.time())}")
                
                success = self.vault.store(vault_id, category, data, source, metadata)
                
                # Record telemetry
                self.telemetry.record_event(
                    TelemetryEventType.DATA_INPUT,
                    "ISS_Handler",
                    "store_data",
                    0.0,
                    success,
                    {'vault_id': vault_id, 'category': category.value}
                )
        
        def handle_query_request(message):
            """Handle query requests from ISS network"""
            payload = message.payload
            query = payload['query']
            requester = payload['requester']
            
            # Process query (simplified)
            results = self._process_query(query)
            
            # Send response back
            self.iss_connector.send_message(
                requester,
                ISSMessageType.STATUS_UPDATE,
                {'query_results': results, 'original_query': query}
            )
        
        # Register handlers
        self.iss_connector.register_handler(ISSMessageType.DATA_INPUT, handle_data_input)
        self.iss_connector.register_handler(ISSMessageType.QUERY_REQUEST, handle_query_request)
    
    def store_data(self, data: Any, category: VaultCategory, source: str, 
                  metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Store data through the complete system pipeline"""
        start_time = time.time()
        
        try:
            # Step 1: Gatekeeper evaluation
            gate_decision = self.gatekeeper.evaluate_input(data, source, metadata or {})
            
            if gate_decision.action != GateAction.ALLOW:
                return {
                    'success': False,
                    'reason': f"Gatekeeper rejected: {gate_decision.action.value}",
                    'reasoning': gate_decision.reasoning
                }
            
            # Step 2: Generate vault ID and glyph
            vault_id = f"{category.value}_{int(time.time())}_{hash(source) % 10000:04d}"
            glyph = self.glyph_generator.generate_data_glyph(str(data), vault_id, metadata)
            
            # Step 3: Store in vault
            success = self.vault.store(vault_id, category, data, source, metadata)
            
            if success:
                # Step 4: Update memory matrix
                pattern = [glyph.complexity, glyph.entropy, len(str(data))]
                associations = [vault_id, category.value, source, f"glyph_{glyph.pattern}"]
                self.memory_matrix.store_pattern(pattern, associations, metadata)
                
                # Step 5: Update apriori engine
                transaction = [
                    f"category:{category.value}", 
                    f"source:{source}",
                    f"operation:store"
                ]
                if metadata:
                    for key, value in metadata.items():
                        if isinstance(value, (str, int, float)):
                            transaction.append(f"meta_{key}:{value}")
                
                self.apriori_engine.add_transaction(transaction, metadata)
            
            duration = time.time() - start_time
            
            # Record telemetry
            self.telemetry.record_event(
                TelemetryEventType.VAULT_ACCESS,
                "IntegratedVaultSystem",
                "store_data",
                duration,
                success,
                {
                    'vault_id': vault_id,
                    'category': category.value,
                    'data_size': len(str(data)),
                    'glyph_pattern': glyph.pattern
                }
            )
            
            return {
                'success': success,
                'vault_id': vault_id,
                'glyph_pattern': glyph.pattern,
                'gate_confidence': gate_decision.confidence,
                'duration': duration
            }
            
        except Exception as e:
            duration = time.time() - start_time
            self.telemetry.record_event(
                TelemetryEventType.VAULT_ACCESS,
                "IntegratedVaultSystem", 
                "store_data",
                duration,
                False,
                {'error': str(e)}
            )
            return {'success': False, 'error': str(e)}
    
    def retrieve_data(self, vault_id: str, category: VaultCategory) -> Dict[str, Any]:
        """Retrieve data through the complete system"""
        start_time = time.time()
        
        try:
            # Step 1: Retrieve from vault
            data = self.vault.retrieve(vault_id, category)
            
            if data is None:
                return {'success': False, 'reason': 'Data not found'}
            
            # Step 2: Generate access glyph
            access_glyph = self.glyph_generator.generate_access_glyph(vault_id, "retrieve")
            
            # Step 3: Update memory associations
            recall_pattern = [len(str(data)), hash(vault_id) % 100, time.time() % 100]
            associations = self.memory_matrix.recall_pattern(recall_pattern)
            
            duration = time.time() - start_time
            
            # Record telemetry
            self.telemetry.record_event(
                TelemetryEventType.VAULT_ACCESS,
                "IntegratedVaultSystem",
                "retrieve_data", 
                duration,
                True,
                {
                    'vault_id': vault_id,
                    'category': category.value,
                    'data_size': len(str(data)),
                    'access_glyph': access_glyph.pattern
                }
            )
            
            return {
                'success': True,
                'data': data,
                'access_glyph': access_glyph.pattern,
                'associations': associations,
                'duration': duration
            }
            
        except Exception as e:
            duration = time.time() - start_time
            self.telemetry.record_event(
                TelemetryEventType.VAULT_ACCESS,
                "IntegratedVaultSystem",
                "retrieve_data",
                duration,
                False,
                {'error': str(e)}
            )
            return {'success': False, 'error': str(e)}
    
    def make_decision(self, context: Dict[str, Any], evidence: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make decision using the complete decision pipeline"""
        start_time = time.time()
        
        try:
            # Use decision engine
            if evidence:
                decision = self.decision_engine.extract_posteriori_decision(context, evidence)
            else:
                decision = self.decision_engine.extract_prior_decision(context)
            
            duration = time.time() - start_time
            
            # Record telemetry
            self.telemetry.record_event(
                TelemetryEventType.DECISION_ENGINE,
                "IntegratedVaultSystem",
                "make_decision",
                duration,
                True,
                {
                    'decision_type': decision.decision_type.value,
                    'confidence': decision.confidence,
                    'risk_level': decision.risk_level.value
                }
            )
            
            return {
                'success': True,
                'decision': decision,
                'duration': duration
            }
            
        except Exception as e:
            duration = time.time() - start_time
            self.telemetry.record_event(
                TelemetryEventType.DECISION_ENGINE,
                "IntegratedVaultSystem",
                "make_decision", 
                duration,
                False,
                {'error': str(e)}
            )
            return {'success': False, 'error': str(e)}
    
    def _process_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Process system query"""
        query_type = query.get('type', 'status')
        
        if query_type == 'system_status':
            return self.get_system_status()
        elif query_type == 'vault_stats':
            return self.vault.get_vault_stats()
        elif query_type == 'telemetry_summary':
            return self.telemetry.get_system_health()
        elif query_type == 'decision_metrics':
            return self.decision_engine.get_decision_metrics()
        else:
            return {'error': f'Unknown query type: {query_type}'}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        return {
            'vault_system': {
                'vault_stats': self.vault.get_vault_stats(),
                'total_components': len(self.blueprint_manager.blueprints)
            },
            'performance': {
                'telemetry_health': self.telemetry.get_system_health(),
                'decision_metrics': self.decision_engine.get_decision_metrics(),
                'gate_statistics': self.gatekeeper.get_gate_statistics()
            },
            'iss_network': self.iss_connector.get_node_status(),
            'timestamp': time.time()
        }
    
    def connect_to_node(self, node_info: Dict[str, Any]) -> bool:
        """Connect to ISS node"""
        return self.iss_connector.connect_node(node_info)
    
    def send_data_to_node(self, node_id: str, data: Any, metadata: Dict[str, Any]):
        """Send data to ISS node"""
        self.iss_connector.send_message(
            node_id,
            ISSMessageType.DATA_INPUT,
            {
                'data': data,
                'metadata': metadata,
                'source': self.iss_connector.node_id
            }
        )

def main():
    """Main demonstration function"""
    print("=== Integrated Vault System Demo ===")
    
    # Initialize system
    vault_system = IntegratedVaultSystem("master_password_2024", "demo_node_1")
    
    # Connect to demo node
    vault_system.connect_to_node({'node_id': 'demo_node_2'})
    
    # Store some data
    print("\n1. Storing Data...")
    result = vault_system.store_data(
        data={"amount": 5000, "currency": "USD", "type": "investment"},
        category=VaultCategory.FINANCIAL,
        source="demo_app",
        metadata={"risk": "medium", "strategy": "growth"}
    )
    print(f"Storage result: {result}")
    
    # Make a decision
    print("\n2. Making Decision...")
    context = {"market": "bullish", "timeframe": "short", "asset": "tech"}
    evidence = {"confidence_boost": 0.8, "return_adjustment": 1000}
    
    decision_result = vault_system.make_decision(context, evidence)
    print(f"Decision: {decision_result}")
    
    # Get system status
    print("\n3. System Status...")
    status = vault_system.get_system_status()
    print(f"System components: {status['vault_system']['total_components']}")
    print(f"Overall health: {status['performance']['telemetry_health']['overall_health']:.2%}")
    
    # Demonstrate ISS communication
    print("\n4. ISS Communication...")
    vault_system.send_data_to_node(
        "demo_node_2",
        {"message": "Hello from demo node!"},
        {"category": "test", "priority": "low"}
    )
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    main()