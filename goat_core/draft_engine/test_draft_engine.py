#!/usr/bin/env python3
"""
GOAT Draft Engine - Test Script
Demonstrates the complete ScribeCore v1 pipeline
"""

import sys
import os
from pathlib import Path

# Add the draft engine to path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules directly
from .structure_interpreter import StructureInterpreter
from .content_generator import ContentGenerator
from continuity_manager import ContinuityManager
from tone_harmonizer import ToneHarmonizer
from quality_validator import QualityValidator
from draft_pipeline import DraftPipeline, generate_goat_content

def test_draft_engine():
    """Test the draft engine with sample content"""

    # Sample book outline
    book_outline = """
I. Introduction
   A. The Legacy Builder Philosophy
   B. Why GOAT Matters
   C. What You'll Learn

II. Core Principles
   A. Understanding Your Audience
   B. Content Structure Fundamentals
   C. The Power of Consistency

III. Practical Applications
   A. Building Your First Book
   B. Course Creation Strategies
   C. Framework Development

IV. Advanced Techniques
   A. Scaling Your Content
   B. Monetization Strategies
   C. Building a Legacy

V. Conclusion
   A. Taking Action
   B. Your Journey Begins
   C. Final Thoughts
"""

    print("🚀 Starting GOAT Draft Engine Test")
    print("=" * 50)

    try:
        # Generate content
        results = generate_goat_content(
            outline_text=book_outline,
            content_type="book",
            project_title="The GOAT Legacy Builder's Guide"
        )

        print(f"✅ Generation completed in {results['generation_time']:.1f} seconds")
        print(f"📊 Generated {results['metadata']['total_sections']} sections")
        print(f"📝 Total words: {results['metadata']['total_words']}")
        print(f"⭐ Average quality score: {results['metadata']['avg_quality_score']:.1f}/10")

        if results['errors']:
            print(f"⚠️  {len(results['errors'])} errors encountered:")
            for error in results['errors'][:3]:  # Show first 3
                print(f"   - {error}")

        # Save results
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)

        # Save full results
        results_file = output_dir / "generation_results.json"
        from draft_pipeline import DraftPipeline
        pipeline = DraftPipeline()
        pipeline.save_results(results, str(results_file))

        # Export to markdown
        markdown_file = output_dir / "generated_content.md"
        pipeline.export_to_markdown(results, str(markdown_file))

        print(f"\n💾 Results saved to: {results_file}")
        print(f"📄 Content exported to: {markdown_file}")

        # Show content preview
        content = results.get('final_content', '')
        if content:
            print("\n📖 Content Preview (first 500 chars):")
            print("-" * 30)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("-" * 30)

        print("\n🎉 GOAT Draft Engine test completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_draft_engine()