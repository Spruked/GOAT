# audiobook_engine/utils/checksum.py
"""
Checksum Utilities for Audiobook Engine

Provides file and data integrity verification using various algorithms.
"""

import hashlib
import logging
from typing import Optional, Union
from pathlib import Path
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)


class ChecksumAlgorithm(Enum):
    """Supported checksum algorithms."""
    SHA256 = "sha256"
    SHA512 = "sha512"
    MD5 = "md5"  # Not recommended for security, but fast
    BLAKE2B = "blake2b"


def calculate_file_checksum(
    file_path: Union[str, Path],
    algorithm: ChecksumAlgorithm = ChecksumAlgorithm.SHA256,
    chunk_size: int = 8192
) -> Optional[str]:
    """
    Calculate checksum of a file.

    Args:
        file_path: Path to the file
        algorithm: Checksum algorithm to use
        chunk_size: Size of chunks to read (for memory efficiency)

    Returns:
        Hexadecimal checksum string, or None if error
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return None

        # Create hash object
        if algorithm == ChecksumAlgorithm.SHA256:
            hash_obj = hashlib.sha256()
        elif algorithm == ChecksumAlgorithm.SHA512:
            hash_obj = hashlib.sha512()
        elif algorithm == ChecksumAlgorithm.MD5:
            hash_obj = hashlib.md5()
        elif algorithm == ChecksumAlgorithm.BLAKE2B:
            hash_obj = hashlib.blake2b()
        else:
            logger.error(f"Unsupported algorithm: {algorithm}")
            return None

        # Read file in chunks and update hash
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hash_obj.update(chunk)

        checksum = hash_obj.hexdigest()
        logger.debug(f"Calculated {algorithm.value} checksum for {file_path}: {checksum}")
        return checksum

    except Exception as e:
        logger.error(f"Failed to calculate checksum for {file_path}: {e}")
        return None


def calculate_data_checksum(
    data: Union[str, bytes],
    algorithm: ChecksumAlgorithm = ChecksumAlgorithm.SHA256
) -> Optional[str]:
    """
    Calculate checksum of data.

    Args:
        data: Data to checksum (string or bytes)
        algorithm: Checksum algorithm to use

    Returns:
        Hexadecimal checksum string, or None if error
    """
    try:
        # Convert string to bytes if needed
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Create hash object
        if algorithm == ChecksumAlgorithm.SHA256:
            hash_obj = hashlib.sha256()
        elif algorithm == ChecksumAlgorithm.SHA512:
            hash_obj = hashlib.sha512()
        elif algorithm == ChecksumAlgorithm.MD5:
            hash_obj = hashlib.md5()
        elif algorithm == ChecksumAlgorithm.BLAKE2B:
            hash_obj = hashlib.blake2b()
        else:
            logger.error(f"Unsupported algorithm: {algorithm}")
            return None

        hash_obj.update(data)
        checksum = hash_obj.hexdigest()

        logger.debug(f"Calculated {algorithm.value} checksum for data: {checksum}")
        return checksum

    except Exception as e:
        logger.error(f"Failed to calculate data checksum: {e}")
        return None


def validate_checksum(
    file_path: Union[str, Path],
    expected_checksum: str,
    algorithm: ChecksumAlgorithm = ChecksumAlgorithm.SHA256
) -> bool:
    """
    Validate file checksum against expected value.

    Args:
        file_path: Path to the file
        expected_checksum: Expected checksum string
        algorithm: Checksum algorithm used

    Returns:
        True if checksum matches, False otherwise
    """
    try:
        actual_checksum = calculate_file_checksum(file_path, algorithm)

        if actual_checksum is None:
            return False

        matches = actual_checksum.lower() == expected_checksum.lower()

        if matches:
            logger.debug(f"Checksum validation passed for {file_path}")
        else:
            logger.warning(f"Checksum validation failed for {file_path}")
            logger.debug(f"Expected: {expected_checksum}")
            logger.debug(f"Actual: {actual_checksum}")

        return matches

    except Exception as e:
        logger.error(f"Checksum validation failed: {e}")
        return False


def get_checksum_algorithm_from_string(algorithm_str: str) -> Optional[ChecksumAlgorithm]:
    """
    Convert algorithm string to ChecksumAlgorithm enum.

    Args:
        algorithm_str: Algorithm name (case-insensitive)

    Returns:
        ChecksumAlgorithm enum value, or None if invalid
    """
    try:
        return ChecksumAlgorithm(algorithm_str.lower())
    except ValueError:
        logger.warning(f"Unknown checksum algorithm: {algorithm_str}")
        return None


def calculate_multi_file_checksum(
    file_paths: list[Union[str, Path]],
    algorithm: ChecksumAlgorithm = ChecksumAlgorithm.SHA256
) -> Optional[str]:
    """
    Calculate combined checksum for multiple files.

    Args:
        file_paths: List of file paths
        algorithm: Checksum algorithm to use

    Returns:
        Combined checksum of all files, or None if error
    """
    try:
        # Create hash object
        if algorithm == ChecksumAlgorithm.SHA256:
            hash_obj = hashlib.sha256()
        elif algorithm == ChecksumAlgorithm.SHA512:
            hash_obj = hashlib.sha512()
        elif algorithm == ChecksumAlgorithm.MD5:
            hash_obj = hashlib.md5()
        elif algorithm == ChecksumAlgorithm.BLAKE2B:
            hash_obj = hashlib.blake2b()
        else:
            logger.error(f"Unsupported algorithm: {algorithm}")
            return None

        # Sort files for consistent ordering
        sorted_paths = sorted(Path(p) for p in file_paths)

        # Hash each file's checksum
        for file_path in sorted_paths:
            file_checksum = calculate_file_checksum(file_path, algorithm)
            if file_checksum is None:
                logger.error(f"Failed to checksum file: {file_path}")
                return None
            hash_obj.update(file_checksum.encode('utf-8'))

        combined_checksum = hash_obj.hexdigest()
        logger.debug(f"Calculated combined {algorithm.value} checksum for {len(file_paths)} files: {combined_checksum}")
        return combined_checksum

    except Exception as e:
        logger.error(f"Failed to calculate multi-file checksum: {e}")
        return None


# Convenience functions for common use cases
def sha256_file(file_path: Union[str, Path]) -> Optional[str]:
    """Calculate SHA256 checksum of a file."""
    return calculate_file_checksum(file_path, ChecksumAlgorithm.SHA256)

def sha256_data(data: Union[str, bytes]) -> Optional[str]:
    """Calculate SHA256 checksum of data."""
    return calculate_data_checksum(data, ChecksumAlgorithm.SHA256)

def validate_sha256(file_path: Union[str, Path], expected: str) -> bool:
    """Validate SHA256 checksum of a file."""
    return validate_checksum(file_path, expected, ChecksumAlgorithm.SHA256)