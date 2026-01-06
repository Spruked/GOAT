# audiobook_engine/utils/temp_manager.py
"""
Temporary File Manager for Audiobook Engine

Manages temporary files and cleanup for audio processing operations.
"""

import os
import tempfile
import logging
from typing import Optional, List, Set
from pathlib import Path
from contextlib import contextmanager

# Configure logging
logger = logging.getLogger(__name__)


class TempFileManager:
    """
    Manages temporary files for audiobook processing.

    Features:
    - Automatic cleanup of temporary files
    - Context manager support
    - File tracking and validation
    - Memory-efficient file handling
    """

    def __init__(self, base_dir: Optional[Path] = None, auto_cleanup: bool = True):
        """
        Initialize temp file manager.

        Args:
            base_dir: Base directory for temp files (default: system temp dir)
            auto_cleanup: Whether to cleanup files on deletion
        """
        self.base_dir = base_dir or Path(tempfile.gettempdir()) / "audiobook_engine"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.auto_cleanup = auto_cleanup
        self.managed_files: Set[Path] = set()

    def create_temp_file(
        self,
        suffix: str = "",
        prefix: str = "temp_",
        content: Optional[bytes] = None
    ) -> Path:
        """
        Create a temporary file and track it for cleanup.

        Args:
            suffix: File extension (e.g., '.wav')
            prefix: File prefix
            content: Optional initial content to write

        Returns:
            Path to created temporary file
        """
        try:
            # Create temporary file
            fd, temp_path = tempfile.mkstemp(
                suffix=suffix,
                prefix=prefix,
                dir=str(self.base_dir)
            )
            os.close(fd)  # Close the file descriptor

            temp_file_path = Path(temp_path)

            # Write content if provided
            if content is not None:
                temp_file_path.write_bytes(content)

            # Track the file
            self.managed_files.add(temp_file_path)

            logger.debug(f"Created temp file: {temp_file_path}")
            return temp_file_path

        except Exception as e:
            logger.error(f"Failed to create temp file: {e}")
            raise

    def create_temp_dir(self, prefix: str = "temp_dir_") -> Path:
        """
        Create a temporary directory and track it.

        Args:
            prefix: Directory prefix

        Returns:
            Path to created temporary directory
        """
        try:
            temp_dir = Path(tempfile.mkdtemp(prefix=prefix, dir=str(self.base_dir)))
            self.managed_files.add(temp_dir)
            logger.debug(f"Created temp dir: {temp_dir}")
            return temp_dir
        except Exception as e:
            logger.error(f"Failed to create temp dir: {e}")
            raise

    def register_file(self, file_path: Path) -> None:
        """
        Register an existing file for management.

        Args:
            file_path: Path to existing file to manage
        """
        if file_path.exists():
            self.managed_files.add(file_path)
            logger.debug(f"Registered file: {file_path}")

    def unregister_file(self, file_path: Path) -> None:
        """
        Unregister a file from management (won't be cleaned up).

        Args:
            file_path: Path to file to unregister
        """
        self.managed_files.discard(file_path)
        logger.debug(f"Unregistered file: {file_path}")

    def cleanup_file(self, file_path: Path) -> bool:
        """
        Manually cleanup a specific file.

        Args:
            file_path: Path to file to cleanup

        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            if file_path.exists():
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    import shutil
                    shutil.rmtree(file_path)
                logger.debug(f"Cleaned up: {file_path}")
            self.managed_files.discard(file_path)
            return True
        except Exception as e:
            logger.warning(f"Failed to cleanup {file_path}: {e}")
            return False

    def cleanup_all(self) -> int:
        """
        Cleanup all managed temporary files.

        Returns:
            Number of files cleaned up
        """
        cleaned_count = 0
        files_to_cleanup = list(self.managed_files)

        for file_path in files_to_cleanup:
            if self.cleanup_file(file_path):
                cleaned_count += 1

        logger.info(f"Cleaned up {cleaned_count} temporary files")
        return cleaned_count

    def get_managed_files(self) -> List[Path]:
        """Get list of currently managed files."""
        return list(self.managed_files)

    def get_stats(self) -> dict:
        """Get statistics about managed files."""
        total_size = 0
        file_count = 0
        dir_count = 0

        for file_path in self.managed_files:
            if file_path.exists():
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1
                elif file_path.is_dir():
                    dir_count += 1

        return {
            'managed_files': len(self.managed_files),
            'existing_files': file_count,
            'existing_dirs': dir_count,
            'total_size_bytes': total_size
        }

    def __del__(self):
        """Cleanup on object destruction if auto_cleanup enabled."""
        if self.auto_cleanup:
            self.cleanup_all()

    @contextmanager
    def temp_file_context(self, suffix: str = "", prefix: str = "temp_"):
        """
        Context manager for temporary file creation and automatic cleanup.

        Usage:
            with temp_manager.temp_file_context(suffix='.wav') as temp_file:
                # Use temp_file
                pass
            # File is automatically cleaned up
        """
        temp_file = None
        try:
            temp_file = self.create_temp_file(suffix=suffix, prefix=prefix)
            yield temp_file
        finally:
            if temp_file and self.auto_cleanup:
                self.cleanup_file(temp_file)

    @contextmanager
    def temp_dir_context(self, prefix: str = "temp_dir_"):
        """
        Context manager for temporary directory creation and automatic cleanup.
        """
        temp_dir = None
        try:
            temp_dir = self.create_temp_dir(prefix=prefix)
            yield temp_dir
        finally:
            if temp_dir and self.auto_cleanup:
                self.cleanup_file(temp_dir)


# Global instance for convenience
_default_temp_manager = None

def get_temp_manager() -> TempFileManager:
    """Get the default global temp file manager."""
    global _default_temp_manager
    if _default_temp_manager is None:
        _default_temp_manager = TempFileManager()
    return _default_temp_manager

# Convenience functions
def create_temp_file(suffix: str = "", prefix: str = "temp_", content: Optional[bytes] = None) -> Path:
    """Create a temporary file using the default manager."""
    return get_temp_manager().create_temp_file(suffix=suffix, prefix=prefix, content=content)

def cleanup_temp_files() -> int:
    """Cleanup all temporary files managed by the default manager."""
    return get_temp_manager().cleanup_all()


class TemporaryDirectory:
    """Context manager for temporary directory creation and cleanup."""

    def __init__(self, prefix: str = "temp_dir_"):
        self.prefix = prefix
        self.temp_dir = None
        self.manager = get_temp_manager()

    def __enter__(self):
        self.temp_dir = self.manager.create_temp_dir(prefix=self.prefix)
        return str(self.temp_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir:
            self.manager.cleanup_file(self.temp_dir)