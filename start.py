import os
import uvicorn
from alpaca_mcp_server.server import mcp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        mcp.streamable_http_app(),
        host="0.0.0.0",
        port=port,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )