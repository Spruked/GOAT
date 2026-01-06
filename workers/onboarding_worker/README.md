# Onboarding Worker - GOAT Initial User Journey

## Purpose
The onboarding worker guides new users through their first experience with GOAT, helping them understand the platform, upload content, configure settings, and start their first project. It implements a structured 6-step conversational flow that adapts to user questions while maintaining learning boundaries.

## Boundaries
- **Restricted Learning Mode**: Cannot self-modify scripts or logic
- **UCM Dependency**: All improvements must be approved by CALI/UCM system
- **Scoped Knowledge**: Only handles onboarding-related questions
- **Transfer Threshold**: Auto-transfers unanswered queries after 3 accumulated questions

## Implementation Notes

### Key Requirements from Specs:
**Temp Vault Transfer**: When unanswered_queries.json reaches threshold (default 3 entries), worker auto-transfers to UCM/CALI via ucm_connector.submit_for_review()

**UCM Integration**: The UCMConnector class provides the interface. In production, this should:
- Send encrypted payload to UCM_4_Core/CALI/
- Write to immutable matrix at UCM_4_Core/CALI/cali_immutable_matrix/
- Trigger ECM convergence for review

**Improvement Loop**: When UCM approves improvements, call worker.apply_improvement(improvement_data) which:
- Updates onboarding_script.json with new/modified sections
- Updates logic.json with new parameters
- Reindexes mini-SKG automatically
- Version numbers increment automatically

**Restricted Learning**: Workers CANNOT self-modify. They:
- Only save unanswered questions to temp vault
- Never update their own scripts directly
- Wait for UCM approval (per memory #18)

**Mini-SKG Integration**: The mini-SKG is embedded within each worker folder and reindexes automatically when scripts update, maintaining local job-specific knowledge.

## Setup Instructions

```bash
# 1. Create directory structure
mkdir -p GOAT/workers/_templates
mkdir -p GOAT/workers/onboarding_worker/{mini_skg,temp_vault}

# 2. Copy template files
cp worker_skg_template.py GOAT/workers/_templates/
cp onboarding_worker.py GOAT/workers/onboarding_worker/worker_body.py

# 3. Create JSON files
# - onboarding_script.json (provided above)
# - logic.json (provided above)
# - unanswered_queries.json (empty array)

# 4. Initialize mini-SKG
touch GOAT/workers/onboarding_worker/mini_skg/knowledge_graph.json
echo '{"nodes": [], "edges": []}' > GOAT/workers/onboarding_worker/mini_skg/knowledge_graph.json
touch GOAT/workers/onboarding_worker/mini_skg/embeddings.db
```

## Integration with DALS Worker Forge

When your DALS system forges new workers, each must:
- Inherit from WorkerSKG base class
- Implement _generate_response() method for job-specific logic
- Create [job_name]_script.json with step-by-step instructions
- Follow identical directory structure
- Use same logic.json schema
- Connect to same UCM/CALI endpoint

This ensures zero glitches between manually created and DALS-forged workers.

## File Structure
```
onboarding_worker/
├── logic.json              # Worker configuration and learning rules
├── onboarding_script.json  # 6-step conversational flow
├── worker_body.py          # OnboardingWorker class implementation
├── README.md               # This documentation
├── mini_skg/
│   ├── knowledge_graph.json # Local knowledge relationships
│   └── embeddings.db        # Vector embeddings storage
└── temp_vault/
    ├── unanswered_queries.json  # Questions for UCM review
    ├── behavior.json            # User interaction patterns
    └── metrics.json             # Performance and completion data
```

## Worker Capabilities
- **Conversational Onboarding**: Guides users through 6 structured steps
- **Question Matching**: Fuzzy logic to match user questions with expected queries
- **Navigation Commands**: "next", "back", "restart", "go to step X"
- **Fallback Handling**: Unanswered questions saved for UCM improvement
- **Progress Tracking**: Maintains user step position and completion status
- **Version Control**: Automatic script and logic versioning on improvements

## Future Worker Examples
Would you like me to create additional worker examples (e.g., for voice profile creation, content uploading, or blockchain minting workflows)?