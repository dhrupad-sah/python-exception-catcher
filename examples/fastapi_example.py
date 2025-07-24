#!/usr/bin/env python3
"""FastAPI example with Mira Sentinel exception catching."""

import os
import sys

# Add the source directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from fastapi import FastAPI
    from exception_catcher import setup_fastapi_mira_sentinel, MiraSentinelConfig
    
    app = FastAPI(title="FastAPI Exception Catcher Example")
    
    # Configuration
    config = MiraSentinelConfig(
        sentinel_url=os.getenv("MIRA_SENTINEL_URL", "https://your-sentinel.com"),
        service_name=os.getenv("MIRA_SERVICE_NAME", "fastapi-example"),
        repo=os.getenv("MIRA_REPO", "company/fastapi-example")
    )
    
    # Set up Mira Sentinel
    sentinel = setup_fastapi_mira_sentinel(
        app,
        config,
        skip_status_codes=[400, 401, 403, 404],
        extract_request_context=lambda request: {
            "user_id": request.headers.get("x-user-id"),
            "trace_id": request.headers.get("x-trace-id")
        }
    )
    
    @app.get("/")
    async def root():
        return {"message": "FastAPI Exception Catcher Example"}
    
    @app.get("/error")
    async def trigger_error():
        """Route that will trigger an exception."""
        raise Exception("This is a test exception from FastAPI!")
    
    @app.get("/users/{user_id}")
    async def get_user(user_id: int):
        """Simulate user lookup that might fail."""
        if user_id == 404:
            raise ValueError(f"User {user_id} not found")
        
        return {"user_id": user_id, "name": f"User {user_id}"}
    
    @app.get("/manual-report")
    async def manual_report():
        """Example of manual exception reporting."""
        try:
            # Simulate some risky operation
            if True:  # This will always trigger
                raise RuntimeError("Manually reported exception")
        except Exception as error:
            # Report to Mira Sentinel
            await app.state.mira_sentinel.report_exception(error, {
                "context": {"operation": "manual_test"},
                "tags": ["manual", "test"],
                "severity": "medium"
            })
            # Return error response
            return {"error": "Operation failed", "reported": True}
    
    if __name__ == "__main__":
        import uvicorn
        print("🚀 Starting FastAPI with Mira Sentinel Exception Catcher")
        print("📡 Try these endpoints:")
        print("  - GET http://localhost:8000/ (normal)")
        print("  - GET http://localhost:8000/error (automatic exception)")
        print("  - GET http://localhost:8000/users/404 (user not found)")
        print("  - GET http://localhost:8000/manual-report (manual reporting)")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)

except ImportError as e:
    print(f"❌ FastAPI not available: {e}")
    print("Install with: pip install fastapi uvicorn")
    print("Or with PDM: pdm add fastapi uvicorn")