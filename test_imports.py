#!/usr/bin/env python3
"""
Simple import test for GOAT Premium Services
"""

import sys
import os

def test_imports():
    print('🔍 Testing GOAT Premium Services Imports...')
    print()

    services = [
        'services.apex_doc_service',
        'services.content_archaeology_service',
        'services.structure_assistant_service',
        'services.zero_friction_storage_service',
        'services.export_concierge_service'
    ]

    results = []

    for service in services:
        try:
            module = __import__(service, fromlist=[''])
            print(f'   ✅ {service}: Imported successfully')
            results.append(f"{service}: OK")
        except Exception as e:
            print(f'   ❌ {service}: {e}')
            results.append(f"{service}: FAILED - {e}")

    print()
    print('📊 Import Test Summary:')
    for result in results:
        print(f'   • {result}')

    return results

if __name__ == "__main__":
    test_imports()