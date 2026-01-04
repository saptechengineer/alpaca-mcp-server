import os
from alpaca_mcp_server.server import mcp

class HostOverrideMiddleware:
    """Middleware to override host header for proxy deployments"""
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Replace host header to pass MCP SDK validation
            headers = list(scope.get("headers", []))
            new_headers = []
            for name, value in headers:
                if name == b"host":
                    new_headers.append((name, b"localhost:8000"))
                else:
                    new_headers.append((name, value))
            scope["headers"] = new_headers
        
        await self.app(scope, receive, send)

# Wrap the MCP app with host override middleware
_original_app = mcp.streamable_http_app()
app = HostOverrideMiddleware(_original_app)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "start:app",
        host="0.0.0.0",
        port=port,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )