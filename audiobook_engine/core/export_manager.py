import json
from pathlib import Path
try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from ..models.audiobook_project import AudiobookProject
from ..utils.glyph_tracer import create_glyph_commit


class ExportManager:

    def __init__(self):
        self.manifest_dir = Path("storage/manifests")
        self.manifest_dir.mkdir(parents=True, exist_ok=True)

    def build_manifest(self, project, stitch_result):

        manifest = {
            "spec": "goat-audiobook-v1",
            "project_id": str(project.id),
            "book_id": str(project.book_project_id),
            "title": project.title,
            "author": project.author,
            "narrator": project.narrator,
            "total_duration_sec": stitch_result.total_duration_sec,
            "chapters": stitch_result.chapter_markers,
            "checksum_sha256": stitch_result.checksum_sha256,
            "glyph_master": stitch_result.glyph_master
        }

        out_path = self.manifest_dir / f"{project.id}_manifest.json"
        out_path.write_text(json.dumps(manifest, indent=2))

        logger.info(f"[ExportManager] Manifest created at {out_path}")

        return manifest