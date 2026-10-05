import argparse
import os
import sys
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.app import app

# Mount static dist files if dist directory exists
frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Serve API routes via router (handled automatically prior to catch-all)
        if full_path.startswith("api"):
            return None
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


def main():
    parser = argparse.ArgumentParser(description="TraceLab Server")
    parser.add_argument("--dev", action="store_true", help="Run in dev mode (API only)")
    parser.add_argument("--host", default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("                      TRACELAB v2.0")
    print("   Interactive Data Structures & Algorithms Laboratory")
    print("=" * 60)
    if args.dev:
        print(f" Development API running at http://{args.host}:{args.port}")
    else:
        print(f" Application running at http://{args.host}:{args.port}")
    print("=" * 60)
    print()

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()