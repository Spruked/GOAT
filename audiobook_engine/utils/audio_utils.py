# audiobook_engine/utils/audio_utils.py
"""
Audio Utilities for Audiobook Engine

Helper functions for audio file processing and analysis.
"""

import os
import logging
from typing import Optional, Dict, Any, Tuple, List
from pathlib import Path

import numpy as np

# Configure logging
logger = logging.getLogger(__name__)


def get_audio_info(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about an audio file.

    Args:
        file_path: Path to audio file

    Returns:
        Dictionary with audio information, or None if error
    """
    try:
        import librosa

        # Load audio to get info
        info = {}

        # Use soundfile for basic info first
        try:
            import soundfile as sf
            with sf.SoundFile(str(file_path)) as sf_file:
                info['samplerate'] = sf_file.samplerate
                info['channels'] = sf_file.channels
                info['frames'] = sf_file.frames
                info['duration'] = sf_file.frames / sf_file.samplerate
                info['format'] = sf_file.format
                info['subtype'] = sf_file.subtype
        except ImportError:
            # Fallback to librosa
            audio, sr = librosa.load(str(file_path), sr=None)
            info['samplerate'] = sr
            info['channels'] = 1 if audio.ndim == 1 else audio.shape[0]
            info['frames'] = len(audio[0]) if audio.ndim > 1 else len(audio)
            info['duration'] = info['frames'] / sr

        # Additional analysis with librosa
        audio, _ = librosa.load(str(file_path), sr=44100)

        # Calculate audio metrics
        rms = np.sqrt(np.mean(audio ** 2))
        info['rms_level'] = 20 * np.log10(rms) if rms > 0 else -60.0
        info['peak_level'] = 20 * np.log10(np.max(np.abs(audio))) if np.max(np.abs(audio)) > 0 else -60.0

        # Dynamic range
        info['dynamic_range'] = info['peak_level'] - info['rms_level']

        # File size
        info['file_size_bytes'] = file_path.stat().st_size

        return info

    except ImportError:
        logger.error("Audio libraries not available (librosa/soundfile)")
        return None
    except Exception as e:
        logger.error(f"Failed to get audio info for {file_path}: {e}")
        return None


def convert_audio_format(
    input_path: Path,
    output_path: Path,
    output_format: str = 'wav',
    sample_rate: Optional[int] = None,
    channels: Optional[int] = None
) -> bool:
    """
    Convert audio file to different format.

    Args:
        input_path: Input audio file path
        output_path: Output audio file path
        output_format: Output format ('wav', 'flac', 'mp3', etc.)
        sample_rate: Target sample rate (None to keep original)
        channels: Target channel count (None to keep original)

    Returns:
        True if conversion successful, False otherwise
    """
    try:
        import subprocess

        # Build ffmpeg command
        cmd = ['ffmpeg', '-y', '-i', str(input_path)]

        # Add sample rate conversion
        if sample_rate:
            cmd.extend(['-ar', str(sample_rate)])

        # Add channel conversion
        if channels:
            if channels == 1:
                cmd.extend(['-ac', '1'])  # Mono
            elif channels == 2:
                cmd.extend(['-ac', '2'])  # Stereo

        # Set output format and path
        if output_format.lower() == 'mp3':
            cmd.extend(['-c:a', 'libmp3lame', '-b:a', '128k'])
        elif output_format.lower() == 'flac':
            cmd.extend(['-c:a', 'flac'])
        elif output_format.lower() == 'wav':
            cmd.extend(['-c:a', 'pcm_s16le'])

        cmd.append(str(output_path))

        # Run conversion
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f"Converted {input_path} to {output_path}")
            return True
        else:
            logger.error(f"Audio conversion failed: {result.stderr}")
            return False

    except ImportError:
        logger.error("ffmpeg not available for audio conversion")
        return False
    except Exception as e:
        logger.error(f"Audio conversion failed: {e}")
        return False


def mix_audio_channels(audio_data: np.ndarray, mix_type: str = 'stereo') -> np.ndarray:
    """
    Mix audio channels.

    Args:
        audio_data: Audio data array (channels, samples)
        mix_type: Mixing type ('mono', 'stereo', 'downmix')

    Returns:
        Mixed audio data
    """
    try:
        if audio_data.ndim == 1:
            # Already mono
            return audio_data

        channels, samples = audio_data.shape

        if mix_type == 'mono':
            # Mix to mono by averaging channels
            return np.mean(audio_data, axis=0)

        elif mix_type == 'stereo':
            if channels == 1:
                # Duplicate mono to stereo
                return np.tile(audio_data, (2, 1))
            elif channels == 2:
                # Already stereo
                return audio_data
            else:
                # Downmix to stereo (take first two channels)
                return audio_data[:2]

        elif mix_type == 'downmix':
            # ITU-R BS.775-1 downmix to stereo
            if channels >= 2:
                left = audio_data[0]
                right = audio_data[1]
                # Add center channel to both if it exists
                if channels >= 3:
                    center = audio_data[2] * 0.707  # -3dB
                    left += center
                    right += center
                return np.array([left, right])

        return audio_data

    except Exception as e:
        logger.error(f"Audio channel mixing failed: {e}")
        return audio_data


def detect_silence(
    audio_data: np.ndarray,
    sample_rate: int,
    threshold_db: float = -40.0,
    min_duration_ms: int = 500
) -> List[Tuple[float, float]]:
    """
    Detect silent segments in audio.

    Args:
        audio_data: Audio data array
        sample_rate: Sample rate
        threshold_db: Silence threshold in dB
        min_duration_ms: Minimum silence duration in milliseconds

    Returns:
        List of (start_time, end_time) tuples for silent segments
    """
    try:
        # Convert threshold to linear
        threshold_linear = 10 ** (threshold_db / 20.0)

        # Calculate RMS in sliding window
        window_size = int(sample_rate * 0.01)  # 10ms windows
        rms_values = []

        for i in range(0, len(audio_data) - window_size, window_size // 2):
            window = audio_data[i:i + window_size]
            rms = np.sqrt(np.mean(window ** 2))
            rms_values.append(rms)

        # Find silent windows
        silent_windows = []
        min_duration_samples = int(min_duration_ms / 1000 * sample_rate)

        i = 0
        while i < len(rms_values):
            if rms_values[i] < threshold_linear:
                # Start of silence
                start_idx = i
                while i < len(rms_values) and rms_values[i] < threshold_linear:
                    i += 1
                end_idx = i

                # Check minimum duration
                duration_samples = (end_idx - start_idx) * (window_size // 2)
                if duration_samples >= min_duration_samples:
                    start_time = start_idx * (window_size // 2) / sample_rate
                    end_time = end_idx * (window_size // 2) / sample_rate
                    silent_windows.append((start_time, end_time))
            else:
                i += 1

        return silent_windows

    except Exception as e:
        logger.error(f"Silence detection failed: {e}")
        return []


def split_audio_by_silence(
    audio_data: np.ndarray,
    sample_rate: int,
    silence_segments: List[Tuple[float, float]],
    min_segment_duration: float = 1.0
) -> List[Tuple[np.ndarray, float, float]]:
    """
    Split audio into segments based on silence detection.

    Args:
        audio_data: Audio data array
        sample_rate: Sample rate
        silence_segments: List of (start, end) silence tuples
        min_segment_duration: Minimum segment duration in seconds

    Returns:
        List of (audio_segment, start_time, end_time) tuples
    """
    try:
        segments = []

        # Start from beginning
        current_start = 0.0

        for silence_start, silence_end in silence_segments:
            # Create segment from current_start to silence_start
            segment_duration = silence_start - current_start

            if segment_duration >= min_segment_duration:
                start_sample = int(current_start * sample_rate)
                end_sample = int(silence_start * sample_rate)

                segment = audio_data[start_sample:end_sample]
                segments.append((segment, current_start, silence_start))

            # Move past silence
            current_start = silence_end

        # Add final segment
        final_duration = len(audio_data) / sample_rate - current_start
        if final_duration >= min_segment_duration:
            start_sample = int(current_start * sample_rate)
            segment = audio_data[start_sample:]
            segments.append((segment, current_start, len(audio_data) / sample_rate))

        return segments

    except Exception as e:
        logger.error(f"Audio splitting failed: {e}")
        return []


def calculate_audio_quality_metrics(audio_data: np.ndarray, sample_rate: int) -> Dict[str, float]:
    """
    Calculate various audio quality metrics.

    Args:
        audio_data: Audio data array
        sample_rate: Sample rate

    Returns:
        Dictionary of quality metrics
    """
    try:
        metrics = {}

        # Basic levels
        rms = np.sqrt(np.mean(audio_data ** 2))
        peak = np.max(np.abs(audio_data))

        metrics['rms_db'] = 20 * np.log10(rms) if rms > 0 else -60.0
        metrics['peak_db'] = 20 * np.log10(peak) if peak > 0 else -60.0
        metrics['crest_factor'] = peak / rms if rms > 0 else 0.0

        # Dynamic range
        metrics['dynamic_range_db'] = metrics['peak_db'] - metrics['rms_db']

        # Noise floor (last 10% of signal)
        noise_start = int(len(audio_data) * 0.9)
        noise_segment = audio_data[noise_start:]
        noise_rms = np.sqrt(np.mean(noise_segment ** 2))
        metrics['noise_floor_db'] = 20 * np.log10(noise_rms) if noise_rms > 0 else -60.0

        # SNR estimate
        if noise_rms > 0 and rms > noise_rms:
            metrics['snr_db'] = 20 * np.log10(rms / noise_rms)
        else:
            metrics['snr_db'] = 60.0  # High SNR if noise below signal

        return metrics

    except Exception as e:
        logger.error(f"Quality metrics calculation failed: {e}")
        return {}


def normalize_audio_levels(
    audio_data: np.ndarray,
    target_level_db: float = -18.0,
    max_peak_db: float = -1.0
) -> np.ndarray:
    """
    Normalize audio to target level with peak limiting.

    Args:
        audio_data: Input audio data
        target_level_db: Target RMS level in dB
        max_peak_db: Maximum peak level in dB

    Returns:
        Normalized audio data
    """
    try:
        # Calculate current RMS
        rms = np.sqrt(np.mean(audio_data ** 2))
        current_level_db = 20 * np.log10(rms) if rms > 0 else -60.0

        # Calculate gain
        gain_db = target_level_db - current_level_db
        gain_linear = 10 ** (gain_db / 20.0)

        # Apply gain
        normalized = audio_data * gain_linear

        # Peak limiting
        max_peak_linear = 10 ** (max_peak_db / 20.0)
        normalized = np.clip(normalized, -max_peak_linear, max_peak_linear)

        return normalized

    except Exception as e:
        logger.error(f"Audio normalization failed: {e}")
        return audio_data