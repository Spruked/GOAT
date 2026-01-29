# legacy_builder.py
"""
GOAT Legacy Builder - Production Hardened
Creates masterpieces from user data using streaming VisiData analysis
Memory-efficient for pay-per-GB model, ChaCha20-256 encryption ready, WorkerSKG integrated
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime
import visidata as vd
import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

# Import WorkerSKG for DALS integration
try:
    from workers._templates.worker_skg_template import WorkerSKG
    WORKERSKG_AVAILABLE = True
except ImportError:
    WORKERSKG_AVAILABLE = False
    print("Warning: WorkerSKG not available, running in standalone mode")

class GOATLegacyBuilder:
    """
    Production-hardened legacy builder with streaming VisiData analysis.
    Memory-efficient for multi-GB files, encryption-ready, WorkerSKG integrated.
    """

    def __init__(self, worker_id: str = None, ucm_connector=None, output_dir: str = "./deliverables/legacy"):
        """
        Initialize with optional WorkerSKG integration

        Args:
            worker_id: Unique worker identifier for DALS integration
            ucm_connector: UCM connector for transfers
            output_dir: Base output directory
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # WorkerSKG integration if available
        if WORKERSKG_AVAILABLE and worker_id and ucm_connector:
            WorkerSKG.__init__(self, worker_id, "legacy_builder", ucm_connector)
            self.worker_mode = True
        else:
            self.worker_mode = False

        # Encryption setup for TrueMark
        self.encryption_key = secrets.token_bytes(32)  # ChaCha20-256 key

    async def build_legacy_streaming(self, user_data: Dict[str, Any], product_type: str = "book") -> AsyncGenerator[Dict[str, Any], None]:
        """
        Build legacy using streaming VisiData analysis - memory efficient for large files
        Yields progress updates for real-time UX
        """

        yield {"status": "starting", "message": "Initializing legacy builder...", "progress": 0}

        # Phase 1: Streaming data analysis
        yield {"status": "analyzing", "message": "Analyzing data files with VisiData...", "progress": 10}
        data_insights = await self._analyze_data_streaming(user_data)

        yield {"status": "analyzing", "message": f"Found {len(data_insights)} data sources", "progress": 30}

        # Phase 2: Content generation
        yield {"status": "generating", "message": "Generating content structure...", "progress": 50}
        content = await self._generate_content_from_insights(user_data, data_insights, product_type)

        # Phase 3: Cost calculation (GOAT pricing: $19.99 base + $5/GB)
        total_gb = self._calculate_data_size(user_data)
        processing_cost = 19.99 + (total_gb * 5)

        yield {"status": "pricing", "message": f"Processing {total_gb:.1f}GB - Cost: ${processing_cost:.2f}", "progress": 70}

        # Phase 4: Encryption preparation for TrueMark
        yield {"status": "encrypting", "message": "Preparing for permanent storage...", "progress": 85}
        encrypted_content = await self._prepare_encrypted_content(content)

        # Phase 5: Final assembly
        legacy = {
            "user_id": user_data.get("user_id", "anonymous"),
            "product_type": product_type,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": "2.0-streaming",
            "data_insights": data_insights,
            "content": content,
            "encrypted_content": encrypted_content,
            "pricing": {
                "data_size_gb": total_gb,
                "processing_cost": processing_cost,
                "permanent_storage_cost": 9.99  # Flat rate for IPFS/Arweave
            },
            "nft_metadata": await self._generate_nft_metadata(user_data, content, product_type)
        }

        # Export files
        await self._export_legacy_files_streaming(legacy)

        yield {"status": "complete", "message": "Legacy created successfully!", "progress": 100, "legacy": legacy}

    async def _analyze_data_streaming(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Streaming VisiData analysis - processes files without loading into memory
        """
        insights = {}

        if "data_files" not in user_data:
            return insights

        for file_path in user_data["data_files"]:
            if not os.path.exists(file_path):
                continue

            try:
                # Use VisiData's streaming capabilities instead of pandas
                vd_sheet = vd.openSource(file_path)

                # Stream analysis without full load
                insights[file_path] = await self._stream_analyze_sheet(vd_sheet, file_path)

            except Exception as e:
                insights[file_path] = {"error": str(e), "streaming_analysis": True}

        return insights

    async def _stream_analyze_sheet(self, vd_sheet, file_path: str) -> Dict[str, Any]:
        """
        Analyze VisiData sheet using streaming - memory efficient
        """
        analysis = {
            "filename": Path(file_path).name,
            "streaming_analysis": True,
            "columns": [],
            "data_types": {},
            "row_sample_size": 0,
            "estimated_total_rows": 0,
            "themes_extracted": [],
            "anomalies_detected": []
        }

        try:
            # Get column information without loading all data
            if hasattr(vd_sheet, 'columns'):
                analysis["columns"] = [str(col) for col in vd_sheet.columns]
                analysis["column_count"] = len(vd_sheet.columns)

            # Sample first 1000 rows for analysis (streaming)
            sample_data = []
            row_count = 0

            for row in vd_sheet.iterrows():
                if row_count >= 1000:  # Limit sample size
                    break
                sample_data.append(row)
                row_count += 1

            analysis["row_sample_size"] = len(sample_data)

            # Estimate total rows (rough calculation)
            file_size = os.path.getsize(file_path)
            avg_row_size = sum(len(str(row)) for row in sample_data) / len(sample_data) if sample_data else 100
            analysis["estimated_total_rows"] = int(file_size / avg_row_size)

            # Extract themes from sample data
            analysis["themes_extracted"] = self._extract_themes_from_sample(sample_data)

            # Detect anomalies in sample
            analysis["anomalies_detected"] = self._detect_anomalies_in_sample(sample_data)

        except Exception as e:
            analysis["streaming_error"] = str(e)

        return analysis

    def _extract_themes_from_sample(self, sample_data: List) -> List[str]:
        """Extract content themes from data sample"""
        themes = set()

        for row in sample_data:
            for cell in row:
                if isinstance(cell, str) and len(cell) > 10:
                    # Simple keyword extraction
                    words = cell.lower().split()
                    for word in words:
                        if len(word) > 4 and word not in ['that', 'with', 'this', 'from', 'they', 'have', 'been', 'were']:
                            themes.add(word.title())

        return list(themes)[:10]  # Limit to 10 themes

    def _detect_anomalies_in_sample(self, sample_data: List) -> List[str]:
        """Detect data anomalies that might suggest stories"""
        anomalies = []

        # Simple anomaly detection - look for outliers in numeric data
        numeric_values = []
        for row in sample_data:
            for cell in row:
                try:
                    if isinstance(cell, (int, float)) or (isinstance(cell, str) and cell.replace('.', '').isdigit()):
                        numeric_values.append(float(cell))
                except:
                    continue

        if len(numeric_values) > 10:
            mean_val = sum(numeric_values) / len(numeric_values)
            std_dev = (sum((x - mean_val) ** 2 for x in numeric_values) / len(numeric_values)) ** 0.5

            outliers = [v for v in numeric_values if abs(v - mean_val) > 2 * std_dev]
            if outliers:
                anomalies.append(f"Found {len(outliers)} statistical outliers - potential story triggers")

        return anomalies

    async def _generate_content_from_insights(self, user_data: Dict[str, Any], insights: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """Generate content structure from streaming insights"""

        # Extract all themes across files
        all_themes = []
        for file_insights in insights.values():
            if isinstance(file_insights, dict):
                all_themes.extend(file_insights.get("themes_extracted", []))

        unique_themes = list(set(all_themes))[:8]  # Limit themes

        if product_type == "book":
            content = {
                "title": user_data.get("title", "Untitled Book"),
                "chapters": [
                    {
                        "number": i + 1,
                        "title": f"Chapter {i+1}: {theme}",
                        "content_outline": f"Exploring {theme} based on data analysis",
                        "estimated_pages": 15,
                        "data_sources": []  # Will be populated from insights
                    } for i, theme in enumerate(unique_themes)
                ],
                "foreword": f"This book represents the greatest work of {user_data.get('author', 'the author')}.",
                "estimated_pages": len(unique_themes) * 15 + 50,
                "key_themes": unique_themes
            }

        elif product_type == "course":
            content = {
                "title": user_data.get("title", "Untitled Course"),
                "modules": [
                    {
                        "number": i + 1,
                        "title": f"Module {i+1}: {theme}",
                        "lessons": ["Introduction", "Core Concepts", "Practice", "Assessment"],
                        "duration_hours": 2
                    } for i, theme in enumerate(unique_themes[:6])
                ],
                "duration_hours": len(unique_themes) * 2,
                "learning_objectives": [f"Master {theme}" for theme in unique_themes[:5]],
                "prerequisites": user_data.get("prerequisites", [])
            }

        else:
            content = {
                "title": user_data.get("title", f"Untitled {product_type.title()}"),
                "sections": [
                    {
                        "number": i + 1,
                        "title": f"Section {i+1}: {theme}",
                        "content_type": product_type
                    } for i, theme in enumerate(unique_themes[:5])
                ],
                "content_type": product_type,
                "insights_summary": {
                    "total_files_analyzed": len(insights),
                    "themes_discovered": len(unique_themes),
                    "key_points": unique_themes[:3]
                }
            }

        return content

    def _calculate_data_size(self, user_data: Dict[str, Any]) -> float:
        """Calculate total data size in GB"""
        total_bytes = 0

        if "data_files" in user_data:
            for file_path in user_data["data_files"]:
                if os.path.exists(file_path):
                    total_bytes += os.path.getsize(file_path)

        return total_bytes / (1024 ** 3)  # Convert to GB

    async def _prepare_encrypted_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare content for ChaCha20-256 encryption (TrueMark ready)
        """
        # Serialize content
        content_json = json.dumps(content, default=str, separators=(',', ':'))

        # Generate nonce for ChaCha20
        nonce = secrets.token_bytes(16)

        # Encrypt with ChaCha20-256
        cipher = Cipher(algorithms.ChaCha20(self.encryption_key, nonce), mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(content_json.encode()) + encryptor.finalize()

        # Create encryption metadata for TrueMark
        encryption_metadata = {
            "algorithm": "ChaCha20-256",
            "key_hash": hashlib.sha256(self.encryption_key).hexdigest(),
            "nonce": base64.b64encode(nonce).decode(),
            "encrypted_size": len(encrypted_data),
            "original_hash": hashlib.sha256(content_json.encode()).hexdigest(),
            "encryption_timestamp": datetime.utcnow().isoformat(),
            "truemark_ready": True
        }

        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "encryption_metadata": encryption_metadata,
            "decryption_key_available": False  # Key stays with GOAT for now
        }

    async def _generate_nft_metadata(self, user_data: Dict[str, Any], content: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """Generate CertSig-ready NFT metadata"""
        return {
            "name": f"GOAT Legacy NFT: {content.get('title', 'Untitled')}",
            "description": f"Permanent proof of authorship for {product_type}: {content.get('title', 'Untitled')} - created through GOAT's streaming legacy building system",
            "external_url": f"https://goat.gg/legacy/{user_data.get('user_id', 'anonymous')}",
            "attributes": [
                {"trait_type": "Product Type", "value": product_type},
                {"trait_type": "Author", "value": user_data.get('author', 'Anonymous')},
                {"trait_type": "Creation Date", "value": datetime.utcnow().date().isoformat()},
                {"trait_type": "Data Sources", "value": len(user_data.get('data_files', []))},
                {"trait_type": "Content Sections", "value": len(content.get('chapters', content.get('modules', content.get('sections', []))))},
                {"trait_type": "Creator", "value": "GOAT AI"},
                {"trait_type": "Streaming Processed", "value": "Yes"},
                {"trait_type": "Encryption Ready", "value": "ChaCha20-256"}
            ],
            "properties": {
                "product_type": product_type,
                "content_structure": {
                    "title": content.get('title'),
                    "sections": len(content.get('chapters', content.get('modules', content.get('sections', []))))
                },
                "authorship_proof": {
                    "author": user_data.get('author'),
                    "creation_timestamp": datetime.utcnow().isoformat(),
                    "data_integrity_hash": hashlib.sha256(json.dumps(content, default=str).encode()).hexdigest()
                },
                "encryption": {
                    "algorithm": "ChaCha20-256",
                    "truemark_compatible": True
                }
            }
        }

    async def _export_legacy_files_streaming(self, legacy: Dict[str, Any]):
        """Export legacy files with streaming-compatible structure"""
        base_path = self.output_dir / f"{legacy['user_id']}_{legacy['product_type']}_streaming"
        base_path.mkdir(exist_ok=True)

        # Export components (excluding encrypted data for security)
        export_data = legacy.copy()
        if "encrypted_content" in export_data:
            del export_data["encrypted_content"]["encrypted_data"]  # Don't export raw encrypted data

        files_to_export = [
            ("content.json", legacy["content"]),
            ("data_insights.json", legacy["data_insights"]),
            ("nft_metadata.json", legacy["nft_metadata"]),
            ("legacy.json", export_data),
            ("pricing.json", legacy["pricing"])
        ]

        for filename, data in files_to_export:
            with open(base_path / filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)

        # Export content as markdown if it's a book
        if legacy["product_type"] == "book" and "chapters" in legacy["content"]:
            with open(base_path / "book_outline.md", 'w', encoding='utf-8') as f:
                f.write(f"# {legacy['content']['title']}\n\n")
                f.write(f"**Author:** {legacy.get('user_data', {}).get('author', 'Anonymous')}\n\n")
                f.write("## Table of Contents\n\n")
                for chapter in legacy["content"]["chapters"]:
                    f.write(f"{chapter['number']}. {chapter['title']}\n")
                    f.write(f"   - {chapter['content_outline']}\n")
                    f.write(f"   - Estimated pages: {chapter['estimated_pages']}\n\n")

    # Legacy method for backward compatibility
    def build_legacy(self, user_data: Dict[str, Any], product_type: str = "book") -> Dict[str, Any]:
        """Legacy synchronous method - redirects to streaming version"""
        # Run async method in sync context
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run_streaming():
            results = []
            async for update in self.build_legacy_streaming(user_data, product_type):
                results.append(update)
            return results[-1] if results else {}

        result = loop.run_until_complete(run_streaming())
        loop.close()

        return result.get("legacy", {})

    def get_legacy_path(self, user_id: str, product_type: str) -> Path:
        """Get path to exported legacy"""
        return self.output_dir / f"{user_id}_{product_type}_streaming"
    """Builds complete legacies from user data using VisiData analysis"""

    def __init__(self, output_dir: str = "./deliverables/legacy"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_legacy(self, user_data: Dict[str, Any], product_type: str = "book") -> Dict[str, Any]:
        """Build complete legacy product using VisiData analysis"""

        # Analyze user data with VisiData
        data_insights = self._analyze_data_with_visidata(user_data)

        # Generate content based on product type
        if product_type == "book":
            content = self._generate_book_content(user_data, data_insights)
        elif product_type == "course":
            content = self._generate_course_content(user_data, data_insights)
        elif product_type == "masterclass":
            content = self._generate_masterclass_content(user_data, data_insights)
        else:
            content = self._generate_general_content(user_data, data_insights, product_type)

        # Generate NFT metadata
        nft_metadata = self._generate_nft_metadata(user_data, content, product_type)

        legacy = {
            "user_id": user_data.get("user_id", "anonymous"),
            "product_type": product_type,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": "1.0",
            "data_insights": data_insights,
            "content": content,
            "nft_metadata": nft_metadata
        }

        # Export files
        self._export_legacy_files(legacy)

        return legacy

    def _analyze_data_with_visidata(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user data using VisiData for insights"""
        insights = {}

        # Convert user data to DataFrame for analysis
        if "data_files" in user_data:
            for file_path in user_data["data_files"]:
                if os.path.exists(file_path):
                    try:
                        # Load data with VisiData
                        vd_sheet = vd.openSource(file_path)
                        df = vd_sheet.to_pandas()

                        # Basic analysis
                        insights[file_path] = {
                            "row_count": len(df),
                            "column_count": len(df.columns),
                            "columns": list(df.columns),
                            "data_types": df.dtypes.to_dict(),
                            "summary_stats": df.describe().to_dict() if df.select_dtypes(include=[int, float]).shape[1] > 0 else {},
                            "null_counts": df.isnull().sum().to_dict()
                        }

                        # Text analysis if text columns exist
                        text_cols = df.select_dtypes(include=['object']).columns
                        if len(text_cols) > 0:
                            insights[file_path]["text_analysis"] = {}
                            for col in text_cols:
                                text_data = df[col].dropna().astype(str)
                                insights[file_path]["text_analysis"][col] = {
                                    "unique_values": text_data.nunique(),
                                    "avg_length": text_data.str.len().mean(),
                                    "word_count": text_data.str.split().str.len().sum()
                                }

                    except Exception as e:
                        insights[file_path] = {"error": str(e)}

        return insights

    def _generate_book_content(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate book content structure"""
        return {
            "title": user_data.get("title", "Untitled Book"),
            "chapters": self._structure_chapters(user_data, insights),
            "foreword": f"This book represents the greatest work of {user_data.get('author', 'the author')}.",
            "estimated_pages": len(insights) * 10 + 50,  # Rough estimate
            "key_themes": self._extract_themes(insights)
        }

    def _generate_course_content(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate course content structure"""
        return {
            "title": user_data.get("title", "Untitled Course"),
            "modules": self._structure_modules(user_data, insights),
            "duration_hours": len(insights) * 2,
            "learning_objectives": self._extract_objectives(insights),
            "prerequisites": user_data.get("prerequisites", [])
        }

    def _generate_masterclass_content(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate masterclass content structure"""
        return {
            "title": user_data.get("title", "Untitled Masterclass"),
            "sessions": self._structure_sessions(user_data, insights),
            "duration_hours": len(insights) * 3,
            "expertise_level": "Advanced",
            "key_takeaways": self._extract_takeaways(insights)
        }

    def _generate_general_content(self, user_data: Dict[str, Any], insights: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """Generate general content structure"""
        return {
            "title": user_data.get("title", f"Untitled {product_type.title()}"),
            "sections": self._structure_sections(user_data, insights, product_type),
            "content_type": product_type,
            "insights_summary": self._summarize_insights(insights)
        }

    def _structure_chapters(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Structure book chapters based on data insights"""
        chapters = []
        themes = self._extract_themes(insights)

        for i, theme in enumerate(themes[:10]):  # Limit to 10 chapters
            chapters.append({
                "number": i + 1,
                "title": f"Chapter {i+1}: {theme.title()}",
                "content_outline": f"Exploring {theme} based on data analysis",
                "estimated_pages": 15
            })

        return chapters

    def _structure_modules(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Structure course modules"""
        modules = []
        objectives = self._extract_objectives(insights)

        for i, objective in enumerate(objectives[:8]):
            modules.append({
                "number": i + 1,
                "title": f"Module {i+1}: {objective}",
                "lessons": ["Introduction", "Core Concepts", "Practice", "Assessment"],
                "duration_hours": 2
            })

        return modules

    def _structure_sessions(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Structure masterclass sessions"""
        sessions = []
        takeaways = self._extract_takeaways(insights)

        for i, takeaway in enumerate(takeaways[:6]):
            sessions.append({
                "number": i + 1,
                "title": f"Session {i+1}: {takeaway}",
                "duration_hours": 1.5,
                "format": "Interactive Workshop"
            })

        return sessions

    def _structure_sections(self, user_data: Dict[str, Any], insights: Dict[str, Any], product_type: str) -> List[Dict[str, Any]]:
        """Structure general sections"""
        sections = []
        summary = self._summarize_insights(insights)

        for i, key_point in enumerate(summary.get("key_points", [])[:5]):
            sections.append({
                "number": i + 1,
                "title": f"Section {i+1}: {key_point}",
                "content_type": product_type
            })

        return sections

    def _extract_themes(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key themes from insights"""
        themes = []
        for file_insights in insights.values():
            if isinstance(file_insights, dict) and "columns" in file_insights:
                themes.extend([col.replace("_", " ").title() for col in file_insights["columns"][:3]])

        # Remove duplicates and limit
        return list(set(themes))[:5] if themes else ["Introduction", "Core Concepts", "Advanced Topics", "Conclusion", "Appendices"]

    def _extract_objectives(self, insights: Dict[str, Any]) -> List[str]:
        """Extract learning objectives"""
        return ["Understand core concepts", "Apply knowledge practically", "Master advanced techniques", "Create original work", "Teach others"]

    def _extract_takeaways(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key takeaways"""
        return ["Master the fundamentals", "Develop expert techniques", "Build practical skills", "Create lasting value", "Inspire others"]

    def _summarize_insights(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize data insights"""
        total_files = len(insights)
        total_rows = sum([f.get("row_count", 0) for f in insights.values() if isinstance(f, dict)])

        return {
            "total_files_analyzed": total_files,
            "total_data_points": total_rows,
            "key_points": ["Data-driven insights", "Structured knowledge", "Actionable intelligence"],
            "recommendations": ["Focus on quality over quantity", "Structure content logically", "Include practical examples"]
        }

    def _generate_nft_metadata(self, user_data: Dict[str, Any], content: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """Generate CertSig-ready NFT metadata"""
        return {
            "name": f"GOAT Legacy NFT: {content.get('title', 'Untitled')}",
            "description": f"Permanent proof of authorship for {product_type}: {content.get('title', 'Untitled')} - created through GOAT's legacy building system",
            "external_url": f"https://goat.gg/legacy/{user_data.get('user_id', 'anonymous')}",
            "attributes": [
                {"trait_type": "Product Type", "value": product_type},
                {"trait_type": "Author", "value": user_data.get('author', 'Anonymous')},
                {"trait_type": "Creation Date", "value": datetime.utcnow().date().isoformat()},
                {"trait_type": "Data Sources", "value": len(user_data.get('data_files', []))},
                {"trait_type": "Content Sections", "value": len(content.get('chapters', content.get('modules', content.get('sections', []))))},
                {"trait_type": "Creator", "value": "GOAT AI"}
            ],
            "properties": {
                "product_type": product_type,
                "content_structure": {
                    "title": content.get('title'),
                    "sections": len(content.get('chapters', content.get('modules', content.get('sections', []))))
                },
                "authorship_proof": {
                    "author": user_data.get('author'),
                    "creation_timestamp": datetime.utcnow().isoformat(),
                    "data_integrity_hash": "placeholder_hash"  # Would be actual hash
                }
            }
        }

    def _export_legacy_files(self, legacy: Dict[str, Any]):
        """Export legacy as individual files"""
        base_path = self.output_dir / f"{legacy['user_id']}_{legacy['product_type']}"
        base_path.mkdir(exist_ok=True)

        # Export each component
        files_to_export = [
            ("content.json", legacy["content"]),
            ("data_insights.json", legacy["data_insights"]),
            ("nft_metadata.json", legacy["nft_metadata"]),
            ("legacy.json", legacy)
        ]

        for filename, data in files_to_export:
            with open(base_path / filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)

        # Export content as markdown if it's a book
        if legacy["product_type"] == "book" and "chapters" in legacy["content"]:
            with open(base_path / "book_outline.md", 'w') as f:
                f.write(f"# {legacy['content']['title']}\n\n")
                f.write(f"**Author:** {legacy.get('user_data', {}).get('author', 'Anonymous')}\n\n")
                f.write("## Table of Contents\n\n")
                for chapter in legacy["content"]["chapters"]:
                    f.write(f"{chapter['number']}. {chapter['title']}\n")

    def get_legacy_path(self, user_id: str, product_type: str) -> Path:
        """Get path to exported legacy"""
        return self.output_dir / f"{user_id}_{product_type}"