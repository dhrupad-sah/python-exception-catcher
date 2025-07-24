#!/usr/bin/env python3
"""Flask example with Mira Sentinel exception catching."""

import os
import sys
import asyncio

# Add the source directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from flask import Flask, jsonify
    from exception_catcher import setup_flask_mira_sentinel, MiraSentinelConfig
    
    app = Flask(__name__)
    
    # Configuration
    config = MiraSentinelConfig(
        sentinel_url=os.getenv("MIRA_SENTINEL_URL", "https://your-sentinel.com"),
        service_name=os.getenv("MIRA_SERVICE_NAME", "flask-example"),
        repo=os.getenv("MIRA_REPO", "company/flask-example")
    )
    
    # Set up Mira Sentinel
    sentinel = setup_flask_mira_sentinel(
        app,
        config,
        include_headers=True,
        skip_status_codes=[400, 401, 403, 404],
        extract_request_context=lambda request: {
            "user_id": request.headers.get("X-User-ID"),
            "session_id": request.headers.get("X-Session-ID")
        }
    )
    
    @app.route("/")
    def root():
        return jsonify({"message": "Flask Exception Catcher Example"})
    
    @app.route("/error")
    def trigger_error():
        """Route that will trigger an exception."""
        raise Exception("This is a test exception from Flask!")
    
    @app.route("/users/<int:user_id>")
    def get_user(user_id):
        """Simulate user lookup that might fail."""
        if user_id == 404:
            raise ValueError(f"User {user_id} not found")
        
        return jsonify({"user_id": user_id, "name": f"User {user_id}"})
    
    @app.route("/manual-report")
    def manual_report():
        """Example of manual exception reporting."""
        try:
            # Simulate some risky operation
            if True:  # This will always trigger
                raise RuntimeError("Manually reported exception")
        except Exception as error:
            # Report to Mira Sentinel (Flask integration runs async in sync context)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(
                    app.mira_sentinel.report_exception(error, {
                        "context": {"operation": "manual_test"},
                        "tags": ["manual", "test"],
                        "severity": "medium"
                    })
                )
            finally:
                loop.close()
            
            # Return error response
            return jsonify({"error": "Operation failed", "reported": True}), 500
    
    if __name__ == "__main__":
        print("🚀 Starting Flask with Mira Sentinel Exception Catcher")
        print("📡 Try these endpoints:")
        print("  - GET http://localhost:5000/ (normal)")
        print("  - GET http://localhost:5000/error (automatic exception)")
        print("  - GET http://localhost:5000/users/404 (user not found)")
        print("  - GET http://localhost:5000/manual-report (manual reporting)")
        
        app.run(host="0.0.0.0", port=5000, debug=True)

except ImportError as e:
    print(f"❌ Flask not available: {e}")
    print("Install with: pip install flask")
    print("Or with PDM: pdm add flask")