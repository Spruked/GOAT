# Swarm Knowledge Graph (SKG) Integration

## System Overview

The **Swarm Knowledge Graph (SKG)** is a pattern learning and drift detection system integrated into the TrueMark Enterprise Certificate Forge v2.0. It automatically ingests certificate data, detects patterns, identifies duplicates, and monitors drift scores for anomaly detection.

## Architecture

### Core Components

1. **skg_node.py**: Data structures (SKGNode, SKGEdge, SKGNodeType)
2. **skg_pattern_learner.py**: Pattern clustering and duplicate detection
3. **skg_drift_analyzer.py**: Drift score calculation (temporal, signature, pattern)
4. **skg_serializer.py**: Vault-compatible JSONL serialization
5. **skg_engine.py**: Main orchestrator with graph queries
6. **skg_integration.py**: Bridge between certificate forge and SKG

## Node Types

- **CERTIFICATE**: Certificate entities with serial numbers, signatures, IPFS hashes
- **IDENTITY**: Owner wallets with behavioral fingerprints
- **CHAIN**: Blockchain contract addresses
- **PATTERN**: Learned patterns (future use)
- **DRIFT_EVENT**: Anomaly events (future use)

## Pattern Learning

The SKG system automatically learns patterns from certificate data:

### Pattern Types

1. **Wallet Behavior**: MD5 fingerprint of wallet addresses (detects same owner)
2. **IPFS Content**: First 16 characters of IPFS hash (detects duplicate content)
3. **Temporal Issuance**: Hourly buckets (YYYY-MM-DDTHH) (detects batch issuance)
4. **Chain Activity**: Blockchain network clustering (detects chain preference)

### Duplicate Detection

Certificates with matching IPFS prefixes are flagged as duplicates:
```
🧠 SKG: Drift=0.000, Duplicates=2
```

## Drift Analysis

Drift scores measure certificate anomalies (0.0 = perfect, >1.0 = anomalous):

### Drift Components

1. **Temporal Drift**: Deviates from baseline issuance interval (300 seconds)
2. **Signature Drift**: Invalid signature format or length
3. **Pattern Drift**: Missing/invalid IPFS hash format

### Drift Formula

```
combined_drift = mean([temporal_drift, signature_drift, pattern_drift])
```

## Vault Storage

SKG data is persisted in vault-compatible JSONL format:

```
vault/skg/nodes.jsonl          # All SKG nodes
vault/skg/edges.jsonl          # All SKG edges
vault/skg/transactions.jsonl   # Transaction log
```

### Node Example

```json
{
  "node_id": "cert_DALSKM20251210-983E0E2E",
  "node_type": "certificate",
  "properties": {
    "serial_number": "DALSKM20251210-983E0E2E",
    "owner_wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "asset_id": "Caleon Prime Knowledge Base",
    "ipfs_hash": "ipfs://Qm962ae8ad13884e889b4afb4c592f4ef6",
    "minted_at": "2025-12-10T23:14:27.069807Z"
  },
  "created_by": "truemark_forge",
  "created_at": "2025-12-10T23:14:27.123456Z",
  "version": 1,
  "is_active": true
}
```

### Edge Example

```json
{
  "edge_id": "edge_owns_cert_DALSKM20251210-983E0E2E",
  "source_id": "owner_5a3b844Bc9e7595f",
  "target_id": "cert_DALSKM20251210-983E0E2E",
  "edge_type": "OWNS",
  "properties": {
    "acquired_at": "2025-12-10T23:14:27.069807Z"
  },
  "created_at": "2025-12-10T23:14:27.234567Z",
  "confidence": 1.0
}
```

## Usage

### Certificate Minting (Automatic SKG Ingestion)

```bash
python certificate_forge.py \
  --owner "Bryan A. Spruk" \
  --wallet "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1" \
  --title "Caleon Prime Knowledge Base" \
  --category Knowledge \
  --chain Polygon
```

Output includes SKG enrichment:
```
🧠 SKG: Drift=0.000, Duplicates=0
```

### SKG Health Metrics

```bash
python certificate_forge.py --skg
```

Output:
```
🧠 SKG Health Metrics
============================================================
Total Nodes: 4
Certificate Nodes: 2
Identity Nodes: 1
Chain Nodes: 1
Total Edges: 4
Global Drift Average: 0.000

Pattern Clusters:
  total_clusters: 6
  wallet_behavior_clusters: 1
  ipfs_clusters: 2
  temporal_clusters: 1
```

### Owner Portfolio Query

```bash
python certificate_forge.py --portfolio "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1"
```

Output:
```
👤 Portfolio for 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1
============================================================
Total Certificates: 2

  🏷️  Serial: DALSKM20251210-983E0E2E
  📦 Asset: Caleon Prime Knowledge Base
  📅 Minted: 2025-12-10T23:14:27.069807Z
  🔗 IPFS: ipfs://Qm962ae8ad13884e889b4afb4c592f4ef6
```

## Integration Flow

1. **Certificate Minted** → `certificate_forge.py::mint_official_certificate()`
2. **Payload Signed** → `crypto_anchor.py::sign_payload()`
3. **PDF Rendered** → `forensic_renderer.py::create_forensic_pdf()`
4. **Vault Logged** → `integration_bridge.py::record_certificate_issuance()`
5. **SKG Ingested** → `skg_integration.py::on_certificate_minted()`
   - Creates certificate node
   - Creates/updates owner node
   - Creates/updates chain node
   - Creates OWNS edge (owner → certificate)
   - Creates ANCHORED_TO edge (certificate → chain)
   - Learns patterns
   - Calculates drift
   - Detects duplicates
6. **Swarm Broadcast** → `integration_bridge.py::broadcast_to_swarm()` (includes SKG payload)
7. **Return Verification** → Package includes `skg_enrichment` data

## API Reference

### CertificateSKGBridge

```python
from skg_core.skg_integration import CertificateSKGBridge

bridge = CertificateSKGBridge(vault_root=Path("./vault"))

# Hook called on certificate minting
enrichment = bridge.on_certificate_minted(cert_data)
# Returns: {skg_ingested, cert_node_id, drift_score, duplicate_count}

# Query certificates by wallet
portfolio = bridge.get_owner_portfolio("0x742d35...")
# Returns: {wallet, certificates[], total}

# Get SKG health metrics
metrics = bridge.get_skg_health_metrics()
# Returns: {total_nodes, certificate_nodes, pattern_clusters, global_drift_average}

# Check duplicate risk
risk = bridge.check_duplicate_risk(cert_data)
# Returns: {is_duplicate, duplicate_count, duplicate_certificates[]}
```

## Monitoring

### Dashboard Integration

SKG metrics are designed for dashboard integration:

```python
skg_metrics = forge.get_skg_metrics()

# Display node counts
print(f"Certificates: {skg_metrics['certificate_nodes']}")
print(f"Identities: {skg_metrics['identity_nodes']}")
print(f"Chains: {skg_metrics['chain_nodes']}")

# Display drift health
if skg_metrics['global_drift_average'] > 0.5:
    print("⚠️  HIGH DRIFT DETECTED")

# Display pattern clustering
clusters = skg_metrics['pattern_clusters']
print(f"Wallet Clusters: {clusters['wallet_behavior_clusters']}")
print(f"IPFS Clusters: {clusters['ipfs_clusters']}")
```

### Transaction Log

Monitor SKG operations:

```python
from skg_core.skg_serializer import SKGSerializer

serializer = SKGSerializer(Path("./vault"))
transactions = serializer.get_transaction_log(limit=100)

for txn in transactions:
    print(f"{txn['timestamp']}: {txn['event_type']} - {txn['payload']}")
```

## Future Enhancements

1. **Swarm Consensus**: Multi-node pattern agreement
2. **Drift Alerting**: Automatic anomaly notifications
3. **Pattern Visualization**: Graph rendering with NetworkX
4. **Machine Learning**: Advanced pattern detection with scikit-learn
5. **Query Language**: GraphQL-style SKG queries
6. **Time-Series Analysis**: Drift trend monitoring

## Technical Notes

- All timestamps use ISO 8601 format with 'Z' suffix (UTC)
- Node IDs use prefixes: `cert_`, `owner_`, `chain_`
- Edge IDs use format: `edge_{type}_{target_node_id}`
- JSONL format ensures immutable append-only logs
- Pattern clusters are rebuilt on warm-start from vault
- Drift baseline metrics are configurable in `SKGDriftAnalyzer`

## License

MIT License - See [LICENSE](LICENSE) file for details.

**Legal Notice**: SKG system is for business documentation and pattern analysis only. It is NOT a legal monitoring instrument or government surveillance system.

## Support

For issues, questions, or contributions:
- **GitHub Issues**: https://github.com/Spruked/GOAT/issues
- **Documentation**: See README.md and DOCKER_DEPLOYMENT.md
- **Email**: bryan@truemark.io
- **Discussions**: GitHub Discussions
