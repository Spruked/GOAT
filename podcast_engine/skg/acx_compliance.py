import pyloudnorm as pyln
import soundfile as sf
import numpy as np
from typing import Dict, Tuple, List
import json

class ACXValidator:
    """
    Ensures audiobook meets ACX Mastered for Audible standards:
    - Peak levels: -3.0 dB (max)
    - RMS levels: -18 to -23 dB LUFS (ideally -19 LUFS)
    - Noise floor: -60 dB FS (room tone)
    - Bitrate: 192 kbps (MP3) or 44.1 kHz/16-bit (WAV)
    - No distortion, clicks, extraneous noises
    """

    def __init__(self):
        self.target_lufs = -19.0
        self.target_peak = -3.0
        self.min_noise_floor = -60.0

    def validate_and_correct(self, audio_path: str) -> Tuple[bool, str, Dict]:
        """
        Returns: (is_compliant, corrected_path, report)
        """
        try:
            data, rate = sf.read(audio_path)

            # 1. Measure loudness
            meter = pyln.Meter(rate)
            loudness = meter.integrated_loudness(data)

            # 2. Measure true peak
            peak_db = 20 * np.log10(np.max(np.abs(data))) if np.max(np.abs(data)) > 0 else -np.inf

            # 3. Measure noise floor (assume first 0.5s is room tone)
            noise_sample = data[:int(rate * 0.5)]
            noise_floor = 20 * np.log10(np.sqrt(np.mean(noise_sample**2)))

            report = {
                "original_loudness": loudness,
                "original_peak": peak_db,
                "noise_floor": noise_floor,
                "duration_seconds": len(data) / rate
            }

            # Auto-correct if needed
            needs_correction = False
            if not self._is_compliant(report):
                corrected_path = self._correct_audio(audio_path, report)
                needs_correction = True
            else:
                corrected_path = audio_path

            # Update report
            if needs_correction:
                final_data, final_rate = sf.read(corrected_path)
                final_loudness = meter.integrated_loudness(final_data)
                final_peak = 20 * np.log10(np.max(np.abs(final_data)))
                report["corrected_loudness"] = final_loudness
                report["corrected_peak"] = final_peak

            report["compliant"] = self._is_compliant(report)
            return (report["compliant"], corrected_path, report)

        except Exception as e:
            return (False, audio_path, {"error": str(e)})

    def _is_compliant(self, report: Dict) -> bool:
        """Check against ACX standards"""
        compliance = {
            "loudness_ok": self.target_lufs - 2 <= report["original_loudness"] <= self.target_lufs + 2,
            "peak_ok": report["original_peak"] <= self.target_peak,
            "noise_ok": report["noise_floor"] <= self.min_noise_floor
        }

        report["compliance_checks"] = compliance
        return all(compliance.values())

    def _correct_audio(self, audio_path: str, report: Dict) -> str:
        """Apply corrections to meet ACX specs"""
        from pydub import AudioSegment
        import math

        audio = AudioSegment.from_file(audio_path)

        # 1. Peak normalization to -3 dB
        if report["original_peak"] > self.target_peak:
            headroom = self.target_peak - report["original_peak"]
            audio = audio.apply_gain(headroom - 0.1)  # Safety margin

        # 2. Loudness normalization to -19 LUFS
        current_lufs = report["original_loudness"]
        lufs_correction = self.target_lufs - current_lufs
        audio = audio.apply_gain(lufs_correction)

        # 3. Noise gate if noise floor is too high
        if report["noise_floor"] > self.min_noise_floor:
            audio = self._apply_noise_gate(audio, threshold=self.min_noise_floor)

        # Export corrected version
        corrected_path = audio_path.replace(".wav", "_acx_mastered.wav")
        audio.export(corrected_path, format="wav", parameters=["-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le"])

        return corrected_path

    def _apply_noise_gate(self, audio: AudioSegment, threshold: float) -> AudioSegment:
        """Simple noise gate: silence segments below threshold"""
        # Convert to numpy for processing
        samples = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate

        # Threshold in amplitude (convert from dB)
        threshold_amp = 10 ** (threshold / 20) * 32768

        # Gate silent sections
        gate_mask = np.abs(samples) > threshold_amp
        gated_samples = samples * gate_mask

        return AudioSegment(
            gated_samples.astype(np.int16).tobytes(),
            frame_rate=sample_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )

    def generate_acx_report(self, report_path: str, audio_files: List[str]):
        """Generate compliance report for entire audiobook"""

        full_report = {
            "audiobook_title": "The Name of the Wind",
            "total_files": len(audio_files),
            "files": []
        }

        all_compliant = True

        for file_path in audio_files:
            is_compliant, corrected_path, file_report = self.validate_and_correct(file_path)

            full_report["files"].append({
                "file": file_path,
                "compliant": is_compliant,
                "corrected_file": corrected_path if corrected_path != file_path else None,
                "metrics": file_report
            })

            if not is_compliant:
                all_compliant = False

        full_report["overall_compliant"] = all_compliant

        # Save report
        with open(report_path, 'w') as f:
            json.dump(full_report, f, indent=2)

        # Print summary
        print(f"\n📊 ACX Compliance Report")
        print(f"{'✅' if all_compliant else '⚠️'}  Overall Status: {'PASS' if all_compliant else 'NEEDS CORRECTION'}")
        print(f"📁 Files processed: {len(audio_files)}")

        return full_report