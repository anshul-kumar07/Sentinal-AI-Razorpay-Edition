"""
Sentinel AI 2.0 - Vercel Serverless Entry Point
Includes WSGI path normalizer for Vercel 59+ rewrites.
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import app

# WSGI Middleware to normalize PATH_INFO for Vercel internal rewrites
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path.startswith("/api/index.py"):
            environ["PATH_INFO"] = path[len("/api/index.py"):] or "/"
        elif path.startswith("/api/index"):
            environ["PATH_INFO"] = path[len("/api/index"):] or "/"
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
