#!/usr/bin/env python3
"""Basic test script for the Python exception catcher."""

import asyncio
import sys
import os

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from exception_catcher import MiraSentinelExceptionCatcher, MiraSentinelConfig, auto_initialize


async def test_basic_functionality():
    """Test basic functionality."""
    print("🧪 Testing Python Exception Catcher")
    
    # Test 1: Basic configuration
    print("\n1. Testing basic configuration...")
    config = MiraSentinelConfig(
        sentinel_url="https://test-sentinel.com",
        service_name="test-python-service",
        repo="test/test-repo"
    )
    
    catcher = MiraSentinelExceptionCatcher(config)
    print("✅ Exception catcher created successfully")
    
    # Test 2: Initialization
    print("\n2. Testing initialization...")
    catcher.initialize()
    print("✅ Exception catcher initialized")
    
    # Test 3: Connection test (will fail but should not crash)
    print("\n3. Testing connection (expected to fail)...")
    try:
        connected = await catcher.test_connection()
        print(f"📡 Connection result: {connected}")
    except Exception as e:
        print(f"⚠️ Connection test failed as expected: {e}")
    
    # Test 4: Manual exception reporting (will fail but should not crash)
    print("\n4. Testing manual exception reporting...")
    try:
        test_error = Exception("Test exception for reporting")
        await catcher.report_exception(test_error)
    except Exception as e:
        print(f"⚠️ Report failed as expected: {e}")
    
    # Test 5: Auto-initialization (should fail due to missing env vars)
    print("\n5. Testing auto-initialization...")
    auto_catcher = auto_initialize()
    if auto_catcher:
        print("✅ Auto-initialization succeeded")
    else:
        print("⚠️ Auto-initialization skipped (expected - no env vars)")
    
    # Test 6: Shutdown
    print("\n6. Testing shutdown...")
    catcher.shutdown()
    print("✅ Exception catcher shut down")
    
    print("\n🎉 All basic tests completed!")


async def test_fastapi_integration():
    """Test FastAPI integration if available."""
    print("\n🧪 Testing FastAPI Integration")
    
    try:
        from exception_catcher import setup_fastapi_mira_sentinel
        print("✅ FastAPI integration imported successfully")
        
        # We can't actually test the full integration without FastAPI app,
        # but we can verify the import works
        
    except ImportError as e:
        print(f"⚠️ FastAPI integration not available: {e}")


async def test_flask_integration():
    """Test Flask integration if available."""
    print("\n🧪 Testing Flask Integration")
    
    try:
        from exception_catcher import setup_flask_mira_sentinel
        print("✅ Flask integration imported successfully")
        
    except ImportError as e:
        print(f"⚠️ Flask integration not available: {e}")


if __name__ == "__main__":
    print("🚀 Starting Python Exception Catcher Tests")
    
    # Run tests
    asyncio.run(test_basic_functionality())
    asyncio.run(test_fastapi_integration())
    asyncio.run(test_flask_integration())
    
    print("\n✨ Test script completed!")