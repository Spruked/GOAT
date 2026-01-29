#!/usr/bin/env python3
"""
GOAT Premium Services Test Script
Tests all premium services to ensure they work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.apex_doc_service import premium_apex_doc_service
from services.content_archaeology_service import premium_content_archaeology_service
from services.structure_assistant_service import premium_structure_assistant_service
from services.zero_friction_storage_service import premium_zero_friction_storage_service
from services.export_concierge_service import premium_export_concierge_service

def test_premium_services():
    print('🔍 Testing GOAT Premium Services...')
    print()

    results = []

    # Test APEX DOC service
    print('1. Testing APEX DOC Service...')
    try:
        result = premium_apex_doc_service.generate_apex_certificate('test_content', 'test_user', 'legacy')
        layers = len(result.get("certificate_layers", []))
        print(f'   ✅ APEX DOC: Generated certificate with {layers} layers')
        results.append(f"APEX DOC: {layers} layers")
    except Exception as e:
        print(f'   ❌ APEX DOC: {e}')
        results.append(f"APEX DOC: FAILED - {e}")

    # Test Content Archaeology
    print('2. Testing Content Archaeology Service...')
    try:
        result = premium_content_archaeology_service.analyze_multi_file_intelligence(['README.md'], {})
        files = result.get("files_analyzed", 0)
        print(f'   ✅ Archaeology: Analyzed {files} files')
        results.append(f"Archaeology: {files} files")
    except Exception as e:
        print(f'   ❌ Archaeology: {e}')
        results.append(f"Archaeology: FAILED - {e}")

    # Test Structure Assistant
    print('3. Testing Structure Assistant Service...')
    try:
        result = premium_structure_assistant_service.analyze_content_structure('Test content for structure analysis', 'article')
        framework = result.get("framework_recommendation", {}).get("recommended_framework", "unknown")
        print(f'   ✅ Structure: Recommended {framework} framework')
        results.append(f"Structure: {framework}")
    except Exception as e:
        print(f'   ❌ Structure: {e}')
        results.append(f"Structure: FAILED - {e}")

    # Test Zero-Friction Storage
    print('4. Testing Zero-Friction Storage Service...')
    try:
        result = premium_zero_friction_storage_service.store_content_zero_friction('Test content', 'text', 'test_user', 'scholar')
        operation = result.get("operation", "unknown")
        print(f'   ✅ Storage: {operation} content successfully')
        results.append(f"Storage: {operation}")
    except Exception as e:
        print(f'   ❌ Storage: {e}')
        results.append(f"Storage: FAILED - {e}")

    # Test Export Concierge
    print('5. Testing Export Concierge Service...')
    try:
        result = premium_export_concierge_service.export_content_intelligently('Test content', {'title': 'Test'}, 'blog_post', ['markdown'], 'test_user', 'professional')
        formats = result.get("formats_exported", 0)
        print(f'   ✅ Export: Exported to {formats} formats')
        results.append(f"Export: {formats} formats")
    except Exception as e:
        print(f'   ❌ Export: {e}')
        results.append(f"Export: FAILED - {e}")

    print()
    print('🎉 GOAT Premium Services test completed!')
    print()

    # Summary
    print('📊 Test Summary:')
    for result in results:
        print(f'   • {result}')

    return results

if __name__ == "__main__":
    test_premium_services()