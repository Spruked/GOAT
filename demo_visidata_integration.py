#!/usr/bin/env python3
"""
GOAT VisiData Integration Demo
Showcases the 3 priority features:
1. Content Archaeology Engine (treasure hunting)
2. Zero-Crypto Storage (Save Forever button)
3. Smart Structure Assistant (template matching)
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, Any, List
import tempfile

# Import our new services
from services.content_archaeology_service import content_archaeology_service
from services.permanent_storage_service import permanent_storage_service
from services.structure_assistant_service import structure_assistant_service
from services.encryption_service import encryption_service
from services.pricing_service import pricing_service
from learning.legacy_builder import GOATLegacyBuilder

class GOATVisiDataDemo:
    """
    Demo showcasing GOAT's VisiData-powered features
    """

    def __init__(self):
        self.demo_data_dir = Path("./demo_data")
        self.demo_data_dir.mkdir(exist_ok=True)

        # Initialize services
        permanent_storage_service.encryption_service = encryption_service

    async def run_full_demo(self):
        """
        Run complete demo of all 3 priority features
        """
        print("🚀 GOAT VisiData Integration Demo")
        print("=" * 50)

        # Create sample data files
        sample_files = await self._create_sample_data()

        print(f"📁 Created {len(sample_files)} sample data files")

        # Feature 1: Content Archaeology Engine
        print("\n🔍 FEATURE 1: Content Archaeology Engine")
        print("-" * 40)

        archaeology_results = await content_archaeology_service.analyze_upload_for_gems(sample_files)

        print(f"📊 Scanned {archaeology_results['total_files_scanned']} files")
        print(f"💎 Found {len(archaeology_results['hidden_gems'])} hidden gems")

        if archaeology_results['hidden_gems']:
            print("\n🎯 Top Hidden Gems:")
            for i, gem in enumerate(archaeology_results['hidden_gems'][:3], 1):
                print(f"  {i}. {gem['type'].title()}: {gem['content'][:60]}...")
                print(".1%")

        # Generate narrative reconstruction
        if archaeology_results['hidden_gems']:
            reconstruction = content_archaeology_service.generate_narrative_reconstruction(
                archaeology_results['hidden_gems']
            )
            print("
📖 Suggested Book Title: {reconstruction['suggested_title']}")
            print(f"📑 Chapter Outline ({len(reconstruction['chapter_outline'])} chapters)")

        # Feature 2: Smart Structure Assistant
        print("\n🏗️  FEATURE 2: Smart Structure Assistant")
        print("-" * 40)

        structure_suggestion = await structure_assistant_service.analyze_and_suggest_structure(
            sample_files,
            user_intent="Create a comprehensive guide for entrepreneurs"
        )

        recommended = structure_suggestion['recommended_structure']
        print(f"🎯 Recommended Structure: {recommended['name']}")
        print(f"📝 Description: {recommended['description']}")
        print(".1%")
        print(f"💡 Why: {recommended['why_this_structure']}")

        print("\n📑 Suggested Chapter Structure:")
        for i, chapter in enumerate(recommended['structure'][:5], 1):
            print(f"  {i}. {chapter}")

        # Feature 3: Zero-Crypto Storage
        print("\n💾 FEATURE 3: Zero-Crypto Storage ('Save Forever')")
        print("-" * 40)

        # Create sample legacy content
        sample_content = {
            "title": "The Entrepreneur's Journey",
            "author": "Demo User",
            "content": "This is a sample legacy created from data analysis...",
            "structure": recommended['structure'],
            "gems_found": len(archaeology_results['hidden_gems']),
            "created_at": "2025-01-27T12:00:00Z"
        }

        # Calculate pricing
        pricing = pricing_service.calculate_total_cost(
            data_size_gb=2.5,  # Sample data size
            output_formats=2,  # Book + Course
            permanent_storage=True
        )

        print("💰 Cost Breakdown:")
        print(f"  Data Processing (2.5GB): ${pricing['processing']['processing_cost']:.2f}")
        print(f"  Output Formats (2): ${pricing['processing']['format_cost']:.2f}")
        print(f"  Permanent Storage: ${pricing['storage']['storage_cost']:.2f}")
        print(f"  Total: ${pricing['total_cost']:.2f}")

        # "Save Forever" simulation
        print("\n🔒 Saving Forever...")
        storage_result = await permanent_storage_service.save_forever(
            sample_content,
            user_id="demo_user",
            content_type="legacy"
        )

        if storage_result['success']:
            print("✅ Content saved permanently!")
            print(f"🔗 Permanent Link: {storage_result['permanent_link']}")
            print(f"🌐 Full URL: {storage_result['full_url']}")
            print(f"💬 User Message: {storage_result['user_message']}")

            # Show technical details (normally hidden from user)
            tech = storage_result['technical_details']
            print("
🔧 Technical Details (hidden from user):"            print(f"  IPFS Hash: {tech['ipfs_hash'][:16]}...")
            print(f"  Arweave TX: {tech['arweave_tx'][:16]}...")
            print(f"  Encryption: {tech['encryption']}")
            print(f"  TrueMark Ready: {tech['truemark_ready']}")
        else:
            print(f"❌ Storage failed: {storage_result.get('error', 'Unknown error')}")

        # Feature 4: Production Legacy Builder
        print("\n⚡ BONUS: Production Legacy Builder")
        print("-" * 40)

        builder = GOATLegacyBuilder()
        print("🏗️ Building legacy with streaming VisiData analysis...")

        progress_updates = []
        async for update in builder.build_legacy_streaming(
            user_data={
                "user_id": "demo_user",
                "title": "Entrepreneur's Data-Driven Legacy",
                "data_files": sample_files,
                "author": "Demo User"
            },
            product_type="book"
        ):
            progress_updates.append(update)
            print(f"📊 {update['message']} ({update['progress']}%)")

        if progress_updates and progress_updates[-1]['status'] == 'complete':
            final_result = progress_updates[-1]['legacy']
            print("✅ Legacy built successfully!")
            print(f"📖 Title: {final_result['content']['title']}")
            print(f"📚 Chapters: {len(final_result['content']['chapters'])}")
            print(f"💰 Cost: ${final_result['pricing']['processing_cost']:.2f} + ${final_result['pricing']['permanent_storage_cost']:.2f} storage")
            print(f"🔒 Encrypted: {final_result['encrypted_content']['encryption_metadata']['truemark_ready']}")

        print("\n🎉 Demo Complete!")
        print("=" * 50)
        print("These features work without UCM, voice, or minting - pure VisiData power!")

    async def _create_sample_data(self) -> List[str]:
        """
        Create sample data files for demo
        """
        sample_files = []

        # Sample 1: Business data with insights
        business_data = [
            ["Month", "Revenue", "Customers", "Key_Event"],
            ["Jan", "15000", "45", "Product launch"],
            ["Feb", "22000", "67", "First big sale - 40% above target!"],
            ["Mar", "18000", "52", "Market expansion begins"],
            ["Apr", "35000", "89", "Unexpected viral marketing success"],
            ["May", "28000", "71", "Strategic partnership formed"],
            ["Jun", "42000", "105", "Breakthrough quarter - how did we do it?"]
        ]

        business_file = self.demo_data_dir / "business_performance.csv"
        with open(business_file, 'w') as f:
            for row in business_data:
                f.write(','.join(str(cell) for cell in row) + '\n')
        sample_files.append(str(business_file))

        # Sample 2: Content notes with unfinished thoughts
        content_notes = [
            ["Topic", "Notes", "Status"],
            ["Marketing Strategy", "The key insight is that we need to stop thinking about features and start thinking about transformations. How do we change lives?", "unfinished"],
            ["Customer Journey", "They come in confused, leave empowered. But what happens in the middle? The messy middle where real change occurs.", "draft"],
            ["Product Vision", "This isn't just software. It's a catalyst for human potential. Every feature should answer: does this unlock human capability?", "complete"],
            ["Market Opportunity", "The real opportunity isn't in our category. It's in becoming the platform where our category evolves. But how?", "question"],
            ["Team Culture", "Culture eats strategy for breakfast. But what if culture could BE the strategy? Revolutionary thought.", "insight"]
        ]

        notes_file = self.demo_data_dir / "content_notes.csv"
        with open(notes_file, 'w') as f:
            for row in content_notes:
                f.write(','.join(f'"{cell}"' for cell in row) + '\n')
        sample_files.append(str(notes_file))

        # Sample 3: Research data
        research_data = [
            ["Study", "Finding", "Implication"],
            ["User Interviews", "Users don't want features, they want outcomes", "This changes everything about product development"],
            ["Competitive Analysis", "No one in our space is actually solving the real problem", "Massive white space opportunity"],
            ["Market Research", "The addressable market is 3x larger than we thought", "We need to expand our vision dramatically"],
            ["Technical Feasibility", "The technology exists today to do what we only dreamed of", "No technical barriers remain"]
        ]

        research_file = self.demo_data_dir / "market_research.csv"
        with open(research_file, 'w') as f:
            for row in research_data:
                f.write(','.join(f'"{cell}"' for cell in row) + '\n')
        sample_files.append(str(research_file))

        return sample_files

async def main():
    """Run the demo"""
    demo = GOATVisiDataDemo()
    await demo.run_full_demo()

if __name__ == "__main__":
    asyncio.run(main())