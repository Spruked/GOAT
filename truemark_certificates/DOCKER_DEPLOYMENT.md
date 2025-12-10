# TrueMark Certificate Forge - Docker Deployment Guide

## Quick Start

### Build and Run with Docker Compose

```bash
cd truemark_certificates
docker-compose up -d
```

### Mint Certificate in Container

```bash
docker exec truemark-certificate-forge python certificate_forge.py \
  --owner "Bryan A. Spruk" \
  --wallet "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1" \
  --title "Caleon Prime Knowledge Base" \
  --category Knowledge \
  --chain Polygon
```

### View SKG Metrics

```bash
docker exec truemark-certificate-forge python certificate_forge.py --skg
```

### Query Owner Portfolio

```bash
docker exec truemark-certificate-forge python certificate_forge.py \
  --portfolio "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1"
```

## Docker Commands

### Build Image

```bash
docker build -t truemark/certificate-forge:v2.0 .
```

### Run Container

```bash
docker run -d \
  --name truemark-forge \
  -v $(pwd)/vault:/app/vault \
  -v $(pwd)/keys:/app/keys \
  -v $(pwd)/truemark_logo.png:/app/truemark_logo.png:ro \
  -v $(pwd)/goldsealtruemark1600.png:/app/goldsealtruemark1600.png:ro \
  -v $(pwd)/watermark_truemark.png:/app/watermark_truemark.png:ro \
  truemark/certificate-forge:v2.0 \
  tail -f /dev/null
```

### Access Container Shell

```bash
docker exec -it truemark-certificate-forge bash
```

### View Logs

```bash
docker logs truemark-certificate-forge
```

### Stop Container

```bash
docker-compose down
```

## Volume Mounts

- **`./vault`**: Persistent certificate storage (JSONL + PDFs)
- **`./keys`**: Cryptographic signing keys (HMAC-SHA256)
- **`./truemark_logo.png`**: Company logo (read-only)
- **`./goldsealtruemark1600.png`**: Gold seal image (read-only)
- **`./watermark_truemark.png`**: Watermark overlay (read-only)

## Environment Variables

- **`VAULT_PATH=/app/vault`**: Base path for vault storage
- **`PYTHONUNBUFFERED=1`**: Real-time log output

## Vault Structure (Persisted)

```
vault/
├── certificates/
│   └── issued/
│       ├── DALSKM20251210-983E0E2E_OFFICIAL.pdf
│       └── DALSAM20251210-592E09BB_OFFICIAL.pdf
├── events/
│   └── vault_events.jsonl
└── skg/
    ├── nodes.jsonl
    ├── edges.jsonl
    └── transactions.jsonl
```

## Health Check

Container includes health check every 30 seconds:

```bash
docker inspect truemark-certificate-forge | grep Health -A 10
```

## Production Deployment

### Docker Swarm

```bash
docker stack deploy -c docker-compose.yml truemark-stack
```

### Kubernetes (Coming Soon)

Create deployment manifests:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: truemark-forge
spec:
  replicas: 3
  selector:
    matchLabels:
      app: truemark-forge
  template:
    metadata:
      labels:
        app: truemark-forge
    spec:
      containers:
      - name: forge
        image: truemark/certificate-forge:v2.0
        volumeMounts:
        - name: vault
          mountPath: /app/vault
        - name: keys
          mountPath: /app/keys
      volumes:
      - name: vault
        persistentVolumeClaim:
          claimName: truemark-vault-pvc
      - name: keys
        secret:
          secretName: truemark-keys
```

## Registry Push

```bash
# Tag for registry
docker tag truemark/certificate-forge:v2.0 \
  registry.truemark.io/certificate-forge:v2.0

# Push to private registry
docker push registry.truemark.io/certificate-forge:v2.0
```

## Security Notes

- **Keys directory**: Mount as volume, never commit to Git
- **Vault data**: Contains sensitive certificate data, secure with encryption at rest
- **Container runs as root**: Consider adding USER directive for production
- **Network isolation**: Use bridge network, no exposed ports by default

## Troubleshooting

### Container Won't Start

```bash
docker logs truemark-certificate-forge
```

### Missing Assets

Ensure logo, seal, and watermark files exist:

```bash
ls -lh truemark_logo.png goldsealtruemark1600.png watermark_truemark.png
```

### Permission Issues

```bash
docker exec truemark-certificate-forge ls -la /app/vault
```

### Rebuild After Code Changes

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Performance

- **Image Size**: ~250MB (Python 3.11-slim + dependencies)
- **Startup Time**: <5 seconds
- **Certificate Generation**: 2-3 seconds per certificate
- **SKG Warm-Start**: <1 second (loads from vault)

## License

Same as parent TrueMark Certificate Forge system.
