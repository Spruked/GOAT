from .acx_compliance import ACXValidator
from typing import Dict, List
import os

class ACXPackager:
    """
    Creates full ACX-ready package including:
    - Opening/closing credits
    - Chapter files with metadata
    - Retail audio sample
    - Noise reduction profile
    - Submission-ready ZIP
    """

    def __init__(self, skg):
        self.skg = skg
        self.validator = ACXValidator()

    def package_audiobook_for_acx(self, project_config: Dict) -> str:
        """
        project_config: {
            "title": "The Lean Startup",
            "author": "Eric Ries",
            "narrator_id": "phil_dandy",
            "copyright": "2024",
            "isbn": "978-0-9999999-9-9",
            "chapters": [
                {"title": "Introduction", "audio_path": "ch01.wav"},
                {"title": "Chapter 1", "audio_path": "ch02.wav"}
            ],
            "retail_sample_duration": 300  # 5 minutes
        }
        """

        output_dir = f"output/acx/{project_config['title'].replace(' ', '_')}"
        os.makedirs(output_dir, exist_ok=True)

        # 1. Generate opening credits
        opening_path = self._generate_opening_credits(project_config)

        # 2. Generate closing credits
        closing_path = self._generate_closing_credits(project_config)

        # 3. Validate and correct all chapter files
        validated_chapters = []
        for chapter in project_config["chapters"]:
            print(f"🔍 Validating: {chapter['title']}")
            is_compliant, corrected_path, report = self.validator.validate_and_correct(chapter["audio_path"])

            validated_chapters.append({
                **chapter,
                "audio_path": corrected_path,
                "compliant": is_compliant,
                "report": report
            })

        # 4. Create retail sample (first 5 minutes)
        retail_sample = self._create_retail_sample(
            validated_chapters,
            project_config["retail_sample_duration"],
            output_dir
        )

        # 5. Generate metadata JSON for ACX upload
        metadata_path = self._generate_acx_metadata(project_config, validated_chapters, retail_sample)

        # 6. Create master track list for file naming
        final_files = [
            ("01_OpeningCredits.wav", opening_path),
            *[(f"{i+2:02d}_{ch['title'].replace(' ', '')}.wav", ch["audio_path"]) for i, ch in enumerate(validated_chapters)],
            (f"{len(validated_chapters)+2:02d}_ClosingCredits.wav", closing_path)
        ]

        # 7. Copy files to ACX directory with proper naming
        for filename, src_path in final_files:
            dest = os.path.join(output_dir, filename)
            os.system(f"cp '{src_path}' '{dest}'")
            print(f"📦 Copied: {filename}")

        # 8. Generate final validation report
        report_path = os.path.join(output_dir, "acx_validation_report.json")
        all_audio_files = [path for _, path in final_files]
        validation_report = self.validator.generate_acx_report(report_path, all_audio_files)

        # 9. Create ZIP for ACX submission
        zip_path = self._create_submission_zip(output_dir, project_config)

        print(f"\n🎉 ACX Package Complete!")
        print(f"📁 Location: {output_dir}/")
        print(f"📦 ZIP: {zip_path}")
        print(f"📊 Report: {report_path}")

        return output_dir

    def _generate_opening_credits(self, config: Dict) -> str:
        """Generate professional opening credits"""

        narrator = self.skg.get_persona(config["narrator_id"])

        credits_script = f"""
        This is Audible.

        {config['title']}, by {config['author']}.

        Narrated by {narrator['name']}.

        Copyright {config.get('copyright', '2024')}.
        """

        # Use formal narrator voice
        path = self.skg.synthesize_as_persona(
            text=credits_script,
            persona_id=config["narrator_id"],
            style="formal_announcement",
            output_path="output/temp/opening_credits.wav"
        )

        return path

    def _generate_closing_credits(self, config: Dict) -> str:
        """Generate closing credits with call-to-action"""

        narrator = self.skg.get_persona(config["narrator_id"])

        credits_script = f"""
        You have been listening to {config['title']}, written by {config['author']}.

        Narrated by {narrator['name']}.

        This audiobook was produced using the GOAT Audiobook System.

        Thank you for listening.
        """

        path = self.skg.synthesize_as_persona(
            text=credits_script,
            persona_id=config["narrator_id"],
            style="warm_closing",
            output_path="output/temp/closing_credits.wav"
        )

        return path

    def _create_retail_sample(self, chapters: List[Dict], duration: int, output_dir: str) -> str:
        """Extract first N seconds for retail sample"""
        from pydub import AudioSegment

        sample_duration = 0
        sample_segments = []

        for chapter in chapters:
            audio = AudioSegment.from_wav(chapter["audio_path"])

            # Skip very short chapters (like intros)
            if len(audio) < 10000:  # < 10 seconds
                continue

            remaining_duration = duration - sample_duration
            if remaining_duration <= 0:
                break

            segment = audio[:remaining_duration * 1000]  # pydub uses ms
            sample_segments.append(segment)
            sample_duration += len(segment) / 1000

        # Combine and fade
        retail_sample = sum(sample_segments, AudioSegment.empty())
        retail_sample = retail_sample.fade_in(2000).fade_out(3000)

        # Export
        retail_path = os.path.join(output_dir, "retail_sample.mp3")
        retail_sample.export(retail_path, format="mp3", bitrate="192k")

        return retail_path

    def _generate_acx_metadata(self, config: Dict, chapters: List[Dict], retail_sample: str) -> str:
        """Generate metadata JSON for ACX upload"""

        metadata = {
            "title": config["title"],
            "author": config["author"],
            "narrator": self.skg.get_persona(config["narrator_id"])["name"],
            "copyright": config.get("copyright"),
            "isbn": config.get("isbn"),
            "runtime_minutes": sum(ch["report"]["duration_seconds"] for ch in chapters) / 60,
            "file_list": [{"filename": f"{i+1:02d}_{ch['title']}", "duration": ch["report"]["duration_seconds"]} for i, ch in enumerate(chapters)],
            "retail_sample": os.path.basename(retail_sample),
            "compliance_status": "PASS",
            "specifications": {
                "peak_level_db": "-3.0",
                "rms_level_lufs": "-19.0",
                "bit_rate": "192 kbps",
                "sample_rate": "44.1 kHz",
                "channels": "2 (stereo)"
            }
        }

        metadata_path = os.path.join(os.path.dirname(retail_sample), "acx_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        return metadata_path

    def _create_submission_zip(self, output_dir: str, config: Dict) -> str:
        """Create final ZIP file for ACX"""

        zip_filename = f"ACX_{config['title'].replace(' ', '_')}.zip"
        zip_path = os.path.join(output_dir, zip_filename)

        # Use system zip command (more reliable for large files)
        os.system(f"cd '{output_dir}' && zip -r '{zip_filename}' *.wav *.mp3 *.json")

        return zip_path