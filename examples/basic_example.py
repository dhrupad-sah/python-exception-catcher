#!/usr/bin/env python3
"""Basic example with Mira Sentinel exception catching."""

import os
import sys
import asyncio
import time

# Add the source directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from exception_catcher import MiraSentinelExceptionCatcher, MiraSentinelConfig, auto_initialize


async def main():
    print("🚀 Basic Mira Sentinel Exception Catcher Example")
    
    # Method 1: Manual configuration
    print("\n📝 Method 1: Manual Configuration")
    config = MiraSentinelConfig(
        sentinel_url=os.getenv("MIRA_SENTINEL_URL", "https://your-sentinel.com"),
        service_name="basic-python-example",
        repo="company/basic-python-example"
    )
    
    catcher = MiraSentinelExceptionCatcher(config)
    
    # Set up custom error filtering
    catcher.set_error_filter(lambda error: "test" not in str(error).lower())
    
    # Set up custom context enrichment
    catcher.set_context_enricher(lambda error, context: {
        "example_id": "basic-001",
        "environment": "development"
    })
    
    catcher.initialize()
    print("✅ Exception catcher initialized")
    
    # Test connection
    print("\n📡 Testing connection...")
    try:
        connected = await catcher.test_connection()
        print(f"Connection result: {connected}")
    except Exception as e:
        print(f"⚠️ Connection test failed (expected): {e}")
    
    # Test manual exception reporting
    print("\n📝 Testing manual exception reporting...")
    try:
        test_error = Exception("This is a manually reported test exception")
        await catcher.report_exception(test_error, {
            "context": {"operation": "manual_test"},
            "tags": ["manual", "example"],
            "severity": "low"
        })
        print("✅ Manual exception reported")
    except Exception as e:
        print(f"⚠️ Manual reporting failed (expected): {e}")
    
    print("\n🎯 Triggering automatic exception catching...")
    print("In 3 seconds, an exception will be thrown and automatically caught...")
    
    # Wait a bit to show the delay
    await asyncio.sleep(3)
    
    # This exception will be caught automatically by the global handler
    try:
        # This will trigger the global exception handler
        raise RuntimeError("This is an automatically caught exception!")
    except Exception:
        # Even though we catch it here, it was already processed by our handler
        print("Exception was thrown and should have been caught by Mira Sentinel")
    
    # Method 2: Auto-initialization
    print("\n📝 Method 2: Auto-initialization (Environment Variables)")
    auto_catcher = auto_initialize()
    if auto_catcher:
        print("✅ Auto-initialization succeeded")
    else:
        print("⚠️ Auto-initialization skipped (no environment variables set)")
    
    # Cleanup
    print("\n🧹 Shutting down...")
    catcher.shutdown()
    print("✅ Exception catcher shut down")
    
    print("\n🎉 Example completed!")
    print("\n💡 To see real exception reporting:")
    print("1. Set up a Mira Sentinel instance")
    print("2. Set MIRA_SENTINEL_URL environment variable")  
    print("3. Run this script again")


def sync_example():
    """Example of using the exception catcher in a synchronous context."""
    print("\n🔄 Synchronous Example")
    
    # This will be caught by the global exception handler if initialized
    def risky_function():
        if True:  # Always trigger
            raise ValueError("This exception from sync code will be caught!")
    
    try:
        risky_function()
    except Exception as e:
        print(f"Caught locally: {e}")


if __name__ == "__main__":
    # Run the async example
    asyncio.run(main())
    
    # Run the sync example
    sync_example()
    
    print("\n✨ All examples completed!")