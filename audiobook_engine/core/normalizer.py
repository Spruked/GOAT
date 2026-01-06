# audiobook_engine/core/normalizer.py
"""
Audio Normalizer for Audiobook Engine

Normalizes audio loudness and removes artifacts for consistent quality.
Implements EBU R128 loudness normalization and audio cleanup.
"""

import os
import logging
from typing import Optional, Dict, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

import numpy as np

from ..config import AUDIO_CONFIG
from ..utils.temp_manager import TempFileManager

# Configure logging
logger = logging.getLogger(__name__)


class NormalizationMode(Enum):
    """Audio normalization modes."""
    EBU_R128 = "ebu_r128"  # Integrated loudness normalization
    RMS = "rms"  # RMS-based normalization
    PEAK = "peak"  # Peak normalization


@dataclass
class NormalizationResult:
    """Result of an audio normalization operation."""
    success: bool
    output_path: Optional[Path] = None
    original_loudness: float = 0.0
    normalized_loudness: float = 0.0
    peak_level: float = 0.0
    dynamic_range: float = 0.0
    artifacts_removed: int = 0
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AudioNormalizer:
    """
    Normalizes audio loudness and removes artifacts.

    Features:
    - EBU R128 integrated loudness normalization
    - RMS and peak normalization modes
    - Artifact detection and removal
    - Dynamic range optimization
    - Quality validation
    """

    def __init__(self, temp_manager: Optional[TempFileManager] = None):
        self.temp_manager = temp_manager or TempFileManager()
        self.target_loudness = AUDIO_CONFIG.get('target_loudness_db', -18.0)  # EBU R128 target
        self.max_peak_level = AUDIO_CONFIG.get('max_peak_level_db', -1.0)  # Headroom
        self.sample_rate = AUDIO_CONFIG.get('sample_rate', 44100)

    def normalize_audio(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        mode: NormalizationMode = NormalizationMode.EBU_R128,
        remove_artifacts: bool = True
    ) -> NormalizationResult:
        """
        Normalize audio file loudness and optionally remove artifacts.

        Args:
            input_path: Path to input audio file
            output_path: Optional output path
            mode: Normalization mode
            remove_artifacts: Whether to remove audio artifacts

        Returns:
            NormalizationResult with processing details
        """
        try:
            # Create output path if not provided
            if output_path is None:
                output_path = self.temp_manager.create_temp_file(
                    suffix=input_path.suffix,
                    prefix="normalized_"
                )

            # Load audio data
            audio_data, sample_rate = self._load_audio(input_path)

            if audio_data is None:
                return NormalizationResult(
                    success=False,
                    error_message="Failed to load audio file"
                )

            # Analyze original audio
            original_loudness = self._calculate_loudness(audio_data, sample_rate, mode)
            original_peak = self._calculate_peak_level(audio_data)
            original_dr = self._calculate_dynamic_range(audio_data)

            # Apply normalization
            normalized_data = self._apply_normalization(audio_data, mode)

            # Remove artifacts if requested
            artifacts_removed = 0
            if remove_artifacts:
                normalized_data, artifacts_removed = self._remove_artifacts(normalized_data)

            # Apply peak limiting
            normalized_data = self._apply_peak_limiting(normalized_data)

            # Save normalized audio
            self._save_audio(normalized_data, sample_rate, output_path)

            # Analyze normalized audio
            normalized_loudness = self._calculate_loudness(normalized_data, sample_rate, mode)
            normalized_peak = self._calculate_peak_level(normalized_data)
            normalized_dr = self._calculate_dynamic_range(normalized_data)

            metadata = {
                'normalization_mode': mode.value,
                'artifacts_removed': artifacts_removed,
                'sample_rate': sample_rate,
                'channels': audio_data.shape[0] if audio_data.ndim > 1 else 1,
                'duration_seconds': len(audio_data[0]) / sample_rate if audio_data.ndim > 1 else len(audio_data) / sample_rate
            }

            logger.info(f"Audio normalized: {input_path} -> {output_path}")
            logger.info(f"Loudness: {original_loudness:.1f}dB -> {normalized_loudness:.1f}dB")

            return NormalizationResult(
                success=True,
                output_path=output_path,
                original_loudness=original_loudness,
                normalized_loudness=normalized_loudness,
                peak_level=normalized_peak,
                dynamic_range=normalized_dr,
                artifacts_removed=artifacts_removed,
                metadata=metadata
            )

        except Exception as e:
            error_msg = f"Normalization failed: {str(e)}"
            logger.error(error_msg)
            return NormalizationResult(
                success=False,
                error_message=error_msg
            )

    def _load_audio(self, file_path: Path) -> Tuple[Optional[np.ndarray], int]:
        """Load audio file into numpy array."""
        try:
            import librosa

            # Load audio with librosa
            audio_data, sample_rate = librosa.load(str(file_path), sr=self.sample_rate, mono=False)

            # Ensure 2D array (channels, samples)
            if audio_data.ndim == 1:
                audio_data = audio_data[np.newaxis, :]

            return audio_data, sample_rate

        except ImportError:
            logger.error("librosa not available for audio loading")
            return None, 0
        except Exception as e:
            logger.error(f"Failed to load audio: {e}")
            return None, 0

    def _save_audio(self, audio_data: np.ndarray, sample_rate: int, output_path: Path):
        """Save audio data to file."""
        try:
            import soundfile as sf

            # Convert back to librosa format if mono
            if audio_data.shape[0] == 1:
                audio_data = audio_data[0]

            # Save with soundfile
            sf.write(str(output_path), audio_data.T if audio_data.ndim > 1 else audio_data,
                    sample_rate, subtype='PCM_16')

        except ImportError:
            logger.error("soundfile not available for audio saving")
            raise
        except Exception as e:
            logger.error(f"Failed to save audio: {e}")
            raise

    def _calculate_loudness(self, audio_data: np.ndarray, sample_rate: int, mode: NormalizationMode) -> float:
        """Calculate audio loudness in dB."""
        try:
            if mode == NormalizationMode.EBU_R128:
                # Simplified EBU R128 calculation
                # In practice, you'd use pyloudnorm or similar
                rms = np.sqrt(np.mean(audio_data ** 2))
                return 20 * np.log10(rms) if rms > 0 else -60.0

            elif mode == NormalizationMode.RMS:
                rms = np.sqrt(np.mean(audio_data ** 2))
                return 20 * np.log10(rms) if rms > 0 else -60.0

            elif mode == NormalizationMode.PEAK:
                return self._calculate_peak_level(audio_data)

        except Exception as e:
            logger.warning(f"Loudness calculation failed: {e}")
            return -60.0

        return -60.0

    def _calculate_peak_level(self, audio_data: np.ndarray) -> float:
        """Calculate peak level in dBFS."""
        peak = np.max(np.abs(audio_data))
        return 20 * np.log10(peak) if peak > 0 else -60.0

    def _calculate_dynamic_range(self, audio_data: np.ndarray) -> float:
        """Calculate dynamic range (difference between peak and RMS)."""
        rms = np.sqrt(np.mean(audio_data ** 2))
        peak = np.max(np.abs(audio_data))

        if rms > 0 and peak > 0:
            return 20 * np.log10(peak / rms)
        return 0.0

    def _apply_normalization(self, audio_data: np.ndarray, mode: NormalizationMode) -> np.ndarray:
        """Apply loudness normalization to audio data."""
        current_loudness = self._calculate_loudness(audio_data, self.sample_rate, mode)

        if mode == NormalizationMode.EBU_R128:
            # Calculate gain needed to reach target loudness
            gain_db = self.target_loudness - current_loudness
        elif mode == NormalizationMode.RMS:
            # Similar to EBU R128 for RMS
            gain_db = self.target_loudness - current_loudness
        elif mode == NormalizationMode.PEAK:
            # Peak normalization to target level
            current_peak = self._calculate_peak_level(audio_data)
            gain_db = self.max_peak_level - current_peak
        else:
            gain_db = 0.0

        # Apply gain
        gain_linear = 10 ** (gain_db / 20.0)
        normalized_data = audio_data * gain_linear

        return normalized_data

    def _apply_peak_limiting(self, audio_data: np.ndarray) -> np.ndarray:
        """Apply peak limiting to prevent clipping."""
        # Simple hard limiting
        max_val = 10 ** (self.max_peak_level / 20.0)
        return np.clip(audio_data, -max_val, max_val)

    def _remove_artifacts(self, audio_data: np.ndarray) -> Tuple[np.ndarray, int]:
        """Remove audio artifacts like clicks and pops."""
        # Simple artifact detection and removal
        # In practice, you'd use more sophisticated algorithms

        artifacts_removed = 0
        cleaned_data = audio_data.copy()

        # Detect clicks (sudden amplitude changes)
        for ch in range(cleaned_data.shape[0]):
            channel_data = cleaned_data[ch]

            # Calculate first derivative
            diff = np.diff(channel_data)

            # Find samples with large changes (potential clicks)
            threshold = np.std(diff) * 3  # 3-sigma threshold
            click_indices = np.where(np.abs(diff) > threshold)[0]

            # Remove clicks by interpolation
            for idx in click_indices:
                if 0 < idx < len(channel_data) - 1:
                    # Linear interpolation
                    channel_data[idx] = (channel_data[idx - 1] + channel_data[idx + 1]) / 2
                    artifacts_removed += 1

        return cleaned_data, artifacts_removed


# Convenience functions
def normalize_audio_file(
    input_path: Path,
    output_path: Optional[Path] = None,
    mode: NormalizationMode = NormalizationMode.EBU_R128,
    remove_artifacts: bool = True
) -> NormalizationResult:
    """Normalize a single audio file."""
    normalizer = AudioNormalizer()
    return normalizer.normalize_audio(input_path, output_path, mode, remove_artifacts)


def batch_normalize_audio(
    input_paths: list[Path],
    output_dir: Optional[Path] = None,
    mode: NormalizationMode = NormalizationMode.EBU_R128,
    remove_artifacts: bool = True
) -> list[NormalizationResult]:
    """Normalize multiple audio files."""
    normalizer = AudioNormalizer()
    results = []

    for input_path in input_paths:
        output_path = None
        if output_dir:
            output_path = output_dir / f"normalized_{input_path.name}"

        result = normalizer.normalize_audio(input_path, output_path, mode, remove_artifacts)
        results.append(result)

    return results