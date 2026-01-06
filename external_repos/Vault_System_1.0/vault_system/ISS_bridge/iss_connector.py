from typing import Dict, List, Any, Optional
import time
import json
import hashlib
from dataclasses import dataclass
from enum import Enum

class ISSMessageType(Enum):
    DATA_INPUT = "data_input"
    QUERY_REQUEST = "query_request"
    SYSTEM_COMMAND = "system_command"
    STATUS_UPDATE = "status_update"
    ALERT_NOTIFICATION = "alert_notification"

@dataclass
class ISSMessage:
    message_id: str
    message_type: ISSMessageType
    timestamp: float
    source: str
    destination: str
    payload: Dict[str, Any]
    priority: int
    signature: Optional[str] = None

class ISSConnector:
    def __init__(self, node_id: str, secret_key: str):
        self.node_id = node_id
        self.secret_key = secret_key
        self.connected_nodes = set()
        self.message_queue = []
        self.handlers = {}
        self.message_history = []
        
    def connect_node(self, node_info: Dict[str, Any]) -> bool:
        """Connect to another ISS node"""
        node_id = node_info.get('node_id')
        if not node_id:
            return False
            
        self.connected_nodes.add(node_id)
        print(f"Connected to node: {node_id}")
        return True
    
    def disconnect_node(self, node_id: str) -> bool:
        """Disconnect from ISS node"""
        if node_id in self.connected_nodes:
            self.connected_nodes.remove(node_id)
            print(f"Disconnected from node: {node_id}")
            return True
        return False
    
    def send_message(self, destination: str, message_type: ISSMessageType,
                   payload: Dict[str, Any], priority: int = 1) -> str:
        """Send message to ISS node"""
        message_id = f"msg_{int(time.time())}_{hashlib.md5(str(payload).encode()).hexdigest()[:8]}"
        
        message = ISSMessage(
            message_id=message_id,
            message_type=message_type,
            timestamp=time.time(),
            source=self.node_id,
            destination=destination,
            payload=payload,
            priority=priority,
            signature=self._sign_message(payload)
        )
        
        if destination in self.connected_nodes:
            self.message_queue.append(message)
            print(f"Message queued for {destination}: {message_type.value}")
        else:
            print(f"Warning: Destination node {destination} not connected")
            
        self.message_history.append(message)
        return message_id
    
    def broadcast_message(self, message_type: ISSMessageType,
                        payload: Dict[str, Any], priority: int = 1) -> List[str]:
        """Broadcast message to all connected nodes"""
        message_ids = []
        for node_id in self.connected_nodes:
            message_id = self.send_message(node_id, message_type, payload, priority)
            message_ids.append(message_id)
            
        return message_ids
    
    def register_handler(self, message_type: ISSMessageType, handler_func):
        """Register handler for specific message type"""
        self.handlers[message_type] = handler_func
    
    def process_incoming_message(self, message: ISSMessage) -> bool:
        """Process incoming ISS message"""
        # Verify message signature
        if not self._verify_signature(message):
            print(f"Invalid signature for message: {message.message_id}")
            return False
            
        # Route to appropriate handler
        handler = self.handlers.get(message.message_type)
        if handler:
            try:
                handler(message)
                print(f"Processed message: {message.message_type.value}")
                return True
            except Exception as e:
                print(f"Error processing message: {e}")
                return False
        else:
            print(f"No handler for message type: {message.message_type.value}")
            return False
    
    def _sign_message(self, payload: Dict[str, Any]) -> str:
        """Create message signature"""
        payload_str = json.dumps(payload, sort_keys=True)
        signature_data = f"{payload_str}{self.secret_key}{int(time.time())}"
        return hashlib.sha256(signature_data.encode()).hexdigest()
    
    def _verify_signature(self, message: ISSMessage) -> bool:
        """Verify message signature"""
        if not message.signature:
            return False
            
        payload_str = json.dumps(message.payload, sort_keys=True)
        expected_signature = hashlib.sha256(
            f"{payload_str}{self.secret_key}{int(message.timestamp)}".encode()
        ).hexdigest()
        
        return message.signature == expected_signature
    
    def get_node_status(self) -> Dict[str, Any]:
        """Get current node status"""
        return {
            'node_id': self.node_id,
            'connected_nodes': list(self.connected_nodes),
            'queued_messages': len(self.message_queue),
            'total_messages_sent': len(self.message_history),
            'registered_handlers': len(self.handlers)
        }
    
    def process_data_input(self, data: Any, source: str, metadata: Dict[str, Any]):
        """Process data input from ISS network"""
        # This would integrate with the vault gatekeeper
        payload = {
            'data': data,
            'source': source,
            'metadata': metadata,
            'processing_node': self.node_id
        }
        
        # Broadcast to interested nodes
        self.broadcast_message(
            ISSMessageType.DATA_INPUT,
            payload,
            priority=2
        )
    
    def query_vault_system(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query vault system through ISS network"""
        message_id = self.broadcast_message(
            ISSMessageType.QUERY_REQUEST,
            {'query': query, 'requester': self.node_id},
            priority=3
        )
        
        # In a real implementation, this would wait for responses
        # For now, return empty list
        return []