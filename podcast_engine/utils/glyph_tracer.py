# audiobook_engine/utils/glyph_tracer.py
"""
Glyph Tracer for Audiobook Engine

Provides immutable lineage tracking using glyph-based commit system.
Ensures content integrity and tracks transformation history.
"""

import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

from .checksum import calculate_data_checksum, ChecksumAlgorithm

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class GlyphCommit:
    """A glyph-based commit with immutable lineage."""
    commit_id: str
    content_checksum: str
    metadata: Dict[str, Any]
    parent_commits: List[str]
    timestamp: datetime
    glyph_signature: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert commit to dictionary."""
        return {
            'commit_id': self.commit_id,
            'content_checksum': self.content_checksum,
            'metadata': self.metadata,
            'parent_commits': self.parent_commits,
            'timestamp': self.timestamp.isoformat(),
            'glyph_signature': self.glyph_signature
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GlyphCommit':
        """Create commit from dictionary."""
        return cls(
            commit_id=data['commit_id'],
            content_checksum=data['content_checksum'],
            metadata=data.get('metadata', {}),
            parent_commits=data.get('parent_commits', []),
            timestamp=datetime.fromisoformat(data['timestamp']),
            glyph_signature=data['glyph_signature']
        )


class GlyphTracer:
    """
    Immutable lineage tracking using glyph-based commits.

    Features:
    - Content integrity verification
    - Transformation history tracking
    - Merkle tree-like structure
    - Glyph-based unique identifiers
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize glyph tracer.

        Args:
            storage_path: Path to store commit data (optional)
        """
        self.storage_path = storage_path or Path("glyph_commits")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.commits: Dict[str, GlyphCommit] = {}

        # Load existing commits
        self._load_commits()

    def create_commit(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        parent_commits: Optional[List[str]] = None
    ) -> str:
        """
        Create a new glyph commit.

        Args:
            content: Content to commit
            metadata: Optional metadata
            parent_commits: List of parent commit IDs

        Returns:
            Generated commit ID
        """
        try:
            # Calculate content checksum
            content_checksum = calculate_data_checksum(content, ChecksumAlgorithm.SHA256)
            if content_checksum is None:
                raise ValueError("Failed to calculate content checksum")

            # Prepare commit data
            metadata = metadata or {}
            parent_commits = parent_commits or []

            # Create commit timestamp
            timestamp = datetime.now()

            # Generate glyph signature (combination of content and metadata)
            glyph_data = {
                'content_checksum': content_checksum,
                'metadata': metadata,
                'parent_commits': sorted(parent_commits),  # Sort for consistency
                'timestamp': timestamp.isoformat()
            }
            glyph_json = json.dumps(glyph_data, sort_keys=True)
            glyph_signature = calculate_data_checksum(glyph_json, ChecksumAlgorithm.BLAKE2B)

            # Generate commit ID from glyph signature
            commit_id = glyph_signature[:16]  # Use first 16 chars as ID

            # Create commit object
            commit = GlyphCommit(
                commit_id=commit_id,
                content_checksum=content_checksum,
                metadata=metadata,
                parent_commits=parent_commits,
                timestamp=timestamp,
                glyph_signature=glyph_signature
            )

            # Store commit
            self.commits[commit_id] = commit
            self._save_commit(commit)

            logger.info(f"Created glyph commit: {commit_id}")
            return commit_id

        except Exception as e:
            logger.error(f"Failed to create glyph commit: {e}")
            raise

    def get_commit(self, commit_id: str) -> Optional[GlyphCommit]:
        """
        Retrieve a commit by ID.

        Args:
            commit_id: Commit ID to retrieve

        Returns:
            GlyphCommit object, or None if not found
        """
        return self.commits.get(commit_id)

    def validate_lineage(self, commit_id: str) -> bool:
        """
        Validate the integrity of a commit's lineage.

        Args:
            commit_id: Commit ID to validate

        Returns:
            True if lineage is valid, False otherwise
        """
        try:
            commit = self.get_commit(commit_id)
            if not commit:
                logger.warning(f"Commit not found: {commit_id}")
                return False

            # Validate glyph signature
            glyph_data = {
                'content_checksum': commit.content_checksum,
                'metadata': commit.metadata,
                'parent_commits': sorted(commit.parent_commits),
                'timestamp': commit.timestamp.isoformat()
            }
            glyph_json = json.dumps(glyph_data, sort_keys=True)
            expected_signature = calculate_data_checksum(glyph_json, ChecksumAlgorithm.BLAKE2B)

            if expected_signature != commit.glyph_signature:
                logger.error(f"Invalid glyph signature for commit: {commit_id}")
                return False

            # Validate parent commits exist
            for parent_id in commit.parent_commits:
                if not self.get_commit(parent_id):
                    logger.error(f"Parent commit not found: {parent_id}")
                    return False

            # Recursively validate parent lineage
            for parent_id in commit.parent_commits:
                if not self.validate_lineage(parent_id):
                    return False

            return True

        except Exception as e:
            logger.error(f"Lineage validation failed for {commit_id}: {e}")
            return False

    def get_lineage_history(self, commit_id: str) -> List[GlyphCommit]:
        """
        Get the complete lineage history for a commit.

        Args:
            commit_id: Starting commit ID

        Returns:
            List of commits in chronological order (oldest first)
        """
        try:
            history = []
            visited = set()

            def traverse(commit_id: str):
                if commit_id in visited:
                    return  # Avoid cycles
                visited.add(commit_id)

                commit = self.get_commit(commit_id)
                if not commit:
                    return

                # Add parents first (depth-first)
                for parent_id in commit.parent_commits:
                    traverse(parent_id)

                history.append(commit)

            traverse(commit_id)
            return history

        except Exception as e:
            logger.error(f"Failed to get lineage history for {commit_id}: {e}")
            return []

    def find_common_ancestor(self, commit_id1: str, commit_id2: str) -> Optional[str]:
        """
        Find the common ancestor of two commits.

        Args:
            commit_id1: First commit ID
            commit_id2: Second commit ID

        Returns:
            Common ancestor commit ID, or None if none found
        """
        try:
            # Get lineage histories
            history1 = {commit.commit_id: commit for commit in self.get_lineage_history(commit_id1)}
            history2 = {commit.commit_id: commit for commit in self.get_lineage_history(commit_id2)}

            # Find intersection
            common_commits = set(history1.keys()) & set(history2.keys())

            if not common_commits:
                return None

            # Return the most recent common ancestor
            # (the one with the latest timestamp among common commits)
            common_ancestors = [history1[cid] for cid in common_commits]
            common_ancestors.sort(key=lambda c: c.timestamp, reverse=True)
            return common_ancestors[0].commit_id

        except Exception as e:
            logger.error(f"Failed to find common ancestor: {e}")
            return None

    def _save_commit(self, commit: GlyphCommit) -> None:
        """Save commit to storage."""
        try:
            commit_file = self.storage_path / f"{commit.commit_id}.json"
            with open(commit_file, 'w', encoding='utf-8') as f:
                json.dump(commit.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save commit {commit.commit_id}: {e}")

    def _load_commits(self) -> None:
        """Load existing commits from storage."""
        try:
            if not self.storage_path.exists():
                return

            for commit_file in self.storage_path.glob("*.json"):
                try:
                    with open(commit_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    commit = GlyphCommit.from_dict(data)
                    self.commits[commit.commit_id] = commit
                except Exception as e:
                    logger.warning(f"Failed to load commit from {commit_file}: {e}")

            logger.info(f"Loaded {len(self.commits)} glyph commits")

        except Exception as e:
            logger.error(f"Failed to load commits: {e}")

    def get_commit_stats(self) -> Dict[str, Any]:
        """Get statistics about stored commits."""
        if not self.commits:
            return {'total_commits': 0}

        timestamps = [commit.timestamp for commit in self.commits.values()]

        return {
            'total_commits': len(self.commits),
            'oldest_commit': min(timestamps).isoformat(),
            'newest_commit': max(timestamps).isoformat(),
            'metadata_types': list(set(
                commit.metadata.get('type', 'unknown')
                for commit in self.commits.values()
            ))
        }


# Convenience functions
def create_glyph_commit(
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    parent_commits: Optional[List[str]] = None
) -> str:
    """Create a glyph commit using default tracer."""
    tracer = GlyphTracer()
    return tracer.create_commit(content, metadata, parent_commits)

def validate_glyph_lineage(commit_id: str) -> bool:
    """Validate lineage of a glyph commit."""
    tracer = GlyphTracer()
    return tracer.validate_lineage(commit_id)