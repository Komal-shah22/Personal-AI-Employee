#!/usr/bin/env python3
"""
Simple test to identify where Unicode character is causing issues
"""
import os
import sys
from pathlib import Path

# Add the dashboard directory to the path so we can import our modules
dashboard_path = Path("ai-employee-dashboard")
sys.path.insert(0, str(dashboard_path))

def test_individual_functions():
    print("Testing individual functions...")

    # Test loading the modules one by one
    print("\\n1. Testing post_linkedin_direct import...")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("post_linkedin_direct",
                                                     dashboard_path / "post_linkedin_direct.py")
        post_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(post_module)
        print("   [OK] Module imported successfully")
    except Exception as e:
        print(f"   [FAIL] Error importing: {e}")
        return

    print("\\n2. Testing create_linkedin_token import...")
    try:
        spec = importlib.util.spec_from_file_location("create_linkedin_token",
                                                     dashboard_path / "create_linkedin_token.py")
        token_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(token_module)
        print("   [OK] Module imported successfully")

        # Test the get_linkedin_access_token function
        print("   Testing get_linkedin_access_token...")
        if hasattr(token_module, 'get_linkedin_access_token'):
            try:
                token = token_module.get_linkedin_access_token()
                print(f"   [OK] Function works, token: {str(token)[:20]}...")
            except Exception as e:
                print(f"   [FAIL] Function error: {e}")
        else:
            print("   [FAIL] Function not found")
    except Exception as e:
        print(f"   [FAIL] Error importing: {e}")
        return

    print("\\n3. Testing update_linkedin_integration import...")
    try:
        spec = importlib.util.spec_from_file_location("update_linkedin_integration",
                                                     dashboard_path / "update_linkedin_integration.py")
        update_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(update_module)
        print("   [OK] Module imported successfully")
    except Exception as e:
        print(f"   [FAIL] Error importing: {e}")
        return

    print("\\n4. Testing integration with LinkedIn class...")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("linkedin_integration",
                                                     ".claude/mcp-servers/social-mcp/linkedin_integration.py")
        li_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(li_module)
        print("   [OK] LinkedIn integration module imported successfully")
    except Exception as e:
        print(f"   [FAIL] Error importing LinkedIn integration: {e}")
        return

if __name__ == "__main__":
    test_individual_functions()